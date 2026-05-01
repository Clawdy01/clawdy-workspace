import json
import importlib.util
from pathlib import Path

path = Path('scripts/ai-briefing-watchdog-producer.py')
spec = importlib.util.spec_from_file_location('watchdog_producer', path)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

payload = {
    'summary': 'test',
    'proof_next_action_text': 'wacht tot 09:15 en draai daarna opnieuw',
    'proof_recheck_after_text_compact': 'wacht tot 09:15 en draai daarna opnieuw',
    'proof_wait_until_text': 'wacht tot 09:15 en draai daarna opnieuw',
    'proof_wait_until_reason_text': 'wacht tot 09:15 en draai daarna opnieuw',
}
quiet = mod.build_quiet_summary(json.dumps(payload), '', 2)
print(quiet)
assert quiet.count('wacht tot 09:15 en draai daarna opnieuw') == 1, quiet
