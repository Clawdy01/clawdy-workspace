const { launchSession } = require('./playwright_session');
(async()=>{
  const term = process.argv[2] || 'GitHub';
  const { context, page } = await launchSession('bitwarden-session-test', { headless: true, timeout: 45000 });
  try {
    await page.goto('https://vault.bitwarden.com/#/vault', { waitUntil: 'domcontentloaded', timeout: 60000 });
    await page.waitForTimeout(2000);
    const addLater = page.getByRole('button', { name: /add it later/i });
    if (await addLater.count()) {
      await addLater.click().catch(() => null);
      await page.waitForTimeout(1500);
    }
    await page.goto('https://vault.bitwarden.com/#/vault', { waitUntil: 'domcontentloaded', timeout: 60000 });
    await page.waitForTimeout(2500);
    const search = page.locator('input[placeholder*="Search" i], input[aria-label*="Search" i], input[type="search"], input[placeholder*="Zoek" i]').first();
    if (await search.count()) {
      await search.fill(term).catch(() => null);
      await page.waitForTimeout(2000);
    }
    const data = await page.evaluate(() => ({
      title: document.title,
      url: location.href,
      body: document.body.innerText.slice(0,8000),
      links:[...document.querySelectorAll('a')].map(e=>({text:(e.innerText||'').trim(),href:e.href||''})).filter(x=>x.text).slice(0,100),
      buttons:[...document.querySelectorAll('button')].map(e=>({text:(e.innerText||'').trim()})).filter(x=>x.text).slice(0,100),
    }));
    console.log(JSON.stringify(data,null,2));
  } finally {
    await context.close();
  }
})();
