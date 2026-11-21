+++
summary = "A quick guide to connecting Winlink Express and VARA HF to a FlexRadio FLEX-8400 with SmartSDR, DAX and CAT. **Read more →**"
title = "Winlink on FlexRadio"
url = "/en/emcomm/quick-guides/winlink-flexradio/"
description = "A quick guide to connecting Winlink Express and VARA HF to a FlexRadio FLEX-8400 with SmartSDR, DAX and CAT."
weight = 10
showDate = false
showAuthor = false
showReadingTime = false
showPagination = false
showDateUpdated = false
showHero = false
+++

This is how I run Winlink from home in Borlänge, with a FlexRadio FLEX-8400 and the callsign SM4T. The same setup works for VarAC. No extra hardware is needed – neither a sound card nor a CAT cable. Everything goes over the network.

## What you need

On the same Windows PC, connected to the same network as the radio:

- [SmartSDR for Windows](https://www.flexradio.com/software/) – the installer also includes DAX (audio) and SmartSDR CAT (radio control)
- [Winlink Express](https://winlink.org/WinlinkExpress)
- [VARA HF](https://rosmodem.wordpress.com/)

The radio and the computer only need to be on the same network. I use a FLEX-8400, but the steps are the same on other FLEX-6000 and FLEX-8000 models.

## 1. Slice, mode and filter in SmartSDR

Create a slice for Winlink and set the mode to **DIGU**, not ordinary USB. In DIGU, the processor and equalizer are kept out of the way; otherwise they can distort the digital signal.

VARA HF uses 2.3 kHz or 500 Hz, so the slice filter needs to be wide enough. FlexRadio recommends about 3.5 kHz for Winlink and VARA; I set it to roughly 3–3.5 kHz. The filter width is adjusted on the Radio Control panel. Under Settings → Radio Setup → Filters you can also adapt the digital filters.

On the P/CW tab under Radio Controls, **DAX** needs to be enabled so that transmit audio comes from DAX and not from the microphone.

## 2. DAX

Open the DAX panel and make sure it is associated with the same station or client that is controlling the radio.

- In the slice, under the DAX menu, choose channel 1 (or another free channel – then use the same number everywhere).
- In the DAX panel, the RX stream for that channel should be active. In current SmartSDR (DAXv2 in v4), the indicator turns blue when the channel is assigned to the slice, and green when a program is actually reading the audio.
- Transmit audio goes through the shared **DAX TX** stream. It turns blue when the DAX button on the P/CW tab is on, and green when the program is transmitting.

In VARA HF, under Settings → SoundCard, select:

- **Input:** `DAX RX 1` (in older SmartSDR this may be called `DAX Audio RX 1`; in DAXv2 often `DAX RX 1 (FlexRadio DAX)`)
- **Output:** `DAX TX` (older name: `DAX Audio TX`; in DAXv2 often `DAX TX (FlexRadio DAX)`)

The devices do not appear in the list until the DAX program is running. They are not always listed in numerical order, so it is easy to pick the wrong channel.

## 3. Levels

FlexRadio has no traditional ALC meter. Set the level as follows:

- In DAX I set the TX slider around the middle, at about 45–50.
- In VARA the drive level can start around −6 dB, but it is the DAX slider and the meter in SmartSDR that count.
- Adjust so that **LEVEL** in SmartSDR peaks just below 0 dB, around −5 dB, and does not go into the red.

Start with moderate power. 30–50 W is about right for a mode that transmits continuously. Increase slowly once everything looks good.

In Windows it is also worth checking that the DAX devices are not the default sound device, that their volume is at 100 %, and that the sample rate is 48 kHz.

## 4. SmartSDR CAT

In SmartSDR CAT I create two virtual COM ports, both tied to the same slice:

- A **CAT port** for frequency and control.
- A separate **PTT port**. FlexRadio recommends a dedicated PTT port so that keying is fast enough for VARA.

When creating the port: choose protocol CAT or PTT respectively, type Serial and FlexVSP, and the slice you will use for Winlink. It is a good idea to enable automatic switching of the TX slice, so the correct slice becomes the transmit slice when the program goes to transmit.

Do not add the TCP ports that Winlink and VARA use between themselves (often 8300) in SmartSDR CAT. Those belong to communication between the programs, not to the radio.

## 5. Winlink Express

In Winlink Express I choose the **VaraHF Winlink** session and open it.

Under Settings → SoundCard in the VARA window, the sound devices should be the same as above. Under Setup → Radio Setup:

- **Radio model:** Flex radios
- **Mode:** USB Digital
- **Radio Control Port:** the virtual CAT port you created
- **PTT Port:** Flex (the dedicated PTT port)

Winlink can then set the frequency for you. On the radio, the slice should remain in DIGU.

## 6. Test against an RMS gateway

In the session window, open Channel Selection and update the table via the internet. Sort by Path Reliability if you like, and pick a suitable gateway, for example a Nordic one on 40 or 80 m.

Check that the antenna is tuned, that the slice is in DIGU, and that the power is moderate. Then click Start. Winlink will show whether the channel is clear and then handle the connection.

## The same setup for VarAC

Audio, DAX, CAT and PTT are the same in VarAC. Point VARA HF at the same DAX devices and the same COM ports, and keep the slice in DIGU.

## Common pitfalls

- The wrong DAX channel in VARA, or no DAX channel selected on the slice
- The DAX button on the P/CW tab is off, so no transmit audio goes out
- Too much drive, so that LEVEL goes into the red
- Windows has chosen a DAX device as the default sound device and is interfering with the stream
- The slice is in ordinary USB instead of DIGU, so the processor or EQ affects the signal
- VARA's TCP ports added in SmartSDR CAT

FlexRadio's own guide for Winlink and VarAC is in their [help centre](https://helpdesk.flexradio.com/hc/en-us/articles/201056839-Configuring-WinLink-Express-and-VaraAC-with-the-FLEX-6000-8000-and-SmartSDR).
