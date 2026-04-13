#!/usr/bin/env python3
import argparse
import json
import subprocess
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

WORKSPACE = Path(__file__).resolve().parent.parent
MEDIA_SANITY = WORKSPACE / 'scripts' / 'media-sanity-check.py'
DEFAULT_REPORT_DIR = WORKSPACE / 'tmp' / 'creative-tooling-check' / 'reports'

CLEANUP_PRESETS = {
    'balanced': {
        'prune_report_older_than_days': 7,
        'prune_daylog_older_than_days': 14,
    },
    'short-reports': {
        'prune_report_older_than_days': 2,
        'prune_daylog_older_than_days': 7,
    },
    'ci-tight': {
        'prune_report_older_than_days': 1,
        'prune_daylog_older_than_days': 3,
    },
}

AUTOMATION_PRESETS = {
    'daylog-balanced': {
        'daylog': True,
        'prune_after_write': True,
        'cleanup_preset': 'balanced',
    },
    'timestamped-short': {
        'report': True,
        'timestamped': True,
        'prune_after_write': True,
        'cleanup_preset': 'short-reports',
    },
    'timestamped-ci': {
        'report': True,
        'timestamped': True,
        'prune_after_write': True,
        'cleanup_preset': 'ci-tight',
    },
}

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



def list_prune_candidates(base_dir: Path, older_than_days: int, *, report_older_than_days: int | None = None, daylog_older_than_days: int | None = None):
    now = datetime.now(timezone.utc)
    retention_days = {
        'report': older_than_days if report_older_than_days is None else report_older_than_days,
        'daylog': older_than_days if daylog_older_than_days is None else daylog_older_than_days,
    }
    pattern_groups = {
        'report': [
            'creative-review-*.jsonl',
            'creative-review-*.json',
            'creative-review-*.txt',
        ],
        'daylog': [
            'creative-review-daylog-*.jsonl',
        ],
    }
    seen = set()
    candidates = []
    for artifact_kind, patterns in pattern_groups.items():
        cutoff = now - timedelta(days=retention_days[artifact_kind])
        for pattern in patterns:
            for path in sorted(base_dir.glob(pattern)):
                if artifact_kind == 'report' and path.name.startswith('creative-review-daylog-'):
                    continue
                resolved = path.resolve()
                if resolved in seen or not path.is_file():
                    continue
                seen.add(resolved)
                modified_at = datetime.fromtimestamp(path.stat().st_mtime, tz=timezone.utc)
                if modified_at < cutoff:
                    candidates.append({
                        'path': str(path),
                        'artifact_kind': artifact_kind,
                        'retain_days': retention_days[artifact_kind],
                        'modified_at': modified_at.isoformat(),
                        'age_days': round((now - modified_at).total_seconds() / 86400, 2),
                    })
    return candidates



def resolve_prune_base_dir(args):
    if args.daylog:
        base_dir = args.daylog_dir
    else:
        base_dir = args.report_dir or args.daylog_dir
    return Path(base_dir).expanduser().resolve() if base_dir else DEFAULT_REPORT_DIR



def render_prune_payload(payload, output_format):
    if output_format == 'jsonl':
        print(json.dumps(payload, ensure_ascii=False))
    elif output_format == 'json':
        print(json.dumps(payload, ensure_ascii=False, indent=2))
    else:
        print(f"creative-review prune report-dir: {payload['report_dir']}")
        print(f"older-than-days: {payload['older_than_days']}")
        print(f"apply: {'yes' if payload['apply'] else 'no'}")
        print(f"candidate-count: {payload['candidate_count']}")
        if 'deleted_count' in payload:
            print(f"deleted-count: {payload['deleted_count']}")
        if 'retention_days' in payload:
            print(
                'retention-days: '
                f"reports={payload['retention_days']['report']}, "
                f"daylogs={payload['retention_days']['daylog']}"
            )
        for item in payload['candidates']:
            print(
                f"- {item['path']} "
                f"(kind={item['artifact_kind']}, retain_days={item['retain_days']}, "
                f"modified_at={item['modified_at']}, age_days={item['age_days']})"
            )



def apply_automation_preset(args):
    if not args.automation_preset:
        return args
    preset = AUTOMATION_PRESETS[args.automation_preset]
    for field, value in preset.items():
        current = getattr(args, field)
        if current in (None, False):
            setattr(args, field, value)
    return args



