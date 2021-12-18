from json.decoder import JSONDecodeError
from math import sqrt
import json
from pyproj import Transformer

def vypocet_vzdalenosti(x_adresa,x_kontejner,y_adresa,y_kontejner):
    return sqrt((x_adresa-x_kontejner)*(x_adresa-x_kontejner)+(y_adresa - y_kontejner)*(y_adresa - y_kontejner))

def otevreni_souboru(soubor):
    try:
        with open(soubor, encoding="utf-8") as vstup:
            return json.load(vstup)
    except FileNotFoundError:
        print(f"Soubor {soubor} se nepodařilo otevřít. Opravte vstup nebo cestu k souboru. Program se nyní vypne.")
        quit()
    except JSONDecodeError:
        print(f"Soubor {soubor} obsahuje chybné nebo žádné hodnoty nebo se nejedná o platný JSON soubor.")
        quit() 

def zmena_projekce(x_souradnice,y_souradnice):
    transformace = Transformer.from_crs(4326,5514, always_xy=True)
    poloha_xy = transformace.transform(x_souradnice,y_souradnice)
    return poloha_xy
    
