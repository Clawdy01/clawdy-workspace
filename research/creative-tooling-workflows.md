# Creative tooling workflows

Doel: kleine interne workflow-notitie met concrete paden die in deze runtime nu al echt werken.

## Verificatie
Getest op 2026-04-12 met synthetische assets in `tmp/creative-tooling-check/`.

Bevestigd werkende output:
- `tmp/creative-tooling-check/sample-video.mp4`
- `tmp/creative-tooling-check/sample-clip.mp4`
- `tmp/creative-tooling-check/frame-01.png`
- `tmp/creative-tooling-check/sample-tone.wav`
- `tmp/creative-tooling-check/sample-tone-normalized.wav`
- `tmp/creative-tooling-check/frame-01-small-gray.png`

## Video
### 1. Kort clipje uit een video halen
```bash
ffmpeg -ss 0.5 -i input.mp4 -t 0.75 -c:v libx264 -an output-clip.mp4
```
Gebruik voor:
- snel een klein bewijsclipje maken
- alleen het relevante fragment delen of inspecteren

### 2. Frames exporteren
```bash
ffmpeg -i input.mp4 -vf fps=1 out/frame-%02d.png
```
Gebruik voor:
- thumbnails
- visuele checkpoints uit video
- input voor latere image-analyse of simpele edits

### 3. Video inspecteren
```bash
ffprobe -v error -show_entries format=duration,size -of json input.mp4
```
Gebruik voor:
- duur/bestandsgrootte snel checken
- verificatie in scripts of statusoutput

## Audio
### 1. Basis toon of testaudio genereren
```bash
sox -n -r 16000 -c 1 sample.wav synth 1 sine 440
```
Gebruik voor:
- testdata voor pipelines
- snelle sanity checks zonder extern bronbestand

### 2. Audio normaliseren
```bash
sox --norm=-3 input.wav output-normalized.wav
```
Gebruik voor:
- ruwe opnames gelijkmatiger maken
- output voorbereiden voor delen of verdere verwerking

## Image
### 1. Resize + grayscale
```bash
convert input.png -resize 160x120 -colorspace Gray output.png
```
Gebruik voor:
- snelle afgeleide previews
- simpele voorbereiding voor documentatie of OCR-achtige workflows

### 2. Afbeelding inspecteren
```bash
identify output.png
```
Gebruik voor:
- formaat en kleurenruimte checken
- naverificatie na batchbewerkingen

## Helperstatus
- `scripts/video-clip.py` bestaat nu als kleine wrapper voor clip + frame-export via ffmpeg
- Live geverifieerd op 2026-04-12 met `tmp/creative-tooling-check/sample-video.mp4`
- Bevestigde helper-output:
  - `tmp/creative-tooling-check/helper-test/test-clip.mp4`
  - `tmp/creative-tooling-check/helper-test/frames/frame-01.png`
  - `tmp/creative-tooling-check/helper-test/frames/frame-02.png`

Voorbeeld:
```bash
python3 scripts/video-clip.py tmp/creative-tooling-check/sample-video.mp4 \
  --start 0.25 \
  --duration 0.8 \
  --clip-out tmp/creative-tooling-check/helper-test/test-clip.mp4 \
  --frames-dir tmp/creative-tooling-check/helper-test/frames \
  --fps 2
```

## Praktische inzet nu
- Video: clippen, transcoderen, frames trekken, snelle inspectie
- Audio: genereren, converteren, normaliseren
- Image: klassieke niet-generatieve bewerkingen en verificatie
- Review housekeeping: `scripts/creative-review.py weekly-cleanup --cleanup-log` kan oude report/daylog-artifacts opruimen én tegelijk een append-vriendelijk JSONL cleanup-log wegschrijven
- End-to-end smoke-check: `scripts/creative-smoke.py full-cycle` draait nu in één wrapper zowel `review-suite --automation-preset daylog-balanced` als `weekly-cleanup --automation-preset weekly-cleanup-logged`, en leest daarna direct de verse daylog- en cleanup-samenvatting terug

### `scripts/creative-smoke.py`
Kleine smoke-testwrapper bovenop review/daylog en cleanup-routes.

Voorbeelden:
```bash
python3 scripts/creative-smoke.py review-daylog
python3 scripts/creative-smoke.py cleanup-audit --format json
python3 scripts/creative-smoke.py full-cycle --format json
python3 scripts/creative-smoke.py full-cycle-brief
```

Live geverifieerd op 2026-04-13:
- `review-daylog` route blijft daylog-events schrijven via `review-suite --automation-preset daylog-balanced`
- `cleanup-audit` route blijft cleanup-audit via `weekly-cleanup --automation-preset weekly-cleanup-logged` teruglezen
- nieuwe `full-cycle` route draaide beide stappen achter elkaar en gaf direct gecombineerde JSON-output met verse `creative-review-daylog-20260413.jsonl` en `creative-review-cleanup-log-20260413.jsonl`
- nieuwe `full-cycle-brief` route gaf compacte statusoutput met alleen pass/fail plus kerngetallen (`events`, `files`, `warnings`, `candidates`, `deleted`), en werkt ook in JSON met `ok: true`

## Huidige grens
- Geen bevestigde sterke generatieve image-route voor identity-preserving remakes in deze runtime
- Voor geavanceerde foto-edits blijft betere lokale/modelroute nodig

## Kleine helper nu beschikbaar
### `scripts/video-clip.py`
Bouwt een korte clip en/of exporteert frames uit een video.

Voorbeeld:
```bash
python3 scripts/video-clip.py input.mp4 --start 0.5 --duration 0.75 --clip-out out/clip.mp4 --frames-dir out/frames --fps 2 --json
```

Live geverifieerd op `tmp/creative-tooling-check/sample-video.mp4` met output:
- `tmp/creative-tooling-check/helper-clip.mp4`
- `tmp/creative-tooling-check/helper-frames/frame-01.png`
- `tmp/creative-tooling-check/helper-frames/frame-02.png`

## Nieuwe helper
### `scripts/media-sanity-check.py`
Snelle inspectie van video-, audio- en image-output, met zowel tekst- als JSON-output.

Voorbeeld:
```bash
python3 scripts/media-sanity-check.py \
  tmp/creative-tooling-check/sample-video.mp4 \
  tmp/creative-tooling-check/sample-tone-normalized.wav \
  tmp/creative-tooling-check/frame-01-small-gray.png
```

