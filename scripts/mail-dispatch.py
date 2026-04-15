#!/usr/bin/env python3
import argparse
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path('/home/clawdy/.openclaw/workspace')
SCRIPTS = ROOT / 'scripts'

def with_defaults(args, *defaults):
    values = list(args)
    for flag in reversed(defaults):
        if flag not in values:
            values = [flag] + values
    return values


ROUTES = {
    'catalog': {
        'description': 'Toon beschikbare mail workflow routes',
        'args': [],
        'examples': ['mail-dispatch.py catalog', 'mail-dispatch.py catalog --json'],
        'runner': None,
    },
    'check': {
        'description': 'Check alleen nieuwe mail sinds de laatste state-update',
        'args': [],
        'examples': ['mail-dispatch.py check'],
        'runner': lambda args, json_mode=False: ['python3', str(SCRIPTS / 'check_mail.py')],
    },
    'summary': {
        'description': 'Nieuwe mail met urgentie en actiehints',
        'args': ['--preview?'],
        'examples': ['mail-dispatch.py summary', 'mail-dispatch.py summary --json'],
        'runner': lambda args, json_mode=False: ['python3', str(SCRIPTS / 'mail-summary.py')] + (['--preview'] if '--preview' in args else []) + (['--json'] if json_mode else []),
    },
    'latest': {
        'description': 'Laatste mails snel bekijken, optioneel gegroepeerd per thread of gefilterd op actie, urgency, actualiteit, reviewwaardigheid, afzender of onderwerp',
        'args': ['-n/--limit?', '--preview?', '--unread?', '--meaningful?', '--actionable?', '--current-only?', '--review-worthy?', '--threads?', '--explain-empty?', '--sender <tekst>?', '--subject <tekst>?', '--action <tekst>?', '--urgency <tekst>?', '--search-limit <n>?'],
        'examples': ['mail-dispatch.py latest', 'mail-dispatch.py latest --unread -n 10', 'mail-dispatch.py latest --actionable --threads -n 5', 'mail-dispatch.py latest --meaningful --current-only --threads -n 5', 'mail-dispatch.py latest --review-worthy --threads -n 5', 'mail-dispatch.py latest --review-worthy --threads --explain-empty -n 5', 'mail-dispatch.py latest --action "security checken" --urgency high', 'mail-dispatch.py latest --sender Proton --subject verification'],
        'runner': lambda args, json_mode=False: ['python3', str(SCRIPTS / 'mail-latest.py')] + args + (['--json'] if json_mode else []),
    },
    'drafts': {
        'description': 'Concept-antwoorden op basis van nieuwe, ongelezen of recente mail',
        'args': ['-n/--limit?', '--unread?', '--all?'],
        'examples': ['mail-dispatch.py drafts', 'mail-dispatch.py drafts --unread', 'mail-dispatch.py drafts --all --json'],
        'runner': lambda args, json_mode=False: ['python3', str(SCRIPTS / 'mail-drafts.py')] + args + (['--json'] if json_mode else []),
    },
    'triage': {
        'description': 'Prioriteer ongelezen of recente mail met actiehints en reply-signalen, met automatische samenklap van herhalende stale no-reply ruis',
        'args': ['-n/--limit?', '--all?/--recent?', '--preview?', '--reply-only?', '--high-only?', '--current-only?', '--review-worthy?', '--clusters?', '--search-limit <n>?', '--explain-empty?'],
        'examples': ['mail-dispatch.py triage', 'mail-dispatch.py triage --recent --preview', 'mail-dispatch.py triage --reply-only', 'mail-dispatch.py triage --recent --current-only', 'mail-dispatch.py triage --recent --review-worthy', 'mail-dispatch.py triage --recent --review-worthy --explain-empty', 'mail-dispatch.py triage --recent --clusters'],
        'runner': lambda args, json_mode=False: ['python3', str(SCRIPTS / 'mail-triage.py')] + args + (['--json'] if json_mode else []),
    },
    'triage-now': {
        'description': 'Prioriteer direct alleen actuele mail met aandachtssignaal, zonder stale fallback',
        'args': ['-n/--limit?', '--preview?', '--reply-only?', '--high-only?', '--clusters?', '--search-limit <n>?', '--explain-empty?'],
        'examples': ['mail-dispatch.py triage-now', 'mail-dispatch.py triage-now --reply-only', 'mail-dispatch.py triage-now --clusters --json', 'mail-dispatch.py triage-now --explain-empty'],
        'runner': lambda args, json_mode=False: ['python3', str(SCRIPTS / 'mail-triage.py')] + with_defaults(args, '--all', '--current-only') + (['--json'] if json_mode else []),
    },
    'triage-review': {
        'description': 'Prioriteer direct alleen reviewwaardige mail zonder code-only of ruisfallback',
        'args': ['-n/--limit?', '--preview?', '--reply-only?', '--high-only?', '--clusters?', '--search-limit <n>?', '--explain-empty?'],
        'examples': ['mail-dispatch.py triage-review', 'mail-dispatch.py triage-review --clusters', 'mail-dispatch.py triage-review --reply-only --json', 'mail-dispatch.py triage-review --explain-empty'],
        'runner': lambda args, json_mode=False: ['python3', str(SCRIPTS / 'mail-triage.py')] + with_defaults(args, '--all', '--review-worthy') + (['--json'] if json_mode else []),
    },
    'now': {
        'description': 'Toon alleen recente mail die nu echt aandacht vraagt, met reply/high filters optioneel en optionele noop-uitleg',
        'args': ['-n/--limit?', '--preview?', '--reply-only?', '--high-only?', '--clusters?', '--search-limit <n>?', '--explain-empty?'],
        'examples': ['mail-dispatch.py now', 'mail-dispatch.py now --reply-only', 'mail-dispatch.py now --explain-empty', 'mail-dispatch.py now --clusters --json'],
        'runner': lambda args, json_mode=False: ['python3', str(SCRIPTS / 'mail-triage.py')] + with_defaults(args, '--all', '--current-only') + (['--json'] if json_mode else []),
    },
    'focus': {
        'description': 'Kies de ene beste mail om nu als eerste op te pakken, optioneel current-only, review-worthy of met conceptantwoord',
        'args': ['-n/--limit?', '--preview?', '--draft?', '--current-only?', '--review-worthy?', '--search-limit <n>?'],
        'examples': ['mail-dispatch.py focus', 'mail-dispatch.py focus --draft', 'mail-dispatch.py focus --current-only', 'mail-dispatch.py focus --review-worthy', 'mail-dispatch.py focus --json'],
        'runner': lambda args, json_mode=False: ['python3', str(SCRIPTS / 'mail-focus.py')] + args + (['--json'] if json_mode else []),
    },
    'focus-now': {
        'description': 'Kies direct de beste actuele mail-focus zonder stale fallback',
        'args': ['-n/--limit?', '--preview?', '--draft?', '--search-limit <n>?'],
        'examples': ['mail-dispatch.py focus-now', 'mail-dispatch.py focus-now --draft', 'mail-dispatch.py focus-now --json'],
        'runner': lambda args, json_mode=False: ['python3', str(SCRIPTS / 'mail-focus.py')] + with_defaults(args, '--current-only') + (['--json'] if json_mode else []),
    },
    'focus-review': {
        'description': 'Kies direct de beste reviewwaardige mail-focus zonder code-only of ruisfallback',
        'args': ['-n/--limit?', '--preview?', '--draft?', '--search-limit <n>?'],
        'examples': ['mail-dispatch.py focus-review', 'mail-dispatch.py focus-review --draft', 'mail-dispatch.py focus-review --json'],
        'runner': lambda args, json_mode=False: ['python3', str(SCRIPTS / 'mail-focus.py')] + with_defaults(args, '--review-worthy') + (['--json'] if json_mode else []),
    },
    'next-step': {
        'description': 'Bepaal de volgende nuttige mailstap, ook als er geen actuele unread-focus meer is',
        'args': ['-n/--limit?', '--draft?', '--current-only?', '--review-worthy?'],
        'examples': ['mail-dispatch.py next-step', 'mail-dispatch.py next-step --draft', 'mail-dispatch.py next-step --current-only', 'mail-dispatch.py next-step --review-worthy', 'mail-dispatch.py next-step -n 3', 'mail-dispatch.py next-step --json'],
        'runner': lambda args, json_mode=False: ['python3', str(SCRIPTS / 'mail-next-step.py')] + args + (['--json'] if json_mode else []),
    },
    'security-alerts': {
        'description': 'Vat actuele en recente security-alert mailclusters samen, met directe review-command',
        'args': ['-n/--limit?', '--current-only?', '--explain-empty?'],
        'examples': ['mail-dispatch.py security-alerts', 'mail-dispatch.py security-alerts --current-only', 'mail-dispatch.py security-alerts --explain-empty', 'mail-dispatch.py security-alerts -n 3', 'mail-dispatch.py security-alerts --json'],
        'runner': lambda args, json_mode=False: ['python3', str(SCRIPTS / 'mail-security-alerts.py')] + args + (['--json'] if json_mode else []),
    },
    'queue': {
        'description': 'Toon een korte prioriteitslijst van de beste volgende mailacties',
        'args': ['-n/--limit?', '--draft?', '--current-only?', '--review-worthy?'],
        'examples': ['mail-dispatch.py queue', 'mail-dispatch.py queue --current-only', 'mail-dispatch.py queue --review-worthy', 'mail-dispatch.py queue -n 3', 'mail-dispatch.py queue --json'],
        'runner': lambda args, json_mode=False: ['python3', str(SCRIPTS / 'mail-next-step.py')] + (([] if ('--limit' in args or '-n' in args) else ['--limit', '3']) + args) + (['--json'] if json_mode else []),
    },
    'review-next': {
        'description': 'Open direct de aanbevolen volgende mailthread met context, alternatieven en optioneel conceptantwoord',
        'args': ['-n/--limit?', '--messages <n>?', '--preview?', '--draft?', '--meaningful?', '--current-only?', '--review-worthy?', '--explain-empty?', '--candidate <n>?'],
        'examples': ['mail-dispatch.py review-next', 'mail-dispatch.py review-next --current-only', 'mail-dispatch.py review-next --review-worthy', 'mail-dispatch.py review-next --review-worthy --explain-empty', 'mail-dispatch.py review-next --candidate 2', 'mail-dispatch.py review-next --draft', 'mail-dispatch.py review-next --preview', 'mail-dispatch.py review-next --json'],
        'runner': lambda args, json_mode=False: ['python3', str(SCRIPTS / 'mail-review-next.py')] + args + (['--json'] if json_mode else []),
    },
    'thread': {
        'description': 'Klap één recente mailthread compact uit, met filters op afzender/onderwerp/actie, reviewwaardigheid en optioneel conceptantwoord',
        'args': ['-n/--limit?', '--search-limit <n>?', '--meaningful?', '--current-only?', '--review-worthy?', '--unread?', '--uid <n>?', '--sender <text>?', '--subject <text>?', '--action <text>?', '--messages <n>?', '--preview?', '--draft?', '--explain-empty?'],
        'examples': ['mail-dispatch.py thread', 'mail-dispatch.py thread --meaningful --current-only', 'mail-dispatch.py thread --review-worthy', 'mail-dispatch.py thread --review-worthy --explain-empty', 'mail-dispatch.py thread --sender bitwarden --draft', 'mail-dispatch.py thread --subject factuur --messages 5'],
        'runner': lambda args, json_mode=False: ['python3', str(SCRIPTS / 'mail-thread.py')] + args + (['--json'] if json_mode else []),
    },
    'thread-now': {
        'description': 'Open direct alleen een actuele mailthread zonder stale fallback',
        'args': ['-n/--limit?', '--search-limit <n>?', '--meaningful?', '--unread?', '--uid <n>?', '--sender <text>?', '--subject <text>?', '--action <text>?', '--messages <n>?', '--preview?', '--draft?', '--explain-empty?'],
        'examples': ['mail-dispatch.py thread-now', 'mail-dispatch.py thread-now --explain-empty', 'mail-dispatch.py thread-now --sender github --json', 'mail-dispatch.py thread-now --subject factuur --messages 5'],
        'runner': lambda args, json_mode=False: ['python3', str(SCRIPTS / 'mail-thread.py')] + with_defaults(args, '--current-only') + (['--json'] if json_mode else []),
    },
    'thread-review': {
        'description': 'Open direct alleen een reviewwaardige mailthread zonder code-only of ruisfallback',
        'args': ['-n/--limit?', '--search-limit <n>?', '--meaningful?', '--unread?', '--uid <n>?', '--sender <text>?', '--subject <text>?', '--action <text>?', '--messages <n>?', '--preview?', '--draft?', '--explain-empty?'],
        'examples': ['mail-dispatch.py thread-review', 'mail-dispatch.py thread-review --explain-empty', 'mail-dispatch.py thread-review --sender bitwarden --json', 'mail-dispatch.py thread-review --messages 5'],
        'runner': lambda args, json_mode=False: ['python3', str(SCRIPTS / 'mail-thread.py')] + with_defaults(args, '--review-worthy') + (['--json'] if json_mode else []),
    },
    'codes': {
        'description': 'Zoek verificatiecodes in recente mail, standaard samengeklapt per vergelijkbare code-mailgroep',
        'args': ['-n/--limit?', '--sender?', '--subject?', '--current-only?', '--explain-empty?', '--all?'],
        'examples': ['mail-dispatch.py codes', 'mail-dispatch.py codes --current-only', 'mail-dispatch.py codes --current-only --explain-empty', 'mail-dispatch.py codes --sender proton', 'mail-dispatch.py codes --all --json'],
        'runner': lambda args, json_mode=False: ['python3', str(SCRIPTS / 'mail-verification-codes.py')] + args + (['--json'] if json_mode else []),
    },
    'board': {
        'description': 'Compact totaaloverzicht van latest/unread/new/drafts, optioneel alleen voor actuele of reviewwaardige mail',
        'args': ['-n/--limit?', '--preview?', '--current-only?', '--review-worthy?'],
        'examples': ['mail-dispatch.py board', 'mail-dispatch.py board --current-only', 'mail-dispatch.py board --review-worthy', 'mail-dispatch.py board --json'],
        'runner': lambda args, json_mode=False: ['python3', str(SCRIPTS / 'mailboard.py')] + args + (['--json'] if json_mode else []),
    },
}
ALIASES = {
    'new': 'check',
    'inbox': 'latest',
    'unread': 'latest',
    'verify': 'codes',
    'overview': 'board',
    'prioritize': 'triage',
    'inbox-triage': 'triage',
    'next': 'focus',
    'first': 'focus',
    'focus-current': 'focus-now',
    'focus-review-worthy': 'focus-review',
    'followup': 'next-step',
    'next-mail-step': 'next-step',
    'security': 'security-alerts',
    'alerts': 'security-alerts',
    'worklist': 'queue',
    'todo': 'queue',
    'review': 'review-next',
    'mailthread': 'thread',
    'thread-current': 'thread-now',
    'thread-now-current': 'thread-now',
    'thread-review-worthy': 'thread-review',
    'next-thread': 'review-next',
    'conversation': 'thread',
    'reply-needed': 'triage',
    'high-priority': 'triage',
    'clusters': 'triage',
    'current': 'now',
    'urgent': 'now',
}


