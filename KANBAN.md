# KANBAN.md

## Execution guardrails
- Operationele werklijst staat ook in Exchange Taken; KANBAN blijft de lokale bron voor structuur en prioriteit.
- Eén primair spoor tegelijk. Alleen het primaire spoor krijgt actieve bouwtijd totdat het klaar of echt geblokkeerd is.
- Huidig primair spoor: Creative tooling/workflows verdiepen voor image/audio/video
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
- Creative tooling/workflows verdiepen voor image/audio/video is nu het primaire spoor
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
- Volgende stap: wrapper desgewenst uitbreiden met artifact-pruning voor terugkerende sanity-checks en oudere timestamped/daglog-artifacts
- GitHub: draait nu als onderhoud via automatische push, geen actief primair spoor meer
- Photo editing / image workflows: generatieve identity-preserving edits blijven geparkeerd tot betere model/hardware-route

## Blocked
- Geen harde blocker op het huidige creative-tooling spoor; nulmeting, workflow-inventaris, helper-thresholds, presets, batch-check, warnings-only, summary-by-kind, exclude-filters, include-filters, naamfilters, artifact-scan profielen, include-gedreven artifactprofielen, herbruikbare exclude-sets, herbruikbare include-sets, dir-aliasen, workflowprofielen, kleine wrapper-commando's, suite-wrapper-runs, daglogmodus, strikte fail-profielen, mixed batch-fail-profielen, rapport-output naar artifact, timestamped output, append-mode, JSONL-reportmode en compacte stdout-JSONL zijn bevestigd en helperbouw kan lokaal doorgaan
- Betere identity-preserving photo edits blijven wel geblokkeerd op een sterkere/lokale modelroute

## Next
- Secrets/workflows verder opruimen nu Bitwarden werkt
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
