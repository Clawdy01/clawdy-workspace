#!/usr/bin/env python3
import argparse
import json
import subprocess
from datetime import datetime, timedelta, UTC
from pathlib import Path
from xml.sax.saxutils import escape
from xml.etree import ElementTree as ET

from workspace_secrets import load_mail_config

ROOT = Path('/home/clawdy/.openclaw/workspace')
NS = {
    's': 'http://schemas.xmlsoap.org/soap/envelope/',
    'm': 'http://schemas.microsoft.com/exchange/services/2006/messages',
    't': 'http://schemas.microsoft.com/exchange/services/2006/types',
}


def ews_request(xml_body: str, timeout: int = 30) -> str:
    conf = load_mail_config()
    host = conf['host']
    username = conf['username']
    password = conf['password']
    cmd = [
        'curl', '-sS', '-k', '--ntlm', '-u', f'{username}:{password}',
        '--connect-timeout', '15', '--max-time', str(timeout),
        '-H', 'Content-Type: text/xml; charset=utf-8',
        '--data-binary', xml_body,
        f'https://{host}/EWS/Exchange.asmx',
    ]
    proc = subprocess.run(cmd, capture_output=True, text=True, check=False)
    if proc.returncode != 0:
        raise RuntimeError(proc.stderr.strip() or proc.stdout.strip() or 'curl failed')
    return proc.stdout


def soap_envelope(body: str) -> str:
    return f'''<?xml version="1.0" encoding="utf-8"?>
<soap:Envelope xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
 xmlns:m="http://schemas.microsoft.com/exchange/services/2006/messages"
 xmlns:t="http://schemas.microsoft.com/exchange/services/2006/types"
 xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/">
  <soap:Header>
    <t:RequestServerVersion Version="Exchange2016" />
  </soap:Header>
  <soap:Body>
    {body}
  </soap:Body>
</soap:Envelope>'''


def text(node, xpath: str):
    found = node.find(xpath, NS)
    return found.text if found is not None else None


def find_inbox(limit: int = 10, unread_only: bool = False, query: str | None = None):
    restriction = ''
    if unread_only:
        restriction = '''
  <m:Restriction>
    <t:IsEqualTo>
      <t:FieldURI FieldURI="message:IsRead" />
      <t:FieldURIOrConstant>
        <t:Constant Value="false" />
      </t:FieldURIOrConstant>
    </t:IsEqualTo>
  </m:Restriction>'''
    body = f'''
<m:FindItem Traversal="Shallow">
  <m:ItemShape>
    <t:BaseShape>AllProperties</t:BaseShape>
  </m:ItemShape>
  {restriction}
  <m:IndexedPageItemView MaxEntriesReturned="{limit}" Offset="0" BasePoint="Beginning" />
  <m:ParentFolderIds>
    <t:DistinguishedFolderId Id="inbox" />
  </m:ParentFolderIds>
</m:FindItem>'''
    xml = ews_request(soap_envelope(body))
    root = ET.fromstring(xml)
    messages = []
    for msg in root.findall('.//t:Message', NS):
        sender_name = text(msg, 't:From/t:Mailbox/t:Name')
        sender_email = text(msg, 't:From/t:Mailbox/t:EmailAddress')
        messages.append({
            'subject': text(msg, 't:Subject'),
            'received': text(msg, 't:DateTimeReceived'),
            'is_read': text(msg, 't:IsRead') == 'true',
            'from_name': sender_name,
            'from_email': sender_email,
            'preview': text(msg, 't:Preview'),
            'item_id': (msg.find('t:ItemId', NS).attrib.get('Id') if msg.find('t:ItemId', NS) is not None else None),
        })
    if query:
        q = query.strip().lower()
        messages = [
            item for item in messages
            if q in str(item.get('subject') or '').lower()
            or q in str(item.get('from_name') or '').lower()
            or q in str(item.get('from_email') or '').lower()
            or q in str(item.get('preview') or '').lower()
        ]
    return messages


