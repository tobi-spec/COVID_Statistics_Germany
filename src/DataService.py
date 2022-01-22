import os
import sys
from os import listdir
from pathlib import Path
import pandas as pd

'''
DIVI.data: Daily reports are seperated into reporting countys. These will be summerize to german wide daily values.
         All Daily values are gathered into a pandas.dataframe.

RKI.data ,the data is seperated into different reporting offices, so the data is summarize to weekly values
pandas.dataframe contains following columnes:
            'AnzahlFall',
            'AnzahlTodesfall',
            'NeuerFall',
            'NeuerTodesfall',
            'NeuGenesen',
            'AnzahlGenesen',
            'IstErkrankungsbeginn'
'''


def divi_data():
    directory = "./data/divi_data/"

    path = Path(directory)
    csv_files = call_archiv(path)
    daily_dataframes = []

    for csv_file in csv_files:

        csv_tester = str(csv_file)
        if not csv_tester.endswith("csv"):
            print(f"{csv_file} is not csv file")
            sys.exit(1)

        df = pd.read_csv(csv_file)

        if 'daten_stand' in df.columns:
            df['daten_stand'] = pd.to_datetime(df['daten_stand'])
            df['daten_stand'] = df['daten_stand'].dt.date
            df_index = df.set_index('daten_stand')
            df_sum = df_index.groupby(by='daten_stand').sum()
            df_clean = df_sum.drop(['bundesland',
                                    'gemeindeschluessel',
                                    'anzahl_meldebereiche',
                                    "anzahl_standorte", ],
                                   axis=1)
            df_clean = df_clean.rename(columns={"faelle_covid_aktuell_beatmet": "faelle_covid_aktuell_invasiv_beatmet"})
            daily_dataframes.append(df_clean)

        else:
            print(f"Tagesdaten von {csv_file} werden nicht erfasst")

    df_divi = pd.concat(daily_dataframes)
    print(df_divi)

    return df_divi


def rki_data():
    """
        Function opens csv with all daily reports of rki covid data
        values of colume "Meldedatum" are converted into pandas datetime objects
        colume "Meldedatum" is set as index
        rows are grouped by "Meldedatum" index
        rows are grouped per week
        values are returned
    """
    directory = Path("Data/rki/")

    df = pd.read_csv(directory)

    df["Meldedatum"] = pd.to_datetime(df["Meldedatum"])
    df_index = df.set_index("Meldedatum")
    df_sum = df_index.groupby(by="Meldedatum").sum()
    df_weekly = df_sum.resample('w').sum()
    df_rki = df_weekly
    df_rki = df_weekly.drop(['FID',
                             'IdBundesland',
                             'IdLandkreis'],
                            axis=1)
    print(df_rki)
    return df_rki


def call_archiv(path):
    if not os.path.exists(path):
        print("call_archive: path doesn't exists")
        sys.exit(1)

    list_of_files = []
    for element in listdir(path):
        data = path / element
        list_of_files.append(str(data))

    return list_of_files
