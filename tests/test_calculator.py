import unittest

from calculator import add


class TestCalculator(unittest.TestCase):
    def test_empty_string_returns_zero(self):
        self.assertEqual(add(""), 0)

    def test_single_number_returns_value(self):
        self.assertEqual(add("5"), 5)

    def test_two_numbers(self):
        self.assertEqual(add("1,2"), 3)

    def test_multiple_numbers(self):
        self.assertEqual(add("1,2,3,4,5"), 15)

    def test_newline_delimiter(self):
        self.assertEqual(add("1\n2,3"), 6)

    def test_multiple_newlines(self):
        self.assertEqual(add("1\n2\n3"), 6)

    def test_custom_delimiter(self):
        self.assertEqual(add("//;\n1;2"), 3)

    def test_custom_delimiter_with_multiple_numbers(self):
        self.assertEqual(add("//|\n1|2|3"), 6)

    def test_single_negative_number(self):
        with self.assertRaisesRegex(ValueError, "negatives not allowed: -2"):
            add("1,-2,3")

    def test_multiple_negative_numbers(self):
        with self.assertRaisesRegex(ValueError, "negatives not allowed: -2,-5"):
            add("1,-2,3,-5")

    def test_numbers_greater_than_1000_are_ignored(self):
        self.assertEqual(add("2,1001"), 2)

    def test_1000_is_included(self):
        self.assertEqual(add("2,1000"), 1002)

    def test_delimiter_of_any_length(self):
        self.assertEqual(add("//[***]\n1***2***3"), 6)

    def test_multiple_custom_delimiters(self):
        self.assertEqual(add("//[*][%]\n1*2%3"), 6)

    def test_multiple_delimiters_of_any_length(self):
        self.assertEqual(add("//[**][%%]\n1**2%%3"), 6)

    def test_zero(self):
        self.assertEqual(add("0"), 0)

    def test_only_numbers_above_1000(self):
        self.assertEqual(add("1001,2000"), 0)

    def test_negative_number_with_custom_delimiter(self):
        with self.assertRaisesRegex(ValueError, "negatives not allowed: -3"):
            add("//;\n1;-3;2")

    def test_long_delimiter_with_special_characters(self):
        self.assertEqual(add("//[***]\n10***20***30"), 60)

    def test_multiple_delimiters_with_different_lengths(self):
        self.assertEqual(add("//[***][%]\n1***2%3"), 6)

    def test_custom_delimiter_with_newline(self):
        self.assertEqual(add("//;\n1;2\n3"), 6)


if __name__ == "__main__":
    unittest.main()
