#!/usr/bin/env python3
import argparse
import json
import subprocess
from pathlib import Path

from mail_heuristics import format_next_step_candidate_hint

ROOT = Path('/home/clawdy/.openclaw/workspace')
SCRIPTS = ROOT / 'scripts'
MAIL_NEXT_STEP = SCRIPTS / 'mail-next-step.py'
MAIL_THREAD = SCRIPTS / 'mail-thread.py'
MAIL_CODES = SCRIPTS / 'mail-verification-codes.py'


def run_json(command, label, timeout=30):
    proc = subprocess.run(
        command,
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=False,
        timeout=timeout,
    )
    if proc.returncode != 0:
        raise SystemExit(proc.stderr.strip() or proc.stdout.strip() or f'{label} failed: {proc.returncode}')
    try:
        return json.loads(proc.stdout)
    except json.JSONDecodeError as exc:
        raise SystemExit(f'invalid json from {label}: {exc}')


def build_thread_command(summary, *, messages=8, preview=False, meaningful=False):
    command = ['python3', str(MAIL_THREAD), '--json', '--draft', '--messages', str(messages)]
    if preview:
        command.append('--preview')
    if meaningful:
        command.append('--meaningful')

    focus = summary.get('selected_focus') or summary.get('focus') or {}
    group = summary.get('selected_group') or {}

    uid = focus.get('uid')
    sender = focus.get('sender_email') or focus.get('from') or group.get('sender_email') or group.get('sender') or group.get('from')
    subject = focus.get('subject') or group.get('latest_subject') or group.get('subject')
    action = focus.get('action_hint') or group.get('action_hint')

    if uid is None:
        uid = group.get('latest_uid')
    if uid is not None:
        command += ['--uid', str(uid)]
    if sender:
        command += ['--sender', sender]
    if action:
        command += ['--action', action]
    elif subject:
        command += ['--subject', subject]
    return command


def build_codes_command(summary):
    command = ['python3', str(MAIL_CODES), '--json']
    focus = summary.get('selected_focus') or summary.get('focus') or {}
    group = summary.get('selected_group') or {}
    sender = focus.get('sender_email') or focus.get('from') or group.get('sender_email') or group.get('sender') or group.get('from')
    subject = focus.get('subject') or group.get('latest_subject') or group.get('subject')
    if sender:
        command += ['--sender', sender]
    if subject:
        command += ['--subject', subject]
    return command


def pick_candidate(summary, candidate_index):
    candidates = summary.get('candidates') or []
    if not candidates:
        return None, None
    candidate_index = max(1, candidate_index)
    if candidate_index > len(candidates):
        return None, len(candidates)
    return candidates[candidate_index - 1], len(candidates)


def build_payload(limit=3, messages=8, preview=False, meaningful=False, candidate_index=1):
    effective_limit = max(limit, candidate_index)
    summary = run_json(['python3', str(MAIL_NEXT_STEP), '--json', '--limit', str(effective_limit)], 'mail-next-step') or {}
    if summary.get('recommended_route') == 'noop':
        return {
            'summary': summary,
            'selected_candidate': None,
            'candidate_index': candidate_index,
            'candidate_count': 0,
            'thread': None,
            'draft': None,
        }

    selected_candidate, candidate_count = pick_candidate(summary, candidate_index)
    if selected_candidate is None:
        raise SystemExit(f'candidate {candidate_index} bestaat niet, er zijn {candidate_count or 0} kandidaat/kandidaten')

    route = selected_candidate.get('recommended_route') or ''
    display_command = selected_candidate.get('recommended_command')
    payload = {
        'summary': summary,
        'selected_candidate': selected_candidate,
        'candidate_index': candidate_index,
        'candidate_count': candidate_count,
        'thread': None,
        'draft': None,
        'matched_count': None,
        'thread_command': display_command,
        'review_data_type': 'thread',
        'codes': None,
    }

    if route.startswith('check-codes'):
        codes_payload = run_json(build_codes_command(selected_candidate), 'mail-verification-codes') or []
        payload.update({
            'review_data_type': 'codes',
            'codes': codes_payload,
        })
        return payload

    thread_payload = run_json(
        build_thread_command(selected_candidate, messages=messages, preview=preview, meaningful=meaningful),
        'mail-thread',
    ) or {}

    payload.update({
        'thread': thread_payload.get('thread'),
        'draft': thread_payload.get('draft'),
        'matched_count': thread_payload.get('filtered_thread_count'),
        'thread_command': display_command or thread_payload.get('command'),
    })
    return payload


