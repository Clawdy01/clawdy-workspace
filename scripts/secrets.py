#!/usr/bin/env python3
"""Compat shim.

Keeps older workspace secret-loader imports working while also behaving enough like
Python's stdlib ``secrets`` module that scripts in this directory do not break when
``import secrets`` resolves here first.
"""

import base64
import binascii
import os

from workspace_secrets import get_secret, load_mail_config, load_secrets

DEFAULT_ENTROPY = 32


def _randbytes(nbytes: int | None = None) -> bytes:
    if nbytes is None:
        nbytes = DEFAULT_ENTROPY
    if nbytes < 0:
        raise ValueError('nbytes must be non-negative')
    return os.urandom(nbytes)


def token_bytes(nbytes: int | None = None) -> bytes:
    return _randbytes(nbytes)


def token_hex(nbytes: int | None = None) -> str:
    return binascii.hexlify(_randbytes(nbytes)).decode('ascii')


def token_urlsafe(nbytes: int | None = None) -> str:
    return base64.urlsafe_b64encode(_randbytes(nbytes)).rstrip(b'=').decode('ascii')