Live geverifieerd op 2026-04-12 met output voor:
- `tmp/creative-tooling-check/sample-video.mp4` → duur 2.000s, H.264, 320x240
- `tmp/creative-tooling-check/sample-tone-normalized.wav` → duur 1.000s, 16 kHz mono
- `tmp/creative-tooling-check/frame-01-small-gray.png` → 160x120, Gray PNG

JSON-variant ook bevestigd via `--json`.

### Thresholds en warnings
De helper ondersteunt nu ook optionele controles zoals:
- `--min-size-bytes`
- `--min-duration`
- `--min-width`
- `--min-height`
- `--expect-sample-rate`
- `--require-audio`

Live geverifieerd op 2026-04-12:
```bash
python3 scripts/media-sanity-check.py \
  tmp/creative-tooling-check/sample-video.mp4 \
  tmp/creative-tooling-check/sample-tone-normalized.wav \
  tmp/creative-tooling-check/frame-01-small-gray.png \
  --min-size-bytes 100 \
  --min-duration 0.5 \
  --min-width 100 \
  --min-height 100 \
  --expect-sample-rate 16000 \
  --json
```
Alle drie testbestanden kwamen terug met `ok: true`.

Extra negatieve check bevestigd:
```bash
python3 scripts/media-sanity-check.py tmp/creative-tooling-check/sample-video.mp4 --require-audio
```
Deze sample-video geeft dan terecht warning `audio stream ontbreekt`.

## Preset-profielen nu beschikbaar
`scripts/media-sanity-check.py` ondersteunt nu ook `--preset` voor terugkerende checks zonder losse flagreeks.

Beschikbare presets:
- `video-proof` → `min_size_bytes=1000`, `min_duration=0.5`, `min_width=320`, `min_height=240`
- `audio-voice-16k` → `min_size_bytes=1000`, `min_duration=0.5`, `expect_sample_rate=16000`
- `image-preview` → `min_size_bytes=100`, `min_width=160`, `min_height=120`

Voorbeeld:
```bash
python3 scripts/media-sanity-check.py tmp/creative-tooling-check/sample-video.mp4 --preset video-proof
python3 scripts/media-sanity-check.py tmp/creative-tooling-check/sample-tone-normalized.wav --preset audio-voice-16k
python3 scripts/media-sanity-check.py tmp/creative-tooling-check/frame-01-small-gray.png --preset image-preview --json
```

Live geverifieerd op 2026-04-12 met alle drie presets.

## Batch-check nu beschikbaar
`scripts/media-sanity-check.py` ondersteunt nu ook mapinspectie via `--dir`, optioneel met `--recursive`.

Voorbeelden:
```bash
python3 scripts/media-sanity-check.py --dir tmp/creative-tooling-check --preset image-preview
python3 scripts/media-sanity-check.py --dir tmp/creative-tooling-check --recursive --json
```

Live geverifieerd op 2026-04-12:
- niet-recursieve mapcheck gaf eerst `summary: total=8 ok=7 warnings=1` en vond daarmee een corrupte `sample-clip.mp4`
- die clip is direct opnieuw opgebouwd via `python3 scripts/video-clip.py ... --clip-out tmp/creative-tooling-check/sample-clip.mp4`
- daarna gaf de batch-check schoon `summary: total=8 ok=8 warnings=0`

## Alleen warnings tonen nu beschikbaar
Voor grotere outputmappen ondersteunt de helper nu ook `--warnings-only`, zodat de itemlijst compact blijft en alleen probleemgevallen toont terwijl de totaalsamenvatting behouden blijft.

Voorbeelden:
```bash
python3 scripts/media-sanity-check.py --dir tmp/creative-tooling-check --warnings-only
python3 scripts/media-sanity-check.py tmp/creative-tooling-check/sample-video.mp4 --require-audio --warnings-only --json
```

Live geverifieerd op 2026-04-12:
- warnings-only op de schone testmap liet alleen de samenvatting zien met `total=8 ok=8 warnings=0`
- de negatieve check met `--require-audio` gaf in warnings-only JSON alleen het probleemitem terug met warning `audio stream ontbreekt`

## Samenvatting per mediatype nu beschikbaar
`scripts/media-sanity-check.py` ondersteunt nu ook `--summary-by-kind`, zodat batch-runs naast de totaalscore direct een compacte opsplitsing per `audio` / `image` / `video` tonen.

Voorbeelden:
```bash
python3 scripts/media-sanity-check.py --dir tmp/creative-tooling-check --summary-by-kind
python3 scripts/media-sanity-check.py --dir tmp/creative-tooling-check --warnings-only --summary-by-kind --json
```

Live geverifieerd op 2026-04-12:
- tekstoutput gaf `summary: total=8 ok=8 warnings=0` plus
  - `audio: total=2 ok=2 warnings=0`
  - `image: total=3 ok=3 warnings=0`
  - `video: total=3 ok=3 warnings=0`
- JSON-output in `--warnings-only` mode hield de itemlijst leeg, maar gaf wel dezelfde `summary_by_kind` terug

## CI-achtige fail mode nu beschikbaar
`scripts/media-sanity-check.py` ondersteunt nu ook `--fail-on-warnings`.

Gebruik:
```bash
python3 scripts/media-sanity-check.py --dir tmp/creative-tooling-check --summary-by-kind --fail-on-warnings
```

Live geverifieerd op 2026-04-12:
- schone batch-run bleef groen met `warnings=0`
- negatieve check op `sample-video.mp4 --require-audio --fail-on-warnings --json` gaf terecht `exit_code: 2`

## Strikte fail-profielen nu beschikbaar
`scripts/media-sanity-check.py` ondersteunt nu ook `--fail-profile`, zodat terugkerende CI-achtige checks per use-case niet steeds losse threshold-flags hoeven te combineren.

Beschikbare fail-profielen:
- `video-strict` → `min_size_bytes=1000`, `min_duration=0.5`, `min_width=320`, `min_height=240`, `require_audio`, `fail_on_warnings`
- `audio-voice-16k-strict` → `min_size_bytes=1000`, `min_duration=0.5`, `expect_sample_rate=16000`, `fail_on_warnings`
- `image-preview-strict` → `min_size_bytes=100`, `min_width=160`, `min_height=120`, `fail_on_warnings`

