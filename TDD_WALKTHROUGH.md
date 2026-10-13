# String Calculator Kata — Python `unittest` TDD Guide

This guide documents the **current class-based `unittest` approach** in [this repository](https://github.com/SLMakomazi/string-calculator-kata). It follows the requirements in the order of the 21 tests in `tests/test_calculator.py`, explaining RED → GREEN → REFACTOR and the code in `calculator.py`.

> **History:** The project originally used pytest-style free functions. The developer switched to `unittest.TestCase` with `self.assertEqual` and `self.assertRaisesRegex`. This guide explains the new version. Intermediate RED/GREEN snippets are teaching reconstructions, **not claims that each version was separately committed**. The final repository code implements all 21 scenarios.

## 1. Getting started

### Project structure

```text
string-calculator-kata/
├── calculator.py             # production code: add(numbers)
├── tests/
│   └── test_calculator.py    # unittest.TestCase and 21 tests
├── requirements.txt          # previous pytest dependency remains optional
└── TDD_WALKTHROUGH.md        # this guide
```

`unittest` comes with Python: **no additional test library is needed**.

From the project root, with your virtual environment activated:

```bash
python -m unittest discover -s tests -p "test_*.py" -v
```

Or, if you want to run the test file directly:

```bash
python tests/test_calculator.py
```

Expected result after all changes: **21 tests, OK**. `pytest` may also discover `unittest.TestCase` tests if installed, but the primary runner for this approach is `unittest`.

### Anatomy of a test

```python
import unittest
from calculator import add


class TestCalculator(unittest.TestCase):
    def test_empty_string_returns_zero(self):
        self.assertEqual(add(""), 0)
```

- `import unittest`: loads Python's built-in test framework.
- `from calculator import add`: imports the real function being tested.
- `class TestCalculator(unittest.TestCase)`: groups related tests into a class inheriting assertion helpers from `TestCase`.
- `def test_...(self):`: a test method; `self` is the current test-class instance.
- `self.assertEqual(actual, expected)`: checks that both values are equal. If not, the test **fails**.
- `self.assertRaisesRegex(ValueError, "message")`: checks that a block raises `ValueError` with a matching message.

**Parameters vs arguments:** `numbers` in `def add(numbers)` is a parameter. `"5"` in `add("5")` is an argument. `return` sends the computed value to the caller; it is not the same as `print()`.

## 2. TDD: RED → GREEN → REFACTOR

**RED:** Add a test for the next requirement, run it, and observe the expected failure.  
**GREEN:** Write the simplest implementation that makes the new test pass **without breaking older tests**.  
**REFACTOR:** Simplify or generalize the code, then run the full suite again.

```bash
python -m unittest discover -s tests -v
```

The output says `FAIL` for a failed assertion, `ERROR` for unexpected exceptions/import errors, and `ok` for passing tests. An `ERROR` during import is not the same as an assertion failure.

## 3. Requirement 1 — Empty input (test 1)

```python
def test_empty_string_returns_zero(self):
    self.assertEqual(add(""), 0)
```

**RED:** With no `add` function, importing it causes an import error. With a stub:

```python
def add(numbers):
    pass
```

the test fails because the function implicitly returns `None`, and `None != 0`.

**GREEN:**

```python
def add(numbers):
    return 0
```

**REFACTOR:** None needed. The one-line solution satisfies only this requirement.

## 4. Requirement 2 — Single number (test 2)

```python
def test_single_number_returns_value(self):
    self.assertEqual(add("5"), 5)
```

**RED:** `return 0` produces `0` instead of `5`.

**GREEN:**

```python
def add(numbers):
    if numbers == "":
        return 0
    return int(numbers)
```

`int("5")` converts text into an integer. **REFACTOR:** No `else` is needed after a `return`, because the function stops at that point.

## 5. Requirement 3 — Two comma-separated numbers (test 3)

```python
def test_two_numbers(self):
    self.assertEqual(add("1,2"), 3)
```

**RED:** `int("1,2")` raises `ValueError`.

**GREEN:** Split the string, convert each piece, and add:

```python
values = numbers.split(",")
total = 0
for value in values:
    total += int(value)
return total
```

Keep the early empty-input check. **REFACTOR:** The same loop works for one number, so the separate `return int(numbers)` is no longer needed.

## 6. Requirement 4 — Arbitrary count (test 4)

```python
def test_multiple_numbers(self):
    self.assertEqual(add("1,2,3,4,5"), 15)
```

**RED:** A two-number-only implementation would fail; the loop-based implementation from test 3 **already passes** this test.

**GREEN:** No additional change if you used `split` and `for`. **REFACTOR:** Prefer the general loop to hard-coded `a + b`. The list `["1", "2", "3", "4", "5"]` is processed one element at a time.

## 7. Requirement 5 — Mixed newline and comma (test 5)

```python
def test_newline_delimiter(self):
    self.assertEqual(add("1\n2,3"), 6)
```

`\n` is a newline character.

**RED:** Splitting only on commas leaves `"1\n2"` together; integer conversion fails.

**GREEN (intermediate):**

```python
numbers = numbers.replace("\n", ",")
values = numbers.split(",")
```

**REFACTOR:** Normalize separators once before the sum, rather than write two separate addition algorithms.

## 8. Requirement 6 — Multiple newlines (test 6)

```python
def test_multiple_newlines(self):
    self.assertEqual(add("1\n2\n3"), 6)
```

**RED:** Fails if newline handling only replaces one occurrence. **GREEN:** Python's `replace("\n", ",")` replaces **all** occurrences, so the previous implementation already passes. **REFACTOR:** No additional change.

## 9. Requirement 7 — One custom delimiter (test 7)

```python
def test_custom_delimiter(self):
    self.assertEqual(add("//;\n1;2"), 3)
```

The syntax is `//<delimiter>\n<numbers>`. The header `//;` declares `;`.

**RED:** The default comma/newline splitter does not parse the header or semicolon.

**GREEN (intermediate):**

```python
delimiter = ","
if numbers.startswith("//"):
    header, numbers = numbers.split("\n", 1)
    delimiter = header[2:]
else:
    numbers = numbers.replace("\n", ",")

values = numbers.split(delimiter)
```

`startswith("//")` detects the header. `split("\n", 1)` splits at the **first** newline. `header[2:]` removes `//`. **REFACTOR:** Keep parsing the header separate from adding the numbers.

## 10. Requirement 8 — Custom delimiter with several values (test 8)

```python
def test_custom_delimiter_with_multiple_numbers(self):
    self.assertEqual(add("//|\n1|2|3"), 6)
```

**RED:** A parser hard-coded for semicolons would fail. **GREEN:** The generic `delimiter = header[2:]` approach already supports `|`. **REFACTOR:** Reuse the existing splitting and sum loop.

## 11. Requirement 9 — Reject a negative (test 9)

```python
def test_single_negative_number(self):
    with self.assertRaisesRegex(ValueError, "negatives not allowed: -2"):
        add("1,-2,3")
```

**RED:** Without validation, `add("1,-2,3")` returns `2` instead of raising.

**GREEN:** Convert values and collect negatives:

```python
total = 0
negatives = []
for value in values:
    number = int(value)
    if number < 0:
        negatives.append(number)
    else:
        total += number

if negatives:
    negative_list = ",".join(str(n) for n in negatives)
    raise ValueError(f"negatives not allowed: {negative_list}")
return total
```

`with self.assertRaisesRegex(...):` expects an exception inside the indented block. `raise ValueError(...)` creates that exception. **REFACTOR:** Convert each token to `int` only once.

## 12. Requirement 10 — Report every negative (test 10)

```python
def test_multiple_negative_numbers(self):
    with self.assertRaisesRegex(ValueError, "negatives not allowed: -2,-5"):
        add("1,-2,3,-5")
```

**RED:** A version that raises immediately on the first negative cannot report `-5`.

**GREEN:** Append all negatives during the loop, then raise **after** it. The list `[-2, -5]` becomes the string `"-2,-5"` via `",".join(str(n) for n in negatives)`. **REFACTOR:** One exception reports the entire invalid set.

## 13. Requirement 11 — Ignore numbers above 1000 (test 11)

```python
def test_numbers_greater_than_1000_are_ignored(self):
    self.assertEqual(add("2,1001"), 2)
```

**RED:** The previous sum would be 1003.

**GREEN:** In the loop, replace the plain `else` with:

```python
if number < 0:
    negatives.append(number)
elif number <= 1000:
    total += number
```

**REFACTOR:** Keep validation and filtering in one loop. Values above 1000 are skipped; negatives are still rejected.

## 14. Requirement 12 — Exactly 1000 counts (test 12)

```python
def test_1000_is_included(self):
    self.assertEqual(add("2,1000"), 1002)
```

**RED:** A mistaken `number < 1000` condition would return 2. **GREEN:** Use `<= 1000`. **REFACTOR:** This boundary test protects against off-by-one mistakes.

## 15. Requirement 13 — Delimiter of any length (test 13)

```python
def test_delimiter_of_any_length(self):
    self.assertEqual(add("//[***]\n1***2***3"), 6)
```

The bracketed `[***]` declares the delimiter `***`, not literal square brackets.

**RED:** `header[2:]` alone produces `"[***]"`, which is not the separator in the body.

**GREEN:** Introduce `import re` and extract bracketed delimiters:

```python
if delimiter_definition.startswith("["):
    delimiters = re.findall(r"\[([^\]]+)\]", delimiter_definition)
else:
    delimiters = [delimiter_definition]

pattern = "|".join(re.escape(d) for d in delimiters)
values = re.split(pattern, numbers)
```

`re.findall` extracts `***`; `re.escape` treats `*` as literal text; `re.split` splits using the regex pattern. **REFACTOR:** Generalize the splitter instead of duplicating the arithmetic.

## 16. Requirement 14 — Multiple custom delimiters (test 14)

```python
def test_multiple_custom_delimiters(self):
    self.assertEqual(add("//[*][%]\n1*2%3"), 6)
```

**RED:** A one-delimiter-only parser cannot split both `*` and `%`. **GREEN:** `re.findall` returns `["*", "%"]`; joining escaped patterns with `|` means **either delimiter**. **REFACTOR:** Keep one regex-based splitter.

## 17. Requirement 15 — Several delimiters of any length (test 15)

```python
def test_multiple_delimiters_of_any_length(self):
    self.assertEqual(add("//[**][%%]\n1**2%%3"), 6)
```

**RED:** Hard-coding a one-character delimiter fails. **GREEN:** The regex list already handles `**` and `%%`. **REFACTOR:** In the final code, `sorted(delimiters, key=len, reverse=True)` tries longer delimiters first when one delimiter begins with another.

## 18. Regression tests — tests 16–20

These tests exercise edge cases and combinations of already implemented requirements. **In the earlier learning session, they passed when added**, so it would be inaccurate to invent a failing RED stage for them.

| # | Test method | Expected behavior | GREEN / REFACTOR significance |
|---|---|---|---|
| 16 | `test_zero` | `add("0") == 0` | Confirms a numeric zero works independently of empty input |
| 17 | `test_only_numbers_above_1000` | `add("1001,2000") == 0` | Confirms filtering can skip every number |
| 18 | `test_negative_number_with_custom_delimiter` | `add("//;\n1;-3;2")` raises `ValueError` mentioning `-3` | Confirms custom parsing still uses negative validation |
| 19 | `test_long_delimiter_with_special_characters` | `add("//[***]\n10***20***30") == 60` | Confirms `re.escape` handles regex-special characters |
| 20 | `test_multiple_delimiters_with_different_lengths` | `add("//[***][%]\n1***2%3") == 6` | Confirms multiple delimiters with different lengths |

**RED:** No new failure occurred when these were added to the working solution. **GREEN:** No new implementation needed. **REFACTOR:** Their presence makes future refactoring safer by guarding existing behavior.

## 19. Requirement 21 — Newlines after custom headers

```python
def test_custom_delimiter_with_newline(self):
    self.assertEqual(add("//;\n1;2\n3"), 6)
```

**RED:** A custom-header implementation that sets `delimiters = [";"]` leaves `"2\n3"` unsplit, causing `ValueError`.

**GREEN:** After extracting custom delimiters, add:

```python
delimiters.append("\n")
```

**REFACTOR:** The common regex splitting logic now supports newline with custom delimiters. **Important:** The final code keeps newline but replaces comma when a custom header is present. That matches the 21 documented cases; other interpretations need a separate test and specification.

## 20. Final `calculator.py` explained

```python
import re


def add(numbers):
    """Sum integers in a delimited string, following the String Calculator Kata."""
    if numbers == "":
        return 0

    delimiters = [",", "\n"]

    if numbers.startswith("//"):
        header, numbers = numbers.split("\n", 1)
        delimiter_definition = header[2:]

        if delimiter_definition.startswith("["):
            delimiters = re.findall(r"\[([^\]]+)\]", delimiter_definition)
        else:
            delimiters = [delimiter_definition]

        delimiters.append("\n")

    # Escape special regex characters; prefer longer delimiters if they overlap.
    pattern = "|".join(re.escape(delimiter) for delimiter in sorted(delimiters, key=len, reverse=True))
    values = re.split(pattern, numbers)

    total = 0
    negatives = []

    for value in values:
        number = int(value)
        if number < 0:
            negatives.append(number)
        elif number <= 1000:
            total += number

    if negatives:
        negative_list = ",".join(str(number) for number in negatives)
        raise ValueError(f"negatives not allowed: {negative_list}")

    return total
```

### Trace a real input

For `add("//[***][%]\n1***2%3")`:

1. Not empty → continue.
2. `startswith("//")` → yes; separate `header = "//[***][%]"` and `numbers = "1***2%3"`.
3. `header[2:]` → `"[***][%]"`.
4. `re.findall(...)` → `["***", "%"]`.
5. Append `"\n"`; escape each delimiter and join them into a regex pattern.
6. `re.split(...)` → `["1", "2", "3"]`.
7. Convert each token to an integer. No negatives or values over 1000.
8. Sum `1 + 2 + 3` → return **6**.

### Common Python concepts

| Concept | Explanation |
|---|---|
| `def` | Define a function |
| `return` | End function and send value to caller |
| `if` / `elif` | Conditional execution |
| `split` | Break a string into parts |
| `[2:]` | Slice off the first two characters |
| `[]` | Create a list |
| `for` | Iterate over items |
| `int` | Convert numeric text to an integer |
| `+=` | Add to the current total |
| `append` | Add an item to a list |
| `re.escape` | Make delimiter text safe for regex matching |
| `re.split` | Split on several possible separators |
| `raise` | Throw an exception |
| `self.assertEqual` | Test value equality |
| `self.assertRaisesRegex` | Test exception type and message |

## 21. Test order in the actual `unittest` class

The methods are **written** in this requirement order, although `unittest` normally **executes test methods alphabetically by name**. The explanation below follows the written/learning order, not the console's execution order.

| # | Test method | Requirement |
|---|---|---|
| 1 | `test_empty_string_returns_zero` | Empty input |
| 2 | `test_single_number_returns_value` | One number |
| 3 | `test_two_numbers` | Two numbers |
| 4 | `test_multiple_numbers` | Many numbers |
| 5 | `test_newline_delimiter` | Comma and newline |
| 6 | `test_multiple_newlines` | Repeated newline |
| 7 | `test_custom_delimiter` | Semicolon |
| 8 | `test_custom_delimiter_with_multiple_numbers` | Pipe |
| 9 | `test_single_negative_number` | One negative exception |
| 10 | `test_multiple_negative_numbers` | All negative values |
| 11 | `test_numbers_greater_than_1000_are_ignored` | Ignore >1000 |
| 12 | `test_1000_is_included` | Include 1000 |
| 13 | `test_delimiter_of_any_length` | Long bracket delimiter |
| 14 | `test_multiple_custom_delimiters` | Multiple separators |
| 15 | `test_multiple_delimiters_of_any_length` | Multiple long separators |
| 16 | `test_zero` | Zero boundary |
| 17 | `test_only_numbers_above_1000` | All ignored |
| 18 | `test_negative_number_with_custom_delimiter` | Combined negative/custom |
| 19 | `test_long_delimiter_with_special_characters` | Regex escaping |
| 20 | `test_multiple_delimiters_with_different_lengths` | Mixed lengths |
| 21 | `test_custom_delimiter_with_newline` | Newline with custom |

## 22. Troubleshooting and Git workflow

**Typical failures:**

- `ImportError`: `add` not defined or incorrect import.
- `AssertionError: 0 != 5`: actual result differs from expected.
- `ValueError: invalid literal for int()`: the delimiter was not split correctly or the input is malformed.
- `SyntaxError: 'return' outside function`: incorrect indentation.
- `self.assertRaisesRegex` fails: no exception, wrong exception type, or message does not match.
- `git diff --check` reports trailing whitespace: formatting cleanup needed; tests can still pass.

**Unspecified cases:** The 21 tests do not define behavior for malformed input such as `"1,,2"`, missing custom headers, or empty bracketed delimiters. Don't claim those cases are supported without additional tests.

To sync your Mac with the GitHub updates:

```bash
git status
git pull --ff-only origin main
python -m unittest discover -s tests -p "test_*.py" -v
code TDD_WALKTHROUGH.md
```

If `git status` shows uncommitted local changes, save or review them before pulling.

## 23. Short presentation script

> “I changed the Kata to Python's built-in `unittest` framework. I group the tests in `TestCalculator(unittest.TestCase)` and use `self.assertEqual` for normal results and `self.assertRaisesRegex` for negative-number exceptions. I followed the TDD idea of writing a test, seeing the expected failure, making it pass, and simplifying the code. I started with an empty string and a single number, then added multiple numbers, newline and custom delimiters, negative validation, the 1000 boundary, and bracketed multiple delimiters. The final implementation uses `re.split` for general delimiter parsing, and the 21 tests protect those requirements from regressions.” 
