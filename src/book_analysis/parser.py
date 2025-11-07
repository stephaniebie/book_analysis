import re
from book_analysis.defaults import ROMAN_NUMERALS


def read_txt(path: str) -> list:
    """
    Read in table of contents from a text file.

    Parameters
    ----------
    path: str
        Path to the text file

    Returns
    -------
    List of lines within the text file
    """
    with open(path, "r") as f:
        lines = f.readlines()
    return lines


def convert_roman_numerals(numerals: str) -> int:
    """
    Convert Roman numerals to an integer value.

    Parameters
    ----------
    numerals: str
        Roman numerals as a string

    Returns
    -------
    Converted value of the Roman numerals as an integer
    """
    value = 0
    for i, n in enumerate(numerals):
        if (
            i + 1 < len(numerals)
            and ROMAN_NUMERALS[n] < ROMAN_NUMERALS[numerals[i + 1]]
        ):
            value -= ROMAN_NUMERALS[n]
            continue
        value += ROMAN_NUMERALS[n]
    return value


def parse_title(title: str) -> tuple[list[int], str]:
    """
    Parse a table of contents section title.
    NOTE: Format is specific to the "Artificial Intelligence: A Modern Approach" format.

    Parameters
    ----------
    title: str
        Title of a section

    Returns
    -------
    List indicating the path to the section within a table of contents
    The title as a string
    """
    # Remove leading and trailing whitespaces
    unformatted_title = title
    title = title.strip()
    # Parse highest level section
    if title.startswith("Part "):
        part_num = title.replace("Part ", "").split(":", maxsplit=1)[0]
        title = title.split(": ", maxsplit=1)[-1].strip()
        return [convert_roman_numerals(part_num)], title
    # Parse second-highest level
    elif re.search(r"^Chapter (\d*)", title):
        chapter_num = re.search("^Chapter ([0-9]*)", title)[1]
        title = title.split(chapter_num, maxsplit=1)[-1].strip()
        return [None, int(chapter_num)], title
    # Parse lowest two levels
    elif re.search(r"^\d*\.\d*\S*", title):
        section_num = re.search(r"^\d*.\d*\S*", title)[0]
        title = title.split(section_num, maxsplit=1)[-1].strip()
        return [None] + [int(n) for n in section_num.split(".")], title
    # Raises an error if format isn't recognized
    raise ValueError(f"'{unformatted_title}' is improperly formatted")
