#!/usr/bin/env python3
import argparse
import json
import os
from datetime import datetime, timedelta, UTC
from urllib.parse import quote

DEFAULT_REDIRECT_URI = 'http://localhost'
RECOMMENDED_SCOPES = [
    'Calendars.Read',
    'Tasks.Read',
]
HELPER_SCOPES = [
    'offline_access',
    'openid',
    'profile',
]


def value_or_env(value: str | None, env_name: str, default: str = '') -> str:
    if value is not None and value.strip():
        return value.strip()
    return os.environ.get(env_name, default).strip()


def build_summary(
    window_days: int,
    tenant_id_override: str | None = None,
    client_id_override: str | None = None,
    redirect_uri_override: str | None = None,
    todo_list_id_override: str | None = None,
):
    tenant_id = value_or_env(tenant_id_override, 'MSGRAPH_TENANT_ID')
    client_id = value_or_env(client_id_override, 'MSGRAPH_CLIENT_ID')
    redirect_uri = value_or_env(redirect_uri_override, 'MSGRAPH_REDIRECT_URI', DEFAULT_REDIRECT_URI) or DEFAULT_REDIRECT_URI
    todo_list_id = value_or_env(todo_list_id_override, 'MSGRAPH_TODO_LIST_ID')

    missing = []
    if not tenant_id:
        missing.append('MSGRAPH_TENANT_ID')
    if not client_id:
        missing.append('MSGRAPH_CLIENT_ID')

    start = datetime.now(UTC).replace(microsecond=0)
    end = start + timedelta(days=window_days)
    start_iso = start.isoformat().replace('+00:00', 'Z')
    end_iso = end.isoformat().replace('+00:00', 'Z')

    auth_scopes = HELPER_SCOPES + RECOMMENDED_SCOPES
    auth_scope_str = ' '.join(auth_scopes)
    auth_url = None
    token_url = None
    if tenant_id and client_id:
        auth_url = (
            f'https://login.microsoftonline.com/{tenant_id}/oauth2/v2.0/authorize'
            f'?client_id={quote(client_id)}'
            f'&response_type=code'
            f'&redirect_uri={quote(redirect_uri, safe="")}'
            f'&response_mode=query'
            f'&scope={quote(auth_scope_str, safe="")}'
        )
        token_url = f'https://login.microsoftonline.com/{tenant_id}/oauth2/v2.0/token'

    routes = [
        {
            'name': 'agenda komende dagen',
            'method': 'GET',
            'path': f'/me/calendarView?startDateTime={start_iso}&endDateTime={end_iso}',
            'why': 'direct bruikbaar tijdvenster voor wat-er-komt-aan workflow',
        },
        {
            'name': 'todo-lijsten',
            'method': 'GET',
            'path': '/me/todo/lists',
            'why': 'eerst beschikbare lijsten inventariseren',
        },
        {
            'name': 'taken uit gekozen lijst',
            'method': 'GET',
            'path': f"/me/todo/lists/{todo_list_id or '{list-id}'}/tasks",
            'why': 'proof-of-route voor concrete tasklijst',
        },
    ]

    env_exports = [
        f"export MSGRAPH_TENANT_ID='{tenant_id or '<tenant-id>'}'",
        f"export MSGRAPH_CLIENT_ID='{client_id or '<client-id>'}'",
        f"export MSGRAPH_REDIRECT_URI='{redirect_uri}'",
        f"export MSGRAPH_SCOPE='{auth_scope_str}'",
        f"export MSGRAPH_TODO_LIST_ID='{todo_list_id or '<later-kiezen-list-id>'}'",
    ]

    cli_examples = []
    if tenant_id and client_id:
        cli_examples.append({
            'name': 'auth start direct via CLI overrides',
            'command': (
                "python3 scripts/graph-auth-start.py "
                f"--tenant-id '{tenant_id}' "
                f"--client-id '{client_id}' "
                f"--redirect-uri '{redirect_uri}'"
            ),
        })
        cli_examples.append({
            'name': 'proof direct via CLI overrides',
            'command': (
                "python3 scripts/graph-proof.py "
                "--code 'http://localhost/?code=<paste-auth-code-here>&state=<paste-state-here>' "
                f"--tenant-id '{tenant_id}' "
                f"--client-id '{client_id}' "
                f"--redirect-uri '{redirect_uri}' "
                f"--scope '{auth_scope_str}' "
                "--code-verifier '<code-verifier-uit-graph-auth-start>' "
                "--expected-state '<state-uit-graph-auth-start>'"
            ),
        })

    curl_examples = []
    if token_url:
        curl_examples.append({
            'name': 'token exchange',
            'command': (
                "curl -sS -X POST "
                f"'{token_url}' "
                "-H 'Content-Type: application/x-www-form-urlencoded' "
                f"--data-urlencode 'client_id={client_id}' "
                "--data-urlencode 'grant_type=authorization_code' "
                "--data-urlencode 'code=<paste-auth-code-here>' "
                f"--data-urlencode 'redirect_uri={redirect_uri}' "
                f"--data-urlencode 'scope={auth_scope_str}'"
            ),
        })
    curl_examples.extend([
        {
            'name': 'calendar komende dagen',
            'command': (
                "curl -sS 'https://graph.microsoft.com/v1.0"
                f"/me/calendarView?startDateTime={start_iso}&endDateTime={end_iso}' "
                "-H 'Authorization: Bearer <access-token>'"
            ),
        },
        {
            'name': 'todo lijsten',
            'command': (
                "curl -sS 'https://graph.microsoft.com/v1.0/me/todo/lists' "
                "-H 'Authorization: Bearer <access-token>'"
            ),
        },
        {
            'name': 'tasks uit gekozen lijst',
            'command': (
                "curl -sS 'https://graph.microsoft.com/v1.0/me/todo/lists/"
                f"{todo_list_id or '<list-id>'}/tasks' "
                "-H 'Authorization: Bearer <access-token>'"
            ),
        },
    ])

    return {
        'ready': not missing,
        'missing_env': missing,
        'tenant_id': tenant_id or None,
        'client_id': client_id or None,
        'redirect_uri': redirect_uri,
        'recommended_scopes': RECOMMENDED_SCOPES,
        'helper_scopes': HELPER_SCOPES,
        'scope_string': auth_scope_str,
        'auth_url': auth_url,
        'token_url': token_url,
        'window_days': window_days,
        'env_exports': env_exports,
        'cli_examples': cli_examples,
        'routes': routes,
        'curl_examples': curl_examples,
        'next_steps': [
            'Maak in Azure een app registration met delegated auth.',
            f'Voeg redirect URI {redirect_uri} toe voor local/manual auth.',
            'Vraag alleen Calendars.Read en Tasks.Read aan voor de eerste route.',
            'Gebruik python3 scripts/graph-auth-start.py voor een PKCE authorize URL + code_verifier.',
            'Plak daarna de auth code terug in de token-exchange curl of in python3 scripts/graph-proof.py --code ... --code-verifier ...',
            'Test eerst /me/calendarView en /me/todo/lists, kies daarna pas een todo-lijst-id.',
            'Beslis pas na een werkende read-only proof-of-route of write-permissies nodig zijn.',
        ],
    }


