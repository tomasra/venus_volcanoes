import os
from lib.models import RawSignal, GroundTruth


def read_signal(spr_path):
    """
    Creates signal object from .spr file
    and its corresponding .sdt file with signal data.
    """

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
    sdt_path = os.path.splitext(spr_path)[0] + '.sdt'
    filename = os.path.splitext(os.path.basename(spr_path))[0]
    with open(sdt_path, 'rb') as f:
        data = [int(b) for b in bytearray(f.read())]

    # Create the signal
    signal = RawSignal(
        rows=rows,
        cols=cols,
        data=data,
        name=filename)
    return signal


def read_signals(directory):
    """
    Enumerates all valid spr/sdt file pairs in given directory
    and creates a list of signal objects
    """
    return [
        read_signal(os.path.join(directory, filename))
        for filename in os.listdir(directory)
        if filename.endswith('.spr')
    ]


def read_lxyr(filename):
    """
    Reads a list of ground truths from lxyr file
    """
    with open(filename, 'r') as f:
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
