import unittest
import mock
from COVID_functions import *
from COVID_DIVI_analyzer import *
from COVID_DIVI_crawler import *


# TODO: pathlib 
liste = ["1","2","3","4"]
dictionary = {1:"A", 2:"B", 3:"C"}
string = "www.google.de/"
url_string = "https://www.google.de/"
url_string_format = "https://www.google.de/{}"
url_list = ["https://www.google.de/"]
url_list_without_http = ["www.google.de/"]
path = ".\\data\\DIVI_data\\"
wrong_path = ".\\data\\DIVI_data123\\"
csv_testlist = [".\\data\\test_data\\DIVI-testfile.csv"]
txt_testlist = [".\\data\\test_data\\DIVI-testfile.txt"]

class COVID_UnitTests(unittest.TestCase):

# Unittests for generate_url_list:

    #Warum funktioniert diese Version nicht? Die nächste aber schon? 
    # def test_generate_url_list_no_http(self):
    #     with self.assertRaises(SystemExit) as cm:
    #         for i in generate_url_list("www.google.de/", start=0,end=0):
    #             print(i)
    #     self.assertEqual(cm.exception.code, 1) 

    def test_generate_url_list_not_http(self):
        with self.assertRaises(SystemExit) as cm:
            next(generate_url_list("www.google.de/{}", start=0, end=0))
        self.assertEqual(cm.exception.code, 1)

    def test_generate_url_list_no_curly_braces(self):
        with self.assertRaises(SystemExit) as cm:
            next(generate_url_list("https://www.google.de/", start=0, end=0))
        self.assertEqual(cm.exception.code, 1) 

    def test_generate_url_list(self):
        working_generator = next(generate_url_list("https://www.google.de/{}", start=0, end=0))
        self.assertTrue(working_generator)


# Unittests for crawl_links_from_url:

    def test_crawl_links_from_url_hasnt_http(self):
        with self.assertRaises(SystemExit) as cm:
            crawl_links_from_url("www.google.de/", "www.google.de/")
        self.assertEqual(cm.exception.code, 1)


    def test_crawl_links_from_url_searched_link_not_str(self):
        with self.assertRaises(SystemExit) as cm:
            crawl_links_from_url("https://www.google.de/", ["https://www.google.de/"])
        self.assertEqual(cm.exception.code, 1)


    def test_crawl_links_from_url(self):
        self.assertIsInstance(crawl_links_from_url(url_string, string), list)

    def test_crawl_links_from_url2(self):
        self.assertTrue(crawl_links_from_url(url_string, string))

# Unittests for download_file:


    def test_download_csv_csv_not_https(self):
        with self.assertRaises(SystemExit) as cm:
            download_csv(string, ".\\data\\test.csv")
        self.assertEqual(cm.exception.code, 1)

    def test_download_csv_output_path_not_string(self):
        with self.assertRaises(SystemExit) as cm:
            download_csv(url_string, 1)
        self.assertEqual(cm.exception.code, 1)

    # There is no current unitests to check the actual request/download function
    

# Unitests for call_archiv:

    def test_call_archiv_path_not_string(self):
        with self.assertRaises(SystemExit) as cm:
            call_archiv(liste)
        self.assertEqual(cm.exception.code, 1)

    def test_call_archiv_path_dont_exists(self):
        with self.assertRaises(SystemExit) as cm:
            call_archiv(wrong_path)
        self.assertEqual(cm.exception.code, 1)

    #TODO: Mock? 
    def test_call_archiv(self):
        self.assertTrue(call_archiv(path))


# Unittest for divi_csv_analyser:

    def test_divi_csv_analyser_file_not_csv(self):
        with self.assertRaises(SystemExit) as cm:
            divi_csv_analyser(txt_testlist, "faelle_covid_aktuell")
        self.assertEqual(cm.exception.code, 1)

    def test_divi_csv_analyser_searched_item_not_string(self):
        with self.assertRaises(SystemExit) as cm:
            divi_csv_analyser(csv_testlist, 1)
        self.assertEqual(cm.exception.code, 1)
    
    # TODO: Mock?
    def test_divi_csv_analyser(self):
        self.assertTrue(divi_csv_analyser(csv_testlist, "faelle_covid_aktuell"))

# Unittests for line_plot:

    def test_line_plot_not_list(self):
        with self.assertRaises(SystemExit) as cm:
            line_plot(string)
        self.assertEqual(cm.exception.code, 1)

    # There is no current unitests to check the actual plot function

# Unittests for COVID_DIVI_crawler:

    #TODO: Mocks? 

# Unittests for COVID_DIVI_analyzer:

    #TODO: Mock?
    def test_divi_analysis(self):
        self.assertEqual(divi_analysis("faelle_covid_aktuell"), plt.show())



if __name__=='__main__': 
    unittest.main()