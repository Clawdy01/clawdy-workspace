const { launchSession } = require('./playwright_session');
(async()=>{
  const itemName = process.argv[2] || 'Github';
  const { context, page } = await launchSession('bitwarden-session-test', { headless: true, timeout: 45000 });
  try {
    await page.goto('https://vault.bitwarden.com/#/vault', { waitUntil: 'domcontentloaded', timeout: 60000 });
    await page.waitForTimeout(2500);
    const search = page.locator('input[placeholder*="Search" i], input[aria-label*="Search" i], input[type="search"]').first();
    if (await search.count()) {
      await search.fill(itemName).catch(() => null);
      await page.waitForTimeout(2000);
    }
    await page.locator('a,button').filter({ hasText: new RegExp(itemName, 'i') }).first().click().catch(() => null);
    await page.waitForTimeout(2500);
    const reveal = page.locator('button, a').filter({ hasText: /reveal|show|toon|view/i }).first();
    if (await reveal.count()) {
      await reveal.click().catch(() => null);
      await page.waitForTimeout(500);
    }
    const data = await page.evaluate(() => ({
      title: document.title,
      url: location.href,
      body: document.body.innerText.slice(0,8000),
      inputs:[...document.querySelectorAll('input')].map(e=>({type:e.type||'',id:e.id||'',name:e.name||'',value:e.value||'',placeholder:e.placeholder||''})).slice(0,50),
      buttons:[...document.querySelectorAll('button')].map(e=>({text:(e.innerText||'').trim()})).filter(x=>x.text).slice(0,80),
    }));
    console.log(JSON.stringify(data,null,2));
  } finally {
    await context.close();
  }
})();