def render_text(summary):
    lines = ['Exchange / Microsoft Graph setup']
    if summary['ready']:
        lines.append('- status: klaar voor eerste delegated auth test')
    else:
        missing = ', '.join(summary['missing_env'])
        lines.append(f'- status: nog niet klaar, ontbreekt {missing}')
    lines.append(f"- redirect: {summary['redirect_uri']}")
    lines.append(f"- scopes: {' '.join(summary['recommended_scopes'])}")
    lines.append(f"- helper scopes: {' '.join(summary['helper_scopes'])}")
    lines.append(f"- scope string: {summary['scope_string']}")
    if summary['auth_url']:
        lines.append(f"- authorize url: {summary['auth_url']}")
    if summary['token_url']:
        lines.append(f"- token url: {summary['token_url']}")
    lines.append('- env exports:')
    for line in summary['env_exports']:
        lines.append(f'  - {line}')
    if summary.get('cli_examples'):
        lines.append('- cli examples:')
        for example in summary['cli_examples']:
            lines.append(f"  - {example['name']}: {example['command']}")
    lines.append('- proof routes:')
    for route in summary['routes']:
        lines.append(f"  - {route['name']}: {route['method']} {route['path']} ({route['why']})")
    lines.append('- curl examples:')
    for example in summary['curl_examples']:
        lines.append(f"  - {example['name']}: {example['command']}")
    lines.append('- next steps:')
    for step in summary['next_steps']:
        lines.append(f'  - {step}')
    return '\n'.join(lines)


def main():
    parser = argparse.ArgumentParser(description='Compacte setupsamenvatting voor Exchange/Microsoft Graph proof-of-route')
    parser.add_argument('--json', action='store_true', help='geef JSON-output')
    parser.add_argument('--window-days', type=int, default=7, help='aantal dagen vooruit voor calendarView (default: 7)')
    parser.add_argument('--tenant-id', help='override MSGRAPH_TENANT_ID zonder export-stap')
    parser.add_argument('--client-id', help='override MSGRAPH_CLIENT_ID zonder export-stap')
    parser.add_argument('--redirect-uri', help='override MSGRAPH_REDIRECT_URI zonder export-stap')
    parser.add_argument('--todo-list-id', help='override MSGRAPH_TODO_LIST_ID zonder export-stap')
    args = parser.parse_args()

    if args.window_days < 1:
        raise SystemExit('--window-days moet minimaal 1 zijn')

    summary = build_summary(
        args.window_days,
        tenant_id_override=args.tenant_id,
        client_id_override=args.client_id,
        redirect_uri_override=args.redirect_uri,
        todo_list_id_override=args.todo_list_id,
    )
    if args.json:
        print(json.dumps(summary, ensure_ascii=False, indent=2))
    else:
        print(render_text(summary))


if __name__ == '__main__':
    main()
