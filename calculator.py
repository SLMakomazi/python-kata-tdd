
import re


def add(numbers):
    # LESSON 1: Empty string
    if numbers == "":
        return 0

    # LESSON 2: Default comma and newline delimiters
    delimiters = [",", "\n"]

    # LESSON 3: Custom delimiters
    if numbers.startswith("//"):
        header, numbers = numbers.split("\n", 1)
        definition = header[2:]

        # LESSON 5: Advanced delimiters
        if definition.startswith("["):
            delimiters = re.findall(r"\[([^\]]+)\]", definition)
        else:
            delimiters = [definition]

        delimiters.append("\n")

    # LESSON 5: Build a pattern for all delimiters
    delimiters.sort(key=len, reverse=True)
    pattern = "|".join(re.escape(d) for d in delimiters)

    # LESSON 2: Split and convert numbers
    values = [int(n) for n in re.split(pattern, numbers)]

    # LESSON 4: Find negative numbers
    negatives = [n for n in values if n < 0]

    if negatives:
        message = ",".join(str(n) for n in negatives)
        raise ValueError(f"negatives not allowed: {message}")

    # LESSON 4: Ignore numbers greater than 1000
    return sum(n for n in values if n <= 1000)
