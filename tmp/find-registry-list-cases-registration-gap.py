from pathlib import Path
import re

path = Path('/home/clawdy/.openclaw/workspace/scripts/ai-briefing-regression-check.py')
text = path.read_text()

name_pattern = re.compile(r"name='(registry-keeps-list-cases-full-registry-[^']+)'")
registered_pattern = re.compile(r"named_cases\['(registry-keeps-list-cases-full-registry-[^']+)'\]")

produced = sorted(set(name_pattern.findall(text)))
registered = sorted(set(registered_pattern.findall(text)))
missing = [name for name in produced if name not in registered]
extra = [name for name in registered if name not in produced]
print('produced', len(produced))
print('registered', len(registered))
print('missing', len(missing))
for name in missing[:50]:
    print('MISSING', name)
print('extra', len(extra))
for name in extra[:50]:
    print('EXTRA', name)
