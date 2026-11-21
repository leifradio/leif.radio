+++
summary = "A quick guide to local handheld radio in Sweden: licence-exempt channels, amateur radio on 2 m and 70 cm, and practical routines for emergency communications nearby. **Read more →**"
title = "Handheld radio for local communication"
url = "/en/emcomm/quick-guides/komradio/"
description = "This is how I use a handheld radio for local contact when the mobile network is down: PMR446, hunting radio, 2 m and 70 cm, plus a few practical habits."
weight = 30
showDate = false
showAuthor = false
showReadingTime = false
showPagination = false
showDateUpdated = false
showHero = false
+++

When the usual channels are not working – a prolonged power outage, an overloaded mobile network, or the internet being down – a handheld radio is the simplest way to keep local contact. For me it belongs with the rest of [emergency communications](/en/emcomm/): regular HF, Winlink and VarAC for longer distances, and handheld radio plus MeshCore-like systems for the local area.

This quick guide is about local communication in Sweden: what is licence-exempt, what requires an amateur radio certificate, which channels actually apply, and a few habits that make it work when it is needed.

A radio in a box is not enough. We need to have agreed on a channel and routines in advance, and to have practised so that everyone in the household can turn the radio on and be heard.

A handheld radio does not replace 112, and it does not replace society's ordinary systems. In an emergency I call 112 for as long as that is possible. Rakel is the authorities' radio system and is not for the general public.

## Two tracks

There are two clearly different ways of running local radio, and they cannot be mixed freely.

**Licence-exempt.** Anyone may use certain equipment on certain frequencies, without an amateur radio certificate, as long as the conditions in the PTS regulations are followed. For the family, PMR446 is the most straightforward choice. There is also CB radio on 27 MHz, and more powerful radio on 155 MHz for agriculture, forestry and hunting. The equipment must be intended for that specific band and CE marked. An amateur radio, for example an IC-705, is not an approved PMR446 set: it has a detachable antenna and higher power, and must not be used licence-exempt on 446 MHz.

**Amateur radio.** On 2 m and 70 cm an amateur radio certificate and your own callsign are required. Then I can use, among other things, an IC-705, higher power and repeaters. Anyone without a certificate must not transmit on the amateur bands on their own (exceptions exist only for time-limited training or demonstration under the supervision of a certificate holder). For contact with family members who do not have a certificate, it is therefore PMR446, not 2 m/70 cm, that applies.

The channels are shared. No one has exclusive rights, and there is no right to protection from interference. All traffic is open: anyone can listen.

## PMR446

PMR446 is the ordinary small walkie-talkies sold for outdoor life, construction sites and family use. They are harmonised in Europe, so a radio bought in another EU country works here.

The rules in Sweden are clear. The frequency range is 446.0–446.2 MHz and the maximum power is 500 mW e.r.p. (0.5 W). The radio must be handheld and have an integral antenna. Base stations and repeaters are not permitted, and you may not extend the range with an external antenna.

There are 16 analogue FM channels with 12.5 kHz channel spacing. Older sets have only channels 1–8. There are also digital variants (dPMR and DMR Tier 1) in the same range; analogue and digital radios cannot hear each other unless they explicitly support the same mode. For family use I stick to analogue FM.

| Channel | Frequency (MHz) | Channel | Frequency (MHz) |
| --- | --- | --- | --- |
| 1 | 446.00625 | 9 | 446.10625 |
| 2 | 446.01875 | 10 | 446.11875 |
| 3 | 446.03125 | 11 | 446.13125 |
| 4 | 446.04375 | 12 | 446.14375 |
| 5 | 446.05625 | 13 | 446.15625 |
| 6 | 446.06875 | 14 | 446.16875 |
| 7 | 446.08125 | 15 | 446.18125 |
| 8 | 446.09375 | 16 | 446.19375 |

PTS itself states the range and the conditions, not the channel numbers. Numbers 1–16 and the frequencies above follow the European channel plan in ECC/DEC/(15)05 (lowest carrier 446.00625 MHz, 12.5 kHz steps). Consumer radios number the channels in the same way.

I have not found any official Swedish emergency or calling channel for PMR446 at PTS, SSA, FRO or the Swedish Agency for Civil Defence (Myndigheten för civilt försvar). Unofficial advice occurs, for example about channel 3, but that is not an authority channel. What matters is that we agree in advance on *one* channel (and a reserve channel), and that all sets are configured the same way.

A subtone (CTCSS/DCS) does not make the conversation private. It only mutes the speaker so that you do not hear traffic that lacks the same tone. On a shared listening channel it is often better to run without a subtone, so that you do not miss anyone. If we use a subtone, everyone must have the same one, and you should still listen to make sure the channel is clear before transmitting.

## Hunting radio on 155 MHz

On 155 MHz there are six licence-exempt carrier frequencies for *mobile radio transmitters for agriculture, forestry and hunting*, with a maximum of 5 W e.r.p. and 25 kHz channel spacing:

