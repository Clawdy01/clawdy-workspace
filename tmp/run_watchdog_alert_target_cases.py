#!/usr/bin/env python3
import importlib.util
import json
from pathlib import Path

module_path = Path('/home/clawdy/.openclaw/workspace/scripts/ai-briefing-regression-check.py')
spec = importlib.util.spec_from_file_location('ai_briefing_regression_check', module_path)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)

wanted = {
    'watchdog-alert-proof-target-check-board-suite-keeps-no-reply-before-deadline',
    'watchdog-alert-proof-target-check-board-suite-unsuppresses-after-deadline',
}
results = [module.evaluate_watchdog_alert_case(case) for case in module.WATCHDOG_ALERT_CASES if case.get('name') in wanted]
failed = [result['name'] for result in results if not result.get('ok')]
print(json.dumps({
    'ok': not failed,
    'failed_count': len(failed),
    'results': results,
}, ensure_ascii=False))
