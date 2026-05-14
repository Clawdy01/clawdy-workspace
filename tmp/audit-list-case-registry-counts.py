#!/usr/bin/env python3
import importlib.util
import json
from pathlib import Path

ROOT = Path('/home/clawdy/.openclaw/workspace')
SCRIPT = ROOT / 'scripts' / 'ai-briefing-regression-check.py'

spec = importlib.util.spec_from_file_location('ai_briefing_regression_check', SCRIPT)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)

status_module = module.load_status_module()
producer_module = module.load_proof_recheck_producer_module()
without_watchdog = module.build_named_case_runners_without_watchdog_batches(status_module, producer_module)
with_watchdog = module.build_named_case_runners(status_module, producer_module)

payload = {
    'default_cases': len(module.DEFAULT_CASES),
    'status_phase_cases': len(module.STATUS_PHASE_CASES),
    'status_stdout_cases': len(module.STATUS_STDOUT_CASES),
    'watchdog_stdout_cases': len(module.WATCHDOG_STDOUT_CASES),
    'status_summary_audit_cases': len(module.STATUS_SUMMARY_AUDIT_CASES),
    'proof_recheck_cases': len(module.PROOF_RECHECK_CASES),
    'proof_recheck_producer_cases': len(module.PROOF_RECHECK_PRODUCER_CASES),
    'brief_consumer_cases': len(module.BRIEF_CONSUMER_CASES),
    'watchdog_alert_cases': len(module.WATCHDOG_ALERT_CASES),
    'watchdog_producer_cases': len(module.WATCHDOG_PRODUCER_CASES),
    'named_cases_without_watchdog_batches': len(without_watchdog),
    'named_cases_with_watchdog_batches': len(with_watchdog),
    'watchdog_batch_delta': len(with_watchdog) - len(without_watchdog),
    'alphabetical_first_case': sorted(with_watchdog)[0],
    'alphabetical_last_case': sorted(with_watchdog)[-1],
}
print(json.dumps(payload, ensure_ascii=False, indent=2))
