+++
summary = "Lathund: så kopplar jag Winlink Express och VARA HF till Lab599 TX-500MP och DIY599 LiNK500MP, trådlöst över Bluetooth. **Läs mer →**"
title = "Winlink med TX-500MP och LiNK500MP"
url = "/krissamband/lathundar/winlink-tx500mp/"
description = "Lathund: så kopplar jag Winlink Express och VARA HF till Lab599 TX-500MP och DIY599 LiNK500MP, trådlöst över Bluetooth."
weight = 20
showDate = false
showAuthor = false
showReadingTime = false
showPagination = false
showDateUpdated = false
showHero = false
+++

Så här kör jag Winlink portabelt, med Lab599 TX-500MP och DIY599 LiNK500MP MK3. CAT och ljud går trådlöst över Bluetooth mellan laptopen och radion.

## Vad som behövs

- Lab599 TX-500MP
- DIY599 LiNK500MP MK3, monterad på radion
- En Windows-laptop med Bluetooth
- [Winlink Express](https://winlink.org/WinlinkExpress)
- [VARA HF](https://rosmodem.wordpress.com/) (finns också via [Winlinks nedladdningssida](https://downloads.winlink.org/VARA%20Products/))
- En antenn som fungerar på bandet, till exempel [Chameleon CHA LEFS4010 eller CHA Feather](/about/utrustning/#portabelt)

## 1. Koppla ihop LiNK500MP och TX-500MP

Montera LiNK500MP på TX-500MP enligt manualen (det görs bara första gången så jag tar inte med det här).

Sätt LiNK:en i **läge 3: BT ⇒ Radio CAT Interface (non iOS devices)**. Det är läget för CAT över Bluetooth till en Windows-dator. Trådlöst ljud finns i alla lägen.

Så här byter du läge:

1. Håll inne VFO-ratten tills den vita MOD-lampan tänds.
2. Vrid medurs. Vid varje steg blinkar lägets nummer; läge 3 är tre blinkningar.
3. Tryck kort på ratten. Det tar ungefär två sekunder innan läget är bytt.

Lysdioden PWR/BT blinkar grönt/blått när Bluetooth är redo, och lyser fast blått när den är ansluten.

USB-C på LiNK:en fungerar som reserv: då får du både ljudkort och CAT via kabel. I Enhetshanteraren syns då typiskt CAT som en Silicon Labs CP210x-port, plus USB PnP-ljud för mikrofon och högtalare. Portnumren varierar mellan datorer.

## 2. Para ihop laptopen

I Windows: **Bluetooth och enheter → Lägg till enhet → Bluetooth → Visa alla enheter**.

Välj enheten **LiNK500MP** (den med rätt symbol i listan). I listan kan även **LiNK500** och **Okänt enhet** dyka upp – ta inte dem. Bekräfta den PIN-kod som Windows visar och klicka på Anslut. När det är klart ska LiNK500MP stå som ansluten mikrofon och ljud.

Öppna Enhetshanteraren:

- Under **Anslutningar (COM & LPT)** finns två portar av typen *Standardmässig seriell över Bluetooth-anslutning*. En av dem är CAT-porten. Skriv upp båda numren; om frekvensstyrningen inte fungerar provar du den andra.
- Under **Ljudingångar och -utgångar** ska LiNK500MP finnas, ofta som *Hörlurar (LiNK500MP Hands-Free)*.

Stäng av **AGC** för LiNK500MP-ljudenheten i Windows, både för in- och utgång. Det gör stor skillnad för den digitala signalen.

## 3. Inställningar i TX-500MP

Grundfunktionerna ligger i skärmmenyn, bland annat **MODE** och **FLT**. Avancerade inställningar nås med **MENU**: bläddra med LEFT/RIGHT, öppna undermeny med F2 (SubMenu) och ändra värden med UP/DOWN. Avsluta med MENU igen.

| Meny | Inställning | Kommentar |
| --- | --- | --- |
| MODE (skärmmeny) | **DIG** | Radion skickar inte ut ljud eller data i vanligt USB. Det måste stå DIG. |
| 03 GAIN → DIG | Börja på **20** (standard och Lab599:s startvärde) | Ljudnivån in i sändaren i DIG. Justera sedan enligt avsnittet om VARA. |
| 04 METR | **DIG** | Visar DIG-nivån i stapeln när du sänder. |
| 01 POWER | Efter behov (10–100 % av max, 1–10 W på HF) | Effekten ställer du här, inte med ljudnivån. |
| 07 CMR | **DISABLE** | Talkompressorn ska vara av för digitalt. Standard är ENABLE. |
| 13 NB, 15 NR, 17 NF | **DISABLE** | Brusspärr, brusreducering och notch ska vara av. |
| 36 CAT Protocol | **TS2000** (standard) | LiNK-manualen anger CAT-rigg som Kenwood TS-2000. |

Välj ett tillräckligt brett mottagarfilter med **FLT** (fyra fasta filter). VARA HF är gjort för en SSB-bandbredd på ungefär 2,4 kHz, så ett smalt filter kan klippa signalen.

RF-förstärkningen (meny 02 RF) kan ställas separat för DIG. Standard är 0; sänk vid behov om starka signaler slår i taket.

Använd den inbyggda tunern vid behov: tryck **TUNE** för att slå på ATU, och håll inne TUNE för att stämma av. Vid SWR 3 eller högre sänker radion själv effekten.

## 4. VARA HF

VARA startas av Winlink Express, men ljudet ställer du in i VARA.

Under **Settings → SoundCard** väljer du LiNK500MP både som Input och Output. Använd inte laptopens inbyggda ljudkort.

Kolla att TCP-porten är densamma som i Winlink Express, oftast **8300**.

Mottagning: justera inspelningsnivån för LiNK500MP i Windows så att VARA:s nivåmätare ligger i grönt och inte klipper.

Sändning: sätt METR till DIG på radion, kör **Tune** i VARA och justera **GAIN → DIG**. Lab599:s guide för digitala moder säger att du ska fylla stapeln, men inte mer. Om DIG-värdet närmar sig max utan att stapeln fylls, höj uppspelningsnivån i Windows (i den guiden nämns ungefär 50–90 % i mixern) i stället för att bara maxa GAIN. Kör inte för hårt: överstyrning gör signalen bredare och sämre. Själva uteffekten ställer du med meny 01 POWER.

PTT sköts i Winlink Express via CAT, inte som en separat inställning som måste göras i VARA.

## 5. Winlink Express

Under **Settings → Winlink Express Setup** fyller jag i anropssignal (SM4T), lösenord och lokator (JP70RM).

I sessionslistan väljer jag **Vara HF Winlink** och öppnar sessionen. Då startar VARA HF.

I sessionsfönstret, under **Settings → Radio Setup**:

- **Radio:** Kenwood TS-2000 (det är den CAT-rigg LiNK-manualen anger)
- **Radio Control Port:** Bluetooth-CAT-porten från avsnitt 2
- **PTT:** via CAT på samma port

Om programmet byter frekvens åt dig fungerar CAT. **Kontrollera sedan att radion fortfarande står i DIG** innan du trycker på Start. LiNK-manualen varnar för att en del program sätter läget till USB via CAT, och då skickas inget ljud ut.

I sessionsfönstret öppnar du **Channel Selection** och uppdaterar tabellen via internet när du har nät. Sortera gärna på Path Reliability och välj en gateway som passar, till exempel en nordisk på 40 eller 80 meter. Spara favoriter i förväg: i ett riktigt krisläge har du ingen internetuppkoppling att hämta listan med.

Det finns också sessioner för direkttrafik mellan stationer (P2P), om båda parter kör samma mode.

## 6. Skicka ett mejl

1. Sätt på radion och LiNK500MP. Kontrollera att LiNK:en är i läge 3 och att PWR/BT lyser fast blått.
2. Sätt MODE till **DIG**, stäm av antennen med TUNE och välj en måttlig effekt.
3. Öppna Winlink Express, skriv meddelandet och öppna en **Vara HF Winlink**-session.
4. Uppdatera Channel Selection om du har internet, välj en gateway och kontrollera att radion hamnar på rätt frekvens **och fortfarande står i DIG**.
5. Klicka på **Start**. Winlink visar om kanalen är ledig och sköter sedan uppkopplingen.
6. När sessionen är klar har utgående mejl skickats och inkommande hämtats.

## Vanliga problem

- **Radion sänder inte, eller bara bärvåg:** den står nästan alltid i USB i stället för DIG. Sätt MODE till DIG.
- **Ingen CAT, frekvensen ändras inte:** fel av de två Bluetooth-COM-portarna, eller så är LiNK:en inte i läge 3. Prova den andra porten och kontrollera att PWR/BT lyser fast blått.
- **Inget ljud in i VARA:** fel ljudenhet vald, eller AGC fortfarande påslaget för LiNK500MP i Windows.
- **Bred eller distorterad signal:** sänk GAIN → DIG eller Windows-volymen. Stäng av CMR, NB, NR och NF.
- **Låg effekt:** SWR 3 eller högre får radion att sänka effekten själv. Stäm av med TUNE.
- **Radion vägrar sända efter en stund:** överhettningsskyddet slår till vid ungefär 60 °C.

## Tips portabelt och för krissamband

VARA sänder länge och tätt. TX-500MP ger högst 10 W på HF, och vid digital trafik är det klokt att inte ligga på max i onödan.

Inom Sverige, mot gateways eller andra stationer på kortare avstånd, är **40 och 80 meter** ofta de mest användbara banden, särskilt när antennen strålar brant uppåt (NVIS). Mer om det finns i [MUF och hur jonosfären fungerar](/om/amatorradio/muf-och-jonosfaren/).

Portabelt använder jag typiskt en enkel trådantenn, till exempel CHA LEFS4010 eller CHA Feather, och den inbyggda ATU:n.

Hämta en färsk kanallista och testa gärna mot en närliggande gateway medan du fortfarande har internet. Då vet du att upplägget fungerar när det väl behövs.

Källor till inställningarna: [Lab599 TX-500MP User manual (FW v1.24)](https://drive.google.com/file/d/1Zuf2KPHnu-Qy6mI1gvAWnFZqALG40wj9/view), [Lab599 TX-500 Digital modes setup guide](https://drive.google.com/file/d/1c3iPxMbwqddngruzKvdYcnaOakmHTs_a/view), [DIY599 LiNK500MP MK2/MK3 Instruction manual (V3.2-1031 rev 3)](https://drive.google.com/file/d/16H6q8aBq-ur9vsQhtR4nIEotIcYdOLjF/view), samt [Winlink Express](https://winlink.org/WinlinkExpress) och [VARA HF](https://rosmodem.wordpress.com/).
