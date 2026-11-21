+++
summary = "A quick guide to connecting Winlink Express and VARA HF to a Lab599 TX-500MP and DIY599 LiNK500MP, wirelessly over Bluetooth. **Read more →**"
title = "Winlink with TX-500MP and LiNK500MP"
url = "/en/emcomm/quick-guides/winlink-tx500mp/"
description = "A quick guide to connecting Winlink Express and VARA HF to a Lab599 TX-500MP and DIY599 LiNK500MP, wirelessly over Bluetooth."
weight = 20
showDate = false
showAuthor = false
showReadingTime = false
showPagination = false
showDateUpdated = false
showHero = false
+++

This is how I run Winlink portable, with a Lab599 TX-500MP and a DIY599 LiNK500MP MK3. CAT and audio go wirelessly over Bluetooth between the laptop and the radio.

## What you need

- A Lab599 TX-500MP
- A DIY599 LiNK500MP MK3, mounted on the radio
- A Windows laptop with Bluetooth
- [Winlink Express](https://winlink.org/WinlinkExpress)
- [VARA HF](https://rosmodem.wordpress.com/) (also available from the [Winlink download page](https://downloads.winlink.org/VARA%20Products/))
- An antenna that works on the band, for example a [Chameleon CHA LEFS4010 or CHA Feather](/en/about/gear/#portable)

## 1. Connecting the LiNK500MP to the TX-500MP

Set the LiNK to **mode 3: BT ⇒ Radio CAT Interface (non iOS devices)**. That is the mode for CAT over Bluetooth to a Windows computer. Wireless audio is available in all modes.

To change mode:

1. Hold the VFO knob until the white MOD LED lights.
2. Turn clockwise. At each step it blinks the mode number; mode 3 is three blinks.
3. Press the knob briefly. It takes about two seconds for the mode to change.

The PWR/BT LED blinks green/blue when Bluetooth is ready, and lights solid blue when it is connected.

USB-C on the LiNK works as a fallback: you then get both a sound card and CAT over a cable. In Device Manager, CAT typically appears as a Silicon Labs CP210x port, plus USB PnP audio for microphone and speaker. The port numbers vary between computers.

## 2. Pairing the laptop

In Windows: **Bluetooth and devices → Add device → Bluetooth → Show all devices**.

Select the device named **LiNK500MP** (the one with the correct symbol in the list). **LiNK500** and **Unknown device** may also appear – do not choose those. Confirm the PIN that Windows displays and click Connect. When it is done, LiNK500MP should be shown as a connected microphone and audio device.

Open Device Manager:

- Under **Ports (COM & LPT)** there are two ports of the type *Standard Serial over Bluetooth link*. One of them is the CAT port. Note both numbers; if frequency control does not work, try the other one.
- Under **Audio inputs and outputs**, LiNK500MP should appear, often as *Headphones (LiNK500MP Hands-Free)*.

Turn off **AGC** for the LiNK500MP audio device in Windows, on both the input and the output. It makes a large difference to the digital signal.

## 3. Settings on the TX-500MP

Basic functions are in the on-screen menu, including **MODE** and **FLT**. Advanced settings are reached with **MENU**: browse with LEFT/RIGHT, open a submenu with F2 (SubMenu) and change values with UP/DOWN. Press MENU again to exit.

| Menu | Setting | Notes |
| --- | --- | --- |
| MODE (on-screen menu) | **DIG** | The radio will not send audio or data in ordinary USB. It must be set to DIG. |
| 03 GAIN → DIG | Start at **20** (the default and Lab599's recommended starting value) | The audio level into the transmitter in DIG. Then adjust as described under VARA. |
| 04 METR | **DIG** | Shows the DIG level on the bar when you transmit. |
| 01 POWER | As needed (10–100 % of maximum, 1–10 W on HF) | Set power here, not with the audio level. |
| 07 CMR | **DISABLE** | The speech compressor must be off for digital modes. The default is ENABLE. |
| 13 NB, 15 NR, 17 NF | **DISABLE** | Noise blanker, noise reduction and notch must be off. |
| 36 CAT Protocol | **TS2000** (default) | The LiNK manual specifies the CAT rig as Kenwood TS-2000. |

Select a sufficiently wide receive filter with **FLT** (four fixed filters). VARA HF is designed for an SSB bandwidth of about 2.4 kHz, so a narrow filter can clip the signal.

RF gain (menu 02 RF) can be set separately for DIG. The default is 0; reduce it if needed when strong signals hit the limit.

Use the built-in tuner when needed: press **TUNE** to enable the ATU, and hold TUNE to start tuning. At SWR 3 or higher the radio reduces power on its own.

## 4. VARA HF

VARA is started by Winlink Express, but you set the audio in VARA.

Under **Settings → SoundCard**, choose LiNK500MP as both Input and Output. Do not use the laptop's built-in sound card.

Check that the TCP port is the same as in Winlink Express, usually **8300**.

Reception: adjust the Windows recording level for LiNK500MP so that VARA's level meter stays in the green and does not clip.

Transmission: set METR to DIG on the radio, use **Tune** in VARA and adjust **GAIN → DIG**. Lab599's digital-modes guide says to fill the meter, but no further. If the DIG value approaches maximum without the meter filling, raise the Windows playback level (that guide mentions about 50–90 % in the mixer) rather than only maxing GAIN. Do not overdrive: overdriving makes the signal wider and worse. RF output is set with menu 01 POWER.

PTT is handled in Winlink Express via CAT, not as a separate setting that has to be made in VARA.

## 5. Winlink Express

Under **Settings → Winlink Express Setup** I enter the callsign (SM4T), password and grid square (JP70RM).

In the session list I select **Vara HF Winlink** and open the session. VARA HF then starts.

In the session window, under **Settings → Radio Setup**:

- **Radio:** Kenwood TS-2000 (the CAT rig specified in the LiNK manual)
- **Radio Control Port:** the Bluetooth CAT port from section 2
- **PTT:** via CAT on the same port

If the program changes frequency for you, CAT is working. **Then check that the radio is still in DIG** before you press Start. The LiNK manual warns that some programs set the mode to USB via CAT, in which case no audio is sent.

In the session window, open **Channel Selection** and update the table via the internet while you have a network connection. Sorting by Path Reliability is useful, and then pick a gateway that fits, for example a Nordic one on 40 or 80 metres. Save favourites in advance: in a real emergency you will not have internet with which to download the list.

There are also sessions for direct station-to-station traffic (P2P), if both ends are running the same mode.

## 6. Sending a message

1. Turn on the radio and the LiNK500MP. Check that the LiNK is in mode 3 and that PWR/BT is solid blue.
2. Set MODE to **DIG**, match the antenna with TUNE and choose a moderate power level.
3. Open Winlink Express, write the message and open a **Vara HF Winlink** session.
4. Update Channel Selection if you have internet, select a gateway and check that the radio is on the right frequency **and still in DIG**.
5. Click **Start**. Winlink shows whether the channel is clear and then handles the connection.
6. When the session finishes, outgoing messages have been sent and incoming ones retrieved.

## Common problems

- **The radio does not transmit, or only a carrier:** it is almost always in USB instead of DIG. Set MODE to DIG.
- **No CAT, the frequency does not change:** the wrong one of the two Bluetooth COM ports, or the LiNK is not in mode 3. Try the other port and check that PWR/BT is solid blue.
- **No audio into VARA:** the wrong sound device is selected, or AGC is still on for LiNK500MP in Windows.
- **A wide or distorted signal:** lower GAIN → DIG or the Windows volume. Turn off CMR, NB, NR and NF.
- **Low power:** SWR of 3 or higher makes the radio reduce power on its own. Tune with TUNE.
- **The radio refuses to transmit after a while:** the overheating protection trips at about 60 °C.

## Tips for portable use and emergency communications

VARA transmits for long stretches at a time. The TX-500MP gives at most 10 W on HF, and for digital work it is wise not to stay on maximum unnecessarily.

Within Sweden, towards gateways or other stations at shorter distances, **40 and 80 metres** are often the most useful bands, especially when the antenna radiates steeply upwards (NVIS). There is more on this in [MUF and how the ionosphere works](/en/about/ham-radio/muf-and-the-ionosphere/).

Portable, I typically use a simple wire antenna, for example a CHA LEFS4010 or CHA Feather, and the built-in ATU.

Download a fresh channel list and, if you can, test against a nearby gateway while you still have internet. Then you know the setup works when it is actually needed.

Sources for the settings: [Lab599 TX-500MP User manual (FW v1.24)](https://drive.google.com/file/d/1Zuf2KPHnu-Qy6mI1gvAWnFZqALG40wj9/view), [Lab599 TX-500 Digital modes setup guide](https://drive.google.com/file/d/1c3iPxMbwqddngruzKvdYcnaOakmHTs_a/view), [DIY599 LiNK500MP MK2/MK3 Instruction manual (V3.2-1031 rev 3)](https://drive.google.com/file/d/16H6q8aBq-ur9vsQhtR4nIEotIcYdOLjF/view), plus [Winlink Express](https://winlink.org/WinlinkExpress) and [VARA HF](https://rosmodem.wordpress.com/).
