import numpy as np
import scipy.ndimage.measurements as msr
from scipy.cluster.vq import kmeans, vq


def quantize_naive(image, count):
    """
    Simplest possible quantization.
    Group image colors into specified count of centroids,
    evenly distributed between 0 and 256
    """
    pixels = np.reshape(image, (image.shape[0] * image.shape[1]))
    # centroids, _ = kmeans(pixels, count)
    # import pdb; pdb.set_trace()
    # quantized, _ = vq(pixels, centroids)
    # quantized_idx = np.reshape(quantized, (image.shape[0], image.shape[1]))
    # result = centroids[quantized_idx]
    return None  # TODO


def quantize_kmeans(image, count):
    """
    Image color quantization with k-means
    """
    pixels = np.reshape(image, (image.shape[0] * image.shape[1]))
    centroids, _ = kmeans(pixels, count)
    quantized, _ = vq(pixels, centroids)
    quantized_idx = np.reshape(quantized, (image.shape[0], image.shape[1]))
    result = centroids[quantized_idx]
    # import pdb; pdb.set_trace()
    return result


def find_long_objects(
        image,
        obj_length=35,
        obj_count=None,
        return_image=False):
    """
    Returns binary image with ones representing
    objects longer than specified length
    """
    quantized = quantize_kmeans(image, 4)
    threshold = np.max(quantized)
    thresholded = (quantized >= threshold).astype(np.uint8)
    thresholded *= 255
    structure = np.array([
        [1, 1, 1],
        [1, 1, 1],
        [1, 1, 1]
    ])
    # Segmentation
    labeled, count = msr.label(thresholded, structure=structure)

    if obj_count:
        # Take specified number of longest objects
        lengths = [
            (label, _shape_length(labeled, label))
            for label in xrange(1, count)
            # Exclude 0-label!
        ]
        # Take 'obj_count' number of longest shape labels
        longest_shape_labels = [
            shape[0]    # Label no.
            for shape in sorted(
                lengths,
                key=lambda shape: shape[1],
                reverse=True)
        ][:obj_count]
    else:
        # Filter by object length
        longest_shape_labels = [
            label
            for label in xrange(1, count)
            if _shape_length(labeled, label) >= obj_length
        ]

    # Show only these longest shapes
    result = (
        np.in1d(labeled, longest_shape_labels)
        .reshape(labeled.shape)
    )
    if return_image:
        result = result.astype(np.uint8) * 255

    return result


def _shape_length(image, label):
    """
    Takes top-left and bottom-right shape points
    and calculates distance between them
    """
    # rows, cols = np.where(image == label)
    # if rows.any() and cols.any():
        # row_diff = np.max(rows) - np.min(rows)
        # col_diff = np.max(cols) - np.min(cols)
    points = np.argwhere(image == label)
    if points.any():
        height = np.abs(points[0][0] - points[-1][0])
        width = np.abs(points[0][1] - points[-1][1])
        length = np.sqrt(width ** 2 + height ** 2)
        return length
    else:
        return 0.0
