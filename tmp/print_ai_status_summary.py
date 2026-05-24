import json
from pathlib import Path
j = json.loads(Path('/tmp/ai_status_after_fix.json').read_text())
print(json.dumps({
  'payload_ok': j['payload_audit']['ok'],
  'payload_text': j['payload_audit']['text'],
  'config_hash': j.get('proof_config_hash'),
  'proof_state': j.get('proof_state'),
  'proof_blocker_kind': j.get('proof_blocker_kind'),
}, ensure_ascii=False))
