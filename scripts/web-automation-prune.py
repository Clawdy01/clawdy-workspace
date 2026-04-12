#!/usr/bin/env python3
import argparse
import json
import subprocess
import sys
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path('/home/clawdy/.openclaw/workspace')
SITES = ROOT / 'scripts' / 'web-automation-sites.py'
DESKTOP = ROOT / 'scripts' / 'desktop-fallback-status.py'
ARTIFACTS = ROOT / 'scripts' / 'web-automation-artifacts.py'


def run_json(command, timeout=30, default=None):
    try:
        proc = subprocess.run(command, cwd=ROOT, capture_output=True, text=True, check=False, timeout=timeout)
    except subprocess.TimeoutExpired:
        return default
    if proc.returncode != 0:
        return default
    try:
        return json.loads(proc.stdout)
    except Exception:
        return default


def relpath(path):
    try:
        return str(path.relative_to(ROOT))
    except Exception:
        return str(path)


def desktop_label(slug=None, metadata_url=None, path=None):
    if slug:
        return f'{slug} desktop'
    host = urlparse(metadata_url or '').netloc
    if host:
        return f'{host} desktop'
    return path or 'desktop'


def path_size_bytes(path):
    candidate = Path(path)
    try:
        if candidate.is_file():
            return candidate.stat().st_size
        if candidate.is_dir():
            total = 0
            for child in candidate.rglob('*'):
                if child.is_file():
                    total += child.stat().st_size
            return total
    except Exception:
        return None
    return None


def add_candidate(candidates, seen, path, kind, slug=None, adapter=None, reason=None, label=None):
    candidate = Path(path)
    if not candidate.exists() or candidate in seen:
        return
    seen.add(candidate)
    candidates.append({
        'path': relpath(candidate),
        'kind': kind,
        'slug': slug,
        'adapter': adapter,
        'reason': reason,
        'label': label,
        'is_dir': candidate.is_dir(),
        'size_bytes': path_size_bytes(candidate),
    })


