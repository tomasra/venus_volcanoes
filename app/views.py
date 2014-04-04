import os
import json
import re
from app import app
from flask import abort, render_template, make_response

from config import IMAGE_DIR, GROUND_TRUTH_DIR, VOLCANO_PIXEL_SIZE
from lib.utils.reader import list_signals, read_signal, read_lxyr
from lib.utils.renderer import render_png_raw


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/images', defaults={'image_name': None})
@app.route('/images/<image_name>')
def images(image_name):
    # Sort images by number
    lst = sorted(
        list_signals(IMAGE_DIR),
        key=lambda item: int(re.search(r'\d+', item).group()))
    return render_template(
        'image.html',
        image_list=lst,
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


@app.route('/images/ground_truths/<image_name>')
def ground_truths(image_name):
    filepath = os.path.join(GROUND_TRUTH_DIR, image_name + '.lxyr')
    gts = read_lxyr(filepath)
    return json.dumps([gt.__dict__ for gt in gts])


@app.route('/images/<image_name>/ground_truths/<int:gt_id>')
def ground_truth_single(image_name, gt_id):
    """
    Returns specified volcano image from specified main image_name
    """

    # First read all ground truths of this image
    filepath = os.path.join(GROUND_TRUTH_DIR, image_name + '.lxyr')
    gts = read_lxyr(filepath)
    try:
        gt = gts[gt_id]
        # Use standard radius for all instances
        gt.radius = VOLCANO_PIXEL_SIZE

        # Extract image fragment
        signal = read_signal(IMAGE_DIR, image_name)
        rect = gt.get_rectangle()
        gt_image = signal.extract_rectangle(rect[0], rect[1])

        # Render
        image_data = render_png_raw(gt_image)
        response = make_response(image_data)
        response.headers['Content-Type'] = 'image/png'
        return response
    except:
        abort(404)


@app.route('/volcanoes')
def all_volcanoes():
    """
    Display all existing ground truth images
    """
    return None
