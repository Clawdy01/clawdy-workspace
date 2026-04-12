from mail_heuristics import extract_deadline_hint, reply_needed, should_offer_reply_draft


def draft_for_message(msg):
    sender = msg.get('sender_name') or msg.get('sender_display') or msg.get('from') or 'daar'
    subject = msg.get('subject') or ''
    action = msg.get('action_hint') or 'ter info'
    preview = (msg.get('preview') or '').strip()
    deadline_hint = msg.get('deadline_hint') or extract_deadline_hint(msg)

    if not should_offer_reply_draft(msg):
        return None

    if action == 'agenda checken':
        draft = (
            f"Hoi {sender}, dank je. Ik heb je bericht over '{subject}' gezien. "
            "Ik check even de agenda en kom daarna bij je terug."
        )
    elif action == 'account activeren':
        draft = (
            f"Hoi {sender}, dank je. Ik heb de activatiemail over '{subject}' gezien "
            "en rond die accountstap zo af."
        )
    elif action == 'financieel checken':
        draft = (
            f"Hoi {sender}, dank je voor het doorsturen. Ik heb het ontvangen en check de details van '{subject}' even intern."
        )
    elif action == 'security checken':
        draft = (
            f"Hoi {sender}, dank je. Ik heb de melding over '{subject}' gezien en controleer dit eerst even zorgvuldig."
        )
    elif action == 'deadline checken':
        draft = (
            f"Hoi {sender}, dank je. Ik heb '{subject}' gezien"
            + (f" met tijdsdruk rond '{deadline_hint}'" if deadline_hint else '')
            + ". Ik pak dit zo snel mogelijk op en kom direct bij je terug zodra ik iets concreets heb."
        )
    elif reply_needed(msg):
        draft = (
            f"Hoi {sender}, dank je voor je mail. Ik heb '{subject}' gezien"
            + (f" en je vraag over '{preview[:60]}'" if preview else '')
            + ". Ik kom hier zo snel mogelijk op terug."
        )
    else:
        draft = f"Hoi {sender}, dank je voor je bericht over '{subject}'. Ik heb het ontvangen."

    return {
        'uid': msg.get('uid'),
        'sender': msg.get('sender_display') or msg.get('from') or 'onbekend',
        'subject': subject or '(geen onderwerp)',
        'action_hint': action,
        'reply_needed': reply_needed(msg),
        'deadline_hint': deadline_hint,
        'draft': draft,
    }


def _thread_draft_score(msg):
    score = 0
    if msg.get('reply_needed') or reply_needed(msg):
        score += 60
    if msg.get('deadline_hint') or extract_deadline_hint(msg):
        score += 30
    if msg.get('urgency') == 'high':
        score += 20
    if msg.get('attention_now'):
        score += 10
    action = msg.get('action_hint') or 'ter info'
    if action not in {'ter info', 'code gebruiken'}:
        score += 10
    score += int(msg.get('date_ts') or 0)
    return score


def draft_for_thread(thread):
    messages = [msg for msg in (thread or {}).get('messages') or [] if should_offer_reply_draft(msg)]
    if not messages:
        return None
    selected = max(messages, key=_thread_draft_score)
    return draft_for_message(selected)
