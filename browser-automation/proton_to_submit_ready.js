const { chromium } = require('playwright-core');
const crypto = require('crypto');
const fs = require('fs');
const path = require('path');

const OUT_DIR = '/home/clawdy/.openclaw/workspace/browser-automation/out';
const DEFAULT_USERNAME = 'clawdy01';

function generateStrongPassword(length = 20) {
  const alphabet = 'ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz23456789!@#$%^&*()-_=+?';
  let out = 'Aa9!';
  while (out.length < length) {
    out += alphabet[crypto.randomInt(0, alphabet.length)];
  }
  return out;
}

(async () => {
  const username = process.argv[2] || DEFAULT_USERNAME;
  const password = process.argv[3] || generateStrongPassword();
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
  await page.waitForTimeout(1500);

  await page.locator('#password').fill(password);
  await page.locator('#password-confirm').fill(password);
  await page.locator('#password-confirm').press('Tab').catch(() => {});
  await page.waitForTimeout(1200);

  const result = await page.evaluate(() => {
    const submit = document.querySelector('button[type="submit"]');
    const fields = ['password', 'password-confirm'].map(id => {
      const el = document.getElementById(id);
      if (!el) return { id, missing: true };
      return {
        id,
        type: el.getAttribute('type') || '',
        ariaInvalid: el.getAttribute('aria-invalid'),
        valueLength: (el.value || '').length,
      };
    });

    const strengthTexts = Array.from(document.querySelectorAll('div, span, p, li, label'))
      .map(n => (n.innerText || n.textContent || '').replace(/\s+/g, ' ').trim())
      .filter(Boolean)
      .filter(text => /vulnerable|weak|strong|password|confirm/i.test(text));

    return {
      title: document.title,
      url: location.href,
      text: (document.body.innerText || '').slice(0, 2500),
      fields,
      submitText: submit ? (submit.innerText || submit.textContent || '').replace(/\s+/g, ' ').trim() : null,
      submitDisabled: submit ? !!submit.disabled : null,
      strengthTexts: strengthTexts.slice(0, 30),
      activeId: document.activeElement ? document.activeElement.id || '' : '',
    };
  });

  const screenshot = path.join(OUT_DIR, 'proton-to-submit-ready.png');
  await page.screenshot({ path: screenshot, fullPage: true });

  const out = {
    checkedAt: new Date().toISOString(),
    username,
    passwordLength: password.length,
    propagated,
    reachedPasswordStep: await page.locator('#password').isVisible().catch(() => false),
    submitReady: result.submitDisabled === false,
    screenshot,
    ...result,
  };

  fs.writeFileSync(path.join(OUT_DIR, 'proton-to-submit-ready.json'), JSON.stringify(out, null, 2));
  console.log(JSON.stringify(out, null, 2));

  await browser.close();
})().catch(err => {
  console.error(err && err.stack || String(err));
  process.exit(1);
});
