import os.path
import sys
import pandas as pd
import seaborn as sns
import pathlib
from os import listdir
import matplotlib.pyplot as plt

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


    archiv_path = pathlib.Path(archiv_path)

    list_of_reports = []
    for element in listdir(archiv_path):
        data = archiv_path / element
        list_of_reports.append(str(data))

    return list_of_reports


def csv_sum_columnes(csv_files, searched_item):
    ''' functions sums up all values of a wanted columne in csv file
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

        if not csv_file.endswith("csv"):
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


def generate_timelabel_dataframe(list_of_values, start_date, end_date):
    ''' Takes a list of values and generates a pandas.DataFrame with daily frequency dates as index'''

    if not isinstance(list_of_values, list):
        print("generate_timelabel_dataframe: list_of_values must be list")
        sys.exit(1)

    if not isinstance(start_date, str):
        print("generate_timelabel_dataframe: start_date must be str")
        sys.exit(1)

    if not isinstance(end_date, str):
        print("generate_timelabel_dataframe: end_date must be str")
        sys.exit(1)

    
    series_index = pd.date_range(start=start_date, end=end_date)
    plotting_df = pd.DataFrame(
                {"ICU Cases": list_of_values,
                "Time": series_index}
            )

    return plotting_df


## Plotter Functions ##

def divi_ICU():
    ''' Generates a line plot to show the course of COVID-19 ICU Cases in Germany'''

    file_path = "./data/DIVI_data/"
    files = call_archiv(file_path)
    numbers = csv_sum_columnes(files, "faelle_covid_aktuell")
    data1 = generate_timelabel_dataframe(
                                        list_of_values=numbers,
                                        start_date=files[0][-14:-4],
                                        end_date=files[-1][-14:-4]
                                        )

    sns.lineplot(data=data1, x="Time", y="ICU Cases")
    plt.show()


if __name__ == '__main__':

    divi_ICU()
