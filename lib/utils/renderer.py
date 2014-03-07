import png
import StringIO


def render_png(signal):
    """
    Renders signal data into grayscale .png image object.
    """
    image_rows = [row for row in signal]
    return png.from_array(image_rows, 'L')  # greyscale


def render_png_raw(signal):
    """
    Renders signal data and returns raw png image data
    """
    output = StringIO.StringIO()
    render_png(signal).save(output)
    raw_data = output.getvalue()
    output.close()
    return raw_data


def render_png_to_file(signal, filename):
    """
    Renders signal and saves as .png file
    """
    image = render_png(signal)
    image.save(filename)
