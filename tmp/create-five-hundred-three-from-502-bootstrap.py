#!/usr/bin/env python3
from pathlib import Path

src = Path('/home/clawdy/.openclaw/workspace/tmp/create-five-hundred-two-from-501.py')
dst = Path('/home/clawdy/.openclaw/workspace/tmp/create-five-hundred-three-from-502.py')
text = src.read_text()

placeholders = [
    ("'create-five-hundred-one-assets.py'", "'__SRC_ASSETS__'"),
    ("'create-five-hundred-two-assets.py'", "'__DST_ASSETS__'"),
    ("'create-five-hundred-one-bootstrap.py'", "'__SRC_BOOTSTRAP__'"),
    ("'create-five-hundred-two-bootstrap.py'", "'__DST_BOOTSTRAP__'"),
    ("'create-five-hundred-one-minimal.py'", "'__SRC_MINIMAL__'"),
    ("'create-five-hundred-two-minimal.py'", "'__DST_MINIMAL__'"),
    ("'make-five-hundred-one.py'", "'__SRC_MAKE__'"),
    ("'make-five-hundred-two.py'", "'__DST_MAKE__'"),
    ("'create-five-hundred-one-files.py'", "'__SRC_FILES__'"),
    ("'create-five-hundred-two-files.py'", "'__DST_FILES__'"),
    ("'create-five-hundred-one.py'", "'__SRC_CREATE__'"),
    ("'create-five-hundred-two.py'", "'__DST_CREATE__'"),
    ("'generate-validate-five-hundred-one.py'", "'__SRC_GEN__'"),
    ("'generate-validate-five-hundred-two.py'", "'__DST_GEN__'"),
    ("'validate-five-hundred-one-valid-list-cases.py'", "'__SRC_LIST__'"),
    ("'validate-five-hundred-two-valid-list-cases.py'", "'__DST_LIST__'"),
    ("'validate-five-hundred-one-valid-mixed.py'", "'__SRC_MIXED__'"),
    ("'validate-five-hundred-two-valid-mixed.py'", "'__DST_MIXED__'"),
    ("'verify-five-hundred-one.py'", "'__SRC_VERIFY__'"),
    ("'verify-five-hundred-two.py'", "'__DST_VERIFY__'"),
    ("('five-hundred-one', 'five-hundred-two')", "('__PAIR_EN_OLD__', '__PAIR_EN_NEW__')"),
    ("('vijfhonderdeen', 'vijfhonderdtwee')", "('__PAIR_NL_OLD__', '__PAIR_NL_NEW__')"),
    ("('all_cases[:486]', 'all_cases[:487]')", "('__PAIR_ALL_OLD__', '__PAIR_ALL_NEW__')"),
    ("('{UNKNOWN, TYPO}][:486]', '{UNKNOWN, TYPO}][:487]')", "('__PAIR_UNKNOWN_OLD__', '__PAIR_UNKNOWN_NEW__')"),
    ("('[:486]', '[:487]')", "('__PAIR_SLICE_OLD__', '__PAIR_SLICE_NEW__')"),
    ("('!= 486', '!= 487')", "('__PAIR_NE_OLD__', '__PAIR_NE_NEW__')"),
    ("('kreeg 486', 'kreeg 487')", "('__PAIR_KREEG_OLD__', '__PAIR_KREEG_NEW__')"),
    ("('len(valid_cases) != 486', 'len(valid_cases) != 487')", "('__PAIR_LEN_OLD__', '__PAIR_LEN_NEW__')"),
]
for old, ph in placeholders:
    if old not in text:
        raise SystemExit(f'missing template snippet: {old}')
    text = text.replace(old, ph)

finals = [
    ("'__SRC_ASSETS__'", "'create-five-hundred-two-assets.py'"),
    ("'__DST_ASSETS__'", "'create-five-hundred-three-assets.py'"),
    ("'__SRC_BOOTSTRAP__'", "'create-five-hundred-two-bootstrap.py'"),
    ("'__DST_BOOTSTRAP__'", "'create-five-hundred-three-bootstrap.py'"),
    ("'__SRC_MINIMAL__'", "'create-five-hundred-two-minimal.py'"),
    ("'__DST_MINIMAL__'", "'create-five-hundred-three-minimal.py'"),
    ("'__SRC_MAKE__'", "'make-five-hundred-two.py'"),
    ("'__DST_MAKE__'", "'make-five-hundred-three.py'"),
    ("'__SRC_FILES__'", "'create-five-hundred-two-files.py'"),
    ("'__DST_FILES__'", "'create-five-hundred-three-files.py'"),
    ("'__SRC_CREATE__'", "'create-five-hundred-two.py'"),
    ("'__DST_CREATE__'", "'create-five-hundred-three.py'"),
    ("'__SRC_GEN__'", "'generate-validate-five-hundred-two.py'"),
    ("'__DST_GEN__'", "'generate-validate-five-hundred-three.py'"),
    ("'__SRC_LIST__'", "'validate-five-hundred-two-valid-list-cases.py'"),
    ("'__DST_LIST__'", "'validate-five-hundred-three-valid-list-cases.py'"),
    ("'__SRC_MIXED__'", "'validate-five-hundred-two-valid-mixed.py'"),
    ("'__DST_MIXED__'", "'validate-five-hundred-three-valid-mixed.py'"),
    ("'__SRC_VERIFY__'", "'verify-five-hundred-two.py'"),
    ("'__DST_VERIFY__'", "'verify-five-hundred-three.py'"),
    ("('__PAIR_EN_OLD__', '__PAIR_EN_NEW__')", "('five-hundred-two', 'five-hundred-three')"),
    ("('__PAIR_NL_OLD__', '__PAIR_NL_NEW__')", "('vijfhonderdtwee', 'vijfhonderddrie')"),
    ("('__PAIR_ALL_OLD__', '__PAIR_ALL_NEW__')", "('all_cases[:487]', 'all_cases[:488]')"),
    ("('__PAIR_UNKNOWN_OLD__', '__PAIR_UNKNOWN_NEW__')", "('{UNKNOWN, TYPO}][:487]', '{UNKNOWN, TYPO}][:488]')"),
    ("('__PAIR_SLICE_OLD__', '__PAIR_SLICE_NEW__')", "('[:487]', '[:488]')"),
    ("('__PAIR_NE_OLD__', '__PAIR_NE_NEW__')", "('!= 487', '!= 488')"),
    ("('__PAIR_KREEG_OLD__', '__PAIR_KREEG_NEW__')", "('kreeg 487', 'kreeg 488')"),
    ("('__PAIR_LEN_OLD__', '__PAIR_LEN_NEW__')", "('len(valid_cases) != 487', 'len(valid_cases) != 488')"),
]
for old, new in finals:
    text = text.replace(old, new)

dst.write_text(text)
print(dst)
