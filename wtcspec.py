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
filename = files[1]

# Read the raw data
tic = time.time()
ray_pulses, cpi_headers = toshi.read(filename)
toc = time.time()
print('{} read in {:.2f} s'.format(os.path.basename(filename), toc - tic))

# Go through the pulses for azimuth
az = np.zeros(len(ray_pulses), dtype=np.single)
for k, pulses in enumerate(ray_pulses):
    az[k] = pulses[0].azimuth

# Dimensions
naz = len(ray_pulses)
ngate_short_hi = ray_pulses[0][0].cpi_header.num_range_short_hi
ngate_short_lo = ray_pulses[0][0].cpi_header.num_range_short_lo
ngate_long = ray_pulses[0][0].cpi_header.num_range_long_hi

scan_time = time.strptime(os.path.basename(filename)[:15], '%Y%m%d_%H%M%S')
scan_el = ray_pulses[0][0].elevation

# Sampling code from the CPI header
fs = 1.0e6 * (1 << cpi_headers[0].fs_code)
dr = 3.0e8 / fs / 2
r = 1.0e-3 * (np.arange(0, ngate_long, dtype=np.single) * dr + 0.5 * dr)

# Cell indices of the cells with wind turbines
cid = cspec.pos2cellid(turbines, np.unique(az), r)

# Revise ngate since I only care up to this gate, pad a bit extra
ngate = np.max(np.array(cid)[:, 1]) + 10

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
        p[j, :ngate] = pc[j, :ngate]                                       # Long only
        p[j, :ngate_short_hi] = pulse.h_short_hi * c                       # Short hi
        p[j, :ngate_short_lo] = pulse.h_short_lo * c                       # Short lo        

    cpuls.append(p)                                                        # Keep a copy of the compressed pulse

# BScope - only look at even rays since it was operated in dual PRF mode
# Unable to determine PRT, best guess is slightly > ngate_long x fs = 0.396 ms
# Assume 0.4 ms, which corresponds to 2500 Hz PRF, reasonable
bscope = np.zeros((ngate, int(naz / 2)), dtype=np.single)
for k, p in enumerate(cpuls[::2]):
    bscope[:, k] = np.mean(np.abs(p / 32e3) ** 2, axis=0)
bscope = 10.0 * np.log10(bscope)
m = [x[1] for x in cid]
n = cpuls[0].shape[0]
te = np.arange(int(naz / 2) + 1) * n * 0.4e-3
re = 1.0e-3 * np.arange(ngate + 1) * dr

plt.pcolormesh(te, re, bscope)
plt.plot(np.ones((len(m),)), r[m], 'xw', linewidth=0.5)
plt.clim((-60, 0))
plt.colorbar()
plt.xlabel('Time (s)')
plt.ylabel('Range (km)')
plt.title('Relative Signal Strength (dB)')

def spectrogram(igate):
    nfft = 1024
    n = cpuls[0].shape[0]
    tscope = np.zeros((int(naz/2), nfft), dtype=np.csingle)
    w = scipy.signal.get_window('blackmanharris', n)
    w /= np.sqrt(np.mean(w ** 2))
    for k, cpul in enumerate(cpuls[::2]):
        p = cpul[:, igate] / 32000
        tscope[k, :] = sp.fft.fft(p * w, nfft, axis=0)
    tscope = sp.fft.fftshift(tscope, axes=(1,))
    tscope = 10.0 * np.log10(np.abs(tscope) ** 2 / np.sqrt(nfft))
    
    te = np.arange(naz + 1) * n * 0.4e-3
    omega = np.arange(-nfft / 2, nfft / 2 + 1) / nfft
    plt.figure()
    plt.pcolormesh(omega, te[::2], tscope)
    plt.clim((-60, -10))
    cb = plt.colorbar()
    cb.ax.set_ylabel('Relative Signal Strength (dB)')
    plt.xlabel('Discrete Frequency (x $\pi$) (rad/sample)')
    plt.ylabel('Time (s)')
    plt.title('Spectogram of Cell #{} ({:.2f} m)'.format(igate, r[igate]))

spectrogram(107)
plt.ylim((0, 5))

# for igate in [107, 113, 117]:
#     spectrogram(igate)
