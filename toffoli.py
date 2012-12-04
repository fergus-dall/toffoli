import sys
import re

validate = re.compile("\s*((TOFF|JMP|IN|OUT)(\s+\d*#?\d+)+)?\s*(;.*)?",re.DOTALL)

memory = {}

def get_bit(bit):
    if not memory.has_key(bit):
        return False
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

with open(sys.argv[1],'r') as file:
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
        
    instruction_pointer += 1

print
