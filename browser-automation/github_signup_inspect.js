const { launchSession } = require('./playwright_session');
(async()=>{
 const {context,page}=await launchSession('github-signup-inspect',{headless:true, timeout:45000});
 await page.goto('https://github.com/signup',{waitUntil:'domcontentloaded', timeout:60000});
 await page.waitForTimeout(3000);
 const data = await page.evaluate(() => ({
   title: document.title,
   url: location.href,
   body: document.body.innerText.slice(0,3000),
   buttons:[...document.querySelectorAll('button,input[type="submit"],input[type="button"]')].map(e=>({tag:e.tagName,text:e.innerText||e.value||'',type:e.type||'',id:e.id||'',name:e.name||'',cls:e.className||''})).slice(0,30),
   inputs:[...document.querySelectorAll('input')].map(e=>({type:e.type||'',id:e.id||'',name:e.name||'',placeholder:e.placeholder||'',value:e.value||''})).slice(0,40),
   forms:[...document.querySelectorAll('form')].map(e=>({action:e.action||'',method:e.method||'',id:e.id||'',cls:e.className||''})).slice(0,20)
 }));
 console.log(JSON.stringify(data,null,2));
 await context.close();
})();
