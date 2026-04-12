# Memory techniques recommendation

Datum: 2026-04-11

## Doel
Een concreet betere geheugenaanpak kiezen voor de huidige OpenClaw setup, zonder meteen over te stappen op zware infra of een vector database.

## Huidige basis
De huidige opzet is al verrassend sterk:
- `memory/YYYY-MM-DD.md` als episodisch logboek
- `MEMORY.md` als gecureerd langetermijngeheugen
- `AGENTS.md` / skills / scripts als procedureel geheugen

Dat sluit goed aan op de klassieke driedeling:
- episodisch: wat gebeurde er
- semantisch: wat moet blijvend onthouden worden
- procedureel: hoe werken we hier

## Beoordeling van betere technieken

### 1. Blijven werken met gescheiden episodisch / semantisch / procedureel geheugen
**Aanrader: ja, behouden en explicieter maken**

Waarom:
- eenvoudig
- uitlegbaar voor Christian
- makkelijk te reviewen en corrigeren
- weinig risico op verborgen of "hallucinerende" memory-lagen

### 2. Retrieval op semantische relevantie in plaats van alles vooraf inladen
**Aanrader: ja, al deels aanwezig via `memory_search`**

Waarom:
- minder contextvervuiling
- lagere tokenkosten
- minder kans dat oude of irrelevante details het gesprek kapen

Advies:
- gebruik `memory_search` standaard voor vragen over eerdere beslissingen, voorkeuren, personen en todo's
- laad alleen gerichte snippets, niet hele bestanden

### 3. Regelmatige consolidatie van daily notes naar curated memory
**Aanrader: sterk ja**

Waarom:
- dagelijkse logs groeien snel en bevatten veel ruis
- nuttige lessen verdwijnen anders in ruwe notities
- dit voorkomt dat `MEMORY.md` achterloopt op wat recent geleerd is

Beste vorm voor deze setup:
- 2-3 keer per week: recente `memory/*.md` nalopen
- blijvende lessen/prompts/voorkeuren samenvatten naar `MEMORY.md`
- tijdelijke details juist níet promoveren

### 4. Samenvattingslagen / rolling summaries
**Aanrader: beperkt, alleen per project of deliverable**

Waarom niet overal:
- algemene rolling summaries driften snel
- ze kunnen feitelijke details platdrukken of vertekenen

Wel nuttig voor:
- lange deliverables
- researchtracks
- migraties of herstelwerk

Beste vorm:
- per groot spoor een klein statusbestand of research-notitie
- liever taakgebonden samenvattingen dan één globale mega-summary

### 5. Vector DB / embedding store voor alles
**Aanrader: nu nog niet**

Waarom:
- extra complexiteit
- moeilijker te inspecteren
- huidige geheugenschaal lijkt nog prima met files + search
- risico op een slim-ogende maar minder betrouwbare laag

Pas zinvol als:
- memory-bestanden echt te groot worden voor file-search
- er veel cross-project retrieval nodig is
- snelheid of recall aantoonbaar tekortschiet

## Concreet aanbevolen model voor Christian

### Bewaren als drie lagen
1. **Daglaag**
   - `memory/YYYY-MM-DD.md`
   - rauwe gebeurtenissen, blockers, besluiten, losse observaties

2. **Curated laag**
   - `MEMORY.md`
   - alleen stabiele voorkeuren, belangrijke context, bewezen lessen

3. **Workflowlaag**
   - `AGENTS.md`, `TOOLS.md`, skills, scripts
   - terugkerende werkwijzen, checks, guardrails en automatisering

## Kleine verbeteringen met hoge opbrengst

### A. Voeg vaste tags/koppen toe aan daily memory
Bijvoorbeeld:
- `Besluit:`
- `Les:`
- `Blocker:`
- `Voorkeur:`
- `Deliverable:`

Waarom:
- makkelijker later consolideren
- makkelijker semantisch zoeken
- minder kans dat belangrijke dingen in proza verdwijnen

### B. Promoveer alleen bewezen dingen naar `MEMORY.md`
Vuistregel:
- pas opslaan in `MEMORY.md` als iets herbruikbaar, stabiel of duidelijk belangrijk is
- eenmalige incidenten blijven in daily memory of projectnotities

### C. Gebruik projectnotities voor lange sporen
Voorbeeld:
- `research/...`
- eventueel later `projects/...`

Waarom:
- voorkomt dat `MEMORY.md` een dump wordt
- houdt open loops zichtbaar buiten de chat zelf

### D. Maak memory maintenance expliciet als routine
Aanrader:
- heartbeat pakt om de paar dagen een korte consolidatieronde
- doel is niet "meer notities", maar betere compressie en duidelijkere lessen

## Aanbevolen volgende stap
De beste eerstvolgende verbetering is niet een nieuwe database of fancy memory stack.

**Aanbevolen eerstvolgende stap:**
- dagelijkse memory notities voortaan iets structureler schrijven met `Besluit`, `Les`, `Blocker`, `Voorkeur`, `Deliverable`
- daarna tijdens heartbeat periodiek de blijvende lessen promoveren naar `MEMORY.md`

Dat is de hoogste opbrengst per moeite voor deze setup.

## Korte conclusie
De juiste richting is:
- huidige file-based memory behouden
- retrieval/selectief lezen blijven gebruiken
- consolidatie strakker maken
- projectnotities gebruiken voor lange sporen
- nog niet naar vector memory of zwaardere infra gaan

Dat is waarschijnlijk betrouwbaarder, goedkoper en beter uitlegbaar dan een complexere memory-stack op dit moment.
