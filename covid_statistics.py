import os.path
import sys
import requests
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlsplit, urlunsplit
from os import listdir
from pathlib import Path



class DIVI:
    '''
    This class enables the download and handle of COVID 19 intensiv care data provided by the DIVI Insitiut (www.divi.de)
    DIVI provides data als daily reports, each report saved as a single csv file.  

    DIVI.fetch: allows the download of the whole csv data files archive, saved in a seperate folder (./data/divi)
    DIVI.update: searches for the latest reports. Notice that it will only find the latest missing files. 
                 Gapes between the files are not controlled.
    DIVI.data: Daily reports are seperated into reporting countys. These will be summerize to german wide daily values. 
                 All Daily values are gathered into a pandas.dataframe. 

    pandas.dataframe contains following columnes:  
        'faelle_covid_aktuell', 
        'faelle_covid_aktuell_invasiv_beatmet',
        'betten_frei', 
        'betten_belegt',
        'betten_frei_nur_erwachsen'
        'betten_belegt_nur_erwachsen', 
    '''

    @classmethod
    def fetch(cls):
        url = "https://www.divi.de/divi-intensivregister-tagesreport-archiv-csv?layout=table&start=0"
        attribute = "aria-label"
        directory = Path("./data/divi_data/")
    
        archive_links = []

        print("scrape archive...")
        archive = cls._get_archive(url)

        print("scrape links...")
        for site in archive:
            links = cls._get_links(site, attribute)
            archive_links.append(links)
            print(archive_links)

        directory =cls._create_directory(directory)

        print("save csv files...")
        for element in archive_links:
            for key, value in element.items():
                download_link =cls._merge_link_with_base(url, value)
                cls._save_csv(directory=f"{directory}/{key}.csv", link=download_link)
                print(key)   

    @classmethod
    def update(cls):
        url = "https://www.divi.de/divi-intensivregister-tagesreport-archiv-csv?layout=table&start={}"
        attribute = "aria-label"
        directory = "./data/divi_data/"

        archive = cls._generate_archive(url)
        
        for site in archive:
            links = cls._get_links(site, attribute)
            for key, value in links.items():
                if f"{key}.csv" not in listdir(directory):
                    download_link =cls._merge_link_with_base(url, value)
                    cls._save_csv(directory=f"{directory}/{key}.csv", link=download_link)
                    print(f"new file found: {key}")
                else:
                    print("archive up to date")
                    sys.exit(1)

    @classmethod
    def data(cls):
        directory = "./data/divi_data/"

        path = Path(directory)
        csv_files =cls._call_archiv(path)
        daily_values = []
        daily_dates = []
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

    def _get_archive(url):
        link_list = []

        while url:
            r = requests.get(url)
            url_soup = BeautifulSoup(r.text, "html.parser")
            link_list.append(url)
            print(url)
            url = False
            
            for tag in url_soup.find_all('a', href=True):
                if tag.get("title") == "Weiter":
                    next_page = tag.get("href") #Dosent find new link on last side, url=False stays and while-loop breaks
                    url = urljoin("https://www.divi.de", next_page)
                    print(url)
        return link_list

    def _generate_archive(url):
        counter = 0
        url = url.format(counter)
        while True:
            counter += 20
            yield(url)

    def _get_links(url, attribute):
        link_dict = {}
        r = requests.get(url)
        soup = BeautifulSoup(r.text, "html.parser")
        for tag in soup.find_all('a', href=True):
            if tag.get(attribute):
                link_dict[tag.get(attribute)] = tag.get("href")

        return link_dict

    def _merge_link_with_base(url, link):
        url = urlsplit(url)
        url = urlunsplit([url.scheme, url.netloc, link, None, None]) #Functions takes only iterable of 5
        return url

    def _create_directory(directory):
        if not os.path.exists(directory):
            os.makedirs(directory)
        return directory

    def _save_csv(directory, link):
        response = requests.get(link)
        with open(Path(directory), 'w', encoding="utf-8", newline='') as file:
                    file.write(response.text)

    def _call_archiv(path):
        if not os.path.exists(path):
            print("call_archiv: path dosent exists")
            sys.exit(1)

        list_of_files = []
        for element in listdir(path):
            data = path / element
            list_of_files.append(str(data))

        return list_of_files


class RKI(DIVI):
    '''
    This class enables the download and handle of COVID-19 epidemiological data provides by the german RKI Institut (www.RKI.de)
    All data is gathereed into a single csv file, which makes the file very large (> 1.8million columns)

    RKI.fetch allows the download of the whole file, saved in a seperated folder (./data/rki)
    RKI.data ,the data is seperated into different reporting offices, so the data is summarize to weekly values 

    pandas.dataframe contains following columnes:  
                'AnzahlFall', 
                'AnzahlTodesfall', 
                'NeuerFall', 
                'NeuerTodesfall',
                'NeuGenesen', 
                'AnzahlGenesen', 
                'IstErkrankungsbeginn' 
    '''

    @classmethod
    def fetch(cls):
        
        url = "https://www.arcgis.com/sharing/rest/content/items/f10774f1c63e40168479a1feb6c7ca74/data"
        directory = Path("./data/rki/")
        print("this will need a while...")
        cls._save_csv(directory, url)
        print("Finished!")

    @classmethod
    def data(cls):
        '''
        Function opens csv with all daily reports of rki covid data
        values of colume "Meldedatum" are converted into pandas datetime objects
        colume "Meldedatum" is set as index
        rows are grouped by "Meldedatum" index
        rows are grouped per week
        values are returned
        '''
        directory = Path("./data/rki/")

        df= pd.read_csv(directory)

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


class Plot:

    def __init__(self, x, y, title):
        self.grid_x = x
        self.grid_y = y
        self.title = title
        self.fig, self.axes = plt.subplots(self.grid_x, self.grid_y)
        self.fig.suptitle(self.title)

    def add_lineplot(self, position, dataframe, title, ylabel):
        plot = sns.lineplot(ax=self.axes[position], data=dataframe)
        self.axes[position].set_title(title)
        self.axes[position].set_ylabel(ylabel)
        self.axes[position].set_xlabel("Zeit")
        plt.setp(plot.get_xticklabels(), rotation=45)
        
        return plot

    def show_plots(self):
        plt.show()


if __name__ == "__main__":

    # Fetch data from DIVI
    DIVI.fetch()

    # Fetch data from RKI
    RKI.fetch()

    # Given an overview about COVID-19 infektions, severe cases and deaths in germany 
    RKI = RKI.data()
    DIVI = DIVI.data()

    overview = Plot(1,3, "COVID-19 Monitor")
    overview.add_lineplot(position=0, 
                        dataframe=RKI['AnzahlFall'], 
                        title='Neue Infektionen pro Woche', 
                        ylabel="Neuinfektionen")

    overview.add_lineplot(position=1, 
                        dataframe=DIVI['faelle_covid_aktuell'], 
                        title='Verlauf schwere COVID-19 Fälle', 
                        ylabel="Intensivfälle")

    overview.add_lineplot(position=2, 
                        dataframe=RKI['AnzahlTodesfall'], 
                        title='Neue Todesfälle pro Woche', 
                        ylabel="Todesfälle")
    overview.show_plots()