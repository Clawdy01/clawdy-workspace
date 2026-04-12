const { launchSession } = require('./playwright_session');

(async()=>{
  const email = process.argv[2];
  const password = process.argv[3];
  const searchTerm = process.argv[4] || 'GitHub';
  const verificationCode = process.argv[5] || '';
  if (!email || !password) {
    console.error('usage: bitwarden_login_and_search.js <email> <password> [searchTerm] [verificationCode]');
    process.exit(2);
  }
  const { context, page } = await launchSession('bitwarden-session-test', { headless: true, timeout: 45000 });
  const out = { ok: false, searchTerm };
  try {
    await page.goto('https://vault.bitwarden.com/#/login', { waitUntil: 'domcontentloaded', timeout: 60000 });
    await page.waitForTimeout(2000);
    const emailInput = page.locator('input[type="email"], input[name*="email" i], input[id*="email" i]').first();
    if (await emailInput.count()) {
      await emailInput.fill(email).catch(() => null);
      await page.locator('button').filter({ hasText: /continue|log in/i }).first().click().catch(() => null);
      await page.waitForTimeout(2000);
    }
    const passwordInput = page.locator('input[type="password"], input[name*="master" i], input[id*="master" i]').first();
    if (await passwordInput.count()) {
      await passwordInput.fill(password).catch(() => null);
    }
    await page.getByRole('button', { name: /log in with master password/i }).click().catch(() => null);
    await page.waitForTimeout(5000);
    const codeInput = page.locator('input[autocomplete="one-time-code"], input[inputmode="numeric"], input[name*="code" i], input[id*="code" i]').first();
    if (verificationCode && await codeInput.count()) {
      await codeInput.fill(verificationCode).catch(() => null);
      await page.getByRole('button', { name: /continue|verify|log in/i }).first().click().catch(() => null);
      await page.waitForTimeout(5000);
    }
    out.afterLogin = {
      title: await page.title(),
      url: page.url(),
      body: ((await page.textContent('body')) || '').slice(0, 4000),
    };
    const search = page.locator('input[placeholder*="Search" i], input[aria-label*="Search" i], input[type="search"]');
    if (await search.count()) {
      await search.first().fill(searchTerm).catch(() => null);
      await page.waitForTimeout(2000);
      const body = ((await page.textContent('body')) || '').slice(0, 5000);
      out.ok = true;
      out.searchBody = body;
    }
  } finally {
    console.log(JSON.stringify(out, null, 2));
    await context.close();
  }
})();
