#!/usr/bin/env python3
import argparse
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path('/home/clawdy/.openclaw/workspace')
BROWSER = ROOT / 'browser-automation'
PROTON_REGRESSION = ROOT / 'scripts' / 'proton-password-regression-report.py'

ROUTES = {
    'catalog': {
        'description': 'Toon beschikbare web automation routes en fallbacks',
        'layer': 'meta',
        'args': [],
        'examples': ['web-automation-dispatch.py catalog', 'web-automation-dispatch.py catalog --json'],
        'runner': None,
    },
    'probe-page': {
        'description': 'DOM/Playwright probe van een URL, optioneel met slug voor site-specifieke artifacts',
        'layer': 'dom',
        'args': ['url', '--slug <name>?', '--outdir <dir>?'],
        'examples': [
            'web-automation-dispatch.py probe-page https://account.proton.me/start',
            'web-automation-dispatch.py probe-page https://app.slack.com/signin --slug slack-signin',
        ],
        'runner': lambda value=None: ['node', str(BROWSER / 'probe_page.js')] + (value if isinstance(value, list) else [value]),
    },
    'artifacts': {
        'description': 'Toon compact overzicht van beschikbare web automation artifacts per adapter, inclusief stale health en refresh-advies',
        'layer': 'meta',
        'args': ['--stale-after <sec>?', '--adapter <name>?'],
        'examples': ['web-automation-dispatch.py artifacts', 'web-automation-dispatch.py artifacts --json', 'web-automation-dispatch.py artifacts --stale-after 1800', 'web-automation-dispatch.py artifacts --adapter github'],
        'runner': lambda value=None, json_mode=False: ['python3', str(ROOT / 'scripts' / 'web-automation-artifacts.py')] + (value if isinstance(value, list) else []) + (['--json'] if json_mode else []),
    },
    'automation-board': {
        'description': 'Toon één compact web automation board met artifacts, sites, desktop fallback, Proton status en de volgende autopilot-stap zonder iets uit te voeren',
        'layer': 'meta',
        'args': ['--stale-after <sec>?', '--configured-only?', '--adapter <name>?', '--slug <name>?', '--attention-only?'],
        'examples': ['web-automation-dispatch.py automation-board', 'web-automation-dispatch.py automation-board --json', 'web-automation-dispatch.py automation-board --configured-only', 'web-automation-dispatch.py automation-board --adapter github', 'web-automation-dispatch.py automation-board --slug slack-signin', 'web-automation-dispatch.py automation-board --attention-only'],
        'runner': lambda value=None, json_mode=False: ['python3', str(ROOT / 'scripts' / 'automation-board.py')] + (value if isinstance(value, list) else []) + (['--json'] if json_mode else []),
    },
    'sites': {
        'description': 'Toon generieke site-probes als herbruikbare adapter-observability met url/title/form-signalen, plus optionele registry-sites zonder artifact',
        'layer': 'meta',
        'args': ['--stale-after <sec>?', '--configured-only?', '--adapter <name>?', '--slug <name>?', '--attention-only?'],
        'examples': ['web-automation-dispatch.py sites', 'web-automation-dispatch.py sites --json', 'web-automation-dispatch.py sites --stale-after 1800', 'web-automation-dispatch.py sites --configured-only', 'web-automation-dispatch.py sites --adapter slack', 'web-automation-dispatch.py sites --slug github-login', 'web-automation-dispatch.py sites --attention-only'],
        'runner': lambda value=None, json_mode=False: ['python3', str(ROOT / 'scripts' / 'web-automation-sites.py')] + (value if isinstance(value, list) else []) + (['--json'] if json_mode else []),
    },
    'stack-status': {
        'description': 'Toon per site één samengevoegde stack-view over DOM probe, desktop fallback, artifacts en workflow-state',
        'layer': 'meta',
        'args': ['--stale-after <sec>?', '--configured-only?', '--adapter <name>?', '--slug <name>?', '--attention-only?', '--artifact-preview <n>?'],
        'examples': ['web-automation-dispatch.py stack-status', 'web-automation-dispatch.py stack-status --json', 'web-automation-dispatch.py stack-status --slug github-login', 'web-automation-dispatch.py stack-status --adapter slack', 'web-automation-dispatch.py stack-status --attention-only'],
        'runner': lambda value=None, json_mode=False: ['python3', str(ROOT / 'scripts' / 'web-automation-stack-status.py')] + (value if isinstance(value, list) else []) + (['--json'] if json_mode else []),
    },
    'selectors': {
        'description': 'Vat de bruikbaarste zichtbare DOM-controls samen uit probe-artifacts, zodat site-adapterwerk sneller selector-hints heeft',
        'layer': 'meta',
        'args': ['--slug <name>?', '--adapter <name>?', '--limit <n>?', '--include-hidden?'],
        'examples': ['web-automation-dispatch.py selectors', 'web-automation-dispatch.py selectors --slug github-login', 'web-automation-dispatch.py selectors --adapter slack --json'],
        'runner': lambda value=None, json_mode=False: ['python3', str(ROOT / 'scripts' / 'web-automation-selectors.py')] + (value if isinstance(value, list) else []) + (['--json'] if json_mode else []),
    },
    'site-registry': {
        'description': 'Beheer herbruikbare registry-sites voor web automation adapters en refresh-routes',
        'layer': 'meta',
        'args': ['list?', 'validate?', 'upsert --slug <name> [--url <url>]?', 'promote --slug <name>?', 'remove --slug <name>?', 'list/validate --slug <name>?', 'list/validate --adapter <naam>?', 'list/validate --desktop-only?', 'list/validate --warnings-only?', '--label <naam>?', '--adapter <naam>?', '--route <dispatch-route>?', '--route-arg <arg>?', '--probe-arg <arg>?', '--refresh-command <cmd>?', '--stale-after <sec>?', '--desktop-keep-screenshots <n>?', '--notes <tekst>?'],
        'examples': [
            'web-automation-dispatch.py site-registry',
            'web-automation-dispatch.py site-registry --json',
            'web-automation-dispatch.py site-registry validate',
            'web-automation-dispatch.py site-registry list --adapter github',
            'web-automation-dispatch.py site-registry list --desktop-only',
            'web-automation-dispatch.py site-registry upsert --slug slack-signin --url https://app.slack.com/signin --notes "Signin warm houden"',
            'web-automation-dispatch.py site-registry upsert --slug slack-signin --url https://app.slack.com/signin --probe-arg --session --probe-arg slack-shared',
            'web-automation-dispatch.py site-registry upsert --slug slack-signin --url https://app.slack.com/signin --stale-after 3600',
            'web-automation-dispatch.py site-registry upsert --slug slack-signin --url https://app.slack.com/signin --desktop-keep-screenshots 6',
            'web-automation-dispatch.py site-registry upsert --slug proton-signup --route proton-refresh --label "Proton signup"',
            'web-automation-dispatch.py site-registry promote --slug bitwarden-login --stale-after 3600 --notes "Vault login observability warm houden"',
            'web-automation-dispatch.py site-registry remove --slug slack-signin',
        ],
        'runner': lambda value=None, json_mode=False: ['python3', str(ROOT / 'scripts' / 'web-automation-site-registry.py')] + (['--json'] if json_mode else []) + (value if isinstance(value, list) else []),
    },
    'refresh-sites': {
        'description': 'Refresh bestaande generieke site-probes op basis van opgeslagen slug/url artifacts of registry-sites, standaard alleen stale sites en optioneel alleen beheerde registry-sites',
        'layer': 'meta',
        'args': ['--all?', '--configured-only?', '--slug <name>?', '--adapter <name>?', '--max-sites <n>?', '--stale-after <sec>?', '--timeout <sec>?', '--plan-only?'],
        'examples': ['web-automation-dispatch.py refresh-sites', 'web-automation-dispatch.py refresh-sites --json', 'web-automation-dispatch.py refresh-sites --configured-only', 'web-automation-dispatch.py refresh-sites --adapter github', 'web-automation-dispatch.py refresh-sites --plan-only', 'web-automation-dispatch.py refresh-sites --timeout 60'],
        'runner': lambda value=None, json_mode=False: ['python3', str(ROOT / 'scripts' / 'web-automation-refresh-sites.py')] + (value if isinstance(value, list) else []) + (['--json'] if json_mode else []),
    },
    'refresh-desktop': {
        'description': 'Refresh stale desktop fallback targets op basis van observability, standaard alleen beheerde targets',
        'layer': 'meta',
        'args': ['--configured-only?', '--all?', '--slug <name>?', '--adapter <name>?', '--max-targets <n>?', '--force?', '--stale-after <sec>?', '--timeout <sec>?', '--plan-only?'],
        'examples': ['web-automation-dispatch.py refresh-desktop', 'web-automation-dispatch.py refresh-desktop --json', 'web-automation-dispatch.py refresh-desktop --configured-only', 'web-automation-dispatch.py refresh-desktop --adapter github', 'web-automation-dispatch.py refresh-desktop --plan-only', 'web-automation-dispatch.py refresh-desktop --slug slack-signin', 'web-automation-dispatch.py refresh-desktop --configured-only --slug github-login --force'],
        'runner': lambda value=None, json_mode=False: ['python3', str(ROOT / 'scripts' / 'web-automation-refresh-desktop.py')] + (value if isinstance(value, list) else []) + (['--json'] if json_mode else []),
    },
    'refresh-stack': {
        'description': 'Refresh één observability-stack over DOM/site probe en desktop fallback heen, zodat een target in één route weer overal vers is',
        'layer': 'meta',
        'args': ['--configured-only?', '--all?', '--slug <name>?', '--adapter <name>?', '--max-sites <n>?', '--max-targets <n>?', '--stale-after <sec>?', '--timeout <sec>?', '--site-timeout <sec>?', '--desktop-timeout <sec>?', '--force-desktop?', '--keep-screenshots <n>?', '--include-terminal?', '--plan-only?'],
        'examples': ['web-automation-dispatch.py refresh-stack', 'web-automation-dispatch.py refresh-stack --json', 'web-automation-dispatch.py refresh-stack --configured-only --slug slack-signin', 'web-automation-dispatch.py refresh-stack --configured-only --slug github-login --force-desktop --keep-screenshots 6', 'web-automation-dispatch.py refresh-stack --adapter github --plan-only'],
        'runner': lambda value=None, json_mode=False: ['python3', str(ROOT / 'scripts' / 'web-automation-refresh-stack.py')] + (value if isinstance(value, list) else []) + (['--json'] if json_mode else []),
    },
    'prune-unmanaged': {
        'description': 'Inventariseer of trash stale onbeheerde probe-artifacts en desktop fallback outdirs, zodat demo/debug-ruis de board niet blijft vervuilen',
        'layer': 'meta',
        'args': ['--stale-after <sec>?', '--adapter <name>?', '--apply?', '--json?'],
        'examples': ['web-automation-dispatch.py prune-unmanaged', 'web-automation-dispatch.py prune-unmanaged --json', 'web-automation-dispatch.py prune-unmanaged --adapter github', 'web-automation-dispatch.py prune-unmanaged --apply'],
        'runner': lambda value=None, json_mode=False: ['python3', str(ROOT / 'scripts' / 'web-automation-prune.py')] + (value if isinstance(value, list) else []) + (['--json'] if json_mode else []),
    },
    'autopilot': {
        'description': 'Voer veilig één of meer betekenisvolle web automation vervolgstappen uit, eerst stale beheerde site-observability refreshen, daarna zo nodig de desktop fallback verversen, anders stale onbeheerde artifacts reviewen of naar Trash sturen, en anders een veilige Proton vervolgstap. Met --plan-only krijg je ook de vermoedelijke vervolgactie als de eerste stap slaagt.',
        'layer': 'meta',
        'args': ['--max-site-refreshes <n>?', '--max-actions <n>?', '--stale-after <sec>?', '--site-timeout <sec>?', '--adapter <name>?', '--apply-prune?', '--plan-only?'],
        'examples': ['web-automation-dispatch.py autopilot', 'web-automation-dispatch.py autopilot --json', 'web-automation-dispatch.py autopilot --plan-only', 'web-automation-dispatch.py autopilot --adapter github', 'web-automation-dispatch.py autopilot --max-site-refreshes 1', 'web-automation-dispatch.py autopilot --max-actions 4', 'web-automation-dispatch.py autopilot --site-timeout 60', 'web-automation-dispatch.py autopilot --apply-prune'],
        'runner': lambda value=None, json_mode=False: ['python3', str(ROOT / 'scripts' / 'web-automation-autopilot.py')] + (value if isinstance(value, list) else []) + (['--json'] if json_mode else []),
    },
    'desktop-probe': {
        'description': 'Desktop fallback probe via lokale desktop stack',
        'layer': 'desktop-fallback',
        'args': ['[outdir]? [url]?', '--slug <name>?', '--url <url>?', '--keep-screenshots <n>?'],
        'examples': [
            'web-automation-dispatch.py desktop-probe',
            'web-automation-dispatch.py desktop-probe /tmp/desktop-probe https://example.com',
            'web-automation-dispatch.py desktop-probe --slug slack-signin',
            'web-automation-dispatch.py desktop-probe --slug slack-signin --keep-screenshots 4',
            'web-automation-dispatch.py desktop-probe --slug slack-signin --url https://app.slack.com/signin',
        ],
        'runner': lambda value=None: ['bash', str(BROWSER / 'desktop_probe.sh'), *parse_desktop_probe_args(value or [])],
    },
    'desktop-status': {
        'description': 'Toon compacte observability-status van de desktop fallback artifacts',
        'layer': 'meta',
        'args': ['--stale-after <sec>?', '--configured-only?', '--adapter <name>?', '--slug <name>?', '--outdir <dir>?'],
        'examples': ['web-automation-dispatch.py desktop-status', 'web-automation-dispatch.py desktop-status --json', 'web-automation-dispatch.py desktop-status --configured-only', 'web-automation-dispatch.py desktop-status --adapter github', 'web-automation-dispatch.py desktop-status --slug slack-signin'],
        'runner': lambda value=None, json_mode=False: ['python3', str(ROOT / 'scripts' / 'desktop-fallback-status.py')] + (value if isinstance(value, list) else []) + (['--json'] if json_mode else []),
    },
    'proton-status': {
        'description': 'Lees huidige Proton automation-status',
        'layer': 'dom',
        'args': [],
        'examples': ['web-automation-dispatch.py proton-status', 'web-automation-dispatch.py proton-status --json'],
        'runner': lambda value=None, json_mode=False: ['python3', str(ROOT / 'scripts' / 'proton-status-summary.py')] + (['--json'] if json_mode else []),
    },
    'proton-board': {
        'description': 'Toon compacte Proton board met status plus volgende stap',
        'layer': 'meta',
        'args': [],
        'examples': ['web-automation-dispatch.py proton-board', 'web-automation-dispatch.py proton-board --json'],
        'runner': lambda value=None, json_mode=False: ['python3', str(ROOT / 'scripts' / 'protonboard.py')] + (['--json'] if json_mode else []),
    },
    'proton-next-step': {
        'description': 'Bepaal de volgende nuttige Proton automation stap op basis van status en verification-artifacts',
        'layer': 'meta',
        'args': [],
        'examples': ['web-automation-dispatch.py proton-next-step', 'web-automation-dispatch.py proton-next-step --json'],
        'runner': lambda value=None, json_mode=False: ['python3', str(ROOT / 'scripts' / 'proton-next-step.py')] + (['--json'] if json_mode else []),
    },
    'proton-autopilot-safe': {
        'description': 'Voer veilig de aanbevolen Proton vervolgstap uit zonder onbedoelde finale submit',
        'layer': 'meta',
        'args': ['--max-steps <n>?'],
        'examples': ['web-automation-dispatch.py proton-autopilot-safe', 'web-automation-dispatch.py proton-autopilot-safe --json', 'web-automation-dispatch.py proton-autopilot-safe --max-steps 2'],
        'runner': lambda value=None, json_mode=False: ['python3', str(ROOT / 'scripts' / 'proton-autopilot-safe.py')] + (value if isinstance(value, list) else []) + (['--json'] if json_mode else []),
    },
    'proton-password-step': {
        'description': 'Breng Proton veilig tot de password-stap',
        'layer': 'dom',
        'args': ['username?'],
        'examples': ['web-automation-dispatch.py proton-password-step', 'web-automation-dispatch.py proton-password-step clawdy01'],
        'runner': lambda value=None: ['node', str(BROWSER / 'proton_to_password_step.js')] + (value if isinstance(value, list) else ([] if value is None else [value])),
    },
    'investigate-password-regression': {
        'description': 'Draai gerichte probes en geef een compacte diagnose van de Proton password-step regressie',
        'layer': 'meta',
        'args': ['--refresh?', '--json?'],
        'examples': ['web-automation-dispatch.py investigate-password-regression', 'web-automation-dispatch.py investigate-password-regression --refresh', 'web-automation-dispatch.py investigate-password-regression --json'],
        'runner': lambda value=None, json_mode=False: ['python3', str(PROTON_REGRESSION)] + (value if isinstance(value, list) else []) + (['--json'] if json_mode else []),
    },
    'proton-refresh': {
        'description': 'Draai veilige Proton automation chain opnieuw',
        'layer': 'dom',
        'args': [],
        'examples': ['web-automation-dispatch.py proton-refresh', 'web-automation-dispatch.py proton-refresh --json'],
        'runner': lambda value=None, json_mode=False: ['python3', str(ROOT / 'scripts' / 'proton-refresh-safe.py')] + (['--json'] if json_mode else []),
    },
    'proton-submit-ready': {
        'description': 'Breng Proton-flow veilig tot vlak voor de finale signup-submit',
        'layer': 'dom',
        'args': ['username?', 'password?'],
        'examples': ['web-automation-dispatch.py proton-submit-ready', "web-automation-dispatch.py proton-submit-ready clawdy01 'Short123!'"] ,
        'runner': lambda value=None: ['node', str(BROWSER / 'proton_to_submit_ready.js')] + (value if isinstance(value, list) else ([] if value is None else [value])),
    },
    'proton-submit-probe': {
        'description': 'Observeer de finale Proton submit-stap, optioneel met echte submit-attempt',
        'layer': 'dom',
        'args': ['username?', 'password?', '--submit?'],
        'examples': ['web-automation-dispatch.py proton-submit-probe', 'web-automation-dispatch.py proton-submit-probe clawdy01', 'web-automation-dispatch.py proton-submit-probe clawdy01 --submit'],
        'runner': lambda value=None: ['node', str(BROWSER / 'proton_submit_probe.js')] + (value if isinstance(value, list) else ([] if value is None else [value])),
    },
    'proton-verification-status': {
        'description': 'Combineer Proton human-verification status met mailbox code lookup',
        'layer': 'meta',
        'args': ['--refresh?', '--refresh-submit?', '--auto?'],
        'examples': ['web-automation-dispatch.py proton-verification-status', 'web-automation-dispatch.py proton-verification-status --json', 'web-automation-dispatch.py proton-verification-status --refresh', 'web-automation-dispatch.py proton-verification-status --auto'],
        'runner': lambda value=None, json_mode=False: ['python3', str(ROOT / 'scripts' / 'proton-verification-status.py')] + (value if isinstance(value, list) else []) + (['--json'] if json_mode else []),
    },
    'proton-verify-refresh': {
        'description': 'Refresh Proton human-verification status veilig, inclusief verse dialog/mail observability',
        'layer': 'meta',
        'args': [],
        'examples': ['web-automation-dispatch.py proton-verify-refresh', 'web-automation-dispatch.py proton-verify-refresh --json'],
        'runner': lambda value=None, json_mode=False: ['python3', str(ROOT / 'scripts' / 'proton-verification-status.py'), '--refresh'] + (['--json'] if json_mode else []),
    },
    'proton-human-verification': {
        'description': 'Breng Proton naar de human-verification dialoog en inspecteer of bedien email/code-controls',
        'layer': 'dom',
        'args': ['username?', 'password?', '--email <adres>?', '--send?', '--code <code>?', '--verify?'],
        'examples': ['web-automation-dispatch.py proton-human-verification', 'web-automation-dispatch.py proton-human-verification clawdy01', 'web-automation-dispatch.py proton-human-verification clawdy01 --email you@example.com --send'],
        'runner': lambda value=None: ['node', str(BROWSER / 'proton_human_verification.js')] + (value if isinstance(value, list) else ([] if value is None else [value])),
    },
    'proton-request-code': {
        'description': 'Vraag automatisch een Proton verificatiecode aan via de human-verification flow met state-defaults',
        'layer': 'meta',
        'args': ['username?', 'password?', '--email <adres>?', '--json?'],
        'examples': ['web-automation-dispatch.py proton-request-code', 'web-automation-dispatch.py proton-request-code --json', 'web-automation-dispatch.py proton-request-code clawdy01'],
        'runner': lambda value=None, json_mode=False: ['python3', str(ROOT / 'scripts' / 'proton-request-verification-code.py')] + (value if isinstance(value, list) else []) + (['--json'] if json_mode else []),
    },
    'proton-use-code': {
        'description': 'Pak automatisch de nieuwste Proton verificatiecode uit mail en probeer die in de Human Verification-flow te gebruiken',
        'layer': 'meta',
        'args': ['username?', 'password?', '--sender <naam>?', '-n <limit>?', '--json?'],
        'examples': ['web-automation-dispatch.py proton-use-code', 'web-automation-dispatch.py proton-use-code --json', 'web-automation-dispatch.py proton-use-code clawdy01'],
        'runner': lambda value=None, json_mode=False: ['python3', str(ROOT / 'scripts' / 'proton-use-verification-code.py')] + (value if isinstance(value, list) else []) + (['--json'] if json_mode else []),
    },
    'proton-manual-finish': {
        'description': 'Toon een compacte handoff zodra Proton de manual boundary of Recovery Kit stap heeft bereikt',
        'layer': 'meta',
        'args': ['--json?'],
        'examples': ['web-automation-dispatch.py proton-manual-finish', 'web-automation-dispatch.py proton-manual-finish --json'],
        'runner': lambda value=None, json_mode=False: ['python3', str(ROOT / 'scripts' / 'proton-manual-finish-summary.py')] + (['--json'] if json_mode else []),
    },
    'continue-password-setup': {
        'description': 'Trek de Proton signup-flow veilig verder via de external-email finish route wanneer verificatie al geaccepteerd lijkt',
        'layer': 'meta',
        'args': ['username?', 'password?', '--email <adres>?', '--json?'],
        'examples': ['web-automation-dispatch.py continue-password-setup', 'web-automation-dispatch.py continue-password-setup --json'],
        'runner': lambda value=None, json_mode=False: ['python3', str(ROOT / 'scripts' / 'proton-continue-password-setup.py')] + (value if isinstance(value, list) else []) + (['--json'] if json_mode else []),
    },
}
ALIASES = {
    'probe': 'probe-page',
    'desktop': 'desktop-probe',
    'desktop-health': 'desktop-status',
    'desktop-board': 'desktop-status',
    'artifact': 'artifacts',
    'automation': 'automation-board',
    'web-board': 'automation-board',
    'site': 'sites',
    'stack': 'stack-status',
    'site-stack': 'stack-status',
    'selector': 'selectors',
    'site-selectors': 'selectors',
    'site-registry-list': 'site-registry',
    'site-registry-add': 'site-registry',
    'refresh-site': 'refresh-sites',
    'refresh': 'refresh-sites',
    'refresh-stack-targets': 'refresh-stack',
    'refresh-observability': 'refresh-stack',
    'refresh-desktop-targets': 'refresh-desktop',
    'desktop-refresh': 'refresh-desktop',
    'prune': 'prune-unmanaged',
    'auto': 'autopilot',
    'autorefresh': 'autopilot',
    'proton': 'proton-status',
    'board': 'proton-board',
    'proton-next': 'proton-next-step',
    'proton-auto': 'proton-autopilot-safe',
    'proton-password': 'proton-password-step',
    'proton-regression': 'investigate-password-regression',
    'proton-ready': 'proton-submit-ready',
    'proton-submit': 'proton-submit-probe',
    'proton-verify': 'proton-verification-status',
    'proton-verify-refresh': 'proton-verify-refresh',
    'proton-human': 'proton-human-verification',
    'proton-request': 'proton-request-code',
    'proton-use': 'proton-use-code',
    'proton-finish': 'proton-manual-finish',
    'proton-continue': 'continue-password-setup',
}


