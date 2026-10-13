from calculator import add
import pytest

def test_empty_string_returns_zero():
    result = add("")

    assert result == 0
    
def test_single_number_returns_its_value():
    result = add("5")

    assert result == 5
    
def test_two_numbers():
    assert add("1,2") == 3


def test_multiple_numbers():
    assert add("1,2,3,4,5") == 15
    
def test_newline_delimiter():
    assert add("1\n2,3") == 6

def test_multiple_newlines():
    assert add("1\n2\n3") == 6
    
def test_custom_delimiter():
    assert add("//;\n1;2") == 3

def test_custom_delimiter_with_multiple_numbers():
    assert add("//|\n1|2|3") == 6
    
def test_single_negative_number():
    with pytest.raises(ValueError, match="negatives not allowed: -2"):
        add("1,-2,3")

def test_multiple_negative_numbers():
    with pytest.raises(ValueError, match="negatives not allowed: -2,-5"):
        add("1,-2,3,-5")

def test_numbers_greater_than_1000_are_ignored():
    assert add("2,1001") == 2

def test_1000_is_included():
    assert add("2,1000") == 1002
    
def test_delimiter_of_any_length():
    assert add("//[***]\n1***2***3") == 6


def test_multiple_custom_delimiters():
    assert add("//[*][%]\n1*2%3") == 6


def test_multiple_delimiters_of_any_length():
    assert add("//[**][%%]\n1**2%%3") == 6
    
def test_zero():
    assert add("0") == 0


def test_only_numbers_above_1000():
    assert add("1001,2000") == 0


def test_negative_number_with_custom_delimiter():
    with pytest.raises(ValueError, match="negatives not allowed: -3"):
        add("//;\n1;-3;2")


def test_long_delimiter_with_special_characters():
    assert add("//[***]\n10***20***30") == 60


def test_multiple_delimiters_with_different_lengths():
    assert add("//[***][%]\n1***2%3") == 6
    
def test_custom_delimiter_with_newline():
    assert add("//;\n1;2\n3") == 6