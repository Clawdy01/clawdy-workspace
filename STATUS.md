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
- Volgende stap is optionele aggregate-warnings of exit-codes per batch-run toevoegen voor CI-achtige checks
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
