import os
import time
import glob
import struct
import numpy as np

from .turbines import *

class Object(object):
    pass

def read(file, verbose=0):
    filesize = os.path.getsize(file)

    # Some pre-defined structure
    head_struct = struct.Struct('IIIIHH')
    pack_struct = struct.Struct('IIIIIHHI')
    cpi_struct = struct.Struct('IIIIHHHHHHHHHHIII')
    pri_struct = struct.Struct('IIHHHHhhhhhhhhHHHHbbbbIIIIIhhhhhhhhIII')

    # Pulse
    def read_pulse(fid, pri_struct, cpi_header):
        tmp = fid.read(32 * 4)
        n = pri_struct.unpack_from(tmp)
        if n[0] != 0x11111111 or n[1] != 0xEEEEEEEE:
            print('Error: Incorrect check codes: 0x{:08X} 0x{:08X}'.format(n[0], n[1]))
            return None

        # I/Q data
        def read_iq_block(align_num, num, fid):
            if align_num:
                tmp = fid.read(align_num * 4)
                raw = np.frombuffer(tmp, dtype='<i2', count=num*2)
                return np.array(raw[::2] + 1j * raw[1::2], dtype=np.csingle)
            else:
                return np.empty(0)

        # Pulse
        pulse = Object()
        pulse.raw_pri = tmp
        pulse.counter = n[3]
        pulse.azimuth = (n[4] & 0x3FFF) * 360 / 2 ** 14
        pulse.elevation = (n[5] & 0x3FFF) * 180 / 2 ** 13
        pulse.h_pilot_hi = n[6] + 1j * n[7]
        pulse.h_pilot_lo = n[8] + 1j * n[9]
        pulse.v_pilot_hi = n[10] + 1j * n[11]
        pulse.v_pilot_lo = n[12] + 1j * n[13]
        pulse.ngate_long_hi = cpi_header.num_range_long_hi
        pulse.ngate_long_lo = cpi_header.num_range_long_lo
        pulse.ngate_short_hi = cpi_header.num_range_short_hi
        pulse.ngate_short_lo = cpi_header.num_range_short_lo
        pulse.tx_power_h_short = n[14]
        pulse.tx_power_h_long = n[15]
        pulse.tx_power_v_short = n[16]
        pulse.tx_power_v_longt = n[17]
        pulse.phase_v_long = n[18] * np.pi / 128
        pulse.phase_v_short = n[19] * np.pi / 128
        pulse.phase_h_long = n[20] * np.pi / 128
        pulse.phase_h_short = n[21] * np.pi / 128
        pulse.latitude = n[35] * 360 / 2 ** 32
        pulse.longitude = n[36] * 360 / 2 ** 32
        pulse.h_sea_level = n[37] * 0.01

        # H channel data
        pulse.h_long_hi = read_iq_block(cpi_header.align_num_range_long_hi, cpi_header.num_range_long_hi, fid)
        pulse.h_long_lo = read_iq_block(cpi_header.align_num_range_long_lo, cpi_header.num_range_long_lo, fid)
        pulse.h_short_hi = read_iq_block(cpi_header.align_num_range_short_hi, cpi_header.num_range_short_hi, fid)
        pulse.h_short_lo = read_iq_block(cpi_header.align_num_range_short_lo, cpi_header.num_range_short_lo, fid)

        # V channel data
        pulse.v_long_hi = read_iq_block(cpi_header.align_num_range_long_hi, cpi_header.num_range_long_hi, fid)
        pulse.v_long_lo = read_iq_block(cpi_header.align_num_range_long_lo, cpi_header.num_range_long_lo, fid)
        pulse.v_short_hi = read_iq_block(cpi_header.align_num_range_short_hi, cpi_header.num_range_short_hi, fid)
        pulse.v_short_lo = read_iq_block(cpi_header.align_num_range_short_lo, cpi_header.num_range_short_lo, fid)

        return pulse


    # CPI data header
    def read_cpi_header(fid, cpi_struct):
        tmp = fid.read(32 * 4)
        n = cpi_struct.unpack_from(tmp)
        if n[0] != 0x0055AAFF or n[1] != 0xFFAA5500:
            print('Error: Incorrect check codes: 0x{:08X} 0x{:08X}'.format(n[0], n[1]))
            return None

        cpi_header = Object()
        cpi_header.check_code_1 = n[0]
        cpi_header.check_code_2 = n[1]
        cpi_header.check_counter = n[2]
        cpi_header.data_size = n[3]
        cpi_header.count = n[4]
        cpi_header.num_samples = n[5]
        cpi_header.align_num_range_short_hi = n[6]
        cpi_header.align_num_range_short_lo = n[7]
        cpi_header.align_num_range_long_hi = n[8]
        cpi_header.align_num_range_long_lo = n[9]
        cpi_header.num_range_short_hi = n[10]
        cpi_header.num_range_short_lo = n[11]
        cpi_header.num_range_long_hi = n[12]
        cpi_header.num_range_long_lo = n[13]
        cpi_header.word9 = n[14]
        cpi_header.prf_code = (n[14] >> 23) & 0x03
        cpi_header.fs_code = (n[14] >> 26) & 0x03
        cpi_header.word10 = n[15]
        cpi_header.stagger_method = (n[15] >> 21) & 0x03

        return cpi_header

    # PACK data header
    def read_pack_header(fid, pack_struct):
        tmp = fid.read(32 * 4)
        n = pack_struct.unpack_from(tmp)
        if n[0] != 0x55555555 or n[1] != 0xAAAAAAAA:
            print('Error: Incorrect check codes: 0x{:08X} 0x{:08X}'.format(n[0], n[1]))
            return None

        pack_header = Object()
        pack_header.check_code_1 = n[0]
        pack_header.check_code_2 = n[1]
        pack_header.check_counter = n[2]
        pack_header.num_cpi = n[3]
        pack_header.pack_data_size = n[4]
        pack_header.division_number = n[5]
        pack_header.division_part_number = n[6]
        pack_header.mode = n[7] & 0x2 >> 1

        return pack_header

    # File header
    def read_file_header(fid, head_struct):
        tmp = fid.read(24)
        n = head_struct.unpack_from(tmp)
        file_header = Object()
        file_header.check_code_1 = n[0]
        file_header.check_code_2 = n[1]
        file_header.unknown_1 = n[2]
        file_header.unknown_2 = n[3]
        file_header.pack_count = n[4]

        return file_header
    
    # Open the file
    fid = open(file, 'rb')
    file_header = read_file_header(fid, head_struct)
    pack_header = read_pack_header(fid, pack_struct)

    if verbose:
        print('File check code 1: 0x{:08X}'.format(file_header.check_code_1))
        print('File check code 2: 0x{:08X}'.format(file_header.check_code_2))
        print('Pack count: {}'.format(file_header.pack_count))
        print('')
        print('Pack check code 1: 0x{:X}'.format(pack_header.check_code_1))
        print('Pack check code 2: 0x{:X}'.format(pack_header.check_code_2))
        print('Pack check counter: {}'.format(pack_header.check_counter))
        print('Number of CPI: {}'.format(pack_header.num_cpi))
        print('Pack data size: {}'.format(pack_header.pack_data_size))
        print('Division number: {} / {}'.format(
            pack_header.division_number, pack_header.division_part_number))
        print('Observation mode: {}'.format(pack_header.mode))
        
    # Rewind back to just after the file header
    fid.seek(24, 0)

    cpis = []
    rays = []
    for _ in range(file_header.pack_count):
        pack_header = read_pack_header(fid, pack_struct)
        if verbose:
            print('Number of CPI: {}'.format(pack_header.num_cpi))
        for _ in range(pack_header.num_cpi):
            cpi_header = read_cpi_header(fid, cpi_struct)
            if cpi_header:
                pulses = []
                for k in range(cpi_header.count):
                    pulse = read_pulse(fid, pri_struct, cpi_header)
                    pulses.append(pulse)
                cpis.append(cpi_header)
                rays.append(pulses)
                if verbose:
                    print('    cpi:{:3d}   {:08d}   E:{:.2f}   A:{:6.2f}-{:6.2f} ({})   size:{}'.format(
                        cpi_header.check_counter,
                        pulses[0].counter,
                        pulses[0].elevation, pulses[0].azimuth, pulses[-1].azimuth,
                        cpi_header.count,
                        cpi_header.data_size))
            else:
                break
    
    if filesize < fid.tell():
        print('Warning: There is still {} B left.'.format(filesize - fid.tell()))
    fid.close()
    
    return rays, cpis
