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

## Aanbevolen volgende stap
- Kleine follow-up: optionele aggregate-warnings of exit-codes per batch-run toevoegen voor CI-achtige checks
