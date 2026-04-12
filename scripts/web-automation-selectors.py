#!/usr/bin/env python3
import argparse
import json
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path('/home/clawdy/.openclaw/workspace')
ARTIFACT_DIR = ROOT / 'browser-automation' / 'out'
REGISTRY_PATH = ROOT / 'state' / 'web-automation-sites.json'

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


def read_json(path):
    try:
        return json.loads(path.read_text())
    except Exception:
        return {}


def normalize_slug(value):
    return str(value or '').strip().lower()


def classify_site(url, slug):
    host = (urlparse(url or '').netloc or '').lower()
    for known_host, info in KNOWN_SITES.items():
        if host == known_host or host.endswith(f'.{known_host}'):
            return {
                'host': host,
                'adapter': info['adapter'],
                'label': info['label'],
            }
    adapter = (slug or host or 'generic').split('-', 1)[0]
    return {
        'host': host,
        'adapter': adapter,
        'label': host or slug or 'Unknown site',
    }


def load_registry():
    raw = read_json(REGISTRY_PATH)
    if isinstance(raw, dict):
        items = raw.get('sites') if isinstance(raw.get('sites'), list) else []
    elif isinstance(raw, list):
        items = raw
    else:
        items = []
    registry = {}
    for item in items:
        if not isinstance(item, dict):
            continue
        slug = normalize_slug(item.get('slug'))
        if slug:
            registry[slug] = item
    return registry


def selector_hints(item):
    hints = []
    if item.get('id'):
        hints.append(f"#{item['id']}")
    if item.get('name'):
        hints.append(f"[name=\"{item['name']}\"]")
    if item.get('role'):
        hints.append(f"[role=\"{item['role']}\"]")
    if item.get('href'):
        parsed = urlparse(item['href'])
        href_hint = parsed.path or item['href']
        if parsed.fragment:
            href_hint += f"#{parsed.fragment}"
        if href_hint:
            hints.append(f"href={href_hint}")
    if item.get('placeholder'):
        hints.append(f"placeholder={item['placeholder']}")
    if item.get('ariaLabel'):
        hints.append(f"aria={item['ariaLabel']}")
    if item.get('text'):
        hints.append(f"text={item['text'][:60]}")
    return hints[:4]


def item_score(item):
    score = 0
    text = str(item.get('text') or '').strip().lower()
    tag = str(item.get('tag') or '').upper()
    if item.get('visible'):
        score += 100
    if tag == 'INPUT':
        score += 45
    elif tag in {'BUTTON', 'TEXTAREA', 'SELECT'}:
        score += 35
    elif tag == 'A':
        score += 5
    if item.get('type') and item.get('type') != 'hidden':
        score += 15
    if item.get('id'):
        score += 15
    if item.get('name'):
        score += 15
    if item.get('placeholder'):
        score += 20
    if item.get('ariaLabel'):
        score += 10
    if item.get('href'):
        score += 5
    if text:
        score += min(len(text), 40) / 5
    if any(word in text for word in {'username', 'email', 'password', 'sign in', 'log in', 'continue', 'search'}):
        score += 18
    if text in {'skip to content', 'terms', 'privacy', 'docs', 'contact github', 'create an account'}:
        score -= 25
    if item.get('disabled'):
        score -= 8
    if item.get('type') == 'hidden':
        score -= 60
    return score


def clean_entry(item):
    text = str(item.get('text') or '').strip()
    if text == 'undefined':
        text = ''
    entry = {
        'tag': item.get('tag') or '',
        'type': item.get('type') or '',
        'role': item.get('role') or '',
        'id': item.get('id') or '',
        'name': item.get('name') or '',
        'text': text,
        'href': item.get('href') or '',
        'placeholder': item.get('placeholder') or '',
        'ariaLabel': item.get('ariaLabel') or '',
        'visible': bool(item.get('visible')),
        'disabled': bool(item.get('disabled')),
    }
    entry['selector_hints'] = selector_hints(entry)
    entry['score'] = round(item_score(entry), 2)
    return entry


