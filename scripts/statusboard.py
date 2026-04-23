#!/usr/bin/env python3
import argparse
import json
import signal
import subprocess
from datetime import datetime, timezone
from pathlib import Path
from time import monotonic

from mail_heuristics import (
    format_attachment_hint,
    format_cluster_hint,
    format_next_step_alternative_commands,
    format_next_step_candidate_hint,
    format_security_alert_hint,
    format_stale_attention_hint,
)

ROOT = Path('/home/clawdy/.openclaw/workspace')
BRIEF = ROOT / 'scripts' / 'clawdy-brief.py'


def unique_bits(bits):
    unique = []
    for bit in bits:
        cleaned = ' '.join((bit or '').split())
        if not cleaned:
            continue
        skip = False
        for existing in list(unique):
            if cleaned == existing or cleaned in existing:
                skip = True
                break
            if existing in cleaned:
                unique.remove(existing)
        if skip:
            continue
        unique.append(cleaned)
    return unique


def extract_json_document(text):
    text = (text or '').strip()
    if not text:
        raise json.JSONDecodeError('Expecting value', text, 0)
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        pass

    lines = text.splitlines()
    for index, line in enumerate(lines):
        stripped = line.lstrip()
        if not stripped.startswith(('{', '[')):
            continue
        candidate = '\n'.join(lines[index:]).strip()
        try:
            return json.loads(candidate)
        except json.JSONDecodeError:
            continue
    raise json.JSONDecodeError('Expecting value', text, 0)


def run_brief_json(reference_ms=None):
    command = ['python3', str(BRIEF), '--json']
    if reference_ms is not None:
        command.extend(['--reference-ms', str(reference_ms)])
    try:
        proc = subprocess.run(
            command,
            cwd=ROOT,
            capture_output=True,
            text=True,
            check=False,
            timeout=60,
        )
    except subprocess.TimeoutExpired:
        raise SystemExit('clawdy-brief timed out')
    if proc.returncode != 0:
        raise SystemExit(proc.stderr.strip() or proc.stdout.strip() or f'clawdy-brief failed: {proc.returncode}')
    return extract_json_document(proc.stdout)


