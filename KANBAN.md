# KANBAN.md

## Execution guardrails
- Eén primair spoor tegelijk. Alleen het primaire spoor krijgt actieve bouwtijd totdat het klaar of echt geblokkeerd is.
- Huidig primair spoor: GitHub
- Parallel mag alleen voor klein onderhoud of wanneer het primaire spoor extern wacht.
- Elk actief spoor moet een concrete definition of done hebben.
- Als een spoor geen tastbaar resultaat oplevert binnen korte tijd, stop en meld de blocker in plaats van door te drijven.
- Harde tijdsgrens: een taak/spoor moet binnen maximaal 1 uur afgerond zijn, of expliciet hard geblokkeerd met bewijs, of opgesplitst worden in kleinere deliverables.
- Geparkeerde of legacy sporen mogen niet als actief in updates verschijnen.

## Definition of done
- GitHub: account bestaat, login werkt, private repo bestaat, eerste push bevestigd
- Exchange SE on-prem: EWS/Autodiscover helper werkt, daarna eerstvolgende bruikbare mailbox- of kalenderactie bevestigd
- Photo editing / image workflows: alleen opnieuw actief zodra er een echte bruikbare modelroute beschikbaar is

## Now
- GitHub: private Clawdy account + private repo + eerste push
- Exchange SE on-prem: wacht als parallel spoor tot GitHub klaar of echt geblokkeerd is
- Photo editing / image workflows: geparkeerd tot betere model/hardware-route

## Blocked
- Geen expliciete blocker hier; open directe deliverables uit chat hebben voorrang als ze bestaan
- GitHub is nog niet geblokkeerd, alleen nog niet afgerond

## Next
- Exchange mailbox/kalender/taken workflow structureren op basis van on-prem entry points, niet Graph
- Creative tooling/workflows verdiepen voor image/audio/video
- Onderzoek naar betere identity-preserving photo edit modellen/workflows
- Secrets/workflows verder opruimen nu Bitwarden werkt

## Backlog
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
- Proton als actief werkspoor, alleen nog bewaren als oude web-automation casus/legacy referentie
- Microsoft Graph / tenant-id / client-id voor Exchange, geparkeerd tenzij later expliciet een echte M365/hybrid route blijkt
- Ski-foto edit, opnieuw oppakken met betere modelroute
- Diepere publieke profielronde / LinkedIn-context later netter afmaken

## Done
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
