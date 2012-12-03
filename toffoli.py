import sys
import termios
import tty

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

def deref(addr):
    if addr[0] == '#':
        return get_bit(int(addr[1:]))
    return int(addr)

def get_ch():
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setraw(sys.stdin.fileno(),termios.TCSADRAIN)
        ch = sys.stdin.read(1)
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
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

with open(sys.argv[1],'r') as file:
    lines = file.readlines()

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
        for i in range(8):
            memory[int(inputs[0][1:]) + i] = l[i]
        
    elif lines[instruction_pointer][0] == 'OUT':
        inputs = lines[instruction_pointer][1:]
        l = []
        for i in range(8):
            l.append(get_bit(int(inputs[0][1:]) + i))
        ch = bit_to_ch(l)
        sys.stdout.write(ch)
        
    instruction_pointer += 1

print
