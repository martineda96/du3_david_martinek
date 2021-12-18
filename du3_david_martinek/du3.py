from funkce import *
from statistics import median

#Otevření vstupních souborů
adresy = otevreni_souboru("adresy.geojson")
kontejnery = otevreni_souboru("kontejnery.geojson")

#Vytvoření seznamu volně přístupných kontejnerů
kontejnery_volne = []
for kos in kontejnery["features"]:
    if kos ["properties"]["PRISTUP"] != "obyvatelům domu":
        kontejnery_volne.append(kos)

#Definice proměnných použitých v cyklu
MAX_VZDALENOST = 10000
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
    try:
        x_adresa,y_adresa = adresa ["geometry"]["coordinates"]
        x_adresa,y_adresa = zmena_projekce(x_adresa,y_adresa)
    except ValueError:
        print(f"Bod {adresa_id} na adrese {adresa_ulice} {adresa_cp} nemá platně zadané souřadnice.")
        quit()
    except KeyError:
        print(f"Bod {adresa_id} na adrese {adresa_ulice} {adresa_cp} nemá informaci o souřadnicích ve správném formátu.")
        quit()

    #Kontrola jednotlivých kontejnerů a výpočet vzdálenosti
    try:
        for kos in kontejnery_volne:
            x_kos,y_kos = kos ["geometry"]["coordinates"]
            kontejner_id = kos ["properties"]["ID"]
            vzdalenost = vypocet_vzdalenosti(x_adresa,x_kos,y_adresa,y_kos)
            if vzdalenost < nejkratsi_vzdalenost:
                nejkratsi_vzdalenost = vzdalenost
    except ValueError:
        print(f"Kontejner {kontejner_id} nemá platně zadané souřadnice.")
        quit()
    except KeyError:
        print(f"Kontejner {kontejner_id} nemá informaci o souřadnicích ve správném formátu.")
        quit()
        
    #Ukončení programu v případě, že je nejbližší kontejner k adrese vzdálen více než 10 km
    if nejkratsi_vzdalenost > MAX_VZDALENOST:
        print(f"Bod: {adresa_id} na adrese {adresa_ulice} {adresa_cp} má nejbližší kontejner dále než 10 km.\
            Program končí.")
        quit()
        
    #Hledání maximální vzdálenosti pro nejbližší kontejner
    if nejkratsi_vzdalenost > maximalni_vzdalenost:
        maximalni_vzdalenost = nejkratsi_vzdalenost
        adresa_ulice_max = adresa_ulice
        adresa_cp_max = adresa_cp
    
    #Přidání klíče kontejner do souboru
    adresy_prirazene = adresa ["properties"]
    adresy_prirazene["kontejner"] = kontejner_id
    adresa ["properties"] = adresy_prirazene

    
    vzdalenost_soucet += nejkratsi_vzdalenost
    adresy_seznam.append(nejkratsi_vzdalenost)

#Vytvoření GeoJSON souboru, kde adresy mají přiřazený nejbližší kontejner v podobě ID
with open("adresy_kontejnery.geojson", "w", encoding="utf-8") as fp:
    json.dump(adresy, fp)

#Textové výstupy informující uživatele o výsledcích programu a jim předcházející výpočty
nejkratsi_vzdalenost_prumer = vzdalenost_soucet/len(adresy_seznam)
nejkratsi_vzdalenost_median = median(adresy_seznam)

print(f"Načteno {len(adresy_seznam)} adresních bodů.")
print(f"Načteno {len(kontejnery_volne)} volných kontejnerů na tříděný odpad.")
print(f"\nPrůměrná vzdálenost ke kontejneru je {nejkratsi_vzdalenost_prumer:.0f} m.")
print(f"Nejdale ke kontejneru je z adresy {adresa_ulice_max} {adresa_cp_max} a to {maximalni_vzdalenost:.0f} m.")
print(f"Medián nejkratších vzáleností ke kontejneru je {nejkratsi_vzdalenost_median:.0f} m.")