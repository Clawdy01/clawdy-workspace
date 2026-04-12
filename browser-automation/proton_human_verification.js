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

function parseArgs(argv) {
  const options = {
    username: DEFAULT_USERNAME,
    password: generateStrongPassword(),
    email: null,
    code: null,
    send: false,
    verify: false,
  };

  const positional = [];
  for (let i = 0; i < argv.length; i++) {
    const arg = argv[i];
    if (arg === '--email') {
      options.email = argv[++i] || null;
    } else if (arg === '--code') {
      options.code = argv[++i] || null;
    } else if (arg === '--send') {
      options.send = true;
    } else if (arg === '--verify') {
      options.verify = true;
    } else {
      positional.push(arg);
    }
  }

  if (positional[0]) options.username = positional[0];
  if (positional[1]) options.password = positional[1];
  return options;
}

async function pageStateSnapshot(page) {
  return await page.evaluate(() => ({
    title: document.title,
    url: location.href,
    bodyText: (document.body.innerText || '').replace(/\s+/g, ' ').trim().slice(0, 2000),
    passwordVisible: !!document.querySelector('#password'),
    passwordConfirmVisible: !!document.querySelector('#password-confirm'),
    usernameValue: document.querySelector('#username')?.value || '',
    submitButtons: Array.from(document.querySelectorAll('button[type="submit"], button'))
      .map(el => (el.innerText || el.textContent || '').replace(/\s+/g, ' ').trim())
      .filter(Boolean)
      .slice(0, 10),
  }));
}

async function buildToVerificationDialog(page, username, password) {
  await page.goto('https://account.proton.me/start', { waitUntil: 'domcontentloaded' });
  await page.waitForLoadState('networkidle', { timeout: 15000 }).catch(() => {});

  const iframeEl = page.locator('iframe[title="Email address"]').first();
  await iframeEl.waitFor({ state: 'visible' });
  const frame = await iframeEl.elementHandle().then(h => h && h.contentFrame());
  if (!frame) {
    return { ok: false, stage: 'email-iframe-missing', snapshot: await pageStateSnapshot(page) };
  }

  const emailInput = frame.locator('input, textarea').first();
  await emailInput.waitFor({ state: 'visible' });
  await emailInput.fill(username);
  await emailInput.press('Tab').catch(() => {});

  await page.waitForFunction(() => {
    const el = document.querySelector('#username');
    return !!el && !!el.value;
  }, { timeout: 15000 }).catch(() => {});

  await page.getByRole('button', { name: /create free account now/i }).click();
  await page.waitForLoadState('networkidle', { timeout: 15000 }).catch(() => {});

  const passwordVisible = await page.locator('#password').isVisible().catch(() => false);
  if (!passwordVisible) {
    return {
      ok: false,
      stage: 'password-step-missing',
      snapshot: await pageStateSnapshot(page),
    };
  }

  await page.locator('#password').fill(password);
  await page.locator('#password-confirm').fill(password);
  await page.waitForTimeout(1000);

  const submitButton = page.locator('button[type="submit"]').first();
  await submitButton.click();
  await page.waitForLoadState('networkidle', { timeout: 12000 }).catch(() => {});
  await page.waitForTimeout(2500);
  return { ok: true, stage: 'verification-dialog', snapshot: await pageStateSnapshot(page) };
}

async function inspectDialog(page) {
  return await page.evaluate(() => {
    const bodyText = (document.body.innerText || '').replace(/\s+/g, ' ').trim();
    const dialog = Array.from(document.querySelectorAll('[role="dialog"], dialog'))
      .find(node => /human verification|verification code|email address/i.test((node.innerText || node.textContent || '').replace(/\s+/g, ' ').trim()));

    const scope = dialog || document;
    const visible = node => {
      if (!(node instanceof HTMLElement)) return false;
      const style = window.getComputedStyle(node);
      const rect = node.getBoundingClientRect();
      return style.visibility !== 'hidden' && style.display !== 'none' && rect.width > 0 && rect.height > 0;
    };

    const labelTextFor = el => {
      if (!(el instanceof HTMLElement)) return '';
      const aria = (el.getAttribute('aria-label') || '').trim();
      if (aria) return aria;
      const labelledby = el.getAttribute('aria-labelledby');
      if (labelledby) {
        const text = labelledby
          .split(/\s+/)
          .map(id => document.getElementById(id))
          .filter(Boolean)
          .map(n => (n.innerText || n.textContent || '').trim())
          .join(' ')
          .trim();
        if (text) return text;
      }
      const id = el.getAttribute('id');
      if (id) {
        const label = document.querySelector(`label[for="${id}"]`);
        if (label) {
          const text = (label.innerText || label.textContent || '').trim();
          if (text) return text;
        }
      }
      const parentLabel = el.closest('label');
      return parentLabel ? (parentLabel.innerText || parentLabel.textContent || '').trim() : '';
    };

    const inputs = Array.from(scope.querySelectorAll('input, textarea'))
      .filter(visible)
      .map((el, index) => ({
        index,
        id: el.id || null,
        name: el.getAttribute('name') || null,
        type: el.getAttribute('type') || 'text',
        inputmode: el.getAttribute('inputmode') || null,
        autocomplete: el.getAttribute('autocomplete') || null,
        placeholder: el.getAttribute('placeholder') || null,
        label: labelTextFor(el),
        valueLength: (el.value || '').length,
        maxLength: el.maxLength > 0 ? el.maxLength : null,
      }));

    const buttons = Array.from(scope.querySelectorAll('button, [role="button"]'))
      .filter(visible)
      .map((el, index) => ({
        index,
        text: (el.innerText || el.textContent || '').replace(/\s+/g, ' ').trim(),
        disabled: !!el.disabled || el.getAttribute('aria-disabled') === 'true',
      }))
      .filter(row => row.text);

    return {
      title: document.title,
      url: location.href,
      verificationScreen: /human verification|verification code|email address|get verification code/i.test(bodyText),
      dialogText: dialog ? (dialog.innerText || dialog.textContent || '').replace(/\s+/g, ' ').trim().slice(0, 2000) : bodyText.slice(0, 2000),
      inputs,
      buttons,
    };
  });
}

