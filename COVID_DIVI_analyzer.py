from COVID_functions import *

       
def divi_analysis(attribute): 
    ''' Generates a line plot to show the course of a wanted attribute
    data for this function must be downloaded before hand by the "COVID_DIVI_crawler" function
    before it can be passed to this function'''

    file_path = "./data/DIVI_data/"
    files = call_archiv(file_path)
    numbers = divi_csv_analyser(files,attribute)

    return line_plot(numbers, "Time", " ICU Cases")


if __name__=='__main__': 

    divi_analysis("faelle_covid_aktuell")
