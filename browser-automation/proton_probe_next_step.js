const { chromium } = require('playwright-core');
const fs = require('fs');
const path = require('path');

const OUT_DIR = '/home/clawdy/.openclaw/workspace/browser-automation/out';

(async () => {
  fs.mkdirSync(OUT_DIR, { recursive: true });
  const browser = await chromium.launch({
    executablePath: '/snap/bin/chromium',
    headless: true,
    args: ['--no-sandbox', '--disable-dev-shm-usage'],
  });
  const page = await browser.newPage({ viewport: { width: 1440, height: 1200 } });
  page.setDefaultTimeout(45000);

  await page.goto('https://account.proton.me/start', { waitUntil: 'domcontentloaded' });
  await page.getByRole('button', { name: /create free account now/i }).click();
  await page.waitForLoadState('networkidle', { timeout: 15000 }).catch(() => {});

  const title = await page.title();
  const url = page.url();
  const text = await page.locator('body').innerText().catch(() => '');
  const screenshot = path.join(OUT_DIR, 'proton-next-step.png');
  await page.screenshot({ path: screenshot, fullPage: true });

  const forms = await page.locator('input, select, textarea, button').evaluateAll(nodes =>
    nodes.map((n, idx) => ({
      index: idx,
      tag: n.tagName.toLowerCase(),
      type: n.getAttribute('type') || '',
      name: n.getAttribute('name') || '',
      placeholder: n.getAttribute('placeholder') || '',
      ariaLabel: n.getAttribute('aria-label') || '',
      text: (n.innerText || '').replace(/\s+/g, ' ').trim(),
      testId: n.getAttribute('data-testid') || '',
    }))
  ).catch(() => []);

  const result = {
    checkedAt: new Date().toISOString(),
    title,
    url,
    excerpt: text.slice(0, 2500),
    forms: forms.slice(0, 80),
    screenshot,
  };

  fs.writeFileSync(path.join(OUT_DIR, 'proton-next-step.json'), JSON.stringify(result, null, 2));
  console.log(JSON.stringify(result, null, 2));
  await browser.close();
})().catch(err => {
  console.error(err && err.stack || String(err));
  process.exit(1);
});