| Frequency (MHz) | Note |
| --- | --- |
| 155.400 | Must not be used within Swedish internal waters and the territorial sea |
| 155.425 | Must not be used within Swedish internal waters and the territorial sea |
| 155.450 | Must not be used within Swedish internal waters and the territorial sea |
| 155.475 | Must not be used within Swedish internal waters and the territorial sea |
| 155.500 | Also permitted at sea within the exemption |
| 155.525 | Also permitted at sea within the exemption |

PTS does not give official channel numbers (K1, K2 and the like). Manufacturers often number the same frequencies differently, and some sets also include 156.000 MHz as a "hunting channel". That frequency is a separate exemption for portable land-mobile transmitters (maximum 5 W e.r.p.), not one of the six hunting frequencies, and it sits next to maritime VHF. Therefore agree on *frequency*, not just "channel 1".

Unlike PMR446, the 155 MHz exemption does not require an integral antenna, and 5 W typically gives more range. The equipment must still be intended and approved for that use. An amateur radio that can be tuned to 155 MHz does not automatically make the transmission licence-exempt.

## Other licence-exempt voice radio

A few other exemptions are useful to know about, even if I do not see them as a first choice for simple family handheld radio:

- **CB radio on 27 MHz.** Licence-exempt in the range 26.965–27.405 MHz, with a maximum of 4 W e.r.p. on FM and 12 W p.e.p. e.r.p. on SSB. It can reach farther than PMR, but requires more antenna and is more exposed to interference and sometimes to long-distance propagation.
- **Land mobile radio on 31 MHz.** Forty carrier frequencies between 30.930 and 31.370 MHz, maximum 5 W e.r.p. The duty cycle is limited to a maximum of 10 percent, so it is not intended for long, frequent conversations. The channel numbers are not specified by PTS.
- **69 MHz.** Eight channels in 69.0–69.2 MHz, maximum 25 W e.r.p. and a duty cycle below 10 percent. One of the channels (69.0125 MHz) may only be used by mobile transmitters in Västra Götaland and Halland counties.

## Amateur radio: 2 m and 70 cm

With an amateur radio certificate I can use 2 m (144–146 MHz) and, in Sweden, 70 cm in the allocation 432–438 MHz. The maximum power under the exemption is 200 W p.e.p. delivered to the antenna system (25 W e.r.p. with an entry-level certificate). A handheld or an IC-705 is well below that. The callsign must be transmitted at the beginning and end of each contact, and repeated at short intervals.

In the IARU Region 1 band plan, which SSA follows, the FM calling frequencies are:

- **145.500 MHz** on 2 m
- **433.500 MHz** on 70 cm

Calls are made there, and then you move to another simplex channel so that the calling frequency is left clear. The simplex range on 2 m is 145.206–145.5625 MHz (12.5 kHz channel steps). On 70 cm, simplex is 433.400–433.575 MHz. 145.375 and 433.450 MHz are calling frequencies for digital voice (DV), not for ordinary FM.

Sweden has, as far as I have been able to see, no emergency channel on the amateur bands specifically designated by PTS. IARU Region 1 does, however, specify centres of activity on HF, including 3.760, 7.110 and 14.300 MHz; Sweden is listed there. They are not exclusive emergency channels, and activity may lie around ±20 kHz. That is a different tool from this quick guide, which is about local communication.

**Repeaters around Borlänge.** Borlänge Sändareamatörer (SK4BW) publish three 70 cm repeaters, all with a −2 MHz shift:

| Type | Output | Input | Access |
| --- | --- | --- | --- |
| Analogue FM | 434.800 MHz | 432.800 MHz | CTCSS 85.4 Hz (no 1750 Hz tone) |
| DMR | 434.850 MHz | 432.850 MHz | Color code 12, repeater-ID 240401 |
| D-STAR | 434.900 MHz | 432.900 MHz | R1: SK4BW B, R2: SK4BW G, UR: CQCQCQ |

