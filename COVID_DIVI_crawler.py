import sys
import requests
import re
import csv
import pathlib
from os.path import isfile
from bs4 import BeautifulSoup
from urllib.request import urlopen
from urllib.parse import urljoin
from os import listdir


## Crawler Functions ##

def generate_url_list(url, start=0, end=500):
    ''' uses the "?start=X" ending of an archiv url to generate a theoretical list of urls to access the complete archiv
    url template must start with http (to be an url obviously) and must contain a {} to fit in the .format methode and 
    to be cyclable'''

    counter = start

    if not url.startswith("http"):
        print("create_url_list: url must start with: http")
        sys.exit(1)

    if "{}" not in url:
        print("create_url_list: url must contain {}")
        sys.exit(1)


    while counter <= end:
        yield url.format(counter)
        counter = counter + 20


def crawl_links_from_url(url, searched_link):
    ''' opens url to find the wanted link(s), urls must start with http (to be an url) and searched link must be string '''

    wanted_links = []

    if not url.startswith("http"):
        print("url must start with: http")
        sys.exit(1)

    if not isinstance(searched_link, str):
        print("crawl_links_from_urls: searched_link must be string/regex pattern")
        sys.exit(1)


    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'html.parser')

    for tag in soup.find_all(href=re.compile(searched_link)):
        wanted_links.append(tag.get("href"))

    return wanted_links


def download_csv(csv_url, output_path='OutputList.csv'):
    '''csv must be a url linked to a csv file, this file will be opend and saved in a output path
    outpu_path must be string and lead to a existing directory 
    existence of directory is not checked by this function yet (08-02-2021) )'''

    if not csv_url.startswith("http"):
        print("url must start with: http")
        sys.exit(1)

    if not isinstance(output_path, str):
        print("save_as_CSV_file: output_path must be string")
        sys.exit(1)


    response = requests.get(csv_url)
    with open(pathlib.Path(output_path), 'w', newline='') as file:
        file.write(response.text)


## DIVI-Crawler ##

def download_divi_archiv():
    ''' Function to download the "Divi-Imntensivregister" daily report archiv, all reports are coded as csv files,
    each csv file represeants one day and contains the reports of covid patients of every included intensiv care unit in germany'''

    # URLs nessesarcy to set up the crawler
    divi_archiv = "https://www.divi.de/divi-intensivregister-tagesreport-archiv-csv?layout=table&start={}"
    divi_regex = r"/divi-intensivregister-tagesreport-archiv-csv/viewdocument/.+"
    divi = "https://www.divi.de/"
    file_name_pattern = "divi-intensivregister-[0-9][0-9][0-9][0-9]-[0-9][0-9]-[0-9][0-9]"
    previouse_daily_reports = []

    # Paths nessesarcy to save data files
    archiv_path = "./data/DIVI_data"
    download_path = "./data/DIVI_data/{}.csv"

    print("This will take a while, grab some coffee...")

    # Generator generates step-by-step urls from divi_archiv variable
    # each url contains 20 links of divi daily reports, reports are csv files
    # crawler opens url and grabs all these 20 links and put them into a list
    for url in generate_url_list(divi_archiv):
        daily_report_urls = crawl_links_from_url(url, divi_regex)

        # If the generator reached the end of the archive
        # last site of the archive will be called again and again
        # so if the current daily reports the same then den previouse
        # end of archiv is reached and the programm will end
        # !!! Functions also ends if  {} in divi_archiv variable reached 500 !!!
        # !!! (which is set by the generate_url_list function and can be altered in there) !!!
        if daily_report_urls == previouse_daily_reports:
            print("end of archive")
            sys.exit(1)

        # Programm joins base path of the divi website with
        # the relative path of the daily report link
        # from this path the date of the current file will be set as file_name
        # Programm checks if the current file is already in the DIVI_data directory
        # If not the file will be saved, else not
        for daily_report in daily_report_urls:
            csv_url = urljoin(divi, daily_report)
            file_name = re.findall(file_name_pattern, csv_url)

            if f"{file_name[0]}.csv" not in listdir(archiv_path):
                print("new file found")
                download_csv(csv_url, download_path.format(file_name[0]))
            else:
                print("file exists")

        # The urls of the currently checked daily_reports are set as previouse
        # so the next group of daily reports can the tests if there are the same as previouse
        # to identify the end of the archive
        previouse_daily_reports = daily_report_urls


if __name__ == '__main__':
    
    download_divi_archiv()