def render_text(payload, *, show_preview=False, show_draft=False, alt_limit=2):
    summary = payload.get('summary') or {}
    selected_candidate = payload.get('selected_candidate') or {}
    if summary.get('recommended_route') == 'noop':
        return 'Geen duidelijke volgende mail-review.'

    route = selected_candidate.get('recommended_route') or summary.get('recommended_route')
    reason = selected_candidate.get('reason') or summary.get('reason')
    review_only = bool(selected_candidate.get('review_only'))
    candidate_index = payload.get('candidate_index') or 1
    candidate_count = payload.get('candidate_count') or len(summary.get('candidates') or [])

    lines = ['Mail review next']
    lines.append(f"- candidate={candidate_index}/{candidate_count}, route={route}, reason={reason}")
    display_command = (
        selected_candidate.get('recommended_command')
        or payload.get('thread_command')
        or summary.get('recommended_command')
    )
    if display_command:
        command_label = 'review-command' if review_only else 'next-command'
        lines.append(f"- {command_label}={display_command}")

    if payload.get('review_data_type') == 'codes':
        codes = payload.get('codes') or []
        selected_hint = format_next_step_candidate_hint(selected_candidate, include_age=True)
        if selected_hint:
            lines.append(f"- code-bron={selected_hint}")
        lines.append(f"- verificatiecodes={len(codes)}")
        for item in codes[:5]:
            code_text = ', '.join(item.get('codes') or []) if item.get('codes') else 'geen code gevonden'
            lines.append(
                f"- #{item.get('uid')} {item.get('from')}: {item.get('subject')} [{code_text}]"
            )
        remaining = len(codes) - min(len(codes), 5)
        if remaining > 0:
            lines.append(f"- +{remaining} oudere code-mail(s)")
    else:
        thread = payload.get('thread') or {}
        if thread:
            stale = ' [niet actueel]' if thread.get('stale_attention') else ''
            security = f" {{{thread.get('security_alert_summary')}}}" if thread.get('security_alert_summary') else ''
            variant_suffix = f", +{thread.get('subject_variant_count', 0) - 1} variant(en)" if (thread.get('subject_variant_count', 0) or 0) > 1 else ''
            time_bits = [bit for bit in [thread.get('latest_age_hint'), thread.get('span_hint')] if bit]
            time_suffix = f", {', '.join(time_bits)}" if time_bits else ''
            lines.append(
                f"- thread={thread.get('subject')} ({thread.get('message_count')}x{variant_suffix}{time_suffix}) [{thread.get('action_hint') or 'ter info'}]{security}{stale}"
            )
            messages = thread.get('messages') or []
            for item in messages[:max(1, min(messages.__len__(), 5))]:
                age = f" ({item.get('age_hint')})" if item.get('age_hint') else ''
                preview = f" — {item.get('preview')[:120]}" if show_preview and item.get('preview') else ''
                stale_item = ' [niet actueel]' if item.get('stale_attention') else ''
                lines.append(
                    f"- #{item.get('uid')} {item.get('from')}: {item.get('subject')} [{item.get('action_hint') or 'ter info'}]{age}{stale_item}{preview}"
                )
                for link in (item.get('action_links') or [])[:1]:
                    lines.append(f"  link: {link}")
            remaining = len(messages) - min(len(messages), 5)
            if remaining > 0:
                lines.append(f"- +{remaining} oudere mail(s)")
            if thread.get('action_links'):
                lines.append(f"- actielinks={', '.join((thread.get('action_links') or [])[:2])}")

    candidates = summary.get('candidates') or []
    shown = 0
    for index, candidate in enumerate(candidates, start=1):
        if index == candidate_index:
            continue
        alt_hint = format_next_step_candidate_hint(candidate, include_age=True) or 'onbekend'
        alt_number = shown + 1
        line = f"- alt{alt_number}={alt_hint}"
        if candidate.get('recommended_command'):
            alt_command_label = 'review-command' if candidate.get('review_only') or candidate.get('stale_attention') else 'command'
            line += f" | {alt_command_label}={candidate.get('recommended_command')}"
        lines.append(line)
        shown += 1
        if shown >= max(0, alt_limit):
            break

    draft = payload.get('draft') or {}
    if show_draft and draft.get('draft'):
        lines.append('')
        lines.append(f"Concept: {draft.get('draft')}")
    return '\n'.join(lines)


def main():
    parser = argparse.ArgumentParser(description='Open direct de aanbevolen volgende mailthread met context en optioneel concept')
    parser.add_argument('--json', action='store_true')
    parser.add_argument('-n', '--limit', type=int, default=3, help='hoeveel next-step kandidaten meenemen voor alternatieven')
    parser.add_argument('--messages', type=int, default=5, help='hoeveel berichten uit de gekozen thread tonen')
    parser.add_argument('--preview', action='store_true', help='toon previews per bericht')
    parser.add_argument('--draft', action='store_true', help='toon bestaand concept als dat er is')
    parser.add_argument('--meaningful', action='store_true', help='forceer betekenisvolle threadselectie bij de review lookup')
    parser.add_argument('--candidate', type=int, default=1, help='open kandidaat N uit mail-next-step in plaats van altijd de eerste')
    args = parser.parse_args()

    payload = build_payload(
        limit=max(1, min(args.limit, 10)),
        messages=max(1, min(args.messages, 20)),
        preview=args.preview,
        meaningful=args.meaningful,
        candidate_index=max(1, min(args.candidate, 10)),
    )
    if args.json:
        print(json.dumps(payload, ensure_ascii=False, indent=2))
    else:
        print(render_text(payload, show_preview=args.preview, show_draft=args.draft, alt_limit=max(0, args.limit - 1)))


if __name__ == '__main__':
    main()