Voorbeelden:
```bash
python3 scripts/media-sanity-check.py tmp/creative-tooling-check/sample-tone-normalized.wav --fail-profile audio-voice-16k-strict
python3 scripts/media-sanity-check.py tmp/creative-tooling-check/frame-01-small-gray.png --fail-profile image-preview-strict --json
python3 scripts/media-sanity-check.py tmp/creative-tooling-check/sample-video.mp4 --fail-profile video-strict --json
```

Live geverifieerd op 2026-04-12:
- `audio-voice-16k-strict` gaf schoon `ok=1`, `warnings=0`
- `image-preview-strict` gaf schoon JSON-resultaat met `exit_code: 0`
- `video-strict` faalde bewust op de sample-video zonder audio met warning `audio stream ontbreekt` en `exit_code: 2`

## Aggregate fail-profielen nu beschikbaar
`scripts/media-sanity-check.py` ondersteunt nu ook `--fail-profile` voor mixed batch-runs.

Nieuwe profielen:
- `mixed-batch-strict`
- `mixed-batch-review`

Voorbeeld:
```bash
python3 scripts/media-sanity-check.py --dir tmp/creative-tooling-check --summary-by-kind --fail-profile mixed-batch-strict
```

Live geverifieerd op 2026-04-12:
- schone map-run met `mixed-batch-strict` bleef groen
- negatieve check op `sample-video.mp4 --require-audio --fail-profile mixed-batch-strict --json` gaf terecht `exit_code: 2`
- JSON-output bevat daarbij ook expliciete `fail_reasons`

## Rapport-output naar artifact nu beschikbaar
`scripts/media-sanity-check.py` ondersteunt nu ook `--report-out` plus `--report-format`, zodat een batch-run naast stdout direct een bewaarrapport als JSON of tekst kan wegschrijven.

Voorbeelden:
```bash
python3 scripts/media-sanity-check.py --dir tmp/creative-tooling-check --summary-by-kind --report-out tmp/creative-tooling-check/report.txt
python3 scripts/media-sanity-check.py --dir tmp/creative-tooling-check --summary-by-kind --json --report-out tmp/creative-tooling-check/report.json
```

Live geverifieerd op 2026-04-12:
- tekst-rapport geschreven naar `tmp/creative-tooling-check/reports/mixed-summary.txt`
- JSON-rapport geschreven naar `tmp/creative-tooling-check/reports/mixed-summary.json`
- stdout bleef tegelijk bruikbaar voor directe inspectie

## Timestamped report-output nu beschikbaar
`scripts/media-sanity-check.py` ondersteunt nu ook `--report-timestamped`, zodat terugkerende runs nieuwe artifactbestanden krijgen zonder eerdere rapporten te overschrijven.

Voorbeelden:
```bash
python3 scripts/media-sanity-check.py --dir tmp/creative-tooling-check --summary-by-kind --report-out tmp/creative-tooling-check/reports/timestamped-summary.txt --report-timestamped
python3 scripts/media-sanity-check.py --dir tmp/creative-tooling-check --summary-by-kind --json --report-out tmp/creative-tooling-check/reports/timestamped-summary.json --report-timestamped
```

Live geverifieerd op 2026-04-12:
- `tmp/creative-tooling-check/reports/timestamped-summary-20260412T202559Z.txt`
- `tmp/creative-tooling-check/reports/timestamped-summary-20260412T202559Z.json`
- beide rapporten kwamen schoon terug met `total=8`, `ok=8`, `warnings=0`

## Rapport append-mode nu beschikbaar
`scripts/media-sanity-check.py` ondersteunt nu ook `--report-append`, zodat terugkerende runs meerdere tekst- of JSON-rapporten in één bestaand artifact kunnen verzamelen in plaats van overschrijven.

Voorbeelden:
```bash
python3 scripts/media-sanity-check.py --dir tmp/creative-tooling-check --summary-by-kind --report-out tmp/creative-tooling-check/reports/append-report.txt --report-append
python3 scripts/media-sanity-check.py tmp/creative-tooling-check/sample-video.mp4 --require-audio --warnings-only --report-out tmp/creative-tooling-check/reports/append-report.txt --report-append
```

Live geverifieerd op 2026-04-12:
- eerste run appende een schone batch-samenvatting aan `tmp/creative-tooling-check/reports/append-report.txt`
- tweede run appende daarna een compacte warning-only rapportsectie voor `sample-video.mp4`
- bestaand rapportbestand bleef behouden en kreeg er per run een nieuwe sectie bij

## JSONL-reportmode nu beschikbaar
`scripts/media-sanity-check.py` ondersteunt nu ook `--report-format jsonl`, zodat terugkerende runs compacte newline-delimited JSON-events kunnen wegschrijven voor latere logverwerking of simpele ingest in andere tools.

Voorbeelden:
```bash
python3 scripts/media-sanity-check.py --dir tmp/creative-tooling-check --summary-by-kind --report-out tmp/creative-tooling-check/reports/jsonl-report.jsonl --report-format jsonl --report-append
python3 scripts/media-sanity-check.py tmp/creative-tooling-check/sample-video.mp4 --require-audio --warnings-only --report-out tmp/creative-tooling-check/reports/jsonl-report.jsonl --report-format jsonl --report-append
```

Live geverifieerd op 2026-04-12:
- `tmp/creative-tooling-check/reports/jsonl-report.jsonl` bevat nu per run precies één JSON-regel
- batch-run schreef een compact success-event met `summary_by_kind`
- warning-only run schreef daarna een apart warning-event voor `sample-video.mp4`
- payload bevat nu ook `generated_at`, zodat downstream logverwerking runs tijdmatig kan ordenen

## Summary-only JSONL nu beschikbaar
`scripts/media-sanity-check.py` ondersteunt nu ook `--report-summary-only`, zodat JSON/JSONL-rapporten compact kunnen blijven zonder volledige itemlijst.

Voorbeelden:
```bash
python3 scripts/media-sanity-check.py --dir tmp/creative-tooling-check --summary-by-kind --report-format jsonl --report-summary-only --report-out tmp/creative-tooling-check/reports/summary-only.jsonl
python3 scripts/media-sanity-check.py tmp/creative-tooling-check/sample-video.mp4 --require-audio --warnings-only --report-format jsonl --report-summary-only --report-append --report-out tmp/creative-tooling-check/reports/summary-only.jsonl
```

