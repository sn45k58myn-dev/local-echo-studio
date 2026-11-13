# Local Echo Studio

A community project to turn the original Echo Studio into a local Home Assistant voice and music endpoint. The target is the stock `O2T2V3` mainboard, microphone array, buttons, light ring and speakers. Home Assistant Assist and a local Music Assistant server are the intended integrations.

**Status: hardware research and host tooling.** This project has no Studio firmware image or verified, supported way to boot replacement firmware on the original board. LibreEcho lists both `octave` revisions as candidates. This is an independent project, with no affiliation with Amazon or LibreEcho. [LibreEcho hardware roadmap](https://libreecho.org/#hardware-roadmap)

| Area | Evidence today |
| --- | --- |
| Models | Original and refreshed Studio share the O2T2V3 model label. Use FCC ID and board markings when comparing samples. |
| Boot | One original Studio reached stock setup mode. Windows briefly detected a MediaTek USB device and failed to load the legacy USB driver. This yielded no firmware or verified boot path. |
| Hardware | Public teardown evidence identifies several audio and LED components. Board-level routing and the mic-mute implementation still need verification. |
| Audio tools | The host WAV analyser measures levels and saturation in local PCM files. Its tests use generated audio. |
| Home Assistant and music | Acceptance criteria are documented. Playback, voice and controls on the Studio remain untested. |

## Start here

- Read the [hardware evidence](docs/hardware.md) and [roadmap and acceptance checks](docs/roadmap.md).
- Try the WAV analyser with any uncompressed PCM WAV on your own computer. Python 3.11 or later, no external packages.

```console
python tools/wav_report.py capture.wav
python -m unittest discover -s tests -v
```

The analyser reads 8-, 16-, 24- and 32-bit integer PCM sample containers. It prints JSON with the sample format, duration, and per-channel peak and RMS in dBFS and full-scale sample counts. Channels are numbered from one, and amplitudes are normalized by 2 to the power of (container bits minus one). A silent channel reports `null` in dBFS. Full-scale samples can indicate saturation. These measurements alone cannot establish the physical signal path or echo-cancellation quality. PCM WAVE_FORMAT_EXTENSIBLE requires Python 3.12 or later.

## Contribute

Start with [contributor guidance](CONTRIBUTING.md). Helpful first reports include a cross-check of board markings, repeatable observations from normal boot, documented component behaviour, and synthetic audio tests. The [hardware report form](.github/ISSUE_TEMPLATE/hardware-observation.md) records model, evidence and the limits of each observation.

New project code and original documentation use the [MIT License](LICENSE). Linked third-party material remains under its own terms.