def load_artifacts():
    registry = load_registry()
    rows = []
    for path in sorted(ARTIFACT_DIR.glob('probe*.json')):
        payload = read_json(path)
        if not isinstance(payload, dict):
            continue
        slug = normalize_slug(payload.get('slug') or (path.stem.removeprefix('probe-') if path.stem.startswith('probe-') else path.stem))
        url = payload.get('finalUrl') or payload.get('url') or ''
        site = classify_site(url, slug)
        configured = registry.get(slug) or {}
        rows.append({
            'slug': slug,
            'label': configured.get('label') or site.get('label') or slug,
            'adapter': configured.get('adapter') or site.get('adapter') or '',
            'url': url,
            'title': payload.get('title') or '',
            'checked_at': payload.get('checkedAt') or payload.get('checked_at'),
            'interactive_count': payload.get('interactiveCount') or len(payload.get('interactives') or []),
            'items': [clean_entry(item) for item in (payload.get('interactives') or []) if isinstance(item, dict)],
            'json_path': str(path.relative_to(ROOT)),
        })
    return rows


def build_summary(slugs=None, adapters=None, limit=12, include_hidden=False):
    slug_filter = {normalize_slug(value) for value in (slugs or []) if normalize_slug(value)}
    adapter_filter = {str(value).strip().lower() for value in (adapters or []) if str(value).strip()}
    artifacts = []
    for artifact in load_artifacts():
        if slug_filter and artifact.get('slug') not in slug_filter:
            continue
        if adapter_filter and str(artifact.get('adapter') or '').lower() not in adapter_filter:
            continue
        items = []
        for item in artifact.get('items') or []:
            if not include_hidden and (not item.get('visible') or item.get('type') == 'hidden'):
                continue
            items.append(item)
        items.sort(key=lambda item: (-item.get('score', 0), item.get('tag') or '', item.get('name') or '', item.get('id') or ''))
        enriched = dict(artifact)
        enriched['candidate_count'] = len(items)
        enriched['top_candidates'] = items[:limit]
        artifacts.append(enriched)
    artifacts.sort(key=lambda item: (item.get('adapter') or '', item.get('slug') or ''))
    return {
        'site_count': len(artifacts),
        'requested_slugs': sorted(slug_filter),
        'requested_adapters': sorted(adapter_filter),
        'include_hidden': bool(include_hidden),
        'limit': limit,
        'sites': artifacts,
    }


def render_text(summary):
    sites = summary.get('sites') or []
    if not sites:
        return 'Web automation selectors: geen probe-artifacts gevonden'
    lines = [f"Web automation selectors: {summary.get('site_count', 0)} site(s)"]
    for site in sites:
        lines.append(
            f"- {site.get('slug')}: {site.get('label')} [{site.get('adapter')}] | candidates {site.get('candidate_count', 0)}/{site.get('interactive_count', 0)}"
        )
        if site.get('title'):
            lines.append(f"  title={site.get('title')}")
        if site.get('checked_at'):
            lines.append(f"  checked={site.get('checked_at')}")
        for item in site.get('top_candidates') or []:
            bits = [bit for bit in [item.get('tag'), item.get('type') or None] if bit]
            head = '/'.join(bits) or item.get('tag') or 'node'
            hints = ', '.join(item.get('selector_hints') or []) or 'geen selector-hints'
            suffix = ' disabled' if item.get('disabled') else ''
            lines.append(f"  - {head}: {hints}{suffix}")
    return '\n'.join(lines)


def main():
    parser = argparse.ArgumentParser(description='Selector-hints uit web automation probe-artifacts voor sneller site-adapterwerk')
    parser.add_argument('--json', action='store_true')
    parser.add_argument('--slug', action='append', help='focus op specifieke slug(s), herhaalbaar')
    parser.add_argument('--adapter', action='append', help='focus op specifieke adapter(s), herhaalbaar')
    parser.add_argument('--limit', type=int, default=12, help='maximaal aantal kandidaat-controls per site')
    parser.add_argument('--include-hidden', action='store_true', help='toon ook verborgen/hidden controls voor debugging')
    args = parser.parse_args()

    summary = build_summary(
        slugs=args.slug,
        adapters=args.adapter,
        limit=max(1, min(args.limit, 50)),
        include_hidden=args.include_hidden,
    )
    if args.json:
        print(json.dumps(summary, ensure_ascii=False, indent=2))
    else:
        print(render_text(summary))


if __name__ == '__main__':
    main()
