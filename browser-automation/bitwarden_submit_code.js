const { launchSession } = require('./playwright_session');
(async()=>{
  const sessionName = process.argv[2] || 'bitwarden-session-test';
  const code = process.argv[3];
  if (!code) {
    console.error('usage: bitwarden_submit_code.js <sessionName> <code>');
    process.exit(2);
  }
  const { context, page } = await launchSession(sessionName, { headless: true, timeout: 45000 });
  await page.goto('https://vault.bitwarden.com/#/device-verification', { waitUntil: 'domcontentloaded', timeout: 60000 });
  await page.waitForTimeout(2000);
  const input = page.locator('input[autocomplete="one-time-code"], input[inputmode="numeric"], input[name*="code" i], input[id*="code" i]').first();
  if (await input.count()) await input.fill(code).catch(() => null);
  await page.getByRole('button', { name: /continue logging in|continue|verify/i }).first().click().catch(() => null);
  await page.waitForTimeout(5000);
  const data = await page.evaluate(() => ({
    title: document.title,
    url: location.href,
    body: document.body.innerText.slice(0,5000),
    searchVisible: !!document.querySelector('input[placeholder*="Search" i], input[aria-label*="Search" i], input[type="search"]')
  }));
  console.log(JSON.stringify(data, null, 2));
  await context.close();
})();
