# Creative tooling baseline

Doel: eerste nuchtere nulmeting voor image/audio/video-workflows in deze runtime, zodat vervolgstappen op echte beschikbare tooling kunnen leunen.

## Beschikbare CLI-tooling bevestigd op 2026-04-12
- ffmpeg: aanwezig (`ffmpeg 6.1.1`)
- ffprobe: aanwezig
- ImageMagick: aanwezig via `convert` / `identify` (`6.9.12-98`)
- sox: aanwezig (`14.4.2`)
- yt-dlp: aanwezig (`2024.04.09`)
- Python 3: aanwezig

## Eerste implicatie per domein
### Video
- basis extractie, transcode, clippen en frame-export zijn direct haalbaar via ffmpeg

### Audio
- basis conversie, normalisatie en inspectie zijn direct haalbaar via ffmpeg + sox

### Image
- klassieke image-bewerkingen en formatconversies zijn haalbaar via ImageMagick
- er is geen bevestigde moderne identity-preserving generative edit route in deze runtime

## Bevestigde beperking
- `magick` ontbreekt als los commando; de host gebruikt ImageMagick 6-tools (`convert`, `identify`)
- de eerder bekende blocker blijft staan voor geavanceerde modelgedreven photo remakes of betere identity-preserving edits

## Nuttige vervolgstappen
1. klein script of skillpad kiezen voor frame/clip-extractie uit video
2. basis image/audio/video use-cases bundelen in één interne workflow-notitie
3. pas daarna beoordelen welke generatieve modelroute echt ontbreekt voor de geparkeerde photo-edit track
