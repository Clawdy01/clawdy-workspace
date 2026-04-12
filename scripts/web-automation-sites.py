#!/usr/bin/env python3
import argparse
import json
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from shlex import quote
from urllib.parse import urlparse

ROOT = Path('/home/clawdy/.openclaw/workspace')
BROWSER = ROOT / 'browser-automation'
ARTIFACT_DIR = BROWSER / 'out'
SITE_REGISTRY = ROOT / 'state' / 'web-automation-sites.json'
PROTON_NEXT = ROOT / 'scripts' / 'proton-next-step.py'
DESKTOP_STATUS = ROOT / 'scripts' / 'desktop-fallback-status.py'
DISPATCH = ROOT / 'scripts' / 'web-automation-dispatch.py'
DEFAULT_STALE_AFTER_SECONDS = 900
DEFAULT_STALE_GRACE_SECONDS = 60

KNOWN_SITES = {
    'account.proton.me': {'adapter': 'proton', 'label': 'Proton'},
    'proton.me': {'adapter': 'proton', 'label': 'Proton'},
    'app.slack.com': {'adapter': 'slack', 'label': 'Slack'},
    'slack.com': {'adapter': 'slack', 'label': 'Slack'},
    'notion.so': {'adapter': 'notion', 'label': 'Notion'},
    'www.notion.so': {'adapter': 'notion', 'label': 'Notion'},
    'github.com': {'adapter': 'github', 'label': 'GitHub'},
    'bitwarden.com': {'adapter': 'bitwarden', 'label': 'Bitwarden'},
    'vault.bitwarden.com': {'adapter': 'bitwarden', 'label': 'Bitwarden vault'},
    'vault.bitwarden.eu': {'adapter': 'bitwarden', 'label': 'Bitwarden vault'},
}


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


def read_json(path):
    try:
        return json.loads(path.read_text())
    except Exception:
        return {}


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


def load_dispatch_catalog():
    payload = run_json(['python3', str(DISPATCH), 'catalog', '--json'], default=None)
    if not payload:
        return {'routes': set(), 'aliases': {}, 'available': False}
    return {
        'routes': {route.get('name') for route in payload.get('routes') or [] if route.get('name')},
        'aliases': payload.get('aliases') or {},
        'available': True,
    }


def validate_registry_item(item, catalog):
    warnings = []
    route = str(item.get('route') or '').strip()
    refresh_command = str(item.get('refresh_command') or '').strip()
    url = str(item.get('url') or '').strip()
    if route and catalog.get('available') and route not in catalog.get('routes', set()) and route not in (catalog.get('aliases') or {}):
        warnings.append(f'onbekende dispatch-route: {route}')
    if route and not catalog.get('available'):
        warnings.append('dispatch catalog niet beschikbaar voor route-validatie')
    if item.get('route_args') is not None and not isinstance(item.get('route_args'), list):
        warnings.append('routeArgs moet een lijst zijn')
    if item.get('probe_args') is not None and not isinstance(item.get('probe_args'), list):
        warnings.append('probeArgs moet een lijst zijn')
    if not (url or route or refresh_command):
        warnings.append('mist URL/route/refreshCommand')
    return warnings


def load_registry():
    raw = read_json(SITE_REGISTRY)
    if isinstance(raw, dict):
        entries = raw.get('sites') if isinstance(raw.get('sites'), list) else raw.get('items')
    elif isinstance(raw, list):
        entries = raw
    else:
        entries = []

    catalog = load_dispatch_catalog()
    registry = {}
    for item in entries or []:
        if not isinstance(item, dict):
            continue
        slug = str(item.get('slug') or '').strip().lower()
        url = str(item.get('url') or '').strip()
        route = str(item.get('route') or '').strip()
        refresh_command = str(item.get('refreshCommand') or '').strip()
        if not slug or (not url and not route and not refresh_command) or item.get('enabled', True) is False:
            continue
        record = {
            'slug': slug,
            'url': url,
            'label': item.get('label'),
            'adapter': item.get('adapter'),
            'host': item.get('host') or (urlparse(url).netloc or '').lower(),
            'notes': item.get('notes') or item.get('note') or '',
            'route': route,
            'route_args': item.get('routeArgs') if isinstance(item.get('routeArgs'), list) else ([str(item.get('routeArgs'))] if item.get('routeArgs') else []),
            'probe_args': item.get('probeArgs') if isinstance(item.get('probeArgs'), list) else ([str(item.get('probeArgs'))] if item.get('probeArgs') else []),
            'refresh_command': refresh_command,
            'stale_after_seconds': int(item.get('staleAfterSeconds')) if str(item.get('staleAfterSeconds') or '').isdigit() and int(item.get('staleAfterSeconds')) > 0 else None,
            'desktop_keep_screenshots': int(item.get('desktopKeepScreenshots')) if str(item.get('desktopKeepScreenshots') or '').isdigit() and int(item.get('desktopKeepScreenshots')) > 0 else None,
        }
        record['validation_warnings'] = validate_registry_item(record, catalog)
        registry[slug] = record
    return registry


