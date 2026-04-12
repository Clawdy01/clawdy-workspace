#!/usr/bin/env python3
import argparse
import json
import mimetypes
import subprocess
import sys
from pathlib import Path


PRESETS = {
    'video-proof': {
        'min_size_bytes': 1000,
        'min_duration': 0.5,
        'min_width': 320,
        'min_height': 240,
    },
    'audio-voice-16k': {
        'min_size_bytes': 1000,
        'min_duration': 0.5,
        'expect_sample_rate': 16000,
    },
    'image-preview': {
        'min_size_bytes': 100,
        'min_width': 160,
        'min_height': 120,
    },
}


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
        'warnings': [],
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


def apply_thresholds(item, args):
    warnings = item.setdefault('warnings', [])
    if item.get('size_bytes', 0) <= 0:
        warnings.append('leeg bestand')
    elif args.min_size_bytes is not None and item['size_bytes'] < args.min_size_bytes:
        warnings.append(f"size {item['size_bytes']} bytes < min {args.min_size_bytes}")

    duration = item.get('duration_seconds')
    if duration is not None and duration <= 0:
        warnings.append('duration is 0s of ontbreekt effectief')
    if args.min_duration is not None and duration is not None and duration < args.min_duration:
        warnings.append(f'duration {duration:.3f}s < min {args.min_duration:.3f}s')

    dimensions = item.get('video') or item.get('image') or {}
    width = dimensions.get('width')
    height = dimensions.get('height')
    if width is not None and int(width) <= 0:
        warnings.append(f'ongeldige width {width}')
    if height is not None and int(height) <= 0:
        warnings.append(f'ongeldige height {height}')
    if args.min_width is not None and width is not None and int(width) < args.min_width:
        warnings.append(f'width {width} < min {args.min_width}')
    if args.min_height is not None and height is not None and int(height) < args.min_height:
        warnings.append(f'height {height} < min {args.min_height}')

    audio = item.get('audio') or {}
    sample_rate = None
    if isinstance(audio, dict):
        sample_rate = audio.get('sample_rate') or audio.get('sample_rate_(hz)')
    if args.expect_sample_rate is not None and sample_rate is not None and int(sample_rate) != args.expect_sample_rate:
        warnings.append(f'sample_rate {sample_rate} != expected {args.expect_sample_rate}')

    if item.get('kind') == 'video':
        if not item.get('video'):
            warnings.append('geen video stream gevonden')
        if args.require_audio and not item.get('audio'):
            warnings.append('audio stream ontbreekt')
    elif item.get('kind') == 'audio':
        if not audio:
            warnings.append('geen audio metadata gevonden')
    elif item.get('kind') == 'image':
        if not item.get('image'):
            warnings.append('geen image metadata gevonden')

    item['ok'] = len(warnings) == 0
    return item


def build_parser():
    parser = argparse.ArgumentParser(description='Snelle sanity-check voor video-, audio- en image-output.')
    parser.add_argument('paths', nargs='*', help='Een of meer mediabestanden om te inspecteren')
    parser.add_argument('--dir', dest='directory', help='Inspecteer alle ondersteunde mediabestanden in deze map')
    parser.add_argument('--recursive', action='store_true', help='Doorzoek submappen ook bij --dir')
    parser.add_argument('--json', action='store_true', help='Geef output als JSON')
    parser.add_argument('--warnings-only', action='store_true', help='Toon alleen bestanden met warnings in de itemlijst')
    parser.add_argument('--summary-by-kind', action='store_true', help='Toon extra samenvatting per mediatype')
    parser.add_argument('--preset', choices=sorted(PRESETS), help='Gebruik een standaard controleprofiel voor terugkerende checks')
    parser.add_argument('--min-size-bytes', type=int, help='Waarschuw als bestand kleiner is dan deze grootte in bytes')
    parser.add_argument('--min-duration', type=float, help='Waarschuw als duration korter is dan deze waarde in seconden')
    parser.add_argument('--min-width', type=int, help='Waarschuw als breedte lager is dan deze waarde')
    parser.add_argument('--min-height', type=int, help='Waarschuw als hoogte lager is dan deze waarde')
    parser.add_argument('--expect-sample-rate', type=int, help='Waarschuw als audio sample rate afwijkt van deze waarde')
    parser.add_argument('--require-audio', action='store_true', help='Waarschuw bij video zonder audio stream')
    return parser


def apply_preset_defaults(args):
    if not args.preset:
        return args
    for key, value in PRESETS[args.preset].items():
        if getattr(args, key) is None:
            setattr(args, key, value)
    return args


def collect_paths(args, parser):
    collected = [Path(p) for p in args.paths]
    if args.directory:
        directory = Path(args.directory).expanduser().resolve()
        if not directory.is_dir():
            parser.error(f'geen map: {directory}')
        iterator = directory.rglob('*') if args.recursive else directory.iterdir()
        for path in sorted(iterator):
            if path.is_file() and detect_kind(path) != 'unknown':
                collected.append(path)
    if not collected:
        parser.error('geef minstens één pad of gebruik --dir')
    return collected


def build_kind_summary(results):
    by_kind = {}
    for item in results:
        kind = item.get('kind') or 'unknown'
        bucket = by_kind.setdefault(kind, {
            'total': 0,
            'ok_count': 0,
            'warning_count': 0,
        })
        bucket['total'] += 1
        if item.get('ok'):
            bucket['ok_count'] += 1
        if item.get('warnings'):
            bucket['warning_count'] += 1
    return dict(sorted(by_kind.items()))


def main():
    parser = build_parser()
    args = apply_preset_defaults(parser.parse_args())
    targets = collect_paths(args, parser)

    results = []
    for raw_path in targets:
        item = summarize_path(Path(raw_path))
        results.append(apply_thresholds(item, args))

    summary = {
        'total': len(results),
        'ok_count': sum(1 for item in results if item.get('ok')),
        'warning_count': sum(1 for item in results if item.get('warnings')),
    }
    kind_summary = build_kind_summary(results) if args.summary_by_kind else None
    displayed_results = [item for item in results if item.get('warnings')] if args.warnings_only else results

    if args.json:
        payload = {
            'preset': args.preset,
            'directory': args.directory,
            'warnings_only': args.warnings_only,
            'summary': summary,
            'items': displayed_results,
        }
        if kind_summary is not None:
            payload['summary_by_kind'] = kind_summary
        print(json.dumps(payload, ensure_ascii=False, indent=2))
        return

    print('Media sanity check')
    if args.preset:
        print(f'preset: {args.preset}')
    if args.directory:
        print(f'directory: {Path(args.directory).expanduser().resolve()}')
    if args.warnings_only:
        print('mode: warnings-only')
    print(f"summary: total={summary['total']} ok={summary['ok_count']} warnings={summary['warning_count']}")
    if kind_summary is not None:
        print('summary-by-kind:')
        for kind, bucket in kind_summary.items():
            print(f"  - {kind}: total={bucket['total']} ok={bucket['ok_count']} warnings={bucket['warning_count']}")
    for item in displayed_results:
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
        if item.get('warnings'):
            print(f"  warnings: {'; '.join(item['warnings'])}")


if __name__ == '__main__':
    try:
        main()
    except Exception as exc:
        print(f'fout: {exc}', file=sys.stderr)
        sys.exit(1)
