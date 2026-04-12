const { chromium } = require('playwright-core');
const fs = require('fs');
(async() => {
  const browser = await chromium.launch({
    executablePath: '/snap/bin/chromium',
    headless: true,
    args: ['--no-sandbox', '--disable-dev-shm-usage']
  });
  const page = await browser.newPage({ viewport: { width: 1440, height: 1200 } });
  page.setDefaultTimeout(30000);
  await page.goto('https://account.proton.me/start', { waitUntil: 'domcontentloaded' });
  await page.screenshot({ path: '/home/clawdy/.openclaw/workspace/browser-automation/proton-start.png', fullPage: true });
  const title = await page.title();
  const url = page.url();
  const text = await page.locator('body').innerText().catch(() => '');
  console.log(JSON.stringify({ title, url, text: text.slice(0, 4000) }, null, 2));
  await browser.close();
})().catch(err => { console.error(err); process.exit(1); });
