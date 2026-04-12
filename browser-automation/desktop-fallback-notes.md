# Desktop Automation Fallback

Primary route remains Playwright.

Fallback stack for awkward interactive pages:
- `xvfb-run`
- `xdotool`
- `wmctrl`
- `x11-utils`
- `scrot`

Use this only when DOM-based automation is unreliable.