def gather_candidates(stale_after_seconds, adapter_filter=None):
    adapter_args = []
    for adapter in sorted({str(item).strip().lower() for item in (adapter_filter or []) if str(item).strip()}):
        adapter_args.extend(['--adapter', adapter])

    sites = run_json(['python3', str(SITES), '--json', '--stale-after', str(stale_after_seconds), *adapter_args], default={}) or {}
    desktop = run_json(['python3', str(DESKTOP), '--json', '--stale-after', str(stale_after_seconds), *adapter_args], default={}) or {}
    artifacts = run_json(['python3', str(ARTIFACTS), '--json', '--stale-after', str(stale_after_seconds), *adapter_args], default={}) or {}

    candidates = []
    seen = set()

    for site in sites.get('sites') or []:
        if site.get('configured') or not site.get('attention_needed', site.get('stale')):
            continue
        for key in ('json_path', 'png_path'):
            value = site.get(key)
            if not value:
                continue
            add_candidate(
                candidates,
                seen,
                ROOT / value,
                kind='site-artifact',
                slug=site.get('slug'),
                adapter=site.get('adapter'),
                reason='stale unmanaged site artifact',
            )

    for outdir in desktop.get('outdirs') or []:
        if outdir.get('configured') or not outdir.get('stale'):
            continue
        path = outdir.get('path')
        if not path:
            continue
        add_candidate(
            candidates,
            seen,
            ROOT / path,
            kind='desktop-outdir',
            slug=outdir.get('slug'),
            adapter=outdir.get('configured_adapter'),
            reason='stale unmanaged desktop fallback outdir',
            label=desktop_label(outdir.get('slug'), outdir.get('metadata_url'), path),
        )

    for item in artifacts.get('items') or []:
        if item.get('site_configured') or not item.get('stale'):
            continue
        artifact_slug = item.get('slug') or item.get('artifact')
        artifact_label = item.get('site_label') or artifact_slug or item.get('json_path')
        for key in ('json_path', 'png_path'):
            value = item.get(key)
            if not value:
                continue
            add_candidate(
                candidates,
                seen,
                ROOT / value,
                kind='artifact-file',
                slug=artifact_slug,
                adapter=item.get('adapter'),
                reason='stale unmanaged automation artifact',
                label=artifact_label,
            )

    targets = {}
    for item in candidates:
        if item.get('kind') == 'desktop-outdir':
            key = (item.get('kind'), item.get('path'))
            target = targets.setdefault(key, {
                'kind': item.get('kind'),
                'slug': item.get('slug'),
                'adapter': item.get('adapter'),
                'reason': item.get('reason'),
                'path_count': 0,
                'paths': [],
                'label': item.get('label') or item.get('slug') or item.get('path'),
                'size_bytes': 0,
            })
        else:
            key = (item.get('kind'), item.get('slug') or item.get('path'))
            target = targets.setdefault(key, {
                'kind': item.get('kind'),
                'slug': item.get('slug'),
                'adapter': item.get('adapter'),
                'reason': item.get('reason'),
                'path_count': 0,
                'paths': [],
                'label': item.get('label') or item.get('slug') or item.get('path'),
                'size_bytes': 0,
            })
        target['path_count'] += 1
        target['paths'].append(item.get('path'))
        if item.get('size_bytes') is not None:
            target['size_bytes'] += item.get('size_bytes') or 0

    total_size_bytes = sum(item.get('size_bytes') or 0 for item in candidates)

    target_list = sorted(
        targets.values(),
        key=lambda item: (item.get('kind') != 'desktop-outdir', item.get('label') or ''),
    )

    return {
        'stale_after_seconds': stale_after_seconds,
        'requested_adapters': sorted({str(item).strip().lower() for item in (adapter_filter or []) if str(item).strip()}),
        'site_count': len([item for item in candidates if item.get('kind') == 'site-artifact']),
        'artifact_file_count': len([item for item in candidates if item.get('kind') == 'artifact-file']),
        'desktop_outdir_count': len([item for item in candidates if item.get('kind') == 'desktop-outdir']),
        'candidate_count': len(candidates),
        'target_count': len(target_list),
        'total_size_bytes': total_size_bytes,
        'targets': target_list,
        'candidates': sorted(candidates, key=lambda item: (item.get('kind') != 'desktop-outdir', item.get('slug') or '', item.get('path') or '')),
        'sites_summary': {
            'unmanaged_stale_site_count': sites.get('unmanaged_stale_site_count', 0),
            'configured_stale_site_count': sites.get('configured_stale_site_count', 0),
            'operationally_healthy': sites.get('operationally_healthy'),
        },
        'desktop_summary': {
            'unmanaged_stale_outdir_count': desktop.get('unmanaged_stale_outdir_count', 0),
            'configured_stale_outdir_count': desktop.get('configured_stale_outdir_count', 0),
            'operationally_healthy': desktop.get('operationally_healthy'),
        },
        'artifacts_summary': {
            'unmanaged_stale_artifact_count': artifacts.get('unmanaged_stale_artifact_count', 0),
            'configured_stale_artifact_count': artifacts.get('configured_stale_artifact_count', 0),
            'operationally_healthy': artifacts.get('operationally_healthy'),
        },
    }


def trash_path(path):
    proc = subprocess.run(['gio', 'trash', str(path)], cwd=ROOT, capture_output=True, text=True, check=False)
    return {
        'path': relpath(path),
        'ok': proc.returncode == 0,
        'returncode': proc.returncode,
        'stderr': (proc.stderr or '').strip(),
    }


