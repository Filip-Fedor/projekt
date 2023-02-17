import pandas as pd
import os


def czytaj_plik(sciezka, nazwa_pliku):
    polacz_sciezke = os.path.join(sciezka, nazwa_pliku)
    if nazwa_pliku == "fossil-fuel-co2-emissions-by-nation.csv":
        return pd.read_csv(polacz_sciezke)
    else:
        return pd.read_csv(polacz_sciezke, skiprows=4)


def przeciecie(a, b, c):
    return list(set(a) & set(b) & set(c))


def roznica_ab(a, b):
    c = []
    for el in a:
        if el not in b:
            c.append(el)
    return c


def wspolne_lata(emisja, gdp, populacja):
    emisja_lata = emisja['Year'].tolist()
    emisja_lata = list(dict.fromkeys(emisja_lata))
    emisja_lata = [str(i) for i in emisja_lata]
    populacja_lata = populacja.columns[4:].tolist()
    gdp_lata = gdp.columns[4:].tolist()
    lata_wspolne = przeciecie(emisja_lata, populacja_lata, gdp_lata)
    lata_wspolne.sort()
    return lata_wspolne


def wspolne_kraje(emisja, gdp, populacja):
    emisja_kraje = emisja['Country'].tolist()
    emisja_kraje1 = list(dict.fromkeys(emisja_kraje))
    gdp_kraje = gdp['Country Name'].tolist()
    gdp_kraje1 = list(dict.fromkeys(gdp_kraje))
    populacja_kraje = populacja['Country Name'].tolist()
    populacja_kraje1 = list(dict.fromkeys(populacja_kraje))
    return przeciecie(emisja_kraje1, gdp_kraje1, populacja_kraje1)


def lista_tabel_kraj_rok(tabela, lata_wspolne):
    lista_tabel = []
    for i in range(len(lata_wspolne)):
        lista_tabel.append(tabela[['Country Name', lata_wspolne[i]]])
    return lista_tabel


def zmiana_nazwy(lista_tabel, nazwa):
    for i in range(len(lista_tabel)):
        lista_tabel[i].columns = ['Country', nazwa]


def lista_tabel_polacz(l1, l2, l3):
    lista_polaczonych_tabel = []
    for i in range(len(l1)):
        lista_polaczonych_tabel.append(pd.merge(pd.merge(l1[i], l2[i], on='Country'), l3[i], on='Country'))
    return lista_polaczonych_tabel
