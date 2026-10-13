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
