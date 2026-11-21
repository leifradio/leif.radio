+++
title = "MUF and how the ionosphere works"
url = "/en/about/ham-radio/muf-and-the-ionosphere/"
aliases = ["/en/about/amateur-radio/muf-and-the-ionosphere/", "/en/about/ham-radio/muf/"]
description = "A walkthrough of the ionospheric layers, MUF, LUF and FOT, and what they mean for 20, 40 and 80 metres from Sweden."
weight = 10
showDate = false
showAuthor = false
showReadingTime = false
showPagination = false
showDateUpdated = false
showHero = false
showTableOfContents = true
+++

When we operate HF – short wave, roughly 1.8 to 30 MHz – radio waves can be bent back in the ionosphere and reach the other side of the Earth. How far they go, and on which band, depends on what the ionosphere looks like at the time. Here I try to explain the terms that come up most often, such as MUF, and how they tie in with what I see myself when I operate from Borlänge (JP70).

## The layers of the ionosphere

The ionosphere is the part of the upper atmosphere where the Sun knocks electrons loose from the gases, so that the air becomes electrically conductive. It is that conductive air that can bend a radio wave back towards the Earth. Without that bending, the HF wave would simply continue out into space.

We usually talk about four layers, by approximate height:

The **D layer**, at about 60–90 km, is present more or less only during the day. It absorbs lower HF frequencies – especially 160 metres, 80 metres and to some extent 40 metres – so longer contacts on those bands are difficult while the Sun is high. When the Sun sets, the electrons recombine quickly and the D layer almost disappears. That is an important reason why 80 and 40 metres come to life in the evening.

The **E layer**, at about 90–150 km, is also strongest during the day. It can provide shorter hops, and sometimes so-called sporadic E appears, which can suddenly open the higher bands over unexpectedly short distances. At night the E layer weakens considerably.

The **F1 and F2 layers** sit highest. F1, at about 150–250 km, is seen mainly during the day and merges with F2 at night. The **F2 layer**, typically 250–400 km and sometimes higher, is the most important one for long-distance HF. It is present both day and night. During the day the electron density is highest, and higher frequencies can be bent back. At night the density drops and the highest bands often close, but F2 remains and still supports 40 metres and, depending on the season and the solar cycle, sometimes 20 metres.

{{< figure src="/img/ionosphere-en.svg" alt="Schematic of the ionosphere's D, E, F1 and F2 layers, with a ground wave, a dead zone and a skywave being bent back in the F2 layer" caption="The ionospheric layers and a typical HF skip. Heights in the diagram are not to scale." >}}

## The solar cycle, solar flux and sunspots

The Sun's activity varies in a cycle of about eleven years. More sunspots generally mean more ultraviolet and X-ray radiation, which in turn builds up the ionosphere more strongly, especially F2. The frequencies that can be used for long-distance traffic then rise, and bands such as 15 and 10 metres open more often.

Two figures keep turning up in space-weather reports:

- **Solar flux** (SFI, Solar Flux Index) is measured at a wavelength of 10.7 cm (2,800 MHz) and is a practical measure of the Sun's activity, even when no spots are visible. Higher solar flux usually means a higher MUF.
- The **sunspot number** (SSN) is counted from the spots on the solar disc. It follows the same cycle and is used a great deal in older tables and prediction models.

Both are indicators, not guarantees. A high solar flux gives better conditions, but time of day, season, the geomagnetic situation and the particular path matter at least as much.

## MUF, LUF and FOT

Three abbreviations describe the frequency window that can actually be used between two places at a given time:

- **MUF**, Maximum Usable Frequency, is the highest frequency that can then support a contact over that path via the ionosphere. Just above the MUF, the wave punches through the F layer and disappears into space. The MUF applies to a particular path and time – it is not a single figure for the whole Earth.
- **LUF**, Lowest Usable Frequency, is the lowest frequency that still gives a usable signal. Below the LUF the signal is eaten up by absorption, mainly in the D layer, or is lost in the noise.
- **FOT**, Frequency of Optimum Traffic, sometimes called the optimum working frequency, is the frequency one often aims for in practice. A common rule of thumb is about 85 percent of the MUF. Right under the MUF the path can suddenly drop out, so a little margin makes traffic more reliable.

The **critical frequency**, foF2, is the highest frequency that bounces straight up and back from the F2 layer. It is measured with ionosondes, which send a pulse vertically and listen for the echo. foF2 is therefore the MUF for a completely vertical path, and it is lower than the MUF for a long DX hop.

The relationship is sometimes called the **secant law**. A wave that enters the ionosphere at an angle travels a longer path through the layer than one that goes straight up, and is therefore bent back even at a higher frequency. In plain terms: the shallower the angle to the layer (a longer hop, a low take-off angle), the higher the MUF for that path. Formally, the MUF is often written as about foF2 times the secant of the angle of incidence, measured from the vertical. That is why you can have DX on 20 or 15 metres even when the local foF2 is some way below the frequency of the band.