def normalize_route(value):
    value = (value or 'catalog').strip()
    return ALIASES.get(value, value)


def catalog_payload():
    return {
        'quickstart': [
            {
                'route': 'board',
                'description': 'totaaloverzicht van mailstatus',
            },
            {
                'route': 'latest --unread',
                'description': 'alleen ongelezen mail',
            },
            {
                'route': 'check',
                'description': 'alleen echt nieuwe mail sinds laatste state-update',
            },
            {
                'route': 'now --explain-empty',
                'description': 'alleen wat nu echt aandacht vraagt, met suppressed-uitleg als het leeg is',
            },
            {
                'route': 'triage-now --explain-empty',
                'description': 'actuele prioritering met suppressed-uitleg bij een lege actuele mailbox',
            },
            {
                'route': 'triage-review --explain-empty',
                'description': 'reviewwaardige prioritering met suppressed-uitleg bij noop',
            },
            {
                'route': 'security-alerts --current-only --explain-empty',
                'description': 'alleen actuele security- of loginmeldingen, met uitleg bij noop',
            },
            {
                'route': 'codes --current-only --explain-empty',
                'description': 'alleen actuele verificatiecodes, met uitleg bij lege mailbox',
            },
            {
                'route': 'focus-now',
                'description': 'beste actuele mail-focus zonder stale fallback',
            },
            {
                'route': 'focus-review',
                'description': 'beste reviewwaardige mail-focus zonder code-only of ruisfallback',
            },
            {
                'route': 'thread-now --explain-empty',
                'description': 'open direct alleen een actuele thread, met suppressed-uitleg bij noop',
            },
            {
                'route': 'thread-review --explain-empty',
                'description': 'open direct alleen een reviewwaardige thread, met suppressed-uitleg bij noop',
            },
            {
                'route': 'review-next',
                'description': 'aanbevolen thread meteen openen',
            },
        ],
        'routes': [
            {
                'name': name,
                'description': meta['description'],
                'args': meta['args'],
                'examples': meta['examples'],
            }
            for name, meta in ROUTES.items()
        ],
        'aliases': ALIASES,
        'notes': 'Gebruik board voor een snel totaalbeeld, eventueel met --current-only voor alleen actuele aandacht of met --review-worthy voor alleen nog zinnige reviewmail. Gebruik now voor wat nu echt aandacht vraagt, en voeg daar --explain-empty toe als je bij een lege actuele mailbox meteen wilt zien welke recente ruis bewust is onderdrukt. Triage-now en triage-review geven diezelfde twee gefilterde prioriteringsroutes meteen direct zonder losse --current-only of --review-worthy flags. Focus is voor de ene beste eerstvolgende mail, desnoods met --current-only voor alleen actuele focus of --review-worthy voor alleen nog zinvolle reviewfocus. Focus-now en focus-review geven die twee gefilterde focusroutes meteen direct zonder extra flags. Next-step gebruik je voor de volgende nuttige mailactie inclusief follow-up buiten unread of met --current-only juist zonder stale fallback of met --review-worthy zonder code-only/noise fallback. Review-next klapt die aanbevolen thread meteen open met context/concept, via --candidate open je een alternatief uit de queue, met --current-only of --review-worthy maak je de kandidaatset strakker, en met --explain-empty zie je bij noop welke kandidaten bewust zijn onderdrukt. Thread klapt één specifieke conversatie compact uit, thread-now en thread-review geven diezelfde twee nuttigste filters meteen direct zonder losse flags, en met --explain-empty laat je ook daar lege threadselectie compact verklaren. Triage gebruik je voor prioritering van unread mail, waarbij herhalende stale no-reply ruis in itemmode automatisch wordt samengeklapt, compacte clusters via --clusters, alleen actuele aandacht via --current-only of alleen nog zinnige reviewitems via --review-worthy, en voeg ook daar --explain-empty toe als je lege resultaten compact wilt laten verklaren. Security-alerts gebruik je voor account- of loginmeldingen, daar sluit --current-only recente reviewfallback uit, en met --explain-empty zie je welke securityclusters bewust zijn onderdrukt. Codes klapt vergelijkbare verificatiemails nu standaard samen, met --current-only zie je alleen nog bruikbare codes, en met --explain-empty krijg je bij lege current-only output direct de onderdrukte oudere codegroepen met reden. Latest gebruik je voor inbox-scan of thread-view en daar helpt --explain-empty ook bij lege current/review-filters. Summary blijft voor alleen nieuwe mail sinds state.',
    }


