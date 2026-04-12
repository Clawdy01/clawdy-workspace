const { chromium } = require('playwright-core');
const crypto = require('crypto');
const fs = require('fs');
const path = require('path');
const cp = require('child_process');

const ROOT = '/home/clawdy/.openclaw/workspace';
const OUT_DIR = '/home/clawdy/.openclaw/workspace/browser-automation/out';
const DEFAULT_EMAIL = 'clawdy01@christiandekok.nl';

function generateStrongPassword(length = 20) {
  const alphabet = 'ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz23456789!@#$%^&*()-_=+?';
  let out = 'Aa9!';
  while (out.length < length) out += alphabet[crypto.randomInt(0, alphabet.length)];
  return out;
}
function sleep(ms) { return new Promise(r => setTimeout(r, ms)); }
async function typeIntoRealInput(page, selector, value) {
  await page.locator(selector).evaluate(el => el.focus());
  await page.keyboard.type(value, { delay: 35 });
}
function fetchLatestCode(minUid = 0) {
  try {
    const out = cp.execFileSync('python3', [
      path.join(ROOT, 'scripts', 'proton-latest-code.py'), '--json', '--min-uid', String(minUid)
    ], { cwd: ROOT, encoding: 'utf8', timeout: 30000 });
    const row = JSON.parse(out || '{}');
    return { row, code: row.code || null };
  } catch (err) {
    return { row: null, code: null, error: String(err) };
  }
}
async function fillVerificationCode(page, code) {
  const inputs = page.locator('input');
  const count = await inputs.count().catch(() => 0);
  let singleFilled = false;
  let splitFilled = 0;
  for (let i = 0; i < count; i++) {
    const input = inputs.nth(i);
    if (!(await input.isVisible().catch(() => false))) continue;
    const maxLength = await input.evaluate(el => el.maxLength || null).catch(() => null);
    const type = await input.evaluate(el => el.type || '').catch(() => '');
    if (maxLength === 1) {
      await input.fill(code[splitFilled] || '');
      splitFilled += 1;
      if (splitFilled >= code.length) return { mode: 'split' };
    } else if (!singleFilled && ['text','number','tel',''].includes(type)) {
      await input.fill(code).catch(() => {});
      const v = await input.inputValue().catch(() => '');
      if (v.replace(/\D/g, '').includes(code)) singleFilled = true;
    }
  }
  return { mode: singleFilled ? 'single' : 'unknown' };
}

