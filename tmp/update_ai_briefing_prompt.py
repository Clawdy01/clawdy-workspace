#!/usr/bin/env python3
import json
from pathlib import Path

p = Path('/home/clawdy/.openclaw/cron/jobs.json')
data = json.loads(p.read_text())
jobs = data.get('jobs') if isinstance(data, dict) else data
changed = False
needle = 'Vergelijk signalen, vermijd dubbele items, filter marketing zonder echte verandering, en focus op echt nieuwe ontwikkelingen uit de afgelopen 48 uur.'
replacement = 'Vergelijk signalen, vermijd dubbele items, en als meerdere bronnen over dezelfde ontwikkeling gaan, bundel dat tot één item met de beste bronverwijzingen. Filter marketing zonder echte verandering, en focus op echt nieuwe ontwikkelingen uit de afgelopen 48 uur.'
for job in jobs:
    if job.get('name') != 'daily-ai-update':
        continue
    payload = job.get('payload') or {}
    message = payload.get('message')
    if isinstance(message, str) and needle in message:
        payload['message'] = message.replace(needle, replacement)
        changed = True
        break
if not changed:
    raise SystemExit('daily-ai-update prompt needle niet gevonden of al aangepast')
p.write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n')
print('updated')
