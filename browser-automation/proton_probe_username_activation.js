const { chromium } = require('playwright-core');
const fs = require('fs');
const path = require('path');

const OUT_DIR = '/home/clawdy/.openclaw/workspace/browser-automation/out';

async function snapshot(page, name) {
  const screenshot = path.join(OUT_DIR, `${name}.png`);
  await page.screenshot({ path: screenshot, fullPage: true });
  return screenshot;
}

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

  const before = await page.evaluate(() => {
    const input = document.querySelector('#username');
    const label = Array.from(document.querySelectorAll('label, button, div, span')).find(n => /username/i.test((n.innerText || n.textContent || '').trim()));
    function box(el) {
      if (!el) return null;
      const r = el.getBoundingClientRect();
      const s = window.getComputedStyle(el);
      return {
        tag: el.tagName.toLowerCase(),
        text: (el.innerText || el.textContent || '').replace(/\s+/g, ' ').trim().slice(0, 200),
        visible: !!(r.width && r.height) && s.visibility !== 'hidden' && s.display !== 'none',
        x: Math.round(r.x), y: Math.round(r.y), width: Math.round(r.width), height: Math.round(r.height),
        opacity: s.opacity, display: s.display, visibility: s.visibility,
      };
    }
    return {
      input: box(input),
      label: box(label),
      activeTag: document.activeElement ? document.activeElement.tagName.toLowerCase() : null,
      activeId: document.activeElement ? document.activeElement.id || '' : '',
    };
  });

  const attempts = [];
  const actions = [
    async () => page.locator('label').filter({ hasText: /username/i }).first().click(),
    async () => page.getByText(/username/i).first().click(),
    async () => page.locator('#username').evaluate(el => el.scrollIntoView({ block: 'center' })),
    async () => page.locator('#username').evaluate(el => {
      el.style.display = 'block';
      el.style.visibility = 'visible';
      el.style.opacity = '1';
      el.style.position = 'relative';
      el.style.left = '0';
      el.style.top = '0';
      el.style.height = '40px';
      el.style.width = '280px';
      el.focus();
    }),
    async () => page.locator('#username').fill('clawdy01-js').catch(() => {}),
  ];

  for (const [i, action] of actions.entries()) {
    try {
      await action();
      await page.waitForTimeout(500);
    } catch (e) {
      attempts.push({ step: i + 1, error: String(e.message || e) });
      continue;
    }
    const state = await page.evaluate(() => {
      const input = document.querySelector('#username');
      const r = input ? input.getBoundingClientRect() : null;
      const s = input ? window.getComputedStyle(input) : null;
      return {
        value: input ? input.value : null,
        visible: !!(r && r.width && r.height) && s.visibility !== 'hidden' && s.display !== 'none',
        x: r ? Math.round(r.x) : null,
        y: r ? Math.round(r.y) : null,
        width: r ? Math.round(r.width) : null,
        height: r ? Math.round(r.height) : null,
        display: s ? s.display : null,
        visibility: s ? s.visibility : null,
        opacity: s ? s.opacity : null,
        activeTag: document.activeElement ? document.activeElement.tagName.toLowerCase() : null,
        activeId: document.activeElement ? document.activeElement.id || '' : '',
      };
    });
    attempts.push({ step: i + 1, state });
  }

  const finalInput = await page.locator('#username').evaluate(el => {
    el.value = 'clawdy01-js';
    el.dispatchEvent(new Event('input', { bubbles: true }));
    el.dispatchEvent(new Event('change', { bubbles: true }));
    return {
      value: el.value,
      ariaInvalid: el.getAttribute('aria-invalid'),
      describedBy: el.getAttribute('aria-describedby'),
    };
  });

  const buttonTexts = await page.locator('button').evaluateAll(nodes => nodes.map(n => (n.innerText || n.textContent || '').replace(/\s+/g, ' ').trim()).filter(Boolean));
  const screenshot = await snapshot(page, 'proton-username-activation');
  const result = { checkedAt: new Date().toISOString(), before, attempts, finalInput, buttonTexts, screenshot, url: page.url(), title: await page.title() };
  fs.writeFileSync(path.join(OUT_DIR, 'proton-username-activation.json'), JSON.stringify(result, null, 2));
  console.log(JSON.stringify(result, null, 2));

  await browser.close();
})().catch(err => {
  console.error(err && err.stack || String(err));
  process.exit(1);
});
