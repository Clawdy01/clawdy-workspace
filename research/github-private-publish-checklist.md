# GitHub private publish checklist

Datum: 2026-04-11

## Doel
De workspace veilig voorbereiden voor een eerste push naar een private GitHub-repo, zonder persoonlijke state, memory of lokale runtime-restanten mee te publiceren.

## Huidige stand
- Git-branch: `master`
- Remote: nog niet ingesteld
- Eerste readiness-check: `python3 scripts/git-publish-readiness.py`

## Bekende risicopaden
Deze horen niet blind mee naar GitHub:
- `MEMORY.md`
- `memory/`
- `.openclaw/`
- `.venv-*` / `.venv/`
- `state/`

## Veilige volgorde
1. Draai `python3 scripts/git-publish-readiness.py`
2. Maak een publish-veilige selectie / `.gitignore`
3. Controleer welke tracked files lokaal/privacygevoelig zijn
4. Maak of koppel een private GitHub-repo
5. Voeg pas daarna de remote toe en doe de eerste push

## Eerste concrete checks
```bash
python3 scripts/git-publish-readiness.py
git status --short --branch
git remote -v
```

## Beslissingen die nog nodig zijn
- Welke workspace-bestanden horen echt in de repo?
- Welke memory/status/state-bestanden blijven lokaal-only?
- Blijft `master` de branchnaam, of wordt dit `main`?

## Verwachte volgende stap
Eerst een publish-veilige selectie en `.gitignore`-strategie bepalen. Daarna pas private remote + eerste push.
