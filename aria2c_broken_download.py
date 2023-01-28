#!/bin/python3

import os, sys
import argparse
from math import ceil, floor
from struct import pack, unpack

# Control file (*.aria2) format
#  0                   1                   2                   3
#  0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1
# +---+-------+-------+-------------------------------------------+
# |VER|  EXT  |INFO   |INFO HASH ...                              |
# |(2)|  (4)  |HASH   | (INFO HASH LENGTH)                        |
# |   |       |LENGTH |                                           |
# |   |       |  (4)  |                                           |
# +---+---+---+-------+---+---------------+-------+---------------+
# |PIECE  |TOTAL LENGTH   |UPLOAD LENGTH  |BIT-   |BITFIELD ...   |
# |LENGTH |     (8)       |     (8)       |FIELD  | (BITFIELD     |
# |  (4)  |               |               |LENGTH |  LENGTH)      |
# |       |               |               |  (4)  |               |
# +-------+-------+-------+-------+-------+-------+---------------+
# |NUM    |INDEX  |LENGTH |PIECE  |PIECE BITFIELD ...             |
# |IN-    |  (4)  |  (4)  |BIT-   | (PIECE BITFIELD LENGTH)       |
# |FLIGHT |       |       |FIELD  |                               |
# |PIECE  |       |       |LENGTH |                               |
# |  (4)  |       |       |  (4)  |                               |
# +-------+-------+-------+-------+-------------------------------+

#         ^                                                       ^
#         |                                                       |
#         +-------------------------------------------------------+
#                 Repeated in (NUM IN-FLIGHT) PIECE times

MiB = 1048576

parser = argparse.ArgumentParser("aria2c HTTP(S)/FTP Broken Download Repair", description="Not repair, but find not downloaded parts (guessing) and (re)build <filename>.aria2 file again :)")
parser.add_argument(metavar='files', dest='files', nargs='+', type=str, help="Broken downloaded file(s)")
args = parser.parse_args()

def create_control_file(file_address, bitfield):
    with open(file_address + '.aria2', "wb") as fo:
        INFO_HASH_LENGTH=0
        EXT=0
        PIECE_LENGTH=MiB
        TOTAL_LENGTH=os.path.getsize(file_address)
        UPLOAD_LENGTH=0
        bitfield_length = ceil(len(bitfield)/8)
        bitfield_packed = [0] * ceil(len(bitfield)/8)
        for i in range(len(bitfield)):
            if bitfield[i] == '1':
                bitfield_packed[int(i/8)] |= 1 << (7-(i%8))
        fo.write(pack('>HIIIQQI', 1, EXT, INFO_HASH_LENGTH, PIECE_LENGTH, TOTAL_LENGTH, UPLOAD_LENGTH, bitfield_length))
        fo.write(bytes(bitfield_packed))
        NUM_INFLIGHT_PIECES=0
        fo.write(pack('>I', NUM_INFLIGHT_PIECES))

for f in args.files:
    if not os.path.exists:
        print(f'ERROR: file "{f}" not exists.')
        continue
    fsize = os.path.getsize(f)
    bitfield = ['0'] * ceil(fsize/MiB)
    with open(f, "rb") as fi:
        for i in range(ceil(fsize/MiB)):
            print(f'\r{f} [{i:04d}/{ceil(fsize/MiB):04d}]', end='')
            fi.seek(i * MiB, os.SEEK_SET) # next block
            if fi.read(1024) == (b'\x00' * 1024):
                print(' EMPTY')
                if i > 0:
                    bitfield[i-1] = '0'
            else:
                bitfield[i] = '1'
        create_control_file(f, bitfield)
