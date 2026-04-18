#!/usr/bin/env python3
import argparse
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path('/home/clawdy/.openclaw/workspace')
STATUS = ROOT / 'scripts' / 'ai-briefing-status.py'
WATCHDOG = ROOT / 'scripts' / 'ai-briefing-watchdog.py'
DEFAULT_REPORT_DIR = ROOT / 'tmp' / 'ai-briefing' / 'reports'

CONSUMER_PRESETS = {
    'board-json': {
        'path': DEFAULT_REPORT_DIR / 'ai-briefing-proof-recheck.json',
        'format': 'json',
        'append': False,
    },
    'board-text': {
        'path': DEFAULT_REPORT_DIR / 'ai-briefing-proof-recheck.txt',
        'format': 'text',
        'append': False,
    },
    'eventlog-jsonl': {
        'path': DEFAULT_REPORT_DIR / 'ai-briefing-proof-recheck.jsonl',
        'format': 'jsonl',
        'append': True,
    },
}
CONSUMER_BUNDLES = {
    'board-pair': ['board-json', 'board-text'],
    'board-suite': ['board-json', 'board-text', 'eventlog-jsonl'],
}


def extract_json_document(text: str):
    text = (text or '').strip()
    if not text:
        raise json.JSONDecodeError('Expecting value', text, 0)
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        pass

    lines = text.splitlines()
    for index, line in enumerate(lines):
        stripped = line.lstrip()
        if not stripped.startswith(('{', '[')):
            continue
        candidate = '\n'.join(lines[index:]).strip()
        try:
            return json.loads(candidate)
        except json.JSONDecodeError:
            continue
    raise json.JSONDecodeError('Expecting value', text, 0)


def run_json(cmd: list[str]) -> tuple[int, dict]:
    proc = subprocess.run(cmd, cwd=ROOT, capture_output=True, text=True, check=False)
    output = proc.stdout.strip() or proc.stderr.strip()
    if not output:
        raise RuntimeError(f'geen output van: {" ".join(cmd)}')
    return proc.returncode, extract_json_document(output)


def first_non_null(*values):
    for value in values:
        if value is not None:
            return value
    return None


