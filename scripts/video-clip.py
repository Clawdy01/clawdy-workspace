#!/usr/bin/env python3
import argparse
import json
import subprocess
import sys
from pathlib import Path


def run(cmd):
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        raise RuntimeError(result.stderr.strip() or 'command failed')
    return result


def ffprobe_duration(path: Path):
    result = run([
        'ffprobe',
        '-v', 'error',
        '-show_entries', 'format=duration',
        '-of', 'json',
        str(path),
    ])
    data = json.loads(result.stdout or '{}')
    duration = (data.get('format') or {}).get('duration')
    return float(duration) if duration is not None else None


def build_parser():
    parser = argparse.ArgumentParser(description='Maak een korte clip en/of exporteer frames uit een video.')
    parser.add_argument('input', help='Pad naar inputvideo')
    parser.add_argument('--start', default='0', help='Starttijd voor clip/frame-export, bv. 0, 1.5 of 00:00:01.500')
    parser.add_argument('--duration', default='1', help='Duur van clipsegment in seconden of ffmpeg-tijdformaat')
    parser.add_argument('--clip-out', help='Pad voor outputclip, bv. out/clip.mp4')
    parser.add_argument('--frames-dir', help='Map voor geëxporteerde frames')
    parser.add_argument('--fps', type=float, default=1.0, help='Frames per seconde voor export, standaard 1')
    parser.add_argument('--frame-format', default='png', choices=['png', 'jpg', 'jpeg'], help='Formaat voor frames')
    parser.add_argument('--prefix', default='frame', help='Bestands-prefix voor frames')
    parser.add_argument('--json', action='store_true', help='Geef samenvatting als JSON')
    return parser


def main():
    parser = build_parser()
    args = parser.parse_args()

    input_path = Path(args.input).expanduser().resolve()
    if not input_path.exists():
        parser.error(f'input bestaat niet: {input_path}')
    if not args.clip_out and not args.frames_dir:
        parser.error('geef minstens --clip-out of --frames-dir op')

    summary = {
        'input': str(input_path),
        'start': args.start,
        'duration': args.duration,
        'clip_out': None,
        'frames_dir': None,
        'frames': [],
    }

    if args.clip_out:
        clip_path = Path(args.clip_out).expanduser().resolve()
        clip_path.parent.mkdir(parents=True, exist_ok=True)
        run([
            'ffmpeg', '-y',
            '-ss', str(args.start),
            '-i', str(input_path),
            '-t', str(args.duration),
            '-c:v', 'libx264',
            '-an',
            str(clip_path),
        ])
        summary['clip_out'] = str(clip_path)
        summary['clip_duration_seconds'] = ffprobe_duration(clip_path)

    if args.frames_dir:
        frames_dir = Path(args.frames_dir).expanduser().resolve()
        frames_dir.mkdir(parents=True, exist_ok=True)
        pattern = frames_dir / f"{args.prefix}-%02d.{args.frame_format}"
        run([
            'ffmpeg', '-y',
            '-ss', str(args.start),
            '-i', str(input_path),
            '-t', str(args.duration),
            '-vf', f'fps={args.fps}',
            str(pattern),
        ])
        frames = sorted(str(path) for path in frames_dir.glob(f'{args.prefix}-*.{args.frame_format}'))
        summary['frames_dir'] = str(frames_dir)
        summary['frames'] = frames
        summary['frame_count'] = len(frames)

    if args.json:
        print(json.dumps(summary, ensure_ascii=False, indent=2))
    else:
        print('Video clip helper')
        print(f"- input: {summary['input']}")
        if summary['clip_out']:
            print(f"- clip: {summary['clip_out']}")
            print(f"- clip duration: {summary.get('clip_duration_seconds')}")
        if summary['frames_dir']:
            print(f"- frames dir: {summary['frames_dir']}")
            print(f"- frames: {summary.get('frame_count', 0)}")
            if summary['frames']:
                print(f"- eerste frame: {summary['frames'][0]}")


if __name__ == '__main__':
    try:
        main()
    except RuntimeError as exc:
        print(f'fout: {exc}', file=sys.stderr)
        sys.exit(1)
