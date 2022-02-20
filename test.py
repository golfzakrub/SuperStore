import unittest
from managerTest import Manager
import pandas 
class Test(unittest.TestCase):
    
    def setUp(self):
        self.manager = Manager()

    def test_check_read_file(self):
        self.assertIsInstance(self.manager.readData('Super2.csv'),
        pandas.core.frame.DataFrame)

    def test_check_split_date(self):
        Dimension = ['Ship Date','Order Date']
        all_data = self.manager.readData('Super2.csv')
        self.assertIsInstance(self.manager.split_date(Dimension,all_data),
        pandas.core.frame.DataFrame)

    def test_get_backup(self):
        file = 'data_head.json'
        self.assertIsInstance(self.manager.get_backup(file),dict)



    


if __name__ == "__main__":
    unittest.main()
