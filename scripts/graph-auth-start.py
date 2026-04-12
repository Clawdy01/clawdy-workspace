#!/usr/bin/env python3
import argparse
import base64
import hashlib
import json
import os
import secrets
from urllib.parse import quote

DEFAULT_REDIRECT_URI = 'http://localhost'
DEFAULT_SCOPES = [
    'offline_access',
    'openid',
    'profile',
    'Calendars.Read',
    'Tasks.Read',
]


def env(name: str, default: str = '') -> str:
    return os.environ.get(name, default).strip()


def pick(value: str | None, env_name: str, default: str = '') -> str:
    if value is not None and value.strip():
        return value.strip()
    return env(env_name, default)


def b64url(data: bytes) -> str:
    return base64.urlsafe_b64encode(data).decode('ascii').rstrip('=')


def make_pkce_pair() -> tuple[str, str]:
    verifier = b64url(secrets.token_bytes(64))
    challenge = b64url(hashlib.sha256(verifier.encode('ascii')).digest())
    return verifier, challenge


def build_auth_payload(
    tenant_id_override: str | None = None,
    client_id_override: str | None = None,
    redirect_uri_override: str | None = None,
    scope_override: str | None = None,
) -> dict:
    tenant_id = pick(tenant_id_override, 'MSGRAPH_TENANT_ID')
    client_id = pick(client_id_override, 'MSGRAPH_CLIENT_ID')
    redirect_uri = pick(redirect_uri_override, 'MSGRAPH_REDIRECT_URI', DEFAULT_REDIRECT_URI) or DEFAULT_REDIRECT_URI
    scope_string = pick(scope_override, 'MSGRAPH_SCOPE') or env('MSGRAPH_SCOPES') or ' '.join(DEFAULT_SCOPES)

    missing = [name for name, value in [
        ('MSGRAPH_TENANT_ID', tenant_id),
        ('MSGRAPH_CLIENT_ID', client_id),
    ] if not value]
    if missing:
        raise SystemExit(f'Ontbrekende env vars: {", ".join(missing)}')

    state = secrets.token_urlsafe(18)
    code_verifier, code_challenge = make_pkce_pair()
    auth_url = (
        f'https://login.microsoftonline.com/{tenant_id}/oauth2/v2.0/authorize'
        f'?client_id={quote(client_id)}'
        f'&response_type=code'
        f'&redirect_uri={quote(redirect_uri, safe="")}'
        f'&response_mode=query'
        f'&scope={quote(scope_string, safe="")}'
        f'&state={quote(state)}'
        f'&code_challenge={quote(code_challenge)}'
        '&code_challenge_method=S256'
    )
    token_url = f'https://login.microsoftonline.com/{tenant_id}/oauth2/v2.0/token'

    return {
        'tenant_id': tenant_id,
        'client_id': client_id,
        'redirect_uri': redirect_uri,
        'scope': scope_string,
        'state': state,
        'code_verifier': code_verifier,
        'code_challenge': code_challenge,
        'env_exports': [
            f"export MSGRAPH_TENANT_ID='{tenant_id}'",
            f"export MSGRAPH_CLIENT_ID='{client_id}'",
            f"export MSGRAPH_REDIRECT_URI='{redirect_uri}'",
            f"export MSGRAPH_SCOPE='{scope_string}'",
            f"export MSGRAPH_CODE_VERIFIER='{code_verifier}'",
            f"export MSGRAPH_STATE='{state}'",
        ],
        'authorize_url': auth_url,
        'token_url': token_url,
        'next_commands': {
            'exchange_code_curl': (
                "curl -sS -X POST "
                f"'{token_url}' "
                "-H 'Content-Type: application/x-www-form-urlencoded' "
                f"--data-urlencode 'client_id={client_id}' "
                "--data-urlencode 'grant_type=authorization_code' "
                "--data-urlencode 'code=<paste-auth-code-here>' "
                f"--data-urlencode 'redirect_uri={redirect_uri}' "
                f"--data-urlencode 'scope={scope_string}' "
                f"--data-urlencode 'code_verifier={code_verifier}'"
            ),
            'proof_helper': (
                "python3 scripts/graph-proof.py "
                "--code 'http://localhost/?code=<paste-auth-code-here>&state=<paste-state-here>' "
                f"--code-verifier '{code_verifier}' "
                f"--expected-state '{state}' "
                f"--tenant-id '{tenant_id}' "
                f"--client-id '{client_id}' "
                f"--redirect-uri '{redirect_uri}' "
                f"--scope '{scope_string}'"
            ),
        },
    }


def render_text(payload: dict) -> str:
    lines = [
        'Exchange / Microsoft Graph auth start',
        f"- redirect: {payload['redirect_uri']}",
        f"- scope: {payload['scope']}",
        f"- state: {payload['state']}",
        f"- code_verifier: {payload['code_verifier']}",
        f"- code_challenge: {payload['code_challenge']}",
        f"- authorize url: {payload['authorize_url']}",
        f"- token url: {payload['token_url']}",
        '- env exports:',
        *[f"  - {line}" for line in payload['env_exports']],
        '- next commands:',
        f"  - token exchange curl: {payload['next_commands']['exchange_code_curl']}",
        f"  - proof helper: {payload['next_commands']['proof_helper']}",
    ]
    return '\n'.join(lines)


def main():
    parser = argparse.ArgumentParser(description='Genereer een PKCE authorize start voor de eerste Microsoft Graph delegated auth test')
    parser.add_argument('--json', action='store_true', help='geef JSON-output')
    parser.add_argument('--tenant-id', help='override MSGRAPH_TENANT_ID zonder export-stap')
    parser.add_argument('--client-id', help='override MSGRAPH_CLIENT_ID zonder export-stap')
    parser.add_argument('--redirect-uri', help='override MSGRAPH_REDIRECT_URI zonder export-stap')
    parser.add_argument('--scope', help='override MSGRAPH_SCOPE zonder export-stap')
    args = parser.parse_args()

    payload = build_auth_payload(
        tenant_id_override=args.tenant_id,
        client_id_override=args.client_id,
        redirect_uri_override=args.redirect_uri,
        scope_override=args.scope,
    )
    if args.json:
        print(json.dumps(payload, ensure_ascii=False, indent=2))
    else:
        print(render_text(payload))


if __name__ == '__main__':
    main()
