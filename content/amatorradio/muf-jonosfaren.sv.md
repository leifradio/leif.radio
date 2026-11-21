+++
title = "MUF och hur jonosfären fungerar"
url = "/om/amatorradio/muf-och-jonosfaren/"
aliases = ["/about/amatorradio/muf-och-jonosfaren/", "/om/amatorradio/muf/"]
description = "En genomgång av jonosfärens skikt, MUF, LUF och FOT, och vad det betyder för 20, 40 och 80 meter från Sverige."
weight = 10
showDate = false
showAuthor = false
showReadingTime = false
showPagination = false
showDateUpdated = false
showHero = false
showTableOfContents = true
+++

När vi kör HF – alltså kortvåg, ungefär 1,8 till 30 MHz – kan radiovågorna böjas tillbaka i jonosfären och nå andra sidan jorden. Hur långt de når, och på vilket band, beror på hur jonosfären ser ut just då. Här försöker jag förklara de begrepp som oftast kommer upp, till exempel MUF, och hur de hänger ihop med det jag själv ser när jag kör från Borlänge (JP70).

## Jonosfärens skikt

Jonosfären är den del av den övre atmosfären där solen slår loss elektroner från gaserna, så att luften blir elektriskt ledande. Det är den ledande luften som kan böja av en radiovåg tillbaka mot jorden. Utan den böjningen skulle HF-vågen bara fortsätta ut i rymden.

Man talar oftast om fyra skikt, efter ungefärlig höjd:

**D-skiktet**, ungefär 60–90 km upp, finns i stort sett bara på dagen. Det absorberar lägre HF-frekvenser – särskilt 160 meter, 80 meter och delvis 40 meter – så att längre förbindelser på de banden blir svåra medan solen står högt. När solen går ner rekombinerar elektronerna snabbt och D-skiktet försvinner nästan helt. Det är en viktig anledning till att 80 och 40 meter vaknar till liv på kvällen.

**E-skiktet**, ungefär 90–150 km, är också starkast på dagen. Det kan ge kortare hopp, och ibland uppträder så kallad sporadisk E, som plötsligt kan öppna högre band över oväntat korta avstånd. På natten försvagas E-skiktet kraftigt.

**F1- och F2-skikten** sitter högst. F1, ungefär 150–250 km, syns främst på dagen och smälter på natten samman med F2. **F2-skiktet**, typiskt 250–400 km och ibland högre, är det viktigaste för långväga HF. Det finns både dag och natt. På dagen är elektrontätheten högst, och högre frekvenser kan böjas tillbaka. På natten sjunker tätheten och de högsta banden stänger ofta, men F2 finns kvar och bär fortfarande 40 meter och, beroende på årstid och solcykel, ibland 20 meter.

{{< figure src="/img/ionosphere-sv.svg" alt="Schematisk bild av jonosfärens D-, E-, F1- och F2-skikt, med markvåg, död zon och en rymdvåg som böjs tillbaka i F2-skiktet" caption="Jonosfärens skikt och ett typiskt HF-hopp. Höjderna i bilden är inte skalenliga." >}}

## Solcykeln, solflöde och solfläckar

Solens aktivitet varierar i en cykel på ungefär elva år. Fler solfläckar betyder i regel mer ultraviolett strålning och röntgenstrålning, som i sin tur bygger upp jonosfären starkare, särskilt F2. Då stiger de frekvenser som kan användas för långväga trafik, och band som 15 och 10 meter öppnar oftare.

Två tal dyker ständigt upp i rymdväderrapporter:

- **Solflödet** (SFI, Solar Flux Index) mäts vid 10,7 cm våglängd (2 800 MHz) och är ett praktiskt mått på solens aktivitet, även när det inte syns några fläckar. Högre solflöde brukar betyda högre MUF.
- **Solfläckstalet** (SSN, sunspot number) räknas från fläckarna på solskivan. Det följer samma cykel och används mycket i äldre tabeller och prognosmodeller.