Live geverifieerd op 2026-04-12:
- `tmp/creative-tooling-check/reports/summary-only.jsonl` bevat nu compacte newline-delimited events
- eerste event: schone batch-run met `total=8`, `ok=8`, `warnings=0`
- tweede event: warning-run met `total=1`, `warnings=1`
- beide events hebben `report_summary_only: true` en geen volledige `items`-lijst

## Exclude-patterns nu beschikbaar
`scripts/media-sanity-check.py` ondersteunt nu ook `--exclude` voor glob-based uitsluiting van tijdelijke files, thumbs of artifactmappen.

Voorbeelden:
```bash
python3 scripts/media-sanity-check.py --dir tmp/creative-tooling-check --recursive --exclude 'reports' --exclude 'helper-*' --summary-by-kind
python3 scripts/media-sanity-check.py --dir tmp/creative-tooling-check --recursive --kind video --exclude 'sample-*' --jsonl --jsonl-summary-only
```

Live geverifieerd op 2026-04-12:
- exclude van `reports` plus `helper-*` gaf een schone batch-run met `total=7`, `ok=7`, `warnings=0`
- gerichte video-run met `--exclude 'sample-*'` gaf compacte JSONL summary-only output met `total=2`, `ok=2`, `warnings=0`
- pattern matching werkt nu ook op padcomponenten, zodat een map als `helper-frames/` haar subtree echt overslaat

## Artifact-scan review-profielen nu beschikbaar
`scripts/media-sanity-check.py` ondersteunt nu ook preset/fail-profielen voor terugkerende outputmappen, inclusief standaard uitsluiting van artifactmappen zoals `reports` en helper-output zoals `helper-*`.

Nieuwe profielen:
- preset `artifact-review` → zet automatisch `--recursive`, `--summary-by-kind`, `--exclude reports`, `--exclude helper-*`
- fail-profile `artifact-scan-review` → zelfde scanbasis, plus reviewgrenzen `max_warning_files=1` en `max_total_warnings=2`
- fail-profile `artifact-scan-strict` → zelfde scanbasis, maar strikt groen met `fail_on_warnings`, `max_warning_files=0`, `max_total_warnings=0`

Voorbeelden:
```bash
python3 scripts/media-sanity-check.py --dir tmp/creative-tooling-check --preset artifact-review
python3 scripts/media-sanity-check.py --dir tmp/creative-tooling-check --fail-profile artifact-scan-review --json
python3 scripts/media-sanity-check.py --dir tmp/creative-tooling-check --fail-profile artifact-scan-strict --jsonl --jsonl-summary-only
```

Live geverifieerd op 2026-04-12:
- `artifact-review` gaf schoon `total=7 ok=7 warnings=0` met `audio=2`, `image=3`, `video=2`
- `artifact-scan-review --json` gaf dezelfde schone map-samenvatting met `exit_code: 0`
- `artifact-scan-strict --jsonl --jsonl-summary-only` gaf een compact groen event zonder itemlijst

Nut:
- minder losse flags bij terugkerende media-outputchecks
- artifactmappen en helper-output standaard buiten de hoofdscan
- review vs strict CI-route nu direct herbruikbaar

## Include-patterns nu beschikbaar
`scripts/media-sanity-check.py` ondersteunt nu ook `--include` voor glob-based selectie van alleen de gewenste artifactgroep binnen een batch-run.

Nieuwe profielen:
- `artifact-frames-review`
- `artifact-frames-strict`

Voorbeelden:
```bash
python3 scripts/media-sanity-check.py --dir tmp/creative-tooling-check --recursive --exclude 'reports' --exclude 'helper-*' --include 'frame-*.png' --summary-by-kind
python3 scripts/media-sanity-check.py --dir tmp/creative-tooling-check --preset artifact-frames-review
python3 scripts/media-sanity-check.py --dir tmp/creative-tooling-check --fail-profile artifact-frames-strict --jsonl --jsonl-summary-only
```

Live geverifieerd op 2026-04-12:
- include-run op `frame-*.png` gaf `total=3`, `ok=3`, `warnings=0`
- `artifact-frames-review` gaf dezelfde schone frame-only review-run
- `artifact-frames-strict` gaf compacte JSONL summary-only output met `total=3`, `ok=3`, `warnings=0`

## Herbruikbare ignore-sets nu beschikbaar
`scripts/media-sanity-check.py` ondersteunt nu ook `--exclude-set`, zodat terugkerende outputmappen minder losse `--exclude` flags nodig hebben.

Beschikbare exclude-sets:
- `artifact-defaults` → `reports`, `helper-*`
- `clip-helper-layout` → `reports`, `helper-*`, `frames`, `*/frames`
- `frame-export-layout` → `reports`, `helper-*`, `clips`, `*/clips`

Nieuwe profielen:
- preset `clip-review`
- preset `frame-export-review`
- fail-profile `clip-review-strict`
- fail-profile `frame-export-strict`

Voorbeelden:
```bash
python3 scripts/media-sanity-check.py --dir tmp/creative-tooling-check --preset clip-review
python3 scripts/media-sanity-check.py --dir tmp/creative-tooling-check --preset frame-export-review --json
python3 scripts/media-sanity-check.py --dir tmp/creative-tooling-check --recursive --exclude-set artifact-defaults --summary-by-kind
```

Live geverifieerd op 2026-04-13:
- `clip-review` gaf schoon `total=7 ok=7 warnings=0`
- `frame-export-review --json` gaf schoon `total=3 ok=3 warnings=0` met alleen image-output
- directe `--exclude-set artifact-defaults` run gaf schoon `total=7 ok=7 warnings=0`

## Include-sets nu beschikbaar
`scripts/media-sanity-check.py` ondersteunt nu ook `--include-set`, zodat terugkerende artifactgroepen met korte herbruikbare bundels geselecteerd kunnen worden.

Beschikbare include-sets:
- `frame-png` → `frame-*.png`
- `clips-video` → `*.mp4`, `*.mov`, `*.mkv`, `*.webm`
- `audio-wav` → `*.wav`

Nieuwe profielen:
- preset `frame-png-review`
- preset `clip-video-review`
- fail-profile `frame-png-strict`
- fail-profile `clip-video-strict`

