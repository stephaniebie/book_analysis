from book_analysis.traversal import preorder_traversal
from book_analysis.toc import Section


def test_preorder_traversal():
    # Create a test ToC
    toc = Section(title="Test Book", children=[])
    toc.insert(path=[1], title="Part One")
    toc.insert(path=[2], title="Part Two")
    toc.insert(path=[1, 2], title="Part One Chapter Two")
    toc.insert(path=[1, 3], title="Part One Chapter Three")
    toc.insert(path=[1, 1], title="Part One Chapter One")
    toc.insert(path=[2, 1], title="Part Two Chapter One")
    toc.insert(path=[1, 2, 1], title="Part One Chapter Two Section One")

    # Traverse the ToC
    sections = preorder_traversal(toc)
    expected_titles = [
        "Test Book",
        "Part One",
        "Part One Chapter One",
        "Part One Chapter Two",
        "Part One Chapter Two Section One",
        "Part One Chapter Three",
        "Part Two",
        "Part Two Chapter One",
    ]
    assert [s.title for s in sections] == expected_titles
