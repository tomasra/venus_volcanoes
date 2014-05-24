import numpy as np
from config import VOLCANO_RADIUS

# What to fill with missing parts of cut rectangles
DEFAULT_PIXEL_VALUE = 0


class Image(object):
    def __init__(self, data, name=None):
        self.data = data
        self.name = name
        self.ground_truths = []

    def __getitem__(self, key):
        """
        Returns row by specified index or slice.
        """
        return self.data.__getitem__(key)

    def __iter__(self):
        """
        Iterates through all rows
        """
        for row in self.data:
            yield row

    def cut(self, rectangle):
        """
        Returns rectangle fragment of image data
        as a new RawSignal object.
        p1 and p2 - top left and bottom right points, respectively
        """
        p1, p2 = rectangle[0], rectangle[1]
        # return self.data[row_from:row_to, col_from:col_to]
        return Image(self.data[
            p1[1]:p2[1] + 1,
            p1[0]:p2[0] + 1]
        )

    def ground_truth_images(
            self,
            class_value=None,
            radius=VOLCANO_RADIUS,
            ground_truths=None,
            valid_only=False,
            to_vectors=False):
        """
        Returns associated ground truths as images,
        with an option to override radius
        """
        # Possibility to override existing volcanoes
        if not ground_truths:
            ground_truths = self.ground_truths

        # Collect the images
        if class_value:
            images = [
                self.cut(gt.get_rectangle(radius))
                for gt in ground_truths
                if gt.class_value == class_value
            ]
        else:
            images = [
                self.cut(gt.get_rectangle(radius))
                for gt in ground_truths
            ]

        # Remove these having invalid dimensions
        # (according to specified radius)
        # This can happen when volcano center is at the very edge of main image
        if valid_only:
            expected_length = pow(radius * 2 + 1, 2)
            images = [
                image
                for image in images
                if len(image.to_vector()) == expected_length
            ]

        # Vectorize?
        if to_vectors:
            images = [image.to_vector() for image in images]

        return images

    def to_vector(self):
        """
        Returns image data as simple vector
        """
        return self.data.flatten()

    def normalize(self):
        """
        Normalizes image data with respect to local brightness
        """
        mean = self.data.mean()
        std_dev = self.data.std()
        ones = np.ones(self.data.shape, dtype=self.data.dtype)
        self.data = self.data - (mean * ones) / std_dev
        return self
