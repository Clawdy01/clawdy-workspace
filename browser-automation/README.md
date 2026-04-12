# Browser Automation

Small Playwright-based helpers for headless web flows.

## Current tools

### Generic

- `probe_page.js`
  - Opens a page in headless Chromium
  - Saves a screenshot and a JSON dump of visible text + interactive elements
  - Adds `checkedAt`, basic form metadata, optional `--slug <name>`, and optional `--session <name>` for reusable browser sessions
  - Useful for understanding JS-heavy signup/login flows before automating them

- `playwright_session.js`
  - Small helper for persistent Chromium sessions (default under `/tmp/openclaw-browser-sessions`, override via `OPENCLAW_BROWSER_SESSIONS_DIR`)
  - Reuses cookies/local browser state so repeated runs do not always look like a brand-new browser

### Proton flow

- `proton_probe_status.js`
  - Quick start-page probe for Proton signup
  - Confirms whether signup is visible and whether captcha/blocking is already present

- `proton_probe_iframe_email.js`
  - Confirms the visible username/email control is an iframe-backed challenge/proxy
  - Fills the visible iframe input and records propagation into hidden `#username`

- `proton_to_password_step.js`
  - Opens Proton signup
  - Fills the visible `Email address` iframe with a username
  - Submits the first step and verifies whether the password step is reached
  - Saves screenshot + JSON result in `browser-automation/out/`

- `proton_probe_password_step.js`
  - Maps the visible password step after the iframe/email step
  - Confirms the visible password controls and active focus

- `proton_to_submit_ready.js`
  - Opens Proton signup
  - Fills the visible `Email address` iframe and the password fields
  - Uses a strong generated password by default when no password is passed
  - Stops before the final signup submit, but records whether the form is submit-ready
  - Saves screenshot + JSON result in `browser-automation/out/`

- `proton_submit_probe.js`
  - Builds the Proton form all the way to the final submit step
  - Records pre-submit state by default
  - Can optionally do a real submit attempt with `--submit` to observe the final blocker screen
  - Saves screenshot + JSON result in `browser-automation/out/`

- `proton_human_verification.js`
  - Drives Proton to the Human Verification dialog after submit
  - Inspects available email/code inputs and buttons by default, without sending anything
  - Can optionally fill an external email and click `Get verification code` with `--email ... --send`
  - Can optionally attempt to fill a received verification code with `--code ... --verify`
  - Saves screenshot + JSON result in `browser-automation/out/`

### Derived helpers in `../scripts/`

- `../scripts/proton-status-summary.py`
  - Compact summary of the latest Proton probe outputs

- `../scripts/protonboard.py`
  - One compact Proton board with start-state, route-state, password-state, and the documented next step
  - Also exposed centrally via `../scripts/web-automation-dispatch.py proton-board`

- `../scripts/proton-next-step.py`
  - Combines Proton status + verification artifacts into one explicit recommended next route/command
  - Prefers a lightweight regression diagnosis when recent artifacts already show the username step works but the password transition regressed, instead of always forcing a full refresh first
  - Useful for resuming the flow without re-deriving the safest next action by hand
  - Also exposed centrally via `../scripts/web-automation-dispatch.py proton-next-step`

- `../scripts/proton-autopilot-safe.py`
  - Reads the current recommended Proton next step and executes the safe continuation automatically
  - Reuses the lighter non-refresh regression route when `proton-next-step` already has enough recent artifacts, which keeps heartbeat-style maintenance faster
  - Stops before risky/manual boundaries like the real final submit or waiting for a mail/code
  - Refreshes only explicitly managed non-Proton registry sites before considering Proton work, so one-off debug probes do not steal maintenance cycles
  - Also exposed centrally via `../scripts/web-automation-dispatch.py proton-autopilot-safe`

- `../scripts/web-automation-autopilot.py`
  - Picks one safe, meaningful maintenance step across managed site probes, desktop fallback, unmanaged stale artifact review, and Proton follow-up
  - Supports `--plan-only` to show the next autopilot step without executing it, which is useful for dashboards/boards
  - Plan output now also includes a compact target preview for both the current step and the predicted follow-up, so boards can show the actual queue instead of only a generic count
  - Supports `--adapter <name>` too, so maintenance can stay focused on one adapter like GitHub or Slack
  - Can switch from prune review to real `gio trash` cleanup with `--apply-prune` once managed site and desktop health are already operationally healthy
  - Useful for heartbeat-style background upkeep where clutter should disappear automatically without risking managed targets
  - Also exposed centrally via `../scripts/web-automation-dispatch.py autopilot`

