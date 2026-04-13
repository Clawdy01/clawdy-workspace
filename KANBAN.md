# KANBAN.md

## Execution guardrails
- Operationele werklijst staat ook in Exchange Taken; KANBAN blijft de lokale bron voor structuur en prioriteit.
- Eén primair spoor tegelijk. Alleen het primaire spoor krijgt actieve bouwtijd totdat het klaar of echt geblokkeerd is.
- Huidig primair spoor: Secrets / password workflow opruimen en bruikbaar structureren
- Parallel mag alleen voor klein onderhoud of wanneer het primaire spoor extern wacht.
- Als het primaire spoor leeg is of extern wacht, herbeoordeel proactief taken, geparkeerde taken en backlog op wat nu wel uitgevoerd kan worden.
- Elk actief spoor moet een concrete definition of done hebben.
- Als een spoor geen tastbaar resultaat oplevert binnen korte tijd, stop en meld de blocker in plaats van door te drijven.
- Harde tijdsgrens: een taak/spoor moet binnen maximaal 1 uur afgerond zijn, of expliciet hard geblokkeerd met bewijs, of opgesplitst worden in kleinere deliverables.
- Na afronding van een primair spoor: eerst KANBAN/STATUS direct syncen, daarna in dezelfde werksessie het volgende spoor activeren.
- Geparkeerde of legacy sporen mogen niet als actief in updates verschijnen.

## Definition of done
- GitHub: account bestaat, login werkt, private repo bestaat, eerste push bevestigd
- Exchange SE on-prem: mailbox, agenda en taken hebben een bruikbare on-prem EWS-route voor lezen én de eerstvolgende nuttige actie is bevestigd
- Photo editing / image workflows: alleen opnieuw actief zodra er een echte bruikbare modelroute beschikbaar is

