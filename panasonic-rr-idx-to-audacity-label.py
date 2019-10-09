#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''
   Copyright (C) 2019-2019 Leonardo Silva Amaral

   panasonic-rr-idx-to-audacity-label is free software: you can redistribute it and/or modify
   it under the terms of the GNU General Public License as published by
   the Free Software Foundation, version 3 of the License.

   panasonic-rr-idx-to-audacity-label is distributed in the hope that it will be useful,
   but WITHOUT ANY WARRANTY; without even the implied warranty of
   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
   GNU General Public License for more details.
'''

import sys
import os

def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)

if len(sys.argv) >= 2:
    filepath = sys.argv[1]
else:
    print("No parameter has been included")
    sys.exit(1)

if not os.path.exists(filepath):
    eprint("File", filepath, "not found!")
    sys.exit(1)

with open(filepath, "rb") as index_file:
    indexes = []
    after = []
    sizeOfIdx = 4
    index_file.seek(0, 0)
    header=str(index_file.read(16),'ISO-8859-1')
    newFileName=os.path.dirname(os.path.realpath(filepath)) + '/' + os.path.splitext(os.path.basename(filepath))[0]+".txt"
    
    if not header == 'INDEX_ICRECORDER':
        eprint("File is not a Panasonic Index!\n\t * Please search for .IDX files into MIC_* or LINE_* folder.")
        sys.exit(2)

    index_file.seek(16, 1)

    numberOfIndexes = int.from_bytes(index_file.read(1), byteorder="little")
    for index in range(0, numberOfIndexes):
        index_file.seek(48 + (sizeOfIdx*index), 0)

        if int.from_bytes(index_file.read(1), byteorder="little") == 224:
            after.append('[PostRecord]')
        else:
            after.append('[AtRecord]')

        ''' Not necessary, just for doc
        index_file.seek(0,1)'''

        sec = int.from_bytes(index_file.read(sizeOfIdx), byteorder="little")/100.00000
        indexes.append(sec)

with open(newFileName, "w+") as result:
    for idx,time in enumerate(indexes):
        print(f'{time}\t{time}\t{after[idx]} INDEX {idx}', file=result)

print("File", newFileName, 'was created!')
