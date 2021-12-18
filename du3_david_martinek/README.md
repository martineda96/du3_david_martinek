Vzdálenost ke kontejnerům na tříděný odpad

Úkolem programu je zjistit nejkratší euklidovskou vzdálenost z domovní adresy ke kontejneru na tříděný odpad. 

Program pracuje s bodovou vrstvou domovních adres (http://overpass-turbo.eu/) a kontejnerů na tříděný odpad
(https://www.geoportalpraha.cz/cs/data/otevrena-data/8726EF0E-0834-463B-9E5F-FE09E62D73FB) v koordinačním
systému S-JTSK - zajišťuje převod vrstvy domovních adres z WGS84. Dále zohledňuje pouze veřejně dostupné
kontejnery. Program prostřednictvím Pythagorovy věty spočítá vzdálenost každé adresy ke každému kontejneru a jako výstup
bere v potaz tu nejkratší. Program se sám ukončí, je-li jako nejbližší kontejner vyhodnocen ten, který je vzdálen více 
než 10 km od právě řešené adresy.

Výstupem programu je soubor 'adresy_kontejnery.geojson', ve kterém je ke každé adrese ve slovníku 'properties' přiřazen
v podobě ID nejbližší kontejner. Dále program vypíše četnost domovních adres a kontejnerů účastnících se výpočtů. Na 
závěr je uživatel v textové podobě informován o průměrné vzdálenosti k nejbližšímu kontejneru, mediánu nejkratších
vzdáleností ke kontejneru a nejdelší vzdálenost k nejbližšímu kontejneru, přičemž je uvedeno, které adresy se to týká.

V případě nastalé výjimky program informuje uživatele o komplikacích a ukončí se.

- David Martínek (18.12.2021)