def build_payload(status_data: dict, watchdog_data: dict) -> dict:
    recheck_window_open = bool(status_data.get('proof_recheck_window_open'))
    proof_target_met = bool(watchdog_data.get('proof_target_met'))
    watchdog_ok = bool(watchdog_data.get('ok'))
    status_ok = bool(status_data.get('ok'))
    summary_output_examples = watchdog_data.get('summary_output_examples') or []

    state = 'waiting'
    exit_code = 2
    result_kind = 'too-early'
    result_text = 'hercheck nog te vroeg, wacht op kwalificatierun en hercheckvenster'
    if recheck_window_open and not watchdog_ok:
        state = 'attention'
        exit_code = 3
        result_kind = 'attention-needed'
        result_text = 'hercheckvenster is open, maar bewijsdoel is nog niet gehaald'
    if proof_target_met and watchdog_ok:
        state = 'ok'
        exit_code = 0
        result_kind = 'proof-target-met'
        result_text = 'hercheck bevestigt dat het bewijsdoel gehaald is'

    summary_bits = [
        status_data.get('summary') or status_data.get('status_text'),
        watchdog_data.get('proof_progress_text'),
        status_data.get('proof_next_action_window_text') or status_data.get('proof_next_action_text'),
    ]
    summary = ' | '.join(bit for bit in summary_bits if bit)

    return {
        'ok': proof_target_met and watchdog_ok,
        'state': state,
        'exit_code': exit_code,
        'result_kind': result_kind,
        'result_text': result_text,
        'summary': summary,
        'reference_now_text': first_non_null(status_data.get('reference_now_text'), watchdog_data.get('reference_now_text')),
        'reference_context_text': first_non_null(status_data.get('reference_context_text'), watchdog_data.get('reference_context_text')),
        'proof_state': first_non_null(status_data.get('proof_state'), watchdog_data.get('proof_state')),
        'proof_state_text': first_non_null(status_data.get('proof_state_text'), watchdog_data.get('proof_state_text')),
        'proof_progress_text': first_non_null(watchdog_data.get('proof_progress_text'), status_data.get('proof_progress_text')),
        'proof_target_met': proof_target_met,
        'proof_recheck_ready': recheck_window_open,
        'proof_runs_remaining': watchdog_data.get('proof_runs_remaining'),
        'proof_recheck_window_open': recheck_window_open,
        'proof_recheck_window_text': status_data.get('proof_recheck_window_text'),
        'proof_recheck_after_text': first_non_null(status_data.get('proof_recheck_after_text'), watchdog_data.get('proof_recheck_after_text')),
        'proof_recheck_after_hint': first_non_null(status_data.get('proof_recheck_after_hint'), watchdog_data.get('proof_recheck_after_hint')),
        'proof_recheck_after_remaining_ms': first_non_null(status_data.get('proof_recheck_after_remaining_ms'), watchdog_data.get('proof_recheck_after_remaining_ms')),
        'proof_next_action_kind': first_non_null(status_data.get('proof_next_action_kind'), watchdog_data.get('proof_next_action_kind')),
        'proof_next_action_text': first_non_null(status_data.get('proof_next_action_text'), watchdog_data.get('proof_next_action_text')),
        'proof_next_action_window_text': first_non_null(status_data.get('proof_next_action_window_text'), watchdog_data.get('proof_next_action_window_text')),
        'proof_recheck_commands': status_data.get('proof_recheck_commands') or watchdog_data.get('proof_recheck_commands') or [],
        'proof_recheck_commands_text': first_non_null(status_data.get('proof_recheck_commands_text'), watchdog_data.get('proof_recheck_commands_text')),
        'proof_blocker_kind': first_non_null(status_data.get('proof_blocker_kind'), watchdog_data.get('proof_blocker_kind')),
        'proof_blocker_text': first_non_null(status_data.get('proof_blocker_text'), watchdog_data.get('proof_blocker_text')),
        'proof_freshness_text': first_non_null((status_data.get('proof_freshness') or {}).get('text'), watchdog_data.get('proof_freshness_text')),
        'summary_output_examples': summary_output_examples,
        'proof_countdown_text': first_non_null(status_data.get('proof_countdown_text'), watchdog_data.get('proof_countdown_text')),
        'proof_schedule_risk_text': first_non_null(status_data.get('proof_schedule_risk_text'), watchdog_data.get('proof_schedule_risk_text')),
        'proof_target_due_at_text': first_non_null(status_data.get('proof_target_due_at_text'), watchdog_data.get('proof_target_due_at_text')),
        'proof_target_due_at_if_next_slot_missed_text': first_non_null(status_data.get('proof_target_due_at_if_next_slot_missed_text'), watchdog_data.get('proof_target_due_at_if_next_slot_missed_text')),
        'proof_config_identity_text': first_non_null(status_data.get('proof_config_identity_text'), watchdog_data.get('proof_config_identity_text')),
        'last_run_config_relation_text': first_non_null(status_data.get('last_run_config_relation_text'), watchdog_data.get('last_run_config_relation_text')),
        'status_ok': status_ok,
        'status_returncode': status_data.get('_returncode'),
        'watchdog_ok': watchdog_ok,
        'watchdog_returncode': watchdog_data.get('_returncode'),
    }


def build_text(payload: dict) -> str:
    summary_output_examples = payload.get('summary_output_examples') or []
    bits = [
        f"AI-briefing proof-recheck: {payload.get('summary')}",
        payload.get('result_text'),
        payload.get('reference_context_text'),
        payload.get('proof_state_text'),
        payload.get('proof_blocker_text'),
        payload.get('proof_freshness_text'),
        ('outputvoorbeelden: ' + '; '.join(summary_output_examples[:2])) if summary_output_examples else None,
        payload.get('proof_recheck_window_text'),
        payload.get('proof_schedule_risk_text'),
        payload.get('proof_countdown_text'),
        payload.get('proof_recheck_commands_text'),
    ]
    unique_bits: list[str] = []
    for bit in bits:
        cleaned = ' '.join((bit or '').split())
        if not cleaned or cleaned in unique_bits:
            continue
        unique_bits.append(cleaned)
    return ' | '.join(unique_bits)


