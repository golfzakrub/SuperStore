from fileinput import filename
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
        self.assertTrue(self.manager.split_date(Dimension,all_data))

    def test_get_backup(self):
        file = 'data_head.json'
        self.assertIsInstance(self.manager.get_backup(file),dict)


    def test_readUnionData(self): #return len
        filename = 'Super2.csv' # Super2.csv have 100 index
        filename_union = 'Super1.csv' # Super1.csv have 200 index
        self.assertEqual(self.manager.readUnionData(filename,filename_union),200)
        
        
    def test_filter(self):
        data = ["South"]
        item = "Region"
        self.assertTrue(self.manager.getDataFilter(data,item))
        
    def test_md5(self):
        namefile = 'Super2'
        pathfile = 'F:\_coding\softdev2\week3\SianStoreReal\SuperStore\Super2.csv'
        data_head = {"Super2": {"Dimension": ["Row ID", "Order ID", "Order Date", "Ship Date", "Ship Mode", "Customer ID", "Customer Name", "Segment", "Country/Region", "City", "State", "Postal Code", "Region", "Product ID", "Category", "Sub-Category", "Product Name"], "Measurement": ["Sales", "Quantity", "Discount", "Profit"], "md5": "c6a410b95fd63be1e41275a7dc4ec820"}, "Super1": {"Dimension": ["Row ID", "Order ID", "Order Date", "Ship Date", "Ship Mode", "Customer ID", "Customer Name", "Segment", "Country/Region", "State", "Postal Code", "Region", "Product ID", "Category", "Sub-Category", "Product Name"], "Measurement": ["Sales", "Quantity", "Discount", "Profit", "City"], "md5": "9e319c5b721ae839558d339338d2d31b"}}
        self.assertTrue(self.manager.check_md5(namefile,pathfile,data_head))

        
    


if __name__ == "__main__":
    unittest.main()
