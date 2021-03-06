import unittest
import os
from lib.utils.image_set import ImageSet


class ImageSetTests(unittest.TestCase):
    def test_get_image_by_name(self):
        """
        Returns image object by its name
        """
        cwd = os.path.dirname(os.path.abspath(__file__))
        test_dir = os.path.join(cwd, 'test_files/')

        # act
        image_set = ImageSet(test_dir)

        # assert
        self.assertEqual(len(image_set), 3)
        self.assertEqual(image_set['test1'].data.shape[0], 4)
        self.assertEqual(image_set['test2'].data.shape[0], 4)
        self.assertEqual(image_set['test3'].data.shape[0], 8)
        self.assertIsNone(image_set['here_be_dragons'])

    def test_get_image_with_ground_truths(self):
        """
        Checks if requested image has associated ground truths loaded
        """
        cwd = os.path.dirname(os.path.abspath(__file__))
        test_dir = os.path.join(cwd, 'test_files/')

        # act
        image_set = ImageSet(test_dir, test_dir)

        # assert
        self.assertEquals(len(image_set['test1'].ground_truths), 3)
        self.assertSequenceEqual(
            [gt.class_value for gt in image_set['test1'].ground_truths],
            [3, 4, 0])
        # no ground truths for this signal
        self.assertEquals(len(image_set['test2'].ground_truths), 0)

    def test_make_image_set_with_name_filter(self):
        """
        Make image set only from specified images in the directory
        """
        cwd = os.path.dirname(os.path.abspath(__file__))
        test_dir = os.path.join(cwd, 'test_files/')
        image_set = ImageSet(test_dir, image_names=['test1', 'test3'])
        self.assertEquals(len(image_set), 2)
        self.assertIsNotNone(image_set['test1'])
        self.assertIsNotNone(image_set['test3'])

    def test_get_ground_truth_classes(self):
        """
        Collect a list of ground truth classes of all signals
        """
        cwd = os.path.dirname(os.path.abspath(__file__))
        test_dir = os.path.join(cwd, 'test_files/')
        image_set = ImageSet(test_dir, test_dir, image_names=['test1', 'test3'])
        classes = image_set.ground_truth_classes()
        self.assertEquals(classes.count(1), 1)
        self.assertEquals(classes.count(2), 1)
        self.assertEquals(classes.count(3), 2)
        self.assertEquals(classes.count(4), 2)
        self.assertEquals(classes.count(0), 1)
