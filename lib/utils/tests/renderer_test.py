import os
import unittest
import png
from lib.utils.renderer import render_png, render_png_to_file, render_png_raw
from lib.models import RawSignal


class RendererTests(unittest.TestCase):
    def test_render_png(self):
        """
        Checks how simple signal is rendered into png format
        """
        signal = RawSignal(rows=3, cols=2, data=[0, 1, 2, 3, 4, 5])
        image = render_png(signal)
        self.assertEqual(image.info['greyscale'], True)
        self.assertEqual(image.info['height'], 3)
        self.assertEqual(image.info['width'], 2)

    def test_render_png_to_file(self):
        """
        Checks if signal is rendered and saved as png file
        """
        cwd = os.path.dirname(os.path.abspath(__file__))
        test_filepath = os.path.join(cwd, 'test.png')
        # Just in case the test image already exists
        if os.path.exists(test_filepath):
            os.remove(test_filepath)

        signal = RawSignal(rows=3, cols=2, data=[0, 1, 2, 3, 4, 5])
        render_png_to_file(signal, test_filepath)
        self.assertTrue(
            os.path.exists(test_filepath),
            'PNG file was not created')

        reader = png.Reader(filename=test_filepath)
        # this returns tuple, not Image object
        image = reader.read()
        self.assertEqual(image[0], 2)   # width
        self.assertEqual(image[1], 3)   # height

        # Cleanup
        if os.path.exists(test_filepath):
            os.remove(test_filepath)

    def test_render_png_for_web(self):
        """
        Checks if signal is rendered and its raw png data is returned
        """
        signal = RawSignal(rows=3, cols=2, data=[0, 1, 2, 3, 4, 5])
        image_data = render_png_raw(signal)
        self.assertTrue('PNG' in image_data)
