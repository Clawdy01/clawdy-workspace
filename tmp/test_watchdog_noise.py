import importlib.util
from pathlib import Path
from subprocess import CompletedProcess

path = Path('/home/clawdy/.openclaw/workspace/scripts/ai-briefing-watchdog.py')
spec = importlib.util.spec_from_file_location('ai_briefing_watchdog', path)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

mod.subprocess.run = lambda *a, **k: CompletedProcess(
    a[0],
    0,
    stdout='noise before json\n{"ok": true, "found": true, "enabled": true, "readiness_phase": "ready-for-first-run", "text": "klaar voor eerste run"}\n',
    stderr='',
)

status = mod.load_status(5)
print(status['text'])
