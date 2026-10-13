from calculator import add

def test_empty_string_returns_zero():
    result = add("")

    assert result == 0