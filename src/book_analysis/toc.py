from __future__ import annotations
from book_analysis.parser import read_txt, parse_title


class Section:
    """
    Node of a tree representing a section of a book.
    """

    def __init__(self, title: str, id: int, children: list[Section]):
        """
        Parameters
        ----------
        title: str
            The title of the section stored at each node
        id: int
            Section title identifier
        children: list[Section]
            List of children nodes
        """
        self.title = title
        self.children = children
        self.id = id

    def __repr__(self):
        return f"({self.id}) {self.title}"

    def height(self) -> int:
        """
        Maximum number of links from the highest level section to the furthest leaf section.
        """
        # Base case
        if not self.children:
            return 0

        # Recursively find the maximum depth
        max_depth = 0
        for section in self.children:
            max_depth = max(section.height(), max_depth)

        return max_depth + 1


class TableOfContents:
    """
    Table of contents tree.
    """

    def __init__(self, children: list[Section]):
        """
        Parameters
        ----------
        children: list[Section] | None
            List of possibly nested sections within the book
        """
        self.children = children

    def insert(self, path: list[int], title: str):
        """
        Insert a section within the table of contents.

        Parameters
        ----------
        path: list[int]
            Path within a tree to insert a section
        title: str
            Title of the section to be inserted
        """
        current_level = self
        for idx in path:
            indices = [s.id for s in current_level.children]
            try:
                found_index = indices.index(idx)
                current_level = current_level.children[found_index]
            except:
                break
        section = Section(title=title, id=idx, children=[])
        try:
            current_level.children.insert(idx - 1, section)
        except:
            current_level.children.append(section)

    def print(self, mode: str = "indented+numbers"):
        """
        Prints the table of contents to stdout.
        """
        # Implementation notes:
        # traverse full tree -> generate a string

        # Developer's note: I'd love to use an Enum here... but that's not in our allowed libraries list :(
        if mode.lower() == "plain":
            pass
        elif mode.lower() == "indented":
            pass
        elif mode.lower() == "indented+numbers":
            pass
        raise NotImplementedError

    def depth(self, title: str) -> int:
        """
        The number of links from the highest level to the requested section node.

        Parameters
        ----------
        title: str
            Title of the section

        Returns
        -------
        The depth of the section as an integer
        """
        raise NotImplementedError

    def height(self) -> int:
        """
        Maximum number of links from the highest level section to the furthest leaf section.
        """
        if self.children:
            return max([s.height() for s in self.children]) + 1
        return 0


def construct_toc(lines: list[str], include_parts: bool = False) -> TableOfContents:
    """
    Construct a TableOfContents object from a list of section titles.

    Parameters
    ----------
    lines: list[str]
        List of section titles
    include_parts: bool
        Determines if the highest level should be parsed

    Returns
    -------
    TableOfContents object
    """
    # Initialize table of contents
    toc = TableOfContents(children=[])
    current_part = None
    # Iterate through list of titles
    for line in lines:
        # Parse the title, catching failures
        try:
            path, title = parse_title(line)
        except:
            continue

        # Populates the highest level section
        if include_parts:
            if path[0] is not None:
                current_part = path[0]
            path[0] = current_part
        else:
            path = path[1:]

        # Inserts the section title into the table of contents
        if path:
            toc.insert(path=path, title=title)
    return toc


def read_toc(path: str, include_parts: bool = False) -> TableOfContents:
    """
    Read in a TXT file containing table of contents data into a TableOfContents object.

    Parameters
    ----------
    path: str
        Path to TXT file
    include_parts: bool
        Determines if the highest level should be parsed

    Returns
    -------
    TableOfContents object
    """
    return construct_toc(read_txt(path), include_parts=include_parts)
