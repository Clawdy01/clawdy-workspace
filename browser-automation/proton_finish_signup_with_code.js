const { chromium } = require('playwright-core');
const crypto = require('crypto');
const fs = require('fs');
const path = require('path');
const cp = require('child_process');

const OUT_DIR = '/home/clawdy/.openclaw/workspace/browser-automation/out';
const ROOT = '/home/clawdy/.openclaw/workspace';
const DEFAULT_USERNAME = 'clawdy01';
const DEFAULT_VERIFICATION_EMAIL = 'clawdy01@christiandekok.nl';

function generateStrongPassword(length = 20) {
  const alphabet = 'ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz23456789!@#$%^&*()-_=+?';
  let out = 'Aa9!';
  while (out.length < length) out += alphabet[crypto.randomInt(0, alphabet.length)];
  return out;
}

function sleep(ms) {
  return new Promise(r => setTimeout(r, ms));
}

function fetchLatestCode() {
  try {
    const out = cp.execFileSync('python3', [
      path.join(ROOT, 'scripts', 'mail-verification-codes.py'),
      '--json', '--sender', 'proton', '-n', '20'
    ], { cwd: ROOT, encoding: 'utf8', timeout: 30000 });
    const rows = JSON.parse(out);
    const row = rows && rows[0];
    const code = row && row.codes && row.codes.find(x => /^\d{6}$/.test(x));
    return { row, code: code || null };
  } catch (err) {
    return { row: null, code: null, error: String(err) };
  }
}

async function fillVerificationCode(page, code) {
  const inputs = await page.locator('input').evaluateAll(nodes => nodes.map(n => ({
    type: n.getAttribute('type') || '',
    id: n.id || '',
    name: n.getAttribute('name') || '',
    maxLength: n.maxLength || null,
    visible: !!(n.offsetWidth || n.offsetHeight || n.getClientRects().length),
    value: n.value || ''
  })));

  const visible = inputs.filter(i => i.visible);
  const oneCharCandidates = visible.filter(i => i.maxLength === 1 || /code|otp|digit/i.test(`${i.id} ${i.name}`));
  if (oneCharCandidates.length >= code.length) {
    const loc = page.locator('input').filter({ has: page.locator(':scope') });
    const all = page.locator('input');
    let filled = 0;
    for (let i = 0; i < await all.count(); i++) {
      const input = all.nth(i);
      const box = await input.boundingBox().catch(() => null);
      if (!box) continue;
      const maxLength = await input.evaluate(el => el.maxLength || null).catch(() => null);
      if (maxLength === 1) {
        await input.fill(code[filled]);
        filled += 1;
        if (filled >= code.length) return { mode: 'split', inputs };
      }
    }
  }

  const broad = page.locator('input[type="text"], input[type="number"], input:not([type])').filter({ hasNot: page.locator('[disabled]') });
  const count = await broad.count().catch(() => 0);
  for (let i = 0; i < count; i++) {
    const input = broad.nth(i);
    if (!(await input.isVisible().catch(() => false))) continue;
    await input.fill(code).catch(() => {});
    const value = await input.inputValue().catch(() => '');
    if (value.replace(/\D/g, '').includes(code)) return { mode: 'single', inputs };
  }
  return { mode: 'unknown', inputs };
}

(async () => {
  const username = process.argv[2] || DEFAULT_USERNAME;
  const verificationEmail = process.argv[3] || DEFAULT_VERIFICATION_EMAIL;
  const password = process.argv[4] || generateStrongPassword();
  fs.mkdirSync(OUT_DIR, { recursive: true });

  const browser = await chromium.launch({ executablePath: '/snap/bin/chromium', headless: true, args: ['--no-sandbox', '--disable-dev-shm-usage'] });
  const page = await browser.newPage({ viewport: { width: 1440, height: 1200 } });
  page.setDefaultTimeout(45000);

  await page.goto('https://account.proton.me/start', { waitUntil: 'domcontentloaded' });
  await page.waitForLoadState('networkidle', { timeout: 15000 }).catch(() => {});
  const iframeEl = page.locator('iframe[title="Email address"]').first();
  await iframeEl.waitFor({ state: 'visible' });
  const frame = await iframeEl.elementHandle().then(h => h.contentFrame());
  const emailInput = frame.locator('input, textarea').first();
  await emailInput.fill(username);
  await page.getByRole('button', { name: /create free account now/i }).click();
  await page.waitForLoadState('networkidle', { timeout: 15000 }).catch(() => {});
  await page.locator('#password').fill(password);
  await page.locator('#password-confirm').fill(password);
  await page.waitForTimeout(1000);
  await page.locator('button[type="submit"]').first().click();
  await page.waitForLoadState('networkidle', { timeout: 12000 }).catch(() => {});
  await page.waitForTimeout(2500);

  const emailField = page.locator('input[type="email"], input[name*="email" i], input[id*="email" i]').first();
  if (await emailField.count().catch(() => 0)) {
    if (await emailField.isVisible().catch(() => false)) {
      await emailField.fill(verificationEmail).catch(() => {});
    }
  }
  await page.getByRole('button', { name: /get verification code/i }).first().click();
  await page.waitForLoadState('networkidle', { timeout: 12000 }).catch(() => {});
  await page.waitForTimeout(3000);

  let mail = null;
  for (let attempt = 0; attempt < 6; attempt++) {
    mail = fetchLatestCode();
    if (mail.code) break;
    await sleep(5000);
  }
  if (!mail || !mail.code) throw new Error('No Proton verification code found in mailbox');

  const fillResult = await fillVerificationCode(page, mail.code);
  await page.waitForTimeout(800);
  const verifyButton = page.getByRole('button', { name: /verify|confirm|continue|submit|next/i }).first();
  const verifyVisible = await verifyButton.isVisible().catch(() => false);
  if (verifyVisible) {
    await verifyButton.click().catch(() => {});
    await page.waitForLoadState('networkidle', { timeout: 12000 }).catch(() => {});
    await page.waitForTimeout(4000);
  }

  const result = await page.evaluate(() => {
    const text = (document.body.innerText || '').replace(/\s+/g, ' ').trim();
    const interesting = text.match(/verification|verify|captcha|human|sms|email|phone|robot|code|security|confirm|invalid|incorrect|welcome|mail|calendar|drive|pass|loading/ig) || [];
    return {
      title: document.title,
      url: location.href,
      text: text.slice(0, 7000),
      interestingSignals: [...new Set(interesting.map(x => x.toLowerCase()))],
    };
  });

  const screenshot = path.join(OUT_DIR, 'proton-finish-signup-with-code.png');
  await page.screenshot({ path: screenshot, fullPage: true });
  const out = {
    checkedAt: new Date().toISOString(),
    username,
    verificationEmail,
    passwordLength: password.length,
    fetchedCode: mail.code,
    mailSubject: mail.row && mail.row.subject,
    fillResult,
    verifyButtonVisible: verifyVisible,
    screenshot,
    result,
  };
  fs.writeFileSync(path.join(OUT_DIR, 'proton-finish-signup-with-code.json'), JSON.stringify(out, null, 2));
  console.log(JSON.stringify(out, null, 2));
  await browser.close();
})().catch(err => {
  console.error(err && err.stack || String(err));
  process.exit(1);
});
