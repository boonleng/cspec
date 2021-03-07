#!/usr/bin/env python3

"""
Created on Sun Mar  7 08:05:32 2021

@author: boonleng
"""

import os
import time
import glob
import numpy as np
import scipy as sp
import scipy.signal
import matplotlib
import matplotlib.patheffects
import matplotlib.pyplot as plt

import toshi
import cspec

# plt.style.use('./darkmode.style')
plt.style.use('./lightmode.style')
vmap = matplotlib.colors.LinearSegmentedColormap.from_list('colors', cspec.colormap.vmap()[:, :3], 64)
zmap = matplotlib.colors.LinearSegmentedColormap.from_list('colors', cspec.colormap.zmap()[:, :3])

path_effects = [
    matplotlib.patheffects.Stroke(linewidth=1.6, foreground=(0, 0, 0, 0.8)),
    matplotlib.patheffects.Normal()
]

###

def proc_file(filename, verbose=0):
    s = time.time()
    ray_pulses, cpi_headers = toshi.read(filename)
    e = time.time()
    if verbose:
        print('{} read in {:.2f} s'.format(os.path.basename(filename), e - s))
    
    return ray_pulses, cpi_headers

###

# Waveform table
waveform = toshi.tx_waveform()
pc_nfft = 1024
wf = sp.fft.fft(waveform / np.sqrt(np.sum(np.abs(waveform) ** 2)), n=pc_nfft)

# WTC table
wtc_loc = toshi.wtc_loc_from_csv()
turbines = np.array([[pt[2], pt[1]] for pt in wtc_loc], dtype=np.single)

# Raw data tree
data_home = os.path.expanduser('~/Downloads/toshiba/AKITA_IQ_TO_OU/IQdata')
files = glob.glob('{}/2021.01.15/*/*.dat'.format(data_home), recursive=True)
files = sorted(files)
filename = files[0]

ray_pulses, cpi_headers = proc_file(filename, verbose=1)

# Go through the pulses for azimuth
az = np.zeros(len(ray_pulses), dtype=np.single)
for k, pulses in enumerate(ray_pulses):
    az[k] = pulses[0].azimuth

# Dimensions
naz = len(ray_pulses)
ngate_long = ray_pulses[0][0].cpi_header.num_range_long_hi
ngate_short_hi = ray_pulses[0][0].cpi_header.num_range_short_hi
ngate_short_lo = ray_pulses[0][0].cpi_header.num_range_short_lo
ngate = ngate_long + ngate_short_hi + ngate_short_lo

scan_time = time.strptime(os.path.basename(filename)[:15], '%Y%m%d_%H%M%S')
scan_el = ray_pulses[0][0].elevation

# Sampling code from the CPI header
fs = 1.0e6 * (1 << cpi_headers[0].fs_code)
dr = 3.0e8 / fs / 2
r = 1.0e-3 * (np.arange(0, ngate, dtype=np.single) * dr + 0.5 * dr)

# Cell indices of the cells with wind turbines
cid = cspec.pos2cellid(turbines, np.unique(az), r)

use_window = True

# Go through the pulses
cpuls = []
for k, (pulses, cpi_header) in enumerate(zip(ray_pulses, cpi_headers)):
    npulse = len(pulses)

    # Decode the long pulse, then compress using wf
    p = np.zeros((npulse, ngate_long), dtype=np.csingle)
    for j, pulse in enumerate(pulses):
        p[j, :] = pulse.h_long_hi * np.exp(-1j * pulse.phase_h_long)       # Phase decoding
    pf = sp.fft.fft(p, n=pc_nfft, axis=1)                                  # Pulse compression in Fourier domain
    pc = sp.fft.ifft(pf * wf, n=pc_nfft, axis=1)                           # Return to time domain

    # Gather the short pulses and the compressed long pulses
    p = np.zeros((npulse, ngate), dtype=np.csingle)
    for j, pulse in enumerate(pulses):
        c = np.exp(-1j * pulse.phase_h_short)                              # Phase code
        p[j, :ngate_long] = pc[j, :ngate_long]                             # Long only
        p[j, :ngate_short_hi] = pulse.h_short_hi * c                       # Short hi
        p[j, :ngate_short_lo] = pulse.h_short_lo * c                       # Short lo        

    cpuls.append(pc[:ngate])                                                       # Keep a copy of the compressed pulse

    # Data windowing
    if use_window:
        w = scipy.signal.get_window('blackmanharris', len(p))
    else:
        w = np.ones((p.shape[0],))
    w /= np.sqrt(np.sum(w ** 2)) / np.sqrt(p.shape[0])                     # Normalize to non-windowed gain
    ww = np.repeat(np.expand_dims(w, axis=1), ngate, axis=1)               # Make same shape
    p *= ww                                                                # Windowing

for cpul in