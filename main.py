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
GDP = czytaj_plik(args.sciezka_GDP, "API_NY.GDP.MKTP.CD_DS2_en_csv_v2_4751562.csv")
populacja = czytaj_plik(args.sciezka_populacja, "API_SP.POP.TOTL_DS2_en_csv_v2_4751604.csv")
