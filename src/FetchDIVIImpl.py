import FetchService
import sys
from os import listdir
from pathlib import Path

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
    directory = Path("src/Data/divi_data/")

    archive_links = []

    print("scrape archive...")
    archive = FetchService.get_archive()

    print("scrape links...")
    for site in archive:
        links = FetchService.get_links(site, attribute)
        archive_links.append(links)
        print(archive_links)

    directory = FetchService.create_directory(directory)

    print("save csv files...")
    for element in archive_links:
        for key, value in element.items():
            download_link = FetchService.merge_link_with_base(url, value)
            FetchService.save_csv(directory=f"{directory}/{key}.csv", link=download_link)
            print(key)


def update():
    url = "https://www.divi.de/divi-intensivregister-tagesreport-archiv-csv?layout=table&start={}"
    attribute = "aria-label"
    directory = "./data/divi_data/"

    archive = FetchService.generate_archive(url)

    for site in archive:
        links = FetchService.get_links(site, attribute)
        for key, value in links.items():
            if f"{key}.csv" not in listdir(directory):
                download_link = FetchService.merge_link_with_base(url, value)
                FetchService.save_csv(directory=f"{directory}/{key}.csv", link=download_link)
                print(f"new file found: {key}")
            else:
                print("archive up to date")
                sys.exit(1)