def apply_cleanup_preset(args):
    if not args.cleanup_preset:
        return args
    preset = CLEANUP_PRESETS[args.cleanup_preset]
    if args.prune_report_older_than_days is None:
        args.prune_report_older_than_days = preset['prune_report_older_than_days']
    if args.prune_daylog_older_than_days is None:
        args.prune_daylog_older_than_days = preset['prune_daylog_older_than_days']
    return args



def run_prune(args, *, emit=True):
    base_dir = resolve_prune_base_dir(args)
    base_dir.mkdir(parents=True, exist_ok=True)
    report_older_than_days = args.prune_report_older_than_days
    daylog_older_than_days = args.prune_daylog_older_than_days
    candidates = list_prune_candidates(
        base_dir,
        args.prune_older_than_days,
        report_older_than_days=report_older_than_days,
        daylog_older_than_days=daylog_older_than_days,
    )
    payload = {
        'report_dir': str(base_dir),
        'older_than_days': args.prune_older_than_days,
        'retention_days': {
            'report': args.prune_older_than_days if report_older_than_days is None else report_older_than_days,
            'daylog': args.prune_older_than_days if daylog_older_than_days is None else daylog_older_than_days,
        },
        'candidate_count': len(candidates),
        'candidates': candidates,
        'apply': args.prune_apply,
    }
    if args.prune_apply:
        for item in candidates:
            Path(item['path']).unlink(missing_ok=True)
        payload['deleted_count'] = len(candidates)
    if emit:
        render_prune_payload(payload, args.format)
    return payload



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
    parser.add_argument('--automation-preset', choices=sorted(AUTOMATION_PRESETS), help='Pas een vaste automation-combinatie toe voor report/daylog plus cleanup')
    parser.add_argument('--report', action='store_true', help='Schrijf ook een rapportartifact weg in de creative reports-map')
    parser.add_argument('--report-dir', help='Overschrijf de standaard rapportmap')
    parser.add_argument('--timestamped', action='store_true', help='Maak timestamped rapportbestanden bij --report')
    parser.add_argument('--append', action='store_true', help='Append naar bestaand rapportbestand bij --report')
    parser.add_argument('--daylog', action='store_true', help='Append compacte JSONL summary-events aan één daglogbestand per UTC-dag')
    parser.add_argument('--daylog-dir', help='Overschrijf de standaard map voor daglog-artifacts')
    parser.add_argument('--prune', action='store_true', help='Toon of verwijder oude creative-review rapportartifacts in de reports-map')
    parser.add_argument('--prune-after-write', action='store_true', help='Draai direct na report/daylog writes een prune-pass op dezelfde artifactmap')
    parser.add_argument('--cleanup-preset', choices=sorted(CLEANUP_PRESETS), help='Gebruik een vaste bewaarbeleidcombinatie voor report- en daglog-pruning')
    parser.add_argument('--prune-older-than-days', type=int, default=7, help='Selecteer report/daylog artifacts ouder dan dit aantal dagen, tenzij een specifiek retain-override is gezet')
    parser.add_argument('--prune-report-older-than-days', type=int, help='Overschrijf prune-retentie alleen voor timestamped/per-run reports')
    parser.add_argument('--prune-daylog-older-than-days', type=int, help='Overschrijf prune-retentie alleen voor daglogs')
    parser.add_argument('--prune-apply', action='store_true', help='Verwijder prune-kandidaten echt in plaats van alleen tonen')
    args, extra = parser.parse_known_args()

    if extra and extra[0] == '--':
        extra = extra[1:]
    args.extra = extra
    args = apply_automation_preset(args)
    args = apply_cleanup_preset(args)

    if args.daylog and (args.timestamped or args.append or args.report_dir):
        parser.error('--daylog gebruikt zijn eigen append-daglog; combineer niet met --timestamped, --append of --report-dir')
    if args.prune and args.mode in SUITES:
        parser.error('--prune werkt op de reports-map en niet samen met suite-executie')
    if args.prune and (args.report or args.daylog or args.timestamped or args.append or args.prune_after_write):
        parser.error('--prune combineert niet met report/daylog schrijfmodi of --prune-after-write')
    if args.prune_after_write and not (args.report or args.daylog):
        parser.error('--prune-after-write vereist --report of --daylog')

    if args.prune:
        run_prune(args)
        raise SystemExit(0)

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

    if args.prune_after_write and exit_code == 0:
        args.prune_apply = True
        run_prune(args, emit=args.format != 'jsonl')

    raise SystemExit(exit_code)


if __name__ == '__main__':
    main()
