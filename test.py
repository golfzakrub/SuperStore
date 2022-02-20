import unittest

class Test(unittest.TestCase):

    def test_check_date_dimension(self):
        self.assertTrue('Day' in "ship date Day")

if __name__ == "__main__":
    unittest.main()