#!/usr/bin/env python3
import argparse
import json
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path('/home/clawdy/.openclaw/workspace')
BROWSER = ROOT / 'browser-automation'
DEFAULT_OUTDIR = BROWSER / 'out-desktop'
DEFAULT_STALE_AFTER_SECONDS = 900
DEFAULT_STALE_GRACE_SECONDS = 60
DEFAULT_COMMAND = 'python3 scripts/web-automation-dispatch.py refresh-desktop --configured-only'
DEFAULT_INTERNAL_COMMAND = 'python3 scripts/web-automation-dispatch.py desktop-probe'
SITE_REGISTRY = ROOT / 'state' / 'web-automation-sites.json'


def slug_to_outdir(slug):
    value = ''.join(ch if ch.isalnum() or ch in {'-', '_'} else '-' for ch in (slug or '').strip().lower()).strip('-_')
    if not value:
        raise ValueError('lege slug')
    return BROWSER / f'out-desktop-{value}'


def read_json(path):
    try:
        return json.loads(path.read_text())
    except Exception:
        return {}


def normalize_url(value):
    parsed = urlparse(value or '')
    if not parsed.scheme and not parsed.netloc and not parsed.path:
        return ''
    path = parsed.path or '/'
    if path != '/':
        path = path.rstrip('/') or '/'
    normalized = f'{parsed.scheme.lower()}://{parsed.netloc.lower()}{path}'
    if parsed.query:
        normalized += f'?{parsed.query}'
    if parsed.fragment:
        normalized += f'#{parsed.fragment}'
    return normalized


def normalize_bool(value, default=False):
    if value is None:
        return default
    if isinstance(value, bool):
        return value
    if isinstance(value, (int, float)):
        return bool(value)
    text = str(value).strip().lower()
    if text in {'1', 'true', 'yes', 'y', 'on'}:
        return True
    if text in {'0', 'false', 'no', 'n', 'off'}:
        return False
    return default


def load_registry():
    raw = read_json(SITE_REGISTRY)
    if isinstance(raw, dict):
        entries = raw.get('sites') if isinstance(raw.get('sites'), list) else raw.get('items')
    elif isinstance(raw, list):
        entries = raw
    else:
        entries = []

    by_slug = {}
    by_url = {}
    desktop_targets = []
    for item in entries or []:
        if not isinstance(item, dict) or item.get('enabled', True) is False:
            continue
        slug = str(item.get('slug') or '').strip().lower()
        url = normalize_url(str(item.get('url') or '').strip())
        stale_after = item.get('staleAfterSeconds')
        desktop_keep_screenshots = item.get('desktopKeepScreenshots')
        try:
            stale_after = int(stale_after)
        except (TypeError, ValueError):
            stale_after = None
        try:
            desktop_keep_screenshots = int(desktop_keep_screenshots)
        except (TypeError, ValueError):
            desktop_keep_screenshots = None
        if stale_after is not None and stale_after <= 0:
            stale_after = None
        if desktop_keep_screenshots is not None and desktop_keep_screenshots <= 0:
            desktop_keep_screenshots = None
        desktop_enabled = normalize_bool(item.get('desktopEnabled'), default=desktop_keep_screenshots is not None)
        enriched = dict(item)
        enriched['staleAfterSeconds'] = stale_after
        enriched['desktopKeepScreenshots'] = desktop_keep_screenshots
        enriched['desktopEnabled'] = desktop_enabled
        if slug:
            by_slug[slug] = enriched
        if url:
            by_url[url] = enriched
        if desktop_enabled and (slug or url):
            desktop_targets.append(enriched)
    return {'by_slug': by_slug, 'by_url': by_url, 'desktop_targets': desktop_targets}


def outdir_slug(outdir):
    name = outdir.name
    if name == 'out-desktop':
        return None
    prefix = 'out-desktop-'
    return name[len(prefix):] if name.startswith(prefix) else None


