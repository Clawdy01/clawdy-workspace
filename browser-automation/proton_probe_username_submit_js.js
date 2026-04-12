const { chromium } = require('playwright-core');
const fs = require('fs');
const path = require('path');

const OUT_DIR = '/home/clawdy/.openclaw/workspace/browser-automation/out';
const USERNAME = 'clawdy01';

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
  await page.waitForLoadState('networkidle', { timeout: 15000 }).catch(() => {});

  const prep = await page.locator('#username').evaluate((el, username) => {
    el.style.display = 'block';
    el.style.visibility = 'visible';
    el.style.opacity = '1';
    el.style.position = 'relative';
    el.style.left = '0';
    el.style.top = '0';
    el.style.height = '40px';
    el.style.width = '280px';
    el.focus();
    el.value = username;
    el.dispatchEvent(new Event('input', { bubbles: true }));
    el.dispatchEvent(new Event('change', { bubbles: true }));
    return {
      value: el.value,
      ariaInvalid: el.getAttribute('aria-invalid'),
    };
  }, USERNAME);

  await page.getByRole('button', { name: /create free account now/i }).click();
  await page.waitForLoadState('networkidle', { timeout: 15000 }).catch(() => {});
  await page.waitForTimeout(3000);

  const screenshot = path.join(OUT_DIR, 'proton-username-submit-js.png');
  await page.screenshot({ path: screenshot, fullPage: true });

  const forms = await page.locator('input, button, select, textarea').evaluateAll(nodes =>
    nodes.map((n, idx) => ({
      index: idx,
      tag: n.tagName.toLowerCase(),
      type: n.getAttribute('type') || '',
      name: n.getAttribute('name') || '',
      id: n.getAttribute('id') || '',
      placeholder: n.getAttribute('placeholder') || '',
      ariaLabel: n.getAttribute('aria-label') || '',
      testId: n.getAttribute('data-testid') || '',
      text: (n.innerText || n.textContent || '').replace(/\s+/g, ' ').trim(),
      value: n.value || '',
    }))
  ).catch(() => []);

  const result = {
    checkedAt: new Date().toISOString(),
    username: USERNAME,
    prep,
    title: await page.title(),
    url: page.url(),
    excerpt: await page.locator('body').innerText().then(t => t.slice(0, 3000)).catch(() => ''),
    forms: forms.slice(0, 80),
    screenshot,
  };

  fs.writeFileSync(path.join(OUT_DIR, 'proton-username-submit-js.json'), JSON.stringify(result, null, 2));
  console.log(JSON.stringify(result, null, 2));
  await browser.close();
})().catch(err => {
  console.error(err && err.stack || String(err));
  process.exit(1);
});