Voorbeelden:
```bash
python3 scripts/media-sanity-check.py --dir tmp/creative-tooling-check --include-set frame-png --exclude-set artifact-defaults --summary-by-kind
python3 scripts/media-sanity-check.py --dir tmp/creative-tooling-check --preset frame-png-review --json
python3 scripts/media-sanity-check.py --dir tmp/creative-tooling-check --fail-profile clip-video-strict --jsonl --jsonl-summary-only
```

Live geverifieerd op 2026-04-13:
- `--include-set frame-png --exclude-set artifact-defaults` gaf `total=3`, `ok=3`, `warnings=0`
- `frame-png-review --json` gaf een schone frame-only samenvatting met `summary_by_kind.image.total=3`
- `clip-video-strict --jsonl --jsonl-summary-only` gaf een compact groen event met `total=2`, `ok=2`, `warnings=0`

## Map-aliasen nu beschikbaar
`scripts/media-sanity-check.py` ondersteunt nu ook `--dir-alias`, zodat terugkerende scanroutes in de lokale creative-tooling testlayout niet steeds als volledig pad hoeven te worden herhaald.

Beschikbare aliasen:
- `creative-tooling-check` → `tmp/creative-tooling-check`
- `creative-reports` → `tmp/creative-tooling-check/reports`
- `creative-helper-frames` → `tmp/creative-tooling-check/helper-frames`
- `creative-helper-test` → `tmp/creative-tooling-check/helper-test`
- `creative-helper-test-frames` → `tmp/creative-tooling-check/helper-test/frames`

Voorbeelden:
```bash
python3 scripts/media-sanity-check.py --dir-alias creative-tooling-check --preset artifact-review
python3 scripts/media-sanity-check.py --dir-alias creative-helper-test-frames --summary-by-kind --json
python3 scripts/media-sanity-check.py --dir-alias creative-tooling-check --recursive --include-set clips-video --jsonl --jsonl-summary-only
```

Live geverifieerd op 2026-04-13:
- `--dir-alias creative-tooling-check --preset artifact-review` gaf schoon `total=7 ok=7 warnings=0`
- `--dir-alias creative-helper-test-frames --summary-by-kind --json` gaf schoon `total=2 ok=2 warnings=0`
- `--dir-alias creative-tooling-check --recursive --include-set clips-video --jsonl --jsonl-summary-only` gaf compact groen event met `total=4 ok=4 warnings=0`

Nut:
- minder herhaling in terugkerende lokale scancommando's
- sneller wisselen tussen hoofdmap, helper-output en frame-submappen
- combineert netjes met bestaande presets, include-sets en JSONL-runs

## Workflowprofielen bovenop map-aliasen nu beschikbaar
`scripts/media-sanity-check.py` ondersteunt nu ook complete preset/fail-profielen die meteen een vaste `--dir-alias` meenemen. Daardoor zijn terugkerende reviewroutes voor de lokale creative-tooling layout nu één kort commando per use-case.

Nieuwe presets:
- `creative-mixed-review` → hele `creative-tooling-check` map, recursief, `summary_by_kind`, standaard artifact-uitsluiting
- `creative-audio-review` → audio-only review op `creative-tooling-check` met `audio-wav`
- `creative-helper-frames-review` → frame-only review op `creative-helper-frames`
- `creative-helper-clips-review` → clip-only review op `creative-helper-test`, met uitsluiting van `frames/`

Nieuwe fail-profielen:
- `creative-mixed-strict`
- `creative-audio-strict`
- `creative-helper-frames-strict`
- `creative-helper-clips-strict`

Voorbeelden:
```bash
python3 scripts/media-sanity-check.py --preset creative-mixed-review
python3 scripts/media-sanity-check.py --preset creative-helper-frames-review --json
python3 scripts/media-sanity-check.py --fail-profile creative-helper-clips-strict --jsonl --jsonl-summary-only
python3 scripts/media-sanity-check.py --fail-profile creative-audio-strict --json
```

Live geverifieerd op 2026-04-13:
- `creative-mixed-review` gaf schoon `total=7 ok=7 warnings=0` met `audio=2`, `image=3`, `video=2`
- `creative-helper-frames-review --json` gaf schoon `total=2 ok=2 warnings=0` op de helper-frame-map
- `creative-helper-clips-strict --jsonl --jsonl-summary-only` gaf een compact groen event met `total=1 ok=1 warnings=0`

## CI-wrapper suites nu beschikbaar
`scripts/creative-review.py` bestond al als korte wrapper rond de vaste creative review-profielen, en ondersteunt nu ook suites zodat alle vaste review- of strict-routes in één run kunnen worden afgewerkt inclusief rapport-artifacts per subrun.

Nieuwe suite-routes:
- `review-suite` → draait `mixed-review`, `audio-review`, `helper-frames-review`, `helper-clips-review`
- `strict-suite` → draait `mixed-strict`, `audio-strict`, `helper-frames-strict`, `helper-clips-strict`

Voorbeelden:
```bash
python3 scripts/creative-review.py review-suite --report --timestamped
python3 scripts/creative-review.py strict-suite --report --timestamped
```

Live geverifieerd op 2026-04-13:
- `review-suite --report --timestamped` draaide alle vier review-routes schoon en schreef per route een timestamped artifact naar `tmp/creative-tooling-check/reports/`
- `strict-suite --report --timestamped` draaide alle vier strikte routes schoon en schreef JSON/JSONL-artifacts per route weg
- suites geven per subrun een duidelijke sectiekop op stderr zodat CI/logs nog leesbaar blijven
- `creative-audio-strict --json` gaf schoon `total=2 ok=2 warnings=0`

Nut:
- vaste reviewroutes nu met één kort profiel in plaats van alias + include/exclude-stapel
- mixed, audio, helper-frames en helper-clips hebben nu elk een herbruikbare review- én strict-route
- minder kans op profiel/alias-mismatches in terugkerende checks

## Kleine wrapper-commando's nu beschikbaar
`script/creative-review.py` bundelt de vaste creative review- en strict-routes in korte wrapper-commando's bovenop `media-sanity-check.py`.

Beschikbare modes:
- `mixed-review`
- `audio-review`
- `helper-frames-review`
- `helper-clips-review`
- `mixed-strict`
- `audio-strict`
- `helper-frames-strict`
- `helper-clips-strict`

