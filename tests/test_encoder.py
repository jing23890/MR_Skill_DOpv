"""End-to-end encoder checks using tiny original standard-library fixtures.

Run: python -m unittest discover -s tests -v
Set FFMPEG to an executable path if it is not on PATH.
"""
from fractions import Fraction
import importlib.util
import os
from pathlib import Path
import shutil
import struct
import subprocess
import tempfile
import unittest
import wave
import zlib

SCRIPT = Path(__file__).resolve().parents[1] / 'skills/concept-pv-production/scripts/encode_sequence.py'
SPEC = importlib.util.spec_from_file_location('encoder', SCRIPT)
encoder = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(encoder)
FFMPEG = os.environ.get('FFMPEG') or shutil.which('ffmpeg')


def png(path, width=64, height=36, value=60):
    def chunk(kind, data):
        return struct.pack('>I', len(data)) + kind + data + struct.pack('>I', zlib.crc32(kind + data))
    raw = b''.join(b'\0' + bytes([value, 90, 130]) * width for _ in range(height))
    data = b'\x89PNG\r\n\x1a\n'
    data += chunk(b'IHDR', struct.pack('>IIBBBBB', width, height, 8, 2, 0, 0, 0))
    data += chunk(b'IDAT', zlib.compress(raw)) + chunk(b'IEND', b'')
    path.write_bytes(data)


@unittest.skipUnless(FFMPEG, 'FFmpeg required; set FFMPEG to its executable path')
class EncoderTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        self.frames = self.root / 'frames'
        self.frames.mkdir()
        for i in range(1, 9):
            png(self.frames / f'frame_{i:04d}.png', value=30 + i * 20)
        self.output = self.root / 'clip.mp4'

    def tearDown(self):
        self.temp.cleanup()

    def args(self, *extra):
        return encoder.parser().parse_args([
            '--ffmpeg', FFMPEG, '--frames-dir', str(self.frames), '--frames', '8',
            '--output', str(self.output), *extra])

    def test_fractional_rate_and_full_decode(self):
        result = encoder.encode(self.args('--fps', '24000/1001'))
        self.assertEqual(result['decoded_video_frames'], 8)
        self.assertEqual(result['source_dimensions'], [64, 36])
        self.assertEqual(result['configured_fps'], '24000/1001')
        self.assertAlmostEqual(result['expected_duration_seconds'], float(8 / Fraction(24000, 1001)))
        self.assertTrue(self.output.with_suffix('.validation.json').is_file())

    def test_short_audio_is_included(self):
        audio = self.root / 'short.wav'
        with wave.open(str(audio), 'wb') as w:
            w.setnchannels(1)
            w.setsampwidth(2)
            w.setframerate(48000)
            w.writeframes(b'\0\0' * 4800)
        result = encoder.encode(self.args('--audio', str(audio)))
        self.assertTrue(result['audio_requested'])
        self.assertEqual(result['decoded_video_frames'], 8)
        probe = subprocess.run([FFMPEG, '-v', 'error', '-i', str(self.output),
                                '-map', '0:a:0', '-f', 'null', '-'], capture_output=True)
        self.assertEqual(probe.returncode, 0, probe.stderr)

    def test_missing_frame_is_rejected(self):
        (self.frames / 'frame_0004.png').unlink()
        with self.assertRaises(FileNotFoundError):
            encoder.encode(self.args())
        self.assertFalse(self.output.exists())

    def test_different_dimensions_are_rejected(self):
        png(self.frames / 'frame_0004.png', width=66)
        with self.assertRaisesRegex(ValueError, 'dimensions differ'):
            encoder.encode(self.args())
        self.assertFalse(self.output.exists())

    def test_corrupt_payload_never_publishes_output(self):
        path = self.frames / 'frame_0004.png'
        path.write_bytes(path.read_bytes()[:24])
        with self.assertRaises(RuntimeError):
            encoder.encode(self.args())
        self.assertFalse(self.output.exists())
        self.assertEqual(list(self.root.glob('.*.partial.mp4')), [])

    def test_existing_output_is_preserved(self):
        self.output.write_bytes(b'previous deliverable')
        with self.assertRaisesRegex(ValueError, 'exists'):
            encoder.encode(self.args())
        self.assertEqual(self.output.read_bytes(), b'previous deliverable')

    def test_explicit_overwrite(self):
        self.output.write_bytes(b'previous deliverable')
        result = encoder.encode(self.args('--overwrite'))
        self.assertTrue(result['decode_success'])
        self.assertNotEqual(self.output.read_bytes(), b'previous deliverable')

    def test_pattern_cannot_escape_frame_directory(self):
        with self.assertRaisesRegex(ValueError, 'basename'):
            encoder.encode(self.args('--pattern', '../frame_%04d.png'))


if __name__ == '__main__':
    unittest.main()