## Now
- Secrets / password workflow opruimen en bruikbaar structureren is nu het primaire spoor
- Eerste nulmeting vastgelegd in `research/creative-tooling-baseline.md` met bevestigde lokale CLI-routes voor ffmpeg, ImageMagick, sox en yt-dlp
- Kleine interne workflow-notitie staat nu in `research/creative-tooling-workflows.md`, met live geteste paden voor video-clippen, frame-export, audio-normalisatie en simpele image-afleidingen
- Eerste helper staat nu live: `scripts/video-clip.py` voor video-clip + frame-export, lokaal geverifieerd op synthetische testvideo
- Tweede helper staat nu live: `scripts/media-sanity-check.py` voor snelle inspectie van video/image/audio-output, live geverifieerd op sample video/audio/image plus JSON-output
- `scripts/media-sanity-check.py` ondersteunt nu optionele thresholds/warnings voor duur, resolutie, sample rate, minimale bestandsgrootte en ontbrekende audio, live geverifieerd op sample media plus negatieve check op video zonder audio
- `scripts/media-sanity-check.py` ondersteunt nu ook preset-profielen (`video-proof`, `audio-voice-16k`, `image-preview`) zodat terugkerende checks minder flags handmatig nodig hebben, live geverifieerd op sample video/audio/image plus JSON-output
- `scripts/media-sanity-check.py` ondersteunt nu ook directory/batch-check via `--dir` en `--recursive`, live geverifieerd op `tmp/creative-tooling-check`
- `scripts/media-sanity-check.py` ondersteunt nu ook `--warnings-only`, live geverifieerd op een schone testmap plus negatieve video-zonder-audio check zodat batch-runs compacter blijven
- `scripts/media-sanity-check.py` ondersteunt nu ook `--summary-by-kind`, live geverifieerd op `tmp/creative-tooling-check` in tekst- en JSON-mode zodat batch-runs direct een compacte opsplitsing per audio/image/video tonen
- `scripts/media-sanity-check.py` ondersteunt nu ook `--fail-on-warnings`, live geverifieerd met een groene batch-run en een negatieve check die terecht exit code 2 geeft
- `scripts/media-sanity-check.py` ondersteunt nu ook aggregate batch-grenzen via `--max-warning-files` en `--max-total-warnings`, live geverifieerd op `tmp/creative-tooling-check` met zowel een groene batch-run als een geforceerde fail-case met exit code 2
- `scripts/media-sanity-check.py` ondersteunt nu ook strikte fail-profielen via `--fail-profile` (`video-strict`, `audio-voice-16k-strict`, `image-preview-strict`), live geverifieerd met een groene audio/image-run en een bewuste video-fail zonder audio (exit code 2)
- `scripts/media-sanity-check.py` ondersteunt nu ook aggregate fail-profielen via `--fail-profile`, inclusief mixed batch-runs met `mixed-batch-strict` en `mixed-batch-review`, live geverifieerd op een schone map-run en een bewuste fail-case
- `scripts/media-sanity-check.py` ondersteunt nu ook rapport-output naar bestand/artifact via `--report-out` en `--report-format`, zodat CI-achtige checks resultaten direct kunnen bewaren of doorgeven
- `scripts/media-sanity-check.py` ondersteunt nu ook timestamped rapport-output via `--report-timestamped`, live geverifieerd met tekst- en JSON-artifacts in `tmp/creative-tooling-check/reports/`
- `scripts/media-sanity-check.py` ondersteunt nu ook append-mode via `--report-append`, live geverifieerd op `tmp/creative-tooling-check/reports/append-report.txt` met opeenvolgende rapportsecties zonder overschrijven
- `scripts/media-sanity-check.py` ondersteunt nu ook JSONL-reportmode via `--report-format jsonl`, live geverifieerd op `tmp/creative-tooling-check/reports/jsonl-report.jsonl` met een batch-event plus een aparte warning-only eventregel
- `scripts/media-sanity-check.py` ondersteunt nu ook `--report-summary-only`, live geverifieerd op `tmp/creative-tooling-check/reports/summary-only.jsonl` met compacte JSONL-events zonder volledige itemlijsten
- `scripts/media-sanity-check.py` ondersteunt nu ook compacte stdout-JSONL via `--jsonl`, inclusief `--jsonl-summary-only` voor alleen summary/meta zonder itemlijsten; live geverifieerd op `tmp/creative-tooling-check` en dezelfde compacte mode werkt ook voor JSONL-rapporten
- `scripts/media-sanity-check.py` ondersteunt nu ook `--kind` filtering, zodat batch-checks gericht alleen audio, image en/of video meenemen; live geverifieerd op `tmp/creative-tooling-check` met `--kind audio image --summary-by-kind` en `--kind video --jsonl --jsonl-summary-only`
- `scripts/media-sanity-check.py` ondersteunt nu ook `--exclude` voor batch-runs, live geverifieerd op `tmp/creative-tooling-check` met uitsluiting van `reports` en `helper-*`
- `scripts/media-sanity-check.py` ondersteunt nu ook naamfilters via `--name-contains` en `--name-not-contains`, live geverifieerd op `tmp/creative-tooling-check` met een gerichte frame-run en een bewuste no-match check
- `scripts/media-sanity-check.py` ondersteunt nu ook artifact-scan profielen (`artifact-review`, `artifact-scan-review`, `artifact-scan-strict`) met standaard `reports`/`helper-*` uitsluiting en compacte review-vs-strict mapchecks, live geverifieerd op `tmp/creative-tooling-check`
- `scripts/media-sanity-check.py` ondersteunt nu ook `--include` glob-patterns voor nog gerichtere batch-selectie, live geverifieerd op `tmp/creative-tooling-check` met `--include 'frame-*.png' --summary-by-kind`
- `scripts/media-sanity-check.py` ondersteunt nu ook include-gedreven artifactprofielen (`artifact-frames-review`, `artifact-frames-strict`) voor frame-only mapscans, live geverifieerd op `tmp/creative-tooling-check`
- `scripts/media-sanity-check.py` ondersteunt nu ook herbruikbare `--exclude-set` bundles voor veelvoorkomende outputmappen (`artifact-defaults`, `clip-helper-layout`, `frame-export-layout`), plus nieuwe presets/fail-profielen `clip-review`, `frame-export-review`, `clip-review-strict` en `frame-export-strict`; live geverifieerd op `tmp/creative-tooling-check`
- `scripts/media-sanity-check.py` ondersteunt nu ook herbruikbare `--include-set` bundles voor veelvoorkomende artifactgroepen (`frame-png`, `clips-video`, `audio-wav`), plus nieuwe presets/fail-profielen `frame-png-review`, `clip-video-review`, `frame-png-strict` en `clip-video-strict`; live geverifieerd op `tmp/creative-tooling-check`
- `scripts/media-sanity-check.py` ondersteunt nu ook `--dir-alias` voor terugkerende scanroots (`creative-tooling-check`, `creative-reports`, `creative-helper-frames`, `creative-helper-test`, `creative-helper-test-frames`), live geverifieerd op artifact-review, frame-submap en clips-video JSONL-run
- `scripts/media-sanity-check.py` ondersteunt nu ook complete workflowprofielen bovenop dir-aliasen: presets `creative-mixed-review`, `creative-audio-review`, `creative-helper-frames-review`, `creative-helper-clips-review` plus strict varianten als fail-profiel, live geverifieerd op mixed/audio/helper-frame/helper-clip runs
- `scripts/creative-review.py` biedt nu korte wrapper-commando's voor vaste creative review- en strict-routes, inclusief optionele rapportartifacts in `tmp/creative-tooling-check/reports/`; live geverifieerd op `mixed-review` en `helper-clips-strict --report --timestamped`
- `scripts/creative-review.py` ondersteunt nu ook suites `review-suite` en `strict-suite`, zodat alle vaste creative review- of strict-routes in één run kunnen worden afgewerkt inclusief timestamped rapportartifacts per subrun; live geverifieerd op de lokale testlayout
- `scripts/creative-review.py` ondersteunt nu ook `--daylog`, zodat review- en strictroutes compacte JSONL summary-events per UTC-dag naar één append-vriendelijk daglogartifact schrijven; live geverifieerd met `python3 scripts/creative-review.py review-suite --daylog` op `tmp/creative-tooling-check/reports/creative-review-daylog-20260412.jsonl`
- `scripts/creative-review.py` ondersteunt nu ook artifact-pruning via `--prune`, `--prune-older-than-days`, `--prune-apply` en automatische opschoning na writes via `--prune-after-write`; live geverifieerd met een tijdelijke reports-map waarin oude `creative-review-*` artifacts na een verse report-run direct zijn opgeschoond
- `scripts/creative-review.py` ondersteunt nu ook aparte prune-retentie voor timestamped/per-run reports versus daglogs via `--prune-report-older-than-days` en `--prune-daylog-older-than-days`; live geverifieerd met `py_compile`, een dry-run in JSON-mode en een apply-run op een tijdelijke testmap waarbij alleen het oude per-run report werd verwijderd en de daglogs bleven staan
- `scripts/creative-review.py` ondersteunt nu ook cleanup-presets (`balanced`, `short-reports`, `ci-tight`) voor vaste prune-combinaties; opnieuw live geverifieerd met `py_compile`, een JSON dry-run en een apply-run op `tmp/creative-review-cleanup-preset-test`, waarbij oude artifacts volgens presetretentie zijn opgeschoond en recente artifacts bleven staan
- `scripts/creative-review.py` ondersteunt nu ook cronvriendelijke `--automation-preset` combinaties (`daylog-balanced`, `timestamped-short`, `timestamped-ci`) die report/daylog, prune-after-write en cleanup-preset bundelen; live geverifieerd met `review-suite --automation-preset daylog-balanced` en `mixed-review --automation-preset timestamped-ci --format json`
- `scripts/creative-review.py` ondersteunt nu ook een echte `cleanup-only` route voor periodieke housekeeping zonder review-run; live geverifieerd met `cleanup-only --cleanup-preset balanced --format json`, plus voorbeeld-cronregel vastgelegd in `research/creative-tooling-workflows.md`
- `scripts/creative-review.py` ondersteunt nu ook directe cleanup-wrapper `weekly-cleanup`, die met `balanced` retentie oude per-run reports en daglogs zonder extra flags opruimt; live geverifieerd op `tmp/creative-review-weekly-cleanup-test` waarbij een oud report en oude daglog zijn verwijderd en een recent report bleef staan
- `scripts/creative-review.py` ondersteunt nu ook `--cleanup-log` plus automation-preset `weekly-cleanup-logged`, zodat prune/cleanup-runs append-vriendelijk JSONL naar een vaste logbestemming kunnen wegschrijven; live geverifieerd op `tmp/creative-review-cleanup-log-test` met een dry-run en echte `weekly-cleanup` apply-run waarbij twee oude artifacts verdwenen en het cleanup-log beide events vastlegde
- `scripts/creative-review.py` ondersteunt nu ook cleanup-logrotatie via `--prune-cleanup-log-older-than-days`, inclusief preset-defaults (`balanced=30`, `short-reports=14`, `ci-tight=7`); live geverifieerd op `tmp/creative-review-cleanup-log-rotation-test`, waarbij een oude cleanup-log plus oud report verdwenen en recente files bleven staan
- `research/creative-tooling-workflows.md` bevat nu ook een concreet cronvoorbeeld voor `weekly-cleanup-logged`, zodat wekelijkse housekeeping met auditlog direct inzetbaar is
- Nieuwe loginspectie-helper staat nu live: `scripts/creative-log-summary.py` vat creative daylogs en cleanup-logs samen in tekst of JSON, live geverifieerd op bestaande logs in `tmp/creative-tooling-check/reports` en `tmp/creative-review-cleanup-log-test/logs`
- Nieuwe smoke-wrapper staat nu live: `scripts/creative-smoke.py` bundelt vaste review/daylog- en cleanup-audit-routes met directe logsamenvatting in één kort commando; live geverifieerd met `review-daylog --format json` en `cleanup-audit --format json`
- `scripts/creative-smoke.py` ondersteunt nu ook end-to-end mode `full-cycle`, live geverifieerd met `python3 scripts/creative-smoke.py full-cycle --format json` zodat review-suite, cleanup-audit en verse daylog/cleanup-samenvatting in één run samenkomen
- `scripts/creative-smoke.py` ondersteunt nu ook compacte mode `full-cycle-brief`, live geverifieerd met tekst- en JSON-output zodat cron/statuschecks alleen pass/fail plus kerngetallen hoeven terug te lezen
- `scripts/clawdy-brief.py` en `scripts/statusboard.py` nemen nu ook direct de compacte creative smoke-samenvatting mee via `creative-smoke.py full-cycle-brief --format json`; live geverifieerd met `clawdy-brief --json` en `statusboard.py`, waarbij `statusboard` nu expliciet `creative smoke: ok (review-daylog: 108/108 ok, 0 warnings; cleanup-audit: cand 0, del 0)` toont
- `scripts/creative-smoke.py` ondersteunt nu ook `--consumer-out`, `--consumer-format` en `--consumer-append`, zodat compacte smoke-output direct naar een cron- of board-consumerbestand geschreven kan worden; live geverifieerd met `full-cycle-brief` naar `tmp/creative-tooling-check/reports/creative-smoke-consumer.json` en `creative-smoke-consumer.txt`
- `scripts/creative-smoke.py` ondersteunt nu ook vaste `--consumer-preset` routes (`board-json`, `board-text`, `eventlog-jsonl`) voor de standaard smoke-consumer-artifacts in `tmp/creative-tooling-check/reports/`, live geverifieerd met drie echte `full-cycle-brief` runs inclusief bestandsschrijfcontrole
- `scripts/creative-smoke.py` ondersteunt nu ook `--consumer-bundle` (`board-pair`, `board-suite`), zodat één smoke-run meerdere standaard consumer-artifacts tegelijk kan vullen; live geverifieerd met `full-cycle-brief --format json --consumer-bundle board-suite` plus artifact-nacheck op JSON, tekst en JSONL
- `scripts/creative-smoke-producer.py` gebruikt nu die bundels voor producer-modes `board` en `all`, zodat die routes nog maar één volledige smoke-run per publicatie hoeven te doen; live geverifieerd met `creative-smoke-producer.py board --quiet` en `all --quiet`
- `research/creative-tooling-workflows.md` bevat nu ook concrete cronvoorbeelden voor `creative-smoke-producer.py board` en `all`, zodat periodieke board-publicatie of board+eventlog direct planbaar is
- Creative tooling/workflows is functioneel afgerond als primair spoor: producerroute en board-integratie zijn live bevestigd met `python3 scripts/creative-smoke-producer.py all --quiet` en `python3 scripts/statusboard.py`, inclusief `creative smoke: ok`
- Nieuw primair spoor: secrets / password workflow opruimen en bruikbaar structureren nu Bitwarden werkt
- Eerste discovery op dit spoor staat in `research/secrets-password-workflow-round-1.md`: confirmed opslagpunten, actieve consumers en een directe opruimkans rond de dubbele loaders `scripts/workspace_secrets.py` en `scripts/secrets.py`
- `scripts/secrets.py` is nu teruggebracht tot expliciete compat-shim: het hergebruikt de canonieke loader uit `workspace_secrets.py` en exposeert tegelijk stdlib-compatibele `token_bytes`/`token_hex`/`token_urlsafe`, live geverifieerd doordat `python3 scripts/graph-auth-start.py --tenant-id demo-tenant --client-id demo-client` weer werkt ondanks lokale naamshadowing
- `scripts/workspace_secrets.py` ondersteunt nu ook canonieke secret-aliassen voor normalisatie (`mail.password`, `proton.password`, `github.password`) terwijl legacy keys blijven werken; `load_mail_config()` leest nu via `mail.password`, zodat consumers veilig stapsgewijs kunnen migreren zonder directe state-rewrite
- Eerste consumer-migratie op dit spoor is nu gedaan: de drie actieve Proton-scripts lezen canoniek via `proton.password`; live geverifieerd met `py_compile`, een alias-check zonder secretoutput, en `grep` die alleen nog de bewuste alias-definitie in `workspace_secrets.py` laat staan
- Mail- en GitHub-consumers zijn nagekeken: mail loopt aan de Python-kant al via `load_mail_config()`, en de nagekeken GitHub/Bitwarden automation-consumers tonen geen directe read van `github_account_password`; brede `grep` vond voor mail/GitHub alleen nog alias-definities in `workspace_secrets.py`
- Laatste workspacebrede scan buiten `state/`, `tmp/` en `.git/` vond geen verborgen shell/JS-routes die `state/secrets.json` direct lezen of legacy keys consumeren
- Veilige migratie-helper `scripts/secrets-normalize.py` staat nu live; dry-run (`python3 scripts/secrets-normalize.py --json`) is groen met `ok: true`, `conflicts: []` en een concreet migratieplan voor `mail.password`, `proton.password` en `github.password`
- Canonieke JSON-migratie is nu uitgevoerd met `python3 scripts/secrets-normalize.py --apply`; `state/secrets.json` bevat alleen nog `mail.password`, `proton.password` en `github.password`, loader-checks voor mail/Proton/GitHub bleven groen, en een nacheck-bug in `SECRET_ALIASES` is direct hersteld zodat dry-runs geen spook-acties meer tonen
- De legacy alias-ondersteuning is nu ook verwijderd uit `workspace_secrets.py`; verificatie bleef groen met schone `py_compile`, `python3 scripts/secrets-normalize.py --json` -> `actions: []`, canonieke loader-checks voor mail/Proton/GitHub en expliciete bevestiging dat legacy lookups geen waarde meer teruggeven
- Gerichte naverificatie op de volledig opgeschoonde loader is nu ook afgerond: brede `py_compile` voor mail/Proton/loader-scripts bleef groen, `python3 scripts/mail-auth-check.py` gaf live `login+select ok`, `python3 scripts/secrets-normalize.py --json` bleef schoon op `actions: []`, legacy lookups voor `mail_password`/`proton_pass_password`/`github_account_password` geven nu expliciet `False`, en de drie Proton-consumers laden nog steeds schoon via `--help`
- Secrets / password workflow opruimen en bruikbaar structureren is hiermee functioneel afgerond als primair spoor
- Nieuw primair spoor: mail workflow slimmer maken
- Eerste concrete stap op dit spoor staat nu live: `scripts/mail-next-step.py` ondersteunt `--current-only`, zodat queue/next-step alleen actuele mailacties tonen zonder stale follow-up of codefallback; `scripts/mail-dispatch.py` exposeert die route nu ook voor `next-step` en `queue`, live geverifieerd met `python3 scripts/mail-next-step.py --current-only --json -n 3` en `python3 scripts/mail-dispatch.py queue --current-only --json`
- Focus/actualiteitsheuristiek is nu aangescherpt: pure `ter info` mails zonder reply/deadline/hoog-signaal tellen niet meer als `attention_now`, en `scripts/mail-focus.py` kiest unread-focus nu eerst alleen uit echte actie-mails. Live geverifieerd met `python3 scripts/mail-dispatch.py queue --current-only --json` -> `recommended_route: noop`, `python3 scripts/mail-dispatch.py focus --json` -> `focus: null`, en `python3 scripts/mail-dispatch.py triage --all --current-only --clusters --json -n 5` -> geen actuele clusters terwijl de GitHub SSH-key notificatie alleen nog als stale info zichtbaar blijft
- GitHub: draait nu als onderhoud via automatische push, geen actief primair spoor meer
- Photo editing / image workflows: generatieve identity-preserving edits blijven geparkeerd tot betere model/hardware-route

