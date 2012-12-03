Toffoli
=============

Toffoli is a turing tarpit based on toffoli gates. It was created as a
pltgames submission.

To use the interpreter, call toffoli.py on the command line with your
code as input, eg:

`python toffoli.py hello_world.toff`

Memory
=============

Memory in Toffoli is an infinite array, starting at adress 0, of bits
that are initalised to 0.

Syntax
=============

Toffoli syntax is very simple, just the name of the instruction,
followed by the inputs, separated by spaces:

[instruction] [input1] [input2] [input3] ...

Each input can be either a number or a reference to a memory
address. Numbers are written literaly while memory addresses are
prefaced by a #, e.g.:

* 1 is the number 1
* #7 is a reference to memory address 7

Instructions
=============

Toffoli contains four instructions:

* TOFF
* JMP
* IN
* OUT

TOFF - toffoli gate
-------
Usage:

`TOFF [num/addr] [num/addr] [num/addr] [addr]`

A toffoli gate, or a controlled-controlled-NOT gate works as follows:

If the first two inputs are both 1, output the result of appling a NOT
gate to the third input

Otherwise, output the third input unchanged

The TOFF instruction applies a toffoli gate to the first three inputs
and stores the result in the address given as the fourth input.

JMP -- Conditional jump
-------
Usage:

`JMP [num/addr] [num]`

If the first input is not 0, or if the value stored at the bit refered
to by the first input is 1, then continue execution at the instruction
numbered by the second input. Instructions are numbered starting at 0.

IN -- input
-------
Usage:

`IN [addr]`

Take one character as input and store the corresponding byte in the 8
bits starting at `[addr]`.

OUT -- output
-------
Usage:

`OUT [addr]`

Interpret the 8 bits starting at `[addr]` as a character and output it.
