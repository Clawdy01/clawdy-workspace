#!/usr/bin/env python3
import argparse
import json
import shlex
import subprocess
from pathlib import Path

from mail_heuristics import format_next_step_candidate_hint

ROOT = Path('/home/clawdy/.openclaw/workspace')
SCRIPTS = ROOT / 'scripts'
MAIL_FOCUS = SCRIPTS / 'mail-focus.py'
MAIL_TRIAGE = SCRIPTS / 'mail-triage.py'
MAIL_THREAD = SCRIPTS / 'mail-thread.py'


def run_json(command, default=None, timeout=20):
    try:
        proc = subprocess.run(
            command,
            cwd=ROOT,
            capture_output=True,
            text=True,
            check=False,
            timeout=timeout,
        )
    except subprocess.TimeoutExpired:
        return default
    if proc.returncode != 0:
        return default
    try:
        return json.loads(proc.stdout)
    except Exception:
        return default


def shell_join(parts):
    return ' '.join(shlex.quote(str(part)) for part in parts)


def build_thread_command(group, include_draft=False):
    args = ['python3', 'scripts/mail-dispatch.py', 'thread']
    latest_uid = (group or {}).get('latest_uid')
    sender = (group or {}).get('sender_email') or (group or {}).get('sender') or (group or {}).get('from')
    action = (group or {}).get('action_hint')
    if latest_uid is not None:
        args += ['--uid', str(latest_uid)]
    if sender:
        args += ['--sender', sender]
    if action:
        args += ['--action', action]
    args += ['--messages', '5']
    if include_draft:
        args.append('--draft')
    return shell_join(args)


def build_codes_command(group):
    args = ['python3', 'scripts/mail-dispatch.py', 'codes']
    sender = (group or {}).get('sender') or (group or {}).get('from')
    if sender:
        args += ['--sender', sender]
    return shell_join(args)


def build_focus_command(include_draft=False):
    args = ['python3', 'scripts/mail-dispatch.py', 'focus']
    if include_draft:
        args.append('--draft')
    return shell_join(args)


def load_thread_review(group):
    if not group:
        return {}
    command = ['python3', str(MAIL_THREAD), '--json', '--draft', '--messages', '5']
    latest_uid = group.get('latest_uid')
    sender = group.get('sender_email') or group.get('sender') or group.get('from')
    action = group.get('action_hint')
    if latest_uid is not None:
        command += ['--uid', str(latest_uid)]
    if sender:
        command += ['--sender', sender]
    if action:
        command += ['--action', action]
    return run_json(command, default={}) or {}


def group_score(group, prefer_current=False):
    group = group or {}
    score = 0
    if group.get('attention_now'):
        score += 100
    if group.get('urgency') == 'high':
        score += 30
    elif group.get('urgency') == 'medium':
        score += 15
    if group.get('action_hint') and group.get('action_hint') != 'code gebruiken':
        score += 12
    if group.get('security_alert_summary'):
        score += 10
    if group.get('count'):
        score += min(int(group.get('count', 0)), 10)
    if prefer_current and not group.get('attention_now'):
        score -= 25
    if group.get('stale_attention'):
        score -= 8
    score += int(group.get('latest_date_ts') or 0) / 1_000_000_000
    return score


def pick_best_group(groups, *, skip_code=False, prefer_current=False):
    ranked = rank_groups(groups, skip_code=skip_code, prefer_current=prefer_current)
    return ranked[0] if ranked else None


def rank_groups(groups, *, skip_code=False, prefer_current=False):
    groups = list(groups or [])
    if skip_code:
        filtered = [group for group in groups if group.get('action_hint') != 'code gebruiken']
        if filtered:
            groups = filtered
    return sorted(groups, key=lambda item: group_score(item, prefer_current=prefer_current), reverse=True)


def candidate_key(candidate):
    focus = candidate.get('focus') or {}
    group = candidate.get('selected_group') or {}
    if focus.get('uid') is not None:
        return ('focus', focus.get('uid'))
    return (
        candidate.get('recommended_route'),
        group.get('latest_uid'),
        group.get('action_hint'),
        group.get('sender_email') or group.get('sender') or group.get('from'),
    )


def summarize_candidate(candidate):
    focus = candidate.get('focus') or {}
    group = candidate.get('selected_group') or {}
    draft = candidate.get('focus_draft') or candidate.get('selected_draft') or {}
    item = focus or group
    review_only = bool(candidate.get('review_only'))
    return {
        'recommended_route': candidate.get('recommended_route'),
        'recommended_command': candidate.get('recommended_command'),
        'reason': candidate.get('reason'),
        'review_only': review_only,
        'has_draft': bool(draft),
        'focus': focus or None,
        'selected_group': group or None,
        'selected_draft': draft or None,
        'label': item.get('from') or item.get('sender') or item.get('latest_from'),
        'subject': item.get('subject') or item.get('latest_subject'),
        'action_hint': item.get('action_hint'),
        'age_hint': item.get('age_hint') or item.get('latest_age_hint'),
        'stale_attention': item.get('stale_attention'),
        'security_alert_summary': item.get('security_alert_summary'),
        'count': item.get('count') or item.get('message_count') or 1,
    }


