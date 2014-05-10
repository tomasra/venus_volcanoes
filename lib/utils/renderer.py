import png
import StringIO
import numpy as np


def render_png(image):
    """
    Renders signal data into grayscale .png image object.
    """
    image_rows = [row.astype(np.uint8) for row in image]
    return png.from_array(image_rows, 'L')  # greyscale


def render_png_raw(image):
    """
    Renders signal data and returns raw png image data
    """
    output = StringIO.StringIO()
    render_png(image).save(output)
    raw_data = output.getvalue()
    output.close()
    return raw_data


def render_png_to_file(image, filename):
    """
    Renders signal and saves as .png file
    """
    rendered = render_png(image)
    rendered.save(filename)
