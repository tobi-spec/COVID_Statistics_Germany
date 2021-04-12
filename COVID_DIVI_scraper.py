from bs4 import BeautifulSoup
from urllib.parse import urljoin
from os import listdir
import requests
import pathlib
import csv
import sys


def scrape_divi_archiv():
    '''
    function cycles through the sites of the DIVI Intensivcare register archiv
    (https://www.divi.de/divi-intensivregister-tagesreport-archiv)
    function scraps from each site:
        1) labels of all daily report csv files 
        2) all links for daily report csv files
        3) url of the next archiv site
    function saves all found daily report links in a dict
    labels are used as key, urls are used as value
    '''

    divi = "https://www.divi.de/"
    url = "https://www.divi.de/divi-intensivregister-tagesreport-archiv-csv?layout=table&start=0"
    csv_dict = {}

    print("This will take some time...")
    counter = 1 

    while url != None:

        r = requests.get(url)
        soup = BeautifulSoup(r.text, "html.parser")
        url = None

        for tag in soup.find_all('a', href=True):
            if tag.get("aria-label") != None:
                csv_dict[tag.get("aria-label")] = tag.get("href")

            if tag.get("title") == "Weiter":
                next_page = tag.get("href")
                url = urljoin(divi, next_page)

        print(f"{counter} site(s) of archiv scraped")
        counter += 1

    return csv_dict


def download_csv(csv_dict):
    '''
    function iterates over dict with urls to csv files
    key is used as file name, value is used as url for download
    before each file is downloaded, function checks if name of the file (key) exists in download path
    '''
    
    divi = "https://www.divi.de/"
    download_path = pathlib.Path("./data/DIVI_data/")

    if not isinstance(csv_dict, dict):
        print("csv files must be passed to function as dict")
        sys.exit(1)

    for key, value in csv_dict.items(): 
        download_link = urljoin(divi, value)
        response = requests.get(download_link)
        file_path = f"{download_path}/{key}.csv"
        
        if f"{key}.csv" not in listdir(download_path):
            print(f"New file downloaded: {key}")
            with open(pathlib.Path(file_path), 'w', newline='') as file:
                file.write(response.text)
        else:
            print(f"File exists: {key}")
        
    print("Finished")
    
if __name__ == '__main__':
    
    csv_dict = scrape_divi_archiv()
    download_csv(csv_dict)