def normalize_route(value):
    value = (value or 'catalog').strip()
    return ALIASES.get(value, value)


def desktop_slug_to_outdir(slug):
    value = ''.join(ch if ch.isalnum() or ch in {'-', '_'} else '-' for ch in (slug or '').strip().lower()).strip('-_')
    if not value:
        raise SystemExit('desktop-probe vereist een niet-lege slug')
    return str(BROWSER / f'out-desktop-{value}')


def load_site_registry_by_slug():
    path = ROOT / 'state' / 'web-automation-sites.json'
    try:
        payload = json.loads(path.read_text())
    except Exception:
        return {}

    if isinstance(payload, dict):
        entries = payload.get('sites') if isinstance(payload.get('sites'), list) else payload.get('items')
    elif isinstance(payload, list):
        entries = payload
    else:
        entries = []

    registry = {}
    for item in entries or []:
        if not isinstance(item, dict) or item.get('enabled', True) is False:
            continue
        slug = str(item.get('slug') or '').strip().lower()
        url = str(item.get('url') or '').strip()
        if slug:
            registry[slug] = {
                'url': url,
                'route': str(item.get('route') or '').strip(),
                'label': str(item.get('label') or '').strip(),
            }
    return registry


def parse_desktop_probe_args(route_args):
    outdir = None
    url = None
    slug = None
    keep_screenshots = None
    idx = 0
    while idx < len(route_args):
        arg = route_args[idx]
        if arg == '--slug':
            idx += 1
            if idx >= len(route_args):
                raise SystemExit('--slug vereist een waarde')
            slug = str(route_args[idx]).strip().lower()
            outdir = desktop_slug_to_outdir(slug)
        elif arg == '--url':
            idx += 1
            if idx >= len(route_args):
                raise SystemExit('--url vereist een waarde')
            url = route_args[idx]
        elif arg == '--keep-screenshots':
            idx += 1
            if idx >= len(route_args):
                raise SystemExit('--keep-screenshots vereist een waarde')
            keep_screenshots = route_args[idx]
        elif arg.startswith('--'):
            raise SystemExit(f'onbekende desktop-probe optie: {arg}')
        elif outdir is None:
            outdir = arg
        elif url is None:
            url = arg
        else:
            raise SystemExit('desktop-probe accepteert hooguit een outdir en een url')
        idx += 1

    if slug and not url:
        registry_entry = load_site_registry_by_slug().get(slug) or {}
        url = registry_entry.get('url') or None
        if not url:
            raise SystemExit(f'desktop-probe kan zonder --url alleen een slug gebruiken die een URL heeft in state/web-automation-sites.json ({slug})')

    cmd_args = []
    if keep_screenshots is not None:
        cmd_args.extend(['--keep-screenshots', str(keep_screenshots)])
    if outdir:
        cmd_args.append(outdir)
    if url:
        if not outdir:
            cmd_args.append(str(BROWSER / 'out-desktop'))
        cmd_args.append(url)
    return cmd_args


