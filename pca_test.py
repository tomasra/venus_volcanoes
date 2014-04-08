#!venv/bin/python

import os
import matplotlib.pyplot as plt
from lib.utils.image_set import ImageSet
from lib.algorithms.classifier import Classifier

VOLCANO_RADIUS = 8

cwd = os.path.dirname(os.path.abspath(__file__))
image_dir = os.path.join(cwd, 'data/Images')
gt_dir = os.path.join(cwd, 'data/GroundTruths')

# HOM1/#1 - train
image_set = ImageSet(image_dir, gt_dir, ['img2', 'img3', 'img4'])
image_set_test = ImageSet(image_dir, gt_dir, ['img1'])

vectors = [
    gt_image.to_vector()
    for gt_image in image_set.ground_truth_images(VOLCANO_RADIUS)
]
classes = image_set.ground_truth_classes()

test_vectors = [
    gt_image.to_vector()
    for gt_image in image_set_test.ground_truth_images(VOLCANO_RADIUS)
]

classifier = Classifier()
# scaled_vectors = classifier._reduce_dimensions(original_vectors)
gt_predicted = classifier.train(vectors, classes).run(test_vectors)
gt_test = image_set_test.ground_truth_classes()

# import pdb; pdb.set_trace()
print list(gt_predicted)
print gt_test

# print scaled_vectors

# fig1 = plt.figure()
# x = [vector[2] for vector in scaled_vectors]
# y = [vector[3] for vector in scaled_vectors]
# plt.plot(x, y, 'ro')
# plt.show()
