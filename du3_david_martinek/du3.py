from funkce import *
from statistics import mean, median

MAX_VZDALENOST = 10000

#nahrani souboru
adresy = otevreni_souboru("adresy.geojson")
kontejnery = otevreni_souboru("kontejnery.geojson")

#Vytvoření seznamu volně přístupných kontejnerů
kontejnery_volne = []
pocet_kontejneru = 0
for kos in kontejnery["features"]:
    if kos ["properties"]["PRISTUP"] != "obyvatelům domu":
        kontejnery_volne.append(kos)
        pocet_kontejneru += 1

#Definice proměnných použitých v cyklu
maximalni_vzdalenost = 0
vzdalenost_soucet = 0
adresy_seznam = []

#Cyklus pro hledání nejbližšího kontejneru
for adresa in adresy["features"]:
    nejkratsi_vzdalenost = float('inf')
    adresa_id = adresa ["properties"]["@id"]
    adresa_ulice = adresa ["properties"]["addr:street"]
    adresa_cp = adresa ["properties"]["addr:housenumber"]
    
    #Převod adres do S-JTSK (z WGS84)
    x_adresa,y_adresa = adresa ["geometry"]["coordinates"]
    x_adresa,y_adresa = zmena_projekce(x_adresa,y_adresa)

    #Kontrola jednotlivých kontejnerů a výpočet vzdálenosti
    for kos in kontejnery_volne:
        x_kos,y_kos = kos ["geometry"]["coordinates"]
        vzdalenost = vypocet_vzdalenosti(x_adresa,x_kos,y_adresa,y_kos)
        if vzdalenost < nejkratsi_vzdalenost:
            nejkratsi_vzdalenost = vzdalenost
            kontejner_id = kos ["properties"]["ID"]
    
    #Shození programu v případě, že je nejbližší kontejner k adrese vzdálen více než 10 km
    if nejkratsi_vzdalenost > MAX_VZDALENOST:
        print(f"Bod: {adresa_id} na adrese {adresa_ulice} {adresa_cp} má nejbližší kontejner dále než 10 km.\
            Program končí.")
        quit()
    
    #Hledání maximální vzdálenosti pro nejbližší kontejner
    if nejkratsi_vzdalenost > maximalni_vzdalenost:
        maximalni_vzdalenost = nejkratsi_vzdalenost
        adresa_ulice_max = adresa_ulice
        adresa_cp_max = adresa_cp
    
    vzdalenost_soucet += nejkratsi_vzdalenost
    adresy_seznam.append(nejkratsi_vzdalenost)

nejkratsi_vzdalenost_prumer = vzdalenost_soucet/len(adresy_seznam)
nejkratsi_vzdalenost_median = median(adresy_seznam)
#vystup (printy)
print(f"Načteno {len(adresy_seznam)} adresních bodů.")
print(f"Načteno {pocet_kontejneru} volných kontejnerů na tříděný odpad.")
print(f"\nPrůměrná vzdálenost ke kontejneru je {nejkratsi_vzdalenost_prumer:.0f} m.")
print(f"Nejdale ke kontejneru je z adresy {adresa_ulice_max} {adresa_cp_max} a to {maximalni_vzdalenost:.0f} m.")
print(f"Medián nejkratších vzáleností ke kontejneru je {nejkratsi_vzdalenost_median:.0f} m.")