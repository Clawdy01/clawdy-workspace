# TOOLING_INVENTORY.md

## Core/OpenClaw
- OpenClaw main agent
- Telegram integration
- Web search / fetch
- Memory search
- Exec/process tools

## Media/Image
- ImageMagick (`convert`)
- ffmpeg
- libvips (`vips`)
- Pillow (Python)
- rembg + onnxruntime in `.venv-photo`
- webp tools
- libheif tools
- pngquant
- jpegoptim
- optipng
- inkscape
- gimp
- mediainfo

## OCR / Documents
- tesseract
- ocrmypdf
- poppler-utils (`pdftotext`, `pdfinfo`)
- pandoc
- csvkit
- exiftool

## Audio / Video
- sox
- opus-tools
- yt-dlp

## CLI / Debug / System
- jq
- ripgrep (`rg`)
- fd-find (`fdfind`)
- sqlite3
- tree
- ncdu
- moreutils
- inotify-tools
- httpie (`http`)
- dnsutils (`dig`)
- parallel

## Browser / UI
- chromium-browser
- xvfb
- Playwright (`browser-automation/`)

## Local scripts/workflows
- `scripts/send-telegram-file.js` — send files/images directly to Telegram
- `scripts/openclaw-status-summary.py` — compacte Nederlandse statussamenvatting, nu ook met `--json` voor command/status workflows
- `scripts/clawdy-brief.py` — combineert OpenClaw status + mailstaat in één compacte brief, ook met `--json`
- `scripts/statusboard.py` — compacte statusboard-weergave op basis van `clawdy-brief.py`, ook met `--json` en `--preview`
- `scripts/toolsboard.py` — compacte toolsboard-weergave uit `TOOLING_INVENTORY.md`, ook met `--json`, `--section` en `--limit`
- `scripts/security-summary.py` — compacte security audit samenvatting voor status/command workflows
- `scripts/task-audit-summary.py` — compacte task/audit samenvatting voor failures, lost en warns
- `scripts/mail-summary.py` — compacte mailsamenvatting met urgentie en simpele actiehints, ook met `--json`
- `scripts/mail-drafts.py` — simpele concept-antwoorden op basis van mail-summary output, ook met `--json`, `--stdin` en `--input`
- `scripts/mail-latest.py` — snelle view van laatste of ongelezen mails, nu ook met preview, urgentie, `--unread`, threadgroepering en `--current-only` om oude/stale alerts weg te filteren
- `scripts/mailboard.py` — compacte mailboard-view die latest, unread, new en drafts combineert, ook met `--preview`, en nu waar mogelijk expliciet actuele betekenisvolle mail/thread boven stale fallback verkiest
- `scripts/mail-dispatch.py` — dispatcher/catalogus voor mailroutes zoals `check`, `summary`, `latest`, `drafts`, `triage`, `now`, `focus`, `next-step`, `queue`, `review-next`, `thread`, `clusters`, `codes` en `board`, inclusief aliases en JSON-output
- `scripts/mail-review-next.py` — opent direct de door `mail-next-step` gekozen volgende mailthread, of via `--candidate N` een alternatief uit die queue, met context, alternatieven en optioneel bestaand conceptantwoord
- `scripts/mail-thread.py` — klapt één recente mailthread compact uit, met filters op afzender/onderwerp/actie, message-timeline, attachment/security hints en optioneel bestaand conceptantwoord
- `scripts/command-board.py` — gecombineerde board-view voor status, mail, security, tasks, automation en tools, nu gebouwd op de dispatchers zodat board/output consistenter blijft, ook met JSON en tool-filter
- `scripts/command-dispatch.py` — simpele router voor `status`, `tools`, `mail`, `mail-latest`, `mail-summary`, `mail-drafts`, `mail-triage`, `mail-now`, `mail-focus`, `mail-next-step`, `mail-queue`, `mail-review-next`, `mail-thread`, `mail-clusters`, `mail-codes`, `mail-catalog`, `board`, `brief`, `proton`, `proton-board`, `proton-refresh`, `proton-verify`, `security`, `tasks`, `automation`, `automation-board`, `automation-catalog`, `automation-proton-status` en `automation-proton-refresh`, inclusief slash-commands, help/list en JSON-help, zonder dubbele automation-entries
- `scripts/proton-status-summary.py` — compacte Proton signup samenvatting op basis van probe-output
- `scripts/proton-refresh-safe.py` — draait veilige Proton probes opnieuw en geeft daarna direct verse status
- `scripts/automation-board.py` — compacte automation-board met route-overzicht en desktop-fallback health; Proton wordt alleen nog expliciet meegenomen als de adapter bewust gefilterd wordt
- `scripts/web-automation-dispatch.py` — dispatcher/catalogus voor web automation routes, inclusief DOM/desktop fallback, aliases, desktop-status, nieuwe per-target `stack-status` view, gecombineerde `refresh-stack` route, en Proton flows zoals status, password-step, refresh en submit-ready, plus adaptergerichte artifact/site/desktop filtering
- `scripts/web-automation-stack-status.py` — combineert per target DOM probe, desktop fallback, artifact-breadcrumbs en workflow-state in één gerichte stack-view voor adapterwerk of debugging
- `scripts/web-automation-refresh-stack.py` — refreshes één target over zowel DOM/site probe als desktop fallback heen, zodat een adapter in één route weer volledig warm staat
- `scripts/desktop-fallback-status.py` — compacte health/observability-view voor `browser-automation/out-desktop*`, met screenshot/window-capture freshness en refresh-command
- `scripts/git-publish-readiness.py` — snelle check of de workspace publish-veilig is voor een eerste private GitHub push
- `scripts/gitignore-proposal-check.py` — laat zien wat het GitHub private `.gitignore`-voorstel al wel/niet afdekt
- `scripts/git-first-push-plan.py` — geeft concrete commando’s voor de eerste private GitHub push, zonder al iets te wijzigen
- `scripts/git-sensitive-tracked.py` — toont gevoelige paden die nog tracked zijn en eerst uit git moeten voor een veilige private push
- `scripts/exchange-ews-check.py` — snelle Exchange SE on-prem check voor Autodiscover + EWS-basisroute
- `scripts/exchange-ews-tool.py` — praktische Exchange SE helper voor inbox, agenda, taken, taakcreatie en taakstatus-updates via EWS
- `scripts/exchange-mailbox.py` — compacte mailbox-view voor unread/latest Exchange-mail bovenop EWS
- `scripts/exchange-summary.py` — compacte Exchange SE samenvatting bovenop EWS-check, unread mailbox, agenda en taken
- `browser-automation/proton_probe_status.js` — herhaalbare Proton signup probe met screenshot, JSON status en candidate actions
- `browser-automation/proton_probe_username_activation.js` — toont waarom `#username` niet normaal invulbaar is en test JS-activering
- `browser-automation/proton_probe_username_submit_js.js` — probeert submit na JS-activering van `#username` en legt de vervolgstap vast
- `browser-automation/proton_probe_input_proxy.js` — laat zien dat de zichtbare Proton username/email control via een iframe challenge/proxy loopt
- `browser-automation/proton_probe_iframe_email.js` — vult de zichtbare Proton iframe-input en bevestigt doorgang naar de password-stap
- `browser-automation/proton_probe_password_step.js` — brengt de Proton password-stap in kaart zonder accountcreatie af te ronden
- `browser-automation/proton_probe_password_validation.js` — test veilige password-validatie/strength feedback zonder de finale signup-submit te doen
- `browser-automation/proton_to_password_step.js` — herbruikbare route van Proton startpagina naar de password-stap via de zichtbare iframe-input
- `scripts/proton-status-summary.py` — compacte Proton signup status op basis van probe-output
- `scripts/protonboard.py` — compacte Proton board uit probe-status plus volgende stap uit notes
- `browser-automation/README.md` — compacte routekaart voor de web automation en Proton flow
- `browser-automation/proton_to_submit_ready.js` — herbruikbare route tot vlak voor de finale Proton signup-submit, inclusief passwordvelden
- `scripts/photo-mask-bg-edit.sh` — generate subject cutout + mask
- `scripts/photo-bg-sunny-fireworks.sh` — experimental masked background edit
- `scripts/photo-workflow-notes.md` — workflow notes