def human_bytes(size_bytes):
    if size_bytes is None:
        return '?'
    value = float(size_bytes)
    units = ['B', 'KB', 'MB', 'GB', 'TB']
    for unit in units:
        if value < 1024 or unit == units[-1]:
            if unit == 'B':
                return f'{int(value)} {unit}'
            return f'{value:.1f} {unit}'
        value /= 1024
    return f'{int(size_bytes)} B'


def render_text(summary):
    lines = ['Web automation prune unmanaged']
    if summary.get('requested_adapters'):
        lines.append(f"- adapters={', '.join(summary.get('requested_adapters') or [])}")
    lines.append(
        f"- candidates={summary.get('candidate_count')} | targets={summary.get('target_count')} | total-size={human_bytes(summary.get('total_size_bytes'))} | site-artifacts={summary.get('site_count')} | artifact-files={summary.get('artifact_file_count')} | desktop-outdirs={summary.get('desktop_outdir_count')} | stale-after={summary.get('stale_after_seconds')}s"
    )
    lines.append(
        f"- site health: configured stale={summary.get('sites_summary', {}).get('configured_stale_site_count', 0)}, unmanaged stale={summary.get('sites_summary', {}).get('unmanaged_stale_site_count', 0)}, operational={summary.get('sites_summary', {}).get('operationally_healthy')}"
    )
    lines.append(
        f"- desktop health: configured stale={summary.get('desktop_summary', {}).get('configured_stale_outdir_count', 0)}, unmanaged stale={summary.get('desktop_summary', {}).get('unmanaged_stale_outdir_count', 0)}, operational={summary.get('desktop_summary', {}).get('operationally_healthy')}"
    )
    lines.append(
        f"- artifact health: configured stale={summary.get('artifacts_summary', {}).get('configured_stale_artifact_count', 0)}, unmanaged stale={summary.get('artifacts_summary', {}).get('unmanaged_stale_artifact_count', 0)}, operational={summary.get('artifacts_summary', {}).get('operationally_healthy')}"
    )
    for item in summary.get('targets') or []:
        label = item.get('label') or item.get('slug') or item.get('paths', ['?'])[0]
        adapter = f" [{item.get('adapter')}]" if item.get('adapter') else ''
        lines.append(f"- target: {item.get('kind')} {label}{adapter} ({item.get('path_count')} path(s), {human_bytes(item.get('size_bytes'))})")
    for item in summary.get('candidates') or []:
        lines.append(f"- {item.get('kind')}: {item.get('path')} ({item.get('reason')}, {human_bytes(item.get('size_bytes'))})")
    results = summary.get('results') or []
    if results:
        ok_count = sum(1 for item in results if item.get('ok'))
        lines.append(f'- trashed={ok_count}/{len(results)}')
        for item in results:
            if not item.get('ok'):
                lines.append(f"- failed: {item.get('path')} -> {item.get('stderr') or 'unknown error'}")
    return '\n'.join(lines)


def main():
    parser = argparse.ArgumentParser(description='Verzamel of trash stale onbeheerde web automation artifacts en desktop outdirs')
    parser.add_argument('--json', action='store_true')
    parser.add_argument('--apply', action='store_true', help='voer de prune echt uit via gio trash')
    parser.add_argument('--stale-after', type=int, default=900)
    parser.add_argument('--adapter', action='append', help='beperk prune-review tot één adapter (herhaalbaar)')
    args = parser.parse_args()

    summary = gather_candidates(args.stale_after, adapter_filter=args.adapter)
    if args.apply:
        summary['results'] = [trash_path(ROOT / item['path']) for item in summary.get('candidates') or []]
        summary['applied'] = True
    else:
        summary['applied'] = False

    try:
        if args.json:
            print(json.dumps(summary, ensure_ascii=False, indent=2))
        else:
            print(render_text(summary))
    except BrokenPipeError:
        try:
            sys.stdout.close()
        except Exception:
            pass

    if args.apply and any(not item.get('ok') for item in summary.get('results') or []):
        raise SystemExit(1)


if __name__ == '__main__':
    main()
