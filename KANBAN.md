# KANBAN.md

## Execution guardrails
- Operationele werklijst staat ook in Exchange Taken; KANBAN blijft de lokale bron voor structuur en prioriteit.
- Eén primair spoor tegelijk. Alleen het primaire spoor krijgt actieve bouwtijd totdat het klaar of echt geblokkeerd is.
- Huidig primair spoor: Creative tooling/workflows verdiepen voor image/audio/video
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
- Creative tooling/workflows verdiepen voor image/audio/video is nu het primaire spoor
- Eerste nulmeting vastgelegd in `research/creative-tooling-baseline.md` met bevestigde lokale CLI-routes voor ffmpeg, ImageMagick, sox en yt-dlp
- Kleine interne workflow-notitie staat nu in `research/creative-tooling-workflows.md`, met live geteste paden voor video-clippen, frame-export, audio-normalisatie en simpele image-afleidingen
- Eerste helper staat nu live: `scripts/video-clip.py` voor video-clip + frame-export, lokaal geverifieerd op synthetische testvideo
- Tweede helper staat nu live: `scripts/media-sanity-check.py` voor snelle inspectie van video/image/audio-output, live geverifieerd op sample video/audio/image plus JSON-output
- Volgende stap: helper aanscherpen met optionele thresholds/warnings voor resolutie, sample rate of lege outputdetectie
- GitHub: draait nu als onderhoud via automatische push, geen actief primair spoor meer
- Photo editing / image workflows: generatieve identity-preserving edits blijven geparkeerd tot betere model/hardware-route

## Blocked
- Geen harde blocker op het huidige creative-tooling spoor; nulmeting en workflow-inventaris zijn bevestigd en helperbouw kan lokaal doorgaan
- Betere identity-preserving photo edits blijven wel geblokkeerd op een sterkere/lokale modelroute

## Next
- Secrets/workflows verder opruimen nu Bitwarden werkt
- Daarna Mac migratieplan en lokale LLM/media-workflows oppakken
- Onderzoek naar betere identity-preserving photo edit modellen/workflows
- Regelmatige research-workflows opzetten voor onderwerpen die Christian wil volgen

## Backlog
- Eventuele publieke LinkedIn-tekst later netter maken zodra dat nog nuttig blijkt, maar pas na de interne contextopbouw voor ondersteuning
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
- Christian contextopbouw via LinkedIn/profielinformatie afgerond als interne ondersteuningscontext in `research/christian-support-context.md`, met achtergrond, rollen, projecten en actuele focus
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
- Creative tooling helper gebouwd en live geverifieerd: `scripts/video-clip.py` maakt korte clips plus frame-export uit video
- Creative tooling helper gebouwd en live geverifieerd: `scripts/media-sanity-check.py` inspecteert video, audio en image-output met tekst- en JSON-output
