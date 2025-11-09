import pytest
from book_analysis.toc import construct_toc, read_toc, Section


def get_titles(toc):
    return [c.title for c in toc.children]


def test_Section():
    # Initialize ToC
    toc = Section(title="Test Book", children=[])
    assert toc.title == "Test Book"
    assert toc.children == []
    assert toc.id is None

    # Insert
    toc.insert(path=[1], title="Part One")
    toc.insert(path=[2], title="Part Two")
    toc.insert(path=[1, 2], title="Part One Chapter Two")
    toc.insert(path=[1, 3], title="Part One Chapter Three")
    toc.insert(path=[1, 1], title="Part One Chapter One")
    toc.insert(path=[2, 1], title="Part Two Chapter One")
    toc.insert(path=[1, 2, 1], title="Part One Chapter Two Section One")
    assert get_titles(toc) == ["Part One", "Part Two"]
    assert get_titles(toc.children[0]) == [
        "Part One Chapter One",
        "Part One Chapter Two",
        "Part One Chapter Three",
    ]
    assert get_titles(toc.children[0].children[0]) == []
    assert get_titles(toc.children[0].children[1]) == [
        "Part One Chapter Two Section One"
    ]
    assert get_titles(toc.children[0].children[2]) == []
    assert get_titles(toc.children[1]) == ["Part Two Chapter One"]
    assert get_titles(toc.children[1].children[0]) == []

    # Invalid insert
    with pytest.raises(IndexError) as exception:
        toc.insert(path=[1, 1, 1, 1, 1], title="Way too nested")
    assert "Invalid path [1, 1, 1, 1, 1]" == str(exception.value)

    # Depth
    assert toc.depth(title="Test Book") == 0
    assert toc.depth(title="Part One") == 1
    assert toc.depth(title="Part One Chapter Two") == 2
    assert toc.depth(title="Part One Chapter Two Section One") == 3
    assert toc.depth(title="Title does not exist") is None

    # Height
    assert toc.height() == 3


def test_construct_toc():
    toc_lines = [
        "Part I: Part One ",
        "   Chapter 1  Part One Chapter One",
        "   Chapter 2  Part One Chapter Two\n",
        "     2.1 Part One Chapter Two Section One   ",
        "   Chapter 3   Part One Chapter Three \t",
        "Part II: Part Two\n",
        "   Chapter 4  Part Two Chapter One",
    ]
    # With top level
    toc = construct_toc(lines=toc_lines, title="Top Level", top_level=True)
    assert toc.title == "Top Level"
    assert toc.height() == 3
    assert get_titles(toc) == ["Part One", "Part Two"]
    assert get_titles(toc.children[0]) == [
        "Part One Chapter One",
        "Part One Chapter Two",
        "Part One Chapter Three",
    ]
    assert get_titles(toc.children[0].children[0]) == []
    assert get_titles(toc.children[0].children[1]) == [
        "Part One Chapter Two Section One"
    ]
    assert get_titles(toc.children[0].children[2]) == []
    assert get_titles(toc.children[1]) == ["Part Two Chapter One"]
    assert get_titles(toc.children[1].children[0]) == []

    # Without top level
    toc = construct_toc(lines=toc_lines, title="No Top Level", top_level=False)
    assert toc.title == "No Top Level"
    assert toc.height() == 2
    assert get_titles(toc) == [
        "Part One Chapter One",
        "Part One Chapter Two",
        "Part One Chapter Three",
        "Part Two Chapter One",
    ]
    assert get_titles(toc.children[0]) == []
    assert get_titles(toc.children[1]) == ["Part One Chapter Two Section One"]
    assert get_titles(toc.children[2]) == []
    assert get_titles(toc.children[3]) == []


def test_read_toc(tmp_path):
    # Create temporary file for test
    toc_lines = [
        "Part I: Part One ",
        "   Chapter 1  Part One Chapter One",
        "   Chapter 2  Part One Chapter Two",
        "     2.1 Part One Chapter Two Section One   ",
        "   Chapter 3   Part One Chapter Three \t",
        "Part II: Part Two",
        "   Chapter 4  Part Two Chapter One",
    ]
    temp_file = tmp_path / "test_read_toc.txt"
    temp_file.write_text("\n".join(toc_lines))

    # With top level
    toc = read_toc(path=temp_file, title="Top Level", top_level=True)
    assert toc.title == "Top Level"
    assert toc.height() == 3
    assert get_titles(toc) == ["Part One", "Part Two"]
    assert get_titles(toc.children[0]) == [
        "Part One Chapter One",
        "Part One Chapter Two",
        "Part One Chapter Three",
    ]
    assert get_titles(toc.children[0].children[0]) == []
    assert get_titles(toc.children[0].children[1]) == [
        "Part One Chapter Two Section One"
    ]
    assert get_titles(toc.children[0].children[2]) == []
    assert get_titles(toc.children[1]) == ["Part Two Chapter One"]
    assert get_titles(toc.children[1].children[0]) == []

    # Without top level
    toc = read_toc(path=temp_file, title="No Top Level", top_level=False)
    assert toc.title == "No Top Level"
    assert toc.height() == 2
    assert get_titles(toc) == [
        "Part One Chapter One",
        "Part One Chapter Two",
        "Part One Chapter Three",
        "Part Two Chapter One",
    ]
    assert get_titles(toc.children[0]) == []
    assert get_titles(toc.children[1]) == ["Part One Chapter Two Section One"]
    assert get_titles(toc.children[2]) == []
    assert get_titles(toc.children[3]) == []
