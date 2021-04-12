import os.path
import sys
import pandas as pd
import seaborn as sns
import pathlib
from os import listdir
import matplotlib.pyplot as plt

## Calculator Functions ##

def call_archiv(archiv_path):
    ''' 
    function calls the path of an folder and puts every element of that folder to a list
    function checks if certain path exists
    '''

    if not os.path.exists(archiv_path):
        print("call_archiv: path dosent exists")
        sys.exit(1)


    archiv_path = pathlib.Path(archiv_path)

    list_of_files = []
    for element in listdir(archiv_path):
        data = archiv_path / element
        list_of_files.append(str(data))

    return list_of_files


def csv_sum_columnes(csv_files, searched_item):
    
    ''' 
    functions sums up all values of a wanted columne in csv file
        1) checks if searched item is string
        2) checks if given elements of file list are csv files by checking .csv ending
        3) sums up columne with name given by "searched_item" of each csv file
        4) adds results of all csv files in list
    '''

    values_of_all_files = []

    if not isinstance(searched_item, str):
        print("divi_csv_analyser: searched_item must be string")
        sys.exit(1)

    for csv_file in csv_files:

        csv_tester = str(csv_file)
        if not csv_tester.endswith("csv"):
            print(f"{csv_file} is not csv file")
            sys.exit(1)


        df_csv_file = pd.read_csv(csv_file)
        
        if searched_item in df_csv_file.columns:
            sum_columns = sum(df_csv_file[searched_item])
            values_of_all_files.append(sum_columns)
        else:
            print("unused file: " + str(csv_file))
            values_of_all_files.append(None)
            
    return values_of_all_files


## Plotter Functions ##

def divi_ICU():
    ''' 
    function calls "call_archiv()" to get all files
    function calls "csv_sum_columns" to calculate course of ICU patients per day
    function generated suitable date range
    ICU patients course and date range are merged as pandas dataframe
    function plots dataframe and saves plot in folder
    '''

    file_path = pathlib.Path("./data/DIVI_data/")
    files = call_archiv(file_path)

    numbers = csv_sum_columnes(files, "faelle_covid_aktuell")
    dates = pd.date_range(start=files[0][-20:-10], end=files[-1][-20:-10], periods=len(files))

    df = pd.DataFrame({
            "ICU cases":numbers, 
            "Time":dates
                        })

    sns.lineplot(data=df, x="Time", y="ICU cases")
    plt.savefig("ICU Patients in Germany")


if __name__ == '__main__':

    divi_ICU()

