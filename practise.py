import re

numbers = "1***2%3"

values = re.split(r"\*|%", numbers)

print(values)