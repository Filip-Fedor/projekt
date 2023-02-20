import pandas as pd
import os


# Dostaje sciezke do pliku oraz nazwe pliku csv i zwraca dataframe
def czytaj_plik(sciezka, nazwa_pliku):
    polacz_sciezke = os.path.join(sciezka, nazwa_pliku)
    if nazwa_pliku == "fossil-fuel-co2-emissions-by-nation.csv":
        return pd.read_csv(polacz_sciezke)
    else:
        return pd.read_csv(polacz_sciezke, skiprows=4)


# Zwraca przeciecie 2 list
def przeciecie2(a, b):
    return list(set(a) & set(b))


# zwraca przeciecie 3 list
def przeciecie3(a, b, c):
    return list(set(a) & set(b) & set(c))


# Mamy 2 listy a i b.
# Zwraca liste elementow ktore sa w a ale nie sa b.
def roznica_ab(a, b):
    c = []
    for el in a:
        if el not in b:
            c.append(el)
    return c


# Mamy 2 liczby typu str (start, koniec)
# Zwraca liste z intow w przedziale [int(start), int(koniec)]
def przedzial_lat(start, koniec):
    lata = []
    for i in range(int(start), int(koniec)+1):
        lata.append(str(i))
    return lata


# Mamy 3 dataframy: emisja, gdp, populacja
# Z df emisji wybieramy wszystkie wiersze z kolumny Year, czyli wszystkie lata, ktore sie znajduja w dataframie.
# Dataframy: populacja, gdp maja kolumny: Country Name, Country Code, Indicator Name, Indicator Code, a pozniej kolumny z latami.
# Wybieramy wszystkie kolumny z latami i wrzucamy do listy.
# Na koncu przecinamy wszystkie 3 listy, aby dostac lata, ktore sa we wszystkich dataframach i sortujemy.
def wspolne_lata(emisja, gdp, populacja):
    emisja_lata = emisja['Year'].tolist()
    emisja_lata = list(dict.fromkeys(emisja_lata))
    emisja_lata = [str(i) for i in emisja_lata]
    populacja_lata = populacja.columns[4:].tolist()
    gdp_lata = gdp.columns[4:].tolist()
    lata_wspolne = przeciecie3(emisja_lata, populacja_lata, gdp_lata)
    lata_wspolne.sort()
    return lata_wspolne



# Mamy dataframe tabela, ktora zawiera kolumny: Country Name oraz kolumny z latami, ktore sa tez w liscie lata_wspolne
# Zwraca liste dataframow z nazwa kolumny: Country Name, w ktorej sa nazwy panstw, oraz z rokiem.
def lista_tabel_kraj_rok(tabela, lata_wspolne):
    lista_tabel = []
    for i in range(len(lata_wspolne)):
        lista_tabel.append(tabela[['Country Name', lata_wspolne[i]]])
    return lista_tabel


# Zamiana nazwy kolumny w dataframach z listy lista_tabel.
def zmiana_nazwy(lista_tabel, nazwa):
    for i in range(len(lista_tabel)):
        lista_tabel[i].columns = ['Country', nazwa]


# Dla 3 list jednakowej dlugosci, ktore zawieraja dataframy, ktore maja taka sama nazwe kolumny Country,
# laczymy je po tej kolumnie.
def lista_tabel_polacz(l1, l2, l3):
    lista_polaczonych_tabel = []
    for i in range(len(l1)):
        lista_polaczonych_tabel.append(pd.merge(pd.merge(l1[i], l2[i], on='Country'), l3[i], on='Country'))
    return lista_polaczonych_tabel


# Dla danej listy dataframow (wszystkie z takimi samymi kolumnami, ale inne dane),
# tworzymy liste dataframow, ktore zawieraja tylko czesc kolumn z poczatkowych dataframow.
# nastepnie kazdego dataframa sortujemy po jendej z kolumn
# zwraca dataframe, ktory zostal polaczony ze wszystkich df z nowej listy.
def tabela_najwiecej_co2(tabele_emisja):
    tabele_rok = []
    for i in range(len(tabele_emisja)):
        tabele_rok.append(tabele_emisja[i][['Year', 'Country', 'Per Capita', 'Total']])
        tabele_rok[i] = tabele_rok[i].sort_values('Per Capita', ascending=False)
        tabele_rok[i] = tabele_rok[i].head()
    tabela = pd.concat(tabele_rok)
    return tabela


# Mamy liste dataframow, ktore maja miedzy innymi kolumny z rokiem, krajem, populacja, GDP,
# Tworzymy nowa liste dataframow z danej listy z kolumanmi: 'Year', 'Country', 'Population', 'GDP'
# Nastepnie dla kazdego dataframe w nowej liscie dodajemy nowa kolumne z wartosciami: GDP/Population
# Sortujemy po nowo dodanej kolumnie i zostawiamy w kazdym dataframie tylko 5 gornych wierszy.
# Laczymy wszystkie dataframy z listy w jeden dataframe i go zwracamy.
def tabela_najwiekszy_przychod(tabele_emisja_pop_gdp):
    tabele_rok = []
    tabele_rok2 = []
    for i in range(len(tabele_emisja_pop_gdp)):
        tabele_rok.append(tabele_emisja_pop_gdp[i][['Year', 'Country', 'Population', 'GDP']])
        tabele_rok2.append(tabele_rok[i].assign(c=lambda x: x.GDP/x.Population))
        tabele_rok2[i] = tabele_rok2[i].sort_values('c', ascending=False)
        tabele_rok2[i] = tabele_rok2[i].head()
    tabela = pd.concat(tabele_rok2)
    del tabela['Population']
    return tabela


# Mamy dataframe emisja, oraz liste lat (niepusta) posortowana rosnaco
# Tworzymy nowa liste z ostatnimi 10 latami, albo jesli lista jest krotsza to zostawiamy ja
# Nastepnie tworzymy nowy dataframe z danego dataframa z kolumnami: 'Year', 'Country', 'Per Capita'
# Nastepnie tworzymy dwa nowe dataframy, jeden z pierwszym rokiem z listy lat, drugi z ostatnim rokiem z listy lat
# Pozniej laczymy te dwa dataframy po kolumnie 'Country' i tworzymy nowa kolumne z roznica:
# Per Capita z  ostatniego roku z Per Capita z pierwszego roku
def roznica_max_min(emisja, lata_wspolne):
    if len(lata_wspolne) > 10:
        lata_ostatnie = []
        for i in range(-10, 0):
            lata_ostatnie.append(lata_wspolne[i])
    else:
        lata_ostatnie = lata_wspolne
    emisja2 = emisja[['Year', 'Country', 'Per Capita']]
    emisja_rok_pierwszy = emisja2[emisja2['Year'] == lata_ostatnie[0]]
    emisja_rok_ostatni = emisja2[emisja2['Year'] == lata_ostatnie[-1]]
    wynik = pd.merge(emisja_rok_pierwszy, emisja_rok_ostatni, on="Country")
    wynik.loc[:, 'diff'] = wynik['Per Capita_y'] - wynik['Per Capita_x']
    wynik_max = wynik.sort_values('diff').head()
    wynik_min = wynik.sort_values('diff', ascending=False).head()
    print(wynik.sort_values('diff'))
    print(wynik_max)
    print(wynik_min)
