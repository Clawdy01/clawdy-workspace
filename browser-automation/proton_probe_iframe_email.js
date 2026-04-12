const { chromium } = require('playwright-core');
const fs = require('fs');
const path = require('path');

const OUT_DIR = '/home/clawdy/.openclaw/workspace/browser-automation/out';
const VALUE = 'clawdy01';

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

  const iframeEl = page.locator('iframe[title="Email address"]').first();
  await iframeEl.waitFor({ state: 'visible' });
  const frame = await iframeEl.elementHandle().then(h => h.contentFrame());
  if (!frame) throw new Error('Could not access Email address iframe');

  const initial = await frame.evaluate(() => {
    const nodes = Array.from(document.querySelectorAll('input, textarea, button, div, span, label'));
    return nodes.map((n, idx) => ({
      index: idx,
      tag: n.tagName.toLowerCase(),
      id: n.id || '',
      name: n.getAttribute('name') || '',
      type: n.getAttribute('type') || '',
      placeholder: n.getAttribute('placeholder') || '',
      ariaLabel: n.getAttribute('aria-label') || '',
      text: (n.innerText || n.textContent || '').replace(/\s+/g, ' ').trim(),
      value: n.value || '',
    })).filter(x => /email|user|name|address|input|challenge/i.test(`${x.id} ${x.name} ${x.placeholder} ${x.ariaLabel} ${x.text}`));
  });

  const input = frame.locator('input, textarea').first();
  await input.waitFor({ state: 'visible' });
  await input.fill(VALUE);
  await input.press('Tab').catch(() => {});
  await page.waitForTimeout(1000);

  const post = await frame.evaluate(() => {
    const active = document.activeElement;
    const inputs = Array.from(document.querySelectorAll('input, textarea')).map((n, idx) => ({
      index: idx,
      id: n.id || '',
      name: n.getAttribute('name') || '',
      type: n.getAttribute('type') || '',
      placeholder: n.getAttribute('placeholder') || '',
      ariaLabel: n.getAttribute('aria-label') || '',
      value: n.value || '',
    }));
    return {
      activeTag: active ? active.tagName.toLowerCase() : null,
      activeId: active ? active.id || '' : '',
      inputs,
      text: (document.body.innerText || '').replace(/\s+/g, ' ').trim().slice(0, 1000),
    };
  });

  const pageValue = await page.locator('#username').evaluate(el => ({ value: el.value, ariaInvalid: el.getAttribute('aria-invalid') }));

  await page.getByRole('button', { name: /create free account now/i }).click();
  await page.waitForLoadState('networkidle', { timeout: 15000 }).catch(() => {});
  await page.waitForTimeout(2000);

  const screenshot = path.join(OUT_DIR, 'proton-iframe-email.png');
  await page.screenshot({ path: screenshot, fullPage: true });

  const result = {
    checkedAt: new Date().toISOString(),
    initial,
    post,
    pageValue,
    title: await page.title(),
    url: page.url(),
    excerpt: await page.locator('body').innerText().then(t => t.slice(0, 2500)).catch(() => ''),
    screenshot,
  };

  fs.writeFileSync(path.join(OUT_DIR, 'proton-iframe-email.json'), JSON.stringify(result, null, 2));
  console.log(JSON.stringify(result, null, 2));
  await browser.close();
})().catch(err => {
  console.error(err && err.stack || String(err));
  process.exit(1);
});
