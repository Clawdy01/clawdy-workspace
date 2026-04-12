#!/usr/bin/env python3
import argparse
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

WORKSPACE = Path(__file__).resolve().parent.parent
MEDIA_SANITY = WORKSPACE / 'scripts' / 'media-sanity-check.py'
DEFAULT_REPORT_DIR = WORKSPACE / 'tmp' / 'creative-tooling-check' / 'reports'

MODES = {
    'mixed-review': {
        'kind': 'preset',
        'profile': 'creative-mixed-review',
        'default_format': 'text',
    },
    'audio-review': {
        'kind': 'preset',
        'profile': 'creative-audio-review',
        'default_format': 'text',
    },
    'helper-frames-review': {
        'kind': 'preset',
        'profile': 'creative-helper-frames-review',
        'default_format': 'json',
    },
    'helper-clips-review': {
        'kind': 'preset',
        'profile': 'creative-helper-clips-review',
        'default_format': 'text',
    },
    'mixed-strict': {
        'kind': 'fail_profile',
        'profile': 'creative-mixed-strict',
        'default_format': 'jsonl',
        'summary_only': True,
    },
    'audio-strict': {
        'kind': 'fail_profile',
        'profile': 'creative-audio-strict',
        'default_format': 'json',
    },
    'helper-frames-strict': {
        'kind': 'fail_profile',
        'profile': 'creative-helper-frames-strict',
        'default_format': 'jsonl',
        'summary_only': True,
    },
    'helper-clips-strict': {
        'kind': 'fail_profile',
        'profile': 'creative-helper-clips-strict',
        'default_format': 'jsonl',
        'summary_only': True,
    },
}

SUITES = {
    'review-suite': [
        'mixed-review',
        'audio-review',
        'helper-frames-review',
        'helper-clips-review',
    ],
    'strict-suite': [
        'mixed-strict',
        'audio-strict',
        'helper-frames-strict',
        'helper-clips-strict',
    ],
}


def slugify(name: str) -> str:
    return name.replace('_', '-').replace(' ', '-').lower()



def utc_day_stamp() -> str:
    return datetime.now(timezone.utc).strftime('%Y%m%d')



def build_command(mode_name, args):
    mode = MODES[mode_name]
    cmd = ['python3', str(MEDIA_SANITY)]
    flag = '--preset' if mode['kind'] == 'preset' else '--fail-profile'
    cmd.extend([flag, mode['profile']])

    output_format = args.format or mode['default_format']
    if output_format == 'json':
        cmd.append('--json')
    elif output_format == 'jsonl':
        cmd.append('--jsonl')
        if args.summary_only or mode.get('summary_only'):
            cmd.append('--jsonl-summary-only')

    if args.report or args.daylog:
        if args.daylog:
            report_dir = Path(args.daylog_dir).expanduser().resolve() if args.daylog_dir else DEFAULT_REPORT_DIR
            report_path = report_dir / f"creative-review-daylog-{utc_day_stamp()}.jsonl"
            cmd.extend(['--report-out', str(report_path), '--report-format', 'jsonl', '--report-append', '--report-summary-only'])
        else:
            report_dir = Path(args.report_dir).expanduser().resolve() if args.report_dir else DEFAULT_REPORT_DIR
            suffix = '.jsonl' if output_format == 'jsonl' else '.json' if output_format == 'json' else '.txt'
            report_path = report_dir / f"creative-review-{slugify(mode_name)}{suffix}"
            cmd.extend(['--report-out', str(report_path), '--report-format', output_format])
            if args.timestamped:
                cmd.append('--report-timestamped')
            if args.append:
                cmd.append('--report-append')
            if args.summary_only or mode.get('summary_only'):
                cmd.append('--report-summary-only')

    if args.extra:
        cmd.extend(args.extra)
    return cmd



def main():
    parser = argparse.ArgumentParser(description='Kleine wrapper rond media-sanity-check voor vaste creative review- en strict-routes.')
    parser.add_argument('mode', choices=sorted(list(MODES) + list(SUITES)), help='Welke vaste review-, strict- of suite-route je wilt draaien')
    parser.add_argument('--format', choices=['text', 'json', 'jsonl'], help='Forceer stdout-formaat; default hangt af van mode')
    parser.add_argument('--summary-only', action='store_true', help='Gebruik compacte summary-only output waar relevant')
    parser.add_argument('--report', action='store_true', help='Schrijf ook een rapportartifact weg in de creative reports-map')
    parser.add_argument('--report-dir', help='Overschrijf de standaard rapportmap')
    parser.add_argument('--timestamped', action='store_true', help='Maak timestamped rapportbestanden bij --report')
    parser.add_argument('--append', action='store_true', help='Append naar bestaand rapportbestand bij --report')
    parser.add_argument('--daylog', action='store_true', help='Append compacte JSONL summary-events aan één daglogbestand per UTC-dag')
    parser.add_argument('--daylog-dir', help='Overschrijf de standaard map voor daglog-artifacts')
    args, extra = parser.parse_known_args()

    if args.daylog and (args.timestamped or args.append or args.report_dir):
        parser.error('--daylog gebruikt zijn eigen append-daglog; combineer niet met --timestamped, --append of --report-dir')

    if extra and extra[0] == '--':
        extra = extra[1:]
    args.extra = extra

    modes = SUITES.get(args.mode, [args.mode])
    exit_code = 0
    for index, mode_name in enumerate(modes):
        if len(modes) > 1:
            if index > 0:
                print()
            print(f'== {mode_name} ==', file=sys.stderr)
        cmd = build_command(mode_name, args)
        result = subprocess.run(cmd)
        if result.returncode != 0 and exit_code == 0:
            exit_code = result.returncode
    raise SystemExit(exit_code)


if __name__ == '__main__':
    main()
