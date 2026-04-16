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
    'latest-now': {
        'description': 'Bekijk direct alleen actuele recente mail of threads zonder losse --current-only vlag',
        'args': ['-n/--limit?', '--preview?', '--unread?', '--meaningful?', '--actionable?', '--threads?', '--explain-empty?', '--sender <tekst>?', '--subject <tekst>?', '--action <tekst>?', '--urgency <tekst>?', '--search-limit <n>?'],
        'examples': ['mail-dispatch.py latest-now', 'mail-dispatch.py latest-now --threads --explain-empty -n 5', 'mail-dispatch.py latest-now --sender github --json'],
        'runner': lambda args, json_mode=False: ['python3', str(SCRIPTS / 'mail-latest.py')] + with_defaults(args, '--current-only') + (['--json'] if json_mode else []),
    },
    'latest-review': {
        'description': 'Bekijk direct alleen reviewwaardige recente mail of threads zonder losse --review-worthy vlag',
        'args': ['-n/--limit?', '--preview?', '--unread?', '--meaningful?', '--actionable?', '--threads?', '--explain-empty?', '--sender <tekst>?', '--subject <tekst>?', '--action <tekst>?', '--urgency <tekst>?', '--search-limit <n>?'],
        'examples': ['mail-dispatch.py latest-review', 'mail-dispatch.py latest-review --threads --explain-empty -n 5', 'mail-dispatch.py latest-review --subject factuur --json'],
        'runner': lambda args, json_mode=False: ['python3', str(SCRIPTS / 'mail-latest.py')] + with_defaults(args, '--review-worthy') + (['--json'] if json_mode else []),
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
    'next-step-now': {
        'description': 'Bepaal direct alleen de volgende actuele mailstap zonder stale fallback',
        'args': ['-n/--limit?', '--draft?'],
        'examples': ['mail-dispatch.py next-step-now', 'mail-dispatch.py next-step-now --draft', 'mail-dispatch.py next-step-now --json'],
        'runner': lambda args, json_mode=False: ['python3', str(SCRIPTS / 'mail-next-step.py')] + with_defaults(args, '--current-only') + (['--json'] if json_mode else []),
    },
    'next-step-review': {
        'description': 'Bepaal direct alleen de volgende reviewwaardige mailstap zonder code-only of ruisfallback',
        'args': ['-n/--limit?', '--draft?'],
        'examples': ['mail-dispatch.py next-step-review', 'mail-dispatch.py next-step-review --draft', 'mail-dispatch.py next-step-review --json'],
        'runner': lambda args, json_mode=False: ['python3', str(SCRIPTS / 'mail-next-step.py')] + with_defaults(args, '--review-worthy') + (['--json'] if json_mode else []),
    },
    'security-alerts': {
        'description': 'Vat actuele en recente security-alert mailclusters samen, met directe review-command',
        'args': ['-n/--limit?', '--current-only?', '--explain-empty?'],
        'examples': ['mail-dispatch.py security-alerts', 'mail-dispatch.py security-alerts --current-only', 'mail-dispatch.py security-alerts --explain-empty', 'mail-dispatch.py security-alerts -n 3', 'mail-dispatch.py security-alerts --json'],
        'runner': lambda args, json_mode=False: ['python3', str(SCRIPTS / 'mail-security-alerts.py')] + args + (['--json'] if json_mode else []),
    },
    'security-alerts-now': {
        'description': 'Bekijk direct alleen actuele security- of loginmeldingen zonder losse --current-only en --explain-empty vlaggen',
        'args': ['-n/--limit?'],
        'examples': ['mail-dispatch.py security-alerts-now', 'mail-dispatch.py security-alerts-now -n 3', 'mail-dispatch.py security-alerts-now --json'],
        'runner': lambda args, json_mode=False: ['python3', str(SCRIPTS / 'mail-security-alerts.py')] + with_defaults(args, '--current-only', '--explain-empty') + (['--json'] if json_mode else []),
    },
    'queue': {
        'description': 'Toon een korte prioriteitslijst van de beste volgende mailacties',
        'args': ['-n/--limit?', '--draft?', '--current-only?', '--review-worthy?'],
        'examples': ['mail-dispatch.py queue', 'mail-dispatch.py queue --current-only', 'mail-dispatch.py queue --review-worthy', 'mail-dispatch.py queue -n 3', 'mail-dispatch.py queue --json'],
        'runner': lambda args, json_mode=False: ['python3', str(SCRIPTS / 'mail-next-step.py')] + (([] if ('--limit' in args or '-n' in args) else ['--limit', '3']) + args) + (['--json'] if json_mode else []),
    },
    'queue-now': {
        'description': 'Toon direct alleen een actuele mailwerkrij zonder stale fallback',
        'args': ['-n/--limit?', '--draft?'],
        'examples': ['mail-dispatch.py queue-now', 'mail-dispatch.py queue-now --draft', 'mail-dispatch.py queue-now --json'],
        'runner': lambda args, json_mode=False: ['python3', str(SCRIPTS / 'mail-next-step.py')] + (([] if ('--limit' in args or '-n' in args) else ['--limit', '3']) + with_defaults(args, '--current-only')) + (['--json'] if json_mode else []),
    },
    'queue-review': {
        'description': 'Toon direct alleen reviewwaardige mailvervolgstappen zonder code-only of ruisfallback',
        'args': ['-n/--limit?', '--draft?'],
        'examples': ['mail-dispatch.py queue-review', 'mail-dispatch.py queue-review --draft', 'mail-dispatch.py queue-review --json'],
        'runner': lambda args, json_mode=False: ['python3', str(SCRIPTS / 'mail-next-step.py')] + (([] if ('--limit' in args or '-n' in args) else ['--limit', '3']) + with_defaults(args, '--review-worthy')) + (['--json'] if json_mode else []),
    },
    'review-next': {
        'description': 'Open direct de aanbevolen volgende mailthread met context, alternatieven en optioneel conceptantwoord',
        'args': ['-n/--limit?', '--messages <n>?', '--preview?', '--draft?', '--meaningful?', '--current-only?', '--review-worthy?', '--explain-empty?', '--candidate <n>?'],
        'examples': ['mail-dispatch.py review-next', 'mail-dispatch.py review-next --current-only', 'mail-dispatch.py review-next --review-worthy', 'mail-dispatch.py review-next --review-worthy --explain-empty', 'mail-dispatch.py review-next --candidate 2', 'mail-dispatch.py review-next --draft', 'mail-dispatch.py review-next --preview', 'mail-dispatch.py review-next --json'],
        'runner': lambda args, json_mode=False: ['python3', str(SCRIPTS / 'mail-review-next.py')] + args + (['--json'] if json_mode else []),
    },
    'review-next-now': {
        'description': 'Open direct alleen de aanbevolen actuele mailthread zonder losse --current-only vlag',
        'args': ['-n/--limit?', '--messages <n>?', '--preview?', '--draft?', '--meaningful?', '--explain-empty?', '--candidate <n>?'],
        'examples': ['mail-dispatch.py review-next-now', 'mail-dispatch.py review-next-now --explain-empty', 'mail-dispatch.py review-next-now --candidate 2', 'mail-dispatch.py review-next-now --json'],
        'runner': lambda args, json_mode=False: ['python3', str(SCRIPTS / 'mail-review-next.py')] + with_defaults(args, '--current-only') + (['--json'] if json_mode else []),
    },
    'review-next-review': {
        'description': 'Open direct alleen de aanbevolen reviewwaardige mailthread zonder losse --review-worthy vlag',
        'args': ['-n/--limit?', '--messages <n>?', '--preview?', '--draft?', '--meaningful?', '--explain-empty?', '--candidate <n>?'],
        'examples': ['mail-dispatch.py review-next-review', 'mail-dispatch.py review-next-review --explain-empty', 'mail-dispatch.py review-next-review --candidate 2', 'mail-dispatch.py review-next-review --json'],
        'runner': lambda args, json_mode=False: ['python3', str(SCRIPTS / 'mail-review-next.py')] + with_defaults(args, '--review-worthy') + (['--json'] if json_mode else []),
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
        'description': 'Zoek verificatiecodes in recente mail, ook via code, verify, otp en auth-code, standaard samengeklapt per vergelijkbare code-mailgroep',
        'args': ['-n/--limit?', '--sender?', '--subject?', '--current-only?', '--explain-empty?', '--all?'],
        'examples': ['mail-dispatch.py codes', 'mail-dispatch.py code', 'mail-dispatch.py otp', 'mail-dispatch.py auth-code', 'mail-dispatch.py codes --current-only --explain-empty', 'mail-dispatch.py codes --sender proton', 'mail-dispatch.py codes --all --json'],
        'runner': lambda args, json_mode=False: ['python3', str(SCRIPTS / 'mail-verification-codes.py')] + args + (['--json'] if json_mode else []),
    },
    'codes-now': {
        'description': 'Bekijk direct alleen actuele verificatiecodes zonder losse --current-only en --explain-empty vlaggen',
        'args': ['-n/--limit?', '--sender?', '--subject?', '--all?'],
        'examples': ['mail-dispatch.py codes-now', 'mail-dispatch.py codes-now --sender proton', 'mail-dispatch.py codes-now --json'],
        'runner': lambda args, json_mode=False: ['python3', str(SCRIPTS / 'mail-verification-codes.py')] + with_defaults(args, '--current-only', '--explain-empty') + (['--json'] if json_mode else []),
    },
    'board': {
        'description': 'Compact totaaloverzicht van latest/unread/new/drafts, optioneel alleen voor actuele of reviewwaardige mail',
        'args': ['-n/--limit?', '--preview?', '--current-only?', '--review-worthy?'],
        'examples': ['mail-dispatch.py board', 'mail-dispatch.py board --current-only', 'mail-dispatch.py board --review-worthy', 'mail-dispatch.py board --json'],
        'runner': lambda args, json_mode=False: ['python3', str(SCRIPTS / 'mailboard.py')] + args + (['--json'] if json_mode else []),
    },
    'board-now': {
        'description': 'Toon direct alleen een compact board met actuele mailaandacht zonder losse --current-only vlag',
        'args': ['-n/--limit?', '--preview?'],
        'examples': ['mail-dispatch.py board-now', 'mail-dispatch.py board-now --preview', 'mail-dispatch.py board-now --json'],
        'runner': lambda args, json_mode=False: ['python3', str(SCRIPTS / 'mailboard.py')] + with_defaults(args, '--current-only') + (['--json'] if json_mode else []),
    },
    'board-review': {
        'description': 'Toon direct alleen een compact board met reviewwaardige mail zonder losse --review-worthy vlag',
        'args': ['-n/--limit?', '--preview?'],
        'examples': ['mail-dispatch.py board-review', 'mail-dispatch.py board-review --preview', 'mail-dispatch.py board-review --json'],
        'runner': lambda args, json_mode=False: ['python3', str(SCRIPTS / 'mailboard.py')] + with_defaults(args, '--review-worthy') + (['--json'] if json_mode else []),
    },
}
ALIASES = {
    'new': 'check',
    'inbox': 'latest',
    'unread': 'latest',
    'code': 'codes',
    'codes': 'codes',
    'verify': 'codes',
    'otp': 'codes',
    'auth-code': 'codes',
    'code-now': 'codes-now',
    'code-current': 'codes-now',
    'codes-current': 'codes-now',
    'verify-now': 'codes-now',
    'verify-current': 'codes-now',
    'otp-now': 'codes-now',
    'otp-current': 'codes-now',
    'auth-code-now': 'codes-now',
    'auth-code-current': 'codes-now',
    'overview': 'board',
    'overview-now': 'board-now',
    'overview-current': 'board-now',
    'overview-review': 'board-review',
    'overview-review-worthy': 'board-review',
    'board-current': 'board-now',
    'board-now-current': 'board-now',
    'board-review-worthy': 'board-review',
    'prioritize': 'triage',
    'inbox-triage': 'triage',
    'next': 'focus',
    'first': 'focus',
    'latest-current': 'latest-now',
    'latest-now-current': 'latest-now',
    'latest-review-worthy': 'latest-review',
    'triage-current': 'triage-now',
    'triage-review-worthy': 'triage-review',
    'focus-current': 'focus-now',
    'focus-review-worthy': 'focus-review',
    'followup': 'next-step',
    'next-mail-step': 'next-step',
    'next-step-current': 'next-step-now',
    'next-now': 'next-step-now',
    'next-step-review-worthy': 'next-step-review',
    'next-review': 'next-step-review',
    'security': 'security-alerts',
    'alerts': 'security-alerts',
    'security-now': 'security-alerts-now',
    'security-current': 'security-alerts-now',
    'security-alerts-current': 'security-alerts-now',
    'alerts-now': 'security-alerts-now',
    'alerts-current': 'security-alerts-now',
    'worklist': 'queue',
    'todo': 'queue',
    'worklist-now': 'queue-now',
    'worklist-current': 'queue-now',
    'todo-now': 'queue-now',
    'todo-current': 'queue-now',
    'worklist-review': 'queue-review',
    'worklist-review-worthy': 'queue-review',
    'todo-review': 'queue-review',
    'todo-review-worthy': 'queue-review',
    'queue-current': 'queue-now',
    'queue-now-current': 'queue-now',
    'queue-review-worthy': 'queue-review',
    'review': 'review-next',
    'open': 'review-next',
    'review-next-current': 'review-next-now',
    'review-now': 'review-next-now',
    'open-current': 'review-next-now',
    'open-now': 'review-next-now',
    'review-next-review-worthy': 'review-next-review',
    'review-review': 'review-next-review',
    'open-review': 'review-next-review',
    'open-review-worthy': 'review-next-review',
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
                'route': 'board-now',
                'description': 'compact board met alleen actuele aandacht zonder losse flags',
            },
            {
                'route': 'board-review',
                'description': 'compact board met alleen reviewwaardige mail zonder losse flags',
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
                'route': 'latest-now --threads --explain-empty',
                'description': 'alleen actuele recente threads, met suppressed-uitleg als het leeg is',
            },
            {
                'route': 'latest-review --threads --explain-empty',
                'description': 'alleen reviewwaardige recente threads, met noop-uitleg als het leeg is',
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
                'route': 'security-alerts-now',
                'description': 'alleen actuele security- of loginmeldingen, met noop-uitleg al ingebouwd',
            },
            {
                'route': 'code-now',
                'description': 'alleen actuele verificatiecodes, ook via verify-now, otp-now, auth-code-now en codes-now, met uitleg bij lege mailbox al ingebouwd',
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
                'route': 'next-step-now',
                'description': 'beste actuele vervolgstap zonder stale fallback',
            },
            {
                'route': 'next-step-review',
                'description': 'beste reviewwaardige vervolgstap zonder ruisfallback',
            },
            {
                'route': 'queue-now',
                'description': 'korte actuele werkrij zonder stale fallback, ook via worklist-now, worklist-current, todo-now of todo-current',
            },
            {
                'route': 'queue-review',
                'description': 'korte reviewwaardige werkrij zonder code-only of ruisfallback, ook via worklist-review, worklist-review-worthy, todo-review of todo-review-worthy',
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
                'route': 'open-now --explain-empty',
                'description': 'aanbevolen actuele thread meteen openen, met suppressed-uitleg bij noop',
            },
            {
                'route': 'open-review --explain-empty',
                'description': 'aanbevolen reviewwaardige thread meteen openen, met suppressed-uitleg bij noop',
            },
            {
                'route': 'open',
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
        'notes': 'Gebruik board voor een snel totaalbeeld, eventueel met --current-only voor alleen actuele aandacht of met --review-worthy voor alleen nog zinnige reviewmail. Board-now en board-review geven die twee nuttigste boardfilters nu ook direct zonder losse flags, en overview-current plus overview-review-worthy gebruiken daar nu ook dezelfde current/review-taal voor. Gebruik latest voor inbox-scan of thread-view, desnoods met --current-only of --review-worthy, en latest-now plus latest-review geven die twee nuttigste latest-filters meteen direct zonder losse flags. Voeg bij lege current/review-runs --explain-empty toe om onderdrukte recente ruis direct te zien. Gebruik now voor wat nu echt aandacht vraagt, en voeg daar --explain-empty toe als je bij een lege actuele mailbox meteen wilt zien welke recente ruis bewust is onderdrukt. Triage-now en triage-review geven diezelfde twee gefilterde prioriteringsroutes meteen direct zonder losse --current-only of --review-worthy flags, en triage-current plus triage-review-worthy gebruiken daar nu ook dezelfde current/review-taal voor. Focus is voor de ene beste eerstvolgende mail, desnoods met --current-only voor alleen actuele focus of --review-worthy voor alleen nog zinvolle reviewfocus. Focus-now en focus-review geven die twee gefilterde focusroutes meteen direct zonder extra flags. Next-step gebruik je voor de volgende nuttige mailactie inclusief follow-up buiten unread of met --current-only juist zonder stale fallback of met --review-worthy zonder code-only/noise fallback. Next-step-now, next-step-review, queue-now en queue-review geven die twee nuttigste vervolgfilters nu ook direct zonder losse flags, en worklist-current plus todo-current of worklist-review-worthy plus todo-review-worthy gebruiken daarbij dezelfde current/review-taal. Review-next klapt die aanbevolen thread meteen open met context/concept, review-next-now en review-next-review geven daarvan nu ook de twee nuttigste filters direct zonder losse flags, via --candidate open je een alternatief uit de queue, en met --explain-empty zie je bij noop welke kandidaten bewust zijn onderdrukt. De korte aliasen open, open-current, open-now, open-review en open-review-worthy geven diezelfde openroutes nu ook direct via mailboxtaal zonder review-prefix. Thread klapt één specifieke conversatie compact uit, thread-now en thread-review geven diezelfde twee nuttigste filters meteen direct zonder losse flags, en met --explain-empty laat je ook daar lege threadselectie compact verklaren. Triage gebruik je voor prioritering van unread mail, waarbij herhalende stale no-reply ruis in itemmode automatisch wordt samengeklapt, compacte clusters via --clusters, alleen actuele aandacht via --current-only of alleen nog zinnige reviewitems via --review-worthy, en voeg ook daar --explain-empty toe als je lege resultaten compact wilt laten verklaren. Security-alerts gebruik je voor account- of loginmeldingen, daar sluit --current-only recente reviewfallback uit, met --explain-empty zie je welke securityclusters bewust zijn onderdrukt, en security-alerts-now geeft die actuele noop-verklaarde check nu ook direct zonder losse flags. Codes klapt vergelijkbare verificatiemails nu standaard samen, ook via de korte aliasen code, verify, otp en auth-code, met --current-only zie je alleen nog bruikbare codes, met --explain-empty krijg je bij lege current-only output direct de onderdrukte oudere codegroepen met reden, en code-now plus verify-now, otp-now, auth-code-now en codes-now geven die actuele codecheck nu ook direct zonder losse flags. Summary blijft voor alleen nieuwe mail sinds state.',
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
