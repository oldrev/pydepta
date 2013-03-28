from __future__ import division

def tree_size(root):
    """
    Get the subtree size.
    """
    if len(root) == 0:
        return 1
    return sum([tree_size(child) for child in root])

def tree_depth(root):
    """
    Get the subtree depth.
    """
    if len(root) == 0:
        return 0
    return max([tree_depth(child) for child in root]) + 1


class SimpleTreeMatch(object):
    """
    Abstract Simple Tree Match.
    """
    def __init__(self, ger_root, get_children_count, get_child):
        self.get_root = ger_root
        self.get_children_count = get_children_count
        self.get_child = get_child

    def match(self, t1, t2):
        """
        match two trees with generalized node.
        """
        matrix = [[0 for _ in range(len(t1) + 1)] for _ in range(len(t2) + 1)]
        for i in xrange(1, len(matrix)):
            for j in xrange(1, len(matrix[0])):
                matrix[i][j] = max(matrix[i][j - 1], matrix[i - 1][j])
                matrix[i][j] = max(matrix[i][j], matrix[i - 1][j - 1] + self._single_match(t1[i - 1], t2[j - 1]))
        return 1 + matrix[i][j]

    def normalized_match_score(self, t1, t2):
        t1size = sum([tree_size(e) for e in t1]) + 1
        t2size = sum([tree_size(e) for e in t2]) + 1
        return self.match(t1, t2) / ((t1size + t2size) / 2)

    def _single_match(self, t1, t2):
        """
        match two single trees.
        >>> get_root = lambda x: x[0]
        >>> get_children_count = lambda x: len(x[1])
        >>> get_child = lambda x, i: x[i+1]
        >>> stm = SimpleTreeMatch(get_root, get_children_count, get_child)
        >>> t1 = ('tr', ('td', ()), ('td', ()))
        >>> t2 = ('tr', ('td', ()), ('tr', ()))
        >>> stm._single_match(t1, t2)
        """
        if self.get_root(t1) is None or self.get_root(t2) is None:
            return 0
        if self.get_root(t1) != self.get_root(t2):
            return 0
        matrix = [[0 for i in range(self.get_children_count(t1) + 1)] for j in range(self.get_children_count(t2) + 1)]
        for i in xrange(1, len(matrix)):
            for j in xrange(1, len(matrix[0])):
                matrix[i][j] = max(matrix[i][j - 1], matrix[i - 1][j])
                matrix[i][j] = max(matrix[i][j], matrix[i - 1][j - 1] + \
                                                 self._single_match(self.get_child(t1, i - 1), self.get_child(t2, j - 1)))
        return 1 + matrix[i][j]