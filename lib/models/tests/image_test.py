import unittest
import numpy as np
from lib.models import Image


class ImageTests(unittest.TestCase):
    def test_get_row(self):
        """
        Creates a raw signal object and extracts one specified row
        """
        # 4x4 test data

        # data = [chr(i) for i in xrange(0, 6)]
        # signal = RawSignal(rows=2, cols=3, data=data)
        # expected = [chr(i) for i in xrange(3, 6)]
        # self.assertSequenceEqual(signal[1], expected)
        data = np.arange(16).reshape((4, 4))
        image = Image(data)
        actual = image[1]
        expected = np.array([4, 5, 6, 7])
        self.assertTrue(
            np.array_equal(actual, expected))

    def test_iterator(self):
        """
        Checks if row iterator works fine
        """
        # data = [0, 1, 2, 3, 4, 5]
        data = np.arange(4).reshape((2, 2))
        image = Image(data=data)
        rows = [row for row in image]
        self.assertTrue(
            np.array_equal(rows[0], np.array([0, 1])))
        self.assertTrue(
            np.array_equal(rows[1], np.array([2, 3])))

    def test_get_rect(self):
        """
        Cuts a rectangle area from one signal
        and checks if the new signal object was created correctly
        """
        # 4x4 test data
        data = np.arange(16).reshape((4, 4))
        image = Image(data)
        actual = image.cut(((1, 1), (2, 2))).data
        expected = np.array([[5, 6], [9, 10]])
        print actual
        self.assertTrue(
            np.array_equal(actual, expected))

    # @unittest.skip("")
    def test_signal_to_vector(self):
        """
        Flatten 2D signal data into simple vector
        """
        data = np.arange(6).reshape((2, 3))
        actual = Image(data).to_vector()
        expected = np.array([0, 1, 2, 3, 4, 5])
        self.assertTrue(np.array_equal(actual, expected))
