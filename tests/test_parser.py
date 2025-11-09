import pytest
from book_analysis.parser import convert_roman_numerals, parse_title


@pytest.mark.parametrize(
    ("roman_numerals", "expected_value"),
    [
        ("I", 1),
        ("IV", 4),
        ("DCCLXXXIX", 789),
        ("MMMCMXCIX", 3999),
    ],
)
def test_convert_roman_numerals(roman_numerals, expected_value):
    assert convert_roman_numerals(roman_numerals) == expected_value


@pytest.mark.parametrize(
    ("title", "expected_path", "expected_title"),
    [
        ("Part III: Part three's title", [3], "Part three's title"),
        ("     Chapter 5 This is chapter five   ", [None, 5], "This is chapter five"),
        (" 10.11 A nested subsection", [None, 10, 11], "A nested subsection"),
        (" 1.2.3 A nested subsubsection", [None, 1, 2, 3], "A nested subsubsection"),
    ],
)
def test_parse_title(title, expected_path, expected_title):
    actual_path, actual_title = parse_title(title)
    assert actual_path == expected_path
    assert actual_title == expected_title

    # Check that ValueErrors are raised appropriately
    with pytest.raises(ValueError) as exception:
        parse_title("invalid start " + title)
    assert f"'invalid start {title}' is improperly formatted" == str(exception.value)
