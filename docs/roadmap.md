# Roadmap and acceptance checks

| Milestone | Evidence required |
| --- | --- |
| Confirm each hardware variant | Redacted FCC ID and PCB markings from independent samples, with source links. Identify whether the same documented components are present on each board. |
| Confirm a supported firmware path | A documented, authorized way to boot an owner-built image and return to working stock or supported recovery on the same revision. Record the models and versions actually tested. |
| Bring up stock playback and capture | Verify safe muted startup, known output channel mapping at low level, stable capture and actual hardware mute. Tune crossovers and limits before testing the drivers at normal listening volume. |
| Bring up the physical controls | Verify mute, volume, action and the light ring. The mute indication must correspond to actual capture state across reboots. |
| Verify local voice and music | With WAN disconnected and the local server reachable, test a wake word, a Home Assistant command, a spoken reply and playback of a local file through Music Assistant. Test pickup with music playing and record the conditions. |
| Package a release | Publish revision-specific support and recovery documentation, repeatable build instructions and checksums only after passing the device tests. |

Work that can start on a host now includes PCM regression tests, audio latency measurement on supported reference hardware, and preparing an Assist playback/capture test protocol. Label results by hardware. Use [Home Assistant's local Assist guide](https://www.home-assistant.io/voice_control/voice_remote_local_assistant/) as the reference for local speech services.
