# KANBAN.md

## Execution guardrails
- Operationele werklijst staat ook in Exchange Taken; KANBAN blijft de lokale bron voor structuur en prioriteit.
- Eén primair spoor tegelijk. Alleen het primaire spoor krijgt actieve bouwtijd totdat het klaar of echt geblokkeerd is.
- Huidig primair spoor: publieke profielronde / LinkedIn-context
- Parallel mag alleen voor klein onderhoud of wanneer het primaire spoor extern wacht.
- Als het primaire spoor leeg is of extern wacht, herbeoordeel proactief taken, geparkeerde taken en backlog op wat nu wel uitgevoerd kan worden.
- Elk actief spoor moet een concrete definition of done hebben.
- Als een spoor geen tastbaar resultaat oplevert binnen korte tijd, stop en meld de blocker in plaats van door te drijven.
- Harde tijdsgrens: een taak/spoor moet binnen maximaal 1 uur afgerond zijn, of expliciet hard geblokkeerd met bewijs, of opgesplitst worden in kleinere deliverables.
- Na afronding van een primair spoor: eerst KANBAN/STATUS direct syncen, daarna in dezelfde werksessie het volgende spoor activeren.
- Geparkeerde of legacy sporen mogen niet als actief in updates verschijnen.

## Definition of done
- GitHub: account bestaat, login werkt, private repo bestaat, eerste push bevestigd
- Exchange SE on-prem: mailbox, agenda en taken hebben een bruikbare on-prem EWS-route voor lezen én de eerstvolgende nuttige actie is bevestigd
- Photo editing / image workflows: alleen opnieuw actief zodra er een echte bruikbare modelroute beschikbaar is

## Now
- Publieke profielronde / LinkedIn-context: eerste audit + headline/About-draft staan vast in `research/linkedin-profile-round-1.md`; rewrite-kader en before/after-werkblad staan nu klaar
- Nieuwe concrete stap afgerond: bewijsbare profielclaims en accomplishment-bullets uit de workspace staan nu in `research/linkedin-proof-points.md`, zodat ronde 2 niet alleen op toon maar ook op harde voorbeelden leunt
- Extra concrete stap afgerond: publiek verifieerbare context uit CleverIT/CleverEnable en een extern interview is toegevoegd aan `research/linkedin-proof-points.md`, zodat de rewrite straks ook op zichtbare externe profielsignalen kan steunen
- Volgende stap blijft: de echte huidige LinkedIn-tekst ernaast leggen en de gerichte rewrite invullen met minimaal 2 bewijsblokken uit `research/linkedin-proof-points.md`
- Verplichte anti-stall regel: als dit spoor stilvalt zonder blocker, direct één concrete stap uitvoeren of de blocker met bewijs vastleggen
- GitHub: draait nu als onderhoud via automatische push, geen actief primair spoor meer
- Photo editing / image workflows: geparkeerd tot betere model/hardware-route

## Blocked
- LinkedIn rewrite ronde 2 blijft inhoudelijk geblokkeerd op bronmateriaal: huidige headline/About of exacte LinkedIn-URL ontbreekt nog; extra lokale search, gerichte publieke LinkedIn-lookups en publiek contextonderzoek op 2026-04-12 leverden wel ondersteunende CleverIT/CleverEnable-bronnen op, maar nog geen bevestigde live LinkedIn-profieltekst

## Next
- Creative tooling/workflows verdiepen voor image/audio/video
- Secrets/workflows verder opruimen nu Bitwarden werkt
- Daarna Mac migratieplan en lokale LLM/media-workflows oppakken
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
- Exchange summary aangescherpt: onderscheid tussen actiegerichte vs notificatie-unread, signalering van afspraken binnen 24 uur, en overdue actieve taken zodat `next_action` minder snel op ruis blijft hangen
- Exchange huidige actieve taak afgerond: summary live geverifieerd en Exchange-taak `Exchange SE: mailbox/agenda helper verder uitbouwen` staat nu op Completed
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
