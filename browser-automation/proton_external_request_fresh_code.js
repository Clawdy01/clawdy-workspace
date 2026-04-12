const { chromium } = require('playwright-core');
const cp = require('child_process');

function latestAfter(minUid) {
  try {
    const out = cp.execFileSync('python3', ['/home/clawdy/.openclaw/workspace/scripts/proton-latest-code.py', '--json', '--min-uid', String(minUid)], { encoding: 'utf8', timeout: 30000 });
    return JSON.parse(out || '{}');
  } catch {
    return {};
  }
}
function latestAny() {
  return latestAfter(0);
}
function sleep(ms) { return new Promise(r => setTimeout(r, ms)); }

(async () => {
  const email = 'clawdy01@christiandekok.nl';
  const password = 'Aa9!$2dnZx49wbdAg+gT';
  const baseline = latestAny().uid || 0;
  const browser = await chromium.launch({ executablePath: '/snap/bin/chromium', headless: true, args: ['--no-sandbox', '--disable-dev-shm-usage'] });
  const page = await browser.newPage({ viewport: { width: 1440, height: 1200 } });
  page.setDefaultTimeout(45000);
  await page.goto('https://account.proton.me/start', { waitUntil: 'domcontentloaded' });
  await page.waitForLoadState('networkidle', { timeout: 15000 }).catch(() => {});
  await page.getByRole('button', { name: /use your current email/i }).click();
  await page.waitForTimeout(1200);
  await page.locator('#email').evaluate(el => el.focus());
  await page.keyboard.type(email, { delay: 35 });
  await page.locator('button[type="submit"]').first().evaluate(el => el.click());
  await page.waitForLoadState('networkidle', { timeout: 15000 }).catch(() => {});
  await page.waitForTimeout(1000);
  await page.locator('#password').fill(password);
  await page.locator('#password-confirm').fill(password);
  await page.locator('button[type="submit"]').first().click();
  await page.waitForLoadState('networkidle', { timeout: 12000 }).catch(() => {});
  await page.waitForTimeout(4000);
  const requestBtn = page.getByRole('button', { name: /request new code/i }).first();
  const requestVisible = await requestBtn.isVisible().catch(() => false);
  if (requestVisible) {
    await requestBtn.click();
    await page.waitForLoadState('networkidle', { timeout: 12000 }).catch(() => {});
    await page.waitForTimeout(3000);
  }
  let fresh = {};
  for (let i = 0; i < 10; i++) {
    fresh = latestAfter(baseline);
    if (fresh && fresh.code) break;
    await sleep(5000);
  }
  console.log(JSON.stringify({ baseline, requestVisible, fresh }, null, 2));
  await browser.close();
})().catch(err => { console.error(err && err.stack || String(err)); process.exit(1); });
