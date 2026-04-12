const { launchSession } = require('./playwright_session');
(async()=>{
 const {context,page}=await launchSession('github-shared',{headless:true, timeout:45000});
 await page.goto('https://github.com/new',{waitUntil:'domcontentloaded', timeout:60000});
 await page.waitForTimeout(3000);
 const data = await page.evaluate(() => ({
   title: document.title,
   url: location.href,
   body: document.body.innerText.slice(0,4000),
   inputs:[...document.querySelectorAll('input,textarea,select')].map(e=>({tag:e.tagName,type:e.type||'',id:e.id||'',name:e.name||'',placeholder:e.placeholder||'',aria:e.getAttribute('aria-label')||'',value:e.value||'',checked:e.checked||false})).slice(0,120),
   buttons:[...document.querySelectorAll('button')].map(e=>({text:(e.innerText||'').trim(),type:e.type||'',aria:e.getAttribute('aria-label')||''})).filter(x=>x.text||x.aria).slice(0,120)
 }));
 console.log(JSON.stringify(data,null,2));
 await context.close();
})();
