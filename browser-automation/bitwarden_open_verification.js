const { launchSession } = require('./playwright_session');
(async()=>{
  const email = process.argv[2];
  const password = process.argv[3];
  if (!email || !password) {
    console.error('usage: bitwarden_open_verification.js <email> <password>');
    process.exit(2);
  }
  const { context, page } = await launchSession('bitwarden-session-test', { headless: true, timeout: 45000 });
  try {
    await page.goto('https://vault.bitwarden.com/#/login', { waitUntil: 'domcontentloaded', timeout: 60000 });
    await page.waitForTimeout(1500);
    const emailInput = page.locator('input[type="email"], input[name*="email" i], input[id*="email" i]').first();
    if (await emailInput.count()) {
      await emailInput.fill(email).catch(() => null);
      await page.locator('button').filter({ hasText: /continue|log in/i }).first().click().catch(() => null);
      await page.waitForTimeout(1500);
    }
    const passwordInput = page.locator('input[type="password"], input[name*="master" i], input[id*="master" i]').first();
    if (await passwordInput.count()) {
      await passwordInput.fill(password).catch(() => null);
      await passwordInput.press('Enter').catch(() => null);
    }
    await page.getByRole('button', { name: /log in with master password/i }).click().catch(() => null);
    await page.waitForTimeout(5000);
    const resend = page.getByRole('button', { name: /resend code/i });
    if (await resend.count()) {
      await resend.click().catch(() => null);
      await page.waitForTimeout(2000);
    }
    const body = ((await page.textContent('body')) || '').slice(0, 3000);
    console.log(JSON.stringify({ title: await page.title(), url: page.url(), body }, null, 2));
  } finally {
    await context.close();
  }
})();
