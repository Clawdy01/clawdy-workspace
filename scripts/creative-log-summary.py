#!/usr/bin/env python3
import argparse
import json
from collections import Counter, defaultdict
from pathlib import Path

WORKSPACE = Path(__file__).resolve().parent.parent
DEFAULT_REPORT_DIR = WORKSPACE / 'tmp' / 'creative-tooling-check' / 'reports'

LOG_PATTERNS = {
    'cleanup': 'creative-review-cleanup-log-*.jsonl',
    'daylog': 'creative-review-daylog-*.jsonl',
}


def iter_events(paths):
    for path in paths:
        with path.open('r', encoding='utf-8') as handle:
            for line_no, line in enumerate(handle, start=1):
                raw = line.strip()
                if not raw:
                    continue
                payload = json.loads(raw)
                payload['_path'] = str(path)
                payload['_line'] = line_no
                yield payload


def summarize_cleanup(events):
    events = list(events)
    artifact_counts = Counter()
    candidate_total = 0
    deleted_total = 0
    modes = Counter()
    latest = None
    for event in events:
        modes[event.get('mode') or 'unknown'] += 1
        candidate_total += int(event.get('candidate_count') or 0)
        deleted_total += int(event.get('deleted_count') or 0)
        for candidate in event.get('candidates') or []:
            artifact_counts[candidate.get('artifact_kind') or 'unknown'] += 1
        if latest is None or (event.get('generated_at') or '') > (latest.get('generated_at') or ''):
            latest = event
    return {
        'kind': 'cleanup',
        'event_count': len(events),
        'modes': dict(sorted(modes.items())),
        'candidate_total': candidate_total,
        'deleted_total': deleted_total,
        'candidate_artifacts': dict(sorted(artifact_counts.items())),
        'latest_event': None if latest is None else {
            'generated_at': latest.get('generated_at'),
            'mode': latest.get('mode'),
            'candidate_count': latest.get('candidate_count'),
            'deleted_count': latest.get('deleted_count', 0),
            'report_dir': latest.get('report_dir'),
            'cleanup_log_path': latest.get('_path'),
        },
    }


def summarize_daylog(events):
    events = list(events)
    presets = Counter()
    exit_codes = Counter()
    totals = Counter()
    summary_by_kind = defaultdict(lambda: Counter())
    latest = None
    for event in events:
        presets[event.get('preset') or event.get('fail_profile') or 'unknown'] += 1
        exit_codes[str(event.get('exit_code', 'unknown'))] += 1
        summary = event.get('summary') or {}
        totals['files_total'] += int(summary.get('total') or 0)
        totals['files_ok'] += int(summary.get('ok_count') or 0)
        totals['files_warning'] += int(summary.get('warning_count') or 0)
        for kind, kind_summary in (event.get('summary_by_kind') or {}).items():
            summary_by_kind[kind]['total'] += int(kind_summary.get('total') or 0)
            summary_by_kind[kind]['ok_count'] += int(kind_summary.get('ok_count') or 0)
            summary_by_kind[kind]['warning_count'] += int(kind_summary.get('warning_count') or 0)
        if latest is None or (event.get('generated_at') or '') > (latest.get('generated_at') or ''):
            latest = event
    return {
        'kind': 'daylog',
        'event_count': len(events),
        'profiles': dict(sorted(presets.items())),
        'exit_codes': dict(sorted(exit_codes.items())),
        'totals': dict(totals),
        'summary_by_kind': {kind: dict(values) for kind, values in sorted(summary_by_kind.items())},
        'latest_event': None if latest is None else {
            'generated_at': latest.get('generated_at'),
            'preset': latest.get('preset'),
            'fail_profile': latest.get('fail_profile'),
            'directory': latest.get('directory'),
            'daylog_path': latest.get('_path'),
        },
    }


def render_text(summary):
    print(f"kind: {summary['kind']}")
    print(f"event-count: {summary['event_count']}")
    latest = summary.get('latest_event')
    if summary['kind'] == 'cleanup':
        print(f"candidate-total: {summary['candidate_total']}")
        print(f"deleted-total: {summary['deleted_total']}")
        if summary['modes']:
            print('modes:')
            for mode, count in summary['modes'].items():
                print(f"- {mode}: {count}")
        if summary['candidate_artifacts']:
            print('candidate-artifacts:')
            for kind, count in summary['candidate_artifacts'].items():
                print(f"- {kind}: {count}")
        if latest:
            print('latest-event:')
            print(f"- generated_at: {latest['generated_at']}")
            print(f"- mode: {latest['mode']}")
            print(f"- candidate_count: {latest['candidate_count']}")
            print(f"- deleted_count: {latest['deleted_count']}")
            print(f"- report_dir: {latest['report_dir']}")
            print(f"- log_path: {latest['cleanup_log_path']}")
    else:
        if summary['profiles']:
            print('profiles:')
            for profile, count in summary['profiles'].items():
                print(f"- {profile}: {count}")
        if summary['exit_codes']:
            print('exit-codes:')
            for code, count in summary['exit_codes'].items():
                print(f"- {code}: {count}")
        if summary['totals']:
            print('totals:')
            print(f"- files_total: {summary['totals'].get('files_total', 0)}")
            print(f"- files_ok: {summary['totals'].get('files_ok', 0)}")
            print(f"- files_warning: {summary['totals'].get('files_warning', 0)}")
        if summary['summary_by_kind']:
            print('summary-by-kind:')
            for kind, values in summary['summary_by_kind'].items():
                print(
                    f"- {kind}: total={values.get('total', 0)} ok={values.get('ok_count', 0)} warnings={values.get('warning_count', 0)}"
                )
        if latest:
            print('latest-event:')
            print(f"- generated_at: {latest['generated_at']}")
            print(f"- preset: {latest['preset']}")
            print(f"- fail_profile: {latest['fail_profile']}")
            print(f"- directory: {latest['directory']}")
            print(f"- log_path: {latest['daylog_path']}")


def main():
    parser = argparse.ArgumentParser(description='Vat creative cleanup-logs of daylogs samen.')
    parser.add_argument('kind', choices=sorted(LOG_PATTERNS), help='Welk logtype samengevat moet worden')
    parser.add_argument('--log-dir', default=str(DEFAULT_REPORT_DIR), help='Map met JSONL logs')
    parser.add_argument('--format', choices=['text', 'json'], default='text', help='Outputformaat')
    parser.add_argument('--limit', type=int, help='Beperk tot de laatste N logbestanden')
    args = parser.parse_args()

    log_dir = Path(args.log_dir).expanduser().resolve()
    paths = sorted(log_dir.glob(LOG_PATTERNS[args.kind]))
    if args.limit:
        paths = paths[-args.limit:]
    if not paths:
        raise SystemExit(f'Geen {args.kind}-logs gevonden in {log_dir}')

    events = list(iter_events(paths))
    summary = summarize_cleanup(events) if args.kind == 'cleanup' else summarize_daylog(events)
    summary['log_dir'] = str(log_dir)
    summary['files'] = [str(path) for path in paths]

    if args.format == 'json':
        print(json.dumps(summary, ensure_ascii=False, indent=2))
    else:
        render_text(summary)


if __name__ == '__main__':
    main()