def render_catalog():
    payload = catalog_payload()
    lines = ['Mail workflow dispatch']
    if payload.get('quickstart'):
        lines.append('- snelle start:')
        for item in payload['quickstart']:
            lines.append(f"  - {item['route']}: {item['description']}")
    for route in payload['routes']:
        arg_text = f" ({', '.join(route['args'])})" if route['args'] else ''
        lines.append(f"- {route['name']} {route['description']}{arg_text}")
    if payload['aliases']:
        lines.append(f"- aliases: {', '.join(f'{k}->{v}' for k, v in sorted(payload['aliases'].items()))}")
    lines.append(f"- note: {payload['notes']}")
    return '\n'.join(lines)


def run(cmd):
    proc = subprocess.run(cmd, cwd=ROOT, text=True, capture_output=True, check=False)
    if proc.stdout:
        sys.stdout.write(proc.stdout)
    if proc.stderr:
        sys.stderr.write(proc.stderr)
    raise SystemExit(proc.returncode)


def main():
    raw_args = sys.argv[1:]
    if '--help' in raw_args or '-h' in raw_args:
        if '--json' in raw_args:
            print(json.dumps(catalog_payload(), ensure_ascii=False, indent=2))
        else:
            print(render_catalog())
        return

    parser = argparse.ArgumentParser(description='Dispatcher voor Clawdy mail workflows', add_help=False)
    parser.add_argument('--json', action='store_true')
    parser.add_argument('route', nargs='?', default='catalog')
    parsed, passthrough_args = parser.parse_known_args()

    route = normalize_route(parsed.route)
    if route == 'catalog':
        if parsed.json:
            print(json.dumps(catalog_payload(), ensure_ascii=False, indent=2))
        else:
            print(render_catalog())
        return
    if route not in ROUTES:
        raise SystemExit(f'Onbekende route: {parsed.route}')

    passthrough = list(passthrough_args)
    if parsed.route == 'unread' and '--unread' not in passthrough:
        passthrough = ['--unread'] + passthrough
    if parsed.route == 'reply-needed' and '--reply-only' not in passthrough:
        passthrough = ['--reply-only'] + passthrough
    if parsed.route == 'high-priority' and '--high-only' not in passthrough:
        passthrough = ['--high-only'] + passthrough
    if parsed.route == 'clusters':
        if '--clusters' not in passthrough and '--clusters-only' not in passthrough:
            passthrough = ['--clusters'] + passthrough
        if '--all' not in passthrough and '--recent' not in passthrough:
            passthrough = ['--all'] + passthrough

    cmd = ROUTES[route]['runner'](passthrough, json_mode=parsed.json)
    run(cmd)


if __name__ == '__main__':
    try:
        main()
    except BrokenPipeError:
        raise SystemExit(0)
