import unittest
import numpy as np
from lib.algorithms.finder import Finder


class FinderTests(unittest.TestCase):
    def test_collect_points(self):
        """
        Finder - collect points
        """
        image = np.array([
            [2, 1, 1],
            [1, 1, 2],
            [1, 2, 1]
        ])
        finder = Finder([])
        actual = finder._collect_points(image, point_value=2)
        expected = [(0, 0), (1, 2), (2, 1)]
        self.assertSequenceEqual(actual, expected)
