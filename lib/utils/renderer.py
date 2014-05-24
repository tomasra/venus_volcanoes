import png
import StringIO
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as cm


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


def render_png_plot(image):
    plt.imshow(image, cmap=cm.Greys_r)
    plt.show()


def render_mosaic(images, filename):
    """
    Copy-paste from GA code...
    """
    images = [
        [img.data]
        for img in images
    ]
    width = int(np.sqrt(len(images))) + 1
    height = int(np.sqrt(len(images))) + 1
    borders = True
    """
    Makes a width x height mosaic
    from provided images (lists of numpy arrays)
    """
    shapes = set([
        plane.shape
        for image in images
        for plane in image
    ])
    planes = set([len(image) for image in images])
    if len(planes) > 1:
        raise ValueError(
            "Images should have the same number of color planes")
    if len(shapes) > 1:
        raise ValueError(
            "Images should have the same dimensions")
    elif len(images) > (width * height):
        raise ValueError(
            "Image count is larger than mosaic dimensions")
    else:
        shape, planes = list(shapes)[0], list(planes)[0]
        image_width, image_height = shape[1], shape[0]
        mosaic_width = image_width * width
        mosaic_height = image_height * height
        mosaic = [
            np.zeros((mosaic_height, mosaic_width), dtype=np.uint8)
            for i in xrange(planes)
        ]
        for idx, image in enumerate(images):
            # Image indexes (0-based) in the mosaic
            mosaic_x, mosaic_y = idx % width, idx / width
            top_left_x = mosaic_x * image_width
            top_left_y = mosaic_y * image_height
            # Copy all planes
            for plane_idx in xrange(planes):
                mosaic[plane_idx][
                    top_left_y:top_left_y + image_height,
                    top_left_x:top_left_x + image_width
                ] = image[plane_idx]
            if borders:
                # Right and bottom border for each image
                for plane_idx in xrange(planes):
                    # Right
                    mosaic[plane_idx][
                        top_left_y:top_left_y + image_height,
                        # "Index out of bounds" happens without this one
                        top_left_x + image_width - 1
                    ] = 0
                    # Bottom
                    mosaic[plane_idx][
                        top_left_y + image_height - 1,
                        top_left_x:top_left_x + image_width
                    ] = 0
        # Top and left border for whole mosaic
        if borders:
            for plane_idx in xrange(planes):
                mosaic[plane_idx][0, 0:mosaic_width] = 0
                mosaic[plane_idx][0:mosaic_height, 0] = 0
    render_png_to_file(mosaic[0], filename)
