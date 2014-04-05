import unittest
import numpy as np
from lib.models import RawSignal


class RawSignalTests(unittest.TestCase):
    def test_get_row(self):
        """
        Creates a raw signal object and extracts one specified row
        """
        # 4x4 test data
        data = [chr(i) for i in xrange(0, 6)]
        signal = RawSignal(rows=2, cols=3, data=data)
        expected = [chr(i) for i in xrange(3, 6)]
        self.assertSequenceEqual(signal[1], expected)

    def test_iterator(self):
        """
        Checks if row iterator works fine
        """
        data = [0, 1, 2, 3, 4, 5]
        signal = RawSignal(rows=3, cols=2, data=data)
        self.assertSequenceEqual(
            [row for row in signal],
            [[0, 1], [2, 3], [4, 5]])

    def test_get_rect(self):
        """
        Cuts a rectangle area from one signal
        and checks if the new signal object was created correctly
        """
        # 4x4 test data
        data = [i for i in xrange(0, 16)]
        rows, cols = 4, 4
        signal = RawSignal(rows, cols, data)
        new_signal = signal.extract_rectangle((1, 1), (2, 2))
        self.assertSequenceEqual(new_signal.data, [5, 6, 9, 10])

    def test_extract_rectangle_invalid_points(self):
        """
        Tests various invalid conditions of rectangle area extraction
        """
        data = [i for i in xrange(0, 16)]
        rows, cols = 4, 4
        signal = RawSignal(rows, cols, data)
        # top-left point out of range
        self.assertRaises(
            ValueError,
            lambda: signal.extract_rectangle((-1, 2), (3, 3)))
        # bottom-right point out of range
        self.assertRaises(
            ValueError,
            lambda: signal.extract_rectangle((1, 1), (99, 99)))
        # reversed points
        self.assertRaises(
            ValueError,
            lambda: signal.extract_rectangle((3, 3), (1, 1)))
        # requested rectangle larger than original
        self.assertRaises(
            ValueError,
            lambda: signal.extract_rectangle((0, 0), (4, 4)))
        # invalid parameter types
        self.assertRaises(
            ValueError,
            lambda: signal.extract_rectangle("a", "b"))

    def test_signal_to_np_vector(self):
        """
        Convert signal data to numpy vector
        """
        data = [i for i in xrange(0, 6)]
        rows, cols = 2, 3
        signal = RawSignal(rows, cols, data)
        actual = signal.to_np_vector()
        expected = np.array(data)
        self.assertSequenceEqual(actual, expected)
