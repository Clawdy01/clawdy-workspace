#!/usr/bin/env python3
import importlib.util
from pathlib import Path

path = Path('/home/clawdy/.openclaw/workspace/scripts/ai-briefing-status.py')
spec = importlib.util.spec_from_file_location('ai_briefing_status', path)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)
summary = '''Titel

1) Frontier modelupdates
- GPT en Claude model update

2) Agents en automation workflows
- Nieuwe coding workflow

3) Research
- Nieuwe research paper op arXiv

Wat moeten wij hiermee?
- Iets

Wat ik vandaag het belangrijkst vind
- Dit

Bronnenlijst met URLs
- https://openai.com/index/test
- https://github.com/test/repo
- https://arxiv.org/abs/1234.5678
'''
audit = mod.audit_summary_output(summary)
print(audit['ok'])
print(audit['category_theme_count'])
print(audit['text'])