The club's page also describes the Svxlink node SK4RVN on 434.800 MHz, with a link to among others SK4RGL in Falun. Repeaters change, so I take the current status from the [club page](https://www.sk4bw.net/repeater/) and SSA's [repeater map](https://www.ssa.se/ssa/repeatrar-fyrar/). The IC-705 handles both analogue FM and D-STAR, which fits the local D-STAR repeater.

Amateur traffic must not be encoded to conceal its content. It is open, just like PMR.

## FRO, SSA and what is not a public channel

Frivilliga Radioorganisationen (FRO) is a voluntary defence organisation that trains, among others, radio operators in support of command and coordination when ordinary systems are not sufficient. You do not need to be a radio amateur to get involved there. SSA (Sveriges Sändareamatörer, the Swedish amateur radio society) and the local amateur radio clubs practise preparedness and can support society, but that happens by agreement and under the command that applies to the operation.

There are therefore organisations and routines for emergency communications, but not a public "emergency channel" that the general public is expected to gather on with PMR or hunting radio. Plan for your own circle: family, neighbours, or the group you actually need to reach.

Rakel may only be used by the authorised user group that has duties in public order, security or health. It is not a system that I or other private individuals can join.

## Practical habits

**Agree in advance.** Write it down and practise:

- which type of radio (PMR446, hunting radio or amateur radio – they cannot be mixed)
- channel or exact frequency, and a reserve channel
- subtone or not (and if so, which one)
- when we listen, for example five minutes at every hour on the hour
- what we say, and what we *do not* say over an open channel

**Range.** It depends mostly on terrain and antenna height, not on what it says on the box. With PMR at 0.5 W and a fixed antenna, in a built-up area and in woodland it is often a few hundred metres up to a kilometre or so. With a clear line of sight, especially from a height, it can be longer. 5 W hunting radio typically reaches farther, but is still limited by hills, buildings and forest. Going up a floor, onto a hill, or simply walking out of a valley makes more difference than raising your voice into the microphone.

**Antenna and height.** On PMR the antenna must not be changed. Height is then what you can influence: go upwards, hold the radio upright, and avoid standing behind a building. On hunting radio and amateur radio, a better antenna and a higher placement make a big difference. On 2 m and 70 cm, a small outdoor antenna or working through a repeater can change coverage completely.

**Batteries.** Spare batteries matter more than spare radios. A battery tray for AA cells is useful when charging is not possible. Charge before an outage, do not waste transmission unnecessarily, and expect a radio left listening around the clock to run down faster than you think. A simple schedule (switched off between listening periods) often lasts longer.

**Operating habits.** Listen first. Hold PTT for a brief moment before you speak, and release when you are done so the other person can answer. Call clearly, for example: "Evalena, this is Leif, come in." Keep messages short and concrete: where you are, how you are, what you need, when you will listen next. Say names and places clearly, preferably twice if it is important. "Roger" is enough as a confirmation. End so that the other person knows you are finished.

**Privacy.** Everything that is said can be heard by others. Do not send information that cannot stand being made public: precise alarm details about a third person, door codes, and the like. A subtone, digital "privacy" and the privacy codes on cheap radios are not encryption.

## MeshCore and similar LoRa networks

As a complement to voice radio I like to use MeshCore-like systems: small LoRa nodes that send text and position in a mesh, without a mobile network. In Sweden this is licence-exempt as short-range devices in the 868 MHz range, provided you stay within the correct sub-band, power and duty cycle.

A common mode, which Meshtastic calls EU_868, is in 869.40–869.65 MHz. There, PTS allows a maximum of 500 mW e.r.p. and, unless another approved technique is used to avoid interference, a duty cycle of at most 10 percent. Other sub-bands, for example 868.0–868.6 MHz, have lower power (25 mW) and a stricter duty cycle. Region and settings must be the same on all nodes that are to hear each other, and the duty cycle must not be circumvented.

This does not replace voice on a handheld radio. It is a good complement for short messages and status information, especially if the nodes are placed high. Just as with other licence-exempt radio, the traffic is in principle something others can receive.

## Sources

- PTS, *PTSFS 2025:1*, regulations on exemption from the licence requirement, including Chapter 3, Sections 27, 69–84, 91, 100, 103–104, 109–110, 123–124, 128 and 141–149. In force from 17 March 2025: [the regulation](https://pts.se/regelbibliotek/foreskrifter-ptsfs-20251-om-undantag-fran-tillstandsplikt-for-anvandning-av-vissa-radiosandare/)
- CEPT, [ECC/DEC/(15)05](https://docdb.cept.org/download/b8797390-4577/ECCDec1505.pdf) on PMR446 (channel plan, 500 mW, handheld radio with integral antenna)
- SSA, [band plan 144–146 MHz](https://www.ssa.se/vushf/wp-content/uploads/sites/12/2020/11/144-MHz.pdf) (2020-11-26) and [band plan 432–438 MHz](https://www.ssa.se/vushf/wp-content/uploads/sites/12/2024/06/432-MHz.pdf) (2024-04-08), based on IARU Region 1
- IARU Region 1, [Emergency Communications Frequencies](https://www.iaru-r1.org/about-us/committees-and-working-groups/emcomm/emergency-communications-frequencies/)
- SSA, [Repeaters & beacons](https://www.ssa.se/ssa/repeatrar-fyrar/) (repeater map), and [SK4BW's repeater page](https://www.sk4bw.net/repeater/)
- Swedish Agency for Civil Defence (Myndigheten för civilt försvar), [Who can connect to Rakel](https://www.mcf.se/sv/amnesomraden/samhallsviktiga-kommunikationstjanster/rakel/anslut-till-rakel/vilka-kan-ansluta-till-rakel/)
- FRO, [Radio operator](https://fro.se/radiooperator/)
- ITU Radio Regulations, Article 25 (the amateur service; transmissions shall not be encoded to conceal their meaning)
- Meshtastic, [LoRa configuration / region EU_868](https://meshtastic.org/docs/configuration/radio/lora/), together with PTSFS 2025:1, Section 146

The conditions can change. Always check the current text at PTS before you buy or transmit.