- `../scripts/automation-board.py`
  - One compact board for artifacts, generic sites, desktop fallback, Proton flow state, and the next autopilot step
  - Uses autopilot planning mode, so it can show the recommended next action without mutating anything
  - Useful as a single observability/status entrypoint while the framework grows beyond one adapter
  - Supports `--configured-only`, `--adapter <name>`, `--slug <name>`, `--attention-only`, and `--stale-after <sec>` so the board can focus on one managed target or adapter instead of always showing the whole estate
  - Also exposed centrally via `../scripts/web-automation-dispatch.py automation-board`

- `../scripts/proton-verification-status.py`
  - Combines the latest Proton submit-probe result with mailbox lookup for verification codes
  - Useful once the flow reaches Human Verification by email
  - Also exposed centrally via `../scripts/web-automation-dispatch.py proton-verification-status`

- `../scripts/proton-human-verification-summary.py`
  - Compact summary of the latest human-verification dialog probe
  - Useful to confirm which email/code controls are currently visible

- `../scripts/proton-request-verification-code.py`
  - Reuses the saved mailbox address + Proton password to request a verification code from the Human Verification dialog
  - Gives the Proton signup case an explicit resumable step before waiting on mail
  - Also exposed centrally via `../scripts/web-automation-dispatch.py proton-request-code`

- `../scripts/proton-use-verification-code.py`
  - Pulls the latest Proton verification code from the mailbox and tries it in the Human Verification flow
  - Gives the Proton signup case a concrete resumable step once the verification mail arrives
  - Also exposed centrally via `../scripts/web-automation-dispatch.py proton-use-code`

- `../scripts/proton-manual-finish-summary.py`
  - Builds a compact handoff once Proton reaches the Recovery Kit or account-created boundary
  - Surfaces the used code, Recovery Kit state, and a short manual checklist so the automation can stop cleanly at the human-only step
  - Also exposed centrally via `../scripts/web-automation-dispatch.py proton-manual-finish`

- `../scripts/proton-refresh-safe.py`
  - Runs the safe Proton probe chain again
  - Refreshes the derived JSON artifacts
  - Prints the latest Proton status summary in text or JSON

- `../scripts/web-automation-dispatch.py`
  - Single dispatcher/catalog for web automation routes
  - Exposes DOM probes, desktop fallback, Proton status/password/refresh/submit-ready flows
  - Also provides route aliases and machine-readable route metadata via `catalog --json`
  - `desktop-probe` now accepts a reusable `--slug <name>` plus optional `--url <url>`, so named desktop-fallback targets can live next to DOM site probes instead of only one global `out-desktop`
  - `desktop-probe` and `refresh-desktop` can now also cap numbered screenshot history with `--keep-screenshots <n>`, so long-running observability targets do not grow forever while keeping the latest `desktop.png` plus a short breadcrumb trail
  - Includes `desktop-status`, which can now also focus on one named desktop target via `--slug` or `--outdir`, or on one configured adapter via `--adapter <name>`
  - Includes `stack-status`, which rolls DOM, desktop, artifact, and workflow state into one per-target view for adapter work and focused debugging
  - `autopilot` and `prune-unmanaged` can now also focus on one adapter via `--adapter <name>` for targeted maintenance and verification

- `../scripts/desktop-fallback-status.py`
  - Compact observability view for desktop fallback artifacts in `out-desktop*`
  - Reports screenshot/window-capture freshness, probe metadata freshness, last URL/duration/window count, default outdir health, and the exact refresh command when the fallback probe is stale or missing
  - Registry targets with `desktopEnabled` now also show up before their first outdir exists, so managed desktop fallback can be bootstrapped instead of staying invisible
  - Honors per-site `staleAfterSeconds` from `../state/web-automation-sites.json`, so slower-moving configured desktop targets do not flap unhealthy under the global default threshold
  - Can also inspect one named target directly with `--slug <name>` or `--outdir <dir>`, limit the view to managed registry targets with `--configured-only`, or zoom to one configured adapter via `--adapter <name>`, which pairs with the reusable registry-driven desktop flows
  - Useful to verify that the desktop layer itself is still usable before relying on it as the last-resort automation path

