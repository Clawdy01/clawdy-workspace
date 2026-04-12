const { launchSession } = require('./playwright_session');
(async()=>{
  const login = process.argv[2];
  const password = process.argv[3];
  const repo = process.argv[4] || 'clawdy-workspace';
  if (!login || !password) {
    console.error('usage: github_login_create_repo.js <login> <password> [repo]');
    process.exit(2);
  }
  const { context, page } = await launchSession('github-shared', { headless: true, timeout: 45000 });
  const out = { ok: false, repo };
  try {
    await page.goto('https://github.com/login', { waitUntil: 'domcontentloaded', timeout: 60000 });
    await page.waitForTimeout(1500);
    await page.locator('#login_field, input[name="login"]').first().fill(login).catch(() => null);
    await page.locator('#password, input[name="password"]').first().fill(password).catch(() => null);
    await page.locator('input[type="submit"], button[type="submit"]').first().click().catch(() => null);
    await page.waitForTimeout(5000);
    out.afterLogin = { url: page.url(), title: await page.title(), body: ((await page.textContent('body')) || '').slice(0, 5000) };
    if (page.url().includes('/sessions/verified-device') || page.url().includes('/login/device')) {
      out.needDevice = true;
      console.log(JSON.stringify(out, null, 2));
      return;
    }
    await page.goto('https://github.com/new', { waitUntil: 'domcontentloaded', timeout: 60000 });
    await page.waitForTimeout(3000);
    out.afterNew = { url: page.url(), title: await page.title(), body: ((await page.textContent('body')) || '').slice(0, 5000) };
    const repoInput = page.locator('#repository-name-input, input[name="repository[name]"], #repository_name').first();
    if (await repoInput.count()) await repoInput.fill(repo).catch(() => null);
    await page.locator('button').filter({ hasText: /^Public$/i }).first().click().catch(() => null);
    await page.waitForTimeout(800);
    await page.locator('button, label, div').filter({ hasText: /^Private$/i }).first().click().catch(() => null);
    await page.waitForTimeout(800);
    const createButton = page.locator('button').filter({ hasText: /create repository/i }).first();
    if (await createButton.count()) {
      await createButton.click().catch(() => null);
      await page.waitForTimeout(5000);
    }
    out.final = { url: page.url(), title: await page.title(), body: ((await page.textContent('body')) || '').slice(0, 5000) };
    out.ok = /github.com\/.+\/.+/.test(page.url());
  } finally {
    console.log(JSON.stringify(out, null, 2));
    await context.close();
  }
})();