def classify_outdir(outdir, metadata, registry):
    slug = outdir_slug(outdir)
    normalized_url = normalize_url(metadata.get('url') or '') if isinstance(metadata, dict) else ''
    configured = None
    if slug:
        configured = (registry.get('by_slug') or {}).get(slug)
    if not configured and normalized_url:
        configured = (registry.get('by_url') or {}).get(normalized_url)
    return {
        'slug': slug,
        'configured': bool(configured),
        'configured_adapter': str(configured.get('adapter') or '').strip().lower() if configured else None,
        'configured_slug': str(configured.get('slug') or '').strip().lower() if configured else None,
        'configured_label': configured.get('label') if configured else None,
        'configured_url': normalize_url(str(configured.get('url') or '').strip()) if configured else None,
        'configured_stale_after_seconds': configured.get('staleAfterSeconds') if configured else None,
        'configured_desktop_keep_screenshots': configured.get('desktopKeepScreenshots') if configured else None,
        'configured_desktop_enabled': configured.get('desktopEnabled') if configured else None,
        'metadata_url_normalized': normalized_url or None,
    }


def fmt_age(seconds):
    if seconds is None:
        return 'unknown'
    if seconds < 60:
        return f'{seconds}s'
    if seconds < 3600:
        return f'{seconds // 60}m'
    return f'{seconds // 3600}h{(seconds % 3600) // 60:02d}m'


def iso_from_ts(ts):
    if ts is None:
        return None
    return datetime.fromtimestamp(ts, tz=timezone.utc).isoformat().replace('+00:00', 'Z')