def make_focus_candidate(focus_item, focus_draft):
    if not focus_item:
        return None
    return {
        'recommended_route': 'review-draft' if focus_draft else 'review-focus',
        'recommended_command': build_focus_command(include_draft=bool(focus_draft)),
        'reason': 'er is een duidelijke mail-focus' + (' met bestaand conceptantwoord' if focus_draft else ''),
        'review_only': False,
        'focus': focus_item,
        'focus_draft': focus_draft or None,
        'selected_group': None,
        'selected_draft': None,
    }


def make_group_candidate(group, route_name, reason, *, review_only=False):
    if not group:
        return None
    return {
        'recommended_route': route_name,
        'recommended_command': build_thread_command(group, include_draft=False),
        'reason': reason,
        'review_only': review_only,
        'focus': None,
        'focus_draft': None,
        'selected_group': group,
        'selected_draft': None,
        'thread_review': None,
    }


def make_codes_candidate(group):
    if not group:
        return None
    return {
        'recommended_route': 'check-codes',
        'recommended_command': build_codes_command(group),
        'reason': 'de resterende hoge mail lijkt vooral verificatiecode-verkeer',
        'review_only': bool(group.get('stale_attention')),
        'focus': None,
        'focus_draft': None,
        'selected_group': group,
        'selected_draft': None,
        'thread_review': None,
    }


def enrich_group_candidate(candidate):
    if not candidate:
        return candidate
    group = candidate.get('selected_group') or {}
    route = candidate.get('recommended_route') or ''
    if not group or route.startswith('check-codes'):
        return candidate
    thread_review = candidate.get('thread_review')
    if thread_review is None:
        thread_review = load_thread_review(group)
        candidate['thread_review'] = thread_review
    draft = (thread_review or {}).get('draft') or None
    base_route = route[:-6] if route.endswith('-draft') else route
    candidate['selected_draft'] = draft
    candidate['recommended_route'] = f'{base_route}-draft' if draft else base_route
    candidate['recommended_command'] = build_thread_command(group, include_draft=bool(draft))
    base_reason = candidate.get('reason') or ''
    draft_suffix = ' en er ligt al een concept klaar'
    if draft:
        if not base_reason.endswith(draft_suffix):
            candidate['reason'] = base_reason + draft_suffix
    elif base_reason.endswith(draft_suffix):
        candidate['reason'] = base_reason[:-len(draft_suffix)]
    return candidate


def build_summary(limit=1):
    limit = max(1, min(limit, 10))
    focus = run_json(['python3', str(MAIL_FOCUS), '--json', '-n', '5'], default={}) or {}
    current = run_json(
        ['python3', str(MAIL_TRIAGE), '--json', '--all', '--current-only', '--clusters', '-n', '5', '--search-limit', '50'],
        default={},
    ) or {}
    high = run_json(
        ['python3', str(MAIL_TRIAGE), '--json', '--all', '--high-only', '--clusters', '-n', '5', '--search-limit', '50'],
        default={},
    ) or {}

    focus_item = focus.get('focus') or {}
    focus_draft = focus.get('draft') or {}
    current_groups = current.get('groups') or current.get('items') or []
    high_groups = high.get('groups') or high.get('items') or []

    candidates = []
    seen = set()

    def add_candidate(candidate):
        if not candidate:
            return
        key = candidate_key(candidate)
        if key in seen:
            return
        seen.add(key)
        candidates.append(candidate)

    add_candidate(make_focus_candidate(focus_item, focus_draft))

    for group in rank_groups(current_groups, skip_code=True, prefer_current=True)[:limit]:
        add_candidate(make_group_candidate(
            group,
            'current-thread',
            'er is een actuele mailcluster die nu aandacht vraagt',
            review_only=False,
        ))

    for group in rank_groups(high_groups, skip_code=True)[:limit]:
        add_candidate(make_group_candidate(
            group,
            'stale-followup',
            'er is geen actuele mail, maar wel een recente belangrijke follow-up die waarschijnlijk nog review verdient',
            review_only=True,
        ))

    code_groups = [group for group in rank_groups(high_groups, skip_code=False) if group.get('action_hint') == 'code gebruiken']
    if code_groups:
        add_candidate(make_codes_candidate(code_groups[0]))

    for candidate in candidates[:limit]:
        enrich_group_candidate(candidate)

    selected = candidates[0] if candidates else None
    selected_summary = summarize_candidate(selected) if selected else {}
    alternative_summaries = [summarize_candidate(candidate) for candidate in candidates[:limit]]

    if not selected:
        selected_summary = {
            'recommended_route': 'noop',
            'recommended_command': None,
            'reason': 'geen duidelijke mail-vervolgstap',
            'focus': None,
            'selected_group': None,
            'selected_draft': None,
        }

    review_only = bool(selected_summary.get('review_only'))
    return {
        'focus_scope': focus.get('scope'),
        'focus': focus_item or None,
        'focus_draft': focus_draft or None,
        'current_group_count': current.get('group_count', 0),
        'current_attention_now_count': current.get('attention_now_count', 0),
        'high_group_count': high.get('group_count', 0),
        'high_attention_now_count': high.get('attention_now_count', 0),
        'high_stale_attention_count': high.get('stale_attention_count', 0),
        'recommended_route': selected_summary.get('recommended_route', 'noop'),
        'recommended_command': selected_summary.get('recommended_command'),
        'reason': selected_summary.get('reason', 'geen duidelijke mail-vervolgstap'),
        'review_only': review_only,
        'needs_attention_now': bool(selected_summary) and selected_summary.get('recommended_route') != 'noop' and not review_only,
        'selected_group': selected_summary.get('selected_group'),
        'selected_draft': selected_summary.get('selected_draft'),
        'selected_focus': selected_summary.get('focus'),
        'candidate_count': len(candidates),
        'candidates': alternative_summaries,
    }


