import os
import json
from app import app
from flask import abort, render_template, make_response

from config import IMAGE_DIR, GROUND_TRUTH_DIR
from lib.utils.reader import list_signals, read_signal, read_lxyr
from lib.utils.renderer import render_png_raw


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/images')
def images():
    lst = sorted(list_signals(IMAGE_DIR))
    return render_template(
        'image.html',
        image_list=lst,
        selected_image=None)


@app.route('/images/<image_name>')
def image_select(image_name):
    lst = sorted(list_signals(IMAGE_DIR))
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
