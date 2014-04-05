import numpy as np


class RawSignal(object):
    def __init__(self, rows, cols, data, name=None):
        self.rows = rows
        self.cols = cols
        self.data = data
        self.name = name
        self.ground_truths = []

    def __getitem__(self, key):
        """
        Returns row by specified index or slice.
        """
        if isinstance(key, slice):
            # Collect rows according to slice
            return [self[i] for i in xrange(*key.indices(self.rows))]
        elif isinstance(key, int):
            # Check for negative or out-of-range indexes
            if key >= self.rows or key < 0:
                raise IndexError("Sequence index out of range.")
            return self.data[(self.cols * key):(self.cols * (key + 1))]
        else:
            raise TypeError("Invalid argument type.")

    def __iter__(self):
        """
        Iterates through all rows
        """
        for i in range(0, self.rows):
            yield self[i]

    def extract_rectangle(self, p1, p2):
        """
        Returns rectangle fragment of image data
        as a new RawSignal object.
        p1 and p2 - top left and bottom right points, respectively
        """
        try:
            # Increment cols/rows to allow returning a single item
            # if both rectangle points are the same
            cols = (p2[0] - p1[0]) + 1    # x coordinates
            rows = (p2[1] - p1[1]) + 1    # y coordinates

            # Check for negative or out-of-range cols/rows.
            if cols < 0 or cols > self.cols:
                raise Exception
            if rows < 0 or rows > self.rows:
                raise Exception

            # Collect a flat list of items bounded by rectangle.
            data = [
                point
                for row in self[p1[1]:p1[1] + rows]
                for point in row[p1[0]:p1[0] + cols]
            ]
            return RawSignal(rows, cols, data)
        except Exception:
            raise ValueError("Invalid rectangle points")

    def to_np_vector(self):
        """
        Returns image data as numpy vector
        """
        return np.array(self.data)
