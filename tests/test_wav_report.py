"""Exercise WAV inspection with generated samples only."""

import contextlib
import io
import json
import math
from pathlib import Path
import sys
import tempfile
import unittest
import wave

from tools.wav_report import main, wav_report


class WavReportTests(unittest.TestCase):
    def setUp(self):
        temp_dir = tempfile.TemporaryDirectory()
        self.addCleanup(temp_dir.cleanup)
        self.wav = Path(temp_dir.name) / "fixture.wav"

    def write_samples(self, samples, *, channels=1, width=2, rate=8000):
        if width == 1:
            data = bytes(sample + 128 for sample in samples)
        else:
            data = b"".join(
                sample.to_bytes(width, sys.byteorder, signed=True) for sample in samples
            )
        with wave.open(str(self.wav), "wb") as audio:
            audio.setparams((channels, width, rate, 0, "NONE", "not compressed"))
            audio.writeframes(data)

    def test_all_sample_widths_keep_channels_separate(self):
        for width in (1, 2, 3, 4):
            with self.subTest(width=width):
                scale = 1 << (8 * width - 1)
                half = scale // 2
                self.write_samples((-scale, half, scale - 1, -half), channels=2, width=width)
                report = wav_report(self.wav)
                self.assertEqual(report["sample_width_bits"], 8 * width)
                self.assertEqual(report["sample_rate_hz"], 8000)
                self.assertEqual(report["channels"], 2)
                self.assertEqual(report["frames"], 2)
                self.assertEqual(report["duration_seconds"], 2 / 8000)
                left, right = report["channel_metrics"]
                self.assertEqual(left["channel"], 1)
                self.assertEqual(left["peak_dbfs"], 0)
                left_rms = math.sqrt((scale**2 + (scale - 1)**2) / 2)
                self.assertAlmostEqual(left["rms_dbfs"], 20 * math.log10(left_rms / scale))
                self.assertEqual(left["full_scale_samples"], 2)
                self.assertEqual(right["channel"], 2)
                self.assertAlmostEqual(right["peak_dbfs"], 20 * math.log10(0.5))
                self.assertAlmostEqual(right["rms_dbfs"], 20 * math.log10(0.5))
                self.assertEqual(right["full_scale_samples"], 0)

    def test_silent_and_empty_recordings_have_json_null_levels(self):
        for samples in ((), (0, 0, 0)):
            with self.subTest(samples=samples):
                self.write_samples(samples, width=1)
                output = io.StringIO()
                with contextlib.redirect_stdout(output):
                    self.assertEqual(main([str(self.wav)]), 0)
                report = json.loads(output.getvalue())
                self.assertEqual(report["frames"], len(samples))
                self.assertIsNone(report["channel_metrics"][0]["peak_dbfs"])
                self.assertIsNone(report["channel_metrics"][0]["rms_dbfs"])
                self.assertEqual(report["channel_metrics"][0]["full_scale_samples"], 0)

    def test_frame_counts_and_metrics_across_read_blocks(self):
        self.write_samples((0, 0) * 4096 + (0, -32768), channels=2)
        report = wav_report(self.wav)
        self.assertEqual(report["frames"], 4097)
        self.assertIsNone(report["channel_metrics"][0]["peak_dbfs"])
        self.assertEqual(report["channel_metrics"][1]["full_scale_samples"], 1)

    def test_truncation_is_rejected(self):
        self.write_samples((0, 0, 0, 0), channels=2)
        complete = self.wav.read_bytes()
        for missing_bytes in (1, 4):
            with self.subTest(missing_bytes=missing_bytes):
                self.wav.write_bytes(complete[:-missing_bytes])
                with self.assertRaisesRegex(ValueError, "incomplete frame|declared frame count"):
                    wav_report(self.wav)

    def test_invalid_input_reports_an_error_and_no_json(self):
        self.wav.write_bytes(b"not a WAV")
        output = io.StringIO()
        error = io.StringIO()
        with contextlib.redirect_stdout(output), contextlib.redirect_stderr(error):
            with self.assertRaises(SystemExit) as exited:
                main([str(self.wav)])
        self.assertEqual(exited.exception.code, 2)
        self.assertEqual(output.getvalue(), "")
        self.assertIn("Could not read PCM WAV", error.getvalue())


if __name__ == "__main__":
    unittest.main()