def catalog_payload():
    return {
        'routes': [
            {
                'name': name,
                'description': meta['description'],
                'layer': meta['layer'],
                'args': meta['args'],
                'examples': meta['examples'],
            }
            for name, meta in ROUTES.items()
        ],
        'aliases': ALIASES,
        'layers': ['api', 'dom', 'desktop-fallback'],
        'notes': 'Primary route is DOM/Playwright, with desktop fallback available for awkward UI flows. Generic probes can store per-site artifacts via --slug, the sites route can merge those artifacts with optional state/web-automation-sites.json registry entries, optionally filter to managed targets via --configured-only, the stack-status route can combine DOM, desktop, artifact, and workflow state per target, artifacts/sites/desktop views can now all be narrowed per adapter, site-registry can manage those saved targets or promote an existing artifact into the registry, refresh-sites and refresh-desktop can now also run in --plan-only mode for safe queue/heartbeat observability, prune-unmanaged and autopilot can likewise be scoped to one adapter, desktop refreshes can inherit per-site screenshot retention from the registry, and desktop-probe can infer a configured URL from the registry when called with --slug.',
    }


def render_catalog():
    payload = catalog_payload()
    lines = ['Web automation dispatch']
    lines.append(f"- lagen: {', '.join(payload['layers'])}")
    for route in payload['routes']:
        arg_text = f" ({', '.join(route['args'])})" if route['args'] else ''
        lines.append(f"- {route['name']} [{route['layer']}] {route['description']}{arg_text}")
    if payload['aliases']:
        lines.append(f"- aliases: {', '.join(f'{k}->{v}' for k, v in sorted(payload['aliases'].items()))}")
    lines.append(f"- note: {payload['notes']}")
    return '\n'.join(lines)


