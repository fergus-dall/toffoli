#########################################################################
# This program is Copyright (C) 2012 Fergus Dall                        #
#                                                                       #
# This program is free software: you can redistribute it and/or modify  #
# it under the terms of the GNU General Public License as published by  #
# the Free Software Foundation, either version 3 of the License, or     #
# (at your option) any later version.                                   #
#                                                                       #
# This program is distributed in the hope that it will be useful,       #
# but WITHOUT ANY WARRANTY; without even the implied warranty of        #
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the         #
# GNU General Public License for more details.                          #
#                                                                       #
# You should have received a copy of the GNU General Public License     #
# along with this program.  If not, see <http://www.gnu.org/licenses/>. #
#########################################################################

import sys
import argparse

arg = argparse.ArgumentParser(
    description = "A brainfuck to Toffoli compiler",
    )

arg.add_argument(
    'file-name',
    help = 'filename to be compiled'
    )

arg.add_argument(
    '--pointer-len',
    help = 'length of the cell pointer to be used in bits (default 32)',
    default = 32,
    type = int,
    )

arg.add_argument(
    '--dump',
    help = 'add DUMP commands to resultant code',
    action = 'store_true',
    )

arg = vars(arg.parse_args())
file_name = arg['file-name']
pointer_len = arg['pointer_len']
carry_start = pointer_len * 8
carry_end = carry_start + max(8,pointer_len)
dump = arg['dump']

def bf_mvright():
    inst_list = []
    for i in range(8):
        for j in range(carry_start,carry_start + pointer_len):
            #set each value in the carry area to 0
            inst_list.append("TOFF 1 #%s #%s #%s" % (j,j,j))
            if j == carry_start + pointer_len - 4:
                #flip the fourth bit to add 8 to the pointer
                inst_list.append("TOFF 1 1 #%s #%s" % (j,j))

        for j in range((i+1)*pointer_len - 1,i*pointer_len,-1):
            #if both the carry bit and the value are set, set the
            #next carry bit
            inst_list.append(
                "TOFF #%s #%s #%s #%s" % (j, j + pointer_len*(8-i),
                                          j + pointer_len*(8-i) - 1,
                                          j + pointer_len*(8-i) - 1))
            #if carry XOR value is true, set the value bit
            inst_list.append(
                "TOFF 1 #%s #%s #%s" % (j, j + pointer_len*(8-i), j))
        #last bit doesn't set a carry bit
        inst_list.append("TOFF 1 #%s #%s #%s" % (i*pointer_len,
                                                 carry_start,
                                                 i*pointer_len))

    if dump:
        inst_list.append("DUMP")

    return inst_list

def bf_mvleft():
    inst_list = []
    for i in range(8):
        for j in range(carry_start,carry_start + pointer_len):
            #set each value in the carry area to 0
            inst_list.append("TOFF 1 #%s #%s #%s" % (j,j,j))
            if j == carry_start + pointer_len - 4:
                #flip the fourth bit to add 8 to the pointer
                inst_list.append("TOFF 1 1 #%s #%s" % (j,j))

        for j in range((i+1)*pointer_len - 1,i*pointer_len,-1):
            #if the carry bit is set and the value is not, set the
            #next carry bit
            inst_list.append("TOFF 1 1 #%s #%s" % (j,j))
            inst_list.append(
                "TOFF #%s #%s #%s #%s" % (j, j + pointer_len*(8-i),
                                          j + pointer_len*(8-i) - 1,
                                          j + pointer_len*(8-i) - 1))
            inst_list.append("TOFF 1 1 #%s #%s" % (j,j))
            #if carry XOR value is true, set the value bit
            inst_list.append(
                "TOFF 1 #%s #%s #%s" % (j, j + pointer_len*(8-i), j))
        #last bit doesn't set a carry bit
        inst_list.append("TOFF 1 #%s #%s #%s" % (i*pointer_len,
                                                 carry_start,
                                                 i*pointer_len))

    if dump:
        inst_list.append("DUMP")

    return inst_list

def bf_plus():
    inst_list = []
    for j in range(carry_start,carry_start + 8):
        #set each value in the carry area to 0
        inst_list.append("TOFF 1 #%s #%s #%s" % (j,j,j))
        if j == carry_start + 7:
            #flip the first bit to add 1 to the cell
            inst_list.append("TOFF 1 1 #%s #%s" % (j,j))
    for j in range(7,0,-1):
        #if both the carry bit and the value are set, set the
        #next carry bit
        inst_list.append(
            "TOFF #%s %s#%s #%s #%s" % (j + carry_start,
                                        pointer_len, j*pointer_len,
                                        j + carry_start - 1,
                                        j + carry_start - 1))
        #if carry XOR value is true, set the value bit
        inst_list.append(
            "TOFF 1 #%s %s#%s %s#%s" % (j + carry_start,
                                        pointer_len, j*pointer_len,
                                        pointer_len, j*pointer_len))
    #last bit doesn't set a carry bit
    inst_list.append("TOFF 1 %s#0 #%s %s#0" % (pointer_len,
                                               carry_start,
                                               pointer_len))

    if dump:
        inst_list.append("DUMP")
    
    return inst_list

