#!/usr/bin/env python3
import argparse
import json
import subprocess
import sys
from pathlib import Path

WORKSPACE = Path(__file__).resolve().parent.parent
CREATIVE_REVIEW = WORKSPACE / 'scripts' / 'creative-review.py'
CREATIVE_LOG_SUMMARY = WORKSPACE / 'scripts' / 'creative-log-summary.py'
DEFAULT_REPORT_DIR = WORKSPACE / 'tmp' / 'creative-tooling-check' / 'reports'
CONSUMER_PRESETS = {
    'board-json': {
        'path': DEFAULT_REPORT_DIR / 'creative-smoke-consumer.json',
        'format': 'json',
        'append': False,
    },
    'board-text': {
        'path': DEFAULT_REPORT_DIR / 'creative-smoke-consumer.txt',
        'format': 'text',
        'append': False,
    },
    'eventlog-jsonl': {
        'path': DEFAULT_REPORT_DIR / 'creative-smoke-consumer.jsonl',
        'format': 'jsonl',
        'append': True,
    },
}

MODES = {
    'review-daylog': {
        'review_args': ['review-suite', '--automation-preset', 'daylog-balanced'],
        'summary_kind': 'daylog',
        'default_log_dir': DEFAULT_REPORT_DIR,
    },
    'cleanup-audit': {
        'review_args': ['weekly-cleanup', '--automation-preset', 'weekly-cleanup-logged'],
        'summary_kind': 'cleanup',
        'default_log_dir': DEFAULT_REPORT_DIR,
    },
    'full-cycle': {
        'steps': ['review-daylog', 'cleanup-audit'],
    },
    'full-cycle-brief': {
        'steps': ['review-daylog', 'cleanup-audit'],
        'brief': True,
    },
}


def run_command(cmd):
    result = subprocess.run(cmd, text=True, capture_output=True)
    return {
        'command': cmd,
        'returncode': result.returncode,
        'stdout': result.stdout,
        'stderr': result.stderr,
    }


def resolve_consumer_settings(args, *, default_format):
    output_path = args.consumer_out
    output_format = args.consumer_format or default_format
    append = args.consumer_append

    if args.consumer_preset:
        preset = CONSUMER_PRESETS[args.consumer_preset]
        output_path = str(preset['path'])
        output_format = args.consumer_format or preset['format']
        append = args.consumer_append or preset['append']

    return output_path, output_format, append


def emit_output(text=None, payload=None, *, output_format='text', output_path=None, append=False):
    if output_format == 'json':
        rendered = json.dumps(payload, ensure_ascii=False, indent=2) + '\n'
    elif output_format == 'jsonl':
        rendered = json.dumps(payload, ensure_ascii=False) + '\n'
    else:
        rendered = text if text.endswith('\n') else text + '\n'

    if output_path:
        path = Path(output_path).expanduser().resolve()
        path.parent.mkdir(parents=True, exist_ok=True)
        mode = 'a' if append else 'w'
        with path.open(mode, encoding='utf-8') as handle:
            handle.write(rendered)

    sys.stdout.write(rendered)



def build_review_command(mode, args, extra):
    review_cmd = ['python3', str(CREATIVE_REVIEW), *mode['review_args']]
    if args.report_dir:
        review_cmd.extend(['--report-dir', args.report_dir])
    if args.cleanup_log_dir:
        review_cmd.extend(['--cleanup-log-dir', args.cleanup_log_dir])
    if extra:
        review_cmd.extend(extra)
    return review_cmd



def build_summary_command(mode, args):
    summary_log_dir = args.log_dir or args.cleanup_log_dir or args.report_dir or str(mode['default_log_dir'])
    return [
        'python3',
        str(CREATIVE_LOG_SUMMARY),
        mode['summary_kind'],
        '--log-dir',
        summary_log_dir,
        '--limit',
        str(args.summary_limit),
        '--format',
        'json',
    ]



def run_smoke_mode(mode_name, args, extra):
    mode = MODES[mode_name]
    review_cmd = build_review_command(mode, args, extra)
    review_result = run_command(review_cmd)
    if review_result['returncode'] != 0:
        return {
            'mode': mode_name,
            'review_command': review_cmd,
            'review': review_result,
        }, review_result['returncode']

    summary_cmd = build_summary_command(mode, args)
    summary_result = run_command(summary_cmd)
    if summary_result['returncode'] != 0:
        return {
            'mode': mode_name,
            'review_command': review_cmd,
            'summary_command': summary_cmd,
            'review': review_result,
            'summary': summary_result,
        }, summary_result['returncode']

    return {
        'mode': mode_name,
        'review_command': review_cmd,
        'summary_command': summary_cmd,
        'review': review_result,
        'summary': json.loads(summary_result['stdout']),
    }, 0