(async () => {
  const email = process.argv[2] || DEFAULT_EMAIL;
  const password = process.argv[3] || generateStrongPassword();
  fs.mkdirSync(OUT_DIR, { recursive: true });

  const browser = await chromium.launch({ executablePath: '/snap/bin/chromium', headless: true, args: ['--no-sandbox','--disable-dev-shm-usage'] });
  const page = await browser.newPage({ viewport: { width: 1440, height: 1200 } });
  page.setDefaultTimeout(45000);

  await page.goto('https://account.proton.me/start', { waitUntil: 'domcontentloaded' });
  await page.waitForLoadState('networkidle', { timeout: 15000 }).catch(() => {});
  await page.getByRole('button', { name: /use your current email/i }).click();
  await page.waitForTimeout(1200);
  await typeIntoRealInput(page, '#email', email);
  await page.waitForTimeout(800);
  await page.locator('button[type="submit"]').first().evaluate(el => el.click());
  await page.waitForLoadState('networkidle', { timeout: 15000 }).catch(() => {});
  await page.waitForTimeout(1500);

  await page.locator('#password').fill(password);
  await page.locator('#password-confirm').fill(password);
  await page.waitForTimeout(1000);
  await page.locator('button[type="submit"]').first().click();
  await page.waitForLoadState('networkidle', { timeout: 12000 }).catch(() => {});
  await page.waitForTimeout(3000);

  await page.waitForTimeout(3000);

  const baselineMail = fetchLatestCode();
  const baselineUid = baselineMail.row && baselineMail.row.uid || 0;
  let mail = null;
  for (let attempt = 0; attempt < 8; attempt++) {
    mail = fetchLatestCode();
    if (mail.code) break;
    await sleep(5000);
  }
  if (!mail || !mail.code) throw new Error('No Proton verification code found in mailbox');

  const verificationInput = page.locator('#verification').first();
  await verificationInput.evaluate(el => el.focus());
  await page.keyboard.type(mail.code, { delay: 35 });
  await verificationInput.press('Tab').catch(() => {});
  await page.waitForTimeout(1000);
  const verifyBtn = page.getByRole('button', { name: /^verify$/i }).first();
  const verifyVisible = await verifyBtn.isVisible().catch(() => false);
  const verifyDisabled = await verifyBtn.isDisabled().catch(() => null);
  const fillResult = { mode: 'single', field: 'verification', verifyDisabled };
  if (verifyVisible) {
    await verifyBtn.click().catch(() => {});
    await page.waitForLoadState('networkidle', { timeout: 12000 }).catch(() => {});
    await page.waitForTimeout(3000);
  }

  const invalidText = await page.locator('body').innerText().catch(() => '');
  let retryMail = null;
  if (/invalid verification code/i.test(invalidText)) {
    const requestNew = page.getByRole('button', { name: /resend code|request new code/i }).first();
    if (await requestNew.isVisible().catch(() => false)) {
      await requestNew.click().catch(() => {});
      await page.waitForLoadState('networkidle', { timeout: 12000 }).catch(() => {});
      await page.waitForTimeout(3000);
      for (let attempt = 0; attempt < 10; attempt++) {
        retryMail = fetchLatestCode(baselineUid);
        if (retryMail.code) break;
        await sleep(5000);
      }
      if (retryMail && retryMail.code) {
        await verificationInput.fill('');
        await verificationInput.evaluate(el => el.focus());
        await page.keyboard.type(retryMail.code, { delay: 35 });
        await page.waitForTimeout(1000);
        if (await verifyBtn.isVisible().catch(() => false)) {
          await verifyBtn.click().catch(() => {});
          await page.waitForLoadState('networkidle', { timeout: 12000 }).catch(() => {});
          await page.waitForTimeout(3000);
        }
      }
    }
  }

  const finalStartBtn = page.getByRole('button', { name: /^get started$/i }).first();
  const finalStartVisible = await finalStartBtn.isVisible().catch(() => false);
  const finalStartDisabled = await finalStartBtn.isDisabled().catch(() => null);
  if (finalStartVisible && finalStartDisabled === false) {
    await finalStartBtn.click().catch(() => {});
    await page.waitForLoadState('networkidle', { timeout: 12000 }).catch(() => {});
    await page.waitForTimeout(4000);
  }

  const result = await page.evaluate(() => {
    const text = (document.body.innerText || '').replace(/\s+/g, ' ').trim();
    const interesting = text.match(/verification|verify|captcha|human|email|code|invalid|incorrect|welcome|recovery|pass|mail|account/ig) || [];
    return {
      title: document.title,
      url: location.href,
      text: text.slice(0, 7000),
      interestingSignals: [...new Set(interesting.map(x => x.toLowerCase()))],
    };
  });

  const screenshot = path.join(OUT_DIR, 'proton-external-finish-with-code.png');
  await page.screenshot({ path: screenshot, fullPage: true });
  const out = {
    checkedAt: new Date().toISOString(),
    email,
    password,
    passwordLength: password.length,
    fetchedCode: mail.code,
    mailSubject: mail.row && mail.row.subject,
    retryCode: retryMail && retryMail.code,
    retryMailSubject: retryMail && retryMail.row && retryMail.row.subject,
    fillResult,
    verifyButtonVisible: verifyVisible,
    finalStartVisible,
    finalStartDisabled,
    screenshot,
    result,
  };
  fs.writeFileSync(path.join(OUT_DIR, 'proton-external-finish-with-code.json'), JSON.stringify(out, null, 2));
  console.log(JSON.stringify(out, null, 2));
  await browser.close();
})().catch(err => {
  console.error(err && err.stack || String(err));
  process.exit(1);
});
