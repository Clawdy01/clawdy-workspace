const { chromium } = require('playwright-core');
const fs = require('fs');
const path = require('path');

const OUT_DIR = '/home/clawdy/.openclaw/workspace/browser-automation/out';
const USERNAME = 'clawdy01';

(async () => {
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

  await page.locator('#username').fill(USERNAME);
  await page.getByRole('button', { name: /create free account now/i }).click();
  await page.waitForLoadState('networkidle', { timeout: 15000 }).catch(() => {});
  await page.waitForTimeout(3000);

  const title = await page.title();
  const url = page.url();
  const text = await page.locator('body').innerText().catch(() => '');
  const screenshot = path.join(OUT_DIR, 'proton-username-submit.png');
  await page.screenshot({ path: screenshot, fullPage: true });

  const result = {
    checkedAt: new Date().toISOString(),
    username: USERNAME,
    title,
    url,
    excerpt: text.slice(0, 3000),
    screenshot,
  };

  fs.writeFileSync(path.join(OUT_DIR, 'proton-username-submit.json'), JSON.stringify(result, null, 2));
  console.log(JSON.stringify(result, null, 2));
  await browser.close();
})().catch(err => {
  console.error(err && err.stack || String(err));
  process.exit(1);
});
