import BasicMethods
from pathlib import Path
import pandas as pd

'''
This class enables the download and handle of COVID-19 epidemiological data provides by the german RKI Institut (www.RKI.de)
All data is gathereed into a single csv file, which makes the file very large (> 1.8million columns)

RKI.fetch allows the download of the whole file, saved in a seperated folder (./data/rki)

'''


def fetch():
    url = "https://www.arcgis.com/sharing/rest/content/items/f10774f1c63e40168479a1feb6c7ca74/data"
    directory = Path("./data/rki/")
    print("this will need a while...")
    BasicMethods.save_csv(directory, url)
    print("Finished!")


def rki_data():
    '''
    Function opens csv with all daily reports of rki covid data
    values of colume "Meldedatum" are converted into pandas datetime objects
    colume "Meldedatum" is set as index
    rows are grouped by "Meldedatum" index
    rows are grouped per week
    values are returned
    '''
    directory = Path("./data/rki/")

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

