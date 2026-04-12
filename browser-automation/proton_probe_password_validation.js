const { chromium } = require('playwright-core');
const fs = require('fs');
const path = require('path');

const OUT_DIR = '/home/clawdy/.openclaw/workspace/browser-automation/out';
const USERNAME = 'clawdy01';
const TEST_PASSWORD = 'Short123!';

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

  const emailInput = frame.locator('input, textarea').first();
  await emailInput.waitFor({ state: 'visible' });
  await emailInput.fill(USERNAME);
  await emailInput.press('Tab').catch(() => {});
  await page.getByRole('button', { name: /create free account now/i }).click();
  await page.waitForLoadState('networkidle', { timeout: 15000 }).catch(() => {});
  await page.waitForTimeout(1500);

  await page.locator('#password').fill(TEST_PASSWORD);
  await page.locator('#password-confirm').fill(TEST_PASSWORD);
  await page.locator('#password-confirm').press('Tab').catch(() => {});
  await page.waitForTimeout(1200);

  const result = await page.evaluate(() => {
    const fields = ['password', 'password-confirm'].map(id => {
      const el = document.getElementById(id);
      if (!el) return { id, missing: true };
      const describedBy = (el.getAttribute('aria-describedby') || '').split(/\s+/).filter(Boolean);
      const describedTexts = describedBy.map(x => {
        const node = document.getElementById(x);
        return node ? (node.innerText || node.textContent || '').replace(/\s+/g, ' ').trim() : '';
      }).filter(Boolean);
      return {
        id,
        type: el.getAttribute('type') || '',
        ariaInvalid: el.getAttribute('aria-invalid'),
        describedBy,
        describedTexts,
        valueLength: (el.value || '').length,
      };
    });

    const interesting = Array.from(document.querySelectorAll('div, span, label, p, li')).map((n, idx) => ({
      index: idx,
      id: n.id || '',
      className: typeof n.className === 'string' ? n.className : '',
      text: (n.innerText || n.textContent || '').replace(/\s+/g, ' ').trim(),
    })).filter(x => /password|strong|weak|match|confirm|characters|secure|invalid|required/i.test(`${x.id} ${x.className} ${x.text}`));

    const getStarted = document.querySelector('button[type="submit"]');
    return {
      title: document.title,
      text: (document.body.innerText || '').slice(0, 2500),
      fields,
      interesting: interesting.slice(0, 80),
      submitDisabled: getStarted ? !!getStarted.disabled : null,
      submitText: getStarted ? (getStarted.innerText || getStarted.textContent || '').replace(/\s+/g, ' ').trim() : null,
    };
  });

  const screenshot = path.join(OUT_DIR, 'proton-password-validation.png');
  await page.screenshot({ path: screenshot, fullPage: true });
  result.checkedAt = new Date().toISOString();
  result.url = page.url();
  result.username = USERNAME;
  result.testPasswordLength = TEST_PASSWORD.length;
  result.screenshot = screenshot;

  fs.writeFileSync(path.join(OUT_DIR, 'proton-password-validation.json'), JSON.stringify(result, null, 2));
  console.log(JSON.stringify(result, null, 2));
  await browser.close();
})().catch(err => {
  console.error(err && err.stack || String(err));
  process.exit(1);
});
