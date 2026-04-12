const { launchSession } = require('./playwright_session');
(async()=>{
 const {context,page}=await launchSession('bitwarden-setup-inspect',{headless:true, timeout:45000});
 await page.goto('https://vault.bitwarden.com/#/setup-extension',{waitUntil:'domcontentloaded', timeout:60000});
 await page.waitForTimeout(2000);
 const data = await page.evaluate(() => ({
   body: document.body.innerText.slice(0,3000),
   links:[...document.querySelectorAll('a')].map(e=>({text:(e.innerText||'').trim(),href:e.href||'',outer:e.outerHTML.slice(0,500)})).filter(x=>x.text),
   buttons:[...document.querySelectorAll('button')].map(e=>({text:(e.innerText||'').trim(),outer:e.outerHTML.slice(0,500)})).filter(x=>x.text),
 }));
 console.log(JSON.stringify(data,null,2));
 await context.close();
})();
