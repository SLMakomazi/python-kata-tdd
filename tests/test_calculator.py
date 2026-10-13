from calculator import add
import unittest

class TestCalculator(unittest.TestCase):
    def test_empty_string_returns_zero(self):
        self.assertEqual(add(""), 0)
        
    def test_single_number_returns_value(self):
        self.assertEqual(add("5"), 5)
        
    
