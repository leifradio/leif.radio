+++
summary = "Lathund för lokal komradio i Sverige: tillståndsfria kanaler, amatörradio på 2 m och 70 cm, och praktiska rutiner för krissamband i närområdet. **Läs mer →**"
title = "Komradio för närkommunikation"
url = "/krissamband/lathundar/komradio/"
description = "Så här använder jag handhållen komradio för lokal kontakt när mobilnätet inte fungerar: PMR446, jaktradio, 2 m och 70 cm, plus några praktiska vanor."
weight = 30
showDate = false
showAuthor = false
showReadingTime = false
showPagination = false
showDateUpdated = false
showHero = false
+++

När de vanliga vägarna inte fungerar – längre strömavbrott, överbelastat mobilnät eller internet som ligger nere – är en handhållen komradio det enklaste sättet att hålla lokal kontakt. För mig hör det ihop med övrigt [krissamband](/krissamband/): vanlig HF, Winlink och VarAC för längre håll, och komradio plus MeshCore-liknande system för närområdet.

Den här lathunden handlar om närkommunikation i Sverige: vad som är tillståndsfritt, vad som kräver amatörradiocertifikat, vilka kanaler som faktiskt gäller, och några vanor som gör att det fungerar när det behövs.

En radio i en låda räcker inte. Vi behöver ha bestämt kanal och rutiner i förväg, och ha övat så att alla i hushållet kan slå på radion och bli hörda.

Komradio ersätter inte 112 och inte samhällets ordinarie system. Vid nöd ringer jag 112 så länge det går. Rakel är myndigheternas radiosystem och är inte till för allmänheten.

## Två spår

Det finns två tydligt olika sätt att köra lokal radio, och de går inte att blanda hur som helst.

**Tillståndsfritt.** Vem som helst får använda viss utrustning på vissa frekvenser, utan amatörradiocertifikat, så länge villkoren i PTS föreskrifter följs. För familjen är PMR446 det mest raka valet. Det finns också privatradio på 27 MHz och starkare radio på 155 MHz för jord- och skogsbruk samt jakt. Utrustningen ska vara avsedd för just det bandet och CE-märkt. En amatörradio, till exempel IC-705, är inte en godkänd PMR446-apparat: den har utbytbar antenn och högre effekt, och får inte användas tillståndsfritt på 446 MHz.

**Amatörradio.** På 2 m och 70 cm krävs amatörradiocertifikat och en egen anropssignal. Då får jag använda bland annat IC-705, högre effekt och repeatrar. Den som inte har certifikat får inte sända på amatörbanden på egen hand (undantag finns bara för tidsbegränsad utbildning eller förevisning under uppsikt av en certifikatinnehavare). För kontakt med familjen utan certifikat är därför PMR446, inte 2 m/70 cm, det som gäller.

Kanalerna är delade. Ingen har ensamrätt, och man har ingen rätt att skyddas mot störning. All trafik är öppen: vem som helst kan lyssna.

## PMR446

PMR446 är de vanliga små walkie-talkies som säljs för friluftsliv, byggarbetsplatser och familjebruk. De är harmoniserade i Europa, så en radio som köps i ett annat EU-land fungerar här.

Reglerna i Sverige är tydliga. Frekvensområdet är 446,0–446,2 MHz och högsta effekten 500 mW e.r.p. (0,5 W). Radion ska vara handhållen och ha integrerad antenn. Basstationer och repeatrar är inte tillåtna, och man får inte bygga ut räckvidden med en yttre antenn.

Det finns 16 analoga FM-kanaler med 12,5 kHz kanaldelning. Äldre apparater har bara kanal 1–8. Det finns också digitala varianter (dPMR och DMR Tier 1) i samma område; analog och digital radio hör inte varandra om de inte explicit stöder samma läge. För familjebruk håller jag mig till analog FM.

| Kanal | Frekvens (MHz) | Kanal | Frekvens (MHz) |
| --- | --- | --- | --- |
| 1 | 446,00625 | 9 | 446,10625 |
| 2 | 446,01875 | 10 | 446,11875 |
| 3 | 446,03125 | 11 | 446,13125 |
| 4 | 446,04375 | 12 | 446,14375 |
| 5 | 446,05625 | 13 | 446,15625 |
| 6 | 446,06875 | 14 | 446,16875 |
| 7 | 446,08125 | 15 | 446,18125 |
| 8 | 446,09375 | 16 | 446,19375 |

