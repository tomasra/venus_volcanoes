import unittest
from lib.models import GroundTruth


class GroundTruthTests(unittest.TestCase):
    def test_get_rectangle(self):
        """
        Checks if ground truth circle is correctly returned as a rectangle.
        """
        gt = GroundTruth(10, 10, 2)
        expected = [(8, 8), (12, 12)]
        self.assertEquals(gt.get_rectangle(), expected)

    def test_get_rectangle_with_float_radius(self):
        """
        Radius from .lxyr file is float number and can have fraction.
        It should be rounded before calculating rectangle points.
        """
        gt1 = GroundTruth(10, 10, 2.4)
        gt2 = GroundTruth(10, 10, 2.5)
        expected1 = [(8, 8), (12, 12)]
        expected2 = [(7, 7), (13, 13)]
        self.assertEquals(gt1.get_rectangle(), expected1)
        self.assertEquals(gt2.get_rectangle(), expected2)
