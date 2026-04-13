#!/usr/bin/env python3
import json
from pathlib import Path

ROOT = Path('/home/clawdy/.openclaw/workspace')
STATE = ROOT / 'state'
SECRETS = STATE / 'secrets.json'
MAIL_CONFIG = STATE / 'mail-config.json'

SECRET_ALIASES = {
    'mail.password': (),
    'proton.password': (),
    'github.password': (),
}


def _expanded_secret_names(name):
    return [name]


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