## Blocked
- Geen harde blocker op het huidige creative-tooling spoor; nulmeting, workflow-inventaris, helper-thresholds, presets, batch-check, warnings-only, summary-by-kind, exclude-filters, include-filters, naamfilters, artifact-scan profielen, include-gedreven artifactprofielen, herbruikbare exclude-sets, herbruikbare include-sets, dir-aliasen, workflowprofielen, kleine wrapper-commando's, suite-wrapper-runs, daglogmodus, veilige prune-routes, strikte fail-profielen, mixed batch-fail-profielen, rapport-output naar artifact, timestamped output, append-mode, JSONL-reportmode en compacte stdout-JSONL zijn bevestigd en helperbouw kan lokaal doorgaan
- Betere identity-preserving photo edits blijven wel geblokkeerd op een sterkere/lokale modelroute

## Next
- Mail workflow verder aanscherpen, waarschijnlijk rond verschil tussen echte reply/deadline-acties en lage-waarde notificatieclusters zodra er weer nieuwe mail binnenkomt
- Daarna Mac migratieplan en lokale LLM/media-workflows oppakken
- Onderzoek naar betere identity-preserving photo edit modellen/workflows
- Regelmatige research-workflows opzetten voor onderwerpen die Christian wil volgen

## Backlog
- Eventuele publieke LinkedIn-tekst later netter maken zodra dat nog nuttig blijkt, maar pas na de interne contextopbouw voor ondersteuning
- Mac migratieplan voor lokale LLMs en media workflows
- Lokale LLM/image stack voorbereiden voor de nieuwe MacBook Pro
- Home Assistant / Z-Wave toegang voorbereiden zodra beschikbaar
- Security / hardening verbeteringen blijven nalopen
- Proper HTTPS / nette LAN-toegang voor de Control UI
- Betaalworkflow / debitcard-regels vastleggen voordat die koppeling er komt
- Regelmatige research-workflows opzetten voor onderwerpen die Christian wil volgen
- Herhalende taken expliciet omzetten naar skills/scripts/workflows in plaats van losse eenmalige oplossingen
- Mailbox, kalender en taken verder integreren in bruikbare routines

