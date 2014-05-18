import os
basedir = os.path.abspath(os.path.dirname(__file__))

IMAGE_DIR = os.path.join(basedir, 'data/Images')
GROUND_TRUTH_DIR = os.path.join(basedir, 'data/GroundTruths')
VOLCANO_PIXEL_SIZE = 15
FOA_THRESHOLD = 0.45
VOLCANO_RADIUS = 8
