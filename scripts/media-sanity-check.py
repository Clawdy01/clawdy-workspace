#!/usr/bin/env python3
import argparse
import json
import mimetypes
import subprocess
import sys
from pathlib import Path


def run(cmd):
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        raise RuntimeError(result.stderr.strip() or result.stdout.strip() or 'command failed')
    return result.stdout


def parse_json_output(cmd):
    return json.loads(run(cmd) or '{}')


def detect_kind(path: Path):
    mime, _ = mimetypes.guess_type(str(path))
    if mime:
        if mime.startswith('video/'):
            return 'video'
        if mime.startswith('audio/'):
            return 'audio'
        if mime.startswith('image/'):
            return 'image'
    suffix = path.suffix.lower()
    if suffix in {'.mp4', '.mov', '.mkv', '.webm', '.avi', '.m4v'}:
        return 'video'
    if suffix in {'.wav', '.mp3', '.m4a', '.flac', '.ogg', '.aac'}:
        return 'audio'
    if suffix in {'.png', '.jpg', '.jpeg', '.gif', '.webp', '.bmp', '.tif', '.tiff'}:
        return 'image'
    return 'unknown'


def ffprobe_summary(path: Path):
    data = parse_json_output([
        'ffprobe', '-v', 'error',
        '-show_entries', 'format=duration,size,bit_rate:stream=index,codec_type,codec_name,width,height,pix_fmt,r_frame_rate,sample_rate,channels',
        '-of', 'json',
        str(path),
    ])
    fmt = data.get('format') or {}
    streams = data.get('streams') or []
    summary = {
        'duration_seconds': float(fmt['duration']) if fmt.get('duration') not in (None, 'N/A') else None,
        'size_bytes': int(fmt['size']) if fmt.get('size') not in (None, 'N/A') else None,
        'bit_rate': int(fmt['bit_rate']) if fmt.get('bit_rate') not in (None, 'N/A') else None,
        'streams': streams,
    }
    return summary


def image_summary(path: Path):
    data = parse_json_output(['identify', '-format', '{"width":%w,"height":%h,"colorspace":"%[colorspace]","format":"%m"}', str(path)])
    return data


def audio_summary(path: Path):
    text = run(['soxi', str(path)])
    summary = {}
    for line in text.splitlines():
        if ':' not in line:
            continue
        key, value = line.split(':', 1)
        key = key.strip().lower().replace(' ', '_')
        summary[key] = value.strip()
    return summary


def summarize_path(path: Path):
    path = path.expanduser().resolve()
    if not path.exists():
        raise FileNotFoundError(f'bestand bestaat niet: {path}')
    kind = detect_kind(path)
    summary = {
        'path': str(path),
        'exists': True,
        'kind': kind,
        'size_bytes': path.stat().st_size,
    }
    if kind == 'video':
        probe = ffprobe_summary(path)
        summary.update({
            'duration_seconds': probe['duration_seconds'],
            'bit_rate': probe['bit_rate'],
        })
        video_stream = next((s for s in probe['streams'] if s.get('codec_type') == 'video'), None)
        audio_stream = next((s for s in probe['streams'] if s.get('codec_type') == 'audio'), None)
        if video_stream:
            summary['video'] = {
                'codec': video_stream.get('codec_name'),
                'width': video_stream.get('width'),
                'height': video_stream.get('height'),
                'pixel_format': video_stream.get('pix_fmt'),
                'frame_rate': video_stream.get('r_frame_rate'),
            }
        if audio_stream:
            summary['audio'] = {
                'codec': audio_stream.get('codec_name'),
                'sample_rate': audio_stream.get('sample_rate'),
                'channels': audio_stream.get('channels'),
            }
    elif kind == 'audio':
        probe = ffprobe_summary(path)
        summary.update({
            'duration_seconds': probe['duration_seconds'],
            'bit_rate': probe['bit_rate'],
            'audio': audio_summary(path),
        })
    elif kind == 'image':
        summary['image'] = image_summary(path)
    return summary


def build_parser():
    parser = argparse.ArgumentParser(description='Snelle sanity-check voor video-, audio- en image-output.')
    parser.add_argument('paths', nargs='+', help='Een of meer mediabestanden om te inspecteren')
    parser.add_argument('--json', action='store_true', help='Geef output als JSON')
    return parser


def main():
    parser = build_parser()
    args = parser.parse_args()

    results = []
    for raw_path in args.paths:
        results.append(summarize_path(Path(raw_path)))

    if args.json:
        print(json.dumps({'items': results}, ensure_ascii=False, indent=2))
        return

    print('Media sanity check')
    for item in results:
        print(f"- {item['kind']}: {item['path']}")
        print(f"  size: {item['size_bytes']} bytes")
        if item.get('duration_seconds') is not None:
            print(f"  duration: {item['duration_seconds']:.3f}s")
        if item.get('video'):
            video = item['video']
            print(f"  video: {video.get('codec')} {video.get('width')}x{video.get('height')} fps={video.get('frame_rate')}")
        if item.get('audio'):
            audio = item['audio']
            if isinstance(audio, dict) and 'codec' in audio:
                print(f"  audio stream: {audio.get('codec')} sr={audio.get('sample_rate')} ch={audio.get('channels')}")
            elif isinstance(audio, dict):
                sample_rate = audio.get('sample_rate') or audio.get('sample_rate_(hz)')
                channels = audio.get('channels')
                print(f"  audio: sr={sample_rate} ch={channels}")
        if item.get('image'):
            image = item['image']
            print(f"  image: {image.get('format')} {image.get('width')}x{image.get('height')} {image.get('colorspace')}")


if __name__ == '__main__':
    try:
        main()
    except Exception as exc:
        print(f'fout: {exc}', file=sys.stderr)
        sys.exit(1)
