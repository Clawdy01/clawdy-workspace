from pathlib import Path
import re

path = Path('/home/clawdy/.openclaw/workspace/scripts/ai-briefing-regression-check.py')
text = path.read_text()

prefix = 'registry-keeps-list-cases-'
name_pattern = re.compile(r"name='([^']+)'")
registered_pattern = re.compile(r"named_cases\['([^']+)'\]")
produced = sorted({n for n in name_pattern.findall(text) if n.startswith(prefix)})
registered = sorted({n for n in registered_pattern.findall(text) if n.startswith(prefix)})
missing = [n for n in produced if n not in registered]
extra = [n for n in registered if n not in produced]
print('produced', len(produced))
print('registered', len(registered))
print('missing', len(missing))
for n in missing:
    print('MISSING', n)
print('extra', len(extra))
for n in extra:
    print('EXTRA', n)
