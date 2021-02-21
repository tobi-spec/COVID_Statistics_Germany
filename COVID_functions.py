import re
import csv
import sys
import requests
import pathlib
import os.path
from os import listdir
from bs4 import BeautifulSoup
from urllib.request import urlopen
from urllib.parse import urljoin
from time import sleep
import matplotlib.pyplot as plt



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


    sleep = 0.5
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



## Calculator Functions ##

def call_archiv(archiv_path):
    ''' calls the path of an folder and puts every element of the folder to a list
    path of the folder must be passed to the function as string and will be checked if certain path exists'''

    if not isinstance(archiv_path, str):
        print("call_archiv: archiv_path must be string")
        sys.exit(1)

    if not os.path.exists(archiv_path):
        print("call_archiv: path dosent exists")
        sys.exit(1)

    #TODO: Pathlib, Pathlib.join? Weiterverarbeitung als String? 
    archiv_path = pathlib.Path(archiv_path)

    list_of_reports = []
    for element in listdir(archiv_path):
        data = archiv_path / element
        list_of_reports.append(str(data))

    return list_of_reports


def divi_csv_analyser(csv_files, searched_item):
    ''' divi has a strange way to save informations in csv files:
    function opens file, searches for searched_item in header/first line to find its position, 
    takes value of position in each row and summaries everything
    gives the values for each day/csv_file and append it to a list which contains value of all days'''

    #TODO
    #Code einfacher zu schreiben? sum(value_each_file) ist kerngedanke
    #Mit pandas einfacher zu realisieren? 

    values_of_all_files = []

    if not isinstance(searched_item, str):
        print("divi_csv_analyser: searched_item must be string")
        sys.exit(1)


    for csv_file in csv_files:
        if not csv_file.endswith("csv"):
            print(f"{csv_file} is not csv file")
            sys.exit(1)

        value_each_file = []

        with open(csv_file, "r", encoding="utf-8-sig") as file:
            # Exception as e noch verstehen und einbauen 
            try:
                first_row = file.readline().split(",")
                index_searched_item = first_row.index(searched_item)
            except Exception as e:
                print(f"{searched_item} can not be found in {file}")
                continue

            for row in file.readlines():
                try:
                    value_each_row = (row.split(","))[index_searched_item]
                    value_each_file.append(int(value_each_row))
                except:
                    print(f"{index_searched_item}({searched_item}) not found in {csv_file}")
                    continue

            values_of_all_files.append(sum(value_each_file))
        
    return values_of_all_files

# TODO: Def für rki data



## Plotter functions ##

def line_plot(list_of_numbers, x_axis, y_axis):
    ''' generate a basic line plot from a list of numbers'''

    if not isinstance(list_of_numbers, list):
        print("line_plot: list_of_numbers must be list")
        sys.exit(1)

    ys = list_of_numbers
    xs = [n for n in range(0,len(ys))]
   
    plt.plot(xs, ys)
    plt.xlabel(x_axis)
    plt.ylabel(y_axis)
    
    return plt.show()

# TODO 
 # Funktion trenne in Werte erstellen und Plot zeichnen
# weitere plot varianten (balken, kreis etc.)
# schönere graphen als bisher (achsenbeschriftng)
# Vorallem in Hinblick auf RKI Daten 
