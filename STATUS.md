# STATUS.md

## Operational notes
- Exchange Taken wordt nu gebruikt als operationele takenlijst naast deze statusbestanden.
- Exchange Agenda wordt nu actief gebruikt voor agenda-uitleesroutes.

## Now
- Creative tooling/workflows voor image/audio/video is nu het primaire spoor
- Nulmeting van lokaal bruikbare tooling staat in `research/creative-tooling-baseline.md`
- De eerste workflow-notitie staat nu in `research/creative-tooling-workflows.md`, met live geteste routes voor clippen, frames exporteren, audio normaliseren en simpele image-afleidingen
- Eerste helper nu gebouwd en live geverifieerd: `scripts/video-clip.py` maakt korte clips plus frame-export uit video
- Tweede helper nu gebouwd en live geverifieerd: `scripts/media-sanity-check.py` inspecteert video, audio en image-output met tekst- en JSON-output
- `scripts/media-sanity-check.py` is nu ook aangescherpt met optionele threshold-warnings voor duur, resolutie, sample rate, minimale bestandsgrootte en ontbrekende audio, live geverifieerd op sample media plus negatieve check op video zonder audio
- `scripts/media-sanity-check.py` ondersteunt nu ook preset-profielen (`video-proof`, `audio-voice-16k`, `image-preview`) zodat terugkerende media-checks minder flags handmatig nodig hebben, live geverifieerd op sample video/audio/image plus JSON-output
- `scripts/media-sanity-check.py` ondersteunt nu ook directory/batch-check via `--dir` en `--recursive`, live geverifieerd op `tmp/creative-tooling-check`
- `scripts/media-sanity-check.py` ondersteunt nu ook `--warnings-only`, live geverifieerd op een schone testmap plus negatieve video-zonder-audio check zodat batch-output compacter blijft
- `scripts/media-sanity-check.py` ondersteunt nu ook `--summary-by-kind`, live geverifieerd op `tmp/creative-tooling-check` in tekst- en JSON-output zodat batch-runs direct compacte totalen per audio/image/video tonen
- `scripts/media-sanity-check.py` ondersteunt nu ook `--fail-on-warnings`, live geverifieerd met een groene batch-run en een negatieve check die terecht exit code 2 geeft
- `scripts/media-sanity-check.py` ondersteunt nu ook aggregate batch-grenzen via `--max-warning-files` en `--max-total-warnings`, live geverifieerd op `tmp/creative-tooling-check` met zowel een groene batch-run als een geforceerde fail-case met exit code 2
- `scripts/media-sanity-check.py` ondersteunt nu ook strikte fail-profielen via `--fail-profile` (`video-strict`, `audio-voice-16k-strict`, `image-preview-strict`), live geverifieerd met een groene audio/image-run en een bewuste video-fail zonder audio (exit code 2)
- `scripts/media-sanity-check.py` ondersteunt nu ook aggregate fail-profielen voor mixed batch-runs (`mixed-batch-strict`, `mixed-batch-review`), live geverifieerd met een schone map-run en een bewuste fail-case met `exit_code: 2`
- `scripts/media-sanity-check.py` ondersteunt nu ook rapport-output naar bestand/artifact via `--report-out` en `--report-format`, zodat CI-achtige checks resultaten direct kunnen bewaren of doorgeven
- `scripts/media-sanity-check.py` ondersteunt nu ook timestamped rapport-output via `--report-timestamped`, live geverifieerd met tekst- en JSON-artifacts in `tmp/creative-tooling-check/reports/`
- `scripts/media-sanity-check.py` ondersteunt nu ook `--report-append`, live geverifieerd op `tmp/creative-tooling-check/reports/append-report.txt` met opeenvolgende rapportsecties zonder overschrijven
- `scripts/media-sanity-check.py` ondersteunt nu ook `--report-format jsonl`, live geverifieerd op `tmp/creative-tooling-check/reports/jsonl-report.jsonl` met een batch-event en een aparte warning-only eventregel
- `scripts/media-sanity-check.py` ondersteunt nu ook `--report-summary-only`, live geverifieerd op `tmp/creative-tooling-check/reports/summary-only.jsonl` met compacte JSONL-events zonder volledige itemlijst
- `scripts/media-sanity-check.py` ondersteunt nu ook compacte stdout-JSONL via `--jsonl`, inclusief `--jsonl-summary-only` voor alleen summary/meta zonder itemlijst, live geverifieerd op `tmp/creative-tooling-check`; dezelfde compacte mode werkt ook voor JSONL-rapporten
- `scripts/media-sanity-check.py` ondersteunt nu ook `--kind` filtering, zodat batch-checks gericht alleen audio, image en/of video meenemen; live geverifieerd met `--kind audio image --summary-by-kind` en `--kind video --jsonl --jsonl-summary-only`
- `scripts/media-sanity-check.py` ondersteunt nu ook `--exclude` voor batch-runs, live geverifieerd op `tmp/creative-tooling-check` met uitsluiting van `reports` en `helper-*`
- `scripts/media-sanity-check.py` ondersteunt nu ook naamfilters via `--name-contains` en `--name-not-contains`, live geverifieerd op `tmp/creative-tooling-check` met een gerichte frame-run en een bewuste no-match check
- `scripts/media-sanity-check.py` ondersteunt nu ook artifact-scan profielen (`artifact-review`, `artifact-scan-review`, `artifact-scan-strict`) met standaard uitsluiting van `reports` en `helper-*`, live geverifieerd op `tmp/creative-tooling-check`
- `scripts/media-sanity-check.py` ondersteunt nu ook `--include` glob-patterns voor nog gerichtere batch-selectie, live geverifieerd op `tmp/creative-tooling-check` met `--include 'frame-*.png' --summary-by-kind`
- `scripts/media-sanity-check.py` ondersteunt nu ook include-gedreven artifactprofielen (`artifact-frames-review`, `artifact-frames-strict`) voor frame-only mapscans, live geverifieerd op `tmp/creative-tooling-check`
- `scripts/media-sanity-check.py` ondersteunt nu ook herbruikbare `--exclude-set` bundles voor veelvoorkomende outputmappen (`artifact-defaults`, `clip-helper-layout`, `frame-export-layout`), plus nieuwe presets/fail-profielen `clip-review`, `frame-export-review`, `clip-review-strict` en `frame-export-strict`; live geverifieerd op `tmp/creative-tooling-check`
- Volgende stap is preset include-sets of pad-aliasen bundelen voor nog vaker terugkerende scanroutes
- GitHub is afgerond als actief spoor; alleen nog onderhoud via auto-push

## Next
- Mail workflow slimmer maken
- Secrets / password workflow netter maken
- Mac-migratie en lokale media/LLM-workflows voorbereiden

## Blocked
- Goede beeldgeneratie-route ontbreekt nog in deze runtime, dus betere image-remakes wachten op sterkere/lokale modelroute
- Control UI via LAN zonder SSH vraagt later nog een nette HTTPS-route

## Done
- Christian-contexttrack afgerond: interne ondersteuningssamenvatting staat in `research/christian-support-context.md` met achtergrond, rollen, projecten en actuele focus
- GitHub-track afgerond: private repo bestaat, SSH-auth werkt, eerste push bevestigd, hourly auto-push actief
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
