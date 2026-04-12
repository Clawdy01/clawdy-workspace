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

  const result = await page.evaluate(() => {
    function describe(el) {
      if (!el) return null;
      const r = el.getBoundingClientRect();
      const s = window.getComputedStyle(el);
      return {
        tag: el.tagName.toLowerCase(),
        id: el.id || '',
        className: typeof el.className === 'string' ? el.className : '',
        role: el.getAttribute('role') || '',
        name: el.getAttribute('name') || '',
        type: el.getAttribute('type') || '',
        text: (el.innerText || el.textContent || '').replace(/\s+/g, ' ').trim().slice(0, 200),
        testId: el.getAttribute('data-testid') || '',
        ariaLabel: el.getAttribute('aria-label') || '',
        visible: !!(r.width && r.height) && s.visibility !== 'hidden' && s.display !== 'none',
        x: Math.round(r.x), y: Math.round(r.y), width: Math.round(r.width), height: Math.round(r.height),
        display: s.display, visibility: s.visibility, opacity: s.opacity,
      };
    }

    const username = document.querySelector('#username');
    const chain = [];
    let n = username;
    for (let i = 0; n && i < 6; i++, n = n.parentElement) chain.push(describe(n));

    const candidates = Array.from(document.querySelectorAll('div, span, label, button, input, iframe'))
      .map(describe)
      .filter(x => /username|proton|email-input|input-element|field-two|create free account/i.test(`${x.id} ${x.className} ${x.text} ${x.testId} ${x.ariaLabel}`))
      .slice(0, 80);

    const iframes = Array.from(document.querySelectorAll('iframe')).map((f, idx) => ({
      index: idx,
      ...describe(f),
      src: f.getAttribute('src') || '',
      title: f.getAttribute('title') || '',
      nameAttr: f.getAttribute('name') || '',
    }));

    const active = document.activeElement;
    return {
      url: location.href,
      title: document.title,
      activeElement: describe(active),
      usernameChain: chain,
      candidates,
      iframes,
    };
  });

  const screenshot = path.join(OUT_DIR, 'proton-input-proxy.png');
  await page.screenshot({ path: screenshot, fullPage: true });
  result.screenshot = screenshot;

  fs.writeFileSync(path.join(OUT_DIR, 'proton-input-proxy.json'), JSON.stringify(result, null, 2));
  console.log(JSON.stringify(result, null, 2));
  await browser.close();
})().catch(err => {
  console.error(err && err.stack || String(err));
  process.exit(1);
});
