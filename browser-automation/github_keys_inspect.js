const { launchSession } = require('./playwright_session');
(async()=>{
 const {context,page}=await launchSession('github-shared',{headless:true, timeout:45000});
 await page.goto('https://github.com/settings/keys',{waitUntil:'domcontentloaded', timeout:60000});
 await page.waitForTimeout(3000);
 const data = await page.evaluate(() => ({
   title: document.title,
   url: location.href,
   body: document.body.innerText.slice(0,4000),
   buttons:[...document.querySelectorAll('a,button')].map(e=>({text:(e.innerText||'').trim(),href:e.href||'',aria:e.getAttribute('aria-label')||''})).filter(x=>x.text||x.aria).slice(0,120)
 }));
 console.log(JSON.stringify(data,null,2));
 await context.close();
})();
