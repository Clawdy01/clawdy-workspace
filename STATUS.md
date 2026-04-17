# STATUS.md

## Operational notes
- Exchange Taken wordt nu gebruikt als operationele takenlijst naast deze statusbestanden.
- Exchange Agenda wordt nu actief gebruikt voor agenda-uitleesroutes.

## Now
- Dagelijkse AI-briefing bewijspad is nu het primaire spoor
- Mail workflow slimmer maken is functioneel afgerond; vervolg alleen nog als praktijkgebruik nog concrete frictie laat zien
- Nacheck op het primaire spoor is direct na de 09:00 CEST slotrun opnieuw gedaan: `python3 scripts/ai-briefing-status.py --json`, `python3 scripts/ai-briefing-watchdog.py --json` en `python3 scripts/ai-briefing-watchdog-alert.py --mode proof-check` tonen `cron: job execution timed out`, delivery-status `unknown`, `consecutiveErrors: 1` en `bewijsprogressie 0/3`
- Concrete mitigatie is meteen doorgevoerd: `daily-ai-update` in `/home/clawdy/.openclaw/cron/jobs.json` staat nu op `timeoutSeconds: 480` in plaats van `300`, omdat de mislukte run op `lastDurationMs: 300815` exact tegen de oude timeout aanliep; `python3 scripts/ai-briefing-status.py --json` bevestigt daarna weer `payload_audit.ok: true`
- `scripts/ai-briefing-status.py` maakt de huidige wait-state nu expliciet config-bewust: als de config nieuwer is dan de laatste run krijgt de watchdogsamenvatting voortaan `huidige config wacht nog op eerste run` in plaats van alleen oude totaalcijfers; live geverifieerd met `python3 -m py_compile scripts/ai-briefing-status.py scripts/ai-briefing-watchdog.py scripts/ai-briefing-watchdog-alert.py scripts/ai-briefing-watchdog-producer.py`, `python3 scripts/ai-briefing-status.py --json` en `python3 scripts/ai-briefing-watchdog-alert.py --mode proof-check`
- Eerstvolgende kwalificatierun blijft nu `2026-04-18 09:00 CEST` en het bewijsdoel `2026-04-20 09:15 CEST`
- Actuele attention-status is opnieuw naar de standaard AI-briefing-consumer-artifacts gepubliceerd via `python3 scripts/ai-briefing-watchdog-producer.py proof-all --quiet`; die route eindigde met `exit=2` omdat de watchdog terecht nog de foutstatus van de laatste run rapporteert, niet omdat het publicatiepad zelf kapot is
- `scripts/ai-briefing-watchdog-producer.py` geeft in `--quiet` nu ook direct de bewijscontext mee, inclusief watchdogsamenvatting, `bewijsprogressie`, eerstvolgende kwalificatierun, bewijsdoel en de eerste blockerredenen; live geverifieerd met `python3 -m py_compile scripts/ai-briefing-watchdog-producer.py scripts/ai-briefing-watchdog.py scripts/ai-briefing-watchdog-alert.py scripts/ai-briefing-status.py` en `python3 scripts/ai-briefing-watchdog-producer.py proof-all --quiet`
- `scripts/ai-briefing-status.py` publiceert nu ook `last_run_timeout_audit`, zodat status/watchdog meteen laten zien hoeveel timeout-speling de laatste run nog had en toekomstige bijna-timeouts eerder zichtbaar worden; live geverifieerd met `python3 -m py_compile scripts/ai-briefing-status.py scripts/ai-briefing-watchdog.py scripts/ai-briefing-watchdog-alert.py scripts/ai-briefing-watchdog-producer.py`, `python3 scripts/ai-briefing-status.py --json` en `python3 scripts/ai-briefing-watchdog-producer.py proof-all --quiet`
- `scripts/ai-briefing-status.py` publiceert de kernsamenvatting nu ook expliciet in JSON als `summary` en `status_text` naast `text`, zodat consumers/watchdogs op hetzelfde bewijspad de kernstatus eenduidig kunnen hergebruiken; live geverifieerd met `python3 -m py_compile scripts/ai-briefing-status.py scripts/ai-briefing-watchdog.py scripts/ai-briefing-watchdog-alert.py scripts/ai-briefing-watchdog-producer.py` en `python3 scripts/ai-briefing-watchdog.py --json --require-qualified-runs 3`
- Nog een concrete hardeningstap op hetzelfde bewijspad: `scripts/ai-briefing-status.py` gebruikt nu default `SIGPIPE`, zodat korte pipeline-consumers niet meer eindigen met een Python `BrokenPipeError` traceback als downstream vroeg sluit; live geverifieerd met `python3 -m py_compile scripts/ai-briefing-status.py` en een afgesloten pipe-check via `tmp/ai-briefing/check_status_broken_pipe.py`
- Nog een concrete nuttige stap op hetzelfde bewijspad: `scripts/ai-briefing-watchdog.py` en `scripts/ai-briefing-watchdog-producer.py` geven de `last_run_timeout_audit` nu ook direct door in JSON-, tekst- en quiet-produceroutput, zodat board/eventlog-consumers de resterende timeout-speling meteen zien zonder extra status-call; live geverifieerd met `python3 -m py_compile scripts/ai-briefing-watchdog.py scripts/ai-briefing-watchdog-producer.py`, `python3 scripts/ai-briefing-watchdog.py --json --require-qualified-runs 3` en `python3 scripts/ai-briefing-watchdog-producer.py proof-all --quiet`
- Extra concrete nuttige stap op hetzelfde bewijspad: `scripts/ai-briefing-watchdog-producer.py --quiet` en `scripts/ai-briefing-watchdog-alert.py` tonen nu ook alle geplande kwalificatie-slots, zodat compacte cron/alert-consumers meteen het volledige proving-pad zien in plaats van alleen de eerstvolgende kwalificatierun; live geverifieerd met `python3 -m py_compile scripts/ai-briefing-watchdog-producer.py scripts/ai-briefing-watchdog-alert.py`, `python3 scripts/ai-briefing-watchdog-producer.py proof-all --quiet` en `python3 scripts/ai-briefing-watchdog-alert.py --mode proof-progress`
- Nog een concrete nuttige stap op hetzelfde bewijspad: `scripts/ai-briefing-status.py` publiceert nu ook expliciet `proof_today_block_text`, `proof_no_more_qualifying_runs_today` en een daglabel voor de eerstvolgende kwalificatierun, zodat status/watchdog/alert/producer meteen laten zien dat er vandaag geen kwalificerende run meer mogelijk is en dat het eerstvolgende slot morgen valt; live geverifieerd met `python3 -m py_compile scripts/ai-briefing-status.py scripts/ai-briefing-watchdog.py scripts/ai-briefing-watchdog-alert.py scripts/ai-briefing-watchdog-producer.py`, `python3 scripts/ai-briefing-status.py --json`, `python3 scripts/ai-briefing-watchdog.py --json --require-qualified-runs 3`, `python3 scripts/ai-briefing-watchdog-alert.py --mode proof-progress` en `python3 scripts/ai-briefing-watchdog-producer.py proof-all --quiet`
- Extra concrete nuttige stap op hetzelfde bewijspad: `scripts/ai-briefing-status.py` publiceert nu ook contexttekst per kwalificatieslot (`proof_target_run_slots_context_text` plus daglabels), en watchdog/alert/producer nemen die direct over zodat compacte consumeroutput meteen laat zien welke proof-slots morgen, over 2 dagen en over 3 dagen vallen; live geverifieerd met `python3 -m py_compile scripts/ai-briefing-status.py scripts/ai-briefing-watchdog.py scripts/ai-briefing-watchdog-alert.py scripts/ai-briefing-watchdog-producer.py`, `python3 scripts/ai-briefing-watchdog.py --json --require-qualified-runs 3`, `python3 scripts/ai-briefing-watchdog-alert.py --mode proof-progress` en `python3 scripts/ai-briefing-watchdog-producer.py proof-all --quiet`
- Nog een concrete nuttige stap op hetzelfde bewijspad: `scripts/ai-briefing-status.py` markeert timeout-headroom nu expliciet als historische oude-limiet-context wanneer een run op timeout faalde vóór een latere config-update, zodat watchdog/producer niet misleidend doen alsof die mislukte run al onder de huidige limiet draaide; live geverifieerd met `python3 -m py_compile scripts/ai-briefing-status.py scripts/ai-briefing-watchdog.py scripts/ai-briefing-watchdog-producer.py`, `python3 scripts/ai-briefing-status.py --json` en `python3 scripts/ai-briefing-watchdog-producer.py proof-all --quiet`

