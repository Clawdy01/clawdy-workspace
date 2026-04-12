# STATUS.md

## Operational notes
- Exchange Taken wordt nu gebruikt als operationele takenlijst naast deze statusbestanden.
- Exchange Agenda wordt nu actief gebruikt voor agenda-uitleesroutes.

## Now
- Exchange SE on-prem is nu het primaire spoor
- Doel: task lifecycle en nuttige mailbox/agenda samenvattingen verder aanscherpen nu de eerste echte read/write EWS-actie bevestigd is
- GitHub is afgerond als actief spoor; alleen nog onderhoud via auto-push

## Next
- Exchange kalender/taken workflow verder opzetten op basis van on-prem routes
- Daarna mail workflow slimmer maken
- Creative tooling/workflows voor image/audio/video verbeteren
- Secrets / password workflow netter maken

## Blocked
- Goede beeldgeneratie-route ontbreekt nog in deze runtime, dus betere image-remakes wachten op sterkere/lokale modelroute
- Control UI via LAN zonder SSH vraagt later nog een nette HTTPS-route

## Done
- GitHub-track afgerond: private repo bestaat, SSH-auth werkt, eerste push bevestigd, hourly auto-push actief
- Exchange-track eerste echte actie bevestigd: Autodiscover + EWS werken, unread inbox-check gelukt, kalenderroute werkt, en een verouderde GitHub-taak is via EWS op `Completed` gezet en teruggelezen
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
