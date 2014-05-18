import os
import numpy as np
from lib.models import Image, GroundTruth


def list_signals(directory):
    """
    Returns list of signal (SPR/SDT file pair) names
    in given directory
    """
    return [
        # Unique filenames without extensions
        signal_name
        for signal_name in set([
            os.path.splitext(filename)[0]
            for filename in os.listdir(directory)
        ])
        # Check if both SPR and SDT files exist
        if _get_signal_filenames(directory, signal_name)
    ]


def read_signal(directory, signal_name):
    """
    Creates signal object from .spr file
    and its corresponding .sdt file with signal data.
    """
    # try:
    signal_filenames = _get_signal_filenames(directory, signal_name)
    spr_path = signal_filenames['spr']
    sdt_path = signal_filenames['sdt']

    # Read .spr file
    with open(spr_path, 'r') as f:
        # num not needed at the moment
        f.readline()
        cols = int(f.readline())
        # not needed
        f.readline()
        f.readline()
        rows = int(f.readline())
        # not needed
        f.readline()
        f.readline()
        # dtype not needed at the moment
        f.readline()

    # Read .sdt file
    with open(sdt_path, 'rb') as f:
        data = [int(b) for b in bytearray(f.read())]

    # Convert to numpy array
    data = np.array(data).reshape((rows, cols)).astype(np.uint8)

    # Create the signal
    signal = Image(
        data=data,
        name=signal_name)
    return signal
    # except Exception:
    #     # Files not found?
    #     return None


def read_spoiled_image(directory, image_name, spoil_size=2):
    """
    Special case for reading matched filter template images.
    Their actual dimensions are twice as big as specified in .spr file,
    so it's necessary to read the image in small blocks
    (spoil_size X spoil_size) and take their averages.
    """
    image_filenames = _get_signal_filenames(directory, image_name)
    spr_path = image_filenames['spr']
    sdt_path = image_filenames['sdt']

    # Read .spr file
    with open(spr_path, 'r') as f:
        # num not needed at the moment
        f.readline()
        cols = int(f.readline())
        # not needed
        f.readline()
        f.readline()
        rows = int(f.readline())
        # not needed
        f.readline()
        f.readline()
        # dtype not needed at the moment
        f.readline()

    # Read .sdt file
    with open(sdt_path, 'rb') as f:
        data = [int(b) for b in bytearray(f.read())]

    # data_rows = rows * spoil_size
    # data_cols = cols * spoil_size
    # raw_data = np.array(data).reshape((data_rows, data_cols)).astype(np.uint8)

    # spoiled_data = np.array([
    #     int(np.rint(np.mean(raw_data[
    #         row:row + spoil_size,
    #         col:col + spoil_size])))
    #     for col in xrange(0, data_cols, spoil_size)
    #     for row in xrange(0, data_rows, spoil_size)
    # ]).reshape(rows, cols).astype(np.uint8)

    spoiled_data = np.array([
        int(np.rint(np.mean(data[idx:idx + pow(spoil_size, 2)])))
        for idx in xrange(0, len(data), pow(spoil_size, 2))
    ]).reshape(rows, cols).astype(np.uint8)

    # import pdb; pdb.set_trace()
    # Convert to numpy array

    # Create the signal
    signal = Image(
        data=spoiled_data,
        name=image_name)
    return signal


def read_signals(directory, image_names=None):
    """
    Enumerates all valid spr/sdt file pairs in given directory
    and creates a list of signal objects
    """
    if image_names:
        return [
            read_signal(directory, name)
            for name in list_signals(directory)
            if name in image_names
        ]
    else:
        return [
            read_signal(directory, name)
            for name in list_signals(directory)
        ]


def read_lxyr(directory, image_name):
    """
    Reads a list of ground truths from lxyr file
    """
    filepath = os.path.join(directory, image_name + '.lxyr')
    with open(filepath, 'r') as f:
        ground_truths = [
            _parse_lxyr_entry(line)
            for line in f.readlines()
            # Check if string is not empty
            # (remove trailing whitespace with strip()).
            if line.strip()
        ]
    return ground_truths


def read_lxyrs(directory):
    """
    Reads dict of all ground truth files from directory
    """
    gt_names = _get_lxyr_list(directory)
    return dict(zip(
        gt_names,
        [read_lxyr(directory, gt_name) for gt_name in gt_names]
    ))


def read_lxyv(directory, image_name):
    """
    Reads FOA entries from lxyv file
    """
    filepath = os.path.join(directory, image_name + '.lxyv')
    with open(filepath, 'r') as f:
        ground_truths = [
            _parse_lxyv_entry(line)
            for line in f.readlines()
            # Check if string is not empty
            # (remove trailing whitespace with strip()).
            if line.strip()
        ]
    return ground_truths


def _parse_lxyr_entry(line):
    """
    Parses one line from .lxyr file and returns ground truth object.
    """
    parts = line.split()
    return GroundTruth(
        x=int(float(parts[1])),
        y=int(float(parts[2])),
        radius=float(parts[3]),
        class_value=int(parts[0])
    )


def _parse_lxyv_entry(line):
    """
    Parses one line from .lxyv file and
    returns GroundTruth object
    """
    parts = line.split()
    return GroundTruth(
        x=int(float(parts[1])),
        y=int(float(parts[2])),
        corr_value=float(parts[3]),
        class_value=int(parts[0])
    )


def _get_signal_filenames(directory, signal_name):
    """
    Finds SPR/SDT files with given name in the directory
    and returns their full paths as a dictionary
    """
    spr_path = os.path.join(directory, signal_name + '.spr')
    sdt_path = os.path.join(directory, signal_name + '.sdt')
    if os.path.isfile(spr_path) and os.path.isfile(sdt_path):
        return {
            'spr': spr_path,
            'sdt': sdt_path
        }
    else:
        # One or both files not found?
        return None


def _get_lxyr_list(directory):
    """
    Returns .lxyr file list from specified directory.
    Only filenames without extensions are returned
    """
    return [
        # Unique filenames without extensions
        signal_name
        for signal_name in set([
            os.path.splitext(filename)[0]
            for filename in os.listdir(directory)
            if os.path.splitext(filename)[1] == ".lxyr"
        ])
    ]
