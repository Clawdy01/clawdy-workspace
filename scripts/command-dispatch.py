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
    'mail-board-now': {
        'cmd': ['python3', str(ROOT / 'scripts' / 'mail-dispatch.py'), 'board-now'],
        'description': 'Compact mailboard met alleen actuele aandacht zonder losse --current-only vlag',
    },
    'mail-board-review': {
        'cmd': ['python3', str(ROOT / 'scripts' / 'mail-dispatch.py'), 'board-review'],
        'description': 'Compact mailboard met alleen reviewwaardige mail zonder losse --review-worthy vlag',
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
    'mail-latest-now': {
        'cmd': ['python3', str(ROOT / 'scripts' / 'mail-dispatch.py'), 'latest-now'],
        'description': 'Bekijk direct alleen actuele recente mail of threads zonder losse --current-only vlag',
    },
    'mail-latest-review': {
        'cmd': ['python3', str(ROOT / 'scripts' / 'mail-dispatch.py'), 'latest-review'],
        'description': 'Bekijk direct alleen reviewwaardige recente mail of threads zonder losse --review-worthy vlag',
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
        'description': 'Toon alleen recente mail die nu echt aandacht vraagt, optioneel met suppressed-uitleg via --explain-empty',
    },
    'mail-triage-now': {
        'cmd': ['python3', str(ROOT / 'scripts' / 'mail-dispatch.py'), 'triage-now'],
        'description': 'Prioriteer direct alleen actuele mail met aandachtssignaal, zonder stale fallback',
    },
    'mail-triage-review': {
        'cmd': ['python3', str(ROOT / 'scripts' / 'mail-dispatch.py'), 'triage-review'],
        'description': 'Prioriteer direct alleen reviewwaardige mail zonder code-only of ruisfallback',
    },
    'mail-now-empty': {
        'cmd': ['python3', str(ROOT / 'scripts' / 'mail-dispatch.py'), 'now', '--explain-empty'],
        'description': 'Toon wat nu echt aandacht vraagt, en leg een lege actuele mailbox meteen uit via suppressed-uitleg',
    },
    'mail-focus': {
        'cmd': ['python3', str(ROOT / 'scripts' / 'mail-dispatch.py'), 'focus'],
        'description': 'Kies de ene beste mail om nu als eerste op te pakken, ook met --current-only of --review-worthy en optioneel conceptantwoord',
    },
    'mail-focus-now': {
        'cmd': ['python3', str(ROOT / 'scripts' / 'mail-dispatch.py'), 'focus-now'],
        'description': 'Kies direct de beste actuele mail-focus zonder stale fallback',
    },
    'mail-focus-review': {
        'cmd': ['python3', str(ROOT / 'scripts' / 'mail-dispatch.py'), 'focus-review'],
        'description': 'Kies direct de beste reviewwaardige mail-focus zonder code-only of ruisfallback',
    },
    'mail-first': {
        'cmd': ['python3', str(ROOT / 'scripts' / 'mail-dispatch.py'), 'focus'],
        'description': 'Snelle route naar de ene beste eerstvolgende mail',
    },
    'mail-next-step': {
        'cmd': ['python3', str(ROOT / 'scripts' / 'mail-dispatch.py'), 'next-step'],
        'description': 'Bepaal de volgende nuttige mailstap, ook met --current-only of --review-worthy als stale fallback juist niet gewenst is',
    },
    'mail-next-now': {
        'cmd': ['python3', str(ROOT / 'scripts' / 'mail-dispatch.py'), 'next-step-now'],
        'description': 'Bepaal direct alleen de volgende actuele mailstap zonder losse --current-only vlag',
    },
    'mail-next-review': {
        'cmd': ['python3', str(ROOT / 'scripts' / 'mail-dispatch.py'), 'next-step-review'],
        'description': 'Bepaal direct alleen de volgende reviewwaardige mailstap zonder losse --review-worthy vlag, ook via /mail-next-step-review',
    },
    'mail-queue': {
        'cmd': ['python3', str(ROOT / 'scripts' / 'mail-dispatch.py'), 'queue'],
        'description': 'Toon een korte prioriteitslijst van de beste volgende mailacties',
    },
    'mail-queue-now': {
        'cmd': ['python3', str(ROOT / 'scripts' / 'mail-dispatch.py'), 'queue-now'],
        'description': 'Toon direct alleen een actuele mailwerkrij zonder losse --current-only vlag',
    },
    'mail-queue-review': {
        'cmd': ['python3', str(ROOT / 'scripts' / 'mail-dispatch.py'), 'queue-review'],
        'description': 'Toon direct alleen reviewwaardige mailvervolgstappen zonder losse --review-worthy vlag',
    },
    'mail-security-alerts': {
        'cmd': ['python3', str(ROOT / 'scripts' / 'mail-dispatch.py'), 'security-alerts'],
        'description': 'Toon compacte account- en login-alerts met current-only en suppressed-uitleg',
    },
    'mail-alerts-now': {
        'cmd': ['python3', str(ROOT / 'scripts' / 'mail-dispatch.py'), 'security-alerts-now'],
        'description': 'Toon alleen actuele security- of loginmeldingen en leg een lege check meteen uit',
    },
    'mail-review-next': {
        'cmd': ['python3', str(ROOT / 'scripts' / 'mail-dispatch.py'), 'review-next'],
        'description': 'Open direct de aanbevolen volgende mailthread met context, alternatieven, optioneel conceptantwoord en noop-uitleg via --explain-empty',
    },
    'mail-review-next-now': {
        'cmd': ['python3', str(ROOT / 'scripts' / 'mail-dispatch.py'), 'review-next-now'],
        'description': 'Open direct alleen de aanbevolen actuele mailthread zonder losse --current-only vlag',
    },
    'mail-review-next-review': {
        'cmd': ['python3', str(ROOT / 'scripts' / 'mail-dispatch.py'), 'review-next-review'],
        'description': 'Open direct alleen de aanbevolen reviewwaardige mailthread zonder losse --review-worthy vlag',
    },
    'mail-thread': {
        'cmd': ['python3', str(ROOT / 'scripts' / 'mail-dispatch.py'), 'thread'],
        'description': 'Klap één recente mailthread compact uit, met filters op afzender/onderwerp/actie en optioneel conceptantwoord',
    },
    'mail-thread-now': {
        'cmd': ['python3', str(ROOT / 'scripts' / 'mail-dispatch.py'), 'thread-now'],
        'description': 'Open direct alleen een actuele mailthread, met suppressed-uitleg via --explain-empty',
    },
    'mail-thread-review': {
        'cmd': ['python3', str(ROOT / 'scripts' / 'mail-dispatch.py'), 'thread-review'],
        'description': 'Open direct alleen een reviewwaardige mailthread, met noop-uitleg via --explain-empty',
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
        'description': 'Zoek verificatiecodes in recente mail, ook via /mail-code, /mail-verify, /mail-otp en /mail-auth-code, met --current-only of suppressed-uitleg via --explain-empty',
    },
    'mail-code-now': {
        'cmd': ['python3', str(ROOT / 'scripts' / 'mail-dispatch.py'), 'codes-now'],
        'description': 'Toon alleen actuele verificatiecodes en leg een lege mailboxcheck meteen uit, ook via verify-now, otp-now en auth-code-now',
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
    '/mail-board-now': 'mail-board-now',
    '/mail-now-board': 'mail-board-now',
    '/mail-overview-now': 'mail-board-now',
    '/mail-overview-current': 'mail-board-now',
    '/mail-board-current': 'mail-board-now',
    '/mail-board-review': 'mail-board-review',
    '/mail-review-board': 'mail-board-review',
    '/mail-overview-review': 'mail-board-review',
    '/mail-overview-review-worthy': 'mail-board-review',
    '/mail-board-review-worthy': 'mail-board-review',
    '/mail-inbox': 'mail-inbox',
    '/mail-unread': 'mail-unread',
    '/mail-latest': 'mail-latest',
    '/mail-latest-now': 'mail-latest-now',
    '/mail-now-latest': 'mail-latest-now',
    '/mail-latest-current': 'mail-latest-now',
    '/mail-latest-review': 'mail-latest-review',
    '/mail-review-latest': 'mail-latest-review',
    '/mail-latest-review-worthy': 'mail-latest-review',
    '/mail-check': 'mail-check',
    '/mail-new': 'mail-check',
    '/mail-summary': 'mail-summary',
    '/mail-drafts': 'mail-drafts',
    '/mail-triage': 'mail-triage',
    '/mail-prioritize': 'mail-triage',
    '/mail-now': 'mail-now',
    '/mail-current': 'mail-now',
    '/mail-urgent': 'mail-now',
    '/mail-triage-now': 'mail-triage-now',
    '/mail-now-triage': 'mail-triage-now',
    '/mail-triage-current': 'mail-triage-now',
    '/mail-triage-review': 'mail-triage-review',
    '/mail-review-triage': 'mail-triage-review',
    '/mail-triage-review-worthy': 'mail-triage-review',
    '/mail-now-empty': 'mail-now-empty',
    '/mail-current-empty': 'mail-now-empty',
    '/mail-focus': 'mail-focus',
    '/mail-focus-now': 'mail-focus-now',
    '/mail-now-focus': 'mail-focus-now',
    '/mail-focus-current': 'mail-focus-now',
    '/mail-focus-review': 'mail-focus-review',
    '/mail-review-focus': 'mail-focus-review',
    '/mail-focus-review-worthy': 'mail-focus-review',
    '/mail-first': 'mail-first',
    '/mail-next-step': 'mail-next-step',
    '/mail-next': 'mail-next-step',
    '/mail-followup': 'mail-next-step',
    '/mail-next-now': 'mail-next-now',
    '/mail-now-next': 'mail-next-now',
    '/mail-next-current': 'mail-next-now',
    '/mail-next-step-now': 'mail-next-now',
    '/mail-next-step-current': 'mail-next-now',
    '/mail-next-review': 'mail-next-review',
    '/mail-review-next-step': 'mail-next-review',
    '/mail-next-step-review': 'mail-next-review',
    '/mail-next-review-worthy': 'mail-next-review',
    '/mail-next-step-review-worthy': 'mail-next-review',
    '/mail-queue': 'mail-queue',
    '/mail-worklist': 'mail-queue',
    '/mail-todo': 'mail-queue',
    '/mail-queue-now': 'mail-queue-now',
    '/mail-now-queue': 'mail-queue-now',
    '/mail-worklist-now': 'mail-queue-now',
    '/mail-worklist-current': 'mail-queue-now',
    '/mail-todo-now': 'mail-queue-now',
    '/mail-todo-current': 'mail-queue-now',
    '/mail-queue-current': 'mail-queue-now',
    '/mail-queue-review': 'mail-queue-review',
    '/mail-review-queue': 'mail-queue-review',
    '/mail-worklist-review': 'mail-queue-review',
    '/mail-worklist-review-worthy': 'mail-queue-review',
    '/mail-todo-review': 'mail-queue-review',
    '/mail-todo-review-worthy': 'mail-queue-review',
    '/mail-queue-review-worthy': 'mail-queue-review',
    '/mail-security-alerts': 'mail-security-alerts',
    '/mail-security': 'mail-security-alerts',
    '/mail-alerts': 'mail-security-alerts',
    '/mail-alerts-now': 'mail-alerts-now',
    '/mail-alerts-current': 'mail-alerts-now',
    '/mail-security-now': 'mail-alerts-now',
    '/mail-security-current': 'mail-alerts-now',
    '/mail-security-alerts-now': 'mail-alerts-now',
    '/mail-security-alerts-current': 'mail-alerts-now',
    '/mail-review-next': 'mail-review-next',
    '/mail-review': 'mail-review-next',
    '/mail-open': 'mail-review-next',
    '/mail-next-thread': 'mail-review-next',
    '/mail-review-next-now': 'mail-review-next-now',
    '/mail-now-open': 'mail-review-next-now',
    '/mail-open-now': 'mail-review-next-now',
    '/mail-review-next-current': 'mail-review-next-now',
    '/mail-open-current': 'mail-review-next-now',
    '/mail-review-next-review': 'mail-review-next-review',
    '/mail-review-open': 'mail-review-next-review',
    '/mail-open-review': 'mail-review-next-review',
    '/mail-review-next-review-worthy': 'mail-review-next-review',
    '/mail-open-review-worthy': 'mail-review-next-review',
    '/mail-thread': 'mail-thread',
    '/mail-threads': 'mail-thread',
    '/mail-conversation': 'mail-thread',
    '/mail-thread-now': 'mail-thread-now',
    '/mail-now-thread': 'mail-thread-now',
    '/mail-thread-current': 'mail-thread-now',
    '/mail-thread-review': 'mail-thread-review',
    '/mail-review-thread': 'mail-thread-review',
    '/mail-thread-review-worthy': 'mail-thread-review',
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
    '/mail-code-now': 'mail-code-now',
    '/mail-code-current': 'mail-code-now',
    '/mail-verify-now': 'mail-code-now',
    '/mail-verify-current': 'mail-code-now',
    '/mail-otp-now': 'mail-code-now',
    '/mail-otp-current': 'mail-code-now',
    '/mail-auth-code-now': 'mail-code-now',
    '/mail-auth-code-current': 'mail-code-now',
    '/mail-codes-now': 'mail-code-now',
    '/mail-codes-current': 'mail-code-now',
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


def aliases_for_command(command_name):
    canonical_slash = f'/{command_name}'
    return sorted(
        alias
        for alias, target in ALIASES.items()
        if alias.startswith('/') and target == command_name and alias != canonical_slash
    )


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
            'slash': '/mail-board-now',
            'also': ['/mail-now-board', '/mail-overview-now', '/mail-overview-current', '/mail-board-current'],
            'description': 'compact board met alleen actuele aandacht en ingebouwde suppressed-uitleg',
        },
        {
            'slash': '/mail-board-review',
            'also': ['/mail-review-board', '/mail-overview-review', '/mail-overview-review-worthy', '/mail-board-review-worthy'],
            'description': 'compact board met alleen reviewwaardige mail en ingebouwde noop-uitleg',
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
            'slash': '/mail-latest-now',
            'also': ['/mail-now-latest', '/mail-latest-current'],
            'description': 'actuele recente mail of threads zonder losse --current-only vlag',
        },
        {
            'slash': '/mail-latest-review',
            'also': ['/mail-review-latest', '/mail-latest-review-worthy'],
            'description': 'reviewwaardige recente mail of threads zonder losse --review-worthy vlag',
        },
        {
            'slash': '/mail-now',
            'also': ['/mail-current'],
            'description': 'alleen wat nu echt aandacht vraagt, ook via /mail-current, met --explain-empty voor suppressed-uitleg',
        },
        {
            'slash': '/mail-triage-now',
            'also': ['/mail-now-triage', '/mail-triage-current'],
            'description': 'actuele mail prioriteren zonder losse --current-only vlag',
        },
        {
            'slash': '/mail-triage-review',
            'also': ['/mail-review-triage', '/mail-triage-review-worthy'],
            'description': 'reviewwaardige mail prioriteren zonder losse --review-worthy vlag',
        },
        {
            'slash': '/mail-now-empty',
            'also': ['/mail-current-empty'],
            'description': 'actuele mailcheck met suppressed-uitleg al ingebouwd',
        },
        {
            'slash': '/mail-alerts-now',
            'also': ['/mail-alerts-current', '/mail-security-now', '/mail-security-current', '/mail-security-alerts-now', '/mail-security-alerts-current'],
            'description': 'actuele security- of loginmeldingen, met current-only en noop-uitleg al ingebouwd',
        },
        {
            'slash': '/mail-code',
            'also': ['/mail-codes', '/mail-verify', '/mail-otp', '/mail-auth-code'],
            'description': 'recente verificatiecodes compact bekijken via de korte code-, verify-, otp- en auth-code-ingangen',
        },
        {
            'slash': '/mail-code-now',
            'also': ['/mail-code-current', '/mail-verify-now', '/mail-verify-current', '/mail-otp-now', '/mail-otp-current', '/mail-auth-code-now', '/mail-auth-code-current', '/mail-codes-now', '/mail-codes-current'],
            'description': 'actuele verificatiecode-check met current-only en noop-uitleg al ingebouwd',
        },
        {
            'slash': '/mail-focus-now',
            'also': ['/mail-now-focus', '/mail-focus-current'],
            'description': 'beste actuele mail-focus zonder stale fallback, ook via /mail-focus-current',
        },
        {
            'slash': '/mail-focus-review',
            'also': ['/mail-review-focus', '/mail-focus-review-worthy'],
            'description': 'beste reviewwaardige mail-focus zonder code-only of ruisfallback, ook via /mail-focus-review-worthy',
        },
        {
            'slash': '/mail-next-now',
            'also': ['/mail-now-next', '/mail-next-current', '/mail-next-step-now', '/mail-next-step-current'],
            'description': 'beste actuele mailvervolgstap zonder losse --current-only vlag',
        },
        {
            'slash': '/mail-next-review',
            'also': ['/mail-review-next-step', '/mail-next-step-review', '/mail-next-review-worthy', '/mail-next-step-review-worthy'],
            'description': 'beste reviewwaardige mailvervolgstap zonder losse --review-worthy vlag',
        },
        {
            'slash': '/mail-queue-now',
            'also': ['/mail-now-queue', '/mail-queue-current', '/mail-worklist-now', '/mail-worklist-current', '/mail-todo-now', '/mail-todo-current'],
            'description': 'korte actuele mailwerkrij zonder losse --current-only vlag, ook via worklist/todo',
        },
        {
            'slash': '/mail-queue-review',
            'also': ['/mail-review-queue', '/mail-queue-review-worthy', '/mail-worklist-review', '/mail-worklist-review-worthy', '/mail-todo-review', '/mail-todo-review-worthy'],
            'description': 'korte reviewwaardige mailwerkrij zonder losse --review-worthy vlag, ook via worklist/todo',
        },
        {
            'slash': '/mail-thread-now',
            'also': ['/mail-now-thread', '/mail-thread-current'],
            'description': 'open direct alleen een actuele thread zonder losse --current-only vlag',
        },
        {
            'slash': '/mail-thread-review',
            'also': ['/mail-review-thread', '/mail-thread-review-worthy'],
            'description': 'open direct alleen een reviewwaardige thread zonder losse --review-worthy vlag',
        },
        {
            'slash': '/mail-first',
            'description': 'beste eerstvolgende mail',
        },
        {
            'slash': '/mail-open-now',
            'also': ['/mail-review-next-now', '/mail-now-open', '/mail-review-next-current', '/mail-open-current'],
            'description': 'aanbevolen actuele thread meteen openklappen zonder losse --current-only vlag',
        },
        {
            'slash': '/mail-open-review',
            'also': ['/mail-review-next-review', '/mail-review-open', '/mail-review-next-review-worthy', '/mail-open-review-worthy'],
            'description': 'aanbevolen reviewwaardige thread meteen openklappen zonder losse --review-worthy vlag',
        },
        {
            'slash': '/mail-open',
            'also': ['/mail-review-next'],
            'description': 'aanbevolen thread meteen openklappen, met --explain-empty als noop-uitleg',
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
                'also': aliases_for_command(name),
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
        '- slash-vorm werkt ook, bijvoorbeeld /status, /mail, /mail-latest-now of /mail-now',
        '- snelle mailstart:',
    ]
    for item in payload.get('quickstart', []):
        label = item['slash']
        if item.get('also'):
            label = f"{label} of {' of '.join(item['also'])}"
        lines.append(f"  - {label}: {item['description']}")
    lines.append('- beschikbaar:')
    for item in payload['commands']:
        label = item['slash']
        if item.get('also'):
            label = f"{label} of {' of '.join(item['also'])}"
        lines.append(f"  - {label}: {item['description']}")
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