Voorbeelden:
```bash
python3 scripts/creative-review.py mixed-review
python3 scripts/creative-review.py helper-clips-strict --report --timestamped
python3 scripts/creative-review.py audio-strict --format json
```

Wat de wrapper doet:
- kiest automatisch de juiste preset of fail-profile
- kiest een logisch stdout-formaat per mode
- kan optioneel direct rapportartifacts wegschrijven naar `tmp/creative-tooling-check/reports/`
- ondersteunt `--timestamped` en `--append` voor terugkerende runs

Live geverifieerd op 2026-04-13:
- `mixed-review` gaf schoon `total=7`, `ok=7`, `warnings=0`
- `helper-clips-strict --report --timestamped` gaf een compact groen JSONL-event met `total=1`, `ok=1`, `warnings=0`
- bevestigd rapportartifact: `tmp/creative-tooling-check/reports/creative-review-helper-clips-strict-20260412T225552Z.jsonl`

## Daglogmodus nu beschikbaar
`scripts/creative-review.py` ondersteunt nu ook `--daylog`, zodat terugkerende review-runs compacte JSONL summary-events per UTC-dag naar één gedeeld logbestand appenden.

Voorbeelden:
```bash
python3 scripts/creative-review.py review-suite --daylog
python3 scripts/creative-review.py strict-suite --daylog
```

Live geverifieerd op 2026-04-13:
- `review-suite --daylog` draaide alle vier review-routes schoon
- bevestigde daglog-output: `tmp/creative-tooling-check/reports/creative-review-daylog-20260412.jsonl`
- het daglogbestand bevat nu per subrun één compact JSONL-event met `summary_only: true`, inclusief `preset`, `dir_alias`, totals en `summary_by_kind`

Nut:
- terugkerende creative checks kunnen nu naar één append-vriendelijk dagartifact loggen zonder per run losse timestamp-bestanden te maken
- suites bouwen zo een compact dagspoor op dat makkelijk te tailen of later te verwerken is

## Artifact-pruning nu beschikbaar
`scripts/creative-review.py` ondersteunt nu ook een veilige prune-route voor oudere creative-review artifacts en daglogs.

Nieuwe opties:
- `--prune`
- `--prune-older-than-days N`
- `--prune-apply`

Gedrag:
- standaard is prune een dry-run en toont alleen kandidaten
- selecteert creative-review timestamped rapporten en daglogs in de reports-map
- echte verwijdering gebeurt alleen met expliciet `--prune-apply`

Voorbeeld:
```bash
python3 scripts/creative-review.py mixed-review --prune --prune-older-than-days 7 --format json
```

Live geverifieerd op 2026-04-13:
- dry-run met `--prune-older-than-days 0 --format json` gaf een geldige kandidaatlijst terug voor oudere creative-review artifacts in `tmp/creative-tooling-check/reports`
- bevestigde velden: `report_dir`, `candidate_count`, `candidates`, `apply`
- geen bestanden verwijderd tijdens verificatie (`apply: false`)

## Aparte prune-retentie voor daglogs en per-run reports nu beschikbaar
`scripts/creative-review.py` ondersteunt nu ook aparte prune-retentie voor gewone creative-review rapporten versus daglogs.

Nieuwe opties:
- `--prune-report-older-than-days N`
- `--prune-daylog-older-than-days N`

Gedrag:
- beide opties overrulen alleen hun eigen artifactsoort
- zonder override blijft `--prune-older-than-days` de gedeelde fallback
- prune-output vermeldt nu ook `artifact_kind` en `retain_days` per kandidaat

Voorbeelden:
```bash
python3 scripts/creative-review.py mixed-review --prune --prune-report-older-than-days 2 --prune-daylog-older-than-days 14 --format json
python3 scripts/creative-review.py mixed-review --report --timestamped --prune-after-write --prune-report-older-than-days 2 --prune-daylog-older-than-days 14
```

Live geverifieerd op 2026-04-13:
- `py_compile` op `scripts/creative-review.py` bleef groen
- dry-run op een tijdelijke testmap liet aparte retentievelden zien in JSON-output
- apply-run met `--prune-report-older-than-days 2 --prune-daylog-older-than-days 4` verwijderde alleen het oude per-run report, terwijl beide daglogs bleven staan

Nut:
- daglogs kunnen langer bewaard blijven dan losse timestamped run-artifacts
- cron- of CI-runs kunnen agressiever opruimen zonder het compacte dagspoor kwijt te raken

## Cleanup-presets nu beschikbaar
`scripts/creative-review.py` ondersteunt nu ook vaste cleanup-presets voor veelgebruikte prune-combinaties.

Beschikbare presets:
- `balanced` → reports 7 dagen, daglogs 14 dagen
- `short-reports` → reports 2 dagen, daglogs 7 dagen
- `ci-tight` → reports 1 dag, daglogs 3 dagen

Voorbeelden:
```bash
python3 scripts/creative-review.py mixed-review --prune --cleanup-preset short-reports --format json
python3 scripts/creative-review.py mixed-review --report --timestamped --prune-after-write --cleanup-preset ci-tight
```

Live geverifieerd op 2026-04-13:
- dry-run met `--cleanup-preset short-reports --format json` gaf correcte retentievelden terug: `report=2`, `daylog=7`
- `--report --timestamped --prune-after-write --cleanup-preset ci-tight` draaide schoon en liet daarna prune-retentie `report=1`, `daylog=3` zien
- geen prune-kandidaten in de verificatierun, dus `deleted_count: 0`

## Automation-presets nu beschikbaar
`scripts/creative-review.py` ondersteunt nu ook `--automation-preset`, zodat terugkerende cron- of CI-runs niet steeds losse flags voor report/daylog, timestamping, prune-after-write en cleanup-preset hoeven te stapelen.

Beschikbare automation-presets:
- `daylog-balanced` → zet `--daylog`, `--prune-after-write` en `--cleanup-preset balanced`
- `timestamped-short` → zet `--report --timestamped --prune-after-write --cleanup-preset short-reports`
- `timestamped-ci` → zet `--report --timestamped --prune-after-write --cleanup-preset ci-tight`

Voorbeelden:
```bash
python3 scripts/creative-review.py review-suite --automation-preset daylog-balanced
python3 scripts/creative-review.py mixed-review --automation-preset timestamped-ci --format json
```

