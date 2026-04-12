# Exchange / Microsoft Graph setup checklist

> Status: legacy / geparkeerd. Niet gebruiken als hoofdroute voor de huidige lokale Exchange SE omgeving, tenzij later expliciet een echte M365/hybrid Graph-route blijkt.

Datum: 2026-04-11

## Doel
De eerste read-only proof-of-route voor Exchange kalender en Microsoft To Do klein en controleerbaar opzetten.

## Benodigde env vars
- `MSGRAPH_TENANT_ID`
- `MSGRAPH_CLIENT_ID`
- optioneel `MSGRAPH_REDIRECT_URI` (default in helper: `http://localhost`)
- later optioneel `MSGRAPH_TODO_LIST_ID`

## Azure app registration
1. Maak een nieuwe app registration.
2. Kies delegated auth voor Christian zelf.
3. Voeg alleen deze Graph delegated permissions toe:
   - `Calendars.Read`
   - `Tasks.Read`
4. Voeg een local/manual redirect URI toe, bijvoorbeeld `http://localhost`.
5. Geef admin consent alleen als de tenant dat vereist.

## Eerste proof-of-route
1. Calendar window:
   - `GET /me/calendarView?startDateTime=...&endDateTime=...`
2. Todo lists:
   - `GET /me/todo/lists`
3. Taken uit gekozen lijst:
   - `GET /me/todo/lists/{list-id}/tasks`

## Handige lokale helper
Gebruik:

```bash
python3 scripts/graph-setup-summary.py
python3 scripts/graph-setup-summary.py --json
python3 scripts/graph-setup-summary.py --tenant-id '...' --client-id '...'
python3 scripts/graph-auth-start.py
python3 scripts/graph-auth-start.py --json
python3 scripts/graph-auth-start.py --tenant-id '...' --client-id '...'
python3 scripts/graph-proof.py --code 'http://localhost/?code=...'
python3 scripts/graph-proof.py --code 'http://localhost/?code=...' --code-verifier '...'
python3 scripts/graph-proof.py --code 'http://localhost/?code=...' --code-verifier '...' --tenant-id '...' --client-id '...'
python3 scripts/graph-proof.py --access-token '...'
```

Die helpers laten direct zien:
- welke env vars nog ontbreken
- welke scopes/scope-combinatie nu aanbevolen is
- een authorize URL zodra tenant/client-id bekend zijn
- een PKCE `code_verifier` + `code_challenge` set voor een nette public-client flow
- de token endpoint URL
- kant-en-klare `export ...` regels voor lokale env-setup
- concrete `curl` voorbeelden voor token exchange, agenda en To Do
- de concrete eerste Graph-routes voor kalender en taken
- een lokale proof-run die een auth code of redirect URL kan omzetten naar een token en daarna direct `calendarView`, `todo/lists` en optioneel `tasks` test
- CLI overrides voor tenant/client/redirect/scope zodat de eerste test ook zonder voorafgaande `export ...` stap kan

## Aanbevolen volgorde
1. Tenant/client-id invullen
2. `python3 scripts/graph-setup-summary.py` draaien en de `export ...` regels overnemen
3. `python3 scripts/graph-auth-start.py` draaien en de authorize URL openen
4. Bewaar de getoonde `code_verifier` tijdelijk voor de token exchange / proof-run
5. Auth code terugplakken in de token-exchange `curl`, of direct in `python3 scripts/graph-proof.py --code 'http://localhost/?code=...' --code-verifier '...' --tenant-id '...' --client-id '...'`
6. Eerst alleen read-routes laten werken, bijvoorbeeld via de door `graph-auth-start.py` getoonde volledige proof-helperregel
7. Pas daarna beslissen over write-scope of mail-koppeling
