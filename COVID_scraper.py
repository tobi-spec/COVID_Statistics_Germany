from bs4 import BeautifulSoup
from urllib.parse import urljoin
import os
import requests
import pathlib
import csv
import sys


class COVID_Scraper: 

    def __scrape_divi_page_one(self):
        '''
        function scrapes the first site of the DIVI intensivcare register archiv
        (https://www.divi.de/divi-intensivregister-tagesreport-archiv)
        function scraps from site:
            1) labels of all daily report csv files 
            2) all links for daily report csv files
        function saves all found daily report links in a dict
        labels are used as key, urls are used as value
        '''

        divi = "https://www.divi.de/"
        url = "https://www.divi.de/divi-intensivregister-tagesreport-archiv-csv?layout=table&start=0"
        csv_dict = {}

        r = requests.get(url)
        soup = BeautifulSoup(r.text, "html.parser")

        for tag in soup.find_all('a', href=True):
            if tag.get("aria-label") != None:
                csv_dict[tag.get("aria-label")] = tag.get("href")

        print("first site of archiv scraped")

        return csv_dict


    def __scrape_divi_archiv(self):
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

            print(f"{counter} sites of archiv scraped")
            counter += 1

        return csv_dict


    def __download_csv_from_divi(self, csv_dict):
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

        if not os.path.exists(download_path):
            os.mkdir(download_path)


        for key, value in csv_dict.items(): 
            download_link = urljoin(divi, value)
            response = requests.get(download_link)
            file_path = f"{download_path}/{key}.csv"
            
            if f"{key}.csv" not in os.listdir(download_path):
                print(f"New file downloaded: {key}")
                with open(pathlib.Path(file_path), 'w', newline='') as file:
                    file.write(response.text)
            else:
                print(f"File exists: {key}")
        
        print("Finished")


    def divi_full_load(self):
        print("Downloading full DIVI archiv, this will need some time")
        csv_dict = self.__scrape_divi_archiv()
        download = self.__download_csv_from_divi(csv_dict)
        return download


    def divi_add_load(self):    
        csv_dict = self.__scrape_divi_page_one()
        download = self.__download_csv_from_divi(csv_dict)
        return download


    def rki_load(self):
        '''
        Function requests the csv file with daily COVID-19 values from rki 
        function saves file in subfolder RKI_data
        if subfolder dosent exsis, folder will created
        '''
        
        response = requests.get("https://www.arcgis.com/sharing/rest/content/items/f10774f1c63e40168479a1feb6c7ca74/data")
        download_path = pathlib.Path("./data/RKI_data/")
        file_path = file_path = f"{download_path}/RKI_COVID19.csv"

        if not os.path.exists(download_path):
            os.mkdir(download_path)

        print("Downloading RKI data, this will need some time!")
        with open(pathlib.Path(file_path), 'w', newline='') as file:
                    file.write(response.text)
        
        print("Finished")


if __name__ == '__main__':

    # TODO Input() function um consolenbefehle zu erstellen 

    all_entrys = COVID_Scraper()
    all_entrys.divi_full_load()

    print("Next will be the RKI data!")

    # new_entrys = COVID_Scraper()
    # new_entrys.divi_add_load()

    rki_entrys = COVID_Scraper()
    rki_entrys.rki_load()








    


