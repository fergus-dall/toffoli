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
import re
import argparse
import pprint

arg = argparse.ArgumentParser(
    description = "An interpreter for the Toffoli esoteric language",
    )

arg.add_argument(
    'file-name',
    help = "filename of toffoli program to run",
    )

arg.add_argument(
    '--dump',
    action = 'store_true',
    help = "make DUMP commands print memory to stdout",
    )

arg = vars(arg.parse_args())
file_name = arg['file-name']
dump = arg['dump']

validate = re.compile(
    "\s*((TOFF|JMP|IN|OUT|DUMP)(\s+\d*#?\d+)*)?\s*(;.*)?"
    ,re.DOTALL)

memory = {}

def get_bit(bit):
    global memory
    if not memory.has_key(bit):
        memory[bit] = False
    return memory[bit]

def toffoli(in1,in2,in3,out):
    global memory
    if in1 and in2:
        memory[out] = not in3
    else:
        memory[out] = in3

def get_addr(addr):
    if addr[0] == '#':
        return int(addr[1:])
    else:
        pointer_len = int(addr[:addr.find('#')])
        pointer_loc = int(addr[addr.find('#')+1:])
        pointer_list = []
        for i in range(pointer_loc,pointer_loc+pointer_len):
            pointer_list.append(get_bit(i))
        pointer = bit_to_int(pointer_list)
        return pointer

def deref(addr):
    if addr.count('#') != 0:
        return get_bit(get_addr(addr))
    else:
        return int(addr)

def get_ch():
    ch = sys.stdin.read(1)
    return ch

def ch_to_bit(ch):
    ch = ord(ch)
    l = []
    for i in range(8):
        l.insert(0,ch%2 == 1)
        ch >>= 1
    return l

def bit_to_ch(l):
    ch = 0
    while len(l) != 0:
        ch <<= 1
        ch += l.pop(0)
    return chr(ch)

def bit_to_int(l):
    i = 0
    while len(l) != 0:
        i <<= 1
        i += l.pop(0)
    return i

def validate_line(str):
    result = validate.match(str)
    if result is not None:
        return str[:result.end()] == str
    else:
        return False

with open(file_name,'r') as file:
    lines = file.readlines()

for (index,i) in enumerate(lines):
    if not validate_line(i):
        print "Syntax error on line %s\n%s" %(index,i)
        sys.exit(1)

for (index,i) in enumerate(lines):
    if i.find(';') != -1:
        lines[index] = i[0:i.find(';')]
    lines[index] = lines[index].split()

while lines.count([]) != 0:
    lines.remove([])

instruction_pointer = 0
while instruction_pointer < len(lines):
    if lines[instruction_pointer][0] == 'TOFF':
        inputs = lines[instruction_pointer][1:]
        in1 = deref(inputs[0])
        in2 = deref(inputs[1])
        in3 = deref(inputs[2])
        out = int(inputs[3][1:])
        toffoli(in1,in2,in3,out)
        
    elif lines[instruction_pointer][0] == 'JMP':
        inputs = lines[instruction_pointer][1:]
        if deref(inputs[0]):
            instruction_pointer = int(inputs[1]) - 1

    elif lines[instruction_pointer][0] == 'IN':
        inputs = lines[instruction_pointer][1:]
        ch = get_ch()
        l = ch_to_bit(ch)
        addr = get_addr(inputs[0])
        for i in range(8):
            memory[addr + i] = l[i]
        
    elif lines[instruction_pointer][0] == 'OUT':
        inputs = lines[instruction_pointer][1:]
        l = []
        addr = get_addr(inputs[0])
        for i in range(8):
            l.append(get_bit(addr + i))
        ch = bit_to_ch(l)
        sys.stdout.write(ch)

    elif lines[instruction_pointer][0] == 'DUMP':
        if dump:
            pprint(memory)

    instruction_pointer += 1

print
