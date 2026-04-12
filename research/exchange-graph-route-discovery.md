# Exchange / Microsoft Graph route discovery

> Status: legacy / geparkeerd. Dit document beschrijft een mogelijke latere Graph-route, maar niet de huidige hoofdroute voor de lokale Exchange SE setup.

Datum: 2026-04-11

## Doel
Een smalle, bruikbare eerste Graph-route kiezen voor Exchange kalender/taken, zonder meteen te breed te permissieren.

## Aanbevolen eerste scope
Gebruik **delegated auth** met alleen de permissies die nodig zijn voor Christian zelf:

- `Calendars.Read` voor eigen agenda-events lezen
- `Tasks.Read` of `Tasks.ReadWrite` voor Microsoft To Do taken/lijsten
- optioneel later `Calendars.Read.Shared` als gedeelde/delegated agenda's nodig blijken
- optioneel later `Mail.Read` als mailcontext direct in dezelfde Graph-route nodig is

## Aanbevolen eerste routes
### Kalender
- `GET /me/calendar/events`
- `GET /me/calendars`
- `GET /me/calendarView?startDateTime=...&endDateTime=...`

Praktisch advies: voor een "wat komt eraan" workflow is `calendarView` het nuttigst, omdat die direct een tijdvenster teruggeeft.

### Taken
Gebruik **Microsoft To Do via Graph**, niet de oude Outlook tasks-route.

- `GET /me/todo/lists`
- `GET /me/todo/lists/{list-id}/tasks`

## Eerste concrete implementatieroute
1. App registration met delegated auth
2. Start alleen met `Calendars.Read` + `Tasks.Read`
3. Proof-of-route:
   - agenda komende 7 dagen via `calendarView`
   - alle todo-lijsten ophalen
   - taken uit 1 gekozen lijst ophalen
4. Pas daarna besluiten of write-permissions echt nodig zijn

## Waarom dit de beste eerste route lijkt
- kleinste bruikbare permissieset
- sluit direct aan op de gewenste Exchange kalender/taken workflow
- vermijdt legacy Outlook tasks API
- houdt mail los totdat duidelijk is dat die koppeling echt nodig is

## Bronnen
- Microsoft Graph overview
- Microsoft Graph calendar API docs
- Microsoft Graph To Do overview / todoTaskList docs
- Microsoft Graph permissions overview
