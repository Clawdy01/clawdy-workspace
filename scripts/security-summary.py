#!/usr/bin/env python3
import argparse
import json
import re
import subprocess
import time
from pathlib import Path

ROOT = Path('/home/clawdy/.openclaw/workspace')
STATE = ROOT / 'state'
CACHE = STATE / 'security-summary.json'
CACHE_MAX_AGE = 3600


def load_cache(max_age=CACHE_MAX_AGE):
    try:
        data = json.loads(CACHE.read_text())
    except Exception:
        return None
    ts = data.get('_cached_at', 0)
    if max_age is not None and (time.time() - ts) > max_age:
        return None
    return data


def save_cache(summary):
    STATE.mkdir(parents=True, exist_ok=True)
    CACHE.write_text(json.dumps({**summary, '_cached_at': time.time()}, ensure_ascii=False, indent=2))


def run_audit():
    try:
        proc = subprocess.run(
            ['openclaw', 'security', 'audit'],
            cwd=ROOT,
            capture_output=True,
            text=True,
            check=False,
            timeout=20,
        )
    except subprocess.TimeoutExpired:
        cached = load_cache(max_age=None)
        if cached:
            cached['cached'] = True
            return cached
        raise SystemExit('openclaw security audit timed out')
    if proc.returncode != 0:
        cached = load_cache(max_age=None)
        if cached:
            cached['cached'] = True
            return cached
        raise SystemExit(proc.stderr.strip() or proc.stdout.strip() or f'openclaw security audit failed: {proc.returncode}')
    return proc.stdout


def summarize(text):
    m = re.search(r'Summary:\s*(\d+) critical\s*·\s*(\d+) warn\s*·\s*(\d+) info', text)
    if not m:
        return {'text': 'onbekend', 'critical': None, 'warn': None, 'info': None}
    critical, warn, info = map(int, m.groups())
    return {
        'critical': critical,
        'warn': warn,
        'info': info,
        'text': f'{critical} critical, {warn} warn, {info} info',
    }


def main():
    parser = argparse.ArgumentParser(description='Compacte security audit samenvatting')
    parser.add_argument('--json', action='store_true')
    args = parser.parse_args()

    audit_result = run_audit()
    summary = audit_result if isinstance(audit_result, dict) else summarize(audit_result)
    if not summary.get('cached'):
        save_cache(summary)
    if args.json:
        print(json.dumps(summary, ensure_ascii=False, indent=2))
    else:
        print('Security audit')
        suffix = ' (cache)' if summary.get('cached') else ''
        print(f"- {summary['text']}{suffix}")


if __name__ == '__main__':
    main()
