# Current images deliverable checklist

Datum: 2026-04-11

## Open deliverable
- `d-current-images`
- Doel: nieuwe Clawdy-afbeeldingen maken via een **echte beeldroute** en ze daarna als **echte Telegram-media** afleveren

## Al bevestigd
- Deliverable staat nog open in `state/open-deliverables.json`
- Telegram afleverpad is helder:
  - helper: `scripts/send-telegram-file.js`
  - doelchat: `16584407`
- Referentie-art bestaat al in `art/`

## Huidige blocker
- Er is nog **geen geverifieerde write-capable image-generation route** in deze runtime
- Eerdere echte beeldtests liepen vast op onvoldoende permissies

## Zodra beeldroute beschikbaar is
1. Genereer nieuwe Clawdy-afbeeldingen via de echte beeldroute
2. Controleer dat de output echte PNG-media zijn
3. Lever af via Telegram:
   ```bash
   node scripts/send-telegram-file.js 16584407 /pad/naar/output.png "Clawdy voor Lisa en Vivian"
   ```
4. Bevestig zichtbaar dat de media echt zijn aangekomen
5. Sluit daarna pas `d-current-images`

## Snelle readiness-check
```bash
python3 scripts/current-images-readiness.py
```
