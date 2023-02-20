import argparse
from funkcje import *

parser = argparse.ArgumentParser()
parser.add_argument("sciezka_emisja", help="Sciezka do pliku csv (Emisja CO2)")
parser.add_argument("sciezka_GDP", help="Sciezka do pliku csv (GDP)")
parser.add_argument("sciezka_populacja", help="Sciezka do pliku csv (populacja)")
parser.add_argument("start_rok", help="Poczatek badanych lat")
parser.add_argument("koniec_rok", help="Koniec badanych lat")
args = parser.parse_args()

# wczytanie dataframow
emisja = czytaj_plik(args.sciezka_emisja, "fossil-fuel-co2-emissions-by-nation.csv")
gdp = czytaj_plik(args.sciezka_GDP, "API_NY.GDP.MKTP.CD_DS2_en_csv_v2_4751562.csv")
populacja = czytaj_plik(args.sciezka_populacja, "API_SP.POP.TOTL_DS2_en_csv_v2_4751604.csv")

# usuniecie ostatnich kolumn, w ktorych nic nie bylo
del populacja[populacja.columns[-1]]
del gdp[gdp.columns[-1]]

# tworzenie dwoch list: lista lat, ktore podal uzytkownik oraz lista lat wspolnych w 3 dataframach.
lata_podane = przedzial_lat(args.start_rok, args.koniec_rok)
lata_wspolne_tabele = wspolne_lata(emisja, gdp, populacja)
lata_wspolne_str = przeciecie2(lata_podane, lata_wspolne_tabele)
lata_wspolne_str.sort()

# sprawdzamy czy lista jest pusta, jesli tak to informujemy i konczymy.
if len(lata_wspolne_str) == 0:
    print("przedzial lat pusty")
    exit()

# W dataframe populacja, gdp mamy kolumny liczac od 4 z danym rokiem, tworzymy liste wszystkich lat.
populacja_lata = populacja.columns[4:].tolist()
gdp_lata = gdp.columns[4:].tolist()
# tworzymy listy lat, ktore sa w kolumnach dataframow (populacja, gdp), ale nie sa we wszystkich dataframach.
kol_usun_pop = roznica_ab(populacja_lata, lata_wspolne_str)
kol_usun_gdp = roznica_ab(gdp_lata, lata_wspolne_str)
lata_wspolne_int = [int(i) for i in lata_wspolne_str]
# Zostawiamy tylko te lata, ktore sa we wszystkich dataframach (emisja, gdp, populacja)
emisja = emisja[emisja['Year'].isin(lata_wspolne_int)]
gdp = gdp.drop(kol_usun_gdp, axis=1)
populacja = populacja.drop(kol_usun_pop, axis=1)

populacja['Country Name'] = populacja['Country Name'].str.upper()
gdp['Country Name'] = gdp['Country Name'].str.upper()


# Dla wspolnych lat tworzymy dla kazdej dataframe liste dataframow dla kazdego roku oddzielnie
tabele_populacja = lista_tabel_kraj_rok(populacja, lata_wspolne_str)
tabele_gdp = lista_tabel_kraj_rok(gdp, lata_wspolne_str)
tabele_emisja = []
for i in range(len(lata_wspolne_int)):
    tabele_emisja.append(emisja[emisja['Year'] == lata_wspolne_int[i]])


zmiana_nazwy(tabele_populacja, 'Population')
zmiana_nazwy(tabele_gdp, 'GDP')

# Lista dataframow dla kazdego roku oddzielnie, z infomacja o emisji, populacji i gdp
tabele_emisja_pop_gdp = lista_tabel_polacz(tabele_emisja, tabele_populacja, tabele_gdp)

# Laczenie wszystkich dataframow w liscie tabele_emisja_pop_gdp w jeden dataframe.
df_emisja_pop_gdp = pd.concat(tabele_emisja_pop_gdp)
print(df_emisja_pop_gdp)

# Dataframe z krajami w poszczegolnych latach, ktore produkuja najwiecej CO2 na mieszkanca.
df_najwiecej_co2 = tabela_najwiecej_co2(tabele_emisja)
print(df_najwiecej_co2)

# Dataframe z krajami w poszeczegolnych latach, ktore maja najwiekszy przychod na mieszkanca.
df_najwiekszy_przychod = tabela_najwiekszy_przychod(tabele_emisja_pop_gdp)
print(df_najwiekszy_przychod)

roznica_max_min(emisja, lata_wspolne_int)
