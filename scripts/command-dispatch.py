#!/usr/bin/env python3
import argparse
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path('/home/clawdy/.openclaw/workspace')

COMMANDS = {
    'status': {
        'cmd': ['python3', str(ROOT / 'scripts' / 'statusboard.py')],
        'description': 'Compacte OpenClaw status',
    },
    'tools': {
        'cmd': ['python3', str(ROOT / 'scripts' / 'toolsboard.py')],
        'description': 'Overzicht van beschikbare tools en scripts',
    },
    'mail': {
        'cmd': ['python3', str(ROOT / 'scripts' / 'mail-dispatch.py'), 'board'],
        'description': 'Mail-overzicht met latest, unread, new en drafts',
    },
    'mail-inbox': {
        'cmd': ['python3', str(ROOT / 'scripts' / 'mail-dispatch.py'), 'latest'],
        'description': 'Snelle inbox-view van recente mail',
    },
    'mail-unread': {
        'cmd': ['python3', str(ROOT / 'scripts' / 'mail-dispatch.py'), 'latest', '--unread'],
        'description': 'Toon direct alleen ongelezen mail',
    },
    'mail-latest': {
        'cmd': ['python3', str(ROOT / 'scripts' / 'mail-dispatch.py'), 'latest'],
        'description': 'Laatste mails of ongelezen inbox-items bekijken',
    },
    'mail-check': {
        'cmd': ['python3', str(ROOT / 'scripts' / 'mail-dispatch.py'), 'check'],
        'description': 'Check alleen echt nieuwe mail sinds de laatste state-update',
    },
    'mail-summary': {
        'cmd': ['python3', str(ROOT / 'scripts' / 'mail-dispatch.py'), 'summary'],
        'description': 'Nieuwe mail met urgentie en actiehints',
    },
    'mail-drafts': {
        'cmd': ['python3', str(ROOT / 'scripts' / 'mail-dispatch.py'), 'drafts'],
        'description': 'Concept-antwoorden op basis van nieuwe, ongelezen of recente mail',
    },
    'mail-triage': {
        'cmd': ['python3', str(ROOT / 'scripts' / 'mail-dispatch.py'), 'triage'],
        'description': 'Prioriteer ongelezen mail met actiehints en reply-signalen',
    },
    'mail-now': {
        'cmd': ['python3', str(ROOT / 'scripts' / 'mail-dispatch.py'), 'now'],
        'description': 'Toon alleen recente mail die nu echt aandacht vraagt',
    },
    'mail-focus': {
        'cmd': ['python3', str(ROOT / 'scripts' / 'mail-dispatch.py'), 'focus'],
        'description': 'Kies de ene beste mail om nu als eerste op te pakken, optioneel met conceptantwoord',
    },
    'mail-first': {
        'cmd': ['python3', str(ROOT / 'scripts' / 'mail-dispatch.py'), 'focus'],
        'description': 'Snelle route naar de ene beste eerstvolgende mail',
    },
    'mail-next-step': {
        'cmd': ['python3', str(ROOT / 'scripts' / 'mail-dispatch.py'), 'next-step'],
        'description': 'Bepaal de volgende nuttige mailstap, ook als er geen actuele unread-focus meer is',
    },
    'mail-queue': {
        'cmd': ['python3', str(ROOT / 'scripts' / 'mail-dispatch.py'), 'queue'],
        'description': 'Toon een korte prioriteitslijst van de beste volgende mailacties',
    },
    'mail-security-alerts': {
        'cmd': ['python3', str(ROOT / 'scripts' / 'mail-dispatch.py'), 'security-alerts'],
        'description': 'Toon compacte account- en login-alerts met current-only en suppressed-uitleg',
    },
    'mail-review-next': {
        'cmd': ['python3', str(ROOT / 'scripts' / 'mail-dispatch.py'), 'review-next'],
        'description': 'Open direct de aanbevolen volgende mailthread met context, alternatieven en optioneel conceptantwoord',
    },
    'mail-thread': {
        'cmd': ['python3', str(ROOT / 'scripts' / 'mail-dispatch.py'), 'thread'],
        'description': 'Klap één recente mailthread compact uit, met filters op afzender/onderwerp/actie en optioneel conceptantwoord',
    },
    'mail-clusters': {
        'cmd': ['python3', str(ROOT / 'scripts' / 'mail-dispatch.py'), 'clusters'],
        'description': 'Toon recente mail geclusterd per afzender/actie zodat bursts compacter zichtbaar zijn',
    },
    'mail-reply-needed': {
        'cmd': ['python3', str(ROOT / 'scripts' / 'mail-dispatch.py'), 'reply-needed'],
        'description': 'Toon snel welke recente mails waarschijnlijk antwoord nodig hebben',
    },
    'mail-high-priority': {
        'cmd': ['python3', str(ROOT / 'scripts' / 'mail-dispatch.py'), 'high-priority'],
        'description': 'Toon snel welke recente mails als high priority gezien worden',
    },
    'mail-codes': {
        'cmd': ['python3', str(ROOT / 'scripts' / 'mail-dispatch.py'), 'codes'],
        'description': 'Zoek verificatiecodes in recente mail',
    },
    'mail-catalog': {
        'cmd': ['python3', str(ROOT / 'scripts' / 'mail-dispatch.py'), 'catalog'],
        'description': 'Mail workflow catalogus en dispatcher-routes',
    },
    'board': {
        'cmd': ['python3', str(ROOT / 'scripts' / 'command-board.py')],
        'description': 'Gecombineerd board voor status, mail, proton, security, tasks en tools',
    },
    'brief': {
        'cmd': ['python3', str(ROOT / 'scripts' / 'clawdy-brief.py')],
        'description': 'Korte gecombineerde status- en mailbrief',
    },
    'proton': {
        'cmd': ['python3', str(ROOT / 'scripts' / 'proton-status-summary.py')],
        'description': 'Samenvatting van de Proton signup automation-status',
    },
    'proton-board': {
        'cmd': ['python3', str(ROOT / 'scripts' / 'protonboard.py')],
        'description': 'Compact Proton board met status plus volgende stap',
    },
    'proton-next-step': {
        'cmd': ['python3', str(ROOT / 'scripts' / 'proton-next-step.py')],
        'description': 'Bepaal de volgende nuttige Proton automation stap',
    },
    'proton-refresh': {
        'cmd': ['python3', str(ROOT / 'scripts' / 'proton-refresh-safe.py')],
        'description': 'Draai veilige Proton probes opnieuw en toon verse status',
    },
    'proton-auto': {
        'cmd': ['python3', str(ROOT / 'scripts' / 'proton-autopilot-safe.py')],
        'description': 'Voer veilig de aanbevolen Proton vervolgstap uit zonder finale submit',
    },
    'proton-verify': {
        'cmd': ['python3', str(ROOT / 'scripts' / 'proton-verification-status.py')],
        'description': 'Combineer Proton verificatiestatus met mailbox-code lookup',
    },
    'proton-human': {
        'cmd': ['python3', str(ROOT / 'scripts' / 'proton-human-verification-summary.py')],
        'description': 'Compact overzicht van de Proton human-verification dialoog en beschikbare email/code-controls',
    },
    'proton-use-code': {
        'cmd': ['python3', str(ROOT / 'scripts' / 'proton-use-verification-code.py')],
        'description': 'Pak automatisch de nieuwste Proton verificatiecode uit mail en probeer die in de Human Verification-flow te gebruiken',
    },
    'proton-finish': {
        'cmd': ['python3', str(ROOT / 'scripts' / 'proton-manual-finish-summary.py')],
        'description': 'Compacte handoff voor de Proton manual boundary en Recovery Kit stap',
    },
    'proton-continue': {
        'cmd': ['python3', str(ROOT / 'scripts' / 'proton-continue-password-setup.py')],
        'description': 'Trek de Proton signup-flow veilig verder via de external-email finish route wanneer verificatie al geaccepteerd lijkt',
    },
    'proton-request-code': {
        'cmd': ['python3', str(ROOT / 'scripts' / 'proton-request-verification-code.py')],
        'description': 'Vraag automatisch een Proton verificatiecode aan via de human-verification flow met state-defaults',
    },
    'automation-board': {
        'cmd': ['python3', str(ROOT / 'scripts' / 'automation-board.py')],
        'description': 'Compact overzicht van web automation routes, Proton readiness en verification-status',
    },
    'automation-artifacts': {
        'cmd': ['python3', str(ROOT / 'scripts' / 'web-automation-dispatch.py'), 'artifacts'],
        'description': 'Toon web automation artifacts per adapter met freshness en refresh-advies',
    },
    'security': {
        'cmd': ['python3', str(ROOT / 'scripts' / 'security-summary.py')],
        'description': 'Compacte security-audit samenvatting',
    },
    'tasks': {
        'cmd': ['python3', str(ROOT / 'scripts' / 'task-audit-summary.py')],
        'description': 'Compacte task-audit samenvatting',
    },
    'automation': {
        'cmd': ['python3', str(ROOT / 'scripts' / 'automation-board.py')],
        'description': 'Compact overzicht van web automation status, routes, Proton readiness en verification-status',
    },
    'automation-catalog': {
        'cmd': ['python3', str(ROOT / 'scripts' / 'web-automation-dispatch.py'), 'catalog'],
        'description': 'Web automation catalogus en dispatcher voor DOM/desktop/Proton routes',
    },
    'automation-sites': {
        'cmd': ['python3', str(ROOT / 'scripts' / 'web-automation-dispatch.py'), 'sites'],
        'description': 'Toon opgeslagen generieke web site probes met freshness en refresh-advies',
    },
    'automation-stack': {
        'cmd': ['python3', str(ROOT / 'scripts' / 'web-automation-dispatch.py'), 'stack-status'],
        'description': 'Toon gecombineerde DOM, desktop, artifact en workflow status per web automation target',
    },
    'automation-selectors': {
        'cmd': ['python3', str(ROOT / 'scripts' / 'web-automation-dispatch.py'), 'selectors'],
        'description': 'Toon selector-hints uit recente web probes voor sneller adapterwerk',
    },
    'automation-site-registry': {
        'cmd': ['python3', str(ROOT / 'scripts' / 'web-automation-dispatch.py'), 'site-registry'],
        'description': 'Beheer en valideer opgeslagen web automation targets in de site-registry',
    },
    'automation-desktop-status': {
        'cmd': ['python3', str(ROOT / 'scripts' / 'web-automation-dispatch.py'), 'desktop-status'],
        'description': 'Toon compacte desktop-fallback status per beheerd web automation target',
    },
    'automation-refresh-sites': {
        'cmd': ['python3', str(ROOT / 'scripts' / 'web-automation-dispatch.py'), 'refresh-sites'],
        'description': 'Refresh opgeslagen generieke web site probes, standaard alleen stale sites',
    },
    'automation-refresh-desktop': {
        'cmd': ['python3', str(ROOT / 'scripts' / 'web-automation-dispatch.py'), 'refresh-desktop'],
        'description': 'Refresh desktop-fallback observability voor beheerde web automation targets',
    },
    'automation-refresh-stack': {
        'cmd': ['python3', str(ROOT / 'scripts' / 'web-automation-dispatch.py'), 'refresh-stack'],
        'description': 'Refresh DOM en desktop observability samen voor web automation targets',
    },
    'automation-auto': {
        'cmd': ['python3', str(ROOT / 'scripts' / 'web-automation-dispatch.py'), 'autopilot'],
        'description': 'Voer veilig één of meer betekenisvolle web automation vervolgstappen uit, inclusief site-refresh, desktop-fallback en cleanup/handoff waar nodig',
    },
    'automation-proton-status': {
        'cmd': ['python3', str(ROOT / 'scripts' / 'web-automation-dispatch.py'), 'proton-status'],
        'description': 'Lees huidige Proton automation-status via de centrale automation-dispatcher',
    },
    'automation-proton-refresh': {
        'cmd': ['python3', str(ROOT / 'scripts' / 'web-automation-dispatch.py'), 'proton-refresh'],
        'description': 'Draai de veilige Proton automation-chain via de centrale automation-dispatcher',
    },
}
ALIASES = {
    '/status': 'status',
    '/tools': 'tools',
    '/mail': 'mail',
    '/mail-board': 'mail',
    '/mail-overview': 'mail',
    '/mail-inbox': 'mail-inbox',
    '/mail-unread': 'mail-unread',
    '/mail-latest': 'mail-latest',
    '/mail-check': 'mail-check',
    '/mail-new': 'mail-check',
    '/mail-summary': 'mail-summary',
    '/mail-drafts': 'mail-drafts',
    '/mail-triage': 'mail-triage',
    '/mail-prioritize': 'mail-triage',
    '/mail-now': 'mail-now',
    '/mail-current': 'mail-now',
    '/mail-urgent': 'mail-now',
    '/mail-focus': 'mail-focus',
    '/mail-first': 'mail-first',
    '/mail-next-step': 'mail-next-step',
    '/mail-next': 'mail-next-step',
    '/mail-followup': 'mail-next-step',
    '/mail-queue': 'mail-queue',
    '/mail-worklist': 'mail-queue',
    '/mail-todo': 'mail-queue',
    '/mail-security-alerts': 'mail-security-alerts',
    '/mail-security': 'mail-security-alerts',
    '/mail-alerts': 'mail-security-alerts',
    '/mail-review-next': 'mail-review-next',
    '/mail-review': 'mail-review-next',
    '/mail-open': 'mail-review-next',
    '/mail-next-thread': 'mail-review-next',
    '/mail-thread': 'mail-thread',
    '/mail-threads': 'mail-thread',
    '/mail-conversation': 'mail-thread',
    '/mail-clusters': 'mail-clusters',
    '/mail-cluster': 'mail-clusters',
    '/mail-reply-needed': 'mail-reply-needed',
    '/mail-replies': 'mail-reply-needed',
    '/mail-high-priority': 'mail-high-priority',
    '/mail-priority': 'mail-high-priority',
    '/mail-codes': 'mail-codes',
    '/mail-code': 'mail-codes',
    '/mail-verify': 'mail-codes',
    '/mail-otp': 'mail-codes',
    '/mail-auth-code': 'mail-codes',
    '/mail-catalog': 'mail-catalog',
    '/mail-help': 'mail-catalog',
    '/mail-routes': 'mail-catalog',
    '/mail-commands': 'mail-catalog',
    '/board': 'board',
    '/brief': 'brief',
    '/proton': 'proton',
    '/proton-board': 'proton-board',
    '/proton-next-step': 'proton-next-step',
    '/proton-refresh': 'proton-refresh',
    '/proton-auto': 'proton-auto',
    '/proton-verify': 'proton-verify',
    '/proton-human': 'proton-human',
    '/proton-use-code': 'proton-use-code',
    '/proton-finish': 'proton-finish',
    '/proton-continue': 'proton-continue',
    '/proton-request-code': 'proton-request-code',
    '/automation-board': 'automation-board',
    '/automation-artifacts': 'automation-artifacts',
    '/security': 'security',
    '/tasks': 'tasks',
    '/automation': 'automation',
    '/automation-catalog': 'automation-catalog',
    '/automation-sites': 'automation-sites',
    '/automation-stack': 'automation-stack',
    '/automation-selectors': 'automation-selectors',
    '/automation-site-registry': 'automation-site-registry',
    '/automation-desktop-status': 'automation-desktop-status',
    '/automation-refresh-sites': 'automation-refresh-sites',
    '/automation-refresh-desktop': 'automation-refresh-desktop',
    '/automation-refresh-stack': 'automation-refresh-stack',
    '/automation-auto': 'automation-auto',
    '/automation-proton-status': 'automation-proton-status',
    '/automation-proton-refresh': 'automation-proton-refresh',
    'commands': 'help',
    '/commands': 'help',
    'help': 'help',
    '/help': 'help',
    'list': 'help',
    '/list': 'help',
}


