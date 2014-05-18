#!venv/bin/python
import os
from lib.utils.image_set import ImageSet
from lib.algorithms.finder import Finder
from lib.utils.renderer import render_png_to_file, render_png_plot
from lib.utils.reader import read_lxyv, read_signal
from lib.utils.reader import read_spoiled_image
from config import VOLCANO_RADIUS

cwd = os.path.dirname(os.path.abspath(__file__))
image_dir = os.path.join(cwd, 'data/Images')
gt_dir = os.path.join(cwd, 'data/GroundTruths')
foa_dir = os.path.join(cwd, 'data/FOA/exp_A/exp_A1/tst')





image_set_train = ImageSet(image_dir, gt_dir, ['img2', 'img3', 'img4'])
image_set_test = ImageSet(image_dir, gt_dir, ['img1'])

# for i in xrange(1, 5):
# for i in xrange(1, 2):
    # All volcano classes

volcanoes = image_set_train.ground_truth_images(
    # class_value=i,
    radius=VOLCANO_RADIUS)

finder = Finder(volcanoes)
actual = finder.run(image_set_test['img1'])
expected = read_lxyv(foa_dir, 'img1')

print "---Actual:"
for point in actual:
    # print point.x, point.y
    print "1", float(point.x), float(point.y), "30.0"

# print "---Expected:"
# expected.sort(key=lambda p: p.x)
# expected.sort(key=lambda p: p.y)
# for point in expected:
#     print point.x, point.y





# print len(gts)
# for gt in gts:
#     print gt.x, gt.y, gt.corr_value
# print points
# filename = os.path.join(cwd, 'average' + str(i) + '.png')



# filename = os.path.join(cwd, 'average.png')
# render_png_to_file(finder.template, filename)

# matched_filter_dir = os.path.join(cwd, 'data/FOA/exp_A/exp_A1/trn')
# # matched_filter = read_spoiled_image(matched_filter_dir, 'matched_filter')
# matched_filter = read_signal(matched_filter_dir, 'matched_filter_test')
# render_png_plot(matched_filter)
