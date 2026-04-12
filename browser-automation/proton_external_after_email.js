const { chromium } = require('playwright-core');
(async () => {
  const email = process.argv[2] || 'clawdy01@christiandekok.nl';
  const browser = await chromium.launch({ executablePath: '/snap/bin/chromium', headless: true, args: ['--no-sandbox', '--disable-dev-shm-usage'] });
  const page = await browser.newPage({ viewport: { width: 1440, height: 1200 } });
  page.setDefaultTimeout(45000);
  await page.goto('https://account.proton.me/start', { waitUntil: 'domcontentloaded' });
  await page.waitForLoadState('networkidle', { timeout: 15000 }).catch(() => {});
  await page.getByRole('button', { name: /use your current email/i }).click();
  await page.waitForTimeout(1200);
  await page.locator('#email').evaluate(el => el.focus());
  await page.keyboard.type(email, { delay: 35 });
  await page.locator('button[type="submit"]').first().evaluate(el => el.click());
  await page.waitForLoadState('networkidle', { timeout: 15000 }).catch(() => {});
  await page.waitForTimeout(3000);
  const data = await page.evaluate(() => ({
    title: document.title,
    url: location.href,
    text: (document.body.innerText || '').replace(/\s+/g, ' ').trim().slice(0, 6000),
    buttons: Array.from(document.querySelectorAll('button')).map(el => ({ text: (el.innerText || el.textContent || '').replace(/\s+/g, ' ').trim(), disabled: !!el.disabled })).filter(x => x.text),
    inputs: Array.from(document.querySelectorAll('input')).map(el => ({ id: el.id || '', type: el.type || '', value: (el.value || '').slice(0,120), ariaInvalid: el.getAttribute('aria-invalid') }))
  }));
  console.log(JSON.stringify(data, null, 2));
  await browser.close();
})().catch(err => { console.error(err && err.stack || String(err)); process.exit(1); });
