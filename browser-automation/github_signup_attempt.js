#!/usr/bin/env node
const fs = require('fs');
const path = require('path');
const { launchSession } = require('./playwright_session');

async function textContentSafe(page, sel) {
  try {
    const loc = page.locator(sel).first();
    if (await loc.count()) return (await loc.textContent())?.trim() || null;
  } catch {}
  return null;
}

(async () => {
  const [, , email, password, username] = process.argv;
  if (!email || !password || !username) {
    console.error('usage: github_signup_attempt.js <email> <password> <username>');
    process.exit(2);
  }
  const outDir = '/home/clawdy/.openclaw/workspace/browser-automation/out';
  fs.mkdirSync(outDir, { recursive: true });
  const screenshot = path.join(outDir, 'github-signup-attempt.png');
  const outJson = path.join(outDir, 'github-signup-attempt.json');

  const { context, page } = await launchSession('github-signup', { headless: true, timeout: 45000 });
  const out = { email, username, ok: false };
  try {
    await page.goto('https://github.com/signup', { waitUntil: 'domcontentloaded', timeout: 60000 });
    await page.fill('#email', email);
    await page.fill('#password', password);
    await page.fill('#login', username);
    const consent = page.locator('input[type="checkbox"][name="user_signup[marketing_consent]"]');
    if (await consent.count()) {
      try { await consent.check(); } catch {}
    }
    await page.screenshot({ path: screenshot, fullPage: true });
    const submit = page.locator('button[type="submit"], input[type="submit"]');
    out.before = {
      title: await page.title(),
      url: page.url(),
      submitCount: await submit.count(),
      emailError: await textContentSafe(page, '#email-err'),
      usernameHelper: await textContentSafe(page, '#username-helper'),
      passwordHelper: await textContentSafe(page, '#password-helper'),
      bodySnippet: ((await page.textContent('body')) || '').slice(0, 4000),
    };
    if (await submit.count()) {
      await submit.first().click({ timeout: 10000 }).catch(() => null);
      await page.waitForLoadState('domcontentloaded', { timeout: 30000 }).catch(() => null);
      await page.waitForTimeout(3000);
    }
    await page.screenshot({ path: screenshot, fullPage: true });
    const body = ((await page.textContent('body')) || '').trim();
    out.after = {
      title: await page.title(),
      url: page.url(),
      emailError: await textContentSafe(page, '#email-err'),
      usernameHelper: await textContentSafe(page, '#username-helper'),
      passwordHelper: await textContentSafe(page, '#password-helper'),
      bodySnippet: body.slice(0, 5000),
      hasCaptchaToken: body.toLowerCase().includes('captcha') || body.toLowerCase().includes('puzzle'),
      asksVerifyEmail: body.toLowerCase().includes('verify your email') || body.toLowerCase().includes('check your email'),
    };
    out.ok = !out.after.emailError && !out.after.hasCaptchaToken;
  } finally {
    fs.writeFileSync(outJson, JSON.stringify(out, null, 2));
    await context.close();
  }
  console.log(JSON.stringify(out, null, 2));
})();
