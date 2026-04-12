const { chromium } = require('playwright-core');
const fs = require('fs');
const path = require('path');

const OUT_DIR = '/home/clawdy/.openclaw/workspace/browser-automation/out';
const URL = 'https://account.proton.me/start';

function detectFlags(text, url) {
  const hay = `${text}\n${url}`.toLowerCase();
  return {
    loginVisible: /sign in|log in|already have an account/.test(hay),
    signupVisible: /create account|get proton for free|free plan|sign up/.test(hay),
    captchaLikely: /captcha|human verification|verify you are human|recaptcha|hcaptcha/.test(hay),
    blocked: /access denied|temporarily unavailable|blocked|unusual traffic/.test(hay),
  };
}

async function collectActions(page) {
  const items = await page.locator('button, a, [role="button"]').evaluateAll(nodes =>
    nodes.map((n, idx) => ({
      index: idx,
      tag: n.tagName.toLowerCase(),
      text: (n.innerText || n.textContent || '').replace(/\s+/g, ' ').trim(),
      href: n.href || '',
      type: n.getAttribute('type') || '',
      ariaLabel: n.getAttribute('aria-label') || '',
      testId: n.getAttribute('data-testid') || '',
    }))
    .filter(x => x.text || x.ariaLabel)
  ).catch(() => []);

  return items
    .filter(x => /create account|get proton for free|free|sign up|continue|next|pass/i.test(`${x.text} ${x.ariaLabel}`))
    .slice(0, 20);
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

  await page.goto(URL, { waitUntil: 'domcontentloaded' });
  await page.waitForLoadState('networkidle', { timeout: 15000 }).catch(() => {});

  const title = await page.title();
  const url = page.url();
  const bodyText = await page.locator('body').innerText().catch(() => '');
  const flags = detectFlags(bodyText, url);
  const candidateActions = await collectActions(page);
  const screenshot = path.join(OUT_DIR, 'proton-status.png');
  await page.screenshot({ path: screenshot, fullPage: true });

  const result = {
    checkedAt: new Date().toISOString(),
    title,
    url,
    flags,
    candidateActions,
    excerpt: bodyText.slice(0, 2000),
    screenshot,
  };

  fs.writeFileSync(path.join(OUT_DIR, 'proton-status.json'), JSON.stringify(result, null, 2));
  console.log(JSON.stringify(result, null, 2));

  await browser.close();
})().catch(err => {
  console.error(err && err.stack || String(err));
  process.exit(1);
});
