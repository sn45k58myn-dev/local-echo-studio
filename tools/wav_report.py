"""Report per-channel levels for an uncompressed integer PCM WAV file."""

import argparse
import json
import math
from pathlib import Path
import struct
import sys
import wave


def dbfs(amplitude: float, full_scale: int) -> float | None:
    """Use None for silence so the result is valid JSON."""
    if amplitude == 0:
        return None
    return 20 * math.log10(amplitude / full_scale)


def wav_report(path: str | Path) -> dict:
    """Read PCM in blocks and report levels relative to the sample container."""
    with wave.open(str(path), "rb") as audio:
        channels = audio.getnchannels()
        sample_width = audio.getsampwidth()
        sample_rate = audio.getframerate()
        if audio.getcomptype() != "NONE" or sample_width not in (1, 2, 3, 4):
            raise ValueError("expected uncompressed 8-, 16-, 24- or 32-bit integer PCM")
        if channels < 1 or sample_rate < 1:
            raise ValueError("expected a positive channel count and sample rate")

        sample_bits = sample_width * 8
        full_scale = 1 << (sample_bits - 1)
        frame_width = channels * sample_width
        peaks = [0] * channels
        squared_sums = [0] * channels
        full_scale_counts = [0] * channels
        frame_count = 0

        while block := audio.readframes(4096):
            if len(block) % frame_width:
                raise ValueError("audio data ends with an incomplete frame")
            frame_count += len(block) // frame_width
            for index, offset in enumerate(range(0, len(block), sample_width)):
                channel = index % channels
                if sample_width == 1:
                    sample = block[offset] - full_scale
                else:
                    sample = int.from_bytes(
                        block[offset : offset + sample_width], sys.byteorder, signed=True
                    )
                peaks[channel] = max(peaks[channel], abs(sample))
                squared_sums[channel] += sample * sample
                if sample in (-full_scale, full_scale - 1):
                    full_scale_counts[channel] += 1

        if frame_count != audio.getnframes():
            raise ValueError("audio data is shorter than the declared frame count")

    return {
        "sample_rate_hz": sample_rate,
        "sample_width_bits": sample_bits,
        "channels": channels,
        "frames": frame_count,
        "duration_seconds": frame_count / sample_rate,
        "channel_metrics": [
            {
                "channel": channel + 1,
                "peak_dbfs": dbfs(peaks[channel], full_scale),
                "rms_dbfs": dbfs(
                    math.sqrt(squared_sums[channel] / frame_count) if frame_count else 0,
                    full_scale,
                ),
                "full_scale_samples": full_scale_counts[channel],
            }
            for channel in range(channels)
        ],
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("wav", type=Path, help="path to an uncompressed PCM WAV file")
    args = parser.parse_args(argv)
    try:
        report = wav_report(args.wav)
    except (EOFError, OSError, ValueError, struct.error, wave.Error) as error:
        parser.exit(2, f"Could not read PCM WAV: {str(error) or 'incomplete WAV header'}\n")
    print(json.dumps(report, indent=2, allow_nan=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
