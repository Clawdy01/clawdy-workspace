const fs = require('fs');
const { launchSession } = require('./playwright_session');
(async()=>{
  const title = process.argv[2] || 'openclaw01-clawdy';
  const keyPath = process.argv[3] || '/home/clawdy/.ssh/id_ed25519_github_clawdy.pub';
  const key = fs.readFileSync(keyPath, 'utf8').trim();
  const { context, page } = await launchSession('github-shared', { headless: true, timeout: 45000 });
  const out = { ok: false, title };
  try {
    await page.goto('https://github.com/settings/ssh/new', { waitUntil: 'domcontentloaded', timeout: 60000 });
    await page.waitForTimeout(2500);
    out.before = { url: page.url(), title: await page.title(), body: ((await page.textContent('body')) || '').slice(0, 3000) };
    await page.locator('#ssh_key_title, input[name="ssh_key[title]"]').first().fill(title).catch(() => null);
    await page.locator('#ssh_key_key, textarea[name="ssh_key[key]"]').first().fill(key).catch(() => null);
    await page.locator('button').filter({ hasText: /add ssh key/i }).first().click().catch(() => null);
    await page.waitForTimeout(5000);
    out.after = { url: page.url(), title: await page.title(), body: ((await page.textContent('body')) || '').slice(0, 4000) };
    out.ok = /settings\/keys/.test(page.url()) || /SSH keys/.test(out.after.title);
  } finally {
    console.log(JSON.stringify(out, null, 2));
    await context.close();
  }
})();