Båda är indikatorer, inte garantier. Ett högt solflöde ger bättre förutsättningar, men tid på dygnet, årstid, geomagnetiskt läge och den aktuella vägen betyder minst lika mycket.

## MUF, LUF och FOT

Tre förkortningar beskriver vilket frekvensfönster som faktiskt går att använda mellan två platser vid en given tid:

- **MUF**, Maximum Usable Frequency, är den högsta frekvens som just då kan bära en förbindelse den vägen via jonosfären. Strax ovanför MUF tränger vågen igenom F-skiktet och försvinner ut i rymden. MUF gäller en viss väg och tid – den är inte ett enda tal för hela jorden.
- **LUF**, Lowest Usable Frequency, är den lägsta frekvens som fortfarande ger en användbar signal. Under LUF äts signalen upp av absorption, framför allt i D-skiktet, eller drunknar i brus.
- **FOT**, Frequency of Optimum Traffic, ibland kallad optimum working frequency, är den frekvens man i praktiken ofta siktar på. En vanlig tumregel är ungefär 85 procent av MUF. Precis under MUF kan förbindelsen slå om och försvinna, så en bit marginal gör trafiken mer pålitlig.

**Kritisk frekvens**, foF2, är den högsta frekvens som studsar rakt upp och tillbaka från F2-skiktet. Den mäts med jonosonder, som skickar en puls lodrätt och lyssnar efter eko. foF2 är alltså MUF för en helt vertikal väg, och den är lägre än MUF för ett långt DX-hopp.

Sambandet kallas ibland **sekantlagen**. En våg som går snett in i jonosfären färdas en längre väg genom skiktet än en som går rakt upp, och böjs därför tillbaka även på en högre frekvens. Enkelt uttryckt: ju flackare vinkel mot skiktet (längre hopp, låg utstrålningsvinkel), desto högre MUF för den vägen. Formellt brukar man skriva att MUF är ungefär foF2 gånger sekanten för infallsvinkeln, räknat från lodlinjen. Därför kan man ha DX på 20 eller 15 meter även när den lokala foF2 ligger en bit under bandets frekvens.

## Skip och död zon

En HF-våg som lämnar antennen kan följa marken en bit (markvåg) och samtidigt gå upp mot jonosfären och komma ner igen längre bort (rymdvåg). Avståndet till första nedslagspunkten för rymdvågen kallas hopplängd eller skip distance.

Mellan slutet på markvågen och första rymdvågsnedslaget finns en **död zon** (skip zone) där stationen inte hörs, eller hörs mycket svagt. På högre band, till exempel 20 meter, kan den zonen vara flera hundra kilometer. Det är därför en station i södra Sverige eller norra Tyskland ibland kan vara svårare att nå från Borlänge på 20 meter än en station i södra Europa eller på andra sidan Atlanten. På lägre band, och när MUF är låg, kan vågen komma ner redan på kortare avstånd – det som ofta kallas NVIS, när antennen strålar brant uppåt och täcker närområdet.

## 20 meter på dagen, 40 och 80 på kvällen

Sett från Sverige, och från mitt QTH i JP70, är dygnsrytmen ofta tydlig.

**20 meter** (14 MHz) är i första hand ett dagsband. På dagen ligger MUF ofta tillräckligt högt för att 14 MHz ska böjas tillbaka i F2, och D-skiktet absorberar inte 20 meter lika hårt som de lägre banden. På förmiddagen öppnar det gärna österut och söderut, mot Asien och Afrika, och på eftermiddagen mer västerut, mot Nordamerika. På kvällen och natten sjunker MUF. Nära solfläcksmaximum kan 20 meter hålla sig öppet längre, men i tystare perioder och mitt i vintern stänger det ofta när det blir mörkt.

