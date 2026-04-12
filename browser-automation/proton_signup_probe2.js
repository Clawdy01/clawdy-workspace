const { chromium } = require('playwright-core');
(async() => {
  const browser = await chromium.launch({ executablePath: '/snap/bin/chromium', headless: true, args: ['--no-sandbox', '--disable-dev-shm-usage'] });
  const page = await browser.newPage({ viewport: { width: 1440, height: 1200 } });
  page.setDefaultTimeout(30000);
  await page.goto('https://account.proton.me/start', { waitUntil: 'domcontentloaded' });
  const buttons = await page.locator('button, a').evaluateAll(nodes => nodes.map(n => ({text:(n.innerText||'').trim(), href:n.href||'', role:n.getAttribute('role')||'', type:n.getAttribute('type')||''})).filter(x => x.text));
  console.log(JSON.stringify(buttons.slice(0,80), null, 2));
  await browser.close();
})().catch(err => { console.error(err); process.exit(1); });