- `../scripts/web-automation-artifacts.py`
  - Compact artifact/observability overview across `browser-automation/out*`
  - Groups outputs by adapter, marks stale artifacts, and suggests the right refresh command per adapter
  - Reuses managed site-board context where possible, so configured generic probes inherit site-specific stale thresholds, adapter labels, and exact site-specific refresh commands instead of falling back to vague placeholders
  - Supports `--stale-after <sec>` to tune freshness thresholds for monitoring vs debugging, plus `--adapter <name>` to zoom in on one adapter without board noise
  - Also exposed centrally via `../scripts/web-automation-dispatch.py artifacts`

- `../scripts/web-automation-sites.py`
  - Turns generic `probe*.json` artifacts into a small site board with url/title/form signals per slug
  - Can also merge in optional registry entries from `../state/web-automation-sites.json`, so reusable site targets can exist even before the first probe artifact is created
  - Registry entries can optionally carry an adapter-specific `route` or explicit `refreshCommand`, so non-generic flows like Proton can still live on the same board with the right refresh action
  - Adds adapter-specific workflow overlays where available, so Proton can show terminal/manual-boundary states like `account-created` instead of looking perpetually unhealthy because an old start-page probe is stale
  - Surfaces a concrete handoff command for terminal/manual states, so Proton can point straight at `proton-manual-finish` instead of losing the next action when the flow is already complete enough for humans
  - Distinguishes managed registry sites from unmanaged/ad-hoc probe artifacts in the summary, so one-off debug probes do not blur real automation health
  - Supports `--configured-only`, `--slug <name>`, and `--attention-only` to focus the board on explicitly managed registry sites, a single reusable target, or only the sites that currently need action
  - Surfaces registry validation warnings inline, so bad routes or malformed saved metadata show up on the board instead of failing silently later
  - Useful for growing reusable site adapters beyond Proton, while keeping generic Playwright probes observable
  - Supports `--stale-after <sec>` and suggests the exact refresh command per stale or not-yet-probed site
  - Also exposed centrally via `../scripts/web-automation-dispatch.py sites`

- `../scripts/web-automation-stack-status.py`
  - Builds one focused stack view per target by combining `sites`, `artifacts`, and `desktop-status`
  - Useful when adapter work needs the full picture for one slug, instead of reading the broad global board plus three separate subviews
  - Supports `--slug`, `--adapter`, `--configured-only`, `--attention-only`, and a small `--artifact-preview` for recent breadcrumbs
  - Also exposed centrally via `../scripts/web-automation-dispatch.py stack-status`

- `../scripts/web-automation-selectors.py`
  - Turns the latest generic probe artifact into a compact list of visible, likely-useful controls with selector hints
  - Filters away hidden/noisy controls by default, while still allowing `--include-hidden` for debugging
  - Useful when building a new site adapter and you want likely ids, names, hrefs, labels, or placeholders without re-reading raw probe JSON
  - Also exposed centrally via `../scripts/web-automation-dispatch.py selectors`

- `../scripts/web-automation-site-registry.py`
  - Manages `../state/web-automation-sites.json` without hand-editing JSON
  - Supports listing, validating, upserting, promoting existing probe artifacts, and removing reusable site targets for adapters and refresh flows
  - `list` and `validate` can now also be filtered by `--slug`, `--adapter`, `--desktop-only`, or `--warnings-only`, which helps when growing or auditing one adapter at a time
  - Accepts generic URL-backed probes, but can also store route-only adapter entries when a site should refresh through a named flow instead of a direct URL probe
  - Generic probe-backed sites can also store `probeArgs` (for example a reusable `--session` name), so registry-driven refreshes can keep sticky browser state without custom wrapper scripts
  - Registry items can also opt into managed desktop fallback with `desktopEnabled`, which makes missing desktop targets visible and refreshable before the first desktop probe exists
  - Registry items can also store `desktopKeepScreenshots`, so named desktop fallback targets keep a short breadcrumb trail without every refresh command having to repeat `--keep-screenshots`
  - `promote --slug ...` can turn an existing unmanaged `probe-*.json` artifact into a managed registry entry, which is handy once a one-off probe becomes a real maintained target
  - Validates saved dispatch routes against the current dispatcher catalog, so broken registry entries show up before refresh-time
  - Supports optional per-site `staleAfterSeconds` overrides, so slower-moving targets can stay healthy without forcing the whole board to use a looser threshold
  - Useful when growing the web automation framework to new sites, while keeping refresh metadata consistent
  - Also exposed centrally via `../scripts/web-automation-dispatch.py site-registry`