def build_summary(stale_after_seconds=DEFAULT_STALE_AFTER_SECONDS, default_outdir=DEFAULT_OUTDIR, only_outdirs=None, stale_grace_seconds=DEFAULT_STALE_GRACE_SECONDS, adapter_filter=None, configured_only=False):
    now = datetime.now(timezone.utc)
    registry = load_registry()
    outdirs = []
    all_artifacts = []

    wanted = None
    if only_outdirs:
        wanted = {Path(item).resolve() for item in only_outdirs}

    wanted_adapters = None
    if adapter_filter:
        wanted_adapters = {str(item).strip().lower() for item in adapter_filter if str(item).strip()}

    for outdir in sorted(BROWSER.glob('out-desktop*')):
        if not outdir.is_dir():
            continue
        if wanted is not None and outdir.resolve() not in wanted:
            continue
        artifact_items = []
        latest_ts = None
        metadata = read_json(outdir / 'metadata.json')
        classification = classify_outdir(outdir, metadata, registry)
        if wanted_adapters is not None and classification.get('configured_adapter') not in wanted_adapters:
            continue
        if configured_only and not classification.get('configured'):
            continue
        metadata_checked_at = None
        if metadata.get('checkedAt'):
            try:
                metadata_checked_at = datetime.fromisoformat(str(metadata['checkedAt']).replace('Z', '+00:00')).astimezone(timezone.utc)
            except Exception:
                metadata_checked_at = None
        for path in sorted(outdir.iterdir()):
            if not path.is_file():
                continue
            try:
                mtime = path.stat().st_mtime
            except Exception:
                mtime = None
            latest_ts = max(latest_ts or 0, mtime or 0) or latest_ts
            age_seconds = int((now - datetime.fromtimestamp(mtime, tz=timezone.utc)).total_seconds()) if mtime else None
            item = {
                'path': str(path.relative_to(ROOT)),
                'name': path.name,
                'kind': 'metadata' if path.name == 'metadata.json' else ('screenshot' if path.suffix.lower() == '.png' else ('window-list' if path.name == 'windows.txt' else 'other')),
                'size_bytes': path.stat().st_size if path.exists() else None,
                'modified_at': iso_from_ts(mtime),
                'age_seconds': age_seconds,
                'age_human': fmt_age(age_seconds),
            }
            artifact_items.append(item)
            all_artifacts.append(item)

        screenshot_count = sum(1 for item in artifact_items if item.get('kind') == 'screenshot')
        latest_age_seconds = int((now - datetime.fromtimestamp(latest_ts, tz=timezone.utc)).total_seconds()) if latest_ts else None
        metadata_age_seconds = int((now - metadata_checked_at).total_seconds()) if metadata_checked_at else None
        latest_screenshot = next(
            (item for item in sorted(artifact_items, key=lambda item: item.get('age_seconds') if item.get('age_seconds') is not None else 10**12) if item.get('kind') == 'screenshot'),
            None,
        )
        effective_age_seconds = metadata_age_seconds if metadata_age_seconds is not None else latest_age_seconds
        metadata_success = metadata.get('success') if isinstance(metadata.get('success'), bool) else None
        effective_stale_after_seconds = classification.get('configured_stale_after_seconds') or stale_after_seconds
        effective_stale_grace_seconds = max(stale_grace_seconds, int(effective_stale_after_seconds * 0.05))
        outdirs.append({
            'path': str(outdir.relative_to(ROOT)),
            'slug': classification.get('slug'),
            'configured': classification.get('configured'),
            'configured_adapter': classification.get('configured_adapter'),
            'configured_slug': classification.get('configured_slug'),
            'configured_label': classification.get('configured_label'),
            'configured_url': classification.get('configured_url'),
            'configured_desktop_keep_screenshots': classification.get('configured_desktop_keep_screenshots'),
            'stale_after_seconds': effective_stale_after_seconds,
            'stale_grace_seconds': effective_stale_grace_seconds,
            'metadata_url_normalized': classification.get('metadata_url_normalized'),
            'artifact_count': len(artifact_items),
            'screenshot_count': screenshot_count,
            'has_windows_capture': any(item.get('name') == 'windows.txt' for item in artifact_items),
            'latest_modified_at': iso_from_ts(latest_ts),
            'latest_age_seconds': latest_age_seconds,
            'latest_age_human': fmt_age(latest_age_seconds),
            'metadata_checked_at': metadata_checked_at.isoformat().replace('+00:00', 'Z') if metadata_checked_at else None,
            'metadata_age_seconds': metadata_age_seconds,
            'metadata_age_human': fmt_age(metadata_age_seconds),
            'stale': effective_age_seconds is None or effective_age_seconds > (effective_stale_after_seconds + effective_stale_grace_seconds),
            'latest_screenshot': latest_screenshot,
            'metadata_present': bool(metadata),
            'metadata_success': metadata_success,
            'metadata_url': metadata.get('url') or None,
            'metadata_duration_seconds': metadata.get('durationSeconds'),
            'metadata_window_count': metadata.get('windowCount'),
            'metadata_error': metadata.get('error') or '',
            'artifacts': artifact_items,
        })

    freshest = min((item.get('age_seconds') for item in all_artifacts if item.get('age_seconds') is not None), default=None)
    stalest = max((item.get('age_seconds') for item in all_artifacts if item.get('age_seconds') is not None), default=None)
    default_outdir = Path(default_outdir)
    latest_default = next((item for item in outdirs if item.get('path') == str(default_outdir.relative_to(ROOT))), None)
    configured_outdirs = [item for item in outdirs if item.get('configured')]
    unmanaged_outdirs = [item for item in outdirs if not item.get('configured')]
    configured_stale_outdirs = [
        item for item in configured_outdirs
        if item.get('stale') or item.get('metadata_success', True) is False or not item.get('screenshot_count')
    ]
    unmanaged_stale_outdirs = [
        item for item in unmanaged_outdirs
        if item.get('stale') or item.get('metadata_success', True) is False or not item.get('screenshot_count')
    ]

    existing_configured_keys = set()
    for item in configured_outdirs:
        if item.get('configured_slug'):
            existing_configured_keys.add(('slug', item.get('configured_slug')))
        if item.get('configured_url'):
            existing_configured_keys.add(('url', item.get('configured_url')))

    missing_configured_targets = []
    for item in registry.get('desktop_targets') or []:
        slug = str(item.get('slug') or '').strip().lower() or None
        url = normalize_url(str(item.get('url') or '').strip()) or None
        if (slug and ('slug', slug) in existing_configured_keys) or (url and ('url', url) in existing_configured_keys):
            continue
        outdir = slug_to_outdir(slug) if slug else None
        missing_configured_targets.append({
            'path': str(outdir.relative_to(ROOT)) if outdir else None,
            'slug': slug,
            'configured': True,
            'configured_adapter': str(item.get('adapter') or '').strip().lower() or None,
            'configured_slug': slug,
            'configured_label': item.get('label') or None,
            'configured_url': url,
            'configured_desktop_keep_screenshots': item.get('desktopKeepScreenshots'),
            'configured_desktop_enabled': item.get('desktopEnabled'),
            'stale_after_seconds': item.get('staleAfterSeconds') or stale_after_seconds,
            'stale_grace_seconds': max(stale_grace_seconds, int((item.get('staleAfterSeconds') or stale_after_seconds) * 0.05)),
            'metadata_url_normalized': url,
            'artifact_count': 0,
            'screenshot_count': 0,
            'has_windows_capture': False,
            'latest_modified_at': None,
            'latest_age_seconds': None,
            'latest_age_human': 'missing',
            'metadata_checked_at': None,
            'metadata_age_seconds': None,
            'metadata_age_human': 'missing',
            'stale': True,
            'latest_screenshot': None,
            'metadata_present': False,
            'metadata_success': None,
            'metadata_url': url,
            'metadata_duration_seconds': None,
            'metadata_window_count': None,
            'metadata_error': '',
            'artifacts': [],
            'missing_outdir': True,
        })

    freshest_configured = min(
        configured_outdirs,
        key=lambda item: item.get('metadata_age_seconds') if item.get('metadata_age_seconds') is not None else (item.get('latest_age_seconds') if item.get('latest_age_seconds') is not None else 10**12),
        default=None,
    )
    display_outdir = latest_default if latest_default and latest_default.get('configured') else (freshest_configured or latest_default)
    display_scope = 'default' if display_outdir and latest_default and display_outdir.get('path') == latest_default.get('path') else ('configured' if display_outdir and display_outdir.get('configured') else 'fallback')
    healthy = bool(
        display_outdir
        and not display_outdir.get('stale')
        and display_outdir.get('screenshot_count')
        and display_outdir.get('metadata_success', True) is not False
    )
    stale_outdirs = [
        item for item in outdirs
        if item.get('stale') or item.get('metadata_success', True) is False or not item.get('screenshot_count')
    ]
    overall_healthy = bool(outdirs) and not stale_outdirs
    configured_attention_targets = list(configured_stale_outdirs) + missing_configured_targets
    configured_healthy = not configured_attention_targets
    operationally_healthy = configured_healthy
    configured_recommended_actions = []
    for item in configured_attention_targets:
        slug = item.get('configured_slug') or item.get('slug')
        internal_command = DEFAULT_INTERNAL_COMMAND
        recommended_command = DEFAULT_COMMAND
        if slug:
            keep_screenshots = item.get('configured_desktop_keep_screenshots')
            internal_parts = ['python3', 'scripts/web-automation-dispatch.py', 'desktop-probe', '--slug', slug]
            recommended_parts = ['python3', 'scripts/web-automation-dispatch.py', 'refresh-desktop', '--configured-only', '--slug', slug]
            stack_parts = ['python3', 'scripts/web-automation-dispatch.py', 'refresh-stack', '--configured-only', '--slug', slug]
            if keep_screenshots:
                recommended_parts.extend(['--keep-screenshots', str(keep_screenshots)])
            internal_command = ' '.join(internal_parts)
            recommended_command = ' '.join(recommended_parts)
            stack_command = ' '.join(stack_parts)
        else:
            stack_command = None
        configured_recommended_actions.append({
            'path': item.get('path'),
            'slug': slug,
            'missing_outdir': bool(item.get('missing_outdir')),
            'command': internal_command,
            'internal_command': internal_command,
            'recommended_command': recommended_command,
            'stack_command': stack_command,
            'keep_screenshots': item.get('configured_desktop_keep_screenshots'),
        })

    return {
        'healthy': healthy,
        'overall_healthy': overall_healthy,
        'configured_healthy': configured_healthy,
        'operationally_healthy': operationally_healthy,
        'configured_only': configured_only,
        'stale_outdir_count': len(stale_outdirs),
        'stale_outdirs': [item.get('path') for item in stale_outdirs],
        'configured_outdir_count': len(configured_outdirs),
        'configured_stale_outdir_count': len(configured_stale_outdirs),
        'configured_stale_outdirs': [item.get('path') for item in configured_stale_outdirs],
        'missing_configured_target_count': len(missing_configured_targets),
        'missing_configured_targets': [
            {
                'slug': item.get('configured_slug') or item.get('slug'),
                'path': item.get('path'),
                'adapter': item.get('configured_adapter'),
                'url': item.get('configured_url'),
                'keep_screenshots': item.get('configured_desktop_keep_screenshots'),
            }
            for item in missing_configured_targets
        ],
        'configured_attention_target_count': len(configured_attention_targets),
        'configured_recommended_actions': configured_recommended_actions,
        'unmanaged_outdir_count': len(unmanaged_outdirs),
        'unmanaged_stale_outdir_count': len(unmanaged_stale_outdirs),
        'unmanaged_stale_outdirs': [item.get('path') for item in unmanaged_stale_outdirs],
        'stale_after_seconds': stale_after_seconds,
        'stale_grace_seconds': stale_grace_seconds,
        'outdir_count': len(outdirs),
        'artifact_count': len(all_artifacts),
        'screenshot_count': sum(item.get('screenshot_count', 0) for item in outdirs),
        'default_outdir': str(default_outdir.relative_to(ROOT)),
        'default_present': bool(latest_default),
        'default_configured': latest_default.get('configured') if latest_default else False,
        'default_configured_slug': latest_default.get('configured_slug') if latest_default else None,
        'default_stale': latest_default.get('stale') if latest_default else True,
        'default_latest_age_seconds': latest_default.get('latest_age_seconds') if latest_default else None,
        'default_latest_age_human': latest_default.get('latest_age_human') if latest_default else 'unknown',
        'default_has_windows_capture': latest_default.get('has_windows_capture') if latest_default else False,
        'default_metadata_present': latest_default.get('metadata_present') if latest_default else False,
        'default_metadata_success': latest_default.get('metadata_success') if latest_default else None,
        'default_metadata_checked_at': latest_default.get('metadata_checked_at') if latest_default else None,
        'default_metadata_age_seconds': latest_default.get('metadata_age_seconds') if latest_default else None,
        'default_metadata_age_human': latest_default.get('metadata_age_human') if latest_default else 'unknown',
        'default_metadata_url': latest_default.get('metadata_url') if latest_default else None,
        'default_metadata_duration_seconds': latest_default.get('metadata_duration_seconds') if latest_default else None,
        'default_metadata_window_count': latest_default.get('metadata_window_count') if latest_default else None,
        'default_metadata_error': latest_default.get('metadata_error') if latest_default else '',
        'latest_screenshot': (latest_default or {}).get('latest_screenshot'),
        'freshest_age_seconds': freshest,
        'freshest_age_human': fmt_age(freshest),
        'stalest_age_seconds': stalest,
        'stalest_age_human': fmt_age(stalest),
        'recommended_command': configured_recommended_actions[0]['recommended_command'] if configured_recommended_actions else (None if operationally_healthy else DEFAULT_COMMAND),
        'recommended_stack_command': configured_recommended_actions[0].get('stack_command') if configured_recommended_actions else None,
        'internal_recommended_command': configured_recommended_actions[0]['internal_command'] if configured_recommended_actions else (None if operationally_healthy else DEFAULT_INTERNAL_COMMAND),
        'display_scope': display_scope,
        'display_path': display_outdir.get('path') if display_outdir else None,
        'display_slug': display_outdir.get('configured_slug') or display_outdir.get('slug') if display_outdir else None,
        'display_latest_age_seconds': display_outdir.get('latest_age_seconds') if display_outdir else None,
        'display_latest_age_human': display_outdir.get('latest_age_human') if display_outdir else 'unknown',
        'display_metadata_checked_at': display_outdir.get('metadata_checked_at') if display_outdir else None,
        'display_metadata_age_seconds': display_outdir.get('metadata_age_seconds') if display_outdir else None,
        'display_metadata_age_human': display_outdir.get('metadata_age_human') if display_outdir else 'unknown',
        'display_screenshot_count': display_outdir.get('screenshot_count') if display_outdir else 0,
        'display_has_windows_capture': display_outdir.get('has_windows_capture') if display_outdir else False,
        'display_metadata_url': display_outdir.get('metadata_url') if display_outdir else None,
        'display_metadata_duration_seconds': display_outdir.get('metadata_duration_seconds') if display_outdir else None,
        'display_metadata_window_count': display_outdir.get('metadata_window_count') if display_outdir else None,
        'display_metadata_error': display_outdir.get('metadata_error') if display_outdir else '',
        'display_latest_screenshot': display_outdir.get('latest_screenshot') if display_outdir else None,
        'outdirs': outdirs,
    }


