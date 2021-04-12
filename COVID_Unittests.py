import unittest
import pathlib
from COVID_DIVI_analyzer import call_archiv, csv_sum_columnes
from COVID_DIVI_crawler import download_csv


# TODO: pathlib
liste = ["1", "2", "3", "4"]
wrong_path = pathlib.Path(".\\data\\DIVI_data123\\")
csv_testlist = [pathlib.Path(".\\data\\test_data\\DIVI-testfile.csv")]
txt_testlist = [pathlib.Path(".\\data\\test_data\\DIVI-testfile.txt")]
path = pathlib.Path(".\\data\\DIVI_data\\")






class COVID_UnitTests(unittest.TestCase):


# Unittests for download_csv():

    def test_download_csv_not_dict(self):
        with self.assertRaises(SystemExit) as cm:
            download_csv(liste)
        self.assertEqual(cm.exception.code, 1)


# Unitests for call_archiv():

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


if __name__ == '__main__':

    unittest.main()
