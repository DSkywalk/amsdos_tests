#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
   Copyright (C) 2022 David Colmenero - D_Skywalk

   This program is free software; you can redistribute it and/or modify
   it under the terms of the GNU General Public License as published by
   the Free Software Foundation; either version 3 of the License, or
   higher any later version.

   This program is distributed in the hope that it will be useful,
   but WITHOUT ANY WARRANTY; without even the implied warranty of
   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
   GNU General Public License for more details.

   You should have received a copy of the GNU General Public License
   along with this program; if not, write to the Free Software Foundation,
   Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301  USA
   
   HACK AMSDOS HEADER!
   
"""

import os, sys, struct

if sys.argv.__len__() != 6:
    print('Error: invalid args\nusage:', sys.argv[0], '<source-bas-path> <source-bin-path> <hex-address-append> <hex-token-exe> <out-file>')
    exit(1)

bas_file = sys.argv[1]
bin_file = sys.argv[2]
file_size = -1
addr = int(sys.argv[3], 16)
exe = int(sys.argv[4], 16)
out_file = sys.argv[5]
header_len = 128
call_token = int('0x1c0000', 16)

with open(bas_file, 'rb') as lr:
    # start get data!    
    fstatus = lr.read(1)
    print('status', fstatus)
    name = lr.read(8+3).decode('ascii')
    print('name', name)
    zeroes_pad = lr.read(4)
    # print('pad_1', zeroes_pad, '(unused)')
    block_nr = lr.read(1)
    print('block_nr', block_nr, '(unused)')
    block_last = lr.read(1)
    print('block_last', block_last, '(unused)')
    file_type = lr.read(1)
    print('file_type', file_type)
    data_length = lr.read(2)
    print('data_length', data_length)
    data_location = int.from_bytes(lr.read(2), byteorder='little', signed=False)
    print('data_location', hex(data_location))
    first_block = lr.read(1)
    print('first_block', first_block)
    logical_length = int.from_bytes(lr.read(2), byteorder='little', signed=False)
    print('logical_length', logical_length, '(%s)' % hex(logical_length))
    entry_address = int.from_bytes(lr.read(2), byteorder='little', signed=False)
    print('entry_address', entry_address, '(%s)' % hex(entry_address))
    zeroes_pad = lr.read(36)
    # print('pad_2', zeroes_pad, '(unused)')
    file_length = int.from_bytes(lr.read(3), byteorder='little', signed=False)
    print('file_length', file_length, '{0:#0{1}x}'.format(file_length, 8))
    checksum = int.from_bytes(lr.read(2), byteorder='little', signed=False)
    print('checksum', checksum, '{0:#0{1}x}'.format(checksum, 6))

    
    # copy bas to destiny file
    fout = open(out_file,'wb')
    lr.seek(0, os.SEEK_SET)
    bas_data = header_len + logical_length
    data = lr.read(bas_data)
    fout.write(data)

    # dummy data until bin addr
    for n in range(0, addr - bas_data):
        fout.write(struct.pack("<B", 0))
    
    # copy bin to destiny file
    fbin = open(bin_file,'rb')
    data = fbin.read()
    fout.write(data)
    fbin.close()
    file_size = fout.tell() - header_len - 1

    # change length
    fout.seek(24)
    # logical_length
    print('old_length', hex(logical_length), '=> new_length', hex(file_size))
    fout.write(struct.pack("<H", file_size))
    # file_length
    fout.seek(36 + 2, os.SEEK_CUR) # pass 36 + 2 bytes
    fout.write(struct.pack("<H", file_size))

    # find CALL &FEA5 [1CA5FE]
    lr.seek(header_len, os.SEEK_SET)
    found = False
    while True:
        position = lr.tell()
        token = int.from_bytes(lr.read(3), byteorder='big', signed=False)
        # print(hex(token), position)
        if token == 0x1CA5FE:
            fout.seek(position + 1, os.SEEK_SET)
            # 1C > ADD EXEC ADDRESS AFTER TOKEN
            fout.write(struct.pack("<H", exe))
            print('CALL TOKEN [1CA5FE]: found at', position, 'exec:', hex(exe))
            found = True
        if position > (logical_length + header_len):
            if not found:
                print("CALL TOKEN [1CA5FE]: NOT FOUND!", position, logical_length + header_len)
            break
        lr.seek(-2, os.SEEK_CUR)

    # close to read current header
    fout.close()
    # calc new checksum with refresh data
    fout = open(out_file,'rb')
    calc = 0
    for n in range(0, 66 + 1):
        byte_val = int.from_bytes(fout.read(1), byteorder='little', signed=False)
        calc += byte_val
    print('new_checksum', calc, n, hex(calc))

    # update checksum
    fout = open(out_file,'r+b')
    fout.seek(67, os.SEEK_SET)
    fout.write(struct.pack("<H", calc))
    
    # clean rest header 
    for n in range(0, header_len - (67 + 2)):
        fout.write(struct.pack("<B", 0))
    
    # finally close
    fout.close()