PTS anger själva intervallet och villkoren, inte kanalnumren. Nummer 1–16 och frekvenserna ovan följer den europeiska kanalplanen i ECC/DEC/(15)05 (lägsta bärvåg 446,00625 MHz, 12,5 kHz steg). Konsumentradior numrerar kanalerna på samma sätt.

Jag har inte hittat någon officiell svensk nöd- eller anropskanal för PMR446 hos PTS, SSA, FRO eller Myndigheten för civilt försvar. Det förekommer inofficiella råd om till exempel kanal 3, men det är inte en myndighetskanal. Det viktiga är att vi i förväg bestämmer *en* kanal (och en reservkanal), och att alla apparater är inställda likadant.

Subton (CTCSS/DCS) gör inte samtalet privat. Den spärrar bara högtalaren så att du inte hör trafik som saknar samma ton. På en gemensam lyssningskanal är det ofta bättre att köra utan subton, så att man inte missar någon. Om vi använder subton måste alla ha samma, och man ska ändå lyssna att kanalen är ledig innan man sänder.

## Jaktradio på 155 MHz

På 155 MHz finns sex tillståndsfria bärvågsfrekvenser för *mobila radiosändare för jord- och skogsbruk samt jakt*, med högst 5 W e.r.p. och 25 kHz kanaldelning:

| Frekvens (MHz) | Anmärkning |
| --- | --- |
| 155,400 | Får inte användas inom svenskt inre vatten och territorialhav |
| 155,425 | Får inte användas inom svenskt inre vatten och territorialhav |
| 155,450 | Får inte användas inom svenskt inre vatten och territorialhav |
| 155,475 | Får inte användas inom svenskt inre vatten och territorialhav |
| 155,500 | Även tillåten till sjöss inom undantaget |
| 155,525 | Även tillåten till sjöss inom undantaget |

PTS ger inga officiella kanalnummer (K1, K2 och liknande). Tillverkare numrerar ofta samma frekvenser olika, och en del apparater tar också med 156,000 MHz som en "jaktkanal". Den frekvensen är ett separat undantag för bärbara landmobila sändare (högst 5 W e.r.p.), inte en av de sex jaktfrekvenserna, och den ligger intill sjöfartens marina VHF. Kom därför överens om *frekvens*, inte bara "kanal 1".

Till skillnad från PMR446 kräver undantaget på 155 MHz inte fast antenn, och 5 W ger typiskt mer räckvidd. Utrustningen ska ändå vara avsedd och godkänd för den användningen. En amatörradio som kan ställas in på 155 MHz gör inte automatiskt sändningen tillståndsfri.

## Annan tillståndsfri röstadio

Några andra undantag kan vara bra att känna till, även om jag inte ser dem som förstahandsval för enkel familjekomradio:

- **Privatradio (CB) på 27 MHz.** Tillståndsfritt i området 26,965–27,405 MHz, med högst 4 W e.r.p. vid FM och 12 W p.e.p. e.r.p. vid SSB. Kan nå längre än PMR, men kräver mer antenn och är mer utsatt för störningar och ibland för fjärrutbredning.
- **Landmobilradio på 31 MHz.** Fyrtio bärvågsfrekvenser mellan 30,930 och 31,370 MHz, högst 5 W e.r.p. Sändningscykeln är begränsad till högst 10 procent, så det är inte tänkt för långa, täta samtal. Kanalnumren är inte angivna av PTS.
- **69 MHz.** Åtta kanaler i 69,0–69,2 MHz, högst 25 W e.r.p. och sändningscykel under 10 procent. En av kanalerna (69,0125 MHz) får bara användas av mobila sändare i Västra Götalands och Hallands län.

## Amatörradio: 2 m och 70 cm

Med amatörradiocertifikat kan jag använda 2 m (144–146 MHz) och, i Sverige, 70 cm i tilldelningen 432–438 MHz. Högsta effekten enligt undantaget är 200 W p.e.p. tillförd antennsystemet (25 W e.r.p. med instegscertifikat). En handapparat eller IC-705 ligger långt under det. Anropssignalen ska sändas i början och slutet av varje förbindelse, och upprepas med korta mellanrum.

I IARU Region 1:s bandplan, som SSA följer, är FM-anropsfrekvenserna:

- **145,500 MHz** på 2 m
- **433,500 MHz** på 70 cm