Live geverifieerd op 2026-04-13:
- `review-suite --automation-preset daylog-balanced` draaide alle vier review-routes schoon en appende naar `tmp/creative-tooling-check/reports/creative-review-daylog-20260413.jsonl`
- `mixed-review --automation-preset timestamped-ci --format json` schreef schoon een timestamped JSON-report naar `tmp/creative-tooling-check/reports/creative-review-mixed-review-20260413T000535Z.json`
- de ingebouwde prune-pass draaide direct mee met retentie `report=1`, `daylog=3` en vond in de verificatierun geen opruimkandidaten

Nut:
- cronvriendelijke vaste combinaties zonder losse flagstapels
- minder kans op drift tussen report/daylog-routes en cleanupbeleid
- snelle inzet voor zowel dagelijkse logging als strakkere CI-artifacts

## Cleanup-only route nu beschikbaar
`scripts/creative-review.py` ondersteunt nu ook een echte cleanup-only route, zodat periodieke housekeeping geen review-mode meer hoeft mee te geven.

Nieuwe route:
- `cleanup-only`

Voorbeelden:
```bash
python3 scripts/creative-review.py cleanup-only --cleanup-preset balanced --format json
python3 scripts/creative-review.py cleanup-only --cleanup-preset short-reports --prune-apply
```

Live geverifieerd op 2026-04-13:
- `cleanup-only --cleanup-preset balanced --format json` gaf een geldige prune-samenvatting met `report=7`, `daylog=14`
- verificatierun bleef veilig dry-run met `apply: false`

Voorbeeld cronregel (wekelijks opschonen):
```cron
17 3 * * 1 cd /home/clawdy/.openclaw/workspace && python3 scripts/creative-review.py cleanup-only --cleanup-preset balanced --prune-apply >> /home/clawdy/.openclaw/workspace/tmp/creative-tooling-check/reports/creative-review-cleanup.log 2>&1
```

## Cleanup-logrotatie nu beschikbaar
`scripts/creative-review.py` kan cleanup-logs nu ook zelf roteren binnen dezelfde prune-flow.

Nieuwe vlag:
- `--prune-cleanup-log-older-than-days`

Preset-defaults:
- `balanced` → cleanup-logs 30 dagen
- `short-reports` → cleanup-logs 14 dagen
- `ci-tight` → cleanup-logs 7 dagen

Voorbeeld:
```bash
python3 scripts/creative-review.py cleanup-only --cleanup-preset balanced --cleanup-log --cleanup-log-dir tmp/creative-review-cleanup-log-rotation-test/logs --report-dir tmp/creative-review-cleanup-log-rotation-test/reports --prune-apply --format json
```

Live geverifieerd op 2026-04-13:
- oud report (`10` dagen) werd verwijderd
- oude cleanup-log (`40` dagen) werd verwijderd
- recent report (`1` dag) bleef staan
- recente cleanup-log (`2` dagen) bleef staan
- de actuele cleanup-run schreef daarna zelf weer naar `creative-review-cleanup-log-20260413.jsonl`

## Wekelijkse cleanup met auditlog via cron
`weekly-cleanup-logged` bundelt nu een echte apply-run, balanced retentie en append-vriendelijk JSON cleanup-log in één cronvriendelijke route.

Voorbeeld cronregel:
```cron
17 3 * * 1 cd /home/clawdy/.openclaw/workspace && python3 scripts/creative-review.py weekly-cleanup --automation-preset weekly-cleanup-logged --cleanup-log-dir /home/clawdy/.openclaw/workspace/tmp/creative-tooling-check/reports >> /home/clawdy/.openclaw/workspace/tmp/creative-tooling-check/reports/creative-review-weekly-cleanup.log 2>&1
```

Praktisch effect:
- ruimt oude reports, daglogs en cleanup-logs op volgens preset `balanced`
- schrijft tegelijk JSONL audit-events naar `creative-review-cleanup-log-YYYYMMDD.jsonl`
- houdt stdout/stderr apart beschikbaar in een gewone cron-logfile voor snelle foutinspectie

## Auditlog-inspectie nu beschikbaar
`scripts/creative-log-summary.py` vat bestaande creative daylogs en cleanup-logs samen zonder handmatig JSONL te hoeven lezen.

Ondersteunde routes:
- `daylog` → telt review-events, profielen, exit-codes en totalen per mediatype
- `cleanup` → telt cleanup-events, kandidaat-artifacts, deletes en laatste cleanup-run

Voorbeelden:
```bash
python3 scripts/creative-log-summary.py daylog --log-dir tmp/creative-tooling-check/reports
python3 scripts/creative-log-summary.py cleanup --log-dir tmp/creative-review-cleanup-log-test/logs
python3 scripts/creative-log-summary.py daylog --log-dir tmp/creative-tooling-check/reports --format json
```

Live geverifieerd op 2026-04-13:
- daylog-samenvatting op `tmp/creative-tooling-check/reports` gaf `event-count=8`, alle `exit-codes=0`, en aggregate totalen `files_total=24`, `files_ok=24`, `files_warning=0`
- cleanup-samenvatting op `tmp/creative-review-cleanup-log-test/logs` gaf `event-count=2`, `candidate-total=4`, `deleted-total=2`, met laatste event `weekly-cleanup`
- JSON-output werkt voor beide routes en bevat ook `latest_event`, `log_dir` en de gebruikte logbestanden

## Smoke-wrapper nu beschikbaar
`scripts/creative-smoke.py` bundelt een vaste creative-review of cleanup-run direct met een logsamenvatting, zodat cron-nazicht en snelle handmatige checks één kort commando worden.

Ondersteunde routes:
- `review-daylog`
- `cleanup-audit`
- `full-cycle`
- `full-cycle-brief`

Voorbeelden:
```bash
python3 scripts/creative-smoke.py review-daylog --format json
python3 scripts/creative-smoke.py cleanup-audit --format json --report-dir tmp/creative-review-cleanup-log-test/reports --cleanup-log-dir tmp/creative-review-cleanup-log-test/logs
python3 scripts/creative-smoke.py full-cycle-brief
python3 scripts/creative-smoke.py full-cycle-brief --format json --consumer-out tmp/creative-tooling-check/reports/creative-smoke-consumer.json
python3 scripts/creative-smoke.py full-cycle-brief --consumer-preset board-text
python3 scripts/creative-smoke.py full-cycle-brief --consumer-preset board-json --format json
python3 scripts/creative-smoke.py full-cycle-brief --consumer-preset eventlog-jsonl --format json
python3 scripts/creative-smoke.py full-cycle-brief --format json --consumer-bundle board-suite
```