def resolve_consumer_settings(args, *, default_format: str):
    output_path = args.consumer_out
    output_format = args.consumer_format or default_format
    append = args.consumer_append

    if args.consumer_preset:
        preset = CONSUMER_PRESETS[args.consumer_preset]
        output_path = str(preset['path'])
        output_format = args.consumer_format or preset['format']
        append = args.consumer_append or preset['append']

    return output_path, output_format, append


def render_output(*, text: str, payload: dict, output_format: str) -> str:
    if output_format == 'json':
        return json.dumps(payload, ensure_ascii=False, indent=2) + '\n'
    if output_format == 'jsonl':
        return json.dumps(payload, ensure_ascii=False) + '\n'
    return text if text.endswith('\n') else text + '\n'


def write_output(rendered: str, *, output_path: str | None = None, append: bool = False) -> None:
    if not output_path:
        return
    path = Path(output_path).expanduser().resolve()
    path.parent.mkdir(parents=True, exist_ok=True)
    mode = 'a' if append else 'w'
    with path.open(mode, encoding='utf-8') as handle:
        handle.write(rendered)


def emit_output(*, text: str, payload: dict, output_format: str, output_path: str | None = None, append: bool = False) -> None:
    rendered = render_output(text=text, payload=payload, output_format=output_format)
    write_output(rendered, output_path=output_path, append=append)
    sys.stdout.write(rendered)


def emit_output_with_bundle(*, text: str, payload: dict, stdout_format: str, stdout_output_path: str | None = None, stdout_append: bool = False, consumer_bundle: str | None = None) -> None:
    emit_output(
        text=text,
        payload=payload,
        output_format=stdout_format,
        output_path=stdout_output_path,
        append=stdout_append,
    )
    if not consumer_bundle:
        return
    for preset_name in CONSUMER_BUNDLES[consumer_bundle]:
        preset = CONSUMER_PRESETS[preset_name]
        rendered = render_output(text=text, payload=payload, output_format=preset['format'])
        write_output(rendered, output_path=str(preset['path']), append=preset['append'])


def main() -> int:
    parser = argparse.ArgumentParser(description='Draai de AI-briefing status + watchdog hercheck in één commando.')
    parser.add_argument('--json', action='store_true', help='geef machinevriendelijke JSON terug')
    parser.add_argument('--reference-ms', type=int, help='gebruik deze epoch-millis als referentietijd voor deterministische herchecks')
    parser.add_argument('--consumer-out', help='Schrijf de proof-recheck-uitvoer ook naar een bestand voor cron/board-consumers')
    parser.add_argument('--consumer-preset', choices=sorted(CONSUMER_PRESETS), help='Gebruik een vaste consumer-outputroute')
    parser.add_argument('--consumer-bundle', choices=sorted(CONSUMER_BUNDLES), help='Schrijf dezelfde proof-recheck-status naar meerdere standaard consumerbestanden')
    parser.add_argument('--consumer-format', choices=['text', 'json', 'jsonl'], help='Outputformaat voor --consumer-out; default volgt stdout-formaat')
    parser.add_argument('--consumer-append', action='store_true', help='Append naar bestaand consumer-bestand in plaats van overschrijven')
    args = parser.parse_args()

    status_cmd = ['python3', str(STATUS), '--json']
    watchdog_cmd = ['python3', str(WATCHDOG), '--json', '--require-qualified-runs', '3']
    if args.reference_ms is not None:
        status_cmd.extend(['--reference-ms', str(args.reference_ms)])
        watchdog_cmd.extend(['--reference-ms', str(args.reference_ms)])

    status_returncode, status_data = run_json(status_cmd)
    status_data['_returncode'] = status_returncode
    watchdog_returncode, watchdog_data = run_json(watchdog_cmd)
    watchdog_data['_returncode'] = watchdog_returncode

    payload = build_payload(status_data, watchdog_data)
    text_output = build_text(payload)
    stdout_format = 'json' if args.json else 'text'
    consumer_output_path, consumer_output_format, consumer_append = resolve_consumer_settings(
        args,
        default_format=stdout_format,
    )
    emit_output_with_bundle(
        text=text_output,
        payload=payload,
        stdout_format=consumer_output_format,
        stdout_output_path=consumer_output_path,
        stdout_append=consumer_append,
        consumer_bundle=args.consumer_bundle,
    )
    return int(payload['exit_code'])


if __name__ == '__main__':
    raise SystemExit(main())