def bf_minus():
    inst_list = []
    for j in range(carry_start,carry_start + 8):
        #set each value in the carry area to 0
        inst_list.append("TOFF 1 #%s #%s #%s" % (j,j,j))
        if j == carry_start + 7:
            #flip the first bit to add 1 to the cell
            inst_list.append("TOFF 1 1 #%s #%s" % (j,j))
    for j in range(7,0,-1):
        #if both the carry bit is set and the value is not, set the
        #next carry bit
        inst_list.append(
            "TOFF 1 1 %s#%s %s#%s" % (pointer_len, j*pointer_len,
                                      pointer_len, j*pointer_len))
        inst_list.append(
            "TOFF #%s %s#%s #%s #%s" % (j + carry_start,
                                        pointer_len, j*pointer_len,
                                        j + carry_start - 1,
                                        j + carry_start - 1))
        inst_list.append(
            "TOFF 1 1 %s#%s %s#%s" % (pointer_len, j*pointer_len,
                                      pointer_len, j*pointer_len))
        #if carry XOR value is true, set the value bit
        inst_list.append(
            "TOFF 1 #%s %s#%s %s#%s" % (j + carry_start,
                                        pointer_len, j*pointer_len,
                                        pointer_len, j*pointer_len))
    #last bit doesn't set a carry bit
    inst_list.append("TOFF 1 %s#0 #%s %s#0" % (pointer_len,
                                               carry_start,
                                               pointer_len))

    if dump:
        inst_list.append("DUMP")
    
    return inst_list

def bf_input():
    inst_list = []

    inst_list.append("IN %s#0" % (pointer_len,))

    if dump:
        inst_list.append("DUMP")

    return inst_list

def bf_output():
    inst_list = []

    inst_list.append("OUT %s#0" % (pointer_len,))

    if dump:
        inst_list.append("DUMP")

    return inst_list

def bf_loop(code,inst_count):
    count = 1
    read = 1
    while count > 0:
        if code[read] == '[':
            count += 1
        elif code[read] == ']':
            count -= 1
        read += 1

    header_end = inst_count + 9
    inst_count = header_end

    inst_list = parse(code[1:read-1],header_end)
    inst_count += len(inst_list)

    footer_end = inst_count + 8

    header = []
    for i in range(8):
        header.append("JMP %s#%s %s" % (pointer_len,i*pointer_len,
                                            header_end))
    header.append("JMP 1 %s" % (footer_end,))

    footer = []
    for i in range(8):
        footer.append("JMP %s#%s %s" % (pointer_len,i*pointer_len,
                                            header_end))

    inst_list = header + inst_list + footer
    return (inst_list,read)

def parse(code,inst_count = 0):
    inst_list = []
    i = 0

    while i < len(code):
        if code[i] == '>':
            inst_list += bf_mvright()
        elif code[i] == '<':
            inst_list += bf_mvleft()
        elif code[i] == '+':
            inst_list += bf_plus()
        elif code[i] == '-':
            inst_list += bf_minus()
        elif code[i] == ',':
            inst_list += bf_input()
        elif code[i] == '.':
            inst_list += bf_output()
        elif code[i] == '[':
            loop_inst,read = bf_loop(code[i:],inst_count + len(inst_list))
            i += read - 1
            inst_list += loop_inst
        elif code[i] == ']':
            print "error, unmached ']'"
            raise ValueError
        else:
            print "error, unrecognised symbol %s" % (code[i],)
            raise ValueError
        i += 1
    return inst_list

with open(file_name,'r') as file:
    file_string = file.read()

bf_code = ''
for i in file_string:
    if i in {'<','>','+','-','.',',','[',']'}:
        bf_code += i

# Move cell pointer past the end of the carry area so we don't
# overwrite something
bf_code = (carry_end/8 + 1) * '>' + bf_code

inst_list = []

for i in range(8):
    inst_list.append("TOFF 1 %s #%s #%s" % (i & 1<<2,
                                            (i+1) * pointer_len - 3,
                                            (i+1) * pointer_len - 3))
    inst_list.append("TOFF 1 %s #%s #%s" % (i & 1<<1,
                                            (i+1) * pointer_len - 2,
                                            (i+1) * pointer_len - 2))
    inst_list.append("TOFF 1 %s #%s #%s" % (i & 1<<0,
                                            (i+1) * pointer_len - 1,
                                            (i+1) * pointer_len - 1))

if dump:
    inst_list.append("DUMP")

inst_list += parse(bf_code,len(inst_list))

with open('out.toff','w') as file:
    for i in inst_list:
        file.write(i + '\n')
