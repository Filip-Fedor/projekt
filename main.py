import argparse
import pandas as pd
import os
from funkcje import *

parser = argparse.ArgumentParser()
parser.add_argument("sciezka_emisja", help="Sciezka do pliku csv (Emisja CO2)")
parser.add_argument("sciezka_GDP", help="Sciezka do pliku csv (GDP)")
parser.add_argument("sciezka_populacja", help="Sciezka do pliku csv (populacja)")
args = parser.parse_args()


emisja = czytaj_plik(args.sciezka_emisja, "fossil-fuel-co2-emissions-by-nation.csv")
gdp = czytaj_plik(args.sciezka_GDP, "API_NY.GDP.MKTP.CD_DS2_en_csv_v2_4751562.csv")
populacja = czytaj_plik(args.sciezka_populacja, "API_SP.POP.TOTL_DS2_en_csv_v2_4751604.csv")


del populacja[populacja.columns[-1]]
del gdp[gdp.columns[-1]]

lata_wspolne = wspolne_lata(emisja, gdp, populacja)
populacja_lata = populacja.columns[4:].tolist()
gdp_lata = gdp.columns[4:].tolist()
kol_usun_pop = roznica_ab(populacja_lata, lata_wspolne)
kol_usun_gdp = roznica_ab(gdp_lata, lata_wspolne)
lata_wspolne = [int(i) for i in lata_wspolne]
emisja = emisja[emisja['Year'].isin(lata_wspolne)]
gdp = gdp.drop(kol_usun_gdp, axis=1)
populacja = populacja.drop(kol_usun_pop, axis=1)

print(emisja)
print(populacja)
print(gdp)
