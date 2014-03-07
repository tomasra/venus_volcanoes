import png


def render_png(signal):
    """
    Renders signal data into grayscale .png image object.
    """
    image_rows = [row for row in signal]
    return png.from_array(image_rows, 'L')  # greyscale


def render_png_to_file(signal, filename):
    """
    Renders signal and saves as .png file
    """
    image = render_png(signal)
    image.save(filename)
