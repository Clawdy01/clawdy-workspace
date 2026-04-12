const { launchSession } = require('./playwright_session');
(async()=>{
  const email = process.argv[2];
  const password = process.argv[3];
  const { context, page } = await launchSession('bitwarden-inspect', { headless: true, timeout: 45000 });
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
  await page.waitForTimeout(4000);
  const data = await page.evaluate(() => ({
    title: document.title,
    url: location.href,
    body: document.body.innerText.slice(0,3000),
    forms:[...document.querySelectorAll('form')].map(e=>({action:e.action||'',method:e.method||'',outer:e.outerHTML.slice(0,1500)})),
    inputs:[...document.querySelectorAll('input')].map(e=>({type:e.type||'',id:e.id||'',name:e.name||'',autocomplete:e.autocomplete||'',inputmode:e.inputMode||'',outer:e.outerHTML.slice(0,600)})),
    buttons:[...document.querySelectorAll('button')].map(e=>({text:(e.innerText||'').trim(),disabled:e.disabled,aria:e.getAttribute('aria-label')||'',type:e.type||'',outer:e.outerHTML.slice(0,600)}))
  }));
  console.log(JSON.stringify(data,null,2));
  await context.close();
})();
