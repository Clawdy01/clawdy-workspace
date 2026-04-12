#!/usr/bin/env python3
import argparse
import json
import os
import sys
from datetime import datetime, timedelta, UTC
from urllib.error import HTTPError, URLError
from urllib.parse import parse_qs, urlencode, urlparse
from urllib.request import Request, urlopen

DEFAULT_REDIRECT_URI = 'http://localhost'
GRAPH_BASE = 'https://graph.microsoft.com/v1.0'
DEFAULT_SCOPES = 'offline_access openid profile Calendars.Read Tasks.Read'


def env(name: str, default: str = '') -> str:
    return os.environ.get(name, default).strip()


def pick(value: str | None, env_name: str, default: str = '') -> str:
    if value is not None and value.strip():
        return value.strip()
    return env(env_name, default)


def build_window(window_days: int):
    start = datetime.now(UTC).replace(microsecond=0)
    end = start + timedelta(days=window_days)
    return (
        start.isoformat().replace('+00:00', 'Z'),
        end.isoformat().replace('+00:00', 'Z'),
    )


def parse_redirect_params(value: str) -> dict[str, str | None]:
    raw = (value or '').strip()
    if not raw:
        return {'code': None, 'state': None}
    if '://' not in raw and 'code=' not in raw:
        return {'code': raw, 'state': None}
    parsed = urlparse(raw)
    params = parse_qs(parsed.query)
    code_values = params.get('code') or []
    state_values = params.get('state') or []
    return {
        'code': code_values[0].strip() if code_values and code_values[0].strip() else None,
        'state': state_values[0].strip() if state_values and state_values[0].strip() else None,
    }


def post_form(url: str, data: dict[str, str]) -> dict:
    payload = urlencode(data).encode('utf-8')
    request = Request(
        url,
        data=payload,
        headers={'Content-Type': 'application/x-www-form-urlencoded'},
        method='POST',
    )
    try:
        with urlopen(request, timeout=30) as response:
            return json.loads(response.read().decode('utf-8'))
    except HTTPError as exc:
        body = exc.read().decode('utf-8', errors='replace')
        raise SystemExit(f'Token request faalde ({exc.code}): {body}') from exc
    except URLError as exc:
        raise SystemExit(f'Token request faalde: {exc}') from exc


def get_json(url: str, access_token: str) -> dict:
    request = Request(
        url,
        headers={
            'Authorization': f'Bearer {access_token}',
            'Accept': 'application/json',
        },
        method='GET',
    )
    try:
        with urlopen(request, timeout=30) as response:
            return json.loads(response.read().decode('utf-8'))
    except HTTPError as exc:
        body = exc.read().decode('utf-8', errors='replace')
        raise SystemExit(f'Graph request faalde ({exc.code}): {body}') from exc
    except URLError as exc:
        raise SystemExit(f'Graph request faalde: {exc}') from exc


def graph_scope_value(scope_override: str | None = None) -> str:
    return (
        (scope_override or '').strip()
        or env('MSGRAPH_SCOPE')
        or env('MSGRAPH_SCOPES')
        or DEFAULT_SCOPES
    )


def exchange_code_for_token(
    code: str,
    code_verifier: str | None = None,
    tenant_id_override: str | None = None,
    client_id_override: str | None = None,
    redirect_uri_override: str | None = None,
    scope_override: str | None = None,
) -> dict:
    tenant_id = pick(tenant_id_override, 'MSGRAPH_TENANT_ID')
    client_id = pick(client_id_override, 'MSGRAPH_CLIENT_ID')
    redirect_uri = pick(redirect_uri_override, 'MSGRAPH_REDIRECT_URI', DEFAULT_REDIRECT_URI) or DEFAULT_REDIRECT_URI
    scopes = graph_scope_value(scope_override)

    missing = [name for name, value in [
        ('MSGRAPH_TENANT_ID', tenant_id),
        ('MSGRAPH_CLIENT_ID', client_id),
    ] if not value]
    if missing:
        raise SystemExit(f'Ontbrekende env vars voor token exchange: {", ".join(missing)}')

    payload = {
        'client_id': client_id,
        'grant_type': 'authorization_code',
        'code': code,
        'redirect_uri': redirect_uri,
        'scope': scopes,
    }
    verifier = (code_verifier or env('MSGRAPH_CODE_VERIFIER')).strip()
    if verifier:
        payload['code_verifier'] = verifier

    token_url = f'https://login.microsoftonline.com/{tenant_id}/oauth2/v2.0/token'
    return post_form(token_url, payload)


def pick_list_id(todo_lists: dict, preferred_list_id: str | None) -> str | None:
    if preferred_list_id:
        return preferred_list_id
    items = todo_lists.get('value') or []
    if not items:
        return None
    return (items[0].get('id') or '').strip() or None


