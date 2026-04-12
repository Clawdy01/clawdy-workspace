const { launchSession } = require('./playwright_session');
(async()=>{
  const email = process.argv[2];
  const { context, page } = await launchSession('bitwarden-debug', { headless: true, timeout: 45000 });
  await page.goto('https://vault.bitwarden.com/#/login', { waitUntil: 'domcontentloaded', timeout: 60000 });
  await page.waitForTimeout(2000);
  const emailInput = page.locator('input[type="email"], input[name*="email" i], input[id*="email" i]').first();
  if (await emailInput.count()) await emailInput.fill(email);
  await page.locator('button').filter({ hasText: /continue|log in/i }).first().click().catch(() => null);
  await page.waitForTimeout(3000);
  const data = await page.evaluate(() => ({
    body: document.body.innerText.slice(0,5000),
    inputs:[...document.querySelectorAll('input')].map(e=>({type:e.type||'',id:e.id||'',name:e.name||'',placeholder:e.placeholder||'',value:e.value||'',outer:e.outerHTML.slice(0,300)})).slice(0,50),
    buttons:[...document.querySelectorAll('button')].map(e=>({text:(e.innerText||'').trim(),outer:e.outerHTML.slice(0,200)})).slice(0,30)
  }));
  console.log(JSON.stringify(data,null,2));
  await context.close();
})();
