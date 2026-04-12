#!/usr/bin/env python3
import argparse
import base64
import json
import pathlib
import subprocess
import sys

from workspace_secrets import load_mail_config

ROOT = pathlib.Path('/home/clawdy/.openclaw/workspace')

AUTODISCOVER_XML = '''<?xml version="1.0" encoding="utf-8"?>
<Autodiscover xmlns="http://schemas.microsoft.com/exchange/autodiscover/outlook/requestschema/2006">
  <Request>
    <EMailAddress>{email}</EMailAddress>
    <AcceptableResponseSchema>http://schemas.microsoft.com/exchange/autodiscover/outlook/responseschema/2006a</AcceptableResponseSchema>
  </Request>
</Autodiscover>'''

EWS_GET_INBOX = '''<?xml version="1.0" encoding="utf-8"?>
<soap:Envelope xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:m="http://schemas.microsoft.com/exchange/services/2006/messages" xmlns:t="http://schemas.microsoft.com/exchange/services/2006/types" xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/">
  <soap:Header>
    <t:RequestServerVersion Version="Exchange2016" />
  </soap:Header>
  <soap:Body>
    <m:GetFolder>
      <m:FolderShape><t:BaseShape>Default</t:BaseShape></m:FolderShape>
      <m:FolderIds><t:DistinguishedFolderId Id="inbox" /></m:FolderIds>
    </m:GetFolder>
  </soap:Body>
</soap:Envelope>'''


def curl_ntlm(url, username, password, headers=None, data=None, timeout=30):
    cmd = ['curl', '-sS', '-k', '--ntlm', '-u', f'{username}:{password}', '--connect-timeout', '15', '--max-time', str(timeout)]
    for header in headers or []:
        cmd += ['-H', header]
    if data is not None:
        cmd += ['--data-binary', data]
    cmd.append(url)
    proc = subprocess.run(cmd, capture_output=True, text=True, check=False)
    return proc.returncode, proc.stdout, proc.stderr


def between(text, start, end):
    try:
        s = text.index(start) + len(start)
        e = text.index(end, s)
        return text[s:e]
    except ValueError:
        return None


def main():
    parser = argparse.ArgumentParser(description='Snelle Exchange SE on-prem EWS/Autodiscover check')
    parser.add_argument('--json', action='store_true')
    args = parser.parse_args()

    conf = load_mail_config()
    host = conf['host']
    username = conf['username']
    password = conf['password']

    autod_url = f'https://{host}/autodiscover/autodiscover.xml'
    ews_url = f'https://{host}/EWS/Exchange.asmx'

    rc1, autod_body, autod_err = curl_ntlm(
        autod_url,
        username,
        password,
        headers=['Content-Type: text/xml'],
        data=AUTODISCOVER_XML.format(email=username),
    )
    rc2, ews_body, ews_err = curl_ntlm(
        ews_url,
        username,
        password,
        headers=['Content-Type: text/xml; charset=utf-8'],
        data=EWS_GET_INBOX,
    )

    autod_ok = rc1 == 0 and '<Autodiscover' in autod_body and '<EwsUrl>' in autod_body
    ews_ok = rc2 == 0 and 'ResponseClass="Success"' in ews_body and '<t:DisplayName>Postvak IN</t:DisplayName>' in ews_body

    result = {
        'host': host,
        'username': username,
        'autodiscover_ok': autod_ok,
        'ews_ok': ews_ok,
        'ews_url': between(autod_body, '<EwsUrl>', '</EwsUrl>'),
        'display_name': between(autod_body, '<DisplayName>', '</DisplayName>'),
        'smtp': between(autod_body, '<AutoDiscoverSMTPAddress>', '</AutoDiscoverSMTPAddress>'),
        'inbox_name': between(ews_body, '<t:DisplayName>', '</t:DisplayName>'),
        'inbox_total_count': between(ews_body, '<t:TotalCount>', '</t:TotalCount>'),
        'inbox_unread_count': between(ews_body, '<t:UnreadCount>', '</t:UnreadCount>'),
    }

    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        for k, v in result.items():
            print(f'{k}: {v}')

    if not (autod_ok and ews_ok):
        if autod_err:
            print(autod_err, file=sys.stderr)
        if ews_err:
            print(ews_err, file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()
