# Thunderbolt16
Thunderbolt16 is a 16-Bit non piplined RISC processor, which runs on a 32-bit Instruction set Architecture.
The design was simulated on Logisim-Evolution 4.0.1 & assembler programmed in python 2.7

![circuit diagram](tb16.jpg)

it supports 64KB of address space and Dedicate IO instructions.
ISA is provided in file "OP_excel.ods" file

TbAssembler is a two pass assembler that assembles 'code.txt' file into bytecode sequece (code_bytecode.txt) that can be loaded into RAM during Logisim simulation.

The command line syntax of Assembler is as follows:<br />
python assembler.py (filename).txt (debug flag) <br />
file name: it is of .txt format <br />
debug flag: '-d' : prints address mapping of all detected commands, labels, variables and output bytecode sequence.<br />
  

Assembly language reference & sample codes will be uploaded in upcoming commits.