Anrop görs där, och sedan flyttar man till en annan simplexkanal så att anropsfrekvensen blir fri. Simplexområdet på 2 m är 145,206–145,5625 MHz (12,5 kHz kanalsteg). På 70 cm är simplex 433,400–433,575 MHz. 145,375 och 433,450 MHz är anropsfrekvenser för digitalt tal (DV), inte för vanlig FM.

Sverige har, såvitt jag har kunnat se, ingen av PTS särskilt utpekad nödkanal på amatörbanden. IARU Region 1 anger däremot mötespunkter ("centres of activity") på kortvåg, bland annat 3,760, 7,110 och 14,300 MHz; Sverige är listat där. De är inte exklusiva nödkanaler, och aktiviteten kan ligga runt ±20 kHz. Det är ett annat verktyg än den här lathunden, som handlar om närkommunikation.

**Repeatrar runt Borlänge.** Borlänge Sändareamatörer (SK4BW) publicerar tre 70 cm-repeatrar, alla med −2 MHz skift:

| Typ | Utfrekvens | Infrekvens | Öppning |
| --- | --- | --- | --- |
| Analog FM | 434,800 MHz | 432,800 MHz | CTCSS 85,4 Hz (ingen 1750 Hz-ton) |
| DMR | 434,850 MHz | 432,850 MHz | Color code 12, repeater-ID 240401 |
| D-STAR | 434,900 MHz | 432,900 MHz | R1: SK4BW B, R2: SK4BW G, UR: CQCQCQ |