def fallback_checked_at(path):
    try:
        return datetime.fromtimestamp(path.stat().st_mtime, tz=timezone.utc)
    except Exception:
        return None


def classify_site(url, slug):
    host = (urlparse(url).netloc or '').lower()
    for known_host, info in KNOWN_SITES.items():
        if host == known_host or host.endswith(f'.{known_host}'):
            return {
                'host': host,
                'adapter': info['adapter'],
                'label': info['label'],
            }
    label = host or slug or 'unknown'
    adapter = (slug or host or 'generic').split('-', 1)[0]
    return {
        'host': host,
        'adapter': adapter,
        'label': label,
    }


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


def shell_join(parts):
    return ' '.join(quote(str(part)) for part in parts if str(part).strip())


def build_internal_refresh_command(configured, url, slug):
    if configured and configured.get('refresh_command'):
        return configured['refresh_command']
    if configured and configured.get('route'):
        return shell_join(['python3', 'scripts/web-automation-dispatch.py', configured['route'], *(configured.get('route_args') or [])])
    if not url:
        return None
    cmd = ['python3', 'scripts/web-automation-dispatch.py', 'probe-page', url, *(configured.get('probe_args') or [])] if configured else ['python3', 'scripts/web-automation-dispatch.py', 'probe-page', url]
    if slug:
        cmd += ['--slug', slug]
    return shell_join(cmd)


def build_refresh_command(configured, url, slug):
    if configured and slug:
        return shell_join(['python3', 'scripts/web-automation-dispatch.py', 'refresh-sites', '--configured-only', '--slug', slug])
    return build_internal_refresh_command(configured, url, slug)


def build_refresh_stack_command(configured, slug):
    if configured and slug:
        return shell_join(['python3', 'scripts/web-automation-dispatch.py', 'refresh-stack', '--configured-only', '--slug', slug])
    return None


def proton_overlay():
    summary = run_json(['python3', str(PROTON_NEXT), '--json'], default={}) or {}
    if not summary:
        return {}

    verification = summary.get('verification') or {}
    recommended_route = summary.get('recommended_route')
    recommended_command = summary.get('recommended_command')
    terminal_manual = recommended_route == 'account-created'
    return {
        'workflow_state': recommended_route or summary.get('phase') or 'unknown',
        'workflow_terminal': terminal_manual,
        'workflow_attention': 'manual' if terminal_manual else ('none' if recommended_route == 'noop' else 'automation'),
        'workflow_note': summary.get('reason') or '',
        'workflow_checked_at': verification.get('checked_at') or None,
        'workflow_age_seconds': verification.get('age_seconds'),
        'workflow_stale': summary.get('verification_stale') if verification else summary.get('stale'),
        'workflow_command': recommended_command or None,
        'handoff_command': recommended_command or None,
    }