async function fillEmailAndSend(page, email) {
  const emailField = page.locator('[role="dialog"] input').filter({ hasNot: page.locator('input[inputmode="numeric"]') }).first();
  await emailField.waitFor({ state: 'visible', timeout: 8000 });
  await emailField.fill(email);
  await page.waitForTimeout(400);
  const button = page.getByRole('button', { name: /get verification code/i }).first();
  await button.waitFor({ state: 'visible', timeout: 5000 });
  const disabledBefore = await button.isDisabled().catch(() => null);
  await button.click();
  await page.waitForLoadState('networkidle', { timeout: 12000 }).catch(() => {});
  await page.waitForTimeout(2500);
  return { disabledBefore };
}

async function fillCodeAndVerify(page, code) {
  const clean = String(code || '').replace(/\s+/g, '');
  if (!clean) return { filled: false, reason: 'empty-code' };

  const dialog = page.locator('[role="dialog"]').first();
  await dialog.waitFor({ state: 'visible', timeout: 8000 }).catch(() => {});

  const oneTime = dialog.locator('input[autocomplete="one-time-code"], input[name*="code" i], input[id*="code" i], input[inputmode="numeric"], input[maxlength="1"]');
  const count = await oneTime.count().catch(() => 0);

  if (count >= 2) {
    for (let i = 0; i < Math.min(count, clean.length); i++) {
      await oneTime.nth(i).fill(clean[i]);
    }
  } else if (count === 1) {
    await oneTime.first().fill(clean);
  } else {
    const fallback = dialog.locator('input, textarea').last();
    await fallback.fill(clean);
  }

  const verifyButton = page.getByRole('button', { name: /verify|continue|confirm|submit/i }).first();
  const visible = await verifyButton.isVisible().catch(() => false);
  if (visible) {
    await verifyButton.click().catch(() => {});
    await page.waitForLoadState('networkidle', { timeout: 12000 }).catch(() => {});
    await page.waitForTimeout(2500);
  }

  return { filled: true, fieldCount: count, clickedVerify: visible };
}

(async () => {
  const options = parseArgs(process.argv.slice(2));
  fs.mkdirSync(OUT_DIR, { recursive: true });

  const browser = await chromium.launch({
    executablePath: '/snap/bin/chromium',
    headless: true,
    args: ['--no-sandbox', '--disable-dev-shm-usage'],
  });

  const page = await browser.newPage({ viewport: { width: 1440, height: 1200 } });
  page.setDefaultTimeout(45000);

  const flow = await buildToVerificationDialog(page, options.username, options.password);
  const initial = await inspectDialog(page);

  let emailAction = null;
  if (flow.ok && options.email && options.send) {
    emailAction = await fillEmailAndSend(page, options.email);
  }

  let codeAction = null;
  if (flow.ok && options.code && options.verify) {
    codeAction = await fillCodeAndVerify(page, options.code);
  }

  const final = await inspectDialog(page);
  const screenshot = path.join(OUT_DIR, 'proton-human-verification.png');
  await page.screenshot({ path: screenshot, fullPage: true });

  const out = {
    checkedAt: new Date().toISOString(),
    username: options.username,
    passwordLength: options.password.length,
    emailProvided: !!options.email,
    codeProvided: !!options.code,
    sendRequested: options.send,
    verifyRequested: options.verify,
    screenshot,
    flow,
    initial,
    emailAction,
    codeAction,
    final,
  };

  fs.writeFileSync(path.join(OUT_DIR, 'proton-human-verification.json'), JSON.stringify(out, null, 2));
  console.log(JSON.stringify(out, null, 2));
  await browser.close();
  if (!flow.ok) process.exit(2);
})().catch(err => {
  console.error(err && err.stack || String(err));
  process.exit(1);
});