## Skip and the dead zone

An HF wave leaving the antenna can follow the ground for a short distance (the ground wave) and at the same time go up towards the ionosphere and come down again farther away (the skywave). The distance to the first point where the skywave returns to Earth is called the skip distance.

Between the end of the ground wave and the first skywave landing there is a **dead zone**, or skip zone, where the station is not heard, or is heard only very weakly. On the higher bands, for example 20 metres, that zone can be several hundred kilometres. That is why a station in southern Sweden or northern Germany can sometimes be harder to reach from Borlänge on 20 metres than a station in southern Europe or on the other side of the Atlantic. On the lower bands, and when the MUF is low, the wave can come down over much shorter distances – often called NVIS, when the antenna radiates steeply upwards and covers the near area.

## 20 metres by day, 40 and 80 in the evening

Seen from Sweden, and from my QTH in JP70, the daily pattern is often quite clear.

**20 metres** (14 MHz) is primarily a daytime band. During the day the MUF is often high enough for 14 MHz to be bent back in F2, and the D layer does not absorb 20 metres as heavily as the lower bands. In the morning it tends to open to the east and south, towards Asia and Africa, and in the afternoon more to the west, towards North America. In the evening and at night the MUF falls. Near solar maximum, 20 metres can stay open longer, but in quieter periods and in mid-winter it often closes once it gets dark.

**40 metres** (7 MHz) and **80 metres** (3.5 MHz) behave the other way around. During the day the D layer attenuates them, so the range is mostly regional. As the Sun sets the absorption disappears, and longer paths open. From Borlänge, 40 metres is typically a late-afternoon, evening and night-time band – Europe first, then longer DX once it has become dark along the path. 80 metres is affected even more by daytime absorption and is in practice an evening and night-time band, especially in winter when the nights are long and atmospheric noise is lower than in summer.

This is a rule of thumb, not a law. Season, the solar cycle and the geomagnetic situation shift the windows, and any given day can look different.

## Kp, the A-index and disturbances

The Sun does not only send the radiation that builds up the ionosphere. It can also disturb it.

The **Kp index** is a planetary measure of geomagnetic activity, from 0 to 9, in three-hour periods. The **A-index** is a daily value derived from the same data. Low values mean quiet conditions. When Kp rises, the Earth's magnetic field is disturbed, and the ionosphere – especially at higher latitudes – can become unsettled. foF2 often falls, signals can fade quickly, and paths that pass close to the magnetic poles become unreliable. NOAA describes the stronger events on a G scale, from G1 to G5.

This matters here in Sweden. Borlänge lies at about 60 degrees north, much closer to the auroral zone than a station in southern Europe, for example. The same geomagnetic storm that is barely noticeable in the Mediterranean can make HF from Dalarna messy, especially towards North America and Asia.

Another kind of outage comes from **X-ray flares** on the Sun. They strengthen the D layer on the sunlit side of the Earth and can cause sudden absorption, especially on the lower HF bands. NOAA calls these radio blackouts and grades them R1 to R5. Such an outage follows the Sun: it is felt when we have daylight and lifts when the flare is over, often within minutes to an hour or so. Separately, there are also proton events that can cause absorption over the polar regions, known as polar cap absorption.

## Greyline

The greyline is the transition zone between day and night along the Earth's terminator. Right there, the D layer is disappearing at dusk, or has not yet built up at dawn, while the F layer can still be relatively strong. That can give unusually good, sometimes long, openings, especially on 40, 80 and 160 metres.

In practice, that means the end of dawn and the beginning of dusk are times worth listening more carefully, not least towards the opposite side of the Earth along the current greyline. The opening can be short.

## Where to look in practice

I myself look at a few open sources when I want to know how conditions are:

- The [KC2G MUF map](https://prop.kc2g.com/) shows a near-real-time picture of foF2 and MUF, built from ionosonde measurements. It is useful for seeing whether 20 metres should be open at all, and in which direction.
- The [NOAA Space Weather Prediction Center](https://www.swpc.noaa.gov/) publishes solar flux, sunspot number, Kp and forecasts, as well as estimates of [D-region absorption](https://www.swpc.noaa.gov/products/d-region-absorption-predictions-d-rap). Their space weather is the same basis I use when I write about HF conditions on this site.
- The [Reverse Beacon Network (RBN)](https://www.reversebeacon.net/) is a network of automatic listening stations, or skimmers, that report the CW (and some other modes) they hear. By searching for your own callsign you can see where you were actually heard, on which band and at what signal strength. It is one of the most direct ways of checking the theory against reality.

Maps and indices provide a frame. What decides it is still whether anyone is heard in the speaker – and the RBN is often the bridge I use between the forecast and what I transmit myself.
