const fs = require('fs');
const path = require('path');
const { launchSession } = require('./playwright_session');

function parseArgs(argv) {
  const positional = [];
  let outDir = '/home/clawdy/.openclaw/workspace/browser-automation/out';
  let slug = 'probe';
  let session = 'probe-default';

  for (let i = 0; i < argv.length; i += 1) {
    const arg = argv[i];
    if (arg === '--outdir') {
      outDir = argv[i + 1];
      i += 1;
      continue;
    }
    if (arg === '--slug') {
      slug = argv[i + 1] || slug;
      i += 1;
      continue;
    }
    if (arg === '--session') {
      session = argv[i + 1] || session;
      i += 1;
      continue;
    }
    positional.push(arg);
  }

  if (!positional[0]) {
    console.error('Usage: node probe_page.js <url> [outDir] [--slug <name>] [--session <name>] [--outdir <dir>]');
    process.exit(2);
  }
  if (positional[1] && outDir === '/home/clawdy/.openclaw/workspace/browser-automation/out') {
    outDir = positional[1];
  }

  const safeSlug = String(slug || 'probe')
    .trim()
    .toLowerCase()
    .replace(/[^a-z0-9._-]+/g, '-')
    .replace(/^-+|-+$/g, '') || 'probe';

  return {
    url: positional[0],
    outDir,
    slug: safeSlug,
    session,
  };
}

async function main() {
  const { url, outDir, slug, session } = parseArgs(process.argv.slice(2));
  fs.mkdirSync(outDir, { recursive: true });
  const { context, page, sessionDir } = await launchSession(session, {
    timeout: 40000,
    viewport: { width: 1440, height: 1200 },
  });
  await page.goto(url, { waitUntil: 'domcontentloaded' });
  await page.waitForTimeout(1500);
  const title = await page.title();
  const finalUrl = page.url();
  const checkedAt = new Date().toISOString();
  const bodyText = await page.locator('body').innerText().catch(() => '');
  const interactives = await page.locator('a, button, input, textarea, select, [role="button"], [role="link"]').evaluateAll(nodes =>
    nodes.map((n, i) => {
      const rect = typeof n.getBoundingClientRect === 'function' ? n.getBoundingClientRect() : { width: 0, height: 0 };
      const style = typeof window !== 'undefined' && typeof window.getComputedStyle === 'function'
        ? window.getComputedStyle(n)
        : null;
      const href = n.href || n.getAttribute('href') || '';
      const type = n.getAttribute('type') || '';
      const name = n.getAttribute('name') || '';
      const id = n.id || '';
      const placeholder = n.getAttribute('placeholder') || '';
      const ariaLabel = n.getAttribute('aria-label') || '';
      const value = typeof n.value === 'string' ? n.value : '';
      const text = (n.innerText || value || ariaLabel || placeholder || '').trim();
      const visible = Boolean(
        rect && rect.width > 0 && rect.height > 0 && style && style.visibility !== 'hidden' && style.display !== 'none'
      );
      return {
        i,
        tag: n.tagName,
        role: n.getAttribute('role') || '',
        text,
        href,
        type,
        name,
        id,
        placeholder,
        ariaLabel,
        value: value && type !== 'password' ? value : '',
        disabled: Boolean(n.disabled || n.getAttribute('aria-disabled') === 'true'),
        visible,
      };
    }).filter(x => x.text || x.href || x.name || x.id || x.placeholder || x.ariaLabel)
  ).catch(() => []);
  const forms = await page.locator('form').evaluateAll(nodes =>
    nodes.map((n, i) => ({
      i,
      id: n.id || '',
      name: n.getAttribute('name') || '',
      action: n.getAttribute('action') || '',
      method: n.getAttribute('method') || 'get'
    }))
  ).catch(() => []);

  const base = path.join(outDir, slug === 'probe' ? 'probe' : `probe-${slug}`);
  const payload = {
    checkedAt,
    url,
    title,
    finalUrl,
    slug,
    interactives,
    interactiveCount: interactives.length,
    forms,
    formCount: forms.length,
    bodyText: bodyText.slice(0, 12000),
    session,
    sessionDir,
  };
  await page.screenshot({ path: `${base}.png`, fullPage: true });
  fs.writeFileSync(`${base}.json`, JSON.stringify(payload, null, 2));
  console.log(JSON.stringify({ checkedAt, title, finalUrl, slug, interactives: interactives.length, forms: forms.length, outDir, session, sessionDir }, null, 2));
  await context.close();
}

main().catch(err => {
  console.error(err);
  process.exit(1);
});
