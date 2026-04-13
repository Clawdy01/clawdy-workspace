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
