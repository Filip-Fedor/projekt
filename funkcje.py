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

