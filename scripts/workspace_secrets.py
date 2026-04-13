#!/usr/bin/env python3
import json
from pathlib import Path

ROOT = Path('/home/clawdy/.openclaw/workspace')
STATE = ROOT / 'state'
SECRETS = STATE / 'secrets.json'
MAIL_CONFIG = STATE / 'mail-config.json'

SECRET_ALIASES = {
    'mail.password': ('mail.password', 'mail_password'),
    'proton.password': ('proton.password', 'proton_pass_password'),
    'github.password': ('github.password', 'github_account_password'),
}


def _expanded_secret_names(name):
    names = []
    seen = set()
    for candidate in (name, *SECRET_ALIASES.get(name, ())):
        if candidate and candidate not in seen:
            names.append(candidate)
            seen.add(candidate)
    for canonical, aliases in SECRET_ALIASES.items():
        if name == canonical or name in aliases:
            for candidate in (canonical, *aliases):
                if candidate and candidate not in seen:
                    names.append(candidate)
                    seen.add(candidate)
    return names


def load_secrets():
    try:
        return json.loads(SECRETS.read_text())
    except Exception:
        return {}


def load_mail_config():
    config = json.loads(MAIL_CONFIG.read_text())
    password = get_secret('mail.password')
    if password is not None:
        config['password'] = password
    return config


def get_secret(name, default=None):
    secrets = load_secrets()
    for candidate in _expanded_secret_names(name):
        if candidate in secrets:
            return secrets[candidate]
    return default
