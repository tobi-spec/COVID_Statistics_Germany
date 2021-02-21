from COVID_functions import *
from os.path import isfile


def download_divi_archiv():
    ''' Function to download the "Divi-Imntensivregister" daily report archiv, all reports are coded as csv files,
    each csv file represeants one day and contains the reports of covid patients of every included intensiv care unit in germany'''

    # URLs nessesarcy to set up the crawler 
    divi_archiv  =  "https://www.divi.de/divi-intensivregister-tagesreport-archiv-csv?layout=table&start={}"
    divi_regex   =   r"/divi-intensivregister-tagesreport-archiv-csv/viewdocument/.+"
    divi = "https://www.divi.de/"
    file_name_pattern = "divi-intensivregister-[0-9][0-9][0-9][0-9]-[0-9][0-9]-[0-9][0-9]"
    previouse_daily_reports = []

    #Paths nessesarcy to save data files 
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


if __name__=='__main__': 
    download_divi_archiv()


   