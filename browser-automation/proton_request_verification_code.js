const { chromium } = require('playwright-core');
const crypto = require('crypto');
const fs = require('fs');
const path = require('path');

const OUT_DIR = '/home/clawdy/.openclaw/workspace/browser-automation/out';
const DEFAULT_USERNAME = 'clawdy01';
const DEFAULT_VERIFICATION_EMAIL = 'clawdy01@christiandekok.nl';

function generateStrongPassword(length = 20) {
  const alphabet = 'ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz23456789!@#$%^&*()-_=+?';
  let out = 'Aa9!';
  while (out.length < length) out += alphabet[crypto.randomInt(0, alphabet.length)];
  return out;
}

(async () => {
  const username = process.argv[2] || DEFAULT_USERNAME;
  const verificationEmail = process.argv[3] || DEFAULT_VERIFICATION_EMAIL;
  const password = process.argv[4] || generateStrongPassword();
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
  await emailInput.fill(username);
  await emailInput.press('Tab').catch(() => {});

  await page.getByRole('button', { name: /create free account now/i }).click();
  await page.waitForLoadState('networkidle', { timeout: 15000 }).catch(() => {});
  await page.locator('#password').fill(password);
  await page.locator('#password-confirm').fill(password);
  await page.waitForTimeout(1200);

  const submitButton = page.locator('button[type="submit"]').first();
  await submitButton.click();
  await page.waitForLoadState('networkidle', { timeout: 12000 }).catch(() => {});
  await page.waitForTimeout(3000);

  const preRequest = await page.evaluate(() => ({
    title: document.title,
    url: location.href,
    text: (document.body.innerText || '').replace(/\s+/g, ' ').trim().slice(0, 5000),
  }));

  const emailField = page.locator('input[type="email"], input[name*="email" i], input[id*="email" i]').first();
  if (await emailField.count().catch(() => 0)) {
    if (await emailField.isVisible().catch(() => false)) {
      const current = await emailField.inputValue().catch(() => '');
      if (!current || current !== verificationEmail) {
        await emailField.fill(verificationEmail).catch(() => {});
        await page.waitForTimeout(500);
      }
    }
  }

  const requestButton = page.getByRole('button', { name: /get verification code/i }).first();
  await requestButton.waitFor({ state: 'visible', timeout: 10000 });
  const requestButtonDisabledBefore = await requestButton.isDisabled().catch(() => null);
  await requestButton.click();
  await page.waitForLoadState('networkidle', { timeout: 12000 }).catch(() => {});
  await page.waitForTimeout(5000);

  const postRequest = await page.evaluate(() => {
    const text = (document.body.innerText || '').replace(/\s+/g, ' ').trim();
    const interesting = text.match(/verification|verify|captcha|human|sms|email|phone|robot|code|security|confirm|sent|invalid|error|try again/ig) || [];
    const emailInputs = Array.from(document.querySelectorAll('input')).map(el => ({
      type: el.type || '',
      id: el.id || '',
      name: el.name || '',
      value: (el.value || '').slice(0, 120),
      ariaInvalid: el.getAttribute('aria-invalid'),
    }));
    return {
      title: document.title,
      url: location.href,
      text: text.slice(0, 6000),
      interestingSignals: [...new Set(interesting.map(x => x.toLowerCase()))],
      emailInputs,
    };
  });

  const screenshot = path.join(OUT_DIR, 'proton-request-verification-code.png');
  await page.screenshot({ path: screenshot, fullPage: true });

  const out = {
    checkedAt: new Date().toISOString(),
    username,
    verificationEmail,
    passwordLength: password.length,
    requestButtonDisabledBefore,
    screenshot,
    preRequest,
    postRequest,
  };

  fs.writeFileSync(path.join(OUT_DIR, 'proton-request-verification-code.json'), JSON.stringify(out, null, 2));
  console.log(JSON.stringify(out, null, 2));
  await browser.close();
})().catch(err => {
  console.error(err && err.stack || String(err));
  process.exit(1);
});
