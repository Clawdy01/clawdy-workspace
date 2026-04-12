#!/usr/bin/env python3
import argparse
from faster_whisper import WhisperModel

parser = argparse.ArgumentParser()
parser.add_argument('audio')
parser.add_argument('--model', default='medium')
parser.add_argument('--language', default='nl')
parser.add_argument('--prompt', default='Dit is een informeel Nederlands spraakbericht met mogelijk kinderen en meerdere stemmen. Transcribeer letterlijk en zo goed mogelijk.')
args = parser.parse_args()

model = WhisperModel(args.model, device='cpu', compute_type='int8')
segments, info = model.transcribe(
    args.audio,
    beam_size=7,
    best_of=5,
    vad_filter=True,
    language=args.language,
    initial_prompt=args.prompt,
    condition_on_previous_text=True,
)
for seg in segments:
    text = seg.text.strip()
    if text:
        print(f"[{seg.start:0.2f}-{seg.end:0.2f}] {text}")