def render_text(summary):
    lines = ['Desktop fallback status']
    lines.append(
        f"- healthy: {summary.get('healthy')} | overall: {summary.get('overall_healthy')} | operational: {summary.get('operationally_healthy')} | outdirs: {summary.get('outdir_count')} | stale outdirs: {summary.get('stale_outdir_count')} (configured {summary.get('configured_stale_outdir_count')}, unmanaged {summary.get('unmanaged_stale_outdir_count')}) | artifacts: {summary.get('artifact_count')} | screenshots: {summary.get('screenshot_count')} | freshest: {summary.get('freshest_age_human')} | stalest: {summary.get('stalest_age_human')}"
    )
    lines.append(
        f"- default: present={summary.get('default_present')} configured={summary.get('default_configured')} stale={summary.get('default_stale')} latest={summary.get('default_latest_age_human')} metadata={summary.get('default_metadata_present')} success={summary.get('default_metadata_success')} windows={summary.get('default_has_windows_capture')}"
    )
    lines.append(
        f"- display: scope={summary.get('display_scope')} path={summary.get('display_path') or '-'} slug={summary.get('display_slug') or '-'} latest={summary.get('display_latest_age_human')} metadata={summary.get('display_metadata_age_human')} screenshots={summary.get('display_screenshot_count')} windows={summary.get('display_has_windows_capture')}"
    )
    probe_checked_at = summary.get('display_metadata_checked_at') or summary.get('default_metadata_checked_at')
    probe_age = summary.get('display_metadata_age_human') or summary.get('default_metadata_age_human')
    probe_url = summary.get('display_metadata_url') or summary.get('default_metadata_url')
    probe_duration = summary.get('display_metadata_duration_seconds')
    if probe_duration is None:
        probe_duration = summary.get('default_metadata_duration_seconds')
    probe_windows = summary.get('display_metadata_window_count')
    if probe_windows is None:
        probe_windows = summary.get('default_metadata_window_count')
    if probe_checked_at:
        lines.append(
            f"- last probe ({summary.get('display_scope')}): {probe_checked_at} ({probe_age}), url={probe_url or '-'}, duration={probe_duration if probe_duration is not None else '-'}s, windows={probe_windows if probe_windows is not None else '-'}"
        )
    probe_error = summary.get('display_metadata_error') or summary.get('default_metadata_error')
    if probe_error:
        lines.append(f"- last error ({summary.get('display_scope')}): {probe_error}")
    latest_screenshot = summary.get('display_latest_screenshot') or summary.get('latest_screenshot') or {}
    if latest_screenshot.get('path'):
        lines.append(f"- screenshot ({summary.get('display_scope')}): {latest_screenshot.get('path')} ({latest_screenshot.get('age_human')})")
    if summary.get('stale_outdirs'):
        lines.append(f"- stale outdirs: {', '.join(summary.get('stale_outdirs')[:5])}")
    missing_targets = summary.get('missing_configured_targets') or []
    if missing_targets:
        lines.append(
            "- missing managed targets: " + ', '.join(
                item.get('slug') or item.get('path') or '-' for item in missing_targets[:5]
            )
        )
    if summary.get('unmanaged_stale_outdir_count') and not summary.get('configured_attention_target_count'):
        lines.append('- nuance: alleen onbeheerde/demo desktop-artifacts zijn stale, beheerde desktop fallbacks zijn operationeel gezond')
    if summary.get('recommended_command'):
        lines.append(f"- refresh: {summary.get('recommended_command')}")
    configured_overrides = [
        item for item in summary.get('outdirs', [])
        if item.get('configured') and item.get('stale_after_seconds') not in (None, summary.get('stale_after_seconds'))
    ]
    if configured_overrides:
        lines.append(
            "- stale overrides: " + ', '.join(
                f"{item.get('configured_slug') or item.get('slug')}={item.get('stale_after_seconds')}s(+{item.get('stale_grace_seconds')}s)"
                for item in configured_overrides[:5]
            )
        )
    return '\n'.join(lines)


