import unittest
from COVID_DIVI_analyzer import *
from COVID_DIVI_crawler import *


# TODO: pathlib
liste = ["1", "2", "3", "4"]
dictionary = {1: "A", 2: "B", 3: "C"}
string = ("www.google.de/")
url_string = "https://www.google.de/"
url_string_format = "https://www.google.de/{}"
url_list = ["https://www.google.de/"]
url_list_without_http = ["www.google.de/"]
path = ".\\data\\DIVI_data\\"
wrong_path = ".\\data\\DIVI_data123\\"
csv_testlist = [".\\data\\test_data\\DIVI-testfile.csv"]
txt_testlist = [".\\data\\test_data\\DIVI-testfile.txt"]
start_date = "divi-intensivregister-2020-04-24"
end_date = "divi-intensivregister-2021-04-04"


class COVID_UnitTests(unittest.TestCase):

    # Unittests for generate_url_list():

    def test_generate_url_list_not_http(self):
        with self.assertRaises(SystemExit) as cm:
            next(generate_url_list("www.google.de/{}", start=0, end=0))
        self.assertEqual(cm.exception.code, 1)

    def test_generate_url_list_no_curly_braces(self):
        with self.assertRaises(SystemExit) as cm:
            next(generate_url_list("https://www.google.de/", start=0, end=0))
        self.assertEqual(cm.exception.code, 1)

    def test_generate_url_list(self):
        working_generator = next(generate_url_list(
            "https://www.google.de/{}", start=0, end=0))
        self.assertTrue(working_generator)


# Unittests for crawl_links_from_url():

    def test_crawl_links_from_url_hasnt_http(self):
        with self.assertRaises(SystemExit) as cm:
            crawl_links_from_url("www.google.de/", "www.google.de/")
        self.assertEqual(cm.exception.code, 1)

    def test_crawl_links_from_url_searched_link_not_str(self):
        with self.assertRaises(SystemExit) as cm:
            crawl_links_from_url("https://www.google.de/",
                                 ["https://www.google.de/"])
        self.assertEqual(cm.exception.code, 1)

    def test_crawl_links_from_url(self):
        self.assertIsInstance(crawl_links_from_url(url_string, string), list)

    def test_crawl_links_from_url2(self):
        self.assertTrue(crawl_links_from_url(url_string, string))


# Unittests for download_file():

    def test_download_csv_csv_not_https(self):
        with self.assertRaises(SystemExit) as cm:
            download_csv(string, ".\\data\\test.csv")
        self.assertEqual(cm.exception.code, 1)

    def test_download_csv_output_path_not_string(self):
        with self.assertRaises(SystemExit) as cm:
            download_csv(url_string, 1)
        self.assertEqual(cm.exception.code, 1)


# Unitests for call_archiv():

    def test_call_archiv_path_not_string(self):
        with self.assertRaises(SystemExit) as cm:
            call_archiv(liste)
        self.assertEqual(cm.exception.code, 1)

    def test_call_archiv_path_dont_exists(self):
        with self.assertRaises(SystemExit) as cm:
            call_archiv(wrong_path)
        self.assertEqual(cm.exception.code, 1)

    def test_call_archiv(self):
        self.assertTrue(call_archiv(path))


# Unittest for csv_sum_columne():

    def test_csv_sum_columne_file_not_csv(self):
        with self.assertRaises(SystemExit) as cm:
           csv_sum_columnes(txt_testlist, "faelle_covid_aktuell")
        self.assertEqual(cm.exception.code, 1)

    def test_csv_sum_columne_searched_item_not_string(self):
        with self.assertRaises(SystemExit) as cm:
            csv_sum_columnes(csv_testlist, 1)
        self.assertEqual(cm.exception.code, 1)

    def test_csv_sum_columne(self):
        self.assertTrue(csv_sum_columnes(csv_testlist, "faelle_covid_aktuell"))


#Unittest for generate_timelabel_dataframe():

    def test_generate_timelabel_dataframe_not_list(self):
        with self.assertRaises(SystemExit) as cm:
            generate_timelabel_dataframe(string, start_date[0][-14:-4], end_date[-1][-14:-4])
        self.assertEqual(cm.exception.code, 1)

    def test_generate_timelabel_start_date_not_str(self):
        with self.assertRaises(SystemExit) as cm:
            generate_timelabel_dataframe(csv_testlist, liste, end_date[-1][-14:-4])
        self.assertEqual(cm.exception.code, 1)

    def test_generate_timelabel_end_date_not_str(self):
        with self.assertRaises(SystemExit) as cm:
            generate_timelabel_dataframe(csv_testlist, start_date[0][-14:-4], liste)
        self.assertEqual(cm.exception.code, 1)



if __name__ == '__main__':
    unittest.main()
