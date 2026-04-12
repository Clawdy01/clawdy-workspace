const { chromium } = require('playwright-core');
(async() => {
  const browser = await chromium.launch({
    executablePath: '/snap/bin/chromium',
    headless: true,
    args: ['--no-sandbox', '--disable-dev-shm-usage']
  });
  const page = await browser.newPage();
  await page.goto('https://example.com', { waitUntil: 'domcontentloaded', timeout: 30000 });
  console.log(await page.title());
  await browser.close();
})().catch(err => { console.error(err); process.exit(1); });