def render_text_step(result):
    lines = []
    review_stdout = result.get('review', {}).get('stdout') or ''
    if review_stdout:
        lines.append(review_stdout.rstrip('\n'))
    summary_payload = result['summary']
    lines.append('--- smoke summary ---')
    lines.append(f"mode: {result['mode']}")
    lines.append(f"summary-kind: {summary_payload['kind']}")
    lines.append(f"event-count: {summary_payload['event_count']}")
    if summary_payload['kind'] == 'daylog':
        totals = summary_payload.get('totals') or {}
        lines.append(f"files-total: {totals.get('files_total', 0)}")
        lines.append(f"files-ok: {totals.get('files_ok', 0)}")
        lines.append(f"files-warning: {totals.get('files_warning', 0)}")
        latest = summary_payload.get('latest_event') or {}
        lines.append(f"latest-preset: {latest.get('preset')}")
        lines.append(f"latest-log: {latest.get('daylog_path')}")
    else:
        lines.append(f"candidate-total: {summary_payload.get('candidate_total', 0)}")
        lines.append(f"deleted-total: {summary_payload.get('deleted_total', 0)}")
        latest = summary_payload.get('latest_event') or {}
        lines.append(f"latest-mode: {latest.get('mode')}")
        lines.append(f"latest-log: {latest.get('cleanup_log_path')}")
    return '\n'.join(lines) + '\n'



def build_brief_payload(mode_name, step_results):
    payload = {
        'mode': mode_name,
        'ok': True,
        'steps': [],
    }
    for item in step_results:
        summary = item['summary']
        step_payload = {
            'mode': item['mode'],
            'kind': summary['kind'],
            'event_count': summary.get('event_count', 0),
        }
        if summary['kind'] == 'daylog':
            totals = summary.get('totals') or {}
            latest = summary.get('latest_event') or {}
            step_payload.update(
                {
                    'files_total': totals.get('files_total', 0),
                    'files_ok': totals.get('files_ok', 0),
                    'files_warning': totals.get('files_warning', 0),
                    'latest_profile': latest.get('preset') or latest.get('fail_profile'),
                }
            )
            payload['ok'] = payload['ok'] and totals.get('files_warning', 0) == 0
        else:
            latest = summary.get('latest_event') or {}
            step_payload.update(
                {
                    'candidate_total': summary.get('candidate_total', 0),
                    'deleted_total': summary.get('deleted_total', 0),
                    'latest_mode': latest.get('mode'),
                }
            )
        payload['steps'].append(step_payload)
    return payload



def render_text_brief(payload):
    lines = ['smoke: ok' if payload.get('ok') else 'smoke: warning']
    for step in payload.get('steps', []):
        if step['kind'] == 'daylog':
            lines.append(
                f"- {step['mode']}: events={step['event_count']} files={step['files_total']} ok={step['files_ok']} warnings={step['files_warning']} latest={step.get('latest_profile')}"
            )
        else:
            lines.append(
                f"- {step['mode']}: events={step['event_count']} candidates={step['candidate_total']} deleted={step['deleted_total']} latest={step.get('latest_mode')}"
            )
    return '\n'.join(lines) + '\n'



