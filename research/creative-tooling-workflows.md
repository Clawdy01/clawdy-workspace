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

## Aanbevolen volgende stap
- Kleine follow-up: helper uitbreiden met optionele thresholds/warnings, bv. minimale resolutie, verwachte sample rate of lege frame-export detecteren
