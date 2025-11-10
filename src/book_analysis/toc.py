from __future__ import annotations
from book_analysis.parser import parse_title
from book_analysis.traversal import preorder_traversal


class Section:
    """
    Section node within a table of contents tree.
    """

    def __init__(self, title: str, children: list[Section]):
        """
        Parameters
        ----------
        title: str
            The title of the section stored at each node
        children: list[Section]
            List of children nodes. If the current section is a leaf, this will be an empty list.
        """
        self.title = title
        self.children = children
        self._id = None
        self._path = []
        self._depth = 0

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, value: int | None):
        if not isinstance(value, (int, None)):
            raise TypeError(f"Invalide type {type(value)} being set to ID")
        self._id = value

    def __eq__(self, other):
        """
        Define equality between two Section objects as two sections with identical titles.
        NOTE: This does not hold well with certain cases, like with identical titles at different levels within a table of contents!
        """
        if not isinstance(other, Section):
            raise TypeError(
                f"Equality cannot be established between types {Section} and {type(other)}"
            )
        return self.title == other.title

    def __repr__(self):
        if self.id is None:
            return self.title
        return f"({'.'.join([str(i) for i in self._path])}) {self.title}"

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
        # Iterates through each index within the path to find the insertion location
        current_level = self
        for i, idx in enumerate(path):
            # Gets all IDs of the children
            ids = [s.id for s in current_level.children]
            try:
                # Finds the path index within this list of IDs
                found_index = ids.index(idx)
                # If found, shifts the node to the next lower level
                current_level = current_level.children[found_index]
            except:
                break

        # Inserts if path is complete
        if i + 1 == len(path):
            # Create a Section object
            section = Section(title=title, children=[])
            section.id = idx
            section._path = path
            section._depth = len(path)

            # Tries to insert the section at a particular index (to maintain sorting)
            try:
                current_level.children.insert(idx - 1, section)
            # If idx - 1 does not exist, just appends the section to the end of the children list
            except:
                current_level.children.append(section)
        # Does not allow insert if path is incomplete
        else:
            raise IndexError(f"Invalid path {path}")

    def print(self, mode: str = "indented+numbered"):
        """
        Prints the table of contents to stdout.

        Parameters
        ----------
        mode: str
            The format in which to print the table of contents.
            Valid enumerations:
                "plain": Prints the titles in plaintext
                "indented": Prints the titles where nested titles are indented
                "indented+numbered": Prints numbered titles where nested titles are indented
        """
        # Traverse the tree and get a list of all the titles
        sections = preorder_traversal(self)

        # Developer's note: I'd love to use an Enum here... but that's not in our allowed libraries list :(
        # Plaintext
        if mode.lower() == "plain":
            print("\n".join([s.title for s in sections]))
        # Indented
        elif mode.lower() == "indented":
            sections = ["\t" * (s._depth) + s.title for s in sections]
            print("\n".join(sections))
        # Indented with numbers
        elif mode.lower() == "indented+numbered":
            sections = [
                "\t" * (s._depth) + ".".join([str(i) for i in s._path]) + " " + s.title
                for s in sections
            ]
            print("\n".join(sections))
        else:
            raise ValueError(f"'{mode}' is an invalid mode")

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
        # Base case: if the title is found, returns the depth
        if self.title == title:
            return self._depth

        # Iterates through all the children nodes
        for section in self.children:
            # Increase the depth count each time
            section._depth = self._depth + 1
            # Iteratively finds the depth
            section_depth = section.depth(title)
            # Moves further down if the title is found under the child
            if section_depth is not None:
                return section_depth
        return None

    def height(self) -> int:
        """
        Maximum number of links from the highest level section to the furthest leaf section.
        """
        # Base case: height is zero if node has no children
        if not self.children:
            return 0

        # Recursively find the maximum depth
        max_depth = 0
        for section in self.children:
            max_depth = max(section.height(), max_depth)
        return max_depth + 1


def construct_toc(lines: list[str], title: str = "", top_level: bool = True) -> Section:
    """
    Construct a table of contents from a list of section titles.

    Parameters
    ----------
    lines: list[str]
        List of section titles
    top_level: bool
        Determines if the highest level should be parsed

    Returns
    -------
    Root Section object
    """
    # Initialize table of contents
    toc = Section(title=title, children=[])
    current_part = None
    # Iterate through list of titles
    for line in lines:
        # Parse the title, catching failures
        try:
            path, title = parse_title(line)
        except:
            continue

        # Populates the highest level section
        if top_level:
            if path[0] is not None:
                current_part = path[0]
            path[0] = current_part
        else:
            path = path[1:]

        # Inserts the section title into the table of contents
        if path:
            toc.insert(path=path, title=title)
    return toc


def read_toc(path: str, title: str = "", top_level: bool = True) -> Section:
    """
    Read in a TXT file containing table of contents data into a Section object.

    Parameters
    ----------
    path: str
        Path to TXT file
    title: str
        Title of the book
    top_level: bool
        Determines if the highest level should be parsed

    Returns
    -------
    Section object
    """
    # Read in each line of the TXT file
    with open(path, "r") as f:
        lines = f.readlines()
    # Constructs the Section object
    return construct_toc(lines=lines, title=title, top_level=top_level)
