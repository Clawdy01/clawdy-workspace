#!/usr/bin/env python3
import imaplib
import json
import sys

from secrets import load_mail_config


def main():
    conf = load_mail_config()
    host = conf['host']
    port = conf.get('imapPort', 993)
    username = conf['username']
    try:
        M = imaplib.IMAP4_SSL(host, port)
        M.login(username, conf['password'])
        status, _ = M.select('INBOX')
        ok = status == 'OK'
        print(json.dumps({
            'ok': ok,
            'host': host,
            'port': port,
            'username': username,
            'detail': 'login+select ok' if ok else f'select failed: {status}'
        }, ensure_ascii=False, indent=2))
        M.logout()
        sys.exit(0 if ok else 1)
    except Exception as exc:
        print(json.dumps({
            'ok': False,
            'host': host,
            'port': port,
            'username': username,
            'detail': str(exc),
        }, ensure_ascii=False, indent=2))
        sys.exit(1)


if __name__ == '__main__':
    main()