def render_text(data, show_preview=False):
    status = data['status']
    security = data.get('security') or {}
    recent_mail = data.get('recent_mail') or []
    recent_mail_current = data.get('recent_mail_current') or []
    recent_threads = data.get('recent_threads') or []
    recent_threads_current = data.get('recent_threads_current') or []
    mail_triage = data.get('mail_triage') or {}
    mail_focus = data.get('mail_focus') or {}
    mail_high_recent = data.get('mail_high_recent') or {}
    mail_next_step = data.get('mail_next_step') or {}
    creative_smoke = data.get('creative_smoke') or {}
    ai_briefing_status = data.get('ai_briefing_status') or {}
    mail = data['mail']
    session = status.get('session') or {}

    lines = []
    lines.append('Statusboard')
    lines.append(f"- OpenClaw {status['version']}")
    lines.append(f"- gateway: {status['gateway']['text']}")
    lines.append(f"- telegram: {status['telegram']}, heartbeat {status['heartbeat']}")
    lines.append(
        f"- taken: {status['tasks']['active']} actief, {status['tasks']['failures']} failures, {status['tasks']['lost']} vermist"
    )
    lines.append(
        f"- audit: {status['audit']['errors']} errors, {status['audit']['warnings']} warns"
    )
    lines.append(f"- security: {security.get('text', 'onbekend')}")
    if session:
        context = f", {session['percent_used']}% context" if session.get('percent_used') is not None else ''
        lines.append(
            f"- sessie: {session.get('age', 'onbekend')}, model {session.get('model', 'onbekend')}, reasoning {session.get('reasoning', 'uit')}{context}"
        )
    if creative_smoke:
        smoke_steps = creative_smoke.get('steps') or []
        smoke_bits = []
        for step in smoke_steps:
            if step.get('kind') == 'daylog':
                smoke_bits.append(f"{step.get('mode')}: {step.get('files_ok', 0)}/{step.get('files_total', 0)} ok, {step.get('files_warning', 0)} warnings")
            elif step.get('kind') == 'cleanup':
                smoke_bits.append(f"{step.get('mode')}: cand {step.get('candidate_total', 0)}, del {step.get('deleted_total', 0)}")
        smoke_text = '; '.join(smoke_bits) if smoke_bits else 'geen stappen'
        lines.append(f"- creative smoke: {'ok' if creative_smoke.get('ok') else 'warning'} ({smoke_text})")
    if ai_briefing_status:
        ai_bits = [ai_briefing_status.get('text', 'onbekend')]
        if ai_briefing_status.get('readiness_text'):
            ai_bits.append(ai_briefing_status['readiness_text'])
        if ai_briefing_status.get('delivery_text'):
            ai_bits.append(f"naar {ai_briefing_status['delivery_text']}")
        if ai_briefing_status.get('reference_context_text'):
            ai_bits.append(ai_briefing_status['reference_context_text'])
        if ai_briefing_status.get('proof_text'):
            ai_bits.append(ai_briefing_status['proof_text'])
        if ai_briefing_status.get('attention_text'):
            ai_bits.append(f"let op: {ai_briefing_status['attention_text']}")
        runtime_audit = ai_briefing_status.get('runtime_audit') or {}
        next_run_audit = ai_briefing_status.get('next_run_audit') or {}
        storage_audit = ai_briefing_status.get('storage_audit') or {}
        runlog_audit = ai_briefing_status.get('runlog_audit') or {}
        uniqueness_audit = ai_briefing_status.get('uniqueness_audit') or {}
        proof_freshness = ai_briefing_status.get('proof_freshness') or {}
        if runtime_audit.get('session_target') and runtime_audit.get('wake_mode'):
            ai_bits.append(f"route {runtime_audit['session_target']}/{runtime_audit['wake_mode']} via {runtime_audit.get('agent_id') or 'onbekend'}")
        if next_run_audit.get('text'):
            ai_bits.append(next_run_audit['text'])
        if storage_audit.get('text'):
            ai_bits.append(storage_audit['text'])
        if runlog_audit.get('text'):
            ai_bits.append(runlog_audit['text'])
        if uniqueness_audit.get('text'):
            ai_bits.append(uniqueness_audit['text'])
        proof_freshness_text = ai_briefing_status.get('proof_freshness_text') or proof_freshness.get('text')
        if proof_freshness_text:
            ai_bits.append(proof_freshness_text)
        summary_output_examples = [example for example in (ai_briefing_status.get('summary_output_examples') or []) if example]
        if summary_output_examples:
            ai_bits.append('outputvoorbeelden: ' + '; '.join(summary_output_examples[:2]))
        if ai_briefing_status.get('proof_progress_text'):
            ai_bits.append(ai_briefing_status['proof_progress_text'])
        payload_audit = ai_briefing_status.get('payload_audit') or {}
        if ai_briefing_status.get('proof_config_identity_text'):
            ai_bits.append(ai_briefing_status['proof_config_identity_text'])
        if ai_briefing_status.get('last_run_config_relation_text'):
            ai_bits.append(ai_briefing_status['last_run_config_relation_text'])
        elif ai_briefing_status.get('updated_at_hint'):
            fingerprint = payload_audit.get('message_sha256_short')
            if fingerprint:
                ai_bits.append(f"config {ai_briefing_status['updated_at_hint']} gewijzigd, hash {fingerprint}")
            else:
                ai_bits.append(f"config {ai_briefing_status['updated_at_hint']} gewijzigd")
        if ai_briefing_status.get('next_run_at_text') and not ai_briefing_status.get('proof_next_qualifying_slot_at_text'):
            next_run_text = f"volgende {ai_briefing_status['next_run_at_text']}"
            if ai_briefing_status.get('next_run_hint'):
                next_run_text += f" ({ai_briefing_status['next_run_hint']})"
            ai_bits.append(next_run_text)
        if ai_briefing_status.get('proof_due_at_text'):
            proof_due_text = f"bewijs uiterlijk {ai_briefing_status['proof_due_at_text']}"
            if ai_briefing_status.get('proof_due_hint'):
                proof_due_text += f" ({ai_briefing_status['proof_due_hint']})"
            ai_bits.append(proof_due_text)
        if ai_briefing_status.get('proof_target_due_at_text') and not ai_briefing_status.get('proof_countdown_text'):
            proof_target_due_text = f"bewijsdoel bij groene runs uiterlijk {ai_briefing_status['proof_target_due_at_text']}"
            if ai_briefing_status.get('proof_target_due_hint'):
                proof_target_due_text += f" ({ai_briefing_status['proof_target_due_hint']})"
            ai_bits.append(proof_target_due_text)
        if ai_briefing_status.get('proof_state_text'):
            ai_bits.append(ai_briefing_status['proof_state_text'])
        if ai_briefing_status.get('proof_blocker_text'):
            ai_bits.append(ai_briefing_status['proof_blocker_text'])
        if ai_briefing_status.get('proof_wait_until_text'):
            ai_bits.append(ai_briefing_status['proof_wait_until_text'])
        if ai_briefing_status.get('proof_next_action_window_text'):
            ai_bits.append(ai_briefing_status['proof_next_action_window_text'])
        elif ai_briefing_status.get('proof_next_action_text'):
            ai_bits.append(ai_briefing_status['proof_next_action_text'])
        if ai_briefing_status.get('proof_recheck_commands_text'):
            ai_bits.append(ai_briefing_status['proof_recheck_commands_text'])
        if not ai_briefing_status.get('proof_next_action_window_text'):
            if ai_briefing_status.get('proof_recheck_window_text') and ai_briefing_status.get('proof_recheck_window_text') != ai_briefing_status.get('proof_next_action_text'):
                ai_bits.append(ai_briefing_status['proof_recheck_window_text'])
            elif ai_briefing_status.get('proof_recheck_after_text_compact'):
                ai_bits.append(ai_briefing_status['proof_recheck_after_text_compact'])
        if ai_briefing_status.get('proof_plan_text'):
            ai_bits.append(ai_briefing_status['proof_plan_text'])
        if ai_briefing_status.get('proof_schedule_risk_text'):
            ai_bits.append(ai_briefing_status['proof_schedule_risk_text'])
        if ai_briefing_status.get('proof_countdown_text'):
            ai_bits.append(ai_briefing_status['proof_countdown_text'])
        elif ai_briefing_status.get('proof_target_run_slots_context_text'):
            ai_bits.append(f"kwalificatie-slots {ai_briefing_status['proof_target_run_slots_context_text']}")
        if ai_briefing_status.get('last_run_timeout_text'):
            ai_bits.append(ai_briefing_status['last_run_timeout_text'])
        if ai_briefing_status.get('recent_run_duration_text'):
            ai_bits.append(ai_briefing_status['recent_run_duration_text'])
        elif ai_briefing_status.get('proof_target_run_slots_text'):
            ai_bits.append(f"kwalificatie-slots {ai_briefing_status['proof_target_run_slots_text']}")
        if ai_briefing_status.get('proof_target_check_gate_text'):
            ai_bits.append(ai_briefing_status['proof_target_check_gate_text'])
        if ai_briefing_status.get('proof_recheck_schedule_text'):
            ai_bits.append(ai_briefing_status['proof_recheck_schedule_text'])
        if ai_briefing_status.get('proof_recheck_schedule_kind_text'):
            ai_bits.append(ai_briefing_status['proof_recheck_schedule_kind_text'])
        if ai_briefing_status.get('proof_wait_until_reason_text'):
            ai_bits.append(ai_briefing_status['proof_wait_until_reason_text'])
        if ai_briefing_status.get('last_run_at_text'):
            ai_bits.append(f"laatste {ai_briefing_status['last_run_at_text']}")
        last_run_summary = ai_briefing_status.get('last_run_summary') or {}
        if last_run_summary.get('model'):
            model_text = last_run_summary['model']
            if last_run_summary.get('provider'):
                model_text = f"{last_run_summary['provider']}/{model_text}"
            ai_bits.append(f"model {model_text}")
        if last_run_summary.get('duration_text'):
            duration_text = f"duur {last_run_summary['duration_text']}"
            if last_run_summary.get('total_tokens') is not None:
                duration_text += f", {last_run_summary['total_tokens']} tokens"
            ai_bits.append(duration_text)
        if last_run_summary.get('summary_preview'):
            ai_bits.append(f"preview {last_run_summary['summary_preview']}")
        summary_output_audit = last_run_summary.get('summary_output_audit') or {}
        if summary_output_audit.get('available'):
            ai_bits.append(summary_output_audit.get('text', 'output-audit onbekend'))
            ai_bits.append(f"items {summary_output_audit.get('item_count', 0)}")
            ai_bits.append(f"bron-URLs {summary_output_audit.get('source_url_count', 0)}")
            ai_bits.append(f"unieke bron-URLs {summary_output_audit.get('unique_source_url_count', 0)}")
            ai_bits.append(f"unieke titels {summary_output_audit.get('unique_item_title_count', 0)}/{summary_output_audit.get('item_count', 0)}")
            ai_bits.append(f"items met meerdere bron-URLs {summary_output_audit.get('items_with_multiple_sources_count', 0)}/{summary_output_audit.get('item_count', 0)}")
            duplicate_examples = summary_output_audit.get('duplicate_item_title_examples') or []
            if duplicate_examples:
                ai_bits.append(
                    'dubbele titels ' + ', '.join(
                        f"{example.get('title', 'onbekend')} x{example.get('count', 0)}"
                        for example in duplicate_examples[:3]
                    )
                )
            items_missing_source_examples = summary_output_audit.get('items_missing_source_examples') or []
            if items_missing_source_examples:
                ai_bits.append('items zonder bron ' + ', '.join(items_missing_source_examples[:3]))
            items_invalid_source_line_examples = summary_output_audit.get('items_invalid_source_line_examples') or []
            if items_invalid_source_line_examples:
                ai_bits.append(
                    'items met ongeldige Bron-regel '
                    + ', '.join(
                        f"{example.get('title', 'item')} -> {example.get('source_line', '')}"
                        for example in items_invalid_source_line_examples[:2]
                    )
                )
            top3_missing_source_examples = summary_output_audit.get('top3_missing_source_examples') or []
            if top3_missing_source_examples:
                ai_bits.append('top3 zonder bron ' + ', '.join(top3_missing_source_examples[:3]))
            top3_invalid_source_line_examples = summary_output_audit.get('top3_invalid_source_line_examples') or []
            if top3_invalid_source_line_examples:
                ai_bits.append(
                    'top3 met ongeldige Bron-regel '
                    + ', '.join(
                        f"{example.get('title', 'item')} -> {example.get('source_line', '')}"
                        for example in top3_invalid_source_line_examples[:2]
                    )
                )
            top3_missing_multi_source_examples = summary_output_audit.get('top3_missing_multi_source_examples') or []
            if top3_missing_multi_source_examples:
                ai_bits.append('top3 zonder multi-source ' + ', '.join(top3_missing_multi_source_examples[:3]))
            top3_missing_multi_domain_source_examples = summary_output_audit.get('top3_missing_multi_domain_source_examples') or []
            if top3_missing_multi_domain_source_examples:
                ai_bits.append(
                    'top3 zonder multi-domein bronregel '
                    + ', '.join(top3_missing_multi_domain_source_examples[:3])
                )
            top3_missing_recent_date_examples = summary_output_audit.get('top3_missing_recent_date_examples') or []
            if top3_missing_recent_date_examples:
                ai_bits.append('top3 zonder recente datum ' + ', '.join(top3_missing_recent_date_examples[:3]))
            top3_missing_primary_fresh_examples = summary_output_audit.get('top3_missing_primary_fresh_examples') or []
            if top3_missing_primary_fresh_examples:
                ai_bits.append('top3 zonder primaire+verse combo ' + ', '.join(top3_missing_primary_fresh_examples[:3]))
            ai_bits.append(f"top3 brondomeinen {summary_output_audit.get('first3_source_domain_count', 0)}")
            ai_bits.append(f"top3 primaire brondomeinen {summary_output_audit.get('first3_primary_source_domain_count', 0)}")
            ai_bits.append(f"top3 primaire bronfamilies {summary_output_audit.get('first3_primary_source_family_count', 0)}")
            ai_bits.append(f"top3 unieke bron-URLs {summary_output_audit.get('first3_unique_source_url_count', 0)}/3")
            ai_bits.append(f"items met bron {summary_output_audit.get('items_with_source_count', 0)}/{summary_output_audit.get('item_count', 0)}")
            ai_bits.append(
                f"geldige Bron-regels {summary_output_audit.get('items_with_valid_source_line_count', 0)}/{summary_output_audit.get('item_count', 0)}"
            )
            ai_bits.append(f"top3 met bron {summary_output_audit.get('first3_items_with_source_count', 0)}/3")
            ai_bits.append(
                f"top3 geldige Bron-regels {summary_output_audit.get('first3_items_with_valid_source_line_count', 0)}/3"
            )
            ai_bits.append(f"top3 met meerdere bron-URLs {summary_output_audit.get('first3_items_with_multiple_sources_count', 0)}/3")
            ai_bits.append(
                f"top3 met multi-domein bronregels {summary_output_audit.get('first3_items_with_multi_domain_sources_count', 0)}/3"
            )
            ai_bits.append(f"top3 met primaire bron {summary_output_audit.get('first3_items_with_primary_source_count', 0)}/3")
            ai_bits.append(f"datums {summary_output_audit.get('dated_item_count', 0)}/{summary_output_audit.get('item_count', 0)}")
            ai_bits.append(f"vers top3 {summary_output_audit.get('fresh_dated_first3_count', 0)}/3")
            ai_bits.append(f"recent top3 {summary_output_audit.get('recent_dated_first3_count', 0)}/3")
            ai_bits.append(f"toekomstige datums {summary_output_audit.get('future_dated_item_count', 0)}")
            ai_bits.append(f"top3 met bron+recente datum {summary_output_audit.get('first3_evidenced_item_count', 0)}/3")
            ai_bits.append(f"top3 met primaire bron+verse datum {summary_output_audit.get('first3_primary_fresh_item_count', 0)}/3")
            ai_bits.append(
                f"brondomeinen {summary_output_audit.get('source_domain_count', 0)}, primair {summary_output_audit.get('primary_source_domain_count', 0)}"
            )
            ai_bits.append(f"categorie-thema's {summary_output_audit.get('category_theme_count', 0)}/7")
        if ai_briefing_status.get('runs_total'):
            rate_bits = []
            if ai_briefing_status.get('success_rate_pct') is not None:
                rate_bits.append(f"succes {ai_briefing_status['success_rate_pct']:.1f}%")
            if ai_briefing_status.get('delivery_rate_pct') is not None:
                rate_bits.append(f"delivery {ai_briefing_status['delivery_rate_pct']:.1f}%")
            if ai_briefing_status.get('success_streak'):
                rate_bits.append(f"streak {ai_briefing_status['success_streak']}")
            if rate_bits:
                ai_bits.append(', '.join(rate_bits))
        recent_runs = ai_briefing_status.get('recent_runs_summary') or []
        if recent_runs:
            recent_bits = []
            for run in recent_runs[-2:]:
                run_bits = [run.get('status') or 'onbekend']
                if run.get('delivered'):
                    run_bits.append('afgeleverd')
                if run.get('run_at_hint'):
                    run_bits.append(run['run_at_hint'])
                elif run.get('run_at_text'):
                    run_bits.append(run['run_at_text'])
                if run.get('duration_text'):
                    run_bits.append(run['duration_text'])
                recent_bits.append(' / '.join(run_bits))
            ai_bits.append(f"recente runs {'; '.join(recent_bits)}")
        lines.append(f"- ai briefing: {'; '.join(unique_bits(ai_bits))}")
    mail_line = f"- mail: last_uid {mail['last_uid']}, notified {mail['tracked_notifications']} ({mail['account']})"
    recent_high_count = mail_high_recent.get('total_count', mail_high_recent.get('count', 0))
    recent_high_groups = mail_high_recent.get('total_related_group_count', mail_high_recent.get('related_group_count', 0))
    recent_attention_now_count = mail_high_recent.get('total_high_attention_now_count', mail_high_recent.get('total_attention_now_count', mail_high_recent.get('attention_now_count', 0)))
    if recent_high_count > 0:
        mail_line += f", hoog recent {recent_high_count}"
        if recent_high_groups:
            mail_line += f" in {recent_high_groups} cluster(s)"
        recent_stale_high_count = mail_high_recent.get('total_high_stale_attention_count', mail_high_recent.get('total_stale_attention_count', mail_high_recent.get('stale_attention_count', 0)))
        mail_line += f", actueel {recent_attention_now_count}, niet actueel {recent_stale_high_count}"
        if recent_attention_now_count == 0:
            mail_line += ", alles niet actueel"
    lines.append(mail_line)
    top_high_groups = mail_high_recent.get('top_related_groups') or []
    if top_high_groups:
        group_bits = [format_cluster_hint(group, include_age=True) for group in top_high_groups[:2]]
        remaining = max(0, len(top_high_groups) - len(group_bits))
        suffix = f" +{remaining} cluster(s)" if remaining else ''
        lines.append(f"- hoge mailclusters: {'; '.join(group_bits)}{suffix}")
    if recent_mail_current:
        latest = recent_mail_current[0]
        age = f" ({latest.get('age_hint')})" if latest.get('age_hint') else ''
        line = f"- actuele betekenisvolle mail: #{latest.get('uid', '?')} {latest.get('from', 'onbekend')}: {latest.get('subject', '(geen onderwerp)')}{format_attachment_hint(latest)}{format_security_alert_hint(latest)}{age}{format_stale_attention_hint(latest)}"
        if show_preview and latest.get('preview'):
            line += f" — {latest.get('preview')[:140]}"
        lines.append(line)
    elif recent_mail:
        latest = recent_mail[0]
        age = f" ({latest.get('age_hint')})" if latest.get('age_hint') else ''
        line = f"- laatste betekenisvolle mail: #{latest.get('uid', '?')} {latest.get('from', 'onbekend')}: {latest.get('subject', '(geen onderwerp)')}{format_attachment_hint(latest)}{format_security_alert_hint(latest)}{age}{format_stale_attention_hint(latest)}"
        if show_preview and latest.get('preview'):
            line += f" — {latest.get('preview')[:140]}"
        lines.append(line)
    thread = None
    thread_label = 'actieve thread'
    if recent_threads_current:
        thread = recent_threads_current[0]
    elif recent_threads:
        thread = recent_threads[0]
        if thread.get('stale_attention'):
            thread_label = 'laatste betekenisvolle thread'
    if thread:
        stale = ' [niet actueel]' if thread.get('stale_attention') else ''
        variant_suffix = f", +{thread.get('subject_variant_count', 0) - 1} variant(en)" if (thread.get('subject_variant_count', 0) or 0) > 1 else ''
        time_bits = [bit for bit in [thread.get('latest_age_hint'), thread.get('span_hint')] if bit]
        time_suffix = f", {', '.join(time_bits)}" if time_bits else ''
        lines.append(
            f"- {thread_label}: {thread.get('subject', '(geen onderwerp)')} ({thread.get('message_count', 0)}x{variant_suffix}, laatste van {thread.get('latest_from', 'onbekend')}{time_suffix}){format_attachment_hint(thread)}{format_security_alert_hint(thread)}{stale}"
        )
    triage_items = mail_triage.get('items') or []
    if triage_items:
        item = triage_items[0]
        age = f" ({item.get('age_hint')})" if item.get('age_hint') else ''
        stale = ' [niet actueel]' if item.get('stale_attention') else ''
        lines.append(
            f"- triage eerst: #{item.get('uid', '?')} {item.get('from', 'onbekend')}: {item.get('subject', '(geen onderwerp)')}{format_attachment_hint(item)}{format_security_alert_hint(item)} [{item.get('action_hint', 'ter info')}{' ↩' if item.get('reply_needed') else ''}]{age}{stale}"
        )
    focus_item = mail_focus.get('focus')
    if focus_item:
        suffix = ' ↩' if focus_item.get('reply_needed') else ''
        draft_flag = ' + concept' if mail_focus.get('draft') else ''
        age = f" ({focus_item.get('age_hint')})" if focus_item.get('age_hint') else ''
        related_burst = mail_focus.get('focus_related_burst_count', 0)
        exact_burst = mail_focus.get('focus_burst_count', 0)
        burst = max(related_burst, exact_burst)
        burst_label = 'verwant' if related_burst > exact_burst else 'soortgelijk'
        burst_suffix = f' ({burst}x {burst_label})' if burst > 1 else ''
        focus_line = (
            f"- focus nu ({mail_focus.get('scope', 'mail')}): #{focus_item.get('uid', '?')} {focus_item.get('from', 'onbekend')}: {focus_item.get('subject', '(geen onderwerp)')}{format_attachment_hint(focus_item)}{format_security_alert_hint(focus_item)} [{focus_item.get('action_hint', 'ter info')}{suffix}]{draft_flag}{burst_suffix}{age}"
        )
        if focus_item.get('stale_attention'):
            focus_line = (
                f"- geen actuele focus, laatste kandidaat was: #{focus_item.get('uid', '?')} {focus_item.get('from', 'onbekend')}: {focus_item.get('subject', '(geen onderwerp)')}{format_attachment_hint(focus_item)}{format_security_alert_hint(focus_item)} [{focus_item.get('action_hint', 'ter info')}{suffix}]{draft_flag}{burst_suffix}{age} [niet actueel]"
            )
        lines.append(focus_line)
    elif mail_focus.get('fallback_thread'):
        thread = mail_focus.get('fallback_thread') or {}
        participants = ', '.join((thread.get('participants') or [])[:2]) or thread.get('latest_from', 'onbekend')
        extra_people = max(0, len(thread.get('participants') or []) - 2)
        if extra_people:
            participants += f' (+{extra_people})'
        skipped = mail_focus.get('skipped_ephemeral_count', 0)
        time_bits = [bit for bit in [thread.get('latest_age_hint'), thread.get('span_hint')] if bit]
        time_suffix = f", {', '.join(time_bits)}" if time_bits else ''
        stale = ' [niet actueel]' if thread.get('stale_attention') else ''
        suffix = f", code-noise overgeslagen: {skipped}" if skipped else ''
        label = 'geen actuele focus, laatste betekenisvolle thread' if thread.get('stale_attention') else 'focus fallback'
        lines.append(
            f"- {label}: {participants} — {thread.get('subject', '(geen onderwerp)')} ({thread.get('message_count', 0)}x{time_suffix}){format_attachment_hint(thread)}{suffix}{stale}"
        )
    selected_next = mail_next_step.get('selected_group') or {}
    if mail_next_step.get('recommended_route') and mail_next_step.get('recommended_route') != 'noop' and selected_next:
        review_only = bool(mail_next_step.get('review_only'))
        label = 'mail review' if review_only or selected_next.get('stale_attention') else 'mail next'
        lines.append(
            f"- {label}: {format_next_step_candidate_hint(selected_next, include_age=True)}"
            + (' + concept' if mail_next_step.get('selected_draft') else '')
        )
        candidates = mail_next_step.get('candidates') or []
        alternative_candidates = candidates[1:3] if len(candidates) > 1 else []
        if alternative_candidates:
            preview = '; '.join(format_next_step_candidate_hint(candidate, include_age=True) for candidate in alternative_candidates)
            remaining = max(0, len(candidates) - 1 - len(alternative_candidates))
            suffix = f" +{remaining} meer" if remaining else ''
            lines.append(f"- mail queue: {preview}{suffix}")
            command_preview = format_next_step_alternative_commands(alternative_candidates, limit=len(alternative_candidates))
            if command_preview:
                lines.append(f"- mail queue commands: {command_preview}")
        if mail_next_step.get('recommended_command'):
            command_label = 'mail review command' if review_only or selected_next.get('stale_attention') else 'mail next command'
            lines.append(f"- {command_label}: {mail_next_step.get('recommended_command')}")
    return '\n'.join(lines)


