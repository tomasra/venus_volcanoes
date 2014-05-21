import numpy as np
# import matplotlib.pyplot as plt
from lib.models import GroundTruth
import skimage.morphology as fm
from skimage.feature import match_template
# from skimage.filter import threshold_otsu
# from skimage.morphology import skeletonize
# from skimage import img_as_bool
# from config import VOLCANO_PIXEL_SIZE
from lib.algorithms.imaging import find_long_objects
from config import FOA_THRESHOLD


class Finder(object):
    def __init__(self, training_images):
        self.template = self._image_average(
            training_images)

    def run(self, image):
        """
        Return list of possible volcanoes
        (GroundTruth objects)
        """
        # Apply matched filter and binarize image with
        # predefined threshold
        result = match_template(image.data, self.template, pad_input=True)
        binary = result > FOA_THRESHOLD

        # Shrink larger regions?
        skeletonized = fm.skeletonize(binary)

        # Aggregate small pixel groups
        labeled, num = fm.label(
            skeletonized,
            neighbors=8,
            return_num=True)
        raw_points = self._aggregate_point_groups(labeled, num)

        # Pixels of long objects (canyons, etc)
        long_objects = find_long_objects(image.data)
        lo_points = [
            tuple(point)
            for point in np.argwhere(long_objects)  # == True
        ]

        ground_truths = [
            GroundTruth(
                x=point[1],
                y=point[0],
                corr_value=result[point[0]][point[1]],
                radius=15
            )
            for point in raw_points
            if (point[0], point[1]) not in lo_points
        ]

        return ground_truths

    def _image_average(self, images):
        """
        Arithmetic average of multiple images.
        Returns one image of the same dimensions.
        """
        image_data = [
            image.normalize().data for image in images
            # Workaround: skip partial volcano images at the edges
            if image.data.shape[0] == image.data.shape[1]
        ]
        return np.rint(
            np.mean(image_data, axis=0)
        ).astype(np.uint8)

    def _collect_points(self, image, point_value=0):
        """
        Returns list of points (row and col pairs)
        which have specified pixel value in the image.
        """
        return zip(*np.where(image == point_value))

    def _aggregate_point_groups(self, labeled_image, label_count):
        """
        Returns a center point for each labeled adjacent pixel group
        """
        centroid = lambda row_coords, col_coords: (
            int(np.rint(sum(row_coords) / len(row_coords))),
            int(np.rint(sum(col_coords) / len(col_coords)))
        )
        return [
            centroid(*np.where(labeled_image == i))
            for i in xrange(1, label_count)
        ]
