#!/usr/bin/env bash
# Copy/paste template voor eerste Microsoft Graph delegated auth test

export MSGRAPH_TENANT_ID="<tenant-id>"
export MSGRAPH_CLIENT_ID="<client-id>"
# Optioneel, als de app een andere redirect URI gebruikt dan de default in de scripts
# export MSGRAPH_REDIRECT_URI="http://localhost"
# Optioneel, na `python3 scripts/graph-auth-start.py`
# export MSGRAPH_CODE_VERIFIER="<code-verifier-uit-helper>"

# Aanbevolen scopes voor delegated auth en eerste read-only proof
export MSGRAPH_SCOPE="offline_access openid profile Calendars.Read Tasks.Read"
