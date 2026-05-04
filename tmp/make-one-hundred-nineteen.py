from pathlib import Path

root = Path('/home/clawdy/.openclaw/workspace')
for kind in ['list-cases', 'mixed']:
    src = root / 'tmp' / f'validate-one-hundred-eighteen-valid-{kind}.py'
    dst = root / 'tmp' / f'validate-one-hundred-nineteen-valid-{kind}.py'
    text = src.read_text()
    text = text.replace('honderdachttien', 'honderdnegentien')
    text = text.replace('117]', '117, 118]')
    text = text.replace('[:118]', '[:119]')
    text = text.replace('len(valid_cases) != 118', 'len(valid_cases) != 119')
    text = text.replace('kon geen honderdachttien geldige casenamen vinden', 'kon geen honderdnegentien geldige casenamen vinden')
    text = text.replace('alle honderdachttien geldige first-seen cases', 'alle honderdnegentien geldige first-seen cases')
    text = text.replace('honderdachttien geldige first-seen cases', 'honderdnegentien geldige first-seen cases')
    dst.write_text(text)
