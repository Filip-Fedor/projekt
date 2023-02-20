from funkcje import *
import pandas as pd
import pytest


df1 = {"Year": [2000, 2001, 2002, 2003]}
df1 = pd.DataFrame(df1)

df2 = {"Country": ["Poland", "France"], "kolumna2": ["POL", "FRA"], "Kolumna3": ["POL", "FRA"], "Kolumna4": ["POL", "FRA"], "2002": [0, 0], "2003": [0, 0]}
df2 = pd.DataFrame(df2)

df3 = {"Country": ["Poland", "France"], "kolumna2": ["POL", "FRA"], "Kolumna3": ["POL", "FRA"], "Kolumna4": ["POL", "FRA"], "2000": [0, 0], "2003": [0, 0]}
df3 = pd.DataFrame(df3)

@pytest.mark.parametrize("df1, df2, df3, result", [(df1, df2, df3, "2003")])


def test1(df1, df2, df3, result):
    assert wspolne_lata(df1, df2, df3) == ["2003"]


df4 = {"Year": [2000, 2000], "Country": ["Poland", "FRANCE"], "Per Capita": [1, 2], "Total": [1, 2]}
df4 = pd.DataFrame(df4)
df5 = {"Year": [2001, 2001], "Country": ["Poland", "FRANCE"], "Per Capita": [2, 4], "Total": [2, 4]}
df5 = pd.DataFrame(df5)
lista = [df4, df5]

result = {"Year": [2000, 2000, 2001, 2001], "Country": ["FRANCE", "Poland", "FRANCE", "Poland"], "Per Capita": [2, 1, 4, 2], "Total": [2, 1, 4, 2]}
result = pd.DataFrame(result, index = [1, 0, 1, 0])

@pytest.mark.parametrize("lista_tabel, result", [(lista, result)])

def test2(lista_tabel, result):
    assert tabela_najwiecej_co2(lista_tabel).equals(result)