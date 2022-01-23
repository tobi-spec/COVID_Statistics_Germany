import os.path
import unittest
import shutil
from src import FetchRKIService


class FetchRKIServiceTest(unittest.TestCase):

    def test_create_directory(self):
        test_directory = "./data/test"
        FetchRKIService.create_directory(test_directory)
        self.assertTrue(os.path.exists("data/test"))
        shutil.rmtree("./data/")


if __name__ == '__main__':
    unittest.main()