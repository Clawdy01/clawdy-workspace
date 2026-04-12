const { chromium } = require('playwright-core');
const cp = require('child_process');

function latestCode() {
  const out = cp.execFileSync('python3', ['/home/clawdy/.openclaw/workspace/scripts/mail-verification-codes.py', '--json', '--sender', 'proton', '-n', '20'], { encoding: 'utf8', timeout: 30000 });
  const rows = JSON.parse(out);
  return rows[0].codes.find(x => /^\d{6}$/.test(x));
}

(async () => {
  const email = process.argv[2] || 'clawdy01@christiandekok.nl';
  const password = process.argv[3] || 'Aa9!t!(T-7oyw_6(CB8A';
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
  await page.waitForTimeout(5000);
  const code = latestCode();
  const input = page.locator('#verification').first();
  await input.evaluate(el => el.focus());
  await page.keyboard.type(code, { delay: 35 });
  await page.waitForTimeout(1000);
  const buttons = await page.locator('button').evaluateAll(nodes => nodes.map((n, i) => ({
    i,
    text: (n.innerText || n.textContent || '').replace(/\s+/g, ' ').trim(),
    disabled: !!n.disabled,
    ariaLabel: n.getAttribute('aria-label') || ''
  })));
  console.log(JSON.stringify({ code, buttons }, null, 2));
  await browser.close();
})().catch(err => {
  console.error(err && err.stack || String(err));
  process.exit(1);
});
