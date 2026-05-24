import json
from pathlib import Path

p = Path('/home/clawdy/.openclaw/cron/jobs.json')
data = json.loads(p.read_text())
for job in data['jobs']:
    if job.get('name') == 'daily-ai-update':
        msg = job['payload']['message']
        old = 'focus op echt nieuwe ontwikkelingen uit de afgelopen 48 uur. Vermijd dubbele items, en als meerdere bronnen over dezelfde ontwikkeling gaan, bundel dat tot één item.'
        new = 'focus op echt nieuwe ontwikkelingen uit de afgelopen 48 uur. vermijd dubbele items, en als meerdere bronnen over dezelfde ontwikkeling gaan, bundel dat tot één item.'
        if old not in msg:
            raise SystemExit('expected snippet not found')
        job['payload']['message'] = msg.replace(old, new, 1)
        break
else:
    raise SystemExit('daily-ai-update not found')
p.write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n')
