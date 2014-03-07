import os
from lib.models import RawSignal, GroundTruth


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
    try:
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

        # Create the signal
        signal = RawSignal(
            rows=rows,
            cols=cols,
            data=data,
            name=signal_name)
        return signal
    except Exception:
        # Files not found?
        return None


def read_signals(directory):
    """
    Enumerates all valid spr/sdt file pairs in given directory
    and creates a list of signal objects
    """
    return [
        read_signal(directory, signal_name)
        for signal_name in list_signals(directory)
    ]


def read_lxyr(filepath):
    """
    Reads a list of ground truths from lxyr file
    """
    with open(filepath, 'r') as f:
        ground_truths = [
            _parse_lxyr_entry(line)
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
