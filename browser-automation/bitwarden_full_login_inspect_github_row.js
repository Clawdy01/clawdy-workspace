const { execFileSync } = require('child_process');
const { launchSession } = require('./playwright_session');
function latestCode(){const py=String.raw`
import imaplib, email, re, html
from email.header import decode_header, make_header
from scripts.workspace_secrets import load_mail_config
conf=load_mail_config(); M=imaplib.IMAP4_SSL(conf['host'], conf.get('imapPort',993)); M.login(conf['username'], conf['password']); M.select('INBOX')
st,data=M.search(None,'ALL')
ids=data[0].split() if data and data[0] else []
for uid in reversed(ids[-30:]):
    st,msgdata=M.fetch(uid,'(RFC822)')
    msg=email.message_from_bytes(msgdata[0][1])
    subj=str(make_header(decode_header(msg.get('Subject',''))))
    if subj.strip().lower()!='your bitwarden verification code':
        continue
    body=''
    if msg.is_multipart():
        for part in msg.walk():
            if part.get_content_type() in ('text/plain','text/html'):
                body=part.get_payload(decode=True).decode(part.get_content_charset() or 'utf-8','ignore')
                if body: break
    else:
        body=msg.get_payload(decode=True).decode(msg.get_content_charset() or 'utf-8','ignore')
    text=html.unescape(re.sub('<[^>]+>',' ',body))
    m=re.search(r'\b(\d{6})\b', text)
    if m:
        print(m.group(1)); break
M.logout()`;return execFileSync('python3',['-c',py],{cwd:'/home/clawdy/.openclaw/workspace',encoding:'utf8',timeout:120000,env:{...process.env,PYTHONPATH:'/home/clawdy/.openclaw/workspace/scripts'}}).trim();}
(async()=>{
 const email=process.argv[2], password=process.argv[3];
 const {context,page}=await launchSession('bitwarden-session-test',{headless:true,timeout:45000});
 await page.goto('https://vault.bitwarden.com/#/login',{waitUntil:'domcontentloaded',timeout:60000}); await page.waitForTimeout(1500);
 const emailInput=page.locator('input[type="email"], input[name*="email" i], input[id*="email" i]').first(); if(await emailInput.count()){await emailInput.fill(email).catch(()=>null); await page.locator('button').filter({hasText:/continue|log in/i}).first().click().catch(()=>null); await page.waitForTimeout(1500);} 
 const passwordInput=page.locator('input[type="password"], input[name*="master" i], input[id*="master" i]').first(); if(await passwordInput.count()){await passwordInput.fill(password).catch(()=>null); await passwordInput.press('Enter').catch(()=>null);} 
 await page.getByRole('button',{name:/log in with master password/i}).click().catch(()=>null); await page.waitForTimeout(4000);
 if(page.url().includes('/device-verification')){ const code=latestCode(); await page.evaluate((value)=>{const el=document.querySelector('#verificationCode, input[name="verificationCode"], input[formcontrolname="code"]'); if(el){ el.value=value; el.dispatchEvent(new Event('input',{bubbles:true})); el.dispatchEvent(new Event('change',{bubbles:true}));}}, code).catch(()=>null); await page.locator('button, a').filter({hasText:/continue logging in|continue|verify/i}).first().click().catch(()=>null); await page.waitForTimeout(6000); }
 const addLater=page.locator('button, a').filter({hasText:/add it later/i}).first(); if(await addLater.count()){ await addLater.click().catch(()=>null); await page.waitForTimeout(1000); const skip=page.locator('button, a').filter({hasText:/skip to web app/i}).first(); if(await skip.count()) await skip.click().catch(()=>null);} 
 await page.goto('https://vault.bitwarden.com/#/vault?search=Github',{waitUntil:'domcontentloaded',timeout:60000}).catch(()=>null); await page.waitForTimeout(3000);
 await page.evaluate(()=>{ const skip=[...document.querySelectorAll('button,a')].find(el => (el.innerText||'').trim().toLowerCase()==='skip'); if(skip) skip.click(); }).catch(()=>null); await page.waitForTimeout(500);
 const data=await page.evaluate(()=>({
   matches:[...document.querySelectorAll('*')].filter(el => (el.innerText||'').trim()==='Github').slice(0,20).map(el=>({tag:el.tagName, cls:el.className||'', role:el.getAttribute('role')||'', outer:el.outerHTML.slice(0,1200)})),
   links:[...document.querySelectorAll('a[href]')].filter(el => (el.innerText||'').toLowerCase().includes('github')).map(el=>({text:el.innerText,href:el.href,outer:el.outerHTML.slice(0,500)})).slice(0,20),
   buttons:[...document.querySelectorAll('button')].filter(el => (el.innerText||'').toLowerCase().includes('github')).map(el=>({text:el.innerText,outer:el.outerHTML.slice(0,500)})).slice(0,20),
   body:document.body.innerText.slice(0,4000)
 }));
 console.log(JSON.stringify(data,null,2));
 await context.close();
})();