def find_calendar(hours: int = 48):
    start = datetime.now(UTC)
    end = start + timedelta(hours=hours)
    body = f'''
<m:FindItem Traversal="Shallow">
  <m:ItemShape>
    <t:BaseShape>AllProperties</t:BaseShape>
  </m:ItemShape>
  <m:CalendarView StartDate="{start.isoformat().replace('+00:00', 'Z')}" EndDate="{end.isoformat().replace('+00:00', 'Z')}" MaxEntriesReturned="20" />
  <m:ParentFolderIds>
    <t:DistinguishedFolderId Id="calendar" />
  </m:ParentFolderIds>
</m:FindItem>'''
    xml = ews_request(soap_envelope(body))
    root = ET.fromstring(xml)
    events = []
    for item in root.findall('.//t:CalendarItem', NS):
        organizer = text(item, 't:Organizer/t:Mailbox/t:Name') or text(item, 't:Organizer/t:Mailbox/t:EmailAddress')
        events.append({
            'subject': text(item, 't:Subject'),
            'start': text(item, 't:Start'),
            'end': text(item, 't:End'),
            'location': text(item, 't:Location'),
            'organizer': organizer,
            'is_all_day': text(item, 't:IsAllDayEvent') == 'true',
            'item_id': (item.find('t:ItemId', NS).attrib.get('Id') if item.find('t:ItemId', NS) is not None else None),
        })
    return events


def find_tasks(limit: int = 20):
    body = f'''
<m:FindItem Traversal="Shallow">
  <m:ItemShape>
    <t:BaseShape>IdOnly</t:BaseShape>
  </m:ItemShape>
  <m:IndexedPageItemView MaxEntriesReturned="{limit}" Offset="0" BasePoint="Beginning" />
  <m:ParentFolderIds>
    <t:DistinguishedFolderId Id="tasks" />
  </m:ParentFolderIds>
</m:FindItem>'''
    xml = ews_request(soap_envelope(body))
    root = ET.fromstring(xml)
    ids = []
    for item in root.findall('.//t:Task/t:ItemId', NS):
        item_id = item.attrib.get('Id')
        change_key = item.attrib.get('ChangeKey')
        if item_id:
            ids.append((item_id, change_key))
    if not ids:
        return []
    get_items = ''.join(
        f'<t:ItemId Id="{escape(item_id)}"' + (f' ChangeKey="{escape(change_key)}"' if change_key else '') + ' />'
        for item_id, change_key in ids
    )
    get_body = f'''
<m:GetItem>
  <m:ItemShape>
    <t:BaseShape>AllProperties</t:BaseShape>
  </m:ItemShape>
  <m:ItemIds>
    {get_items}
  </m:ItemIds>
</m:GetItem>'''
    xml = ews_request(soap_envelope(get_body))
    root = ET.fromstring(xml)
    tasks = []
    for item in root.findall('.//t:Task', NS):
        tasks.append({
            'subject': text(item, 't:Subject'),
            'status': text(item, 't:Status'),
            'due_date': text(item, 't:DueDate'),
            'start_date': text(item, 't:StartDate'),
            'importance': text(item, 't:Importance'),
            'percent_complete': text(item, 't:PercentComplete'),
            'body': text(item, 't:Body'),
            'item_id': (item.find('t:ItemId', NS).attrib.get('Id') if item.find('t:ItemId', NS) is not None else None),
        })
    return tasks


def create_task(subject: str, body_text: str | None = None, due_days: int | None = None):
    subject_xml = escape(subject)
    body_xml = f'<t:Body BodyType="Text">{escape(body_text)}</t:Body>' if body_text else ''
    due_xml = ''
    if due_days is not None:
        due = datetime.now(UTC) + timedelta(days=due_days)
        due_xml = f'<t:DueDate>{due.isoformat().replace("+00:00", "Z")}</t:DueDate>'
    body = f'''
<m:CreateItem MessageDisposition="SaveOnly">
  <m:SavedItemFolderId>
    <t:DistinguishedFolderId Id="tasks" />
  </m:SavedItemFolderId>
  <m:Items>
    <t:Task>
      <t:Subject>{subject_xml}</t:Subject>
      {body_xml}
      {due_xml}
    </t:Task>
  </m:Items>
</m:CreateItem>'''
    xml = ews_request(soap_envelope(body))
    root = ET.fromstring(xml)
    msg = root.find('.//m:CreateItemResponseMessage', NS)
    if msg is None or msg.attrib.get('ResponseClass') != 'Success':
        raise RuntimeError('task create failed')
    item = root.find('.//t:Task', NS)
    return {
        'subject': text(item, 't:Subject') if item is not None else subject,
        'item_id': (item.find('t:ItemId', NS).attrib.get('Id') if item is not None and item.find('t:ItemId', NS) is not None else None),
    }


