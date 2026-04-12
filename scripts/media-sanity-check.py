#!/usr/bin/env python3
import argparse
import fnmatch
import json
import mimetypes
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path


EXCLUDE_SETS = {
    'artifact-defaults': ['reports', 'helper-*'],
    'clip-helper-layout': ['reports', 'helper-*', 'frames', '*/frames'],
    'frame-export-layout': ['reports', 'helper-*', 'clips', '*/clips'],
}

INCLUDE_SETS = {
    'frame-png': ['frame-*.png'],
    'clips-video': ['*.mp4', '*.mov', '*.mkv', '*.webm'],
    'audio-wav': ['*.wav'],
}

DIR_ALIASES = {
    'creative-tooling-check': 'tmp/creative-tooling-check',
    'creative-reports': 'tmp/creative-tooling-check/reports',
    'creative-helper-frames': 'tmp/creative-tooling-check/helper-frames',
    'creative-helper-test': 'tmp/creative-tooling-check/helper-test',
    'creative-helper-test-frames': 'tmp/creative-tooling-check/helper-test/frames',
}

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
    'artifact-review': {
        'recursive': True,
        'summary_by_kind': True,
        'exclude_sets': ['artifact-defaults'],
    },
    'artifact-frames-review': {
        'recursive': True,
        'summary_by_kind': True,
        'exclude_sets': ['artifact-defaults'],
        'includes': ['frame-*.png'],
    },
    'clip-review': {
        'recursive': True,
        'summary_by_kind': True,
        'exclude_sets': ['clip-helper-layout'],
    },
    'frame-export-review': {
        'recursive': True,
        'summary_by_kind': True,
        'exclude_sets': ['frame-export-layout'],
        'kinds': ['image'],
    },
    'frame-png-review': {
        'recursive': True,
        'summary_by_kind': True,
        'exclude_sets': ['artifact-defaults'],
        'include_sets': ['frame-png'],
    },
    'clip-video-review': {
        'recursive': True,
        'summary_by_kind': True,
        'exclude_sets': ['clip-helper-layout'],
        'include_sets': ['clips-video'],
    },
    'creative-mixed-review': {
        'dir_alias': 'creative-tooling-check',
        'recursive': True,
        'summary_by_kind': True,
        'exclude_sets': ['artifact-defaults'],
    },
    'creative-audio-review': {
        'dir_alias': 'creative-tooling-check',
        'summary_by_kind': True,
        'exclude_sets': ['artifact-defaults'],
        'include_sets': ['audio-wav'],
        'kinds': ['audio'],
    },
    'creative-helper-frames-review': {
        'dir_alias': 'creative-helper-frames',
        'summary_by_kind': True,
        'include_sets': ['frame-png'],
        'kinds': ['image'],
    },
    'creative-helper-clips-review': {
        'dir_alias': 'creative-helper-test',
        'recursive': True,
        'summary_by_kind': True,
        'excludes': ['frames', '*/frames'],
        'include_sets': ['clips-video'],
        'kinds': ['video'],
    },
}

