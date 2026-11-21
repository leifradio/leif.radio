+++
summary = "Lathund: så kopplar jag Winlink Express och VARA HF till FlexRadio FLEX-8400 med SmartSDR, DAX och CAT. **Läs mer →**"
title = "Winlink på Flexradio"
url = "/krissamband/lathundar/winlink-flexradio/"
description = "Lathund: så kopplar jag Winlink Express och VARA HF till FlexRadio FLEX-8400 med SmartSDR, DAX och CAT."
weight = 10
showDate = false
showAuthor = false
showReadingTime = false
showPagination = false
showDateUpdated = false
showHero = false
+++

Det här är så jag kör Winlink hemifrån i Borlänge, med FlexRadio FLEX-8400 och anropssignalen SM4T. Samma upplägg fungerar för VarAC. Ingen extra hårdvara behövs – varken ljudkort eller CAT-kabel. Allt går via nätverket.

## Vad som behövs

På samma Windows-dator, ansluten till samma nätverk som radion:

- [SmartSDR för Windows](https://www.flexradio.com/software/) – tillsammans med programmet installeras DAX (ljudet) och SmartSDR CAT (styrningen)
- [Winlink Express](https://winlink.org/WinlinkExpress)
- [VARA HF](https://rosmodem.wordpress.com/)

Radion och datorn behöver bara ligga på samma nät. Jag använder själv en FLEX-8400, men stegen är desamma på övriga FLEX-6000- och FLEX-8000-modeller.

## 1. Slice, läge och filter i SmartSDR

Skapa en slice för Winlink och sätt läget till **DIGU**, inte vanligt USB. I DIGU hålls processor och equalizer borta, vilket annars kan förvränga den digitala signalen.

VARA HF använder 2,3 kHz eller 500 Hz, så filtret i slicen behöver vara tillräckligt brett. FlexRadio rekommenderar omkring 3,5 kHz för just Winlink och VARA; jag sätter det till ungefär 3–3,5 kHz. Filterbredden justeras i Radio Control-panelen. Under Settings → Radio Setup → Filters går det också att anpassa de digitala filtren.

På P/CW-fliken under Radio Controls ska **DAX** vara påslaget, så att sändarljudet kommer från DAX och inte från mikrofonen.

## 2. DAX

Öppna DAX-panelen och se till att den är kopplad till samma station eller klient som styr radion.

- I slicen, under DAX-menyn, välj kanal 1 (eller en annan ledig kanal – håll sedan samma nummer överallt).
- I DAX-panelen ska RX-strömmen för den kanalen vara aktiv. I nuvarande SmartSDR (DAXv2 i v4) blir indikatorn blå när kanalen är kopplad till slicen, och grön när ett program faktiskt läser ljudet.
- Sändningen går via den gemensamma strömmen **DAX TX**. Den blir blå när DAX-knappen på P/CW-fliken är på, och grön när programmet sänder.

I VARA HF, under Settings → SoundCard, väljer du:

- **Input:** `DAX RX 1` (i äldre SmartSDR kan det heta `DAX Audio RX 1`; i DAXv2 ofta `DAX RX 1 (FlexRadio DAX)`)
- **Output:** `DAX TX` (äldre namn: `DAX Audio TX`; i DAXv2 ofta `DAX TX (FlexRadio DAX)`)

Enheterna syns inte i listan förrän DAX-programmet körs. De står inte alltid i nummerordning, så det är lätt att välja fel kanal.

## 3. Nivåer

FlexRadio har ingen klassisk ALC-mätare. Nivån ställs in så här:

- I DAX sätter jag TX-reglaget ungefär mitt emellan, kring 45–50.
- I VARA kan drive level börja kring −6 dB, men det är DAX-reglaget och mätaren i SmartSDR som gäller.
- Justera så att **LEVEL** i SmartSDR toppar strax under 0 dB, ungefär −5 dB, och inte går in i det röda.

Börja med måttlig effekt. 30–50 W är lagom för ett mode som sänder kontinuerligt. Höj sakta när allt ser bra ut.

I Windows kan det också vara värt att kontrollera att DAX-enheterna inte är standardljudenhet, att volymen står på 100 % och att samplingsfrekvensen är 48 kHz.

## 4. SmartSDR CAT

I SmartSDR CAT skapar jag två virtuella COM-portar, knutna till samma slice:

- En **CAT-port** för frekvens och styrning.
- En separat **PTT-port**. FlexRadio rekommenderar en dedikerad PTT-port, så att nycklingen blir tillräckligt snabb för VARA.

När porten skapas: välj protokoll CAT respektive PTT, typ Serial och FlexVSP, och den slice du kör Winlink på. Det är bra att slå på automatisk växling av TX-slice, så att rätt slice blir sändarsliced när programmet går i sändning.

Lägg inte in de TCP-portar som Winlink och VARA använder mellan sig (ofta 8300) i SmartSDR CAT. De hör till kommunikationen mellan programmen, inte till radion.

## 5. Winlink Express

I Winlink Express väljer jag sessionen **VaraHF Winlink** och öppnar den.

Under Settings → SoundCard i VARA-fönstret ska ljudenheterna vara desamma som ovan. Under Setup → Radio Setup:

- **Radio model:** Flex radios
- **Mode:** USB Digital
- **Radio Control Port:** den virtuella CAT-port du skapade
- **PTT Port:** Flex (den dedikerade PTT-porten)

Då kan Winlink byta frekvens åt dig. På radion ska slicen ligga kvar i DIGU.

## 6. Testa mot en RMS-gateway

I sessionsfönstret, öppna Channel Selection och uppdatera tabellen via internet. Sortera gärna på Path Reliability och välj en gateway som passar, till exempel en nordisk på 40 eller 80 m.

Kontrollera att antennen är avstämd, att slicen är i DIGU och att effekten är måttlig. Klicka sedan på Start. Winlink visar om kanalen är ledig och sköter sedan uppkopplingen.

## Samma sak för VarAC

Ljud, DAX, CAT och PTT är desamma i VarAC. Koppla VARA HF till samma DAX-enheter och samma COM-portar, och kör slicen i DIGU.

## Vanliga fallgropar

- Fel DAX-kanal i VARA, eller att slicen inte har någon DAX-kanal vald
- DAX-knappen på P/CW-fliken är avstängd, så inget sändarljud går ut
- För hög drivning, så att LEVEL går in i det röda
- Windows har valt en DAX-enhet som standardljudenhet och stör strömmen
- Slice i vanligt USB i stället för DIGU, så att processor eller EQ påverkar signalen
- VARA:s TCP-portar tillagda i SmartSDR CAT

FlexRadios egen guide för Winlink och VarAC finns i deras [hjälpcenter](https://helpdesk.flexradio.com/hc/en-us/articles/201056839-Configuring-WinLink-Express-and-VaraAC-with-the-FLEX-6000-8000-and-SmartSDR).
