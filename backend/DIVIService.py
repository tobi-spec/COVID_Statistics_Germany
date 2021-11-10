import sys
from os import listdir
from pathlib import Path
import pandas as pd

import BasicMethods

'''
This class enables the download and handle of COVID 19 intensiv care data provided by the DIVI Insitiut (www.divi.de)
DIVI provides data als daily reports, each report saved as a single csv file.

DIVI.fetch: allows the download of the whole csv data files archive, saved in a seperate folder (./data/divi)
DIVI.update: searches for the latest reports. Notice that it will only find the latest missing files.
         Gapes between the files are not controlled.

pandas.dataframe contains following columnes:
'faelle_covid_aktuell',
'faelle_covid_aktuell_invasiv_beatmet',
'betten_frei',
'betten_belegt',
'betten_frei_nur_erwachsen'
'betten_belegt_nur_erwachsen',
'''


def fetch():
    url = "https://www.divi.de/divi-intensivregister-tagesreport-archiv-csv?layout=table&start=0"
    attribute = "aria-label"
    directory = Path("./data/divi_data/")

    archive_links = []

    print("scrape archive...")
    archive = BasicMethods.get_archive()

    print("scrape links...")
    for site in archive:
        links = BasicMethods.get_links(site, attribute)
        archive_links.append(links)
        print(archive_links)

    directory = BasicMethods.create_directory(directory)

    print("save csv files...")
    for element in archive_links:
        for key, value in element.items():
            download_link = BasicMethods.merge_link_with_base(url, value)
            BasicMethods.save_csv(directory=f"{directory}/{key}.csv", link=download_link)
            print(key)


def update():
    url = "https://www.divi.de/divi-intensivregister-tagesreport-archiv-csv?layout=table&start={}"
    attribute = "aria-label"
    directory = "./data/divi_data/"

    archive = BasicMethods.generate_archive(url)

    for site in archive:
        links = BasicMethods.get_links(site, attribute)
        for key, value in links.items():
            if f"{key}.csv" not in listdir(directory):
                download_link = BasicMethods.merge_link_with_base(url, value)
                BasicMethods.save_csv(directory=f"{directory}/{key}.csv", link=download_link)
                print(f"new file found: {key}")
            else:
                print("archive up to date")
                sys.exit(1)


def divi_data():
    directory = "./data/divi_data/"

    path = Path(directory)
    csv_files = BasicMethods.call_archiv(path)
    daily_dataframes = []

    for csv_file in csv_files:

        csv_tester = str(csv_file)
        if not csv_tester.endswith("csv"):
            print(f"{csv_file} is not csv file")
            sys.exit(1)

        df= pd.read_csv(csv_file)

        if 'daten_stand' in df.columns:
            df['daten_stand'] = pd.to_datetime(df['daten_stand'])
            df['daten_stand'] = df['daten_stand'].dt.date
            df_index = df.set_index('daten_stand')
            df_sum = df_index.groupby(by='daten_stand').sum()
            df_clean = df_sum.drop(['bundesland',
                                    'gemeindeschluessel',
                                    'anzahl_meldebereiche',
                                    "anzahl_standorte",],
                                   axis=1)
            df_clean = df_clean.rename(columns={"faelle_covid_aktuell_beatmet":"faelle_covid_aktuell_invasiv_beatmet"})
            daily_dataframes.append(df_clean)

        else:
            print(f"Tagesdaten von {csv_file} werden nicht erfasst")

    df_divi = pd.concat(daily_dataframes)
    print(df_divi)

    return df_divi
