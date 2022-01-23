import os
import sys

import requests
from pathlib import Path

'''
This class enables the download and handle of COVID-19 epidemiological data provides by the german RKI Institut (www.RKI.de)
All data is gathereed into a single csv file, which makes the file very large (> 1.8million columns)

'''


def fetch():
    url = "https://www.arcgis.com/sharing/rest/content/items/f10774f1c63e40168479a1feb6c7ca74/data"
    directory = Path("./data/raw/rki.csv")

    if not os.path.isdir("./data/raw"):
        create_directory("./data/raw")
    print("this will need a while...")
    save_csv(directory, url)
    print("Finished!")


def create_directory(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)
    return directory


def fetch_csv(link):
    try:
        response = requests.get(link)
        return response.text
    except Exception as e:
        raise SystemExit(e)


def save_csv(directory, string):
    if not isinstance(string, str):
        sys.exit("only strings can saved in csv")
    with open(Path(directory), 'w', encoding="utf-8", newline='') as file:
        file.write(string)


if __name__ == "__main__":
    fetch()
