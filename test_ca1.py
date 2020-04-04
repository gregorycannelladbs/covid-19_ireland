# -*- coding: utf-8 -*-
"""
Created on Tue Mar 31 17:54:04 2020

@author: Greg
"""

import unittest
import ca1

class TestCA1(unittest.TestCase):
    
    def test_missing_values(self):
        lst = ca1.missing_values(list(range(0,50)))
       
        # indexes of missing values
        indexes = sorted(list(range(3,50,5)) + list(range(4,50,5)))
        
        # 50 values + 20 values inserted = 70 values
        self.assertEqual(len(lst), 70)
        # check index of missing values and check that inseted value = 0
        for i in indexes:
            self.assertEqual(lst[i], 0)

    def test_to_matrix(self):
        lst = list(range(0,50))
        matrix = ca1.to_matrix(lst, 5)
        
        # check that the object created is a list made of sub lists of length 5
        self.assertIsInstance(matrix, list)
        for sub_list in matrix:
            self.assertIsInstance(sub_list, list)
            self.assertTrue(len(sub_list), 5)
            
    def test_get_data(self):
        soup = ca1.get_soup()
        data = ca1.get_data(soup)
        
        # check that header values are all strings
        for i in range(0,5):
            self.assertIsInstance(data[i], str)
        
        # check that first column valuesn are all strings
        first_column_values = [data[i] for i in range(5, len(data), 5)]
        for value in first_column_values:
            self.assertIsInstance(value, str)
        
        # check that all other column values are all numbers >= 0
        data_indexes = list(range(5, len(data)))
        other_columns_values = [data[index] for index in data_indexes if index not in range(5, len(data), 5)]
        for value in other_columns_values:
            self.assertTrue(value >= 0)
        
        # check that values in second and fourth columns are all integers
        second_column_values = [data[index] for index in list(range(7, len(data), 5))]
        fourth_column_values = [data[index] for index in list(range(8, len(data), 5))]
        for value in second_column_values and fourth_column_values:
            self.assertIsInstance(value, int)
    
    def test_save_csv(self):
        # create and save matrix
        matrix = [["I", "can", "save", "a", "matrix"], ["I", "can", "save", "a", "matrix"]]
        ca1.save_csv(matrix, path= "test_output.csv")
        # read the saved filed
        saved_file = [line.strip() for line in open('test_output.csv', 'r')]
        # concatenate elements of sub_lists in my matrix
        lines_in_matrix = [",".join(sub_list) for sub_list in matrix]
        # check that the element of 
        self.assertEqual(lines_in_matrix, saved_file)

if __name__ == '__main__':
    unittest.main()
