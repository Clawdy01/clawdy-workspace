#!/usr/bin/env python3
import argparse
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path('/home/clawdy/.openclaw/workspace')
STATUS_SCRIPT = ROOT / 'scripts' / 'ai-briefing-status.py'


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


def load_status(timeout_seconds: int) -> dict:
    proc = subprocess.run(
        ['python3', str(STATUS_SCRIPT), '--json'],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=False,
        timeout=timeout_seconds,
    )
    if proc.returncode != 0:
        raise SystemExit(proc.stderr.strip() or proc.stdout.strip() or f'ai-briefing-status failed: {proc.returncode}')
    return extract_json_document(proc.stdout)


def evaluate(status: dict) -> tuple[bool, list[str], str]:
    reasons: list[str] = []

    if not status.get('ok'):
        reasons.append('status not ok')
    if not status.get('found'):
        reasons.append('job niet gevonden')
    if not status.get('enabled'):
        reasons.append('job staat uit')

    for key in ('payload_audit', 'runtime_audit', 'next_run_audit', 'storage_audit', 'runlog_audit', 'uniqueness_audit', 'proof_freshness'):
        audit = status.get(key) or {}
        if audit and not audit.get('ok', False):
            reasons.append(audit.get('text') or key)

    if status.get('attention_needed'):
        reasons.append(status.get('attention_text') or 'attention nodig')

    readiness_phase = status.get('readiness_phase')
    if readiness_phase == 'ready-for-first-run':
        summary = status.get('text') or 'klaar voor eerste run'
    elif status.get('has_run_proof'):
        summary = status.get('text') or 'runbewijs aanwezig'
    else:
        summary = status.get('text') or 'geen runbewijs'

    return (len(reasons) == 0, reasons, summary)


def main() -> int:
    parser = argparse.ArgumentParser(description='Controleer of de dagelijkse AI-briefing gezond en bewijsbaar is.')
    parser.add_argument('--json', action='store_true', help='print resultaat als JSON')
    parser.add_argument('--timeout', type=int, default=120, help='timeout in seconden voor ai-briefing-status.py')
    args = parser.parse_args()

    status = load_status(args.timeout)
    ok, reasons, summary = evaluate(status)
    result = {
        'ok': ok,
        'summary': summary,
        'reasons': reasons,
        'readiness_phase': status.get('readiness_phase'),
        'proof_progress_text': status.get('proof_progress_text'),
        'proof_target_runs': status.get('proof_target_runs'),
        'proof_qualified_runs': status.get('proof_qualified_runs'),
        'job_name': status.get('job_name'),
        'next_run_at_text': status.get('next_run_at_text'),
        'proof_due_at_text': status.get('proof_due_at_text'),
        'has_run_proof': status.get('has_run_proof'),
        'attention_needed': status.get('attention_needed'),
        'status_text': status.get('text'),
    }

    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        state = 'ok' if ok else 'attention'
        print(f"ai briefing watchdog: {state} - {summary}")
        if reasons:
            print('reasons:')
            for reason in reasons:
                print(f'- {reason}')
        if result['proof_progress_text']:
            print(f"proof progress: {result['proof_progress_text']}")
        if result['next_run_at_text']:
            print(f"next run: {result['next_run_at_text']}")
        if result['proof_due_at_text']:
            print(f"proof due: {result['proof_due_at_text']}")

    return 0 if ok else 2


if __name__ == '__main__':
    raise SystemExit(main())
