from pathlib import Path

root = Path('/home/clawdy/.openclaw/workspace')
src = (root / 'tmp' / 'ai-briefing-explicit-current-with-twenty-eighth-future-source-url-sample.txt').read_text()
src = src.replace('achtentwintigste', 'negenentwintigste')
src = src.replace(
    'https://github.blog/changelog/2028-04-28-example',
    'https://github.blog/changelog/2028-04-28-example | https://github.blog/changelog/2028-05-29-example',
    1,
)
src = src.replace(
    'https://github.blog/changelog/2028-04-28-example\nhttps://openai.com/index/example-orchestration/',
    'https://github.blog/changelog/2028-04-28-example\nhttps://github.blog/changelog/2028-05-29-example\nhttps://openai.com/index/example-orchestration/',
    1,
)
(root / 'tmp' / 'ai-briefing-explicit-current-with-twenty-ninth-future-source-url-sample.txt').write_text(src)
