#!/usr/bin/env python3
import imaplib
import time

from workspace_secrets import load_mail_config


def open_inbox(readonly=True, retries=3, initial_delay=0.75):
    conf = load_mail_config()
    last_error = None

    for attempt in range(1, max(1, retries) + 1):
        mailbox = None
        try:
            mailbox = imaplib.IMAP4_SSL(conf['host'], conf.get('imapPort', 993))
            mailbox.login(conf['username'], conf['password'])
            status, _ = mailbox.select('INBOX', readonly=readonly)
            if status != 'OK':
                raise RuntimeError('select failed')
            return mailbox
        except (imaplib.IMAP4.error, imaplib.IMAP4.abort, OSError, RuntimeError) as exc:
            last_error = exc
            if mailbox is not None:
                try:
                    mailbox.logout()
                except Exception:
                    pass
            if attempt < retries:
                time.sleep(initial_delay * attempt)

    raise SystemExit(f'ERROR: mail connect/login/select failed after {retries} attempts: {last_error}')
