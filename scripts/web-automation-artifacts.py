#!/usr/bin/env python3
import argparse
import json
import subprocess
import sys
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path('/home/clawdy/.openclaw/workspace')
BROWSER = ROOT / 'browser-automation'
ARTIFACT_DIRS = [
    BROWSER / 'out',
    BROWSER / 'out-desktop',
]
DEFAULT_STALE_AFTER_SECONDS = 900
ADAPTER_RECOMMENDATIONS = {
    'desktop': 'python3 scripts/web-automation-dispatch.py desktop-probe',
    'generic': 'python3 scripts/web-automation-dispatch.py probe-page <url>',
    'proton': 'python3 scripts/web-automation-dispatch.py proton-refresh',
}
PROTON_NEXT = ROOT / 'scripts' / 'proton-next-step.py'
SITES = ROOT / 'scripts' / 'web-automation-sites.py'


def parse_iso(value):
    if not value:
        return None
    try:
        return datetime.fromisoformat(str(value).replace('Z', '+00:00')).astimezone(timezone.utc)
    except Exception:
        return None


def fmt_age(seconds):
    if seconds is None:
        return 'unknown'
    if seconds < 60:
        return f'{seconds}s'
    if seconds < 3600:
        return f'{seconds // 60}m'
    return f'{seconds // 3600}h{(seconds % 3600) // 60:02d}m'


def classify_stem(stem):
    stem = stem.lower()
    if stem == 'probe':
        return 'generic', 'probe'
    if stem.startswith('probe-'):
        return 'generic', stem[len('probe-'):]
    if stem.startswith('desktop'):
        return 'desktop', stem
    if stem.startswith('proton'):
        return 'proton', stem
    prefix = stem.split('-', 1)[0]
    return prefix, stem


def read_json(path):
    try:
        return json.loads(path.read_text())
    except Exception:
        return {}


def fallback_checked_at(path):
    try:
        return datetime.fromtimestamp(path.stat().st_mtime, tz=timezone.utc)
    except Exception:
        return None


def run_json(command, timeout=20, default=None):
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


def normalize_url(value):
    parsed = urlparse(value or '')
    if not parsed.scheme and not parsed.netloc and not parsed.path:
        return ''
    path = parsed.path or '/'
    if path != '/':
        path = path.rstrip('/') or '/'
    normalized = f"{parsed.scheme.lower()}://{parsed.netloc.lower()}{path}"
    if parsed.query:
        normalized += f'?{parsed.query}'
    if parsed.fragment:
        normalized += f'#{parsed.fragment}'
    return normalized


def load_site_overlays(stale_after_seconds):
    summary = run_json(
        ['python3', str(SITES), '--json', '--stale-after', str(stale_after_seconds)],
        default={},
    ) or {}
    overlays = {
        'by_slug': {},
        'by_url': {},
    }
    for site in summary.get('sites') or []:
        slug = str(site.get('slug') or '').strip().lower()
        if slug:
            overlays['by_slug'][slug] = site
        for candidate in [site.get('url'), site.get('final_url')]:
            normalized = normalize_url(candidate)
            if normalized:
                overlays['by_url'][normalized] = site
    return overlays


def match_site_overlay(site_overlays, slug, url):
    normalized_slug = str(slug or '').strip().lower()
    if normalized_slug and normalized_slug in site_overlays.get('by_slug', {}):
        return site_overlays['by_slug'][normalized_slug]
    normalized_url = normalize_url(url)
    if normalized_url and normalized_url in site_overlays.get('by_url', {}):
        return site_overlays['by_url'][normalized_url]
    return None


def proton_overlay():
    summary = run_json(['python3', str(PROTON_NEXT), '--json'], default={}) or {}
    if not summary:
        return {}

    recommended_route = summary.get('recommended_route')
    recommended_command = summary.get('recommended_command')
    terminal_manual = recommended_route == 'account-created'
    verification = summary.get('verification') or {}
    return {
        'workflow_state': recommended_route or summary.get('phase') or 'unknown',
        'workflow_terminal': terminal_manual,
        'workflow_attention': 'manual' if terminal_manual else ('none' if recommended_route == 'noop' else 'automation'),
        'workflow_note': summary.get('reason') or '',
        'workflow_checked_at': verification.get('checked_at') or None,
        'workflow_age_seconds': verification.get('age_seconds'),
        'workflow_stale': summary.get('verification_stale') if verification else summary.get('stale'),
        'workflow_command': recommended_command or None,
    }


