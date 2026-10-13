# String Calculator Kata — Complete Beginner's TDD Walkthrough

> **Repository:** [SLMakomazi/string-calculator-kata](https://github.com/SLMakomazi/string-calculator-kata)  
> **Language:** Python 3.13 • **Test runner:** pytest 8.4.2  
> **Source of truth:** `calculator.py` and `tests/test_calculator.py` on `main`, reviewed after commit `154f14e`.  
> **Observed result:** 21 passed (terminal output supplied by the developer).

## 1. What the project does

We built one function, `add(numbers)`, where **the input is a string** and **the output is an integer**. It accepts numbers separated by commas, newlines, or an explicitly declared delimiter. It rejects negative values and ignores positive values above 1000.

Examples:

```python
add("")                        # 0
add("5")                       # 5
add("1,2,3")                   # 6
add("1\n2,3")                  # 6
add("//;\n1;2")                # 3
add("//[***]\n1***2***3")      # 6
add("//[*][%]\n1*2%3")         # 6
add("2,1001")                  # 2
add("2,1000")                  # 1002
add("1,-2,3")                  # raises ValueError
```

**The input `"5"` is text, not the integer `5`.** That is why we eventually use `int(value)`.

### File layout

```text
string-calculator-kata/
├── calculator.py             # actual implementation
├── tests/
│   └── test_calculator.py    # checks what the function must do
├── requirements.txt          # pytest and related dependencies
└── TDD_WALKTHROUGH.md        # this teaching guide
```

Your learning scratch file `practise.py` was used earlier for Python basics; it is not part of the calculator's automated test suite.

## 2. TDD: RED → GREEN → REFACTOR

1. **RED:** Write a test expressing the next requirement. Run pytest; ensure it fails for the expected reason. A failure can be an assertion failure or initially a test-collection error, but those are different signals.
2. **GREEN:** Write the *simplest sufficient* implementation to pass that test **and all earlier tests**.
3. **REFACTOR:** Make the code easier to understand without changing its behavior; run all tests again.

```bash
python -m pytest -v           # detailed names + PASS/FAIL
python -m pytest -q           # brief summary
python -m pytest -x -v        # stop on first failure
```

`test_...` tells pytest which functions are tests. `assert actual == expected` fails if they differ. `pytest.raises(ValueError)` checks exceptions.

> **History note:** These RED/GREEN code samples reconstruct the learning sequence followed in our session. They do **not** claim that each intermediate state exists as its own Git commit. The repository contains the final solution and the 21 tests.

## 3. Starting from zero: the import error and first RED

**Requirement:** An empty string returns zero.

We wrote in `tests/test_calculator.py`:

```python
from calculator import add

def test_empty_string_returns_zero():
    result = add("")
    assert result == 0
```

- `from calculator import add` loads the `add` function from `calculator.py`.
- `result = add("")` supplies an *empty string* argument.
- `assert result == 0` expresses the required outcome.

**Initial RED:** `calculator.py` was empty, so pytest could not import `add`. It said **`ImportError: cannot import name 'add'`** and **`collected 0 items / 1 error`**. This was an **import/collection error**, not yet a failed assertion.

We added a function stub:

```python
def add(numbers):
    pass
```

Now pytest collected the test and reported **`assert None == 0`**. `pass` does nothing; a function without `return` implicitly returns `None`. **This is a genuine failed assertion.**

**GREEN:**

```python
def add(numbers):
    return 0
```

Now `add("")` returns 0 and the first test passes. **REFACTOR:** Nothing to simplify yet. It is deliberately not a complete calculator.

## 4. Single number — test 2

**Requirement:** A string containing one number returns that number.

```python
def test_single_number_returns_its_value():
    result = add("5")
    assert result == 5
```

**RED:** With `return 0`, the assertion says **`assert 0 == 5`**.

**GREEN:**

```python
def add(numbers):
    if numbers == "":
        return 0
    return int(numbers)
```

- `if numbers == ""` handles empty input.
- `return` stops the function immediately.
- `int("5")` converts a numeric string to an integer.

**REFACTOR:** We do not need an `else` after a branch that returns. The second `return` is reached only when the input is nonempty.

## 5. Comma-separated numbers — tests 3 and 4

```python
def test_two_numbers():
    assert add("1,2") == 3

def test_multiple_numbers():
    assert add("1,2,3,4,5") == 15
```

**RED:** `int("1,2")` raises `ValueError`: a comma-separated string cannot be converted directly to one integer.

**GREEN:**

```python
def add(numbers):
    if numbers == "":
        return 0

    values = numbers.split(",")
    total = 0
    for value in values:
        total += int(value)
    return total
```

`"1,2,3".split(",")` becomes `["1", "2", "3"]`. The loop accumulates `0 → 1 → 3 → 6`.

**REFACTOR:** The same loop works for one number (`"5".split(",") == ["5"]`), so the old separate `return int(numbers)` branch is no longer necessary. All the calculation lines must be **indented within the function**; `return` must come **after** the loop.

## 6. Newline separators — tests 5 and 6

```python
def test_newline_delimiter():
    assert add("1\n2,3") == 6

def test_multiple_newlines():
    assert add("1\n2\n3") == 6
```

`\n` is the newline character. In `"1\n2,3"`, the input has a newline between 1 and 2.

**RED:** Splitting only on commas leaves `"1\n2"` as a chunk; `int("1\n2")` fails.

**GREEN:** Add this before splitting:

```python
numbers = numbers.replace("\n", ",")
values = numbers.split(",")
```

The input `"1\n2,3"` becomes `"1,2,3"`.

**REFACTOR:** Normalize delimiters rather than duplicating the summation loop. Later, the regex splitter replaces this normalization strategy entirely.

## 7. A custom one-character delimiter — tests 7 and 8

**Input syntax:** `//<delimiter>\n<numbers>`.

```python
def test_custom_delimiter():
    assert add("//;\n1;2") == 3

def test_custom_delimiter_with_multiple_numbers():
    assert add("//|\n1|2|3") == 6
```

**RED:** The comma/newline splitter does not understand the header `//;` or the separator `;`.

**GREEN (intermediate implementation):**

```python
delimiter = ","
if numbers.startswith("//"):
    header, numbers = numbers.split("\n", 1)
    delimiter = header[2:]
else:
    numbers = numbers.replace("\n", ",")

values = numbers.split(delimiter)
```

- `startswith("//")` detects a custom-delimiter header.
- `split("\n", 1)` splits at **only the first newline**, separating header from body.
- `header[2:]` discards the first two characters, `//`. For `"//;"`, that yields `";"`.
- Then we split the numbers using the chosen delimiter.

**REFACTOR:** Keep header-parsing separate from summing, so later delimiter enhancements do not touch arithmetic.

## 8. Negative numbers — tests 9 and 10

**Requirement:** Never silently accept negative numbers; report **all** negatives.

```python
def test_single_negative_number():
    with pytest.raises(ValueError, match="negatives not allowed: -2"):
        add("1,-2,3")

def test_multiple_negative_numbers():
    with pytest.raises(ValueError, match="negatives not allowed: -2,-5"):
        add("1,-2,3,-5")
```

**RED:** Earlier code happily summed negatives: `1 + (-2) + 3 = 2`; `pytest.raises` fails because no exception occurs.

**GREEN:** Collect negatives while processing values, then raise after checking every number:

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

- `[]` is an empty list.
- `.append(number)` stores a negative.
- `str(n)` turns each integer back into text for the message.
- `",".join(...)` builds the text `-2,-5`.
- `raise ValueError(...)` signals invalid input.

**REFACTOR:** Convert each token to an integer **once**, then reuse `number`. Delay raising until the loop finishes so the error can name every negative. The tests use `match=` (a regex check), not strict whole-string equality.

## 9. Numbers greater than 1000 — tests 11 and 12

```python
def test_numbers_greater_than_1000_are_ignored():
    assert add("2,1001") == 2

def test_1000_is_included():
    assert add("2,1000") == 1002
```

**RED:** The old loop adds 1001, incorrectly producing 1003 for `"2,1001"`.

**GREEN:** Replace the `else` in the summation loop with:

```python
if number < 0:
    negatives.append(number)
elif number <= 1000:
    total += number
```

`elif` means “otherwise, if …”. A value **equal to** 1000 is counted; 1001 and larger are skipped.

**REFACTOR:** The negative check comes first. Negative numbers cannot be hidden by an upper-bound filter.

## 10. A delimiter of any length — test 13

```python
def test_delimiter_of_any_length():
    assert add("//[***]\n1***2***3") == 6
```

**Requirement:** A delimiter such as `***` can be wrapped in square brackets.

**RED:** The single-character header parser treats the delimiter as `"[***]"`, which is not what separates the numbers.

**GREEN:** Introduce Python's regular-expression module:

```python
import re

delimiter_definition = header[2:]
if delimiter_definition.startswith("["):
    delimiters = re.findall(r"\[([^\]]+)\]", delimiter_definition)
else:
    delimiters = [delimiter_definition]

pattern = "|".join(re.escape(d) for d in delimiters)
values = re.split(pattern, numbers)
```

- `re.findall(...)` extracts the text **inside** each `[ ... ]`, e.g., `***`.
- `re.escape("***")` makes `*` literal rather than a regex repetition operator.
- `re.split(...)` divides the number string wherever a declared delimiter appears.

**REFACTOR:** Use **one list of delimiters** and **one `re.split` call**, rather than a different arithmetic path for each delimiter syntax.

## 11. Multiple custom delimiters — test 14

```python
def test_multiple_custom_delimiters():
    assert add("//[*][%]\n1*2%3") == 6
```

**RED:** A solution that supports only one delimiter will leave an unsplit `%` or `*` token.

**GREEN:** The new `re.findall(...)` already extracts **both** bracketed delimiters: `["*", "%"]`. Joining their escaped forms with `|` creates a regex choice: match one **or** the other.

**REFACTOR:** Reuse the general delimiter list from test 13; no new summation logic required.

## 12. Multiple delimiters with multiple characters — test 15

```python
def test_multiple_delimiters_of_any_length():
    assert add("//[**][%%]\n1**2%%3") == 6
```

**RED:** A naïve split on only `**` or only `%%` misses the other delimiter.

**GREEN:** The same regex list approach supports both.

**REFACTOR:** A single general splitting algorithm handles tests 13–15.

## 13. Extra regression coverage — tests 16–20

These validate boundaries and combinations already implied by the requirements. A **regression test** helps ensure later changes don't reintroduce an old bug.

| # | Test name | Input | Expected | Why it matters |
|---|---|---|---|---|
| 16 | `test_zero` | `"0"` | `0` | A real zero must not be confused with an empty input |
| 17 | `test_only_numbers_above_1000` | `"1001,2000"` | `0` | Every large value is omitted |
| 18 | `test_negative_number_with_custom_delimiter` | `"//;\n1;-3;2"` | `ValueError` mentioning `-3` | Negative validation works with custom splitting |
| 19 | `test_long_delimiter_with_special_characters` | `"//[***]\n10***20***30"` | `60` | Repeated `*` is safely escaped in regex |
| 20 | `test_multiple_delimiters_with_different_lengths` | `"//[***][%]\n1***2%3"` | `6` | Long and short separators coexist |

**RED:** These tests are most valuable against a *broken or incomplete* implementation—for example, one that does not escape `*`, includes 1001, or skips validating negatives after a custom delimiter. By the time they were added in our session, the existing implementation **already passed** them. It would be inaccurate to say they failed first.

**GREEN:** No change was needed; they confirmed implemented behavior.

**REFACTOR:** None needed for those cases. They strengthened regression confidence.

## 14. Newlines after a custom delimiter — test 21

```python
def test_custom_delimiter_with_newline():
    assert add("//;\n1;2\n3") == 6
```

**RED:** The earlier custom-header branch *replaced* the default delimiters with `[";"]`. The body `"1;2\n3"` left `"2\n3"` unsplit; converting it to an integer failed.

**GREEN:** After parsing the declared delimiter(s), append newline:

```python
delimiters.append("\n")
```

**REFACTOR:** Keep the newline in the common delimiter list, regardless of which custom syntax the input used. In the current implementation, custom delimiters replace the comma default, but **newline is retained**. This distinction is worth remembering when explaining the code.

## 15. The final `calculator.py` from GitHub

This is the actual version reviewed on `main` (including the same behavior and whitespace):

```python
import re


def add(numbers):
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

    pattern = "|".join(re.escape(delimiter) for delimiter in delimiters)

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
        negative_list = ",".join(str(n) for n in negatives)
        raise ValueError(f"negatives not allowed: {negative_list}")

    return total
```

### Walk through a real call

Take `add("//[***][%]\n1***2%3")`:

1. Input is not empty, so skip the first `return 0`.
2. The input begins with `//`; split header from body at the first newline.
3. `header = "//[***][%]"` and `numbers = "1***2%3"`.
4. Remove the first two header characters: `delimiter_definition = "[***][%]"`.
5. Extract bracketed delimiters: `["***", "%"]`.
6. Add newline as an allowed delimiter: `["***", "%", "\n"]`.
7. Escape regex-special characters, join options with `|`, then split.
8. `values = ["1", "2", "3"]`.
9. Start `total = 0` and `negatives = []`.
10. Convert each token using `int(value)`; add 1, 2, then 3. None are negative or above 1000.
11. Since `negatives` is empty, skip the exception.
12. `return total` returns **6**.

### What each key Python tool contributes

| Python syntax | Purpose |
|---|---|
| `def add(numbers):` | Define function and parameter |
| `if` / `elif` | Branch based on conditions |
| `return` | Send result to caller and end the function |
| `startswith()` | Detect a custom delimiter header |
| `split("\n", 1)` | Divide header from number body once |
| `header[2:]` | Slice off the prefix `//` |
| `re.findall(...)` | Extract one or several bracketed delimiters |
| `re.escape(...)` | Treat regex-special delimiter characters literally |
| `re.split(...)` | Split on any delimiter in the pattern |
| `for value in values:` | Process each token |
| `int(value)` | Convert numeric text to an integer |
| `+=` | Update a running sum |
| `append()` | Save each negative number |
| `raise ValueError(...)` | Reject invalid negative input |
| `pytest.raises(...)` | Assert that rejection happens |

## 16. Test-by-test checklist in the actual repository order

| # | Test | Requirement |
|---|---|---|
| 1 | `test_empty_string_returns_zero` | Empty input |
| 2 | `test_single_number_returns_its_value` | One numeric string |
| 3 | `test_two_numbers` | Two comma-separated numbers |
| 4 | `test_multiple_numbers` | Any number of comma-separated values |
| 5 | `test_newline_delimiter` | Mix newline and comma |
| 6 | `test_multiple_newlines` | Multiple newline separators |
| 7 | `test_custom_delimiter` | One custom separator `;` |
| 8 | `test_custom_delimiter_with_multiple_numbers` | One custom separator `|` |
| 9 | `test_single_negative_number` | Reject one negative |
| 10 | `test_multiple_negative_numbers` | Report all negatives |
| 11 | `test_numbers_greater_than_1000_are_ignored` | Skip values >1000 |
| 12 | `test_1000_is_included` | Include exactly 1000 |
| 13 | `test_delimiter_of_any_length` | Long bracketed delimiter |
| 14 | `test_multiple_custom_delimiters` | More than one separator |
| 15 | `test_multiple_delimiters_of_any_length` | Several long separators |
| 16 | `test_zero` | Zero boundary |
| 17 | `test_only_numbers_above_1000` | All values skipped |
| 18 | `test_negative_number_with_custom_delimiter` | Negative with custom separator |
| 19 | `test_long_delimiter_with_special_characters` | Regex-special delimiter |
| 20 | `test_multiple_delimiters_with_different_lengths` | Mixed-length separators |
| 21 | `test_custom_delimiter_with_newline` | Preserve newline with custom header |

## 17. How to run and troubleshoot

From your Mac's project root:

```bash
source .venv/bin/activate
python -m pytest -v
```

Expected, based on your verified terminal run:

```text
collected 21 items
...
21 passed
```

**Common errors:**

- **`ImportError: cannot import name 'add'`:** the function is missing from `calculator.py`, or named differently.
- **`assert None == 0`:** a function with only `pass` or no explicit return returns `None`.
- **`assert 0 == 5`:** the implementation returns the wrong number; this is a *test assertion failure*.
- **`ValueError: invalid literal for int()`:** an input token still contains delimiter characters, or is not a valid integer.
- **`SyntaxError: 'return' outside function`:** incorrect indentation.
- **`git diff --check` reports trailing whitespace:** there are spaces at the end of lines. It is a formatting problem, not a test failure.

Your earlier `git diff --check` detected trailing whitespace but **did not prevent the commit**. The code was committed and pushed. A later cleanup commit could remove these spaces without changing behavior.

## 18. Practical TDD reflection

A test proves **the behavior it asserts**, not every possible input. For example, a test for `add("1,2")` does not establish that `add("1\n2")` works, or that all negative numbers are reported.

Our development process followed this growing pattern:

```text
empty → single → multiple → newlines → custom delimiters
→ negative validation → ignore >1000 → long/multiple delimiters
→ regression coverage → newline with custom delimiter
```

The first tests forced visible code changes. Some late tests passed immediately because we had already implemented the behavior. That is still useful regression coverage, but it is **not a fresh RED stage**.

**Known boundaries of the current code:** It assumes well-formed headers and valid integer tokens; it does not define friendly behavior for malformed input such as `"1,,2"` or an empty bracket delimiter. Overlapping delimiters may need longest-first ordering. These were not covered by the 21 tests, so do not promise behavior you haven't verified. A custom header currently preserves newline but not the default comma; whether comma should remain allowed is a separate specification decision.

## 19. How to explain your work to another developer

> “I used Python and pytest to build the String Calculator through TDD. I started with a failing empty-input test. At first pytest had an import error; after defining a stub, I got a proper failing assertion, `None == 0`. I made the simplest solution return 0. Then each additional test drove more behavior: parsing a single integer, splitting several values, supporting newline and custom separators, rejecting all negative numbers, ignoring values above 1000, and handling multiple long delimiters through escaped regular expressions. I re-ran all existing tests after changes to check for regressions. The final suite has 21 passing tests.” 

## 20. Git workflow — sync documentation to your Mac

This Markdown file is committed directly to GitHub's `main` branch. On your existing local clone run:

```bash
git status
git pull --ff-only origin main
code TDD_WALKTHROUGH.md
python -m pytest -v
```

If `git status` shows uncommitted local changes, review them before pulling. `--ff-only` avoids an accidental merge commit.

**Remember:** RED proves the new requirement isn't satisfied; GREEN satisfies it with minimal code; REFACTOR keeps the behavior but improves design. **All three steps are supported by running the test suite.**
