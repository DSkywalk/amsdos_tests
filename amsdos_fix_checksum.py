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

if sys.argv.__len__() != 3:
    print('Error: invalid args\nusage:', sys.argv[0], '<source-bas-path> <dest-bas-path>')
    exit(1)

current_file = sys.argv[1]
new_file = sys.argv[2]


with open(current_file, 'rb') as lr:
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

    
    # copy to new file
    fp2 = open(new_file,'wb')
    lr.seek(0, os.SEEK_SET)
    data = lr.read()
    fp2.write(data)
    fp2.close()
    
    # calc new checksum!
    fp2 = open(new_file,'rb')
    calc = 0
    for n in range(0, 66 + 1):
        byte_val = int.from_bytes(fp2.read(1), byteorder='little', signed=False)
        calc += byte_val
    print('new_checksum', calc, n, hex(calc))

    # update checksum
    fp2 = open(new_file,'r+b')
    fp2.seek(67, os.SEEK_SET)
    fp2.write(struct.pack("<H", calc))
    fp2.close()