def run(cmd):
    proc = subprocess.run(cmd, cwd=ROOT, text=True, capture_output=True, check=False)
    try:
        if proc.stdout:
            sys.stdout.write(proc.stdout)
        if proc.stderr:
            sys.stderr.write(proc.stderr)
    except BrokenPipeError:
        try:
            sys.stdout.close()
        except Exception:
            pass
        raise SystemExit(0)
    raise SystemExit(proc.returncode)


def main():
    parser = argparse.ArgumentParser(description='Dispatcher voor web automation routes en fallbacks')
    parser.add_argument('route', nargs='?', default='catalog')
    parser.add_argument('args', nargs='*')
    parser.add_argument('--json', action='store_true')
    parsed, extras = parser.parse_known_args()
    route_args = parsed.args + extras

    route = normalize_route(parsed.route)
    if route == 'catalog':
        try:
            if parsed.json:
                print(json.dumps(catalog_payload(), ensure_ascii=False, indent=2))
            else:
                print(render_catalog())
        except BrokenPipeError:
            try:
                sys.stdout.close()
            except Exception:
                pass
        return
    if route not in ROUTES:
        raise SystemExit(f'Onbekende route: {parsed.route}')

    meta = ROUTES[route]
    if route == 'probe-page':
        if not route_args:
            raise SystemExit('probe-page vereist een URL')
        cmd = meta['runner'](route_args)
    elif route == 'desktop-probe':
        cmd = meta['runner'](parse_desktop_probe_args(route_args))
    elif route in {'proton-status', 'proton-board', 'proton-next-step', 'proton-refresh', 'proton-verify-refresh'}:
        cmd = meta['runner'](json_mode=parsed.json)
    elif route in {'artifacts', 'automation-board', 'sites', 'stack-status', 'selectors', 'site-registry', 'refresh-sites', 'refresh-desktop', 'refresh-stack', 'prune-unmanaged', 'autopilot', 'desktop-status'}:
        cmd = meta['runner'](route_args, json_mode=parsed.json)
    elif route in {'proton-verification-status', 'proton-autopilot-safe', 'proton-request-code', 'proton-use-code', 'proton-manual-finish', 'continue-password-setup', 'investigate-password-regression'}:
        cmd = meta['runner'](route_args, json_mode=parsed.json)
    elif route in {'proton-password-step', 'proton-submit-ready', 'proton-submit-probe', 'proton-human-verification'}:
        cmd = meta['runner'](route_args)
    else:
        raise SystemExit(f'Onbekende route: {route}')

    run(cmd)


if __name__ == '__main__':
    main()
