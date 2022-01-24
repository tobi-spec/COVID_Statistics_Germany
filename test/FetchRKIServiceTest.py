import csv
import os.path
import unittest
import shutil
from src import FetchRKIService


class FetchRKIServiceTest(unittest.TestCase):

    def setUp(self):
        os.mkdir("./testdata")

    def tearDown(self):
        shutil.rmtree("./testdata")

    # test_create_directory_no_string

    def test_create_directory(self):
        test_directory = "./testdata/test"
        FetchRKIService.create_directory(test_directory)
        self.assertTrue(os.path.exists("testdata/test"))

    def test_save_csv_no_directory(self):
        test_directory = "./testdata/test"
        test_filename = "file.csv"
        false_string = "this is a string"
        with self.assertRaises(SystemExit) as cm:
            FetchRKIService.save_csv(test_directory, test_filename, false_string)
        self.assertEqual(cm.exception.code, "directory does not exist")

    def test_save_csv_no_filename(self):
        test_directory = "./testdata"
        test_filename = 1
        false_string = "this is a string"
        with self.assertRaises(SystemExit) as cm:
            FetchRKIService.save_csv(test_directory, test_filename, false_string)
        self.assertEqual(cm.exception.code, "filename must be string")

    def test_save_csv_endswith_csv(self):
        test_directory = "./testdata/"
        test_filename = "file"
        test_string = "this is a string"
        with self.assertRaises(SystemExit) as cm:
            FetchRKIService.save_csv(test_directory, test_filename, test_string)
        self.assertEqual(cm.exception.code, "filename must end with .csv")

    def test_save_csv_no_string(self):
        test_directory = "./testdata/"
        test_filename = "file.csv"
        false_string = 1
        with self.assertRaises(SystemExit) as cm:
            FetchRKIService.save_csv(test_directory, test_filename, false_string)
        self.assertEqual(cm.exception.code, "only strings can saved in csv")

    def test_save_csv(self):
        test_directory = "./testdata/"
        test_filename = "file.csv"
        test_string = "this is a string"
        FetchRKIService.save_csv(test_directory, test_filename, test_string)
        with open("./testdata/file.csv", "r") as file:
            reader = csv.reader(file)
            for row in reader:
                self.assertEqual(row[0], "this is a string")


if __name__ == '__main__':
    unittest.main()
