const { launchSession } = require('./playwright_session');
(async()=>{
 const url = process.argv[2];
 const sessionName = process.argv[3] || 'github-signup';
 if (!url) {
   console.error('usage: github_verify_inspect.js <url> [sessionName]');
   process.exit(2);
 }
 const {context,page}=await launchSession(sessionName,{headless:true, timeout:45000});
 await page.goto(url,{waitUntil:'domcontentloaded', timeout:60000});
 await page.waitForTimeout(5000);
 const data = await page.evaluate(() => ({
   title: document.title,
   url: location.href,
   body: document.body.innerText.slice(0,5000),
   links:[...document.querySelectorAll('a')].map(a=>({text:(a.innerText||'').trim(),href:a.href||''})).filter(x=>x.text).slice(0,80),
   buttons:[...document.querySelectorAll('button,input[type="submit"],input[type="button"]')].map(e=>({text:e.innerText||e.value||'', type:e.type||'', id:e.id||'', name:e.name||''})).slice(0,50),
   forms:[...document.querySelectorAll('form')].map(f=>({action:f.action||'',method:f.method||'',id:f.id||''})).slice(0,20),
   metaUser: document.querySelector('meta[name="user-login"]')?.content || null,
 }));
 console.log(JSON.stringify(data,null,2));
 await context.close();
})();
