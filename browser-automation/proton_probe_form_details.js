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
  await page.waitForLoadState('networkidle', { timeout: 15000 }).catch(() => {});

  const fields = await page.evaluate(() => {
    const nodes = Array.from(document.querySelectorAll('input, button, select, textarea, label'));
    return nodes.map((n, idx) => ({
      index: idx,
      tag: n.tagName.toLowerCase(),
      type: n.getAttribute('type') || '',
      name: n.getAttribute('name') || '',
      id: n.getAttribute('id') || '',
      forAttr: n.getAttribute('for') || '',
      placeholder: n.getAttribute('placeholder') || '',
      value: n.value || '',
      ariaLabel: n.getAttribute('aria-label') || '',
      autoComplete: n.getAttribute('autocomplete') || '',
      role: n.getAttribute('role') || '',
      testId: n.getAttribute('data-testid') || '',
      text: (n.innerText || n.textContent || '').replace(/\s+/g, ' ').trim(),
    }));
  });

  const interesting = fields.filter(x => {
    const hay = `${x.tag} ${x.type} ${x.name} ${x.id} ${x.forAttr} ${x.placeholder} ${x.ariaLabel} ${x.autoComplete} ${x.text} ${x.testId}`.toLowerCase();
    return /user|email|account|name|proton|free|create|sign|continue|next|password/.test(hay);
  });

  const result = {
    checkedAt: new Date().toISOString(),
    title: await page.title(),
    url: page.url(),
    interesting,
  };

  fs.writeFileSync(path.join(OUT_DIR, 'proton-form-details.json'), JSON.stringify(result, null, 2));
  console.log(JSON.stringify(result, null, 2));
  await browser.close();
})().catch(err => {
  console.error(err && err.stack || String(err));
  process.exit(1);
});
