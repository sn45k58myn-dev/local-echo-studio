# Hardware evidence

Record the model, FCC ID and visible PCB marking separately. A component datasheet establishes what a chip can do. Board routing requires evidence from the relevant hardware revision.

## Revision identifiers

| Label or filing | Evidence | Scope |
| --- | --- | --- |
| `O2T2V3`, FCC `2ARGE-6383` | [2019 label exhibit](https://fccid.io/2ARGE-6383/Label/Label-4453139.pdf), [internal photos](https://fccid.io/2ARGE-6383/Internal-Photos/EUT-Photo-Internal-4453172) | Original revision |
| `O2T2V3`, FCC `2ARGE-7432` | [2022 internal-photo exhibit](https://fccid.io/2ARGE-7432/Internal-Photos/IntPho-6024402.pdf) | Refresh, with separate regulatory filing |
| `30-004702` | Visible silkscreen in the [EDN teardown photos](https://www.edn.com/disassembling-the-echo-studio-amazons-apple-homepod-foe/) | The photographed sample. Verify any other board before reusing its component inventory. |

## Audio, microphones and controls

| Observation | Evidence | Open question |
| --- | --- | --- |
| The original Studio has three directional midranges, a tweeter and a 5.25-inch bass driver. | [Amazon's launch information](https://www.aboutamazon.com/news/devices/amazon-devices-event-september-2019) | Driver loads, channel routing, amplifier headroom and safe crossover limits. |
| The teardown identifies a MediaTek MT8516, a Cirrus CS42526 multichannel codec and at least two TI TPA3129D2 amps. | [EDN teardown](https://www.edn.com/disassembling-the-echo-studio-amazons-apple-homepod-foe/), [Cirrus codec](https://www.cirrus.com/products/cs42526), [TI amp](https://www.ti.com/product/TPA3129D2) | Codec bus, channel ordering, clock tree, gain and mute behaviour. |
| The photographed top assembly contains seven mics, four buttons and LP5036 LED control hardware. | [EDN teardown](https://www.edn.com/disassembling-the-echo-studio-amazons-apple-homepod-foe/), [TI LP5036](https://www.ti.com/product/LP5036) | Microphone channel mapping, controls and wiring. Verify that mute actually stops capture. |
| The stock product uses spatial processing tuned for its cabinet. | [Amazon Science](https://www.amazon.science/blog/the-science-behind-amazons-spatial-audio-processing-technology) | Establish safe, intelligible playback before attempting any spatial processing. |

MediaTek's Linux matrix marks the MT8516 audio front end as work in progress. Linux has LP5036 chip support, and its related CS42xx8 I²C codec driver lists CS42448 and CS42888. The Studio's CS42526 still needs a board-specific driver assessment. [MediaTek support matrix](https://mtk.docs.kernel.org/matrix/tablet_chips.html) · [Linux LP50xx driver](https://github.com/torvalds/linux/blob/master/drivers/leds/leds-lp50xx.c) · [Linux codec bindings in source](https://github.com/torvalds/linux/blob/master/sound/soc/codecs/cs42xx8-i2c.c)

## First unit observed

The owner reported a green ring during earlier troubleshooting. Windows also briefly enumerated a MediaTek PreLoader USB interface and logged Device Manager Code 39 and Code Integrity event 3111 when loading the legacy driver. Those are separate observations. We did not establish that the green ring and USB enumeration corresponded to the same boot mode.

At our request, the owner restarted normally with USB unplugged and no buttons held. The ring went blue, then orange, and the stock setup prompt played. [Amazon light guide](https://digprjsurvey.amazon.com/csad/help/node/GKLDRFT7FP4FZE56)

In a later attempt, the owner reported a solid green ring and heard the Windows USB connection chime. Windows recorded the MediaTek PreLoader interface for approximately eight seconds and logged a driver-load failure at arrival. This records the LED and USB observations from the same attempt. The precise boot state and a supported firmware installation remain unverified. [Microsoft Code 39](https://learn.microsoft.com/en-us/windows-hardware/drivers/install/cm-prob-driver-failed-load) · [Microsoft event 3111](https://learn.microsoft.com/en-us/windows/security/application-security/application-control/app-control-for-business/operations/event-id-explanations)

The official safety and compliance sheet describes a mains-powered unit. Keep the enclosure closed for powered observation. [Amazon product specifications](https://digprjsurvey.amazon.com/csad/help/node/GGQPJXRU4PCM4XNA)