def normalize_command(value):
    value = (value or '').strip()
    if not value:
        return 'help'
    return ALIASES.get(value, value.lstrip('/'))


def help_payload():
    alias_entries = sorted(
        (alias, target)
        for alias, target in ALIASES.items()
        if alias.startswith('/') and alias != f'/{target}'
    )
    quickstart = [
        {
            'slash': '/mail-board',
            'also': ['/mail'],
            'description': 'totaaloverzicht',
        },
        {
            'slash': '/mail-inbox',
            'description': 'recente mail snel bekijken',
        },
        {
            'slash': '/mail-unread',
            'description': 'alleen ongelezen mail',
        },
        {
            'slash': '/mail-check',
            'also': ['/mail-new'],
            'description': 'alleen echt nieuwe mail sinds de laatste state-update',
        },
        {
            'slash': '/mail-now',
            'description': 'alleen wat nu echt aandacht vraagt',
        },
        {
            'slash': '/mail-first',
            'description': 'beste eerstvolgende mail',
        },
        {
            'slash': '/mail-review-next',
            'description': 'aanbevolen thread meteen openklappen',
        },
        {
            'slash': '/mail-help',
            'also': ['/mail-routes', '/mail-commands'],
            'description': 'toon alle mailroutes en voorbeelden',
        },
    ]
    return {
        'quickstart': quickstart,
        'commands': [
            {
                'name': name,
                'slash': f'/{name}',
                'description': meta['description'],
            }
            for name, meta in sorted(COMMANDS.items())
        ],
        'aliases': [
            {
                'slash': alias,
                'target': f'/{target}',
            }
            for alias, target in alias_entries
        ],
    }