FAIL_PROFILES = {
    'video-strict': {
        'min_size_bytes': 1000,
        'min_duration': 0.5,
        'min_width': 320,
        'min_height': 240,
        'require_audio': True,
        'fail_on_warnings': True,
    },
    'audio-voice-16k-strict': {
        'min_size_bytes': 1000,
        'min_duration': 0.5,
        'expect_sample_rate': 16000,
        'fail_on_warnings': True,
    },
    'image-preview-strict': {
        'min_size_bytes': 100,
        'min_width': 160,
        'min_height': 120,
        'fail_on_warnings': True,
    },
    'mixed-batch-strict': {
        'fail_on_warnings': True,
        'max_warning_files': 0,
        'max_total_warnings': 0,
    },
    'mixed-batch-review': {
        'max_warning_files': 1,
        'max_total_warnings': 2,
    },
    'artifact-scan-review': {
        'recursive': True,
        'summary_by_kind': True,
        'exclude_sets': ['artifact-defaults'],
        'max_warning_files': 1,
        'max_total_warnings': 2,
    },
    'artifact-scan-strict': {
        'recursive': True,
        'summary_by_kind': True,
        'exclude_sets': ['artifact-defaults'],
        'fail_on_warnings': True,
        'max_warning_files': 0,
        'max_total_warnings': 0,
    },
    'artifact-frames-strict': {
        'recursive': True,
        'summary_by_kind': True,
        'exclude_sets': ['artifact-defaults'],
        'includes': ['frame-*.png'],
        'fail_on_warnings': True,
        'max_warning_files': 0,
        'max_total_warnings': 0,
    },
    'clip-review-strict': {
        'recursive': True,
        'summary_by_kind': True,
        'exclude_sets': ['clip-helper-layout'],
        'fail_on_warnings': True,
        'max_warning_files': 0,
        'max_total_warnings': 0,
    },
    'frame-export-strict': {
        'recursive': True,
        'summary_by_kind': True,
        'exclude_sets': ['frame-export-layout'],
        'kinds': ['image'],
        'fail_on_warnings': True,
        'max_warning_files': 0,
        'max_total_warnings': 0,
    },
    'frame-png-strict': {
        'recursive': True,
        'summary_by_kind': True,
        'exclude_sets': ['artifact-defaults'],
        'include_sets': ['frame-png'],
        'fail_on_warnings': True,
        'max_warning_files': 0,
        'max_total_warnings': 0,
    },
    'clip-video-strict': {
        'recursive': True,
        'summary_by_kind': True,
        'exclude_sets': ['clip-helper-layout'],
        'include_sets': ['clips-video'],
        'fail_on_warnings': True,
        'max_warning_files': 0,
        'max_total_warnings': 0,
    },
    'creative-mixed-strict': {
        'dir_alias': 'creative-tooling-check',
        'recursive': True,
        'summary_by_kind': True,
        'exclude_sets': ['artifact-defaults'],
        'fail_on_warnings': True,
        'max_warning_files': 0,
        'max_total_warnings': 0,
    },
    'creative-audio-strict': {
        'dir_alias': 'creative-tooling-check',
        'summary_by_kind': True,
        'exclude_sets': ['artifact-defaults'],
        'include_sets': ['audio-wav'],
        'kinds': ['audio'],
        'fail_on_warnings': True,
        'max_warning_files': 0,
        'max_total_warnings': 0,
    },
    'creative-helper-frames-strict': {
        'dir_alias': 'creative-helper-frames',
        'summary_by_kind': True,
        'include_sets': ['frame-png'],
        'kinds': ['image'],
        'fail_on_warnings': True,
        'max_warning_files': 0,
        'max_total_warnings': 0,
    },
    'creative-helper-clips-strict': {
        'dir_alias': 'creative-helper-test',
        'recursive': True,
        'summary_by_kind': True,
        'excludes': ['frames', '*/frames'],
        'include_sets': ['clips-video'],
        'kinds': ['video'],
        'fail_on_warnings': True,
        'max_warning_files': 0,
        'max_total_warnings': 0,
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
    parser.add_argument('--dir-alias', choices=sorted(DIR_ALIASES), help='Gebruik een herbruikbare map-alias voor terugkerende scanroutes')
    parser.add_argument('--recursive', action='store_true', help='Doorzoek submappen ook bij --dir')
    parser.add_argument('--kind', dest='kinds', choices=['audio', 'image', 'video'], nargs='+', help='Beperk de check tot alleen deze mediatypes')
    parser.add_argument('--exclude', dest='excludes', action='append', default=[], help='Sla paden/bestandsnamen over via glob-pattern, herhaalbaar')
    parser.add_argument('--exclude-set', dest='exclude_sets', choices=sorted(EXCLUDE_SETS), action='append', default=[], help='Gebruik een herbruikbare set exclude-patterns voor veelvoorkomende outputmappen, herhaalbaar')
    parser.add_argument('--include', dest='includes', action='append', default=[], help='Neem alleen paden/bestandsnamen mee die matchen met dit glob-pattern, herhaalbaar')
    parser.add_argument('--include-set', dest='include_sets', choices=sorted(INCLUDE_SETS), action='append', default=[], help='Gebruik een herbruikbare set include-patterns voor veelvoorkomende artifactgroepen, herhaalbaar')
    parser.add_argument('--name-contains', dest='name_contains', action='append', default=[], help='Neem alleen bestanden mee waarvan de bestandsnaam deze substring bevat, herhaalbaar')
    parser.add_argument('--name-not-contains', dest='name_not_contains', action='append', default=[], help='Sla bestanden over waarvan de bestandsnaam deze substring bevat, herhaalbaar')
    parser.add_argument('--json', action='store_true', help='Geef output als JSON')
    parser.add_argument('--jsonl', action='store_true', help='Geef output als één JSONL-event op stdout')
    parser.add_argument('--jsonl-summary-only', action='store_true', help='Laat bij JSONL-output alleen summary/meta zien, zonder volledige items')
    parser.add_argument('--report-out', help='Schrijf ook een rapportbestand weg')
    parser.add_argument('--report-format', choices=['auto', 'json', 'jsonl', 'text'], default='auto', help='Formaat voor --report-out (default: auto op basis van extensie of stdout-mode)')
    parser.add_argument('--report-summary-only', action='store_true', help='Schrijf in het rapport alleen samenvatting/meta weg, zonder volledige items')
    parser.add_argument('--report-timestamped', action='store_true', help='Voeg een UTC-timestamp toe aan de bestandsnaam van --report-out')
    parser.add_argument('--report-append', action='store_true', help='Append het rapport aan --report-out in plaats van overschrijven')
    parser.add_argument('--warnings-only', action='store_true', help='Toon alleen bestanden met warnings in de itemlijst')
    parser.add_argument('--summary-by-kind', action='store_true', help='Toon extra samenvatting per mediatype')
    parser.add_argument('--fail-on-warnings', action='store_true', help='Exit met code 2 als er warnings zijn, bruikbaar voor CI-achtige checks')
    parser.add_argument('--max-warning-files', type=int, help='Exit met code 2 als meer dan dit aantal bestanden warnings heeft')
    parser.add_argument('--max-total-warnings', type=int, help='Exit met code 2 als het totale aantal warning-meldingen boven deze grens komt')
    parser.add_argument('--preset', choices=sorted(PRESETS), help='Gebruik een standaard controleprofiel voor terugkerende checks')
    parser.add_argument('--fail-profile', choices=sorted(FAIL_PROFILES), help='Gebruik een streng fail-profiel per mediatype/use-case, inclusief fail-on-warnings')
    parser.add_argument('--min-size-bytes', type=int, help='Waarschuw als bestand kleiner is dan deze grootte in bytes')
    parser.add_argument('--min-duration', type=float, help='Waarschuw als duration korter is dan deze waarde in seconden')
    parser.add_argument('--min-width', type=int, help='Waarschuw als breedte lager is dan deze waarde')
    parser.add_argument('--min-height', type=int, help='Waarschuw als hoogte lager is dan deze waarde')
    parser.add_argument('--expect-sample-rate', type=int, help='Waarschuw als audio sample rate afwijkt van deze waarde')
    parser.add_argument('--require-audio', action='store_true', help='Waarschuw bij video zonder audio stream')
    return parser


def apply_profile_defaults(args, profile):
    for key, value in profile.items():
        current = getattr(args, key)
        if isinstance(value, bool):
            if current is False:
                setattr(args, key, value)
        elif isinstance(value, list):
            if not current:
                setattr(args, key, list(value))
        elif current is None:
            setattr(args, key, value)
    return args


def apply_preset_defaults(args):
    if args.preset:
        args = apply_profile_defaults(args, PRESETS[args.preset])
    if args.fail_profile:
        args = apply_profile_defaults(args, FAIL_PROFILES[args.fail_profile])
    return args


def resolve_directory(args, parser):
    if args.directory and args.dir_alias:
        parser.error('gebruik niet tegelijk --dir en --dir-alias')
    if args.dir_alias:
        return Path(DIR_ALIASES[args.dir_alias]).expanduser().resolve()
    if args.directory:
        return Path(args.directory).expanduser().resolve()
    return None


def expand_exclude_patterns(args):
    combined = list(args.excludes or [])
    for set_name in args.exclude_sets or []:
        for pattern in EXCLUDE_SETS[set_name]:
            if pattern not in combined:
                combined.append(pattern)
    return combined


def expand_include_patterns(args):
    combined = list(args.includes or [])
    for set_name in args.include_sets or []:
        for pattern in INCLUDE_SETS[set_name]:
            if pattern not in combined:
                combined.append(pattern)
    return combined


def path_matches_patterns(path: Path, patterns):
    if not patterns:
        return True
    path_str = str(path)
    name = path.name
    posix = path.as_posix()
    parts = path.parts
    for pattern in patterns:
        if fnmatch.fnmatch(name, pattern) or fnmatch.fnmatch(path_str, pattern) or fnmatch.fnmatch(posix, pattern):
            return True
        if any(fnmatch.fnmatch(part, pattern) for part in parts):
            return True
    return False


def is_excluded(path: Path, patterns):
    if not patterns:
        return False
    return path_matches_patterns(path, patterns)


def name_matches(path: Path, includes=None, excludes=None):
    name = path.name
    includes = includes or []
    excludes = excludes or []
    if includes and not any(fragment in name for fragment in includes):
        return False
    if excludes and any(fragment in name for fragment in excludes):
        return False
    return True



def collect_paths(args, parser):
    requested_kinds = set(args.kinds or [])
    exclude_patterns = expand_exclude_patterns(args)
    include_patterns = expand_include_patterns(args)
    directory = resolve_directory(args, parser)
    collected = []

    for raw_path in args.paths:
        path = Path(raw_path)
        if include_patterns and not path_matches_patterns(path, include_patterns):
            continue
        if is_excluded(path, exclude_patterns):
            continue
        if not name_matches(path, includes=args.name_contains, excludes=args.name_not_contains):
            continue
        kind = detect_kind(path)
        if requested_kinds and kind not in requested_kinds:
            continue
        collected.append(path)

    if directory:
        if not directory.is_dir():
            parser.error(f'geen map: {directory}')
        iterator = directory.rglob('*') if args.recursive else directory.iterdir()
        for path in sorted(iterator):
            if include_patterns and not path_matches_patterns(path, include_patterns):
                continue
            if is_excluded(path, exclude_patterns):
                continue
            if not name_matches(path, includes=args.name_contains, excludes=args.name_not_contains):
                continue
            kind = detect_kind(path)
            if path.is_file() and kind != 'unknown':
                if requested_kinds and kind not in requested_kinds:
                    continue
                collected.append(path)
    if not collected:
        if include_patterns:
            parser.error('geen mediabestanden gevonden na include-filters')
        if args.name_contains or args.name_not_contains:
            parser.error('geen mediabestanden gevonden na naamfilters')
        if requested_kinds:
            parser.error(f'geen mediabestanden gevonden voor kind-filter: {", ".join(sorted(requested_kinds))}')
        if exclude_patterns:
            parser.error('geen mediabestanden gevonden na exclude-filters')
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


def build_fail_reasons(summary, args):
    fail_reasons = []
    if args.fail_on_warnings and summary['warning_count'] > 0:
        fail_reasons.append('warning_count > 0')
    if args.max_warning_files is not None and summary['warning_count'] > args.max_warning_files:
        fail_reasons.append(f"warning_count {summary['warning_count']} > max_warning_files {args.max_warning_files}")
    if args.max_total_warnings is not None and summary['total_warnings'] > args.max_total_warnings:
        fail_reasons.append(f"total_warnings {summary['total_warnings']} > max_total_warnings {args.max_total_warnings}")
    return fail_reasons


def build_payload(args, summary, displayed_results, fail_reasons, exit_code, kind_summary=None, summary_only=False):
    payload = {
        'generated_at': datetime.now(timezone.utc).isoformat(),
        'preset': args.preset,
        'fail_profile': args.fail_profile,
        'directory': str(resolve_directory(args, build_parser())) if (args.directory or args.dir_alias) else None,
        'dir_alias': args.dir_alias,
        'kinds': sorted(args.kinds) if args.kinds else None,
        'excludes': expand_exclude_patterns(args) or None,
        'exclude_sets': args.exclude_sets or None,
        'includes': expand_include_patterns(args) or None,
        'include_sets': args.include_sets or None,
        'name_contains': args.name_contains or None,
        'name_not_contains': args.name_not_contains or None,
        'warnings_only': args.warnings_only,
        'report_append': args.report_append,
        'summary_only': summary_only,
        'fail_on_warnings': args.fail_on_warnings,
        'max_warning_files': args.max_warning_files,
        'max_total_warnings': args.max_total_warnings,
        'summary': summary,
        'items': displayed_results,
        'fail_reasons': fail_reasons,
        'exit_code': exit_code,
    }
    if kind_summary is not None:
        payload['summary_by_kind'] = kind_summary
    return payload



def render_text_report(args, summary, displayed_results, fail_reasons, kind_summary=None):
    lines = ['Media sanity check']
    if args.preset:
        lines.append(f'preset: {args.preset}')
    if args.fail_profile:
        lines.append(f'fail-profile: {args.fail_profile}')
    directory = resolve_directory(args, build_parser())
    if args.dir_alias:
        lines.append(f'dir-alias: {args.dir_alias}')
    if directory:
        lines.append(f'directory: {directory}')
    if args.kinds:
        lines.append(f"kinds: {', '.join(sorted(args.kinds))}")
    if args.exclude_sets:
        lines.append(f"exclude-sets: {', '.join(args.exclude_sets)}")
    if args.include_sets:
        lines.append(f"include-sets: {', '.join(args.include_sets)}")
    expanded_excludes = expand_exclude_patterns(args)
    if expanded_excludes:
        lines.append(f"excludes: {', '.join(expanded_excludes)}")
    expanded_includes = expand_include_patterns(args)
    if expanded_includes:
        lines.append(f"includes: {', '.join(expanded_includes)}")
    if args.name_contains:
        lines.append(f"name-contains: {', '.join(args.name_contains)}")
    if args.name_not_contains:
        lines.append(f"name-not-contains: {', '.join(args.name_not_contains)}")
    if args.warnings_only:
        lines.append('mode: warnings-only')
    if args.report_append:
        lines.append('mode: report-append')
    if args.fail_on_warnings:
        lines.append('mode: fail-on-warnings')
    if args.max_warning_files is not None:
        lines.append(f'mode: max-warning-files={args.max_warning_files}')
    if args.max_total_warnings is not None:
        lines.append(f'mode: max-total-warnings={args.max_total_warnings}')
    lines.append(f"summary: total={summary['total']} ok={summary['ok_count']} warnings={summary['warning_count']} total-warning-messages={summary['total_warnings']}")
    if kind_summary is not None:
        lines.append('summary-by-kind:')
        for kind, bucket in kind_summary.items():
            lines.append(f"  - {kind}: total={bucket['total']} ok={bucket['ok_count']} warnings={bucket['warning_count']}")
    for item in displayed_results:
        lines.append(f"- {item['kind']}: {item['path']}")
        lines.append(f"  size: {item['size_bytes']} bytes")
        if item.get('duration_seconds') is not None:
            lines.append(f"  duration: {item['duration_seconds']:.3f}s")
        if item.get('video'):
            video = item['video']
            lines.append(f"  video: {video.get('codec')} {video.get('width')}x{video.get('height')} fps={video.get('frame_rate')}")
        if item.get('audio'):
            audio = item['audio']
            if isinstance(audio, dict) and 'codec' in audio:
                lines.append(f"  audio stream: {audio.get('codec')} sr={audio.get('sample_rate')} ch={audio.get('channels')}")
            elif isinstance(audio, dict):
                sample_rate = audio.get('sample_rate') or audio.get('sample_rate_(hz)')
                channels = audio.get('channels')
                lines.append(f"  audio: sr={sample_rate} ch={channels}")
        if item.get('image'):
            image = item['image']
            lines.append(f"  image: {image.get('format')} {image.get('width')}x{image.get('height')} {image.get('colorspace')}")
        if item.get('warnings'):
            lines.append(f"  warnings: {'; '.join(item['warnings'])}")
    if fail_reasons:
        lines.append(f"fail-reasons: {'; '.join(fail_reasons)}")
    return '\n'.join(lines)



def detect_report_format(args):
    if args.report_format != 'auto':
        return args.report_format
    if args.report_out:
        suffix = Path(args.report_out).suffix.lower()
        if suffix == '.json':
            return 'json'
        if suffix == '.jsonl':
            return 'jsonl'
        if suffix in {'.txt', '.log', '.report'}:
            return 'text'
    return 'json' if args.json else 'text'



def build_report_path(path_value, timestamped=False):
    path = Path(path_value).expanduser().resolve()
    if not timestamped:
        return path
    stamp = datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')
    return path.with_name(f"{path.stem}-{stamp}{path.suffix}")



def write_report(path_value, content, timestamped=False, append=False):
    path = build_report_path(path_value, timestamped=timestamped)
    path.parent.mkdir(parents=True, exist_ok=True)
    existing_size = path.stat().st_size if path.exists() else 0
    if append:
        with path.open('a', encoding='utf-8') as handle:
            if existing_size > 0 and not content.endswith('\n'):
                handle.write('\n\n')
            handle.write(content)
    else:
        path.write_text(content, encoding='utf-8')
    return str(path)



def main():
    parser = build_parser()
    args = apply_preset_defaults(parser.parse_args())
    if args.json and args.jsonl:
        parser.error('gebruik niet tegelijk --json en --jsonl')
    targets = collect_paths(args, parser)

    results = []
    for raw_path in targets:
        item = summarize_path(Path(raw_path))
        results.append(apply_thresholds(item, args))

    summary = {
        'total': len(results),
        'ok_count': sum(1 for item in results if item.get('ok')),
        'warning_count': sum(1 for item in results if item.get('warnings')),
        'total_warnings': sum(len(item.get('warnings') or []) for item in results),
    }
    kind_summary = build_kind_summary(results) if args.summary_by_kind else None
    displayed_results = [item for item in results if item.get('warnings')] if args.warnings_only else results

    fail_reasons = build_fail_reasons(summary, args)
    exit_code = 2 if fail_reasons else 0
    stdout_summary_only = args.jsonl and args.jsonl_summary_only
    stdout_items = [] if stdout_summary_only else displayed_results
    payload = build_payload(
        args,
        summary,
        stdout_items,
        fail_reasons,
        exit_code,
        kind_summary=kind_summary,
        summary_only=stdout_summary_only,
    )
    text_report = render_text_report(args, summary, displayed_results, fail_reasons, kind_summary=kind_summary)

    report_path = None
    if args.report_out:
        report_format = detect_report_format(args)
        report_summary_only = args.report_summary_only or (report_format == 'jsonl' and args.jsonl_summary_only)
        report_payload = build_payload(
            args,
            summary,
            [] if report_summary_only else displayed_results,
            fail_reasons,
            exit_code,
            kind_summary=kind_summary,
            summary_only=report_summary_only,
        )
        if report_format == 'json':
            report_content = json.dumps(report_payload, ensure_ascii=False, indent=2)
        elif report_format == 'jsonl':
            report_content = json.dumps(report_payload, ensure_ascii=False) + '\n'
        else:
            report_content = render_text_report(
                args,
                summary,
                [] if args.report_summary_only else displayed_results,
                fail_reasons,
                kind_summary=kind_summary,
            )
        report_path = write_report(args.report_out, report_content, timestamped=args.report_timestamped, append=args.report_append)
        payload['report_out'] = report_path

    if args.json:
        print(json.dumps(payload, ensure_ascii=False, indent=2))
        raise SystemExit(exit_code)

    if args.jsonl:
        print(json.dumps(payload, ensure_ascii=False))
        raise SystemExit(exit_code)

    if report_path:
        text_report = f"{text_report}\nreport-out: {report_path}"

    print(text_report)
    raise SystemExit(exit_code)


if __name__ == '__main__':
    try:
        main()
    except Exception as exc:
        print(f'fout: {exc}', file=sys.stderr)
        sys.exit(1)