def main():
    parser = argparse.ArgumentParser(description='Kleine smoke-testwrapper voor creative review/daylog en cleanup plus logsamenvatting.')
    parser.add_argument('mode', choices=sorted(MODES), help='Welke vaste smoke-route je wilt draaien')
    parser.add_argument('--format', choices=['text', 'json'], default='text', help='Outputformaat van de wrapper')
    parser.add_argument('--log-dir', help='Overschrijf de logmap voor de samenvatting')
    parser.add_argument('--report-dir', help='Geef een alternatieve reports-map door aan creative-review')
    parser.add_argument('--cleanup-log-dir', help='Geef een alternatieve cleanup-logmap door aan creative-review')
    parser.add_argument('--summary-limit', type=int, default=1, help='Beperk de logsamenvatting tot de laatste N logbestanden')
    parser.add_argument('--consumer-out', help='Schrijf de uiteindelijke smoke-uitvoer ook weg naar een bestand voor cron/board-consumers')
    parser.add_argument('--consumer-preset', choices=sorted(CONSUMER_PRESETS), help='Gebruik een vaste producer/consumer-route voor veelgebruikte consumer-artifacts')
    parser.add_argument('--consumer-format', choices=['text', 'json', 'jsonl'], help='Outputformaat voor --consumer-out; default volgt --format, behalve text bij niet-JSON stdout')
    parser.add_argument('--consumer-append', action='store_true', help='Append naar bestaand consumer-bestand in plaats van overschrijven')
    args, extra = parser.parse_known_args()

    if extra and extra[0] == '--':
        extra = extra[1:]

    mode = MODES[args.mode]
    if 'steps' in mode:
        step_results = []
        for step_name in mode['steps']:
            result, exit_code = run_smoke_mode(step_name, args, extra)
            if exit_code != 0:
                if args.format == 'json':
                    print(json.dumps({'mode': args.mode, 'failed_step': step_name, 'steps': step_results, 'error': result}, ensure_ascii=False, indent=2))
                else:
                    for done in step_results:
                        render_text_step(done)
                        print()
                    review_stdout = result.get('review', {}).get('stdout') or ''
                    review_stderr = result.get('review', {}).get('stderr') or ''
                    summary_stderr = result.get('summary', {}).get('stderr') or ''
                    if review_stdout:
                        sys.stdout.write(review_stdout)
                    if review_stderr:
                        sys.stderr.write(review_stderr)
                    if summary_stderr:
                        sys.stderr.write(summary_stderr)
                raise SystemExit(exit_code)
            step_results.append(result)

        if mode.get('brief'):
            payload = build_brief_payload(args.mode, step_results)
            default_consumer_format = args.format if args.format == 'json' else 'text'
            consumer_output_path, consumer_output_format, consumer_append = resolve_consumer_settings(
                args,
                default_format=default_consumer_format,
            )
            if args.format == 'json':
                emit_output(payload=payload, output_format='json', output_path=consumer_output_path, append=consumer_append)
                return
            emit_output(
                text=render_text_brief(payload),
                payload=payload,
                output_format=consumer_output_format,
                output_path=consumer_output_path,
                append=consumer_append,
            )
            return

        payload = {
            'mode': args.mode,
            'steps': [
                {
                    'mode': item['mode'],
                    'review_command': item['review_command'],
                    'summary_command': item['summary_command'],
                    'summary': item['summary'],
                }
                for item in step_results
            ],
        }
        consumer_output_path, consumer_output_format, consumer_append = resolve_consumer_settings(
            args,
            default_format=args.format if args.format == 'json' else 'text',
        )
        if args.format == 'json':
            emit_output(payload=payload, output_format='json', output_path=consumer_output_path, append=consumer_append)
            return
        text = '\n'.join(render_text_step(item).rstrip('\n') for item in step_results) + '\n'
        emit_output(
            text=text,
            payload=payload,
            output_format=consumer_output_format,
            output_path=consumer_output_path,
            append=consumer_append,
        )
        return

    result, exit_code = run_smoke_mode(args.mode, args, extra)
    if exit_code != 0:
        if args.format == 'json':
            print(json.dumps(result, ensure_ascii=False, indent=2))
        else:
            review_stdout = result.get('review', {}).get('stdout') or ''
            review_stderr = result.get('review', {}).get('stderr') or ''
            summary_stderr = result.get('summary', {}).get('stderr') or ''
            if review_stdout:
                sys.stdout.write(review_stdout)
            if review_stderr:
                sys.stderr.write(review_stderr)
            if summary_stderr:
                sys.stderr.write(summary_stderr)
        raise SystemExit(exit_code)

    payload = {
        'mode': args.mode,
        'review_command': result['review_command'],
        'summary_command': result['summary_command'],
        'summary': result['summary'],
    }

    consumer_output_path, consumer_output_format, consumer_append = resolve_consumer_settings(
        args,
        default_format=args.format if args.format == 'json' else 'text',
    )
    if args.format == 'json':
        emit_output(payload=payload, output_format='json', output_path=consumer_output_path, append=consumer_append)
        return

    emit_output(
        text=render_text_step(result),
        payload=payload,
        output_format=consumer_output_format,
        output_path=consumer_output_path,
        append=consumer_append,
    )


if __name__ == '__main__':
    main()