Live geverifieerd op 2026-04-13:
- `review-daylog --format json` gaf direct een daglogsamenvatting met `event_count=12`, `files_total=36`, `files_ok=36`, `files_warning=0`
- `cleanup-audit --format json` gaf direct een cleanup-samenvatting met `event_count=4`, `candidate_total=4`, `deleted_total=2`, laatste event `weekly-cleanup`
- `full-cycle-brief` gaf compacte statusoutput met alleen pass/fail plus kerngetallen, in tekst én JSON
- `full-cycle-brief --format json --consumer-out .../creative-smoke-consumer.json` schreef dezelfde compacte smoke-status ook direct weg als consumer-artifact; dezelfde route werkt ook als tekstbestand, en `--consumer-format jsonl --consumer-append` maakt append-vriendelijke eventlogs mogelijk
- nieuwe vaste `--consumer-preset` routes werken nu ook direct zonder losse padflags: `board-json` schrijft naar `tmp/creative-tooling-check/reports/creative-smoke-consumer.json`, `board-text` naar `.../creative-smoke-consumer.txt`, en `eventlog-jsonl` appendt naar `.../creative-smoke-consumer.jsonl`
- nieuwe `--consumer-bundle board-suite` schrijft in één smoke-run meteen alle drie standaard consumer-artifacts weg, zodat een vaste cron/producer niet drie losse runs hoeft te doen
- `full-cycle-brief --format json --consumer-bundle board-suite` is live geverifieerd met nacheck van alle drie geschreven artifacts plus stdout-JSON
- wrapperbug rond optionele flags is direct opgelost door over te schakelen van remainder-parsing naar `parse_known_args()`, zodat `--report-dir` en `--cleanup-log-dir` betrouwbaar doorkomen

Nut:
- één kort commando voor run + auditcontrole
- een nog compactere route voor cron-nazicht of statuschecks
- smoke-status kan nu ook direct landen in een simpel cron- of board-consumerbestand
- minder kans op verkeerde logmap of losse naverwerking

## Vaste producer-wrapper nu beschikbaar
`scripts/creative-smoke-producer.py` koppelt de nieuwe consumer-presets aan korte producer-modes, zodat een cron of andere producer straks niet meer alle smoke-details hoeft te kennen.

Producer-modes:
- `board` → draait één smoke-run met bundle `board-pair` en vult zo tegelijk `board-json` en `board-text`
- `eventlog` → appendt naar `eventlog-jsonl`
- `all` → draait één smoke-run met bundle `board-suite` en vult zo tegelijk JSON, tekst en eventlog

Voorbeelden:
```bash
python3 scripts/creative-smoke-producer.py board --quiet
python3 scripts/creative-smoke-producer.py eventlog --quiet
python3 scripts/creative-smoke-producer.py all --quiet
```

Voorbeeld-cronregels:
```bash
*/30 * * * * cd /home/clawdy/.openclaw/workspace && python3 scripts/creative-smoke-producer.py board --quiet
15 */2 * * * cd /home/clawdy/.openclaw/workspace && python3 scripts/creative-smoke-producer.py all --quiet
```

Aanbeveling:
- gebruik `board` voor lichte, frequente board-publicatie
- gebruik `all` alleen als ook de appendende JSONL-eventlog periodiek moet worden bijgewerkt

Live geverifieerd op 2026-04-13:
- `board --quiet` gaf groen terug met één producer-step:
  - `full-cycle-brief --consumer-bundle board-pair --format json: exit=0`
- `eventlog --quiet` gaf groen terug:
  - `full-cycle-brief --consumer-preset eventlog-jsonl --format json: exit=0`
- `all --quiet` gaf groen terug met één producer-step:
  - `full-cycle-brief --consumer-bundle board-suite --format json: exit=0`
- artifacts bevestigd in `tmp/creative-tooling-check/reports/creative-smoke-consumer.{json,txt,jsonl}`
- een eerste producer-wrapperbug slikte `--quiet` door naar child-flags; direct hersteld door over te schakelen naar `parse_known_args()`

Nut:
- één stabiele producer-call voor cron of andere automation
- minder kans dat een consumer-preset verkeerd of onvolledig wordt aangeroepen
- board/all-producers hoeven nu niet meer meerdere volledige smoke-runs achter elkaar te doen
- producer en consumer zijn nu als vaste lagen gescheiden

## Compacte smoke-status nu geland in boards
`clawdy-brief.py` en `statusboard.py` nemen de compacte creative smoke-status nu direct mee via `creative-smoke.py full-cycle-brief --format json`.

Live geverifieerd op 2026-04-13:
- `python3 scripts/clawdy-brief.py --json` bevat nu ook `creative_smoke` met `ok: true`
- `python3 scripts/statusboard.py` toont nu expliciet:
  - `creative smoke: ok (review-daylog: 108/108 ok, 0 warnings; cleanup-audit: cand 0, del 0)`

Nut:
- compacte creative-health landt nu in een bestaande board-consumer
- heartbeat- en statuschecks hoeven die info niet meer apart op te vragen
- de smoke-output is nu echt onderdeel van het operationele cockpitbeeld

## Kind-filtering nu beschikbaar
`scripts/media-sanity-check.py` ondersteunt nu ook `--kind`, zodat batch-checks gericht alleen `audio`, `image` en/of `video` meenemen.

Voorbeelden:
```bash
python3 scripts/media-sanity-check.py --dir tmp/creative-tooling-check --kind audio image --summary-by-kind
python3 scripts/media-sanity-check.py --dir tmp/creative-tooling-check --kind video --jsonl --jsonl-summary-only
```

Live geverifieerd op 2026-04-12:
- `--kind audio image` gaf schoon `summary: total=5 ok=5 warnings=0` met `audio=2` en `image=3`
- `--kind video --jsonl --jsonl-summary-only` gaf een compact event met `total=3 ok=3 warnings=0`

Nut:
- gerichte checks per outputtype zonder handmatig paden te splitsen
- compacter voor CI, triage en vervolgacties per mediafamilie