- `../scripts/web-automation-refresh-sites.py`
  - Re-runs saved generic site probes from their stored slug/url metadata, so stale site observability can be refreshed in one command
  - Also picks up registry-backed sites from `../state/web-automation-sites.json`, which means a site can be declared once and then refreshed without hand-typing the URL again
  - Honors registry `route` or `refreshCommand` values, so site-specific adapters can refresh through the correct safe flow instead of being forced through the generic probe route
  - Respects site-level stale overrides from the registry, so refresh queues can prioritize the right targets instead of treating every site equally
  - Supports `--configured-only` so maintenance can focus on explicitly managed registry sites instead of every ad-hoc probe artifact
  - Supports `--plan-only`, which prints the exact queued refreshes and commands without mutating artifacts yet
  - Defaults to stale-only refresh, with optional `--slug`, `--all`, and `--max-sites`
  - Also exposed centrally via `../scripts/web-automation-dispatch.py refresh-sites`

- `../scripts/web-automation-refresh-stack.py`
  - Refresh one target across both the DOM/site probe layer and the desktop fallback layer in one route
  - Reuses shared filters like `--slug`, `--adapter`, `--configured-only`, `--stale-after`, and `--plan-only`
  - Can also pass desktop-specific knobs like `--force-desktop` and `--keep-screenshots`, plus `--include-terminal` when a site workflow intentionally lives at a manual boundary but still needs a forced refresh
  - Handy when one managed target needs both a fresh probe and a fresh fallback, without manually chaining two commands
  - Also exposed centrally via `../scripts/web-automation-dispatch.py refresh-stack`

- `../scripts/web-automation-prune.py`
  - Collects stale unmanaged generic probe artifacts and stale unmanaged desktop fallback outdirs in one place
  - Supports `--adapter <name>` so cleanup review or Trash runs can stay scoped to one adapter
  - Defaults to a safe dry-run summary, with `--apply` using `gio trash` so cleanup stays recoverable instead of hard-deleting files
  - Useful when one-off debug/demo probes are cluttering the boards even though the managed automation routes are healthy
  - Also exposed centrally via `../scripts/web-automation-dispatch.py prune-unmanaged`

## Recommended Proton sequence

1. `proton_probe_status.js`
2. `proton_to_password_step.js`
3. `proton_probe_password_step.js`
4. `proton_to_submit_ready.js`
5. `proton_submit_probe.js` only when intentionally testing the real final submit path

## Examples

