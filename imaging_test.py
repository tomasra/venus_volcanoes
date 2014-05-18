#!venv/bin/python
import os
cwd = os.path.dirname(os.path.abspath(__file__))
image_dir = os.path.join(cwd, 'data/Images')

from lib.utils.reader import read_signal
# from lib.utils.renderer import render_png_plot
from lib.utils.renderer import render_png_to_file
# from lib.algorithms.imaging import quantize_kmeans
import lib.algorithms.imaging as img
# from skimage.segmentation import slic
import skimage.segmentation as sgm
import matplotlib.pyplot as plt
import numpy as np
from skimage.filter.rank import otsu
from skimage.morphology import disk
import skimage.filter as flt

image = read_signal(image_dir, 'img1')

# result = quantize(image.data, 6)
# render_png_to_file(result, 'quantization_test_6.png')

# result = quantize(image.data, 5)
# render_png_to_file(result, 'quantization_test_5.png')

# result = quantize(image.data, 4)
# render_png_to_file(result, 'quantization_test_4.png')

# result = img.quantize_kmeans(image.data, 3)
# render_png_to_file(result, 'quantization_test_3.png')


# import pdb; pdb.set_trace()


# quantized = img.quantize_kmeans(image.data, 3)
# quantized = img.quantize_naive(image.data, 3)
# import pdb; pdb.set_trace()
# local_otsu = otsu(quantized, disk(5))
# otsu = flt.threshold_otsu(quantized)
# result = (quantized >= otsu).astype(np.uint8)
# result = (quantized >= 140).astype(np.uint8)
# result *= 255

result = img.find_long_objects(image.data, 20)
render_png_to_file(result, 'long_objects_20.png')

result = img.find_long_objects(image.data, 35)
render_png_to_file(result, 'long_objects_35.png')

result = img.find_long_objects(image.data, 50)
render_png_to_file(result, 'long_objects_50.png')

# import pdb; pdb.set_trace()


# segments = sgm.slic(
#     image.data,
#     n_segments=5,
#     multichannel=False).astype(np.uint8)
# segments = sgm.felzenszwalb(image.data)

# quantized = img.quantize_kmeans(image.data, 3)
# segments = img.find_long_objects(quantized)

# segments = sgm.quickshift(image.data)
# import pdb; pdb.set_trace()
# render_png_to_file(segments, 'segments.png')
# plt.imshow(segments)
# plt.show()
