import re


def extract_score(result):

    match = re.search(
        r"ATS_SCORE:\s*(\d+)",
        result
    )

    if match:
        return int(
            match.group(1)
        )

    return None


def extract_skills(result):

    match = re.search(
        r"SKILLS:\s*(.*)",
        result
    )

    if match:

        return [
            x.strip()
            for x
            in match.group(1)
            .split(",")
        ]

    return []


def extract_missing(result):

    match = re.search(
        r"MISSING_SKILLS:\s*(.*)",
        result
    )

    if match:

        return [
            x.strip()
            for x
            in match.group(1)
            .split(",")
        ]

    return []


def extract_section_score(
    result,
    section
):

    match = re.search(
        rf"{section}:\s*(\d+)",
        result
    )

    if match:
        return match.group(1)

    return None

def extract_matched_keywords(result):

    match = re.search(
        r"MATCHED_KEYWORDS:\s*(.*)",
        result
    )

    if match:

        return [
            x.strip()
            for x
            in match.group(1)
            .split(",")
        ]

    return []


def extract_missing_keywords(result):

    match = re.search(
        r"MISSING_KEYWORDS:\s*(.*)",
        result
    )

    if match:

        return [
            x.strip()
            for x
            in match.group(1)
            .split(",")
        ]

    return []

def extract_keyword_percent(result):

    match = re.search(
        r"KEYWORD_MATCH_PERCENT:\s*(\d+)",
        result
    )

    if match:
        return int(
            match.group(1)
        )

    return None