def build_run_metadata(*, started_at, finished_at, duration_ms):
    duration_seconds = round(duration_ms / 1000, 3)
    return {
        'generated_at': finished_at.isoformat(),
        'generated_at_text': finished_at.astimezone().strftime('%Y-%m-%d %H:%M:%S %Z'),
        'started_at': started_at.isoformat(),
        'started_at_text': started_at.astimezone().strftime('%Y-%m-%d %H:%M:%S %Z'),
        'duration_ms': duration_ms,
        'duration_seconds': duration_seconds,
        'duration_text': f'{duration_seconds:.3f}s',
    }


def main():
    parser = argparse.ArgumentParser(description='Compact statusboard voor command workflows')
    parser.add_argument('--json', action='store_true', help='geef JSON-output')
    parser.add_argument('--preview', action='store_true', help='toon korte preview van de laatste mail in tekstoutput')
    parser.add_argument('--reference-ms', type=int, help='gebruik deze epoch-millis als referentietijd voor deterministische AI-briefing-statuschecks')
    args = parser.parse_args()

    started_at = datetime.now(timezone.utc)
    started_monotonic = monotonic()
    data = run_brief_json(reference_ms=args.reference_ms)
    finished_at = datetime.now(timezone.utc)
    duration_ms = int(round((monotonic() - started_monotonic) * 1000))
    if args.json:
        print(json.dumps({
            **data,
            **build_run_metadata(started_at=started_at, finished_at=finished_at, duration_ms=duration_ms),
        }, ensure_ascii=False, indent=2))
    else:
        print(render_text(data, show_preview=args.preview))


if __name__ == '__main__':
    try:
        signal.signal(signal.SIGPIPE, signal.SIG_DFL)
    except (AttributeError, ValueError):
        pass
    try:
        main()
    except BrokenPipeError:
        raise SystemExit(0)