**40 meter** (7 MHz) och **80 meter** (3,5 MHz) beter sig tvärtom. På dagen dämpar D-skiktet, så räckvidden blir mest regional. När solen sjunker försvinner absorptionen, och längre vägar öppnar sig. Från Borlänge är 40 meter typiskt ett band för sen eftermiddag, kväll och natt – Europa först, sedan längre DX när det blivit mörkt längs vägen. 80 meter påverkas ännu mer av dagsabsorption och är i praktiken ett kvälls- och nattband, särskilt vintertid då nätterna är långa och det atmosfäriska bruset lägre än på sommaren.

Det är en tumregel, inte en lag. Årstid, solcykel och geomagnetiskt läge flyttar fönstren, och en enskild dag kan se annorlunda ut.

## Kp, A-index och störningar

Solen skickar inte bara den strålning som bygger upp jonosfären. Den kan också störa den.

**Kp-index** är ett planetariskt mått på geomagnetisk aktivitet, från 0 till 9, i tretimmarsperioder. **A-index** är ett dygnsvärde räknat från samma underlag. Låga värden betyder lugnt läge. När Kp stiger störs jordens magnetfält, och jonosfären – särskilt på högre breddgrader – kan bli orolig. foF2 sjunker ofta, signaler kan fäda, alltså variera snabbt i styrka, och vägar som går nära de magnetiska polerna blir opålitliga. NOAA beskriver de kraftigare händelserna på en G-skala, från G1 till G5.

Det spelar roll här i Sverige. Borlänge ligger på ungefär 60 grader nord, alltså betydligt närmare auroralzonen än till exempel en station i södra Europa. Samma geomagnetiska storm som knappt märks vid Medelhavet kan göra HF från Dalarna stökig, särskilt mot Nordamerika och Asien.

En annan typ av avbrott kommer från **röntgenutbrott** på solen. De förstärker D-skiktet på jordens dagsida och kan ge plötslig absorption, särskilt på de lägre HF-banden. NOAA kallar det radio blackouts och graderar dem R1 till R5. Ett sådant avbrott följer med solen: det märks när vi har dagsljus och släpper när utbrottet är över, ofta inom minuter till någon timme. Separat finns också protonhändelser som kan ge absorption över polarområdena, så kallad polar cap absorption.

## Greyline

Greyline, eller grålinjen, är övergångszonen mellan dag och natt längs jordens terminator. Precis där är D-skiktet på väg att försvinna i skymningen, eller har inte hunnit byggas upp än i gryningen, medan F-skiktet fortfarande kan vara förhållandevis starkt. Det kan ge ovanligt goda, ibland långa, öppningar särskilt på 40, 80 och 160 meter.

I praktiken betyder det att slutet av gryningen och början av skymningen är tider värda att lyssna extra noga, inte minst mot motsatta sidan av jorden längs den aktuella grålinjen. Öppningen kan vara kort.

## Var man tittar i praktiken

Jag tittar själv på några öppna källor när jag vill veta hur läget är:

- [KC2G:s MUF-karta](https://prop.kc2g.com/) visar en nästan realtidsbild av foF2 och MUF, byggd på mätningar från jonosonder. Den är bra för att se om 20 meter över huvud taget bör kunna gå, och åt vilket håll.
- [NOAA Space Weather Prediction Center](https://www.swpc.noaa.gov/) publicerar solflöde, solfläckstal, Kp och prognoser, samt skattningar av [D-skiktsabsorption](https://www.swpc.noaa.gov/products/d-region-absorption-predictions-d-rap). Deras rymdväder är samma underlag som jag använder när jag skriver om HF-läget här på sidan.
- [Reverse Beacon Network (RBN)](https://www.reversebeacon.net/) är ett nät av automatiska lyssnarstationer, skimmers, som rapporterar CW (och en del andra mode) de hör. Genom att söka på den egna anropssignalen ser man var man faktiskt hördes, på vilket band och med vilken signalstyrka. Det är ett av de rakaste sätten att stämma av teorin mot verkligheten.

Kartor och index ger en ram. Det som avgör är ändå om någon hörs i luren – och RBN är ofta den bro jag använder mellan prognos och det jag själv sänder.
