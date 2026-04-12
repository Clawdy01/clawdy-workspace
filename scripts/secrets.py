#!/usr/bin/env python3
import json
from pathlib import Path

ROOT = Path('/home/clawdy/.openclaw/workspace')
STATE = ROOT / 'state'
SECRETS = STATE / 'secrets.json'
MAIL_CONFIG = STATE / 'mail-config.json'


def load_secrets():
    try:
        return json.loads(SECRETS.read_text())
    except Exception:
        return {}


def load_mail_config():
    config = json.loads(MAIL_CONFIG.read_text())
    secrets = load_secrets()
    if 'mail_password' in secrets:
        config['password'] = secrets['mail_password']
    return config


def get_secret(name, default=None):
    return load_secrets().get(name, default)
