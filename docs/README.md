# [A] MOTIVACE


### 1. TEORIE (strucne)
Rezervoary na vodu napriklad do subtropickych oblasti jsou vyrabeny z kompozitnich materialu (20 vrstev skelnych vlaken prosycenych pryskyrici). Tyto zasobniky mivaji ve svem tele technologicke otvory (napr. cistici vypust), ktere jsou po ulozeny do zeme a obsypani zeminou vystaveny zatizeni, ktere v materialu vyvolava deformaci.
K dispozi mame kompozitovou desku (80x40) s technologickym prostupem. V okoli otvoru byl ve trech radach nalepen snimac deformace, kterym je opticke vlakno.
Rize deformace desky byla provedena na zatezovacim stroji uzitim ctyrbodoveho ohybu. Merici metodou byla opticka reflektometrie v casove oblasti, ktera uziva laserovych impulsu.
Pomoci simulovaneho namahani na zatezovacim stroji se chceme dozvedet, jak bude vypadat deformace v okoli kruhoveho otvoru, ktery se bude chovat jako koncentrator napeti.

### 2. NAMERENA DATA
   pozn. Namerena data jsou ulozena v datovem formatu TSV (Tab-Separated-Value, Tabulatorem oddelene hodnoty)

   ### *** Hlavicka souboru ***
   Soubor `./data/BP_4_down_static_loading_2024-04-23_15-23-32_ch1_full.tsv` obsahuje data z mereni.
- "*down/up*" -  oznacuje merenou stranu desky
- "*static/cyclic*" - zatezovaci rezim mereni (<ins>static</ins>: 0 - 10 kN, <ins>cyclic</ins>: 5x 0 - 1 kN)
- "*Measurement Rate Per Channel*" - merici frekvence (pro 10 Hz znamena zaznam kazdych 0,1 s)
- "*Gage Pitch (mm)*" - nejvyse dosazitelna merici citlivost, tedy nejmensi vzdalenost mericich bodu v optickem vlakne
- "*Length (m)*" - celkova delka senzorickeho vlakna
- "*Units (microstrain)*" - microstrain je jednotka deformace

   ### *** Data ***
- "*Prvni radek*" - namerenych dat obsahuje informaci o poloze jednotlivych mericich bodu v senzorickem vlakne ve vzdalenosti od merici centraly (vzdalenost bodu 2,6 mm)

- "*Nasledujici radky:*"
   1. sloupec        -> datum mereni
   2. sloupec        -> cas mereni
   3. sloupec        -> slovo "measurement"
   4. sloupec        -> slovo "strain"
   5. sloupec a dale -> namerena hodnota deformace pro dany merici bod v konkretnim case  
  

    pozn.
    - vybrany radek obsahuje informaci o mire deformace podel senzorickeho vlakna v jednom konkretnim case mereni
    - vybrany sloupec obsahuje informaci o prubehu deformace v case v jednom konkretnim mericim bode


### 3. PRUBEH MERENI

Mereni probehlo na zatezovacim stroji v laboratorich FS CVUT v Praze v Dejvicich.
Jednalo se o ctyrbodovy ohyb.

# [B] Software
- Program Stress Measurement Viewer poskytuje uzivateli jednoduchy graficky nahled namerenych dat, nalezeni vyznamnych oblasti (pro dalsi analyzu) a orezani nepotrebnych dat.
- Strucny navod, jak pouzivat program, se naleza v souboru `./how_to.html`
- programek "Stress Measurement Viewer" verze 1.0 je napsan v jazyce Python v3.11
- pouziva knihovny:
  - numpy
  - matplotlib
  - pyQt


    Jak spustit? V prikazovem radku se odnavigujte do aresare, kde je skript "app.py" a pote spuste prikaz 'python app.py'
   

2. GRAFY
- **Zavislost deformace na poloze**
    - osa x: vzdalenost mericiho bodu v optickem vlakne od merici centraly vysilajici laserovy impuls [metr]
    - osa y: deformace [microstrain]
    - posuvnik: umoznuje prochazet casovym zaznamem mereni

