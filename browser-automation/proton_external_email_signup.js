const { chromium } = require('playwright-core');
const crypto = require('crypto');
const fs = require('fs');
const path = require('path');

const OUT_DIR = '/home/clawdy/.openclaw/workspace/browser-automation/out';
const DEFAULT_EMAIL = 'clawdy01@christiandekok.nl';

function generateStrongPassword(length = 20) {
  const alphabet = 'ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz23456789!@#$%^&*()-_=+?';
  let out = 'Aa9!';
  while (out.length < length) out += alphabet[crypto.randomInt(0, alphabet.length)];
  return out;
}

(async () => {
  const email = process.argv[2] || DEFAULT_EMAIL;
  const password = process.argv[3] || generateStrongPassword();
  fs.mkdirSync(OUT_DIR, { recursive: true });

  const browser = await chromium.launch({ executablePath: '/snap/bin/chromium', headless: true, args: ['--no-sandbox', '--disable-dev-shm-usage'] });
  const page = await browser.newPage({ viewport: { width: 1440, height: 1200 } });
  page.setDefaultTimeout(45000);

  await page.goto('https://account.proton.me/start', { waitUntil: 'domcontentloaded' });
  await page.waitForLoadState('networkidle', { timeout: 15000 }).catch(() => {});
  await page.getByRole('button', { name: /use your current email/i }).click();
  await page.waitForLoadState('networkidle', { timeout: 15000 }).catch(() => {});
  await page.waitForTimeout(1000);

  await page.locator('#email').evaluate(el => el.focus());
  await page.keyboard.type(email, { delay: 35 });
  await page.waitForTimeout(800);
  await page.locator('button[type="submit"]').first().evaluate(el => el.click());
  await page.waitForLoadState('networkidle', { timeout: 15000 }).catch(() => {});
  await page.waitForTimeout(1500);

  const visiblePassword = await page.locator('#password').isVisible().catch(() => false);
  if (visiblePassword) {
    await page.locator('#password').fill(password);
    await page.locator('#password-confirm').fill(password);
    await page.waitForTimeout(1000);
    const submit = page.locator('button[type="submit"]').first();
    const disabled = await submit.isDisabled().catch(() => null);
    if (disabled === false) {
      await submit.click();
      await page.waitForLoadState('networkidle', { timeout: 12000 }).catch(() => {});
      await page.waitForTimeout(3000);
    }
  }

  const result = await page.evaluate(() => {
    const text = (document.body.innerText || '').replace(/\s+/g, ' ').trim();
    const interesting = text.match(/verification|verify|captcha|human|sms|email|phone|robot|code|security|confirm|sent|invalid|error|try again|password|account/ig) || [];
    const inputs = Array.from(document.querySelectorAll('input, textarea')).map(el => ({
      id: el.id || '',
      name: el.name || '',
      type: el.type || '',
      value: (el.value || '').slice(0, 120),
      ariaInvalid: el.getAttribute('aria-invalid'),
      maxLength: el.maxLength || null,
      visible: !!(el.offsetWidth || el.offsetHeight || el.getClientRects().length),
    }));
    return {
      title: document.title,
      url: location.href,
      text: text.slice(0, 6000),
      interestingSignals: [...new Set(interesting.map(x => x.toLowerCase()))],
      inputs,
    };
  });

  const screenshot = path.join(OUT_DIR, 'proton-external-email-signup.png');
  await page.screenshot({ path: screenshot, fullPage: true });
  const out = {
    checkedAt: new Date().toISOString(),
    email,
    password,
    passwordLength: password.length,
    screenshot,
    result,
  };
  fs.writeFileSync(path.join(OUT_DIR, 'proton-external-email-signup.json'), JSON.stringify(out, null, 2));
  console.log(JSON.stringify(out, null, 2));
  await browser.close();
})().catch(err => {
  console.error(err && err.stack || String(err));
  process.exit(1);
});
