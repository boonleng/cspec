import struct

import numpy as np

def drv_sig(filename='blob/LPlsDatHNo1.txt'):
    with open(filename, 'rb') as fid:
        lines = fid.readlines()
    data = []
    for k, row in enumerate(lines):
        if k < 5:
            continue
        s = row.decode().replace('[\t\n]', '')
        n = [float(o) for o in s.split(',')]
        data.append(n)
    return np.array(data, dtype=np.single)


def tx_waveform(filename='blob/Ref_TableH1.bin'):
    with open(filename, 'rb') as fid:
        dat = fid.read()
    count = int(len(dat) / 4)
    samples = struct.unpack('f' * count, dat)
    return np.array(samples[::2]) + 1j * np.array(samples[1::2])