def build_summary(stale_after_seconds=DEFAULT_STALE_AFTER_SECONDS, adapter_filter=None):
    now = datetime.now(timezone.utc)
    items = []
    by_adapter = defaultdict(list)
    adapter_overlays = {
        'proton': proton_overlay(),
    }
    site_overlays = load_site_overlays(stale_after_seconds)
    wanted_adapters = None
    if adapter_filter:
        wanted_adapters = {str(item).strip().lower() for item in adapter_filter if str(item).strip()}

    for artifact_dir in ARTIFACT_DIRS:
        if not artifact_dir.exists():
            continue
        for json_path in sorted(artifact_dir.glob('*.json')):
            data = read_json(json_path)
            stem = json_path.stem
            adapter, artifact = classify_stem(stem)
            checked_at = parse_iso(data.get('checkedAt') or data.get('checked_at')) or fallback_checked_at(json_path)
            age_seconds = int((now - checked_at).total_seconds()) if checked_at else None
            png_path = json_path.with_suffix('.png')
            url = data.get('url') or data.get('finalUrl')
            title = data.get('title')
            slug = data.get('slug')
            raw_stale = age_seconds is None or age_seconds > stale_after_seconds
            item = {
                'adapter': adapter,
                'detected_adapter': adapter,
                'artifact': artifact,
                'json_path': str(json_path.relative_to(ROOT)),
                'png_path': str(png_path.relative_to(ROOT)) if png_path.exists() else None,
                'source_dir': str(artifact_dir.relative_to(ROOT)),
                'checked_at': checked_at.isoformat().replace('+00:00', 'Z') if checked_at else None,
                'age_seconds': age_seconds,
                'age_human': fmt_age(age_seconds),
                'stale': raw_stale,
                'raw_stale': raw_stale,
                'has_screenshot': png_path.exists(),
                'title': title,
                'url': url,
                'slug': slug,
            }
            matched_site = match_site_overlay(site_overlays, slug, url)
            if matched_site:
                item['site_slug'] = matched_site.get('slug')
                item['site_label'] = matched_site.get('label')
                item['site_configured'] = bool(matched_site.get('configured'))
                item['site_stale_after_seconds'] = matched_site.get('stale_after_seconds')
                item['site_recommended_command'] = matched_site.get('recommended_command')
                if matched_site.get('adapter'):
                    item['adapter'] = matched_site.get('adapter')
                if matched_site.get('attention_needed') is not None:
                    item['stale'] = bool(matched_site.get('attention_needed'))
                if matched_site.get('attention_needed') is False and item.get('raw_stale'):
                    item['stale_ignored_reason'] = 'site-overlay'
            overlay = adapter_overlays.get(item['adapter']) or {}
            if overlay:
                item.update({k: v for k, v in overlay.items() if v not in (None, '')})
                if overlay.get('workflow_terminal'):
                    item['stale'] = False
                    item['stale_ignored_reason'] = 'workflow-terminal'
            if wanted_adapters is not None and item['adapter'] not in wanted_adapters:
                continue
            items.append(item)
            by_adapter[item['adapter']].append(item)

    adapters = []
    recommended_actions = []
    configured_recommended_actions = []
    ignored_stale_items = 0
    for adapter, adapter_items in sorted(by_adapter.items()):
        freshest = min(
            (item['age_seconds'] for item in adapter_items if item['age_seconds'] is not None),
            default=None,
        )
        raw_stale_count = sum(1 for item in adapter_items if item.get('raw_stale'))
        stale_count = sum(1 for item in adapter_items if item.get('stale'))
        ignored_here = sum(1 for item in adapter_items if item.get('raw_stale') and not item.get('stale'))
        ignored_stale_items += ignored_here
        latest = sorted(
            adapter_items,
            key=lambda item: (
                item['age_seconds'] is None,
                item['age_seconds'] if item['age_seconds'] is not None else 10**12,
                item['artifact'],
            ),
        )[:5]
        overlay = adapter_overlays.get(adapter) or {}
        fallback_detected_adapters = [item.get('detected_adapter') for item in adapter_items if item.get('detected_adapter')]
        configured_site_commands = [
            item.get('site_recommended_command')
            for item in adapter_items
            if item.get('stale') and item.get('site_configured') and item.get('site_recommended_command')
        ]
        any_site_commands = [
            item.get('site_recommended_command')
            for item in adapter_items
            if item.get('stale') and item.get('site_recommended_command')
        ]
        recommended_command = (
            overlay.get('workflow_command')
            or (configured_site_commands[0] if configured_site_commands else None)
            or (any_site_commands[0] if any_site_commands else None)
            or ADAPTER_RECOMMENDATIONS.get(adapter)
        )
        if not recommended_command:
            for detected_adapter in fallback_detected_adapters:
                recommended_command = ADAPTER_RECOMMENDATIONS.get(detected_adapter)
                if recommended_command:
                    break
        adapter_summary = {
            'adapter': adapter,
            'artifact_count': len(adapter_items),
            'configured_artifact_count': sum(1 for item in adapter_items if item.get('site_configured')),
            'unmanaged_artifact_count': sum(1 for item in adapter_items if not item.get('site_configured')),
            'freshest_age_seconds': freshest,
            'freshest_age_human': fmt_age(freshest),
            'stale_count': stale_count,
            'configured_stale_count': sum(1 for item in adapter_items if item.get('stale') and item.get('site_configured')),
            'unmanaged_stale_count': sum(1 for item in adapter_items if item.get('stale') and not item.get('site_configured')),
            'raw_stale_count': raw_stale_count,
            'ignored_stale_count': ignored_here,
            'healthy': stale_count == 0 and (freshest is not None or overlay.get('workflow_terminal')),
            'configured_healthy': sum(1 for item in adapter_items if item.get('stale') and item.get('site_configured')) == 0,
            'operationally_healthy': sum(1 for item in adapter_items if item.get('stale') and item.get('site_configured')) == 0,
            'recommended_command': recommended_command,
            'latest_artifacts': latest,
        }
        if overlay:
            adapter_summary.update({k: v for k, v in overlay.items() if k not in {'workflow_command'}})
        adapters.append(adapter_summary)
        if stale_count and recommended_command:
            action_reason = f'{stale_count} stale artifacts'
            if configured_site_commands:
                configured_site_slugs = sorted({
                    item.get('site_slug')
                    for item in adapter_items
                    if item.get('stale') and item.get('site_configured') and item.get('site_slug')
                })
                if configured_site_slugs:
                    action_reason = f"{len(configured_site_slugs)} stale configured site(s): {', '.join(configured_site_slugs)}"
            action = {
                'adapter': adapter,
                'reason': action_reason,
                'command': recommended_command,
                'configured': bool(adapter_summary.get('configured_stale_count')),
            }
            recommended_actions.append(action)
            if adapter_summary.get('configured_stale_count'):
                configured_recommended_actions.append(action)

    freshest_global = min((item['age_seconds'] for item in items if item['age_seconds'] is not None), default=None)
    stalest_global = max((item['age_seconds'] for item in items if item['age_seconds'] is not None), default=None)
    raw_stale_items = sum(1 for item in items if item.get('raw_stale'))
    stale_items = sum(1 for item in items if item.get('stale'))
    configured_items = [item for item in items if item.get('site_configured')]
    unmanaged_items = [item for item in items if not item.get('site_configured')]
    configured_stale_items = sum(1 for item in configured_items if item.get('stale'))
    unmanaged_stale_items = sum(1 for item in unmanaged_items if item.get('stale'))
    operationally_healthy = bool(configured_items) and configured_stale_items == 0

    return {
        'artifact_count': len(items),
        'adapter_count': len(adapters),
        'artifact_dirs': [str(path.relative_to(ROOT)) for path in ARTIFACT_DIRS if path.exists()],
        'stale_after_seconds': stale_after_seconds,
        'configured_artifact_count': len(configured_items),
        'unmanaged_artifact_count': len(unmanaged_items),
        'freshest_age_seconds': freshest_global,
        'freshest_age_human': fmt_age(freshest_global),
        'stalest_age_seconds': stalest_global,
        'stalest_age_human': fmt_age(stalest_global),
        'stale_artifact_count': stale_items,
        'configured_stale_artifact_count': configured_stale_items,
        'unmanaged_stale_artifact_count': unmanaged_stale_items,
        'raw_stale_artifact_count': raw_stale_items,
        'ignored_stale_artifact_count': ignored_stale_items,
        'healthy': stale_items == 0 and bool(items),
        'configured_healthy': operationally_healthy,
        'operationally_healthy': operationally_healthy,
        'recommended_actions': recommended_actions,
        'configured_recommended_actions': configured_recommended_actions,
        'adapters': adapters,
        'items': items,
    }


