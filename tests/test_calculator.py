import unittest

from calculator import add

class calc(unittest.TestCase):
    
    def test_empty(self):
        self.assertEqual(add(""),0)
        
    def test_one_num(self):
        self.assertEqual(add("5"),5)
        
    def test_two_nums(self):
        self.assertEqual(add("1,2"),3)
        
    def test_multi_nums(self):
        self.assertEqual(add("1,2,3"),6)
        
    def test_newline(self):
        self.assertEqual(add("1\n2,3"), 6)
        
    def test_custom_delimiter(self):
        self.assertEqual(add("//;\n1;2"),3)
        
    def test_negative(self):
        with self.assertRaisesRegex(ValueError,"negatives not allowed: -2"):
            add("1,-2,3")
            
    def test_multi_negatives(self):
        with self.assertRaisesRegex(ValueError,"negatives not allowed: -2,-3"):
            add("1,-2,-3")
    
    def test_over_1001_num(self):
        self.assertEqual(add("2,1001"), 2)
    
    def test_include_1000(self):
        self.assertEqual(add("2,1000"), 1002)
        
    def test_long_delimiter(self):
        self.assertEqual(add("//[***]\n1***2***3"), 6)

    def test_multiple_delimiters(self):
        self.assertEqual(add("//[*][%]\n1*2%3"), 6)
    
    def test_multiple_long_delimiters(self):
        self.assertEqual(add("//[**][%%]\n1**2%%3"), 6)
        
if __name__ == "__main__":
    unittest.main()