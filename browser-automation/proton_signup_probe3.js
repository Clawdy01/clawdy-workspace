const { chromium } = require('playwright-core');
(async() => {
  const browser = await chromium.launch({ executablePath: '/snap/bin/chromium', headless: true, args: ['--no-sandbox', '--disable-dev-shm-usage'] });
  const page = await browser.newPage({ viewport: { width: 1440, height: 1200 } });
  page.setDefaultTimeout(40000);
  await page.goto('https://account.proton.me/start', { waitUntil: 'networkidle' });
  const html = await page.content();
  console.log(html.slice(0,12000));
  await browser.close();
})().catch(err => { console.error(err); process.exit(1); });