```bash
node /home/clawdy/.openclaw/workspace/browser-automation/probe_page.js \
  https://account.proton.me/start

node /home/clawdy/.openclaw/workspace/browser-automation/probe_page.js \
  https://app.slack.com/signin --slug slack-signin

node /home/clawdy/.openclaw/workspace/browser-automation/probe_page.js \
  https://vault.bitwarden.com/#/login --slug bitwarden-login --session bitwarden-shared

node /home/clawdy/.openclaw/workspace/browser-automation/proton_to_password_step.js \
  clawdy01

node /home/clawdy/.openclaw/workspace/browser-automation/proton_to_submit_ready.js \
  clawdy01 'Short123!'

node /home/clawdy/.openclaw/workspace/browser-automation/proton_submit_probe.js \
  clawdy01

python3 /home/clawdy/.openclaw/workspace/scripts/proton-status-summary.py

python3 /home/clawdy/.openclaw/workspace/scripts/protonboard.py

python3 /home/clawdy/.openclaw/workspace/scripts/proton-next-step.py

python3 /home/clawdy/.openclaw/workspace/scripts/proton-autopilot-safe.py --max-steps 2

python3 /home/clawdy/.openclaw/workspace/scripts/web-automation-autopilot.py --plan-only

python3 /home/clawdy/.openclaw/workspace/scripts/web-automation-autopilot.py --apply-prune

python3 /home/clawdy/.openclaw/workspace/scripts/automation-board.py

python3 /home/clawdy/.openclaw/workspace/scripts/automation-board.py --adapter github

python3 /home/clawdy/.openclaw/workspace/scripts/automation-board.py --configured-only --attention-only

node /home/clawdy/.openclaw/workspace/browser-automation/proton_human_verification.js \
  clawdy01

python3 /home/clawdy/.openclaw/workspace/scripts/proton-verification-status.py

python3 /home/clawdy/.openclaw/workspace/scripts/web-automation-dispatch.py proton-verify-refresh

python3 /home/clawdy/.openclaw/workspace/scripts/proton-request-verification-code.py

python3 /home/clawdy/.openclaw/workspace/scripts/proton-human-verification-summary.py

python3 /home/clawdy/.openclaw/workspace/scripts/proton-manual-finish-summary.py

python3 /home/clawdy/.openclaw/workspace/scripts/web-automation-artifacts.py

python3 /home/clawdy/.openclaw/workspace/scripts/web-automation-site-registry.py \
  promote --slug bitwarden-login --stale-after 3600

python3 /home/clawdy/.openclaw/workspace/scripts/web-automation-artifacts.py --stale-after 1800

python3 /home/clawdy/.openclaw/workspace/scripts/web-automation-artifacts.py --adapter github

python3 /home/clawdy/.openclaw/workspace/scripts/web-automation-sites.py

python3 /home/clawdy/.openclaw/workspace/scripts/web-automation-sites.py --configured-only

python3 /home/clawdy/.openclaw/workspace/scripts/web-automation-sites.py --attention-only

python3 /home/clawdy/.openclaw/workspace/scripts/web-automation-sites.py --slug github-login

python3 /home/clawdy/.openclaw/workspace/scripts/web-automation-dispatch.py artifacts --json

python3 /home/clawdy/.openclaw/workspace/scripts/web-automation-dispatch.py artifacts --adapter github

python3 /home/clawdy/.openclaw/workspace/scripts/web-automation-dispatch.py automation-board --json

python3 /home/clawdy/.openclaw/workspace/scripts/web-automation-dispatch.py automation-board --adapter github

python3 /home/clawdy/.openclaw/workspace/scripts/web-automation-dispatch.py sites --json

python3 /home/clawdy/.openclaw/workspace/scripts/web-automation-dispatch.py sites --configured-only

python3 /home/clawdy/.openclaw/workspace/scripts/web-automation-dispatch.py sites --attention-only

python3 /home/clawdy/.openclaw/workspace/scripts/web-automation-dispatch.py sites --slug github-login

python3 /home/clawdy/.openclaw/workspace/scripts/web-automation-dispatch.py selectors

python3 /home/clawdy/.openclaw/workspace/scripts/web-automation-dispatch.py selectors --slug github-login

python3 /home/clawdy/.openclaw/workspace/scripts/web-automation-dispatch.py selectors --adapter slack --json

python3 /home/clawdy/.openclaw/workspace/scripts/web-automation-dispatch.py site-registry

python3 /home/clawdy/.openclaw/workspace/scripts/web-automation-dispatch.py site-registry validate

python3 /home/clawdy/.openclaw/workspace/scripts/web-automation-dispatch.py site-registry list --adapter github

python3 /home/clawdy/.openclaw/workspace/scripts/web-automation-dispatch.py site-registry list --desktop-only

python3 /home/clawdy/.openclaw/workspace/scripts/web-automation-dispatch.py site-registry upsert \
  --slug github-login --url https://github.com/login --notes 'Houd login-observability warm'

python3 /home/clawdy/.openclaw/workspace/scripts/web-automation-dispatch.py site-registry upsert \
  --slug slack-signin --url https://app.slack.com/signin --stale-after 3600

python3 /home/clawdy/.openclaw/workspace/scripts/web-automation-dispatch.py site-registry upsert \
  --slug slack-signin --url https://app.slack.com/signin \
  --probe-arg --session --probe-arg slack-shared

python3 /home/clawdy/.openclaw/workspace/scripts/web-automation-dispatch.py site-registry upsert \
  --slug slack-signin --url https://app.slack.com/signin \
  --desktop-keep-screenshots 6

python3 /home/clawdy/.openclaw/workspace/scripts/web-automation-dispatch.py site-registry upsert \
  --slug proton-signup --route proton-refresh --label 'Proton signup'

python3 /home/clawdy/.openclaw/workspace/scripts/web-automation-dispatch.py refresh-sites

python3 /home/clawdy/.openclaw/workspace/scripts/web-automation-dispatch.py refresh-sites --configured-only

python3 /home/clawdy/.openclaw/workspace/scripts/web-automation-dispatch.py refresh-sites --plan-only

python3 /home/clawdy/.openclaw/workspace/scripts/web-automation-dispatch.py refresh-stack --configured-only --slug slack-signin

python3 /home/clawdy/.openclaw/workspace/scripts/web-automation-dispatch.py refresh-stack --configured-only --slug github-login --force-desktop --keep-screenshots 6

python3 /home/clawdy/.openclaw/workspace/scripts/web-automation-dispatch.py refresh-stack --adapter github --plan-only

python3 /home/clawdy/.openclaw/workspace/scripts/web-automation-dispatch.py refresh-desktop --plan-only

python3 /home/clawdy/.openclaw/workspace/scripts/web-automation-dispatch.py refresh-desktop --adapter github --plan-only

python3 /home/clawdy/.openclaw/workspace/scripts/web-automation-dispatch.py desktop-status --configured-only

python3 /home/clawdy/.openclaw/workspace/scripts/web-automation-dispatch.py desktop-status --adapter github

python3 /home/clawdy/.openclaw/workspace/scripts/web-automation-dispatch.py prune-unmanaged --adapter github

python3 /home/clawdy/.openclaw/workspace/scripts/web-automation-dispatch.py autopilot --adapter github --plan-only

python3 /home/clawdy/.openclaw/workspace/scripts/web-automation-dispatch.py autopilot --apply-prune

python3 /home/clawdy/.openclaw/workspace/scripts/web-automation-dispatch.py probe-page \
  https://app.slack.com/signin --slug slack-signin
```

