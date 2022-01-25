import os
import sys

import requests
from pathlib import Path

'''
This class enables the download and handle of COVID-19 epidemiological data provides by the german RKI Institut (www.RKI.de)
All data is gathereed into a single csv file, which makes the file very large (> 1.8million columns)

'''


def create_directory(directory):
    if not isinstance(directory, str):
        sys.exit("directory must be string")
    universal_directory = Path(directory)
    if not os.path.isdir(universal_directory):
        os.makedirs(universal_directory)
    else:
        return "directory already exists"


def fetch_csv(link):
    try:
        response = requests.get(link)
        return response.text
    except Exception as e:
        raise SystemExit(e)


def save_csv(directory, filename, string):
    if not os.path.exists(directory):
        sys.exit("directory does not exist")
    if not isinstance(filename, str):
        sys.exit("filename must be string")
    if not filename.endswith(".csv"):
        sys.exit("filename must end with .csv")
    if not isinstance(string, str):
        sys.exit("only strings can saved in csv")
    directory = Path(directory)
    with open(Path(directory / filename), 'w', encoding="utf-8", newline='') as file:
        file.write(string)


if __name__ == "__main__":
    url = "https://www.arcgis.com/sharing/rest/content/items/f10774f1c63e40168479a1feb6c7ca74/data"
    directory = "./data/raw/"
    filename = "rki.csv"
    print("this will need a while...")
    create_directory("./data/raw")
    content = fetch_csv(url)
    save_csv(directory, filename, content)
    print(f"Finished! with {filename}")