def render_help():
    payload = help_payload()
    lines = [
        'Command dispatch',
        '- gebruik: command-dispatch.py <command> [args]',
        '- slash-vorm werkt ook, bijvoorbeeld /status, /mail of /mail-now',
        '- snelle mailstart:',
    ]
    for item in payload.get('quickstart', []):
        label = item['slash']
        if item.get('also'):
            label = f"{label} of {' of '.join(item['also'])}"
        lines.append(f"  - {label}: {item['description']}")
    lines.append('- beschikbaar:')
    for item in payload['commands']:
        lines.append(f"  - {item['slash']}: {item['description']}")
    if payload['aliases']:
        lines.append('- handige aliassen:')
        for item in payload['aliases']:
            lines.append(f"  - {item['slash']} -> {item['target']}")
    return '\n'.join(lines)


def main():
    raw_args = sys.argv[1:]
    if '--help' in raw_args or '-h' in raw_args:
        if '--json-help' in raw_args:
            print(json.dumps(help_payload(), ensure_ascii=False, indent=2))
        else:
            print(render_help())
        raise SystemExit(0)

    parser = argparse.ArgumentParser(description='Eenvoudige command-router voor board/status/mail/tools workflows', add_help=False)
    parser.add_argument('command', nargs='?')
    parser.add_argument('args', nargs=argparse.REMAINDER)
    parser.add_argument('--json-help', action='store_true')
    parsed = parser.parse_args()

    if parsed.json_help:
        print(json.dumps(help_payload(), ensure_ascii=False, indent=2))
        raise SystemExit(0)

    command = normalize_command(parsed.command)
    if command == 'help':
        print(render_help())
        raise SystemExit(0)
    if command not in COMMANDS:
        sys.stderr.write(f"Onbekend command: {parsed.command}\n")
        sys.stderr.write(render_help() + '\n')
        raise SystemExit(2)

    cmd = COMMANDS[command]['cmd'] + parsed.args
    proc = subprocess.run(cmd, cwd=ROOT, text=True, capture_output=True, check=False)
    if proc.stdout:
        sys.stdout.write(proc.stdout)
    if proc.stderr:
        sys.stderr.write(proc.stderr)
    raise SystemExit(proc.returncode)


if __name__ == '__main__':
    try:
        main()
    except BrokenPipeError:
        raise SystemExit(0)
