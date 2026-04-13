#!/usr/bin/env python3
import json
import os
from pathlib import Path

ROOT = Path('/home/clawdy/.openclaw/workspace')
STATE = ROOT / 'state'
SECRETS = STATE / 'secrets.json'
MAIL_CONFIG = STATE / 'mail-config.json'

SECRET_ALIASES = {
    'mail.password': (),
    'proton.password': (),
    'github.password': (),
    'github.ssh.private_key': (),
    'github.ssh.public_key': (),
}


def _expanded_secret_names(name):
    return [name]


def load_secrets():
    try:
        return json.loads(SECRETS.read_text())
    except Exception:
        return {}


def save_secrets(secrets):
    SECRETS.write_text(json.dumps(secrets, indent=2) + '\n')


def set_secret(name, value):
    secrets = load_secrets()
    secrets[name] = value
    save_secrets(secrets)


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


def materialize_github_ssh_key(target='/home/clawdy/.ssh/id_ed25519_github_clawdy'):
    private_key = get_secret('github.ssh.private_key')
    public_key = get_secret('github.ssh.public_key')
    if not private_key:
        raise RuntimeError('missing github.ssh.private_key in secrets.json')
    target_path = Path(target)
    target_path.parent.mkdir(parents=True, exist_ok=True)
    target_path.write_text(private_key if private_key.endswith('\n') else private_key + '\n')
    os.chmod(target_path, 0o600)
    if public_key:
        pub_path = Path(str(target_path) + '.pub')
        pub_path.write_text(public_key if public_key.endswith('\n') else public_key + '\n')
        os.chmod(pub_path, 0o644)
    return str(target_path)
