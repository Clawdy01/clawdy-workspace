const { launchSession } = require('./playwright_session');
(async()=>{
 const sessionName = process.argv[2] || 'bitwarden-session-test';
 const {context,page}=await launchSession(sessionName,{headless:true, timeout:45000});
 await page.goto('https://vault.bitwarden.com/#/login',{waitUntil:'domcontentloaded', timeout:60000});
 await page.waitForTimeout(3000);
 const data = await page.evaluate(() => ({
   title: document.title,
   url: location.href,
   body: document.body.innerText.slice(0,5000),
   inputs:[...document.querySelectorAll('input')].map(e=>({type:e.type||'',id:e.id||'',name:e.name||'',placeholder:e.placeholder||'',value:e.value||''})).slice(0,50),
   buttons:[...document.querySelectorAll('button')].map(e=>({text:(e.innerText||'').trim(),aria:e.getAttribute('aria-label')||''})).filter(x=>x.text||x.aria).slice(0,50),
 }))
 console.log(JSON.stringify(data,null,2));
 await context.close();
})();
