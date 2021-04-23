import os.path
import sys
import pathlib
from os import listdir
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt


class COVID_Analyzer:

        def __init__(self, attribute, path):

            self.attribute = attribute
            self.path = pathlib.Path(path)


class DIVI_Analyzer(COVID_Analyzer):


    def __call_archiv(self):
        ''' 
        function calls the path of an folder and puts every element of that folder to a list
        function checks if certain path exists
        '''

        if not os.path.exists(self.path):
            print("call_archiv: path dosent exists")
            sys.exit(1)

        list_of_files = []
        for element in listdir(self.path):
            data = self.path / element
            list_of_files.append(str(data))

        return list_of_files


    def DIVI_DataFrame(self):
        
        ''' 
        functions trys to sum up wanted columne for each daily fill given 
        daily fill values are added to a pandas dataframe
        function takes columne "daten_stand" for each file and try to used it as index for dataframe
        if try fails, in both caeses failed files are returned
        '''

        csv_files = self.__call_archiv()
        daily_values = []
        daily_dates = []

        if not isinstance(self.attribute, str):
            print("divi_csv_analyser: self.attribute must be string")
            sys.exit(1)

        for csv_file in csv_files:

            csv_tester = str(csv_file)
            if not csv_tester.endswith("csv"):
                print(f"{csv_file} is not csv file")
                sys.exit(1)


            df_csv_file = pd.read_csv(csv_file)
            try: 
                daily_values.append(df_csv_file[self.attribute].sum())
            except Exception as e:
                daily_values.append(None)
                print(f"Value of file not used in {self.attribute}: {csv_file}")
            try:
                daily_dates.append(df_csv_file["daten_stand"][0])
            except Exception as e:
                daily_dates.append(None)
                print(f"Dates of file not used in {self.attribute}: {csv_file}")

            df = pd.DataFrame(data=daily_values, index=pd.to_datetime(daily_dates))
                
        return df


class RKI_Analyzer(COVID_Analyzer):


    def RKI_DataFrame(self):
        '''
        Function opens csv with all daily reports of rki covid data
        values of colume "Meldedatum" are converted into pandas datetime objects
        colume "Meldedatum" is set as index
        rows are grouped by "Meldedatum" index
        rows are grouped per week
        values are returned
        '''

        file_path = pathlib.Path(self.path)

        df= pd.read_csv(file_path)

        df["Meldedatum"] = pd.to_datetime(df["Meldedatum"])
        df_index = df.set_index("Meldedatum")
        df_sum = df_index.groupby(by="Meldedatum").sum()
        df_weekly = df_sum.resample('w').mean()  # mean vermutlich falsche position

        return df_weekly[self.attribute]


if __name__ == '__main__':

    #TODO: Verlauf der Neueinlieferung, nicht der Fallzahl
    # Legende anpassen
    # x Achse anpassen das sie gleichen Zeitintervall wie RKI daten hat  
    severe_cases = DIVI_Analyzer(attribute="faelle_covid_aktuell", path="./data/DIVI_data/")
    severe_cases = severe_cases.DIVI_DataFrame()
    #severe_cases = severe_cases.diff()
    
    #TODO: Korrekte Auswertung - siehe RKI Angaben (Fallzahlen von einzelnen Tagen sind überlappend mit vorherigen Tagen)
    infections = RKI_Analyzer(attribute="AnzahlFall", path="./data/RKI_data/RKI_COVID19.csv") 
    infections = infections.RKI_DataFrame()

    #TODO: Korrekte Auswertung - siehe RKI Angaben (Fallzahlen von einzelnen Tagen sind überlappend mit vorherigen Tagen)
    deaths = RKI_Analyzer(attribute="AnzahlTodesfall", path="./data/RKI_data/RKI_COVID19.csv")
    deaths = deaths.RKI_DataFrame()



    fig, axes = plt.subplots(1,3)
    fig.suptitle('COVID-19 Monitor')

    plot0 = sns.lineplot(ax=axes[0], x=infections.index, y=infections.to_numpy())
    plt.setp(plot0.get_xticklabels(), rotation=45)
    axes[0].set_title('Neue Infektionen')

    plot1 = sns.lineplot(ax=axes[1], data=severe_cases)
    plt.setp(plot1.get_xticklabels(), rotation=45)
    axes[1].set_title('Schwere Fälle')

    plot2 = sns.lineplot(ax=axes[2], x=deaths.index, y=deaths.to_numpy())
    plt.setp(plot2.get_xticklabels(), rotation=45)
    axes[2].set_title('Neue Todesfälle')

    plt.show()


    '''TODO (Möglichkeiten): 
    Verlauf Infiziertenzahl (nicht Neuinfektionen), 
    Verlauf der Intensivbettenbelegung (nicht Neueinlieferungen)
    Verlauf Intensivbettenbelegung, gesamt
    Verlauf der freien Intensivbetten 
    Verlauf der Infektionen nach Altersgruppen
    ...
    Testverlauf gesamt?
    Verlauf positiv Testrate?
    Eurostat für Übersterblichkeit? 

    Erklärungen einfügen? 
    '''

    
