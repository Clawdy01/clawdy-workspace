#!/usr/bin/env python3
import sys
from faster_whisper import WhisperModel

if len(sys.argv) < 2:
    print('usage: transcribe-local-audio.py <audio>', file=sys.stderr)
    sys.exit(2)

model = WhisperModel('tiny', device='cpu', compute_type='int8')
segments, info = model.transcribe(sys.argv[1], beam_size=5, vad_filter=True)
text = ' '.join(seg.text.strip() for seg in segments).strip()
print(text)
