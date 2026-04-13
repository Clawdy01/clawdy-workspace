# Secrets / password workflow round 1

Doel: het nieuwe primaire spoor meteen scherp maken met een kleine inventaris van waar secrets nu echt gebruikt worden en wat eerst opgeschoond moet worden.

## Bevestigde huidige opslagpunten
- `state/secrets.json` via `scripts/workspace_secrets.py`
- `state/mail-config.json` via `scripts/workspace_secrets.py`

## Bevestigde loader-modules
- `scripts/workspace_secrets.py`
- `scripts/secrets.py`

Observatie:
- deze twee Python-modules zijn nu functioneel dubbel; ze bevatten dezelfde loader-logica voor `secrets.json` en `mail-config.json`
- actieve consumers gebruiken op dit moment `workspace_secrets.py`; er is in de huidige workspace geen actieve import gevonden van `scripts/secrets.py`

## Bevestigde actieve consumers
### Mail / Exchange
- `scripts/mail_imap.py`
- `scripts/mail-auth-check.py`
- `scripts/exchange-ews-check.py`
- `scripts/exchange-ews-tool.py`

### Proton
- `scripts/proton-request-verification-code.py`
- `scripts/proton-use-verification-code.py`
- `scripts/proton-continue-password-setup.py`

### Bitwarden browser automation
- `browser-automation/bitwarden_extract_github_fields.js`
- `browser-automation/bitwarden_full_login_inspect_github_row.js`
- `browser-automation/bitwarden_full_login_search.js`
- `browser-automation/bitwarden_click_github_debug.js`
- `browser-automation/bitwarden_full_login_get_item.js`

## Eerste concrete opruimkans
1. één canonical secrets-loader kiezen
2. overbodige dubbele module verwijderen of expliciet als compat-laag markeren
3. daarna pas secret-namen en workflow-routes normaliseren

## Aanbevolen volgende stap
- kleine code-opruimronde: `scripts/secrets.py` omzetten naar dunne compat-wrapper of volledig vervangen door één canonieke loader, zodat secrets-routing niet meer dubbel gedefinieerd staat

## Update ronde 2
- `scripts/secrets.py` is inmiddels een expliciete compat-shim bovenop `workspace_secrets.py`
- `scripts/workspace_secrets.py` ondersteunt nu ook genormaliseerde canonieke namen met alias-resolutie:
  - `mail.password` ↔ `mail_password`
  - `proton.password` ↔ `proton_pass_password`
  - `github.password` ↔ `github_account_password`
- `load_mail_config()` leest nu via de canonieke route `mail.password`, maar legacy sleutels blijven werken

## Nieuwe directe vervolgstap
1. consumers geleidelijk naar canonieke namen laten wijzen (`mail.password`, `proton.password`, `github.password`)
2. daarna pas, in een aparte veilige migratieronde, de JSON-opslag zelf eventueel herschrijven
3. pas na consumer-migratie legacy aliassen verwijderen

## Update ronde 3
- de drie actieve Proton-consumers lezen nu canoniek via `proton.password`:
  - `scripts/proton-request-verification-code.py`
  - `scripts/proton-use-verification-code.py`
  - `scripts/proton-continue-password-setup.py`
- verificatie zonder secretwaarden:
  - `python3 -m py_compile ...` op de drie Proton-scripts plus `workspace_secrets.py` kwam schoon terug
  - `get_secret('proton.password') is not None` kwam `True` terug
  - `grep` op de Proton-scripts vond geen directe legacy read van `proton_pass_password` meer; alleen de alias-definitie in `workspace_secrets.py` bleef bewust staan

## Nieuwe directe vervolgstap na ronde 3
1. mail- en GitHub-consumers nalopen op directe legacy secret-reads
2. daarna pas beoordelen of `state/secrets.json` veilig naar canonieke sleutels kan worden herschreven
3. legacy aliassen pas verwijderen als alle actieve consumers omgezet én geverifieerd zijn

## Update ronde 4
- mail-consumers aan de Python-kant bleken al canoniek via `load_mail_config()` te lopen; `mail-auth-check.py` heeft geen directe legacy secret-read
- de nagekeken GitHub/Bitwarden automation-consumers tonen ook geen directe read van `github_account_password`
- brede `grep` over `scripts/` en `browser-automation/` vond voor mail/GitHub alleen nog de bewuste alias-definities in `workspace_secrets.py`

