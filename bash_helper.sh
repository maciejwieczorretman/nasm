#!/bin/bash
# $1 instruction to assemble / xed hex code to read
# $2 nasm string if the xed instruction disassembling is desired
# $3 bits mode to set for the instruction
# $4 additional flags to pass

bits_ARRAY=($3)
BITS=${bits_ARRAY[1]}
if [[ $2 == "nasm" ]]; then
	COMMAND="intel-xed -$BITS $4 -d $1"
	($COMMAND)
else
	echo $3 > /tmp/nasm_input.asm
	echo $1 >> /tmp/nasm_input.asm
	~/Code/nasm/nasm -f elf -w-prefix-opsize -w-implicit-abs-deprecated /tmp/nasm_input.asm -l /tmp/nasm_output.lst
fi
