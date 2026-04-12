const { launchSession } = require('./playwright_session');
(async()=>{
 const sessionName = process.argv[2] || 'github-signup';
 const {context,page}=await launchSession(sessionName,{headless:true, timeout:45000});
 await page.goto('https://github.com/',{waitUntil:'domcontentloaded', timeout:60000});
 await page.waitForTimeout(3000);
 const data = await page.evaluate(() => ({
   title: document.title,
   url: location.href,
   body: document.body.innerText.slice(0,5000),
   links:[...document.querySelectorAll('a')].map(e=>({text:(e.innerText||'').trim(),href:e.href||'',aria:e.getAttribute('aria-label')||''})).filter(x=>x.text||x.aria).slice(0,200),
   buttons:[...document.querySelectorAll('button')].map(e=>({text:(e.innerText||'').trim(),aria:e.getAttribute('aria-label')||''})).filter(x=>x.text||x.aria).slice(0,100),
   metaUser: document.querySelector('meta[name="user-login"]')?.content || null,
 }))
 console.log(JSON.stringify(data,null,2));
 await context.close();
})();