## Next
- Mac-migratie en lokale media/LLM-workflows voorbereiden
- Mailflow alleen weer oppakken als gebruik concrete problemen blootlegt

## Blocked
- `daily-ai-update` is momenteel nog tijdsgebonden geblokkeerd: de run van `2026-04-17 09:00 CEST` liep in timeout op de oude limiet van 300s (`lastDurationMs: 300815`), de timeout staat nu op 480s, `python3 scripts/ai-briefing-watchdog.py --json --require-qualified-runs 3` toont nog steeds `bewijsprogressie 0/3`, en de eerstvolgende kwalificatierun ligt op `2026-04-18 09:00 CEST`
- Goede beeldgeneratie-route ontbreekt nog in deze runtime, dus betere image-remakes wachten op sterkere/lokale modelroute
- Control UI via LAN zonder SSH vraagt later nog een nette HTTPS-route

## Done
- Mail workflow slimmer maken functioneel afgerond: dispatcher, slash-router en board-help delen nu een consistente inbox/unread/current/review/open/queue/focus/code/security-instaptaal
- Christian-contexttrack afgerond: interne ondersteuningssamenvatting staat in `research/christian-support-context.md` met achtergrond, rollen, projecten en actuele focus
- GitHub-track afgerond: private repo bestaat, SSH-auth werkt, eerste push bevestigd, hourly auto-push actief
- Secrets/password-track afgerond: canonieke secretnamen staan nu als enige in `state/secrets.json`, legacy alias-ondersteuning is verwijderd uit `scripts/workspace_secrets.py`, mail-auth werkt live via de opgeschoonde loader, Proton-consumers laden nog schoon, en legacy sleutelreads geven expliciet niets meer terug
- Exchange-track eerste echte actie bevestigd: Autodiscover + EWS werken, unread inbox-check gelukt, kalenderroute werkt, en een verouderde GitHub-taak is via EWS op `Completed` gezet en teruggelezen
- `scripts/exchange-summary.py` aangescherpt zodat de samenvatting notificatie-mail scheidt van actiegerichte unread, afspraken binnen 24 uur telt, overdue actieve taken markeert, en `next_action` daardoor nuttiger kiest
- Exchange huidig spoor afgerond: summary live geverifieerd, GitHub- en Exchange-taak staan beide op Completed, enige resterende taak in Exchange is nu terecht geparkeerd
- Migratie naar `clawdy` hersteld
- Memory/history grotendeels hersteld
- Root toegang werkend gemaakt
- Telegram file sending werkend gemaakt
- Telegram reactions zichtbaar gemaakt
- OpenClaw panel via SSH tunnel bruikbaar gemaakt
- OAuth/Codex route actief gemaakt
- Oude OpenAI API-key verwijderd
- Brede toolset geïnstalleerd
- Mailbox + automatische mailcheck werken
- Basis browser automation werkt
- Typing feedback en human delay verbeterd
- `scripts/video-clip.py` toegevoegd en live getest op synthetische sample-video voor clip + frame-export
- `scripts/media-sanity-check.py` toegevoegd en live getest op synthetische sample-video, genormaliseerde WAV en afgeleide PNG, inclusief `--json`
- `scripts/media-sanity-check.py` aangescherpt en live getest met threshold-warnings voor minimale duur, resolutie, verwachte sample rate, minimale bestandsgrootte en ontbrekende audio
- `scripts/media-sanity-check.py` verder bruikbaar gemaakt en live getest met preset-profielen voor video-, audio- en image-checks
- `scripts/media-sanity-check.py` verder uitgebreid en live getest met directory/batch-check, inclusief detectie van een sample-clip zonder videostream
- `scripts/media-sanity-check.py` compacter bruikbaar gemaakt en live getest met `--warnings-only`; de kapotte sample-clip is daarna direct opnieuw opgebouwd zodat de batch-check weer volledig groen draait
- `scripts/media-sanity-check.py` verder verdiept en live getest met `--summary-by-kind`, inclusief schone tekstoutput en JSON-output op `tmp/creative-tooling-check`
- `scripts/media-sanity-check.py` automation-vriendelijker gemaakt en live getest met `--fail-on-warnings`, inclusief exit code 2 op een negatieve check
- `scripts/media-sanity-check.py` nog CI-vriendelijker gemaakt en live getest met `--max-warning-files` en `--max-total-warnings`, inclusief fail-reasons en exit code 2 bij overschrijding
- `scripts/media-sanity-check.py` verder verscherpt en live getest met `--fail-profile` voor video-, audio-voice-16k- en image-preview-checks
- `scripts/media-sanity-check.py` ook op batchniveau verscherpt en live getest met mixed `--fail-profile`, inclusief expliciete `fail_reasons` in JSON-output
- `scripts/media-sanity-check.py` verder CI-vriendelijk gemaakt en live getest met `--report-out` en `--report-format`, inclusief tekst- en JSON-artifacts naast normale stdout-output
- `scripts/media-sanity-check.py` verder bruikbaar gemaakt voor terugkerende runs met `--report-timestamped`, inclusief timestamped tekst- en JSON-artifacts zonder overschrijven
- `scripts/media-sanity-check.py` verder bruikbaar gemaakt voor terugkerende runs met `--report-append`, zodat meerdere rapportsecties aan één bestaand artifact kunnen worden toegevoegd zonder overschrijven
- `scripts/media-sanity-check.py` verder logvriendelijk gemaakt en live getest met `--report-format jsonl`, zodat terugkerende runs als newline-delimited JSON-events kunnen worden vastgelegd
- `scripts/media-sanity-check.py` nog compacter gemaakt voor logverwerking met `--report-summary-only`, zodat JSONL-events zonder volledige itemlijst kunnen worden opgeslagen
- `scripts/media-sanity-check.py` ook interactief compacter gemaakt en live getest met `--jsonl --jsonl-summary-only`, zodat stdout ook als compact enkelvoudig summary-event gebruikt kan worden
- `scripts/media-sanity-check.py` nu ook gerichter gemaakt en live getest met `--kind` filtering voor audio/image/video in batch- en stdout-runs
- `scripts/media-sanity-check.py` verder opgeschoond voor batch-runs met `--exclude`, inclusief subtree-uitsluiting via padcomponenten
- `scripts/media-sanity-check.py` nog gerichter gemaakt en live getest met `--name-contains` en `--name-not-contains`, zodat terugkerende batch-runs sneller relevante files selecteren en thumb/tijdelijke varianten overslaan
- `scripts/media-sanity-check.py` nog preciezer gemaakt en live getest met `--include` glob-patterns, zodat batch-runs direct op gewenste artifactgroepen kunnen worden beperkt
- `scripts/media-sanity-check.py` nog sneller bruikbaar gemaakt voor terugkerende lokale scanroutes en live getest met `--dir-alias`, zodat veelgebruikte creative-tooling mappen en submappen kort aanspreekbaar zijn
- `scripts/creative-review.py` verder CI-vriendelijk gemaakt en live getest met suites `review-suite` en `strict-suite`, inclusief timestamped rapportartifacts per subrun
- `scripts/creative-review.py` verder opschoonvriendelijk gemaakt en live getest met artifact-pruning via `--prune` en automatische opschoning na report/daylog writes via `--prune-after-write`
- `scripts/creative-review.py` verder aangescherpt en live getest met aparte prune-retentie voor per-run reports versus daglogs via `--prune-report-older-than-days` en `--prune-daylog-older-than-days`
- `scripts/creative-review.py` verder bruikbaar gemaakt en live getest met directe cleanup-wrapper `weekly-cleanup`, die oude reports/daglogs met `balanced` retentie echt opruimt terwijl recente artifacts blijven staan
- `scripts/creative-review.py` verder geautomatiseerd en live getest met `--cleanup-log` plus automation-preset `weekly-cleanup-logged`, zodat prune/cleanup-runs hun JSONL audittrail direct naar een vaste logmap kunnen appenden
- `research/creative-tooling-workflows.md` verder aangescherpt met een concreet cronvoorbeeld voor `weekly-cleanup-logged`, zodat wekelijkse cleanup plus auditlog direct planbaar is
- `scripts/creative-log-summary.py` toegevoegd en live getest op bestaande creative daylogs en cleanup-logs, zodat auditinspectie nu ook als compacte tekst- of JSON-samenvatting beschikbaar is
- `scripts/creative-smoke.py` verder verdiept en live getest met nieuwe mode `full-cycle`, zodat creative review-daylog en cleanup-audit nu ook als één end-to-end smoke-run plus samenvatting beschikbaar zijn
- `scripts/creative-smoke.py` verder aangescherpt en live getest met compacte mode `full-cycle-brief`, zodat cron/statuschecks alleen pass/fail plus kerngetallen terugkrijgen
- `scripts/creative-smoke.py` verder automation-vriendelijk gemaakt en live getest met `--consumer-out`, `--consumer-format` en `--consumer-append`, zodat dezelfde compacte smoke-status direct naar een consumerbestand voor cron/board-ingest kan worden geschreven
- `scripts/creative-smoke.py` verder gestandaardiseerd en live getest met vaste `--consumer-preset` routes (`board-json`, `board-text`, `eventlog-jsonl`), zodat standaard consumerbestanden zonder losse padflags gevuld kunnen worden
- `scripts/creative-smoke.py` verder producer-vriendelijk gemaakt en live getest met `--consumer-bundle` (`board-pair`, `board-suite`), zodat één compacte smoke-run meerdere standaard consumerbestanden tegelijk publiceert
- `scripts/ai-briefing-watchdog-producer.py` uitgebreid met vaste proving-modes `proof-board`, `proof-eventlog` en `proof-all`, zodat het AI-briefing-bewijspad dezelfde board/eventlog-publicatie zonder losse handmatige flags kan herhalen
- Creative tooling/workflows als primair spoor afgerond en boardsync bevestigd: `creative-smoke-producer.py all --quiet` en `statusboard.py` tonen live een groene `creative smoke` status