def desktop_overlay_by_slug():
    registry = load_registry()
    registry_by_slug = registry or {}
    summary = run_json(['python3', str(DESKTOP_STATUS), '--json'], default={}) or {}
    outdirs = summary.get('outdirs') or []
    overlay = {}
    for item in outdirs:
        if not isinstance(item, dict) or not item.get('configured'):
            continue
        slug = str(item.get('configured_slug') or item.get('slug') or '').strip().lower()
        if not slug:
            continue
        configured = registry_by_slug.get(slug) or {}
        keep_screenshots = configured.get('desktop_keep_screenshots')
        recommended_parts = ['python3', 'scripts/web-automation-dispatch.py', 'refresh-desktop', '--configured-only', '--slug', slug]
        if keep_screenshots:
            recommended_parts.extend(['--keep-screenshots', str(keep_screenshots)])
        recommended = shell_join(recommended_parts)
        stack_command = build_refresh_stack_command(configured, slug)
        overlay[slug] = {
            'desktop_configured': True,
            'desktop_path': item.get('path'),
            'desktop_age_seconds': item.get('metadata_age_seconds') if item.get('metadata_age_seconds') is not None else item.get('latest_age_seconds'),
            'desktop_age_human': item.get('metadata_age_human') if item.get('metadata_age_human') not in (None, 'unknown') else item.get('latest_age_human'),
            'desktop_stale': bool(item.get('stale')),
            'desktop_screenshot_count': item.get('screenshot_count'),
            'desktop_metadata_success': item.get('metadata_success'),
            'desktop_url': item.get('metadata_url') or item.get('configured_url'),
            'desktop_command': recommended,
            'stack_command': stack_command,
            'desktop_keep_screenshots': keep_screenshots,
            'desktop_healthy': bool(
                not item.get('stale')
                and item.get('screenshot_count')
                and item.get('metadata_success', True) is not False
            ),
        }
    return overlay


def apply_adapter_overlay(item, adapter_overlays):
    overlay = adapter_overlays.get(item.get('adapter')) or {}
    if not overlay:
        return item

    updated = dict(item)
    updated.update({k: v for k, v in overlay.items() if v not in (None, '')})
    return updated


def apply_desktop_overlay(item, desktop_overlays):
    slug = str(item.get('slug') or '').strip().lower()
    overlay = desktop_overlays.get(slug) or {}
    if not overlay:
        return item

    updated = dict(item)
    updated.update({k: v for k, v in overlay.items() if v not in (None, '')})
    return updated


def site_stale_after(item, default_stale_after_seconds):
    override = item.get('stale_after_seconds')
    if isinstance(override, int) and override > 0:
        return override
    return default_stale_after_seconds


def stale_grace_seconds_for(item, default_grace_seconds):
    age_seconds = item.get('age_seconds')
    if age_seconds is None:
        return default_grace_seconds
    site_stale_after_seconds = site_stale_after(item, DEFAULT_STALE_AFTER_SECONDS)
    proportional = max(0, int(site_stale_after_seconds * 0.05))
    return max(default_grace_seconds, proportional)


def apply_freshness(item, default_stale_after_seconds, stale_grace_seconds=DEFAULT_STALE_GRACE_SECONDS):
    updated = dict(item)
    effective_stale_after = site_stale_after(updated, default_stale_after_seconds)
    effective_stale_grace = stale_grace_seconds_for(updated, stale_grace_seconds)
    age_seconds = updated.get('age_seconds')
    dom_stale = age_seconds is None or age_seconds > (effective_stale_after + effective_stale_grace)
    updated['stale_after_seconds'] = effective_stale_after
    updated['stale_grace_seconds'] = effective_stale_grace
    updated['dom_stale'] = dom_stale
    updated['dom_healthy'] = not dom_stale and not updated.get('missing_artifact')

    if updated.get('workflow_terminal'):
        updated['stale'] = False
        updated['attention_needed'] = False
        updated['healthy_state'] = True
        updated['operationally_healthy'] = True
        updated['recommended_command'] = updated.get('handoff_command') or updated.get('workflow_command') or updated.get('recommended_command')
        return updated

    desktop_healthy = bool(updated.get('desktop_healthy'))
    operationally_healthy = bool(updated.get('dom_healthy') or desktop_healthy)
    updated['stale'] = not operationally_healthy
    updated['attention_needed'] = not operationally_healthy
    updated['healthy_state'] = operationally_healthy
    updated['operationally_healthy'] = operationally_healthy
    if updated.get('dom_stale') and updated.get('desktop_stale') and updated.get('stack_command'):
        updated['recommended_command'] = updated.get('stack_command')
    elif desktop_healthy and updated.get('dom_stale') and not updated.get('recommended_command') and updated.get('desktop_command'):
        updated['recommended_command'] = updated.get('desktop_command')
    return updated


