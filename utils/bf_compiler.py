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

point_len = int(sys.argv[1])

class bf_compile():
    def __init__(self,code):
        self.code = code
        self.len = len(code)
    def __call__(self,inst_count):
        self.inst_count = 0
        return []

class bf_mvright(bf_compile):
    def __init__(self):
        bf_compile.__init__(self,'>')
    def __call__(self,inst_count):
        inst_list = []

        for i in range(point_len,2*point_len):
            #set each value in the carry area to 0
            inst_list.append("TOFF 1 #%s #%s #%s" % (i,i,i))
            if i == 2*point_len - 4:
                #flip the fourth bit to add 8 to the pointer
                inst_list.append("TOFF 1 1 #%s #%s" % (i,i))
        
        for i in range(point_len - 1,0,-1):
            #if both the carry bit and the value are set, set the next carry bit
            inst_list.append(
                "TOFF #%s #%s #%s #%s" % (i, i+point_len,
                                            i+point_len - 1, i+point_len - 1))
            #if carry XOR value is true, set the value bit
            inst_list.append(
                "TOFF 1 #%s #%s #%s" % (i, i+point_len, i))
        #last bit doesn't set a carry bit
        inst_list.append("TOFF 1 #%s #%s #%s" % (0, point_len, 0))

        self.inst_count = len(inst_list)
        return inst_list

with open(sys.argv[2],'r') as file:
    file_string = file.read()

bf_code = ''
for i in file_string:
    if i in {'<','>','+','-','.',',','[',']'}:
        bf_code += i

bf_obj_list = []
inst_list = []

for i in bf_code:
    if i == '>':
        bf_obj_list.append(bf_mvright())

for i in bf_obj_list:
    inst_list += i(len(inst_list))

with open('out.toff','w') as file:
    for i in inst_list:
        file.write(i + '\n')
