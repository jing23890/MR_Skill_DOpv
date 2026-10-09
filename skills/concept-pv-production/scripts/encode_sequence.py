#!/usr/bin/env python3
"""Encode a completed PNG sequence; validate decoding before publishing output.

Python 3.10+, FFmpeg with libx264. Standard library only.
"""
import argparse
from fractions import Fraction
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
import uuid


def positive_int(value):
    number = int(value)
    if number <= 0:
        raise argparse.ArgumentTypeError('Must be a positive integer')
    return number


def rate(value):
    try:
        result = Fraction(value)
        if result <= 0:
            raise ValueError()
        return result
    except (ValueError, ZeroDivisionError):
        raise argparse.ArgumentTypeError('Use a positive rate, e.g. 24 or 24000/1001')


def parser():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--frames-dir', type=Path, required=True)
    p.add_argument('--pattern', default='frame_%04d.png', help='One %%d or %%0Nd token; PNG files only')
    p.add_argument('--start-number', type=int, default=1)
    p.add_argument('--frames', type=positive_int, required=True)
    p.add_argument('--fps', type=rate, default=Fraction(24))
    p.add_argument('--audio', type=Path)
    p.add_argument('--output', type=Path, required=True)
    p.add_argument('--ffmpeg', default='ffmpeg')
    p.add_argument('--crf', type=int, choices=range(0, 52), default=18, metavar='0..51')
    p.add_argument('--overwrite', action='store_true')
    return p


def check_frames(args):
    # Restrict patterns to a single basename to keep expansion inside frames-dir.
    pat = args.pattern
    if '/' in pat or '\\' in pat or not re.fullmatch(r'[^%]*%(?:0[1-9][0-9]*)?d[^%]*\.png', pat):
        raise ValueError('Pattern must be a PNG basename with exactly one %d or %0Nd token')
    if args.start_number < 0:
        raise ValueError('start-number must be zero or greater')
    dimensions = None
    for number in range(args.start_number, args.start_number + args.frames):
        path = args.frames_dir / (pat % number)
        with path.open('rb') as handle:
            head = handle.read(24)
        if len(head) != 24 or head[:8] != b'\x89PNG\r\n\x1a\n' or head[12:16] != b'IHDR':
            raise ValueError(f'Invalid PNG header: {path.name}')
        size = (int.from_bytes(head[16:20], 'big'), int.from_bytes(head[20:24], 'big'))
        if not all(size) or any(v % 2 for v in size):
            raise ValueError(f'yuv420p requires positive even dimensions: {path.name} {size}')
        if dimensions is not None and dimensions != size:
            raise ValueError(f'Frame dimensions differ: {path.name} {size}, expected {dimensions}')
        dimensions = size
    return dimensions


def run(command):
    result = subprocess.run(command, capture_output=True, text=True, encoding='utf-8', errors='replace')
    if result.returncode:
        raise RuntimeError(result.stderr[-5000:] or f'FFmpeg exited {result.returncode}')
    return result


def encode(args):
    executable = shutil.which(args.ffmpeg)
    if not executable:
        raise ValueError('FFmpeg not found. Supply --ffmpeg /path/to/ffmpeg or add it to PATH.')
    args.frames_dir = args.frames_dir.resolve(strict=True)
    target = args.output.resolve()
    report = target.with_suffix('.validation.json')
    if target.suffix.lower() != '.mp4':
        raise ValueError('Output must use the .mp4 extension')
    if not args.overwrite and (target.exists() or report.exists()):
        raise ValueError('Output or validation report exists; choose another output or use --overwrite')
    audio = args.audio.resolve(strict=True) if args.audio else None
    if audio in (target, report):
        raise ValueError('Output cannot replace the audio input')
    dimensions = check_frames(args)
    target.parent.mkdir(parents=True, exist_ok=True)
    temp = target.with_name(f'.{target.stem}.{uuid.uuid4().hex}.partial.mp4')
    report_temp = report.with_name(f'.{report.name}.{uuid.uuid4().hex}.tmp')
    duration = args.frames / args.fps
    fps = f'{args.fps.numerator}/{args.fps.denominator}'
    command = [executable, '-hide_banner', '-loglevel', 'error', '-xerror', '-y',
               '-framerate', fps, '-start_number', str(args.start_number), '-start_number_range', '1',
               '-i', str(args.frames_dir / args.pattern)]
    if audio:
        command += ['-i', str(audio)]
    command += ['-map', '0:v:0']
    if audio:
        command += ['-map', '1:a:0', '-af', f'apad,atrim=duration={float(duration):.12f}',
                    '-c:a', 'aac', '-b:a', '192k', '-ar', '48000', '-ac', '2']
    else:
        command += ['-an']
    command += ['-frames:v', str(args.frames), '-c:v', 'libx264', '-preset', 'medium',
                '-crf', str(args.crf), '-pix_fmt', 'yuv420p', '-movflags', '+faststart', str(temp)]
    try:
        run(command)
        decoded = run([executable, '-hide_banner', '-loglevel', 'error', '-xerror', '-i', str(temp),
                       '-map', '0:v:0', '-map', '0:a?', '-progress', 'pipe:1', '-nostats', '-f', 'null', '-'])
        counts = re.findall(r'^frame=(\d+)\s*$', decoded.stdout, re.MULTILINE)
        if not counts or int(counts[-1]) != args.frames:
            raise RuntimeError(f'Decoded frame count differs: {counts[-1] if counts else "unavailable"}')
        if not args.overwrite and (target.exists() or report.exists()):
            raise ValueError('A destination appeared during encoding; refusing to replace it')
        result = {
            'output_name': target.name,
            'decoded_video_frames': int(counts[-1]),
            'source_dimensions': list(dimensions),
            'configured_fps': fps,
            'expected_duration_seconds': float(duration),
            'audio_requested': bool(audio),
            'decode_success': True,
            'bytes': temp.stat().st_size,
            'inspection_scope': 'Frame header checks and full decode; visual/audio artistic review still required',
        }
        report_temp.write_text(json.dumps(result, indent=2) + '\n', encoding='utf-8')
        os.replace(temp, target)
        os.replace(report_temp, report)
        return result
    finally:
        temp.unlink(missing_ok=True)
        report_temp.unlink(missing_ok=True)


def main(argv=None):
    args = parser().parse_args(argv)
    try:
        print(json.dumps(encode(args), indent=2))
        return 0
    except (OSError, ValueError, RuntimeError) as error:
        print(f'Error: {error}', file=sys.stderr)
        return 1


if __name__ == '__main__':
    raise SystemExit(main())
