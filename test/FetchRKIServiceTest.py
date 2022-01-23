import os.path
import unittest
import shutil
from src import FetchRKIService
from unittest.mock import patch


class FetchRKIServiceTest(unittest.TestCase):

    def test_create_directory(self):
        test_directory = "./data/test"
        FetchRKIService.create_directory(test_directory)
        self.assertTrue(os.path.exists("data/test"))
        shutil.rmtree("./data/")

    def test_save_csv_no_string(self):
        test_directory = "data/test"
        false_string = 1
        with self.assertRaises(SystemExit) as cm:
            FetchRKIService.save_csv(test_directory, false_string)
        self.assertEqual(cm.exception.code, "only strings can saved in csv")

if __name__ == '__main__':
    unittest.main()