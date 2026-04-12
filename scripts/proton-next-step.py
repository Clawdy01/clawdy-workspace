#!/usr/bin/env python3
import argparse
import json
import subprocess
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path('/home/clawdy/.openclaw/workspace')
PROTON_STATUS = ROOT / 'scripts' / 'proton-status-summary.py'
PROTON_VERIFY = ROOT / 'scripts' / 'proton-verification-status.py'
STALE_AFTER_SECONDS = 900
RECENT_REGRESSION_ARTIFACT_SECONDS = 6 * 60 * 60


def run_json(cmd, default=None):
    try:
        proc = subprocess.run(cmd, cwd=ROOT, capture_output=True, text=True, check=False, timeout=20)
    except subprocess.TimeoutExpired:
        return default
    if proc.returncode != 0:
        return default
    try:
        return json.loads(proc.stdout)
    except Exception:
        return default


def iso_age_seconds(value):
    if not value:
        return None
    try:
        dt = datetime.fromisoformat(value.replace('Z', '+00:00'))
    except Exception:
        return None
    return max(0, int((datetime.now(timezone.utc) - dt.astimezone(timezone.utc)).total_seconds()))


def build_summary():
    status = run_json(['python3', str(PROTON_STATUS), '--json'], default={}) or {}
    verify = run_json(['python3', str(PROTON_VERIFY), '--json'], default={}) or {}

    start = status.get('start') or {}
    route = status.get('route') or {}
    submit_ready = status.get('submit_ready') or {}

    start_age = iso_age_seconds(start.get('checked_at'))
    route_age = iso_age_seconds(route.get('checked_at'))
    ready_age = iso_age_seconds(submit_ready.get('checked_at'))
    verify_age = verify.get('age_seconds')
    freshest_age = min([age for age in [start_age, route_age, ready_age] if age is not None], default=None)
    stale = freshest_age is None or freshest_age > STALE_AFTER_SECONDS
    verification_stale = verify.get('stale') if verify.get('stale') is not None else (verify_age is None or verify_age > STALE_AFTER_SECONDS)
    manual_boundary = bool(verify.get('account_created')) or bool(verify.get('recovery_kit_ready'))

    phase = 'unknown'
    if route.get('reached_password_step'):
        phase = 'password-step'
    elif start.get('signup_visible'):
        phase = 'start-page'

    recommended_route = 'noop'
    command = None
    reason = 'geen duidelijke vervolgstap'

    regression_suspected = False if manual_boundary else bool(status.get('regression_suspected'))

    recent_regression_artifacts = route_age is not None and route_age <= RECENT_REGRESSION_ARTIFACT_SECONDS

    verification_in_progress = bool(verify.get('verification_screen')) and bool(verify.get('submit_ready'))

    if start.get('blocked'):
        recommended_route = 'investigate-blocker'
        reason = 'Proton lijkt geblokkeerd of toont een blokkade-signaal'
    elif verify.get('recommended_action') == 'account-created':
        recommended_route = 'account-created'
        command = 'python3 scripts/web-automation-dispatch.py proton-manual-finish'
        reason = 'de signup-flow heeft de Recovery Kit stap bereikt, dus het Proton-account lijkt aangemaakt en vraagt nu vooral om bewuste afronding/opslag van recovery-materiaal'
        stale = False
        verification_stale = False
    elif verify.get('recommended_action') == 'password-setup-ready':
        recommended_route = 'continue-password-setup'
        command = 'python3 scripts/web-automation-dispatch.py continue-password-setup --json'
        reason = 'de verificatiecode lijkt geaccepteerd en de flow staat weer bij het password-setup deel, dus de veilige external-email finish kan dat stuk nu bevestigen en verder trekken'
    elif verify.get('recommended_action') == 'refresh' and verification_in_progress:
        recommended_route = 'proton-verify-refresh'
        command = 'python3 scripts/web-automation-dispatch.py proton-verify --refresh'
        reason = 'de flow zit al in human verification, maar die status is verouderd en moet eerst ververst worden'
    elif verify.get('recommended_action') == 'request-code' and verification_in_progress:
        recommended_route = 'proton-request-code'
        command = 'python3 scripts/web-automation-dispatch.py proton-request-code'
        reason = 'human verification staat al klaar voor e-mailverificatie, maar er is nog geen code aangevraagd'
    elif verify.get('recommended_action') == 'wait-for-mail' and verification_in_progress:
        recommended_route = 'wait-for-mail'
        reason = 'de flow staat al in human verification en wacht op verificatiemail'
    elif verify.get('recommended_action') == 'use-code' and verification_in_progress:
        recommended_route = 'proton-use-code'
        command = 'python3 scripts/web-automation-dispatch.py proton-use-code'
        reason = 'de flow staat al in human verification en er lijkt een bruikbare verificatiecode in mail te staan'
    elif verify.get('recommended_action') == 'refresh-submit':
        recommended_route = 'manual-submit-decision'
        command = 'python3 scripts/web-automation-dispatch.py proton-submit-probe clawdy01 --submit'
        reason = 'flow staat submit-ready; echte submit naar human verification is nu een bewuste keuze'
    elif phase == 'start-page' and regression_suspected and recent_regression_artifacts:
        recommended_route = 'investigate-password-regression'
        command = 'python3 scripts/web-automation-dispatch.py investigate-password-regression --json'
        reason = 'recente artifacts tonen dat username-propagatie nog werkt, maar de password-step niet meer stabiel verschijnt; gerichte regressiediagnose is nu nuttiger dan een volledige refresh'
    elif stale:
        recommended_route = 'proton-refresh'
        command = 'python3 scripts/web-automation-dispatch.py proton-refresh'
        reason = 'observability-artifacts zijn verouderd of ontbreken'
    elif phase == 'start-page' and regression_suspected:
        recommended_route = 'investigate-password-regression'
        command = 'python3 scripts/web-automation-dispatch.py investigate-password-regression --refresh'
        reason = 'username-propagatie werkt nog, maar de password-step verschijnt niet meer, wat wijst op een Proton-flow regressie of selectorverandering'
    elif phase == 'start-page' and not route.get('reached_password_step'):
        recommended_route = 'proton-password-step'
        command = 'python3 scripts/web-automation-dispatch.py proton-password-step'
        reason = 'signup-start is zichtbaar, maar password-step is nog niet bevestigd'
    elif phase == 'password-step' and not submit_ready.get('submit_ready'):
        recommended_route = 'proton-submit-ready'
        command = 'python3 scripts/web-automation-dispatch.py proton-submit-ready'
        reason = 'password-step is bereikt, maar pre-submit staat nog niet compleet'
    elif verify.get('recommended_action') == 'refresh' or (verification_stale and verify.get('recommended_action') in {'wait-for-mail', 'use-code', 'refresh-submit'}):
        recommended_route = 'proton-verify-refresh'
        command = 'python3 scripts/web-automation-dispatch.py proton-verify --refresh'
        reason = 'verification-status is verouderd en moet eerst ververst worden'
    elif verify.get('recommended_action') == 'request-code':
        recommended_route = 'proton-request-code'
        command = 'python3 scripts/web-automation-dispatch.py proton-request-code'
        reason = 'human verification staat klaar voor e-mailverificatie, maar er is nog geen code aangevraagd'
    elif verify.get('recommended_action') == 'wait-for-mail':
        recommended_route = 'wait-for-mail'
        reason = 'human verification wacht op verificatiemail'
    elif verify.get('recommended_action') == 'use-code':
        recommended_route = 'proton-use-code'
        command = 'python3 scripts/web-automation-dispatch.py proton-use-code'
        reason = 'er lijkt een verificatiecode in de mailbox te staan'

    return {
        'phase': phase,
        'stale': stale,
        'freshest_age_seconds': freshest_age,
        'route_age_seconds': route_age,
        'status': status,
        'verification': verify,
        'verification_stale': verification_stale,
        'manual_boundary': manual_boundary,
        'recommended_route': recommended_route,
        'recommended_command': command,
        'reason': reason,
        'regression_suspected': regression_suspected,
    }


def render_text(summary):
    lines = ['Proton next step']
    lines.append(
        f"- phase={summary.get('phase')}, stale={summary.get('stale')}, age={summary.get('freshest_age_seconds')}"
    )
    lines.append(
        f"- next={summary.get('recommended_route')}, reason={summary.get('reason')}"
    )
    lines.append(f"- regression_suspected={summary.get('regression_suspected')}, manual_boundary={summary.get('manual_boundary')}")
    if summary.get('recommended_command'):
        lines.append(f"- command={summary.get('recommended_command')}")
    verification = summary.get('verification') or {}
    lines.append(
        f"- verify={verification.get('recommended_action')}, stale={summary.get('verification_stale')}, mail_matches={verification.get('verification_mail_matches')}, used_code={verification.get('latest_used_code')}, account_created={verification.get('account_created')}"
    )
    return '\n'.join(lines)


def main():
    parser = argparse.ArgumentParser(description='Bepaal de volgende nuttige Proton automation stap')
    parser.add_argument('--json', action='store_true')
    args = parser.parse_args()

    summary = build_summary()
    if args.json:
        print(json.dumps(summary, ensure_ascii=False, indent=2))
    else:
        print(render_text(summary))


if __name__ == '__main__':
    main()