def render_text(summary, show_alternatives=False):
    lines = ['Mail next step']
    action_mode = 'nu' if summary.get('needs_attention_now') else 'review'
    lines.append(
        f"- next={summary.get('recommended_route')}, mode={action_mode}, reason={summary.get('reason')}"
    )
    lines.append(
        f"- current_groups={summary.get('current_group_count')}, current_attention={summary.get('current_attention_now_count')}, high_groups={summary.get('high_group_count')}, stale_high={summary.get('high_stale_attention_count')}"
    )
    focus = summary.get('selected_focus') or summary.get('focus') or {}
    if focus:
        draft_hint = ' [concept klaar]' if summary.get('focus_draft') else ''
        lines.append(
            f"- focus={focus.get('from')} — {focus.get('subject')} [{focus.get('action_hint') or 'ter info'}], urgency={focus.get('urgency')}, age={focus.get('age_hint')}{draft_hint}"
        )

    candidates = summary.get('candidates') or []
    selected_candidate = candidates[0] if candidates else {}
    selected = summary.get('selected_group') or {}
    if selected_candidate:
        hint = format_next_step_candidate_hint(selected_candidate, include_age=True)
        if hint:
            prefix = '- selected-stale=' if selected_candidate.get('stale_attention') else '- selected='
            lines.append(f"{prefix}{hint}")
    elif selected:
        prefix = '- selected-stale=' if selected.get('stale_attention') else '- selected='
        lines.append(
            f"{prefix}{selected.get('sender') or selected.get('from')} — {selected.get('latest_subject')} [{selected.get('action_hint')}] x{selected.get('count')} ({selected.get('latest_age_hint')})"
        )

    if summary.get('recommended_command'):
        command_label = 'review-command' if summary.get('review_only') or (selected and selected.get('stale_attention')) else 'command'
        lines.append(f"- {command_label}={summary.get('recommended_command')}")
    if show_alternatives and len(candidates) > 1:
        for index, candidate in enumerate(candidates[1:], start=1):
            hint = format_next_step_candidate_hint(candidate, include_age=True) or 'onbekend'
            line = f"- alt{index}={hint}"
            if candidate.get('recommended_command'):
                alt_command_label = 'review-command' if candidate.get('review_only') or candidate.get('stale_attention') else 'command'
                line += f" | {alt_command_label}={candidate.get('recommended_command')}"
            lines.append(line)
    return '\n'.join(lines)


def main():
    parser = argparse.ArgumentParser(description='Bepaal de volgende nuttige stap in de mail-workflow')
    parser.add_argument('--json', action='store_true')
    parser.add_argument('-n', '--limit', type=int, default=1, help='hoeveel vervolgstappen/alternatieven tonen')
    parser.add_argument('--draft', action='store_true', help='toon bij tekstoutput ook meteen het concept als dat voor de gekozen stap bestaat')
    args = parser.parse_args()

    summary = build_summary(limit=args.limit)
    if args.json:
        print(json.dumps(summary, ensure_ascii=False, indent=2))
    else:
        text = render_text(summary, show_alternatives=args.limit > 1)
        if args.draft:
            draft = (summary.get('focus_draft') or summary.get('selected_draft') or {}).get('draft')
            if draft:
                text += f"\n- draft={draft}"
        print(text)


if __name__ == '__main__':
    main()