def ensure_tasks(items):
    existing = find_tasks(limit=200)
    existing_subjects = {str(item.get('subject') or '').strip() for item in existing}
    created = []
    skipped = []
    for item in items:
        subject = item['subject'].strip()
        if subject in existing_subjects:
            skipped.append(subject)
            continue
        created_item = create_task(subject, item.get('body'), item.get('due_days'))
        created.append(created_item)
        existing_subjects.add(subject)
    return {'created': created, 'skipped': skipped}


def render_text(payload):
    lines = []
    if 'inbox' in payload:
        lines.append(f"Inbox ({len(payload['inbox'])})")
        for item in payload['inbox']:
            sender = item.get('from_name') or item.get('from_email') or 'onbekend'
            unread = 'unread' if not item.get('is_read') else 'read'
            lines.append(f"- {sender} — {item.get('subject') or '(geen onderwerp)'} [{unread}] {item.get('received') or ''}".strip())
    if 'calendar' in payload:
        lines.append(f"Agenda ({len(payload['calendar'])})")
        for item in payload['calendar']:
            where = f" @ {item['location']}" if item.get('location') else ''
            lines.append(f"- {item.get('start') or '?'} {item.get('subject') or '(geen onderwerp)'}{where}")
    if 'tasks' in payload:
        lines.append(f"Taken ({len(payload['tasks'])})")
        for item in payload['tasks']:
            due = f" due {item['due_date']}" if item.get('due_date') else ''
            lines.append(f"- {item.get('subject') or '(geen onderwerp)'} [{item.get('status') or 'unknown'}]{due}")
    if 'ensure_tasks' in payload:
        summary = payload['ensure_tasks']
        lines.append(f"Taken bijgewerkt: {len(summary.get('created', []))} nieuw, {len(summary.get('skipped', []))} bestond al")
    return '\n'.join(lines)


def main():
    parser = argparse.ArgumentParser(description='Praktische Exchange SE EWS mailbox/agenda/taken helper')
    parser.add_argument('--json', action='store_true')
    parser.add_argument('--inbox', action='store_true')
    parser.add_argument('--calendar', action='store_true')
    parser.add_argument('--tasks', action='store_true')
    parser.add_argument('--seed-current-tasks', action='store_true')
    parser.add_argument('--unread-only', action='store_true')
    parser.add_argument('--search', help='filter inbox results op onderwerp/afzender/preview')
    parser.add_argument('--limit', type=int, default=10)
    parser.add_argument('--hours', type=int, default=48)
    args = parser.parse_args()

    if not args.inbox and not args.calendar and not args.tasks and not args.seed_current_tasks:
        args.inbox = True
        args.calendar = True

    result = {}
    if args.inbox:
        result['inbox'] = find_inbox(
            limit=max(1, min(args.limit, 50)),
            unread_only=args.unread_only,
            query=args.search,
        )
    if args.calendar:
        result['calendar'] = find_calendar(hours=max(1, min(args.hours, 24 * 14)))
    if args.tasks:
        result['tasks'] = find_tasks(limit=max(1, min(args.limit, 200)))
    if args.seed_current_tasks:
        result['ensure_tasks'] = ensure_tasks([
            {
                'subject': 'GitHub: private account + repo + eerste push afronden',
                'body': 'Primair spoor. Definition of done: account bestaat, login werkt, private repo bestaat, eerste push bevestigd.',
                'due_days': 1,
            },
            {
                'subject': 'Exchange SE: mailbox/agenda helper verder uitbouwen',
                'body': 'Parallel spoor na GitHub. Focus op bruikbare mailbox- en agenda-acties via EWS/Autodiscover.',
                'due_days': 2,
            },
            {
                'subject': 'Image workflows: herstarten zodra echte modelroute beschikbaar is',
                'body': 'Geparkeerd tot betere model/hardware-route. Niet actief oppakken tot de blocker verdwijnt.',
                'due_days': 14,
            },
        ])

    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(render_text(result))


if __name__ == '__main__':
    main()
