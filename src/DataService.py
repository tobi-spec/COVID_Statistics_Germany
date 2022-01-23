import os
import sys
from os import listdir
from pathlib import Path
import pandas as pd


def rki_data():
    """
        Function opens csv with all daily reports of rki covid data
        values of colume "Meldedatum" are converted into pandas datetime objects
        colume "Meldedatum" is set as index
        rows are grouped by "Meldedatum" index
        rows are grouped by week
    """
    directory = Path("data/rki/RKI_COVID19.csv")

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


if __name__ == "__main__":
    rki_data()