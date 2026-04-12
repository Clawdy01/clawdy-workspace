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

## Aanbevolen volgende stap
- Kleine follow-up: preset include-sets of pad-aliasen bundelen voor nog vaker terugkerende scanroutes

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