Optional site registry at `/home/clawdy/.openclaw/workspace/state/web-automation-sites.json`:

```json
{
  "sites": [
    {
      "slug": "proton-signup",
      "label": "Proton signup",
      "adapter": "proton",
      "route": "proton-refresh",
      "notes": "Use the safe Proton refresh chain instead of a generic probe-page refresh"
    },
    {
      "slug": "slack-signin",
      "url": "https://app.slack.com/signin",
      "label": "Slack signin",
      "adapter": "slack",
      "staleAfterSeconds": 3600,
      "desktopKeepScreenshots": 6,
      "notes": "Keep signin selectors fresh"
    }
  ]
}
```

Output goes to:
- `/home/clawdy/.openclaw/workspace/browser-automation/out/probe.png`
- `/home/clawdy/.openclaw/workspace/browser-automation/out/probe.json`
- `/home/clawdy/.openclaw/workspace/browser-automation/out/proton-to-password-step.png`
- `/home/clawdy/.openclaw/workspace/browser-automation/out/proton-to-password-step.json`
- `/home/clawdy/.openclaw/workspace/browser-automation/out/proton-to-submit-ready.png`
- `/home/clawdy/.openclaw/workspace/browser-automation/out/proton-to-submit-ready.json`
- `/home/clawdy/.openclaw/workspace/browser-automation/out/proton-submit-probe.png`
- `/home/clawdy/.openclaw/workspace/browser-automation/out/proton-submit-probe.json`
- `/home/clawdy/.openclaw/workspace/browser-automation/out/proton-human-verification.png`
- `/home/clawdy/.openclaw/workspace/browser-automation/out/proton-human-verification.json`
- `/home/clawdy/.openclaw/workspace/browser-automation/out-desktop/metadata.json`
