const { chromium } = require('playwright-core');
const fs = require('fs');
const path = require('path');

const OUT_DIR = '/home/clawdy/.openclaw/workspace/browser-automation/out';
const DEFAULT_USERNAME = 'clawdy01';

(async () => {
  const username = process.argv[2] || DEFAULT_USERNAME;
  fs.mkdirSync(OUT_DIR, { recursive: true });

  const browser = await chromium.launch({
    executablePath: '/snap/bin/chromium',
    headless: true,
    args: ['--no-sandbox', '--disable-dev-shm-usage'],
  });

  const page = await browser.newPage({ viewport: { width: 1440, height: 1200 } });
  page.setDefaultTimeout(45000);

  await page.goto('https://account.proton.me/start', { waitUntil: 'domcontentloaded' });
  await page.waitForLoadState('networkidle', { timeout: 15000 }).catch(() => {});

  const iframeEl = page.locator('iframe[title="Email address"]').first();
  await iframeEl.waitFor({ state: 'visible' });
  const frame = await iframeEl.elementHandle().then(h => h.contentFrame());
  if (!frame) throw new Error('Could not access Email address iframe');

  const emailInput = frame.locator('input, textarea').first();
  await emailInput.waitFor({ state: 'visible' });
  await emailInput.fill(username);
  await emailInput.press('Tab').catch(() => {});

  const propagated = await page.locator('#username').evaluate(el => ({
    value: el.value,
    ariaInvalid: el.getAttribute('aria-invalid'),
  }));

  await page.getByRole('button', { name: /create free account now/i }).click();
  await page.waitForLoadState('networkidle', { timeout: 15000 }).catch(() => {});
  await page.waitForTimeout(2000);

  const password = page.locator('#password');
  const passwordConfirm = page.locator('#password-confirm');
  const getStarted = page.getByRole('button', { name: /get started/i });

  const result = {
    checkedAt: new Date().toISOString(),
    username,
    propagated,
    title: await page.title(),
    url: page.url(),
    reachedPasswordStep: await password.isVisible().catch(() => false),
    passwordVisible: await password.isVisible().catch(() => false),
    passwordConfirmVisible: await passwordConfirm.isVisible().catch(() => false),
    getStartedVisible: await getStarted.isVisible().catch(() => false),
    excerpt: await page.locator('body').innerText().then(t => t.slice(0, 2500)).catch(() => ''),
  };

  const screenshot = path.join(OUT_DIR, 'proton-to-password-step.png');
  await page.screenshot({ path: screenshot, fullPage: true });
  result.screenshot = screenshot;

  fs.writeFileSync(path.join(OUT_DIR, 'proton-to-password-step.json'), JSON.stringify(result, null, 2));
  console.log(JSON.stringify(result, null, 2));

  await browser.close();
})().catch(err => {
  console.error(err && err.stack || String(err));
  process.exit(1);
});
