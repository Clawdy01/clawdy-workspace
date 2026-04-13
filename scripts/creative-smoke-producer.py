#!/usr/bin/env python3
import argparse
import subprocess
import sys
from pathlib import Path

WORKSPACE = Path(__file__).resolve().parent.parent
CREATIVE_SMOKE = WORKSPACE / 'scripts' / 'creative-smoke.py'

PRODUCER_MODES = {
    'board': [
        ['full-cycle-brief', '--consumer-bundle', 'board-pair', '--format', 'json'],
    ],
    'eventlog': [
        ['full-cycle-brief', '--consumer-preset', 'eventlog-jsonl', '--format', 'json'],
    ],
    'all': [
        ['full-cycle-brief', '--consumer-bundle', 'board-suite', '--format', 'json'],
    ],
}


def run_one(args):
    cmd = ['python3', str(CREATIVE_SMOKE), *args]
    return subprocess.run(cmd, cwd=WORKSPACE, text=True, capture_output=True)



def main():
    parser = argparse.ArgumentParser(description='Vaste producer-wrapper voor compacte creative smoke-consumers.')
    parser.add_argument('mode', choices=sorted(PRODUCER_MODES), help='Welke vaste consumer-producerroute je wilt draaien')
    parser.add_argument('--quiet', action='store_true', help='Toon geen volledige child-output, alleen een compacte producer-status')
    args, extra = parser.parse_known_args()

    if extra and extra[0] == '--':
        extra = extra[1:]

    exit_code = 0
    summaries = []
    for base_args in PRODUCER_MODES[args.mode]:
        proc = run_one(base_args + extra)
        if proc.returncode != 0 and exit_code == 0:
            exit_code = proc.returncode
        summaries.append({
            'args': base_args,
            'returncode': proc.returncode,
            'stdout': proc.stdout,
            'stderr': proc.stderr,
        })
        if not args.quiet:
            if proc.stdout:
                sys.stdout.write(proc.stdout)
                if not proc.stdout.endswith('\n'):
                    print()
            if proc.stderr:
                sys.stderr.write(proc.stderr)

    if args.quiet:
        print(f'creative-smoke-producer: {args.mode}')
        for item in summaries:
            label = ' '.join(item['args'])
            print(f'- {label}: exit={item["returncode"]}')

    raise SystemExit(exit_code)


if __name__ == '__main__':
    main()
