# STATUS.md

## Operational notes
- Exchange Taken wordt nu gebruikt als operationele takenlijst naast deze statusbestanden.
- Exchange Agenda wordt nu actief gebruikt voor agenda-uitleesroutes.

## Now
- Publieke profielronde / LinkedIn-context is nu het primaire spoor
- Eerste concrete stap gezet: audit + headline/About-draft vastgelegd in `research/linkedin-profile-round-1.md`
- Tweede concrete stap gezet: rewrite-kader + before/after-werkblad toegevoegd zodat de echte LinkedIn-tekst direct vergeleken kan worden
- Derde concrete stap gezet: bewijsbare profielclaims, accomplishment-bullets en veilige formuleringen uit de workspace vastgelegd in `research/linkedin-proof-points.md`
- Vierde concrete stap gezet: publiek verifieerbare context uit CleverIT/CleverEnable-teambronnen en een extern interview toegevoegd aan `research/linkedin-proof-points.md`
- Extra gerichte lookup gedaan, maar nog steeds geen bevestigde huidige LinkedIn-tekst of profielmatch gevonden
- Volgende stap: zodra headline/About of LinkedIn-URL beschikbaar is, het gerichte before/after voorstel invullen met minimaal 2 bewijsblokken uit `research/linkedin-proof-points.md`
- GitHub is afgerond als actief spoor; alleen nog onderhoud via auto-push

## Next
- Mail workflow slimmer maken
- Creative tooling/workflows voor image/audio/video verbeteren
- Secrets / password workflow netter maken

## Blocked
- LinkedIn rewrite ronde 2 wacht op bronmateriaal: huidige headline/About of exacte LinkedIn-URL is nog niet beschikbaar; lokale workspace-search, extra gerichte publieke LinkedIn-lookups en aanvullend publiek contextonderzoek op 2026-04-12 bevestigden die tekst nog steeds niet
- Goede beeldgeneratie-route ontbreekt nog in deze runtime, dus betere image-remakes wachten op sterkere/lokale modelroute
- Control UI via LAN zonder SSH vraagt later nog een nette HTTPS-route

## Done
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
