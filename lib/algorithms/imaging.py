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

    # Approximate object lengths
    lengths = _shape_lengths(labeled, count)

    if obj_count:
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
            lengths[i][1]
            for i in xrange(1, count + 1)
            if lengths[i][1] >= obj_length
        ]

    # Show only these longest shapes
    result = (
        np.in1d(labeled, longest_shape_labels)
        .reshape(labeled.shape)
    )
    if return_image:
        result = result.astype(np.uint8) * 255

    return result


def _shape_lengths(labeled_image, label_count):
    """
    Collect bounding boxes of all non-zero labeled regions
    and return their diagonal lengths
    """
    top_left_points = [(0, 0)] * (label_count + 1)
    right_bottom_points = [(0, 0)] * (label_count + 1)

    for (x, y), value in np.ndenumerate(labeled_image):
        # Exclude 0-labeled regions
        if value != 0:
            # First point of this label?
            if top_left_points[value] == (0, 0):
                top_left_points[value] = (x, y)
            # Last point of the label
            right_bottom_points[value] = (x, y)

    # Diagonal lengths
    diffs = np.array(top_left_points) - np.array(right_bottom_points)
    lengths = np.linalg.norm(diffs, axis=1)
    labels = range(0, label_count + 2)
    return zip(labels, lengths)
