#!/usr/bin/env python3
import importlib.util
import json
from pathlib import Path

ROOT = Path('/home/clawdy/.openclaw/workspace')
MODULE_PATH = ROOT / 'scripts' / 'ai-briefing-regression-check.py'
spec = importlib.util.spec_from_file_location('ai_briefing_regression_check', MODULE_PATH)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)

case_names = {
    'watchdog-alert-proof-target-check-suppresses-before-deadline',
    'watchdog-alert-proof-target-check-unsuppresses-after-deadline',
}
results = [
    module.evaluate_watchdog_alert_case(case)
    for case in module.WATCHDOG_ALERT_CASES
    if case.get('name') in case_names
]
summary = {
    'ok': all(result.get('ok') for result in results),
    'failed_count': sum(0 if result.get('ok') else 1 for result in results),
    'failing_case_names': [result.get('name') for result in results if not result.get('ok')],
    'results': results,
}
print(json.dumps(summary, ensure_ascii=False, indent=2))