## Research / runbooks
- `research/github-private-publish-checklist.md` — runbook voor veilige eerste private GitHub push vanuit deze workspace
- `research/github-private-gitignore-proposal.txt` — voorstel voor publish-veilige `.gitignore` bij eerste private push
- `research/github-private-first-push-next-step.md` — compacte next-step volgorde voor de eerste private GitHub push
- `research/linkedin-profile-round-1.md` — eerste profielaudit met headline/About-richting en rewrite-kader
- `research/linkedin-profile-round-2-input-template.md` — klein invultemplate om de echte huidige LinkedIn-tekst snel om te zetten naar een gerichte rewrite
- `research/linkedin-profile-round-2-request.txt` — korte copy/paste aanvraagtekst om de huidige LinkedIn-tekst snel op te halen voor ronde 2
- `research/linkedin-profile-building-blocks.md` — compacte, direct inzetbare profielbouwblokken voor headline/About/Experience
- `scripts/video-clip.py` — kleine helper om een korte video-clip te maken en frames te exporteren via ffmpeg
- `scripts/media-sanity-check.py` — snelle inspectie van video/audio/image-output, inclusief JSON, preset/fail-profielen, threshold-warnings, directory/batch-check via `--dir`, CI-vriendelijke fail-modes, timestamped rapport-output, append-mode en summary-only JSON/JSONL-rapporten

## Notes
- For real-people photo edits: verify both visible effect and identity preservation before delivery.
- Prefer autonomous continuation when the next step is clear.