Klubbens sida beskriver också Svxlink-noden SK4RVN på 434,800 MHz, med koppling mot bland annat SK4RGL i Falun. Repeatrar ändras, så aktuellt läge tar jag från [klubbsidan](https://www.sk4bw.net/repeater/) och SSA:s [repeaterkarta](https://www.ssa.se/ssa/repeatrar-fyrar/). IC-705 klarar både analog FM och D-STAR, vilket passar den lokala D-STAR-repeatern.

Amatörtrafik får inte kodas för att dölja innehållet. Det är öppet, precis som PMR.

## FRO, SSA och vad som inte är en allmän kanal

Frivilliga Radioorganisationen (FRO) är en frivillig försvarsorganisation som utbildar bland annat radiooperatörer till stöd för ledning och samverkan när ordinarie system inte räcker till. Man behöver inte vara radioamatör för att engagera sig där. SSA och de lokala amatörradioklubbarna övar beredskap och kan stödja samhället, men det sker efter överenskommelse och under den ledning som gäller för insatsen.

Det finns alltså organisationer och rutiner för krissamband, men inte en offentlig "kriskanal" som allmänheten förväntas samlas på med PMR eller jaktradio. Planera därför den egna kretsen: familj, grannar eller den grupp du faktiskt ska nå.

Rakel får bara användas av den behöriga användarkrets som har uppgifter inom allmän ordning, säkerhet eller hälsa. Det är inte ett system jag eller andra privatpersoner kan ansluta till.

## Praktiska vanor

**Bestäm i förväg.** Skriv ner och öva:

- vilken typ av radio (PMR446, jaktradio eller amatörradio – de går inte att blanda)
- kanal eller exakt frekvens, och en reservkanal
- subton eller inte (och i så fall vilken)
- när vi lyssnar, till exempel fem minuter vid varje jämn timme
- vad vi säger, och vad vi *inte* säger över en öppen kanal

**Räckvidd.** Den beror mest på terräng och antennhöjd, inte på vad som står på förpackningen. Med PMR på 0,5 W och fast antenn är det i tätort och skog ofta några hundra meter upp till någon kilometer. Med fri sikt, särskilt från en höjd, kan det bli längre. 5 W jaktradio når typiskt längre, men fortfarande begränsas den av kullar, hus och skog. En våning upp, en kulle eller bara att gå ut ur en dal gör mer skillnad än att höja rösten i mikrofonen.

**Antenn och höjd.** På PMR får antennen inte bytas. Då är höjden det som går att påverka: gå uppåt, håll radion lodrätt och undvik att stå bakom en huskropp. På jaktradio och amatörradio gör en bättre antenn och en högre placering stor skillnad. På 2 m och 70 cm kan en liten ytterantenn eller att köra via en repeater förändra täckningen helt.

**Batterier.** Extra batterier är viktigare än extra radioapparater. Ett batterifack för AA-celler är bra när det inte går att ladda. Ladda innan ett avbrott, slösa inte på sändning i onödan, och räkna med att en radio som står och lyssnar dygnet runt tar slut snabbare än man tror. Ett enkelt schema (avstängd mellan lyssningspass) räcker ofta längre.

**Trafikvana.** Lyssna först. Håll PTT inne ett kort ögonblick innan du talar, och släpp när du är klar så att den andra kan svara. Anropa tydligt, till exempel: "Evalena, här är Leif, kom." Håll meddelanden korta och konkreta: var du är, hur du mår, vad du behöver, när du lyssnar nästa gång. Säg namn och platser tydligt, gärna två gånger om det är viktigt. "Uppfattat" räcker som bekräftelse. Avsluta så att den andra vet att du är klar.

**Integritet.** Allt som sägs kan höras av andra. Skicka inte uppgifter som inte tål att bli offentliga: exakta larmuppgifter om tredje person, dörrkoder, och liknande. Subton, digital "privacy" och smutskod på billiga radior är inte kryptering.

## MeshCore och liknande LoRa-nät

Som komplement till röstadio använder jag gärna MeshCore-liknande system: små LoRa-noder som skickar text och position i ett mesh, utan mobilnät. I Sverige är det tillståndsfritt som kortdistansutrustning i 868 MHz-området, förutsatt att man håller sig till rätt delband, effekt och sändningscykel.

Ett vanligt läge, som Meshtastic kallar EU_868, ligger i 869,40–869,65 MHz. Där tillåter PTS högst 500 mW e.r.p. och, om man inte använder annan godkänd teknik för att undvika störning, en sändningscykel på högst 10 procent. Andra delband, till exempel 868,0–868,6 MHz, har lägre effekt (25 mW) och strängare sändningscykel. Region och inställningar måste vara samma hos alla noder som ska höra varandra, och sändningscykeln ska inte kringgås.

Det här ersätter inte röst på komradio. Det är ett bra komplement för korta meddelanden och lägesinformation, särskilt om noderna sitter högt. Precis som övrig tillståndsfri radio är trafiken i grunden något andra kan ta emot.

## Källor

- PTS, *PTSFS 2025:1*, föreskrifter om undantag från tillståndsplikt, bland annat 3 kap. 27, 69–84, 91, 100, 103–104, 109–110, 123–124, 128 och 141–149 §§. Gäller från 17 mars 2025: [föreskriften](https://pts.se/regelbibliotek/foreskrifter-ptsfs-20251-om-undantag-fran-tillstandsplikt-for-anvandning-av-vissa-radiosandare/)
- CEPT, [ECC/DEC/(15)05](https://docdb.cept.org/download/b8797390-4577/ECCDec1505.pdf) om PMR446 (kanalplan, 500 mW, handhållen radio med integrerad antenn)
- SSA, [bandplan 144–146 MHz](https://www.ssa.se/vushf/wp-content/uploads/sites/12/2020/11/144-MHz.pdf) (2020-11-26) och [bandplan 432–438 MHz](https://www.ssa.se/vushf/wp-content/uploads/sites/12/2024/06/432-MHz.pdf) (2024-04-08), baserade på IARU Region 1
- IARU Region 1, [Emergency Communications Frequencies](https://www.iaru-r1.org/about-us/committees-and-working-groups/emcomm/emergency-communications-frequencies/)
- SSA, [Repeatrar & fyrar](https://www.ssa.se/ssa/repeatrar-fyrar/) (repeaterkarta), och [SK4BW:s repeatersida](https://www.sk4bw.net/repeater/)
- Myndigheten för civilt försvar, [Vilka kan ansluta till Rakel](https://www.mcf.se/sv/amnesomraden/samhallsviktiga-kommunikationstjanster/rakel/anslut-till-rakel/vilka-kan-ansluta-till-rakel/)
- FRO, [Radiooperatör](https://fro.se/radiooperator/)
- ITU Radioreglementet, artikel 25 (amatörtjänsten; sändningar ska inte kodas för att dölja innebörden)
- Meshtastic, [LoRa-konfiguration / region EU_868](https://meshtastic.org/docs/configuration/radio/lora/), tillsammans med PTSFS 2025:1, 146 §

Villkoren kan ändras. Kontrollera alltid gällande text hos PTS innan du köper eller sänder.
