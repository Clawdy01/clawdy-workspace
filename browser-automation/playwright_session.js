const { chromium } = require('playwright-core');
const fs = require('fs');
const path = require('path');

const BASE_DIR = '/home/clawdy/.openclaw/workspace/browser-automation';
const SESSIONS_DIR = process.env.OPENCLAW_BROWSER_SESSIONS_DIR || '/tmp/openclaw-browser-sessions';

function sessionDir(name = 'default') {
  const safe = String(name || 'default').replace(/[^a-zA-Z0-9._-]+/g, '-');
  return path.join(SESSIONS_DIR, safe);
}

async function launchSession(name = 'default', options = {}) {
  const dir = sessionDir(name);
  fs.mkdirSync(dir, { recursive: true });
  const context = await chromium.launchPersistentContext(dir, {
    executablePath: '/snap/bin/chromium',
    headless: options.headless !== false,
    viewport: options.viewport || { width: 1440, height: 1200 },
    args: ['--no-sandbox', '--disable-dev-shm-usage'],
    ...options.contextOptions,
  });
  const page = context.pages()[0] || await context.newPage();
  page.setDefaultTimeout(options.timeout || 45000);
  return { context, page, sessionDir: dir };
}

module.exports = { launchSession, sessionDir };
