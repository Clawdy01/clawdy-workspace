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

  const iframeEl = page.locator('iframe[title="Email address"]').first();
  await iframeEl.waitFor({ state: 'visible' });
  const frame = await iframeEl.elementHandle().then(h => h.contentFrame());
  if (!frame) throw new Error('Could not access Email address iframe');

  const input = frame.locator('input, textarea').first();
  await input.waitFor({ state: 'visible' });
  await input.fill(USERNAME);
  await input.press('Tab').catch(() => {});
  await page.getByRole('button', { name: /create free account now/i }).click();
  await page.waitForLoadState('networkidle', { timeout: 15000 }).catch(() => {});
  await page.waitForTimeout(2000);

  const result = await page.evaluate(() => {
    const nodes = Array.from(document.querySelectorAll('input, button, label, div, span, textarea, iframe'));
    const interesting = nodes.map((n, idx) => {
      const r = n.getBoundingClientRect();
      const s = window.getComputedStyle(n);
      return {
        index: idx,
        tag: n.tagName.toLowerCase(),
        id: n.id || '',
        className: typeof n.className === 'string' ? n.className : '',
        name: n.getAttribute('name') || '',
        type: n.getAttribute('type') || '',
        placeholder: n.getAttribute('placeholder') || '',
        ariaLabel: n.getAttribute('aria-label') || '',
        testId: n.getAttribute('data-testid') || '',
        text: (n.innerText || n.textContent || '').replace(/\s+/g, ' ').trim(),
        value: n.value || '',
        visible: !!(r.width && r.height) && s.visibility !== 'hidden' && s.display !== 'none',
        x: Math.round(r.x),
        y: Math.round(r.y),
        width: Math.round(r.width),
        height: Math.round(r.height),
      };
    }).filter(x => /password|get started|confirm|strength|human|verify|captcha|recovery|mail/i.test(`${x.id} ${x.className} ${x.name} ${x.type} ${x.placeholder} ${x.ariaLabel} ${x.testId} ${x.text}`));

    const passwordInputs = Array.from(document.querySelectorAll('input[type="password"], input')).map((n, idx) => ({
      index: idx,
      id: n.id || '',
      name: n.getAttribute('name') || '',
      type: n.getAttribute('type') || '',
      placeholder: n.getAttribute('placeholder') || '',
      ariaLabel: n.getAttribute('aria-label') || '',
      testId: n.getAttribute('data-testid') || '',
      valueLength: (n.value || '').length,
    }));

    return {
      title: document.title,
      text: (document.body.innerText || '').slice(0, 3000),
      interesting,
      passwordInputs,
      activeTag: document.activeElement ? document.activeElement.tagName.toLowerCase() : null,
      activeId: document.activeElement ? document.activeElement.id || '' : '',
    };
  });

  const screenshot = path.join(OUT_DIR, 'proton-password-step.png');
  await page.screenshot({ path: screenshot, fullPage: true });
  result.checkedAt = new Date().toISOString();
  result.url = page.url();
  result.username = USERNAME;
  result.screenshot = screenshot;

  fs.writeFileSync(path.join(OUT_DIR, 'proton-password-step.json'), JSON.stringify(result, null, 2));
  console.log(JSON.stringify(result, null, 2));
  await browser.close();
})().catch(err => {
  console.error(err && err.stack || String(err));
  process.exit(1);
});