def adapter_matches(item, adapter_filter):
    if not adapter_filter:
        return True
    adapter = str(item.get('adapter') or '').strip().lower()
    return adapter in adapter_filter


def slug_matches(item, slug_filter):
    if not slug_filter:
        return True
    slug = str(item.get('slug') or '').strip().lower()
    return slug in slug_filter



def build_summary(
    stale_after_seconds=DEFAULT_STALE_AFTER_SECONDS,
    configured_only=False,
    adapter_filter=None,
    slug_filter=None,
    attention_only=False,
    stale_grace_seconds=DEFAULT_STALE_GRACE_SECONDS,
):
    now = datetime.now(timezone.utc)
    registry = load_registry()
    adapter_overlays = {
        'proton': proton_overlay(),
    }
    desktop_overlays = desktop_overlay_by_slug()
    probe_items = []

    if ARTIFACT_DIR.exists():
        for json_path in sorted(ARTIFACT_DIR.glob('probe*.json')):
            data = read_json(json_path)
            url = data.get('url') or data.get('finalUrl') or ''
            slug = (data.get('slug') or (json_path.stem.removeprefix('probe-') if json_path.stem.startswith('probe-') else 'probe')).strip().lower()
            site = classify_site(url, slug)
            configured = registry.get(slug, {})
            checked_at = parse_iso(data.get('checkedAt') or data.get('checked_at')) or fallback_checked_at(json_path)
            age_seconds = int((now - checked_at).total_seconds()) if checked_at else None
            png_path = json_path.with_suffix('.png')
            effective_url = configured.get('url') or url
            probe_items.append({
                'slug': slug,
                'label': configured.get('label') or site['label'],
                'adapter': configured.get('adapter') or site['adapter'],
                'host': configured.get('host') or site['host'],
                'url': effective_url,
                'final_url': data.get('finalUrl') or effective_url,
                'title': data.get('title'),
                'checked_at': checked_at.isoformat().replace('+00:00', 'Z') if checked_at else None,
                'age_seconds': age_seconds,
                'age_human': fmt_age(age_seconds),
                'missing_artifact': False,
                'interactive_count': data.get('interactiveCount'),
                'form_count': data.get('formCount'),
                'body_preview': (data.get('bodyText') or '').strip()[:220],
                'json_path': str(json_path.relative_to(ROOT)),
                'png_path': str(png_path.relative_to(ROOT)) if png_path.exists() else None,
                'recommended_command': build_refresh_command(configured, effective_url, slug),
                'refresh_command': build_internal_refresh_command(configured, effective_url, slug),
                'route': configured.get('route'),
                'route_args': configured.get('route_args') or [],
                'probe_args': configured.get('probe_args') or [],
                'notes': configured.get('notes') or '',
                'configured': bool(configured),
                'stale_after_seconds': configured.get('stale_after_seconds'),
                'matched_registry_slug': slug if configured else None,
                'url_normalized': normalize_url(effective_url),
                'final_url_normalized': normalize_url(data.get('finalUrl') or effective_url),
            })

    items_by_slug = {}
    claimed_probe_slugs = set()

    for slug, configured in registry.items():
        matched = next((item for item in probe_items if item['slug'] == slug), None)
        if not matched and configured.get('url'):
            configured_url = normalize_url(configured.get('url'))
            matched = next(
                (
                    item for item in probe_items
                    if item['slug'] not in claimed_probe_slugs and configured_url and configured_url in {item.get('url_normalized'), item.get('final_url_normalized')}
                ),
                None,
            )

        if matched:
            claimed_probe_slugs.add(matched['slug'])
            items_by_slug[slug] = {
                **{k: v for k, v in matched.items() if k not in {'url_normalized', 'final_url_normalized', 'matched_registry_slug'}},
                'slug': slug,
                'label': configured.get('label') or matched.get('label'),
                'adapter': configured.get('adapter') or matched.get('adapter'),
                'host': configured.get('host') or matched.get('host'),
                'url': configured.get('url') or matched.get('url'),
                'recommended_command': build_refresh_command(configured, configured.get('url') or matched.get('url'), slug),
                'refresh_command': build_internal_refresh_command(configured, configured.get('url') or matched.get('url'), slug),
                'route': configured.get('route'),
                'route_args': configured.get('route_args') or [],
                'probe_args': configured.get('probe_args') or [],
                'notes': configured.get('notes') or matched.get('notes') or '',
                'configured': True,
                'validation_warnings': configured.get('validation_warnings') or [],
            }
            continue

        site = classify_site(configured.get('url'), slug)
        effective_url = configured.get('url') or ''
        items_by_slug[slug] = {
            'slug': slug,
            'label': configured.get('label') or site['label'],
            'adapter': configured.get('adapter') or site['adapter'],
            'host': configured.get('host') or site['host'],
            'url': effective_url,
            'final_url': effective_url,
            'title': None,
            'checked_at': None,
            'age_seconds': None,
            'age_human': fmt_age(None),
            'missing_artifact': True,
            'interactive_count': None,
            'form_count': None,
            'body_preview': '',
            'json_path': None,
            'png_path': None,
            'recommended_command': build_refresh_command(configured, effective_url, slug),
            'refresh_command': build_internal_refresh_command(configured, effective_url, slug),
            'route': configured.get('route'),
            'route_args': configured.get('route_args') or [],
            'probe_args': configured.get('probe_args') or [],
            'notes': configured.get('notes') or '',
            'configured': True,
            'stale_after_seconds': configured.get('stale_after_seconds'),
            'validation_warnings': configured.get('validation_warnings') or [],
        }

    for item in probe_items:
        if item['slug'] in claimed_probe_slugs or item['slug'] in items_by_slug:
            continue
        items_by_slug[item['slug']] = {k: v for k, v in item.items() if k not in {'url_normalized', 'final_url_normalized', 'matched_registry_slug'}}

    items = [
        apply_freshness(
            apply_desktop_overlay(
                apply_adapter_overlay(item, adapter_overlays),
                desktop_overlays,
            ),
            stale_after_seconds,
            stale_grace_seconds=stale_grace_seconds,
        )
        for item in items_by_slug.values()
    ]
    for item in items:
        warnings = item.get('validation_warnings') or []
        if warnings:
            item['attention_needed'] = True
            item['healthy_state'] = False
            item['stale'] = True
    if configured_only:
        items = [item for item in items if item.get('configured')]
    if adapter_filter:
        items = [item for item in items if adapter_matches(item, adapter_filter)]
    if slug_filter:
        items = [item for item in items if slug_matches(item, slug_filter)]
    if attention_only:
        items = [item for item in items if item.get('attention_needed', item.get('stale'))]

    items = sorted(
        items,
        key=lambda item: (
            not item.get('configured', False),
            not item.get('attention_needed', item.get('stale')),
            item['age_seconds'] is None,
            -(item['age_seconds'] or 0),
            item['slug'],
        )
    )
    stale_count = sum(1 for item in items if item.get('attention_needed', item.get('stale')))
    adapters = sorted({item['adapter'] for item in items if item.get('adapter')})
    missing_artifact_count = sum(1 for item in items if item.get('missing_artifact'))
    configured_items = [item for item in items if item.get('configured')]
    unmanaged_items = [item for item in items if not item.get('configured')]
    configured_stale_count = sum(1 for item in configured_items if item.get('attention_needed', item.get('stale')))
    unmanaged_stale_count = sum(1 for item in unmanaged_items if item.get('attention_needed', item.get('stale')))
    operationally_healthy = configured_stale_count == 0
    age_values = [item.get('age_seconds') for item in items if item.get('age_seconds') is not None]
    freshest = min(age_values) if age_values else None
    stalest = max(age_values) if age_values else None

    adapter_summaries = []
    for adapter in adapters:
        adapter_items = [item for item in items if item.get('adapter') == adapter]
        adapter_configured = [item for item in adapter_items if item.get('configured')]
        adapter_unmanaged = [item for item in adapter_items if not item.get('configured')]
        adapter_stale = [item for item in adapter_items if item.get('attention_needed', item.get('stale'))]
        adapter_configured_stale = [item for item in adapter_configured if item.get('attention_needed', item.get('stale'))]
        adapter_age_values = [item.get('age_seconds') for item in adapter_items if item.get('age_seconds') is not None]
        freshest_adapter = min(adapter_age_values) if adapter_age_values else None
        stalest_adapter = max(adapter_age_values) if adapter_age_values else None
        latest_item = next((item for item in adapter_items if item.get('age_seconds') is not None), None)
        next_attention_item = next((item for item in adapter_items if item.get('attention_needed', item.get('stale'))), None)
        adapter_summaries.append({
            'adapter': adapter,
            'site_count': len(adapter_items),
            'configured_site_count': len(adapter_configured),
            'unmanaged_site_count': len(adapter_unmanaged),
            'stale_site_count': len(adapter_stale),
            'configured_stale_site_count': len(adapter_configured_stale),
            'unmanaged_stale_site_count': sum(1 for item in adapter_unmanaged if item.get('attention_needed', item.get('stale'))),
            'missing_artifact_count': sum(1 for item in adapter_items if item.get('missing_artifact')),
            'operationally_healthy': not adapter_configured_stale,
            'healthy': not adapter_stale,
            'freshest_age_human': fmt_age(freshest_adapter),
            'latest_age_human': latest_item.get('age_human') if latest_item else 'unknown',
            'stalest_age_human': fmt_age(stalest_adapter),
            'latest_slug': latest_item.get('slug') if latest_item else None,
            'next_attention_slug': next_attention_item.get('slug') if next_attention_item else None,
            'next_attention_command': next_attention_item.get('recommended_command') if next_attention_item else None,
        })
    adapter_summaries.sort(key=lambda item: (not item.get('configured_stale_site_count', 0), not item.get('stale_site_count', 0), item.get('adapter') or ''))

    return {
        'site_count': len(items),
        'invalid_site_count': sum(1 for item in items if item.get('validation_warnings')),
        'configured_site_count': len(configured_items),
        'unmanaged_site_count': len(unmanaged_items),
        'missing_artifact_count': missing_artifact_count,
        'stale_site_count': stale_count,
        'configured_stale_site_count': configured_stale_count,
        'unmanaged_stale_site_count': unmanaged_stale_count,
        'healthy': stale_count == 0,
        'configured_healthy': operationally_healthy,
        'operationally_healthy': operationally_healthy,
        'configured_only': configured_only,
        'stale_after_seconds': stale_after_seconds,
        'registry_path': str(SITE_REGISTRY.relative_to(ROOT)),
        'stale_grace_seconds': stale_grace_seconds,
        'freshest_age_human': fmt_age(freshest),
        'stalest_age_human': fmt_age(stalest),
        'adapters': adapters,
        'adapter_summaries': adapter_summaries,
        'sites': items,
    }


