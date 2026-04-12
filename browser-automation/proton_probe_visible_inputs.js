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

  const data = await page.evaluate(() => {
    const items = Array.from(document.querySelectorAll('input, button, label')).map((n, idx) => {
      const r = n.getBoundingClientRect();
      const style = window.getComputedStyle(n);
      return {
        index: idx,
        tag: n.tagName.toLowerCase(),
        id: n.id || '',
        type: n.getAttribute('type') || '',
        text: (n.innerText || n.textContent || '').replace(/\s+/g, ' ').trim(),
        ariaLabel: n.getAttribute('aria-label') || '',
        testId: n.getAttribute('data-testid') || '',
        visible: !!(r.width && r.height) && style.visibility !== 'hidden' && style.display !== 'none',
        x: Math.round(r.x),
        y: Math.round(r.y),
        width: Math.round(r.width),
        height: Math.round(r.height),
      };
    });
    return items.filter(x => /username|proton|create|email|free|account/i.test(`${x.id} ${x.text} ${x.ariaLabel} ${x.testId}`));
  });

  const screenshot = path.join(OUT_DIR, 'proton-visible-inputs.png');
  await page.screenshot({ path: screenshot, fullPage: true });
  const result = { checkedAt: new Date().toISOString(), url: page.url(), data, screenshot };
  fs.writeFileSync(path.join(OUT_DIR, 'proton-visible-inputs.json'), JSON.stringify(result, null, 2));
  console.log(JSON.stringify(result, null, 2));
  await browser.close();
})().catch(err => {
  console.error(err && err.stack || String(err));
  process.exit(1);
});