## Nieuwe directe vervolgstap na ronde 4
1. alleen nog beoordelen of er buiten de actieve consumers verborgen shell/JS-routes bestaan die `state/secrets.json` direct lezen
2. als die scan schoon blijft, een aparte veilige migratieronde voorbereiden voor canonieke JSON-sleutels
3. legacy aliassen pas verwijderen als ook die laatste scan en migratiecontrole groen zijn

## Update ronde 5
- workspacebrede scan buiten `state/`, `tmp/` en `.git/` vond voor secrets-routing alleen nog:
  - documentatie/verwijzingen in `research/`, `KANBAN.md` en `STATUS.md`
  - de bewuste alias-definities in `scripts/workspace_secrets.py`
  - de al omgezette Proton-consumers met canonieke `get_secret('proton.password')`
- er zijn in deze scan geen verborgen shell/JS-routes gevonden die `state/secrets.json` direct lezen of legacy sleutels `mail_password`, `proton_pass_password` of `github_account_password` consumeren
- nieuwe veilige migratie-helper toegevoegd: `scripts/secrets-normalize.py`
  - doet standaard alleen een dry-run
  - meldt alleen sleutelacties, nooit secretwaarden
  - blokkeert `--apply` automatisch bij conflicterende aliaswaarden
- verificatie zonder secretoutput:
  - `python3 -m py_compile scripts/secrets-normalize.py scripts/workspace_secrets.py scripts/secrets.py` kwam schoon terug
  - `python3 scripts/secrets-normalize.py --json` gaf `ok: true`, `conflicts: []` en een voorbereid migratieplan voor `mail.password`, `proton.password` en `github.password`

## Nieuwe directe vervolgstap na ronde 5
1. de canonieke JSON-migratie met `python3 scripts/secrets-normalize.py --apply` uitvoeren
2. daarna gericht verifiëren dat `state/secrets.json` alleen de canonieke sleutels bevat terwijl bestaande consumers blijven werken
3. pas daarna beoordelen of legacy alias-ondersteuning in code verwijderd kan worden

## Update ronde 6
- de canonieke JSON-migratie is uitgevoerd met `python3 scripts/secrets-normalize.py --apply`
- verificatie zonder secretoutput bevestigt dat `state/secrets.json` nu alleen nog `mail.password`, `proton.password` en `github.password` bevat; legacy sleutels zijn weg
- loader-check via `get_secret(...) is not None` bleef groen voor mail, Proton en GitHub
- tijdens de nacheck dook een kleine aliaslijst-bug op: `SECRET_ALIASES` bevatte per ongeluk ook de canonieke naam zelf, waardoor een dry-run spook-acties als `remove_alias` op dezelfde canonieke key kon tonen
- die aliasdefinitie is direct opgeschoond zodat alleen echte legacy sleutels nog als alias gelden
- `python3 -m py_compile ...` op de secrets-loader, normalize-helper en actieve Python-consumers bleef schoon

## Update ronde 7
- de legacy alias-ondersteuning is nu echt verwijderd uit `scripts/workspace_secrets.py`
- `SECRET_ALIASES` bevat alleen nog canonieke sleutels met lege aliaslijsten, en `get_secret()` resolveert daardoor alleen nog expliciete canonieke namen
- verificatie zonder secretoutput:
  - `python3 -m py_compile ...` op de secrets-loader, normalize-helper en actieve Python-consumers bleef schoon
  - `python3 scripts/secrets-normalize.py --json` gaf schoon `actions: []` en `conflicts: []`
  - loader-checks bleven groen voor `mail.password`, `proton.password` en `github.password`
  - legacy lookups `mail_password`, `proton_pass_password` en `github_account_password` geven nu terecht geen waarde meer terug

## Nieuwe directe vervolgstap na ronde 7
1. mail-, Proton- en GitHub-routes nog één keer gericht herverifiëren op de volledig opgeschoonde loader
2. als dat groen blijft, het secrets-spoor als functioneel afgerond markeren en het volgende primaire spoor activeren
1. `python3 scripts/secrets-normalize.py --json` opnieuw draaien en bevestigen dat de dry-run nu echt `actions: []` geeft zonder spook-acties
2. daarna beoordelen of alias-ondersteuning voor deze drie legacy sleutels al veilig uit code kan, of nog kort moet blijven bestaan als compat-laag
3. op basis daarvan KANBAN/STATUS bijwerken naar de volgende kleine secrets-cleanupstap
