#!/usr/bin/env python3
import importlib.util
import json
import pathlib

module_path = pathlib.Path('/home/clawdy/.openclaw/workspace/scripts/ai-briefing-regression-check.py')
spec = importlib.util.spec_from_file_location('ai_briefing_regression_check', module_path)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)
status_module = module.load_status_module()
producer_module = module.load_proof_recheck_producer_module()
results = [module.evaluate_case(status_module, case) for case in module.DEFAULT_CASES]
results.extend(module.evaluate_status_phase_case(status_module, case) for case in module.STATUS_PHASE_CASES)
results.extend(module.evaluate_proof_recheck_case(case) for case in module.PROOF_RECHECK_CASES)
results.extend(module.evaluate_proof_recheck_producer_case(case) for case in module.PROOF_RECHECK_PRODUCER_CASES)
results.extend(module.evaluate_brief_consumer_case(case) for case in module.BRIEF_CONSUMER_CASES)
results.extend(module.evaluate_watchdog_alert_case(case) for case in module.WATCHDOG_ALERT_CASES)
results.extend(module.evaluate_watchdog_producer_case(case) for case in module.WATCHDOG_PRODUCER_CASES)
results.append(module.evaluate_producer_quiet_requested_outputs_fallback_case(producer_module))
results.append(module.evaluate_proof_recheck_consumer_format_passthrough_case())
failing = [r for r in results if not r['ok']]
print(json.dumps({
    'ok': not failing,
    'summary': {
        'case_count': len(results),
        'passed_count': len(results) - len(failing),
        'failed_count': len(failing),
        'failing_case_names': [r['name'] for r in failing],
    },
}, ensure_ascii=False))
raise SystemExit(0 if not failing else 1)
