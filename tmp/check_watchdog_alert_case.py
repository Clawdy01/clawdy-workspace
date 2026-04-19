#!/usr/bin/env python3
import importlib.util
import json
import pathlib

module_path = pathlib.Path('/home/clawdy/.openclaw/workspace/scripts/ai-briefing-regression-check.py')
spec = importlib.util.spec_from_file_location('ai_briefing_regression_check', module_path)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)
case = next(case for case in module.WATCHDOG_ALERT_CASES if case['name'] == 'watchdog-alert-proof-target-check-board-suite-keeps-no-reply-before-deadline')
result = module.evaluate_watchdog_alert_case(case)
print(json.dumps(result, ensure_ascii=False, indent=2))
raise SystemExit(0 if result['ok'] else 1)