## Parked
- Ski-foto edit, opnieuw oppakken met betere modelroute

## Done
- Christian contextopbouw via LinkedIn/profielinformatie afgerond als interne ondersteuningscontext in `research/christian-support-context.md`, met achtergrond, rollen, projecten en actuele focus
- GitHub private repo aangemaakt, SSH-auth ingesteld, eerste push bevestigd, hourly auto-push actief
- Secrets / password workflow functioneel afgerond: canonieke secretnamen staan nu als enige in `state/secrets.json`, legacy alias-ondersteuning is verwijderd uit `workspace_secrets.py`, mail-auth werkt live via de opgeschoonde loader, Proton-consumers importeren nog schoon, en legacy sleutelreads geven expliciet niets meer terug
- Exchange SE on-prem basisroute bevestigd: Autodiscover + EWS werken, unread inbox/kalendercheck gelukt, en een verouderde GitHub-taak is succesvol via EWS naar Completed gezet en teruggelezen
- Exchange summary aangescherpt: onderscheid tussen actiegerichte vs notificatie-unread, signalering van afspraken binnen 24 uur, en overdue actieve taken zodat `next_action` minder snel op ruis blijft hangen
- Exchange huidige actieve taak afgerond: summary live geverifieerd en Exchange-taak `Exchange SE: mailbox/agenda helper verder uitbouwen` staat nu op Completed
- OpenClaw migratie hersteld
- Telegram reactions zichtbaar
- Telegram file sending werkend
- OAuth/Codex route actief
- Oude OpenAI API-key verwijderd
- Mailbox werkt en automatische mailcheck draait
- Status en tooling-overzichten opgezet
- Brede toolset voor media/docs/debug geïnstalleerd
- Basis browser automation met Playwright + headless Chromium werkt
- Control UI bruikbaar via SSH tunnel
- Creative review-wrapper verder bruikbaar gemaakt en live geverifieerd: `scripts/creative-review.py` ondersteunt nu artifact-pruning via `--prune` en automatische opschoning na report/daylog writes via `--prune-after-write`
- Creative review-wrapper verder aangescherpt en live geverifieerd: `scripts/creative-review.py` ondersteunt nu ook aparte prune-retentie voor per-run reports versus daglogs via `--prune-report-older-than-days` en `--prune-daylog-older-than-days`
- Creative review-wrapper verder bruikbaar gemaakt en live geverifieerd: `scripts/creative-review.py` ondersteunt nu ook directe cleanup-wrapper `weekly-cleanup` met `balanced` retentie en echte prune-apply voor oude reports/daglogs, getest op `tmp/creative-review-weekly-cleanup-test` waarbij alleen oude artifacts verdwenen
- Creative review-wrapper verder geautomatiseerd en live geverifieerd: `scripts/creative-review.py` ondersteunt nu ook `--cleanup-log` plus automation-preset `weekly-cleanup-logged`, zodat prune/cleanup-runs hun JSONL audittrail direct naar een vaste logmap kunnen appenden
- Creative tooling-workflows verder aangescherpt: `research/creative-tooling-workflows.md` bevat nu ook een concreet cronvoorbeeld voor `weekly-cleanup-logged`, zodat wekelijkse cleanup plus auditlog direct planbaar is
- Creative tooling-workflows verder bruikbaar gemaakt en live geverifieerd: `scripts/creative-log-summary.py` vat bestaande creative daylogs en cleanup-logs samen in tekst of JSON, zodat auditinspectie niet meer handmatig door JSONL hoeft
- Creative smoke-wrapper verder verdiept en live geverifieerd: `scripts/creative-smoke.py` ondersteunt nu ook end-to-end mode `full-cycle`, zodat creative review-daylog en cleanup-audit als één gecombineerde smoke-run plus samenvatting beschikbaar zijn
- Creative smoke-wrapper verder aangescherpt en live geverifieerd: `scripts/creative-smoke.py` ondersteunt nu ook compacte mode `full-cycle-brief`, zodat cron/statuschecks alleen pass/fail plus kerngetallen terugkrijgen
- Creative smoke-wrapper verder automation-vriendelijk gemaakt en live geverifieerd: `scripts/creative-smoke.py` ondersteunt nu ook `--consumer-out`, `--consumer-format` en `--consumer-append`, zodat dezelfde compacte smoke-status direct naar een consumerbestand voor cron/board-ingest kan worden geschreven
- Creative smoke-wrapper verder gestandaardiseerd en live geverifieerd: `scripts/creative-smoke.py` ondersteunt nu ook vaste `--consumer-preset` routes (`board-json`, `board-text`, `eventlog-jsonl`) zodat standaard consumer-artifacts zonder losse padflags kunnen worden gevuld
- Creative smoke-wrapper verder producer-vriendelijk gemaakt en live geverifieerd: `scripts/creative-smoke.py` ondersteunt nu ook `--consumer-bundle` (`board-pair`, `board-suite`), zodat één compacte smoke-run meerdere standaard consumer-artifacts tegelijk publiceert
- Creative smoke-producer verder efficiënter gemaakt en live geverifieerd: `scripts/creative-smoke-producer.py` laat `board` en `all` nu op één gebundelde smoke-run steunen in plaats van meerdere losse child-runs
- Creative tooling/workflows als primair spoor afgerond en board-ready bevestigd: `creative-smoke-producer.py all --quiet` en `statusboard.py` tonen nu live een groene `creative smoke` status, waarna KANBAN/STATUS direct zijn omgeschakeld naar het volgende primaire spoor
- LAN bind/rate limiting/typing feedback verbeterd
- Memory research: concrete betere geheugentechnieken beoordeeld en aanbeveling vastgelegd in `research/memory-techniques-recommendation.md`
- Creative tooling helper gebouwd en live geverifieerd: `scripts/video-clip.py` maakt korte clips plus frame-export uit video
- Creative tooling helper gebouwd en live geverifieerd: `scripts/media-sanity-check.py` inspecteert video, audio en image-output met tekst- en JSON-output
- Creative tooling helper aangescherpt en live geverifieerd: `scripts/media-sanity-check.py` geeft nu ook optionele threshold-warnings voor duur, resolutie, sample rate, minimale bestandsgrootte en ontbrekende audio
- Creative tooling helper verder bruikbaar gemaakt en live geverifieerd: `scripts/media-sanity-check.py` ondersteunt nu preset-profielen voor video-, audio- en image-checks
- Creative tooling helper verder verdiept en live geverifieerd: `scripts/media-sanity-check.py` kan nu hele outputmappen batchgewijs beoordelen en vond daarbij ook een kapotte sample-clip zonder videostream
- Creative tooling helper compacter bruikbaar gemaakt en live geverifieerd: `scripts/media-sanity-check.py` ondersteunt nu `--warnings-only`, en de eerder kapotte sample-clip is direct herbouwd zodat de batch-check weer 8/8 bestanden groen toont
- Creative tooling helper verder verdiept en live geverifieerd: `scripts/media-sanity-check.py` ondersteunt nu `--summary-by-kind`, zodat batch-runs in tekst- en JSON-output direct een compacte opsplitsing per mediatype tonen
- Creative tooling helper automation-vriendelijker gemaakt en live geverifieerd: `scripts/media-sanity-check.py` ondersteunt nu `--fail-on-warnings` met exit code 2 bij echte warnings
- Creative tooling helper nog CI-vriendelijker gemaakt en live geverifieerd: `scripts/media-sanity-check.py` ondersteunt nu aggregate batch-grenzen via `--max-warning-files` en `--max-total-warnings`, inclusief fail-reasons en exit code 2 bij overschrijding
- Creative tooling helper verder verscherpt en live geverifieerd: `scripts/media-sanity-check.py` ondersteunt nu ook strikte fail-profielen via `--fail-profile` voor video, audio-voice-16k en image-preview checks
- Creative tooling helper ook op batchniveau verscherpt en live geverifieerd: `scripts/media-sanity-check.py` ondersteunt nu mixed fail-profielen voor hele map-runs, inclusief expliciete `fail_reasons` in JSON-output
- Creative tooling helper CI-vriendelijker gemaakt en live geverifieerd: `scripts/media-sanity-check.py` kan nu rapporten als tekst of JSON wegschrijven via `--report-out` en `--report-format`
- Creative tooling helper beter bruikbaar gemaakt voor terugkerende runs: `scripts/media-sanity-check.py` ondersteunt nu ook timestamped rapport-output via `--report-timestamped`
- Creative tooling helper nog praktischer gemaakt voor terugkerende runs en live geverifieerd: `scripts/media-sanity-check.py` ondersteunt nu `--report-append`, zodat meerdere rapportsecties aan één bestaand artifact kunnen worden toegevoegd zonder overschrijven
- Creative tooling helper verder logvriendelijk gemaakt en live geverifieerd: `scripts/media-sanity-check.py` ondersteunt nu `--report-format jsonl` plus `generated_at`, zodat terugkerende runs als newline-delimited events kunnen worden bijgehouden
- Creative tooling helper nog compacter gemaakt voor logverwerking: `scripts/media-sanity-check.py` ondersteunt nu `--report-summary-only` voor JSON/JSONL-rapporten zonder volledige itemlijst
- Creative tooling helper ook interactief compacter gemaakt en live geverifieerd: `scripts/media-sanity-check.py` ondersteunt nu `--jsonl` plus `--jsonl-summary-only` voor één compact stdout-event zonder volledige itemlijst
- Creative tooling helper nu ook gerichter gemaakt en live geverifieerd: `scripts/media-sanity-check.py` ondersteunt `--kind` filtering voor audio/image/video in batch- en stdout-runs
- Creative tooling helper verder opgeschoond voor batch-runs: `scripts/media-sanity-check.py` ondersteunt nu `--exclude` met glob-patterns, inclusief subtree-uitsluiting via padcomponenten
- Creative tooling helper nog gerichter gemaakt en live geverifieerd: `scripts/media-sanity-check.py` ondersteunt nu `--name-contains` en `--name-not-contains` voor relevantere bestandsselectie binnen batch-runs
- Creative tooling helper nog preciezer gemaakt en live geverifieerd: `scripts/media-sanity-check.py` ondersteunt nu ook `--include` glob-patterns voor gerichte batch-selectie van relevante artifacts
- Creative tooling helper nog sneller bruikbaar gemaakt voor terugkerende lokale scanroutes en live geverifieerd: `scripts/media-sanity-check.py` ondersteunt nu ook `--dir-alias` voor veelgebruikte creative-tooling mappen en submappen
