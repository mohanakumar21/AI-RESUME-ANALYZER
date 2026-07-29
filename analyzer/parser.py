import re


def extract_name(text):

    lines = text.split("\n")

    for line in lines:

        line = line.strip()

        if len(line) > 3 and len(line.split()) <= 4:
            return line

    return "Not Found"


def extract_email(text):

    pattern = r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}"

    match = re.search(pattern, text)

    if match:
        return match.group()

    return "Not Found"


def extract_phone(text):

    pattern = r"(\+91[\-\s]?)?[6-9]\d{9}"

    match = re.search(pattern, text)

    if match:
        return match.group()

    return "Not Found"


def parse_resume(text):

    return {

        "name": extract_name(text),

        "email": extract_email(text),

        "phone": extract_phone(text)

    }