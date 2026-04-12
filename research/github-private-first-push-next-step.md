# GitHub private first push - directe next step

Datum: 2026-04-11

## Huidige blocker
De workspace is nog niet publish-veilig genoeg voor een eerste push.

Belangrijkste redenen nu:
- geen remote ingesteld
- branch is nog `master`
- er zijn lokale/sensitieve paden die niet blind mee moeten

## Directe veilige volgorde
1. Bekijk readiness
   ```bash
   python3 scripts/git-publish-readiness.py
   ```
2. Gebruik het voorstel uit:
   - `research/github-private-gitignore-proposal.txt`
3. Zet daarna pas een echte `.gitignore` neer
4. Controleer opnieuw met:
   ```bash
   python3 scripts/git-publish-readiness.py
   git status --short --branch
   ```
5. Voeg daarna private remote toe en doe eerste push

## Nog open beslissingen
- blijft branchnaam `master` of wordt het `main`?
- welke docs/art/scripts horen echt in de repo?
- welke workspace-bestanden blijven strikt lokaal?