def render_text(summary):
    lines = ['Web automation sites']
    lines.append(
        f"- healthy: {summary.get('healthy')} | operational: {summary.get('operationally_healthy')} | sites: {summary.get('site_count')} | configured: {summary.get('configured_site_count')} | unmanaged: {summary.get('unmanaged_site_count')} | invalid: {summary.get('invalid_site_count')} | missing artifacts: {summary.get('missing_artifact_count')} | stale: {summary.get('stale_site_count')} (configured {summary.get('configured_stale_site_count')}, unmanaged {summary.get('unmanaged_stale_site_count')}) | freshest: {summary.get('freshest_age_human')} | stalest: {summary.get('stalest_age_human')} | adapters: {', '.join(summary.get('adapters') or ['geen'])}"
    )
    adapter_summaries = summary.get('adapter_summaries') or []
    if adapter_summaries:
        preview = ', '.join(
            f"{item.get('adapter')}:{item.get('site_count')}"
            + (f" latest={item.get('latest_age_human')}" if item.get('latest_age_human') else '')
            + (f" stale={item.get('stale_site_count')}" if item.get('stale_site_count') else '')
            + (f" cfg={item.get('configured_stale_site_count')}" if item.get('configured_stale_site_count') else '')
            + (f" -> {item.get('next_attention_slug')}" if item.get('next_attention_slug') else '')
            for item in adapter_summaries[:4]
        )
        lines.append(f"- adapter health: {preview}")
    for site in summary.get('sites', []):
        preview = site.get('body_preview') or 'geen tekst'
        if len(preview) > 90:
            preview = preview[:87] + '...'
        missing_suffix = ' (nog niet geprobed)' if site.get('missing_artifact') else ''
        stale_hint = f", stale-after={site.get('stale_after_seconds')}s(+{site.get('stale_grace_seconds')}s grace)" if site.get('stale_after_seconds') else ''
        workflow_suffix = ''
        if site.get('workflow_state'):
            workflow_suffix = f", workflow={site.get('workflow_state')}"
            if site.get('workflow_terminal'):
                workflow_suffix += ' (manual boundary)'
        desktop_suffix = ''
        if site.get('desktop_configured'):
            desktop_suffix = f", desktop={site.get('desktop_age_human') or 'unknown'}"
            desktop_suffix += ' healthy' if site.get('desktop_healthy') else ' stale'
        lines.append(
            f"- {site.get('slug')}: {site.get('label')} [{site.get('adapter')}] {site.get('age_human')}{missing_suffix}, forms={site.get('form_count')}, interactives={site.get('interactive_count')}, title={site.get('title') or '-'}{stale_hint}{workflow_suffix}{desktop_suffix}"
        )
        lines.append(f"  - url: {site.get('final_url') or site.get('url') or '-'}")
        lines.append(f"  - preview: {preview}")
        if site.get('notes'):
            lines.append(f"  - notes: {site.get('notes')}")
        if site.get('validation_warnings'):
            lines.append(f"  - warnings: {'; '.join(site.get('validation_warnings') or [])}")
        if site.get('workflow_note'):
            lines.append(f"  - workflow: {site.get('workflow_note')}")
        if site.get('desktop_configured'):
            lines.append(
                f"  - desktop: {site.get('desktop_path') or '-'} ({site.get('desktop_age_human') or 'unknown'}, {'healthy' if site.get('desktop_healthy') else 'stale'})"
            )
        if site.get('workflow_terminal') and site.get('handoff_command'):
            lines.append(f"  - handoff: {site.get('handoff_command')}")
        elif site.get('attention_needed', site.get('stale')) and site.get('recommended_command'):
            lines.append(f"  - refresh: {site.get('recommended_command')}")
            if site.get('stack_command') and site.get('desktop_stale'):
                lines.append(f"  - full stack: {site.get('stack_command')}")
        elif site.get('dom_stale') and site.get('desktop_healthy') and site.get('desktop_command'):
            lines.append(f"  - desktop fallback beschikbaar: {site.get('desktop_command')}")
    for item in adapter_summaries[:4]:
        if item.get('next_attention_command'):
            lines.append(f"  - adapter refresh {item.get('adapter')}: {item.get('next_attention_command')}")
    return '\n'.join(lines)


