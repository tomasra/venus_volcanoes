#!venv/bin/python
import os
from lib.utils.image_set import ImageSet
# from lib.algorithms.finder import Finder
from lib.algorithms.recognizer import Recognizer
from lib.utils.renderer import render_png_to_file, render_png_plot
from lib.utils.reader import read_lxyv, read_signal
from lib.utils.reader import read_spoiled_image
from config import VOLCANO_RADIUS

from lib.utils.writer import write_lxyr
from lib.algorithms.imaging import cluster_images
from lib.utils.renderer import render_mosaic

cwd = os.path.dirname(os.path.abspath(__file__))
image_dir = os.path.join(cwd, 'data/Images')
gt_dir = os.path.join(cwd, 'data/GroundTruths')
results_dir = os.path.join(cwd, 'data/Results')
foa_dir = os.path.join(cwd, 'data/FOA/exp_A/exp_A1/trn')


image_set_train = ImageSet(
    data_dir=image_dir,
    ground_truth_dir=gt_dir,
    foa_dir=foa_dir,
    image_names=['img2', 'img3', 'img4'],
    negative_examples=True)

class1 = image_set_train.ground_truth_images(
    class_value=1,
    radius=VOLCANO_RADIUS
)

clusters = cluster_images(class1, 4)
render_mosaic(class1, 'class1_raw.png')
render_mosaic(clusters, 'class1_cluster4.png')
