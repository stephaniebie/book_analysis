def preorder_traversal(node, result: list | None = None):
    """
    Traverse a general tree using preorder.

    Parameters
    ----------
    node
        The root node of the tree
    result: list | None
        The resulting nodes after traversing through the tree

    Returns
    -------
    A list of nodes of the tree
    """
    # Preorder Traversal - visit node first, then children
    if result is None:
        result = []

    # Visit current node First
    result.append(node)

    # Visit all children from left to right
    for child in node.children:
        preorder_traversal(child, result)

    return result


# NOTE: Following functions are deprecated... keeping for reference
# Using traversal for depth() and height()
def _depth(root, title):
    # Find depth of a node
    def search(node, target, current_depth=0):
        if node.title == target:
            return current_depth

        for child in node.children:
            result = search(child, target, current_depth + 1)
            if result != -1:
                return result

        return -1

    return search(root, title)


def _height(root):
    # Calculate height of the tree
    def get_height(node):
        if not node.children:
            return 0

        # Get max height of all children, add 1
        return 1 + max(get_height(child) for child in node.children)

    return get_height(root)
