# KANBAN.md

## Execution guardrails
- Operationele werklijst staat ook in Exchange Taken; KANBAN blijft de lokale bron voor structuur en prioriteit.
- Eén primair spoor tegelijk. Alleen het primaire spoor krijgt actieve bouwtijd totdat het klaar of echt geblokkeerd is.
- Huidig primair spoor: Exchange SE on-prem
- Parallel mag alleen voor klein onderhoud of wanneer het primaire spoor extern wacht.
- Als het primaire spoor leeg is of extern wacht, herbeoordeel proactief taken, geparkeerde taken en backlog op wat nu wel uitgevoerd kan worden.
- Elk actief spoor moet een concrete definition of done hebben.
- Als een spoor geen tastbaar resultaat oplevert binnen korte tijd, stop en meld de blocker in plaats van door te drijven.
- Harde tijdsgrens: een taak/spoor moet binnen maximaal 1 uur afgerond zijn, of expliciet hard geblokkeerd met bewijs, of opgesplitst worden in kleinere deliverables.
- Geparkeerde of legacy sporen mogen niet als actief in updates verschijnen.

## Definition of done
- GitHub: account bestaat, login werkt, private repo bestaat, eerste push bevestigd
- Exchange SE on-prem: mailbox, agenda en taken hebben een bruikbare on-prem EWS-route voor lezen én de eerstvolgende nuttige actie is bevestigd
- Photo editing / image workflows: alleen opnieuw actief zodra er een echte bruikbare modelroute beschikbaar is

## Now
- Exchange SE on-prem: task lifecycle en nuttige mailbox/agenda samenvattingen verder aanscherpen nu de eerste echte read/write EWS-actie bevestigd is
- GitHub: draait nu als onderhoud via automatische push, geen actief primair spoor meer
- Photo editing / image workflows: geparkeerd tot betere model/hardware-route

## Blocked
- Geen open deliverables op dit moment

## Next
- Exchange mailbox/kalender/taken workflow verder structureren op basis van on-prem entry points
- Daarna publieke profiel / LinkedIn-context of andere bruikbare backlog opnieuw beoordelen
- Creative tooling/workflows verdiepen voor image/audio/video
- Onderzoek naar betere identity-preserving photo edit modellen/workflows
- Secrets/workflows verder opruimen nu Bitwarden werkt

## Backlog
- Diepere publieke profielronde / LinkedIn-context netter afmaken
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
- Ski-foto edit, opnieuw oppakken met betere modelroute

## Done
- GitHub private repo aangemaakt, SSH-auth ingesteld, eerste push bevestigd, hourly auto-push actief
- Exchange SE on-prem basisroute bevestigd: Autodiscover + EWS werken, unread inbox/kalendercheck gelukt, en een verouderde GitHub-taak is succesvol via EWS naar Completed gezet en teruggelezen
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
