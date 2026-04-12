# Photo Workflow Notes

## Goal
Build a safer, higher-quality photo-editing workflow for real people.

## Current local tools
- ImageMagick
- ffmpeg
- Pillow (planned/installed via python)

## Desired next steps
1. Add masking/segmentation tooling
2. Protect face/person regions before edits
3. Validate both identity preservation and requested visual changes before delivery
4. Use Telegram send helper for verified outputs

## Rules
- Do not send before checking both constraints and requested effects
- Prefer local conservative edits over aggressive generative face changes
- Move to heavier GPU workflows once the new MacBook Pro arrives
