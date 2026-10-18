"""Ida y vuelta de literales LeetCode: python3 -m unittest discover -s local"""

from __future__ import annotations

import unittest

from lc_local import list_to_str, parse_list, parse_tree, tree_to_str


class RoundTripTest(unittest.TestCase):
    def test_trees(self) -> None:
        for literal in ("[]", "[1]", "[1,null,2,3]", "[3,9,20,null,null,15,7]", "[5,4,8,11,null,13,4,7,2,null,null,null,1]"):
            self.assertEqual(tree_to_str(parse_tree(literal)), literal)

    def test_lists(self) -> None:
        for literal in ("[]", "[1]", "[1,2,3,4,5]"):
            self.assertEqual(list_to_str(parse_list(literal)), literal)

    def test_tree_shape(self) -> None:
        root = parse_tree("[1,null,2,3]")
        self.assertIsNone(root.left)
        self.assertEqual(root.right.left.val, 3)


if __name__ == "__main__":
    unittest.main()