def render_text(summary):
    lines = ['Web automation artifacts']
    lines.append(
        f"- healthy: {summary.get('healthy')} | operational: {summary.get('operationally_healthy')} | adapters: {summary.get('adapter_count')} | artifacts: {summary.get('artifact_count')} | configured: {summary.get('configured_artifact_count')} | unmanaged: {summary.get('unmanaged_artifact_count')} | stale: {summary.get('stale_artifact_count')} (configured {summary.get('configured_stale_artifact_count')}, unmanaged {summary.get('unmanaged_stale_artifact_count')}) | raw_stale: {summary.get('raw_stale_artifact_count')} | ignored: {summary.get('ignored_stale_artifact_count')} | freshest: {summary.get('freshest_age_human')} | stalest: {summary.get('stalest_age_human')}"
    )
    for adapter in summary.get('adapters', []):
        latest = adapter.get('latest_artifacts') or []
        preview = ', '.join(
            f"{item.get('artifact')} ({item.get('age_human')})" for item in latest[:3]
        ) or 'geen'
        recommendation = f", refresh {adapter.get('recommended_command')}" if adapter.get('stale_count') and adapter.get('recommended_command') else ''
        workflow = ''
        if adapter.get('workflow_state'):
            workflow = f", workflow {adapter.get('workflow_state')}"
            if adapter.get('workflow_attention'):
                workflow += f"/{adapter.get('workflow_attention')}"
        ignored = f", ignored {adapter.get('ignored_stale_count')}" if adapter.get('ignored_stale_count') else ''
        lines.append(
            f"- {adapter.get('adapter')}: {adapter.get('artifact_count')} artifacts, configured {adapter.get('configured_artifact_count')}, unmanaged {adapter.get('unmanaged_artifact_count')}, stale {adapter.get('stale_count')} (configured {adapter.get('configured_stale_count')}, unmanaged {adapter.get('unmanaged_stale_count')}, raw {adapter.get('raw_stale_count')}{ignored}), freshest {adapter.get('freshest_age_human')}, latest {preview}{workflow}{recommendation}"
        )
    if summary.get('recommended_actions'):
        lines.append('- recommended actions:')
        for action in summary.get('recommended_actions'):
            scope = 'configured' if action.get('configured') else 'unmanaged'
            lines.append(f"  - {action.get('adapter')} ({scope}): {action.get('reason')} -> {action.get('command')}")
    return '\n'.join(lines)


def main():
    parser = argparse.ArgumentParser(description='Compact observability-overzicht van web automation artifacts')
    parser.add_argument('--json', action='store_true')
    parser.add_argument('--stale-after', type=int, default=DEFAULT_STALE_AFTER_SECONDS, help='markeer artifacts ouder dan dit aantal seconden als stale')
    parser.add_argument('--adapter', action='append', help='beperk de artifact-view tot één adapter (herhaalbaar)')
    args = parser.parse_args()

    summary = build_summary(stale_after_seconds=args.stale_after, adapter_filter=args.adapter)
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


if __name__ == '__main__':
    main()
