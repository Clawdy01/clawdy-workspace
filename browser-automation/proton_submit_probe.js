const { chromium } = require('playwright-core');
const crypto = require('crypto');
const fs = require('fs');
const path = require('path');

const OUT_DIR = '/home/clawdy/.openclaw/workspace/browser-automation/out';
const DEFAULT_USERNAME = 'clawdy01';

function generateStrongPassword(length = 20) {
  const alphabet = 'ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz23456789!@#$%^&*()-_=+?';
  let out = 'Aa9!';
  while (out.length < length) out += alphabet[crypto.randomInt(0, alphabet.length)];
  return out;
}

(async () => {
  const args = process.argv.slice(2);
  const submit = args.includes('--submit');
  const positional = args.filter(v => v !== '--submit');
  const username = positional[0] || DEFAULT_USERNAME;
  const password = positional[1] || generateStrongPassword();
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

  await page.getByRole('button', { name: /create free account now/i }).click();
  await page.waitForLoadState('networkidle', { timeout: 15000 }).catch(() => {});
  await page.waitForTimeout(1200);

  await page.locator('#password').fill(password);
  await page.locator('#password-confirm').fill(password);
  await page.waitForTimeout(1200);

  const submitButton = page.locator('button[type="submit"]').first();
  const pre = await page.evaluate(() => ({
    title: document.title,
    url: location.href,
    text: (document.body.innerText || '').slice(0, 2500),
    buttonText: (document.querySelector('button[type="submit"]')?.innerText || '').replace(/\s+/g, ' ').trim(),
    buttonDisabled: !!document.querySelector('button[type="submit"]')?.disabled,
  }));

  let post = null;
  if (submit) {
    await submitButton.click();
    await page.waitForLoadState('networkidle', { timeout: 10000 }).catch(() => {});
    await page.waitForTimeout(4000);
    post = await page.evaluate(() => {
      const text = (document.body.innerText || '').replace(/\s+/g, ' ').trim();
      const interesting = text.match(/verification|verify|captcha|human|sms|email|phone|robot|code|security|confirm/ig) || [];
      return {
        title: document.title,
        url: location.href,
        text: text.slice(0, 4000),
        interestingSignals: [...new Set(interesting.map(x => x.toLowerCase()))],
      };
    });
  }

  const screenshot = path.join(OUT_DIR, 'proton-submit-probe.png');
  await page.screenshot({ path: screenshot, fullPage: true });

  const out = {
    checkedAt: new Date().toISOString(),
    username,
    passwordLength: password.length,
    submitAttempted: submit,
    submitReady: pre.buttonDisabled === false,
    screenshot,
    pre,
    post,
  };

  fs.writeFileSync(path.join(OUT_DIR, 'proton-submit-probe.json'), JSON.stringify(out, null, 2));
  console.log(JSON.stringify(out, null, 2));
  await browser.close();
})().catch(err => {
  console.error(err && err.stack || String(err));
  process.exit(1);
});
