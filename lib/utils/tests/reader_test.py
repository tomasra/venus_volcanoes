import unittest
import os
import numpy as np
from lib.utils.reader import read_signal, read_signals, list_signals
from lib.utils.reader import read_lxyr, read_lxyrs


class ReaderTests(unittest.TestCase):
    def test_read_one_signal(self):
        """
        Reads one signal from test spr/sdt files
        """
        cwd = os.path.dirname(os.path.abspath(__file__))
        spr_path = os.path.join(cwd, 'test_files/')
        signal = read_signal(spr_path, 'test3')
        self.assertEqual(signal.data.shape[0], 8)
        self.assertEqual(signal.data.shape[1], 4)
        actual = signal.to_vector()
        expected = np.arange(32)
        self.assertTrue(np.array_equal(actual, expected))
        self.assertEqual(signal.name, "test3")

    def test_read_one_signal_failure(self):
        """
        Try to read non-existing signal
        or provide invalid directory name
        """
        cwd = os.path.dirname(os.path.abspath(__file__))
        dir1 = os.path.join(cwd, 'test_files/')
        dir2 = '/home/tomas/here-be-dragons/'
        signal1 = read_signal(dir1, 'here-be-dragons')
        signal2 = read_signal(dir2, 'test3')
        self.assertIsNone(signal1)
        self.assertIsNone(signal2)

    def test_list_signal_directory(self):
        """
        Enumerate names of SPR/SDT file pairs
        in given directory
        """
        cwd = os.path.dirname(os.path.abspath(__file__))
        signal_dir = os.path.join(cwd, 'test_files/')
        signal_names = list_signals(signal_dir)
        self.assertSequenceEqual(
            sorted(signal_names),
            sorted(['test1', 'test2', 'test3'])
        )

    def test_read_multiple_signals(self):
        """
        Reads several signals from specified directory
        """
        cwd = os.path.dirname(os.path.abspath(__file__))
        test_dir = os.path.join(cwd, 'test_files/')
        signals = read_signals(test_dir)
        self.assertEqual(len(signals), 3)
        self.assertTrue(
            any(signal for signal in signals if signal.name == "test1"))
        self.assertTrue(
            any(signal for signal in signals if signal.name == "test2"))
        self.assertTrue(
            any(signal for signal in signals if signal.name == "test3"))

    def test_read_multiple_specified_signals(self):
        """
        Reads only specified signals from the directory
        """
        cwd = os.path.dirname(os.path.abspath(__file__))
        test_dir = os.path.join(cwd, 'test_files/')
        signals = read_signals(test_dir, ['test2', 'test3'])
        self.assertEquals(len(signals), 2)

    def test_read_lxyr(self):
        """
        Read ground truths from file
        """
        cwd = os.path.dirname(os.path.abspath(__file__))
        # gt_file = os.path.join(cwd, 'test_files/test_gt.lxyr')
        # ground_truths = read_lxyr(gt_file)
        test_dir = os.path.join(cwd, 'test_files/')
        ground_truths = read_lxyr(test_dir, 'test_gt')
        # print ground_truths
        self.assertTrue(any(
            gt for gt in ground_truths
            if gt.x == 553 and gt.y == 132
            and gt.radius == 16.64 and gt.class_value == 3))
        self.assertTrue(any(
            gt for gt in ground_truths
            if gt.x == 119 and gt.y == 631
            and gt.radius == 15.0 and gt.class_value == 4))

    def test_read_multiple_lxyrs(self):
        """
        Read multiple ground truth files
        """
        cwd = os.path.dirname(os.path.abspath(__file__))
        test_dir = os.path.join(cwd, 'test_files/')
        ground_truths = read_lxyrs(test_dir)
        self.assertEquals(len(ground_truths), 3)
        self.assertEquals(len(ground_truths['test1']), 3)
        self.assertEquals(len(ground_truths['test_gt']), 2)
