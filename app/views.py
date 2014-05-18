import os
import re
import json
from app import app
from flask import abort, render_template, make_response

from config import IMAGE_DIR, GROUND_TRUTH_DIR, VOLCANO_PIXEL_SIZE
from lib.utils.reader import list_signals, read_signal, read_lxyr
from lib.utils.renderer import render_png_raw
from lib.utils.image_set import ImageSet
from config import VOLCANO_RADIUS
# from lib.algorithms.classifier import Classifier
from lib.algorithms.finder import Finder


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/images', defaults={'image_name': None})
@app.route('/images/<image_name>')
def images(image_name):
    return render_template(
        'image.html',
        image_list=_sorted_image_names(),
        selected_image=image_name)


@app.route('/images/render/<image_name>')
def image_render(image_name):
    signal = read_signal(IMAGE_DIR, image_name)
    if signal:
        image_data = render_png_raw(signal)
        response = make_response(image_data)
        response.headers['Content-Type'] = 'image/png'
        return response
    else:
        abort(404)


@app.route('/finder/<image_name>')
def finder_image(image_name):
    return render_template(
        'finder.html',
        image_list=_sorted_image_names(),
        selected_image=image_name)


@app.route('/finder/<image_name>/ground_truths')
def finder_ground_truths(image_name):
    image_set_train = ImageSet(
        IMAGE_DIR,
        GROUND_TRUTH_DIR,
        ['img2', 'img3', 'img4'])
    image_set_test = ImageSet(
        IMAGE_DIR,
        GROUND_TRUTH_DIR,
        [image_name])
    volcanoes = image_set_train.ground_truth_images(
        class_value=1,
        radius=VOLCANO_RADIUS)
    finder = Finder(volcanoes)
    results = finder.run(image_set_test[image_name])

    # floats are incompatible with JSON???
    for gt in results:
        gt.corr_value = None
    # import pdb; pdb.set_trace()
    return json.dumps([gt.__dict__ for gt in results])


# FIX THIS!!!
@app.route('/images/ground_truths/<image_name>')
def ground_truth_contours(image_name):
    # filepath = os.path.join(GROUND_TRUTH_DIR, image_name + '.lxyr')
    gts = read_lxyr(GROUND_TRUTH_DIR, image_name)
    return json.dumps([gt.__dict__ for gt in gts])


@app.route('/ground_truths')
def ground_truths():
    """
    All ground truths of all images
    """
    return render_template(
        'ground_truths.html',
        images=[
            _image_gt_ids(image_name)
            for image_name in _sorted_image_names()
        ]
    )


@app.route('/ground_truths/<image_name>')
def ground_truths_image(image_name):
    """
    All ground truths of a single image
    """
    return render_template(
        'ground_truths.html',
        images=[_image_gt_ids(image_name)])


@app.route('/images/<image_name>/ground_truths/<int:gt_id>')
def ground_truth_single(image_name, gt_id):
    """
    Returns specified volcano image from specified main image_name
    """

    # First read all ground truths of this image
    # filepath = os.path.join(GROUND_TRUTH_DIR, image_name + '.lxyr')
    gts = read_lxyr(GROUND_TRUTH_DIR, image_name)
    try:
        gt = gts[gt_id]
        # Use standard radius for all instances
        gt.radius = VOLCANO_PIXEL_SIZE

        # Extract image fragment
        signal = read_signal(IMAGE_DIR, image_name)
        rect = gt.get_rectangle()
        # gt_image = signal.cut(rect)
        gt_image = signal.cut(rect).normalize()

        # Render
        image_data = render_png_raw(gt_image)
        response = make_response(image_data)
        response.headers['Content-Type'] = 'image/png'
        return response
    except:
        abort(404)


def _sorted_image_names():
    """
    Sort image names by their number part
    """
    lst = sorted(
        list_signals(IMAGE_DIR),
        key=lambda item: int(re.search(r'\d+', item).group()))
    return lst


def _image_gt_ids(image_name):
    """
    Collect ground truth indexes of specified image
    """
    # filepath = os.path.join(GROUND_TRUTH_DIR, image_name + '.lxyr')
    # gts = read_lxyr(filepath)
    gts = read_lxyr(GROUND_TRUTH_DIR, image_name)
    gt_ids = [i for i in range(0, len(gts))]
    return {'name': image_name, 'gt_ids': gt_ids}