def build_proof(access_token: str, window_days: int, todo_list_id: str | None) -> dict:
    start_iso, end_iso = build_window(window_days)
    calendar = get_json(
        f'{GRAPH_BASE}/me/calendarView?startDateTime={start_iso}&endDateTime={end_iso}',
        access_token,
    )
    todo_lists = get_json(f'{GRAPH_BASE}/me/todo/lists', access_token)
    selected_list_id = pick_list_id(todo_lists, todo_list_id)
    tasks = None
    if selected_list_id:
        tasks = get_json(f'{GRAPH_BASE}/me/todo/lists/{selected_list_id}/tasks', access_token)

    return {
        'window_days': window_days,
        'calendar': {
            'path': f'/me/calendarView?startDateTime={start_iso}&endDateTime={end_iso}',
            'count': len(calendar.get('value') or []),
            'items': calendar.get('value') or [],
        },
        'todo_lists': {
            'path': '/me/todo/lists',
            'count': len(todo_lists.get('value') or []),
            'items': todo_lists.get('value') or [],
        },
        'selected_todo_list_id': selected_list_id,
        'tasks': None if tasks is None else {
            'path': f'/me/todo/lists/{selected_list_id}/tasks',
            'count': len(tasks.get('value') or []),
            'items': tasks.get('value') or [],
        },
    }


def render_text(result: dict, token: dict | None):
    lines = ['Exchange / Microsoft Graph proof']
    if token:
        lines.append('- token exchange: gelukt')
        for field in ['token_type', 'scope', 'expires_in']:
            if token.get(field) is not None:
                lines.append(f'- {field}: {token[field]}')
        if token.get('refresh_token'):
            lines.append('- refresh_token: aanwezig')
        if token.get('access_token'):
            lines.append('- access_token: aanwezig')
    if result:
        lines.append(f"- calendarView: {result['calendar']['count']} item(s)")
        lines.append(f"- todo lists: {result['todo_lists']['count']} item(s)")
        if result['selected_todo_list_id']:
            task_count = result['tasks']['count'] if result['tasks'] else 0
            lines.append(f"- selected todo list: {result['selected_todo_list_id']} ({task_count} task(s))")
        else:
            lines.append('- selected todo list: geen lijst gevonden')
    return '\n'.join(lines)


def main():
    parser = argparse.ArgumentParser(description='Doe een eerste lokale Microsoft Graph proof-of-route voor agenda + To Do')
    parser.add_argument('--json', action='store_true', help='geef JSON-output')
    parser.add_argument('--window-days', type=int, default=7, help='aantal dagen vooruit voor calendarView (default: 7)')
    parser.add_argument('--code', help='auth code of volledige redirect URL met ?code=...')
    parser.add_argument('--access-token', help='bestaande access token, anders uit MSGRAPH_ACCESS_TOKEN')
    parser.add_argument('--todo-list-id', help='forceer een specifieke todo-lijst-id, anders eerst beschikbare lijst of MSGRAPH_TODO_LIST_ID')
    parser.add_argument('--code-verifier', help='optionele PKCE code verifier, anders uit MSGRAPH_CODE_VERIFIER')
    parser.add_argument('--expected-state', help='optionele verwachte OAuth state, anders uit MSGRAPH_STATE')
    parser.add_argument('--tenant-id', help='override MSGRAPH_TENANT_ID zonder export-stap')
    parser.add_argument('--client-id', help='override MSGRAPH_CLIENT_ID zonder export-stap')
    parser.add_argument('--redirect-uri', help='override MSGRAPH_REDIRECT_URI zonder export-stap')
    parser.add_argument('--scope', help='override MSGRAPH_SCOPE zonder export-stap')
    args = parser.parse_args()

    if args.window_days < 1:
        raise SystemExit('--window-days moet minimaal 1 zijn')

    token_payload = None
    access_token = (args.access_token or env('MSGRAPH_ACCESS_TOKEN')).strip()

    if args.code:
        redirect = parse_redirect_params(args.code)
        code = redirect['code']
        if not code:
            raise SystemExit('Kon geen auth code vinden in --code')
        expected_state = (args.expected_state or env('MSGRAPH_STATE')).strip()
        actual_state = (redirect.get('state') or '').strip()
        if expected_state and actual_state and actual_state != expected_state:
            raise SystemExit('OAuth state mismatch in redirect URL')
        token_payload = exchange_code_for_token(
            code,
            code_verifier=args.code_verifier,
            tenant_id_override=args.tenant_id,
            client_id_override=args.client_id,
            redirect_uri_override=args.redirect_uri,
            scope_override=args.scope,
        )
        access_token = (token_payload.get('access_token') or '').strip()
        if not access_token:
            raise SystemExit('Token exchange gaf geen access_token terug')

    if not access_token:
        raise SystemExit('Geef --code of --access-token mee, of zet MSGRAPH_ACCESS_TOKEN')

    proof = build_proof(
        access_token=access_token,
        window_days=args.window_days,
        todo_list_id=(args.todo_list_id or env('MSGRAPH_TODO_LIST_ID')).strip() or None,
    )

    if args.json:
        print(json.dumps({
            'token': token_payload,
            'proof': proof,
        }, ensure_ascii=False, indent=2))
        return

    print(render_text(proof, token_payload))


if __name__ == '__main__':
    main()