def main():
    parser = argparse.ArgumentParser(description='Compact observability-overzicht van de desktop fallback artifacts')
    parser.add_argument('--json', action='store_true')
    parser.add_argument('--stale-after', type=int, default=DEFAULT_STALE_AFTER_SECONDS)
    parser.add_argument('--stale-grace', type=int, default=DEFAULT_STALE_GRACE_SECONDS, help='extra grace bovenop stale-after om flappen rond de drempel te voorkomen')
    parser.add_argument('--slug', help='toon/gebruik specifiek desktop fallback target via out-desktop-<slug>')
    parser.add_argument('--outdir', help='toon/gebruik specifiek output-directory pad in plaats van de standaard out-desktop')
    parser.add_argument('--configured-only', action='store_true', help='toon alleen expliciet beheerde desktop fallback targets uit de registry')
    parser.add_argument('--adapter', action='append', help='filter op configured desktop target adapter(s), herhaalbaar, bijvoorbeeld --adapter github --adapter slack')
    args = parser.parse_args()

    default_outdir = DEFAULT_OUTDIR
    only_outdirs = None
    if args.slug:
        default_outdir = slug_to_outdir(args.slug)
        only_outdirs = [default_outdir]
    if args.outdir:
        default_outdir = (Path(args.outdir) if Path(args.outdir).is_absolute() else (ROOT / args.outdir)).resolve()
        only_outdirs = [default_outdir]

    summary = build_summary(
        stale_after_seconds=args.stale_after,
        default_outdir=default_outdir,
        only_outdirs=only_outdirs,
        stale_grace_seconds=max(0, args.stale_grace),
        adapter_filter=args.adapter,
        configured_only=args.configured_only,
    )
    if args.json:
        print(json.dumps(summary, ensure_ascii=False, indent=2))
    else:
        print(render_text(summary))


if __name__ == '__main__':
    main()