def main():
    parser = argparse.ArgumentParser(description='Overzicht van generieke web probe sites en hun laatste artifacts')
    parser.add_argument('--json', action='store_true')
    parser.add_argument('--stale-after', type=int, default=DEFAULT_STALE_AFTER_SECONDS)
    parser.add_argument('--stale-grace', type=int, default=DEFAULT_STALE_GRACE_SECONDS, help='extra grace bovenop stale-after om flappen rond de drempel te voorkomen')
    parser.add_argument('--configured-only', action='store_true', help='toon alleen expliciet beheerde registry-sites')
    parser.add_argument('--adapter', action='append', help='filter op adapter(s), herhaalbaar, bijvoorbeeld --adapter slack --adapter github')
    parser.add_argument('--slug', action='append', help='filter op specifieke slug(s), herhaalbaar, bijvoorbeeld --slug github-login')
    parser.add_argument('--attention-only', action='store_true', help='toon alleen sites die nu aandacht of refresh nodig hebben')
    args = parser.parse_args()

    adapter_filter = {str(item).strip().lower() for item in (args.adapter or []) if str(item).strip()}
    slug_filter = {str(item).strip().lower() for item in (args.slug or []) if str(item).strip()}
    summary = build_summary(
        stale_after_seconds=args.stale_after,
        configured_only=args.configured_only,
        adapter_filter=adapter_filter,
        slug_filter=slug_filter,
        attention_only=args.attention_only,
        stale_grace_seconds=max(0, args.stale_grace),
    )
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
