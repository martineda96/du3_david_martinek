from funkce import *
from statistics import mean, median

MAX_VZDALENOST = 10000

#nahrani souboru
adresa = otevreni_souboru("adresy.geojson")
kontejnery = otevreni_souboru("kontejnery.geojson")

kontejnery_volne = []
pocet_kontejneru = 0
for koš in kontejnery["features"]:
    if koš ["properties"]["PRISTUP"] != "obyvatelům domu":
        kontejnery_volne.append(koš)
        pocet_kontejneru += 1
#prevod adres do S-JTSK

#cyklus - pro kazdou adresu najit nejblizsi kontejner

#prirazeni kontejneru k adresam (tvorba vystupniho souboru)

#domovni kontejnery? (bonus)

# prumer + median? (bonus)

#vystup (printy)

print(f"Načteno {pocet_kontejneru} volných kontejnerů na tříděný odpad.")