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

lata_wspolne_str = wspolne_lata(emisja, gdp, populacja)
populacja_lata = populacja.columns[4:].tolist()
gdp_lata = gdp.columns[4:].tolist()
kol_usun_pop = roznica_ab(populacja_lata, lata_wspolne_str)
kol_usun_gdp = roznica_ab(gdp_lata, lata_wspolne_str)
lata_wspolne_int = [int(i) for i in lata_wspolne_str]
emisja = emisja[emisja['Year'].isin(lata_wspolne_int)]
gdp = gdp.drop(kol_usun_gdp, axis=1)
populacja = populacja.drop(kol_usun_pop, axis=1)

populacja['Country Name'] = populacja['Country Name'].str.upper()
gdp['Country Name'] = gdp['Country Name'].str.upper()
kraje_wspolne = wspolne_kraje(emisja, gdp, populacja)
emisja = emisja[emisja['Country'].isin(kraje_wspolne)]
populacja = populacja[populacja['Country Name'].isin(kraje_wspolne)]
gdp = gdp[gdp['Country Name'].isin(kraje_wspolne)]

tabele_populacja = lista_tabel_kraj_rok(populacja, lata_wspolne_str)
tabele_gdp = lista_tabel_kraj_rok(gdp, lata_wspolne_str)
tabele_emisja = []
for i in range(len(lata_wspolne_int)):
    tabele_emisja.append(emisja[emisja['Year'] == lata_wspolne_int[i]])
zmiana_nazwy(tabele_populacja, 'Population')
zmiana_nazwy(tabele_gdp, 'GDP')

tabele_emisja_pop_gdp = lista_tabel_polacz(tabele_emisja, tabele_populacja, tabele_gdp)

df_emisja_pop_gdp = pd.concat(tabele_emisja_pop_gdp)

print(df_emisja_pop_gdp)
