#!/usr/bin/python3

import subprocess
import os
import re

DEBUG=0

operand_dictionary = {
	'bndreg' : "bnd0",
	'fpu0' : "st0",
	'fpureg' : "st1",
	'fpureg|to' : "st1",
	'ignore' : "",
	'imm' : "0x19",
	'imm16' : "word 0xFFFF",
	'imm16:imm16' : "0x1000:0xF000",
	'imm16:imm16|far' : "0x1000:0xF000",
	'imm16:imm32' : "0x1000:0xF0000000",
	'imm16:imm32|far' : "0x1000:0xF0000000",
	'imm16|short' : "0x10",
	'imm16|abs' : "0xFFFF",
	'imm16|far' : "0x7000",
	'imm16|near' : "0x10",
	'imm16|near|short' : "0x10",
	'imm32' : "dword 0x70000000",
	'imm32:imm32' : "0x10000000:0xF0000000",
	'imm32:imm32|far' : "dword 0x10000000:0x10000000",
	'imm32|abs' : "abs dword 0x70000000",
	'imm32|far' : "dword 0x10000000",
	'imm32|near' : "dword 0x10",
	'imm32|near|short' : "0x10",
	'imm32|short' : "0x10",
	'imm64' : "qword 0xF0000000F0000000",
	'imm64|abs' : "abs qword 0xF0000000F0000000",
	'imm64|near' : "qword 0x10",
	'imm64|near|short' : "0x10",
	'imm64|abs|near' : "abs qword 0x00000000F0000000",
	'imm64|short' : "0x10",
	'imm8' : "byte 0xF0",
	'imm8|abs' : "abs byte 0xFF",
	'imm8|near|short' : "0x10",
	'imm8|short' : "0x10",
	'imm:imm' : "0x10:0x10",
	'imm_known8' : "byte 0x10",
	'imm|near' : "0x10",
	'kreg' : "k0",
	'kreg16' : "k0",
	'kreg16*' : "k0",
	'kreg32' : "k0",
	'kreg32*' : "k0",
	'kreg64' : "k0",
	'kreg64*' : "k0",
	'kreg8' : "k0",
	'kreg8*' : "k0",
	'kreg|mask' : "k0{k1}",
	'kreg|rs2' : "k0",
	'krm16' : "word [RBX]",
	'krm32' : "dword [RBX]",
	'krm64' : "qword [RBX]",
	'krm8' : "byte [RBX]",
	'mem' : "[RBX]",
	'mem128' : "oword [RBX]",
	'mem128|mask' : "oword [RBX]{k1}",
	'mem16' : "word [RBX]",
	'mem16|far' : "word [RBX]",
	'mem16|mask' : "word [RBX]{k1}",
	'mem256' : "yword [RBX]",
	'mem256|mask' : "yword [RBX]{k1}",
	'mem32' : "dword [RBX]",
	'mem32|far' : "dword [RBX]",
	'mem32|mask' : "dword [RBX]{k1}",
	'mem512' : "[RBX]",
	'mem512|mask' : "[RBX]{k1}",
	'mem64' : "qword [RBX]",
	'mem64|far' : "qword [RBX]",
	'mem64|mask' : "qword [RBX]{k1}",
	'mem8' : "byte [RBX]",
	'mem80' : "[RBX]",
	'mem_offs' : "gs:[0x10]",
	'mmxreg' : "mm0",
	'mmxrm' : "[RBX]",
	'mmxrm64' : "[RBX]",
	'reg16' : "CX",
	'reg16?' : "CX",
	'reg32' : "ECX",
	'reg32*' : "ECX",
	'reg32?' : "ECX",
	'reg32na' : "ECX",
	'reg64' : "RCX",
	'reg64*' : "RCX",
	'reg64:reg64' : "RCX:RAX",
	'reg64?' : "RCX",
	'reg8' : "AL",
	'reg8?' : "AH",
	'reg_al' : "AL",
	'reg_ax' : "AX",
	'reg_bx' : "BX",
	'reg_cl' : "CL",
	'reg_creg' : "CR0", #control register
	'reg_cs' : "CS",
	'reg_cx' : "CX",
	'reg_dreg' : "DR0", #debug register
	'reg_ds' : "DS",
	'reg_dx' : "DX",
	'reg_eax' : "EAX",
	'reg_ecx' : "ECX",
	'reg_edx' : "EDX",
	'reg_es' : "ES",
	'reg_fs' : "FS",
	'reg_gs' : "GS",
	'reg_rax' : "RAX",
	'reg_rcx' : "RCX",
	'reg_sreg' : "FS",
	'reg_ss' : "SS",
	'reg_treg' : "TR0",
	'rm16' : "word [RBX]",
	'rm16*' : "word [RBX]",
	'rm16|near' : "word [RBX]",
	'rm32' : "dword [RBX]",
	'rm32*' : "dword [RBX]",
	'rm32|er' : "dword [RBX]",
	'rm32|near' : "dword [RBX]",
	'rm64' : "qword [RBX]",
	'rm64*' : "qword [RBX]",
	'rm64|er' : "qword [RBX]",
	'rm64|near' : "qword [RBX]",
	'rm8' : "byte [RBX]",
	'rm_sel' : "[RBX]",
	'sbytedword32' : "dword 0x05",
	'sbytedword64' : "qword 0x05",
	'sbyteword16' : "word 0x05",
	'sdword64' : "0x70000000",
	'sdword64|near' : "0x00000010",
	'spec4' : "",
	'tmmreg' : "tmm0",
	'udword64' : "dword 0xF0000000",
	'unity' : "0x1",
	'void' : " ",
	'xmem32' : "[xmm0]",
	'xmem32|mask' : "[xmm0]{k1}",
	'xmem64' : "[xmm0]",
	'xmem64|mask' : "[xmm0]{k1}",
	'xmm0' : "xmm0",
	'xmmreg' : "xmm0",
	'xmmreg*' : "xmm0",
	'xmmreg|er' : "xmm0",
	'xmmreg|mask' : "xmm0{k1}",
	'xmmreg|mask|z' : "xmm0{k1}{z}",
	'xmmreg|rs4' : "xmm0+3",
	'xmmrm' : "[RBX]",
	'xmmrm128' : "oword [RBX]",
	'xmmrm128*' : "oword [RBX]",
	'xmmrm128|b16' : "oword [RBX]",
	'xmmrm128|b16|er' : "oword [RBX]",
	'xmmrm128|b16|sae' : "oword [RBX]",
	'xmmrm128|b32' : "oword [RBX]",
	'xmmrm128|b32*' : "oword [RBX]",
	'xmmrm128|b64' : "oword [RBX]",
	'xmmrm128|b64*' : "oword [RBX]",
	'xmmrm128|mask|z' : "oword [RBX]{k1}{z}",
	'xmmrm16' : "word [RBX]",
	'xmmrm16|er' : "word [RBX]",
	'xmmrm16|sae' : "xmm0",
	'xmmrm256|b16' : "yword [RBX]",
	'xmmrm32' : "dword [RBX]",
	'xmmrm32*' : "dword [RBX]",
	'xmmrm32|b16' : "dword [RBX]",
	'xmmrm32|er' : "dword [RBX]",
	'xmmrm32|sae' : "dword [RBX]",
	'xmmrm64' : "qword [RBX]",
	'xmmrm64*' : "qword [RBX]",
	'xmmrm64|b16' : "qword [RBX]",
	'xmmrm64|b32' : "qword [RBX]",
	'xmmrm64|er' : "qword [RBX]",
	'xmmrm64|sae' : "qword [RBX]",
	'xmmrm8' : "byte [RBX]",
	'ymem32' : "[ymm0]",
	'ymem32|mask' : "[ymm0]{k1}",
	'ymem64' : "[ymm0]",
	'ymem64|mask' : "[ymm0]{k1}",
	'ymmreg' : "ymm0",
	'ymmreg*' : "ymm0",
	'ymmreg|mask' : "ymm0{k1}",
	'ymmreg|mask|z' : "ymm0{k1}{z}",
	'ymmrm128|b32' : "oword [RBX]",
	'ymmrm256' : "yword [RBX]",
	'ymmrm256*' : "yword [RBX]",
	'ymmrm256|b16' : "yword [RBX]",
	'ymmrm256|b16|er' : "yword [RBX]",
	'ymmrm256|b16|sae' : "yword [RBX]",
	'ymmrm256|b32' : "yword [RBX]",
	'ymmrm256|b32*' : "yword [RBX]",
	'ymmrm256|b32|er' : "yword [RBX]",
	'ymmrm256|b32|sae' : "yword [RBX]",
	'ymmrm256|b64' : "yword [RBX]",
	'ymmrm256|b64*' : "yword [RBX]",
	'ymmrm256|mask|z' : "yword [RBX]",
	'ymmrm256|sae' : "yword [RBX]",
	'zmem32' : "[zmm0]",
	'zmem32|mask' : "[zmm0]{k1}",
	'zmem64' : "[zmm0]",
	'zmem64|mask' : "[zmm0]{k1}",
	'zmmreg' : "zmm0",
	'zmmreg*' : "zmm0",
	'zmmreg|mask' : "zmm0{k1}",
	'zmmreg|mask|z' : "zmm0{k1}{z}",
	'zmmreg|rs4' : "zmm0+3",
	'zmmreg|sae' : "zmm0",
	'zmmrm128|b32' : "oword [RBX]",
	'zmmrm512' : "zword [RBX]",
	'zmmrm512*' : "zword [RBX]",
	'zmmrm512|b16' : "zword [RBX]",
	'zmmrm512|b16|er' : "zword [RBX]",
	'zmmrm512|b16|sae' : "zword [RBX]",
	'zmmrm512|b32' : "zword [RBX]",
	'zmmrm512|b32*' : "zword [RBX]",
	'zmmrm512|b32|er' : "zword [RBX]",
	'zmmrm512|b32|sae' : "zword [RBX]",
	'zmmrm512|b64' : "zword [RBX]",
	'zmmrm512|b64*' : "zword [RBX]",
	'zmmrm512|b64|er' : "zword [RBX]",
	'zmmrm512|b64|sae' : "zword [RBX]",
	'zmmrm512|mask|z' : "zword [RBX]{k1}{z}"
}

skip_mnemonics = [
	"JMPE", # obsolete
	"RETW", # gives normally non-existent encoding
	"RETFW",
	"RETNW",
	"IRETW",
	"PUSHFW",
	"POPFW",
	"RETF", # xed version doesn't simply assemble
	"RETFD",
	"RETFQ",
	"CMPSB", # the following string ops don't have the base form and error out
	"CMPSW", # because of that
	"CMPSD",
	"CMPSQ",
	"LODSB",
	"LODSW",
	"LODSD",
	"LODSQ",
	"MOVSB",
	"MOVSW",
	"MOVSD",
	"MOVSQ",
	"STOSB",
	"STOSW",
	"STOSD",
	"STOSQ",
	"SCASB",
	"SCASW",
	"SCASD",
	"SCASQ",
	"INSB",
	"INSW",
	"INSD",
	"OUTSB",
	"OUTSW",
	"OUTSD",
	"WBNOINVD", # skip because XED doesn't have this one
	"LDS", # skip because XED decoded it incorrectly
	"LES", # skip because XED decoded it incorrectly
	"LFS", # skip because XED decoded it incorrectly
	"LGS", # skip because XED decoded it incorrectly
	"LSS", # skip because XED decoded it incorrectly
	"LGDT", # XED doesnt' differentiate between 16 and 32 bit versions
	"LIDT", # XED doesnt' differentiate between 16 and 32 bit versions
	"SGDT", # XED doesnt' differentiate between 16 and 32 bit versions
	"SIDT", # XED doesnt' differentiate between 16 and 32 bit versions
	"FCLEX", # XED has FNCLEX encoding flipped with FCLEX
	"FINIT",
	"FNDISI", # these four are not documented and are unsupported
	"FDISI",
	"FNENI",
	"FENI",
	"FNSAVE", # these two are flipped in XED
	"FSAVE",
	"FSTCW", # these two are flipped in XED
	"FNSTCW",
	"FSTENV", # these two are flipped in XED
	"FNSTENV",
	"FSTSW", # these two are flipped in XED
	"FNSTSW",
	"PAVEB", # discontinued, XED doesn't recognize the encoding
	"PMULHRWA", # NASM splits PMULHRW into A and C variants so
	"PMULHRWC", # it doesn't re-assemble well after XED decodes it
	"ENTER", # XED decodes the sizes wrong (imm16,imm16)
	"ENTERW",
	"ENTERD",
	"ENTERQ",
	"UD0", # XED removes all prefixes
	"UD1",
	"UD2A",
	"UD2B",
	"UD2",
	"UDB", # This one is only present in NASM
	"CCMPscc", # scc operator not implemented yet TODO
	"CTESTscc",
	"CMOVcc",
	"CFCMOVcc",
	"SETcc",
	"SETccZU",
	"CMPccXADD",
	"MOVMSKPS", # XED doesn't decode the 64 bit version correctly
	"PREFETCHIT0",
	"PREFETCHIT1",
	"MOVMSKPD", # XED can't decode 64 bit version correctly
	"VMLOAD", # XED wants to put RAX there but NASM doesn't
	"VMRUN",
	"PVALIDATE",
	"RMPADJUST",
	"VMGEXIT", # It is interpreted as VMMCALL if not in the guest
	"EXTRACTPS", # XED can't decode 64 bit version correctly
	"PFRCPV", # XED doesn't recognize it
	"PFRSQRTV",
	"VEXTRACTPS", # XED decodes EVEX form into the VEX form TODO:pass different XED parameter?
	"VMOVDQA32", # XED general error - maybe it's not implemented there?
	"VMOVDQA64",
	"VMOVDQU8",
	"VMOVDQU16",
	"VMOVDQU32",
	"VMOVDQU64",
	"VPEXTRB", # XED decodes EVEX form into the VEX form TODO:pass different XED parameter?
	"VPEXTRW", # XED decodes EVEX form into the VEX form TODO:pass different XED parameter?
	"CLDEMOTE", # XED decodes it into NOP TODO:pass different XED parameter?
	"PREFETCHRST2", # XED decodes it into NOP
	"VMOVW",
	"NOP", # XED doesn't disassemble the NOPs at the end in a way that NASM can handle
]

specific_skips = [
	"movd mm0, qword [rbx]", # it assembles to 480F6E02 but disassembles to 0F6F02
	"movd qword [rbx], mm0", # it assembles to 480F7E02 but disassembles to 0F7F02
]

lose_suffix = [
]

suffix_size_dictionary = {
	'addr16' : 'w',
	'data16' : 'w',
	'addr32' : 'd',
	'data32' : 'd'
}

regex_fixes = {
		# r'[dq](\[.*?\])' : r'\1',
		# r'[dq](.s:)(\[.*?\])' : r'\1\2',
		# r'(:)\[(.*?)\]' : r'\1\2',
		r'xmmword' : r'oword',
		r'ymmword' : r'yword',
		r'zmmword' : r'zword',
		r'data16 nop' : r'nop2',
		r'8087_nop' : r'',
		r'287_nop' : r'',
		r', k1' : r'{k1}',
		r'tileloas' : r'tileloaddrs' # Seems like XED made up a mnemonic?
}

output_saved = []
saved_flags = []
long = ''


# Take an instruction encoding and try to flip the modrm and modreg bit field in
# the last byte. Especially useful with alias instructions that can be disassembled
# with operand in a different order (for example BSWAP reg_ax -> XCHG reg8,rm8)
def flip_modrm_modreg(encoding):
	ret_encoding = encoding
	modrm_nasm = bin(int(ret_encoding[-2:], 16))
	modrm_mode = modrm_nasm[2:4]
	modrm_reg = modrm_nasm[4:7]
	modrm_rm = modrm_nasm[7:10]
	alternate_modrm = "0b" + modrm_mode + modrm_rm + modrm_reg
	alternate_modrm = hex(int(alternate_modrm, 2)).upper()[-2:]
	# print(modrm_nasm, modrm_mode, modrm_reg, modrm_rm)
	# print(alternate_modrm, encoding[-2:])
	ret_encoding = encoding
	ret_encoding = ret_encoding[:-2] + alternate_modrm
	# print(ret_encoding)
	return ret_encoding

def flip_imm(encoding):
	hex_addr = encoding[encoding.find("(")+1:encoding.find(")")]
	# print("Addr in parentheses : ", hex_addr)
	original_len = len(hex_addr)
	instruction_len = int((len(encoding) - 2)/2)
	split_addr = [hex_addr[i:i+2] for i in range (0, len(hex_addr), 2)]
	# print(split_addr, instruction_len)
	reversed_addr = ""
	for byte in reversed(split_addr):
		reversed_addr += byte
	xed_addr = format(int(reversed_addr, 16) - instruction_len, f'0{original_len}x')
	split_addr = [xed_addr[i:i+2] for i in range (0, len(xed_addr), 2)]
	# print(split_addr)
	reversed_addr = ""
	for byte in reversed(split_addr):
		reversed_addr += byte
	# print(reversed_addr.upper())
	# print(re.sub(r"\(.*\)", reversed_addr.upper(), encoding))
	final_encoding = re.sub(r"\(.*\)", reversed_addr.upper(), encoding)
	return final_encoding


def listing_to_encoding(instruction, stderr, line):
	encoding = []
	try:
		with open('/tmp/nasm_output.lst', 'r') as nasm_file:
			lines = nasm_file.readlines()
			for output_line in lines[1:]:
				# parse out the hex code
				encoding.append(output_line.split()[2].replace('-', ''))
			encoding = ''.join(encoding)
			# print(nasm_encoding)
	except:
		print("Error! No NASM output found! : ", instruction)
		print("Instruction flags : ", saved_flags, ", ", long)
		print("XDA file line : ", line)
		# return -1
	return encoding

def xed_format_to_nasm(decoded_instruction, starting_instruction):
	instruction = decoded_instruction
	# print("EXCEPTION: ", starting_instruction, decoded_instruction)
	if (('abs qword' in starting_instruction) and ('qword ptr' in decoded_instruction)):
		# print("EXCEPTION: ", starting_instruction, decoded_instruction)
		instruction = decoded_instruction.replace("qword ptr [", "[abs qword ")
		# print(instruction)

	# find lea instruction and correct the "ptr [offset]" syntax into "<size> <imm>"
	if ('lea ' in starting_instruction) and ('ptr' in decoded_instruction):
		match = re.findall(r', ptr \[0x.*', instruction)
		if (len(match) > 0):
			match2 = re.findall(r', [\w]+[\s]?[\w]+ 0x.*', starting_instruction)
			if (len(match2) > 0):
				instruction = instruction.replace(match[0], match2[0])
				# print(starting_instruction)
				# print(decoded_instruction, ' -> ', instruction)

	# remove any left 'ptr' keywords from the xed
	instruction = instruction.replace('ptr ', '')

	if 'far' in instruction:
		# print(instruction)
		match = re.findall(r'0x[a-f+0-9]+', instruction)
		if len(match) == 2:
			addr_seg = f"{match[1]}:{match[0]}"
			instruction = instruction.replace('far ', '')
			instruction = instruction.replace(',', '')
			instruction = instruction.replace(f"{match[0]} {match[1]}", addr_seg)
		# print(instruction)
		return instruction

	if 'st' in instruction:
		instruction = re.sub(r'st$', 'st0', instruction)
		instruction = re.sub(r'st,', 'st0,', instruction)
	if 'st(1)' in instruction:
		instruction = instruction.replace('st(1)', 'st1')
	if 'st(0)' in instruction:
		instruction = instruction.replace('st(0)', 'st0')

	if 'NO_EXPLICIT_FPU_ST' in saved_flags:
		instruction = re.sub(r'st0$', '', instruction)
		instruction = re.sub(r'st0,', '', instruction)

	# print(instruction)

	return instruction

DEBUG_LINE = 0

def main():
	with open('x86/insns.xda', 'r') as file:
		line_counter = 0
		fail_counter = 0
		skip_counter = 0

		for line in file:
			if line_counter < DEBUG_LINE:
				line_counter+=1
				skip_counter+=1
				continue
			global saved_flags
			global long
			saved_flags = []
			long = 'BITS 32'
			# ditch comments
			if line.strip().startswith(";") or line == "\n":
				continue
			else:
				# ditch last column
				line_parsed = line.strip().split('[')[0].split()
				flags = line.strip().split(']')
				# print(line_parsed, flags)

				# breakup line into instruction + operands
				mnemonic = line_parsed[0]
				operands = line_parsed[1].split(',')

				# save instruction flags to check exceptions
				if (len(flags) > 1):
					saved_flags = flags[1].split(',')
					if (saved_flags):
						saved_flags[0] = saved_flags[0].strip()

				# print(saved_flags)
				if 'LONG' in saved_flags or ('FUTURE' in saved_flags and 'NOLONG' not in saved_flags):
					long = 'BITS 64'

				# skip stuff from the first lines
				if 'PSEUDO' in saved_flags or 'OBSOLETE' in saved_flags or 'CLZERO' in saved_flags:
					line_counter+=1
					skip_counter+=1
					continue

				# skip hacky stuff because xed doesn't want to assemble this properly
				if 'SX' in saved_flags:
					line_counter+=1
					skip_counter+=1
					continue

				if ('ignore' in operands or mnemonic.lower() == "equ"):
					line_counter+=1
					skip_counter+=1
					continue

				# This is TODO
				# these can be resolved with data16 etc -> -w suffix added to the mnemonic
				if "Jcc" in mnemonic:
					line_counter+=1
					skip_counter+=1
					continue
				# if "LOOP" in mnemonic or "RET" in mnemonic:
				# 	line_counter+=1
				# 	skip_counter+=1
				# 	continue

				# Hint NOPs are at the end and there is no point checking them here
				if mnemonic == "HINT_NOP":
					print(f"Checked {round((line_counter/7133) * 100, 2)}% instructions ({line_counter} / 7133)...")
					return

				# skip test if mnemonic is on the skip list
				if mnemonic in skip_mnemonics:
					line_counter+=1
					skip_counter+=1
					continue

				if ('FPU' in saved_flags) and ('fpureg' not in operands) and ('fpu0' not in operands):
					saved_flags.append("NO_EXPLICIT_FPU_ST")

				if ('FPU' in saved_flags) and (('fpureg' in operands) ^ ('fpu0' in operands)):
					saved_flags.append("NO_EXPLICIT_FPU_ST")

			# for now only check MOV, later we'll do more
			# if mnemonic != None:

			# if mnemonic != "JCXZ":
			# 	continue

			new_operands = []
			operands_len = 0
			for operand in operands:

				# swap template operands for actual ones stored in the
				# operand dictionary
				swapped_operand = ""
				try:
					if operand_dictionary[operand] == None: #make special value for operands not in the array
						pass
				except:
					line_counter+=1
					skip_counter+=1
					continue
				if operand_dictionary[operand] == "": #make special value for operands not in the array
					swapped_operand = f"N({operand})"
				# fixup the register addressing for 32 bits
				elif long == 'BITS 32':
					swapped_operand = operand_dictionary[operand]
					# If 16-bit addressing is specifically requested BX needs to be used as
					# the memory addressing register.
					if " a16 " in line:
						swapped_operand = swapped_operand.replace('[RBX]', '[BX]')
					else:
						swapped_operand = swapped_operand.replace('[RBX]', '[EBX]')
				else: # just get the actual operand from the array
					swapped_operand = operand_dictionary[operand]

				# By default in 64 bit mode the RBX is used to address memory. When a32 is
				# directly specified it needs to be overriden into EBX.
				if " a32 " in line:
					swapped_operand = swapped_operand.replace('[RBX]', '[EBX]')

				# now we can work on the operand for special cases
				if operand == "mem_offs" and "reg_rax" in operands:
					swapped_operand = "[abs qword 0x10]"
				new_operands.append(swapped_operand)

			operands_len = len(new_operands)

			if "APX" in saved_flags:
				if operands_len > 1 and new_operands[0] is new_operands[1]:
					new_operands[1] = new_operands[1].replace('C', 'A')

			for flag in saved_flags:
				if "AVX" in flag or "AMX" in flag:
					if operands_len > 1 and ('mm0' in new_operands[1]):
						new_operands[1] = new_operands[1].replace('0', '1')
					if operands_len > 2 and ('mm0' in new_operands[2]):
						new_operands[2] = new_operands[2].replace('0', '2')
					break

			# patch starting instruction before stitching it together into a string
			if "NF_R" in saved_flags:
				mnemonic = mnemonic + " {nf}"

			starting_instruction = mnemonic.lower(), ', '.join(new_operands).lower()
			starting_instruction = ' '.join(starting_instruction)

			# set of specific entries that doesn't assemble well with XED
			if starting_instruction in specific_skips:
				line_counter+=1
				skip_counter+=1
				continue

			# print(starting_instruction)

			# write out instruction to a file and assemble it with nasm
			result = subprocess.run(['./bash_helper.sh', f'{starting_instruction}', '', long], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

			# get the nasm_encoding from the listing file
			nasm_encoding = listing_to_encoding(starting_instruction, result.stderr, line)
			if nasm_encoding == -1:
				return

			if ('(' in nasm_encoding and ')' in nasm_encoding):
				nasm_encoding = flip_imm(nasm_encoding)

			# print(nasm_encoding)

			special_xed_flag = ''
			if 'MPX' in saved_flags:
				special_xed_flag += '-mpx'
			if 'CET' in saved_flags:
				special_xed_flag += ' -cet'

			# feed encoding into xed
			result = subprocess.run(['./bash_helper.sh', f'{nasm_encoding}', 'nasm', long, special_xed_flag], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
			# get the decoded instruction this way
			xed_output = ""
			for xed_line in result.stdout.decode('utf-8').split('\n'):
				if xed_line.startswith("SHORT:"):
					xed_output = xed_line
			decoded_instruction = ':'.join(xed_output.split(':')[1:])
			# print("XED decoded instruction: ", decoded_instruction)
			# print("Xed output: \n", result.stdout.decode('utf-8'))
			# print("Xed errors: \n", result.stderr.decode('utf-8'))

			# fixup the mnemonic to use the 16 bit or 32 bit version
			if 'addr' in decoded_instruction:
				decoded_instruction = decoded_instruction.replace('addr', 'a')
			if 'data' in decoded_instruction:
				decoded_instruction = decoded_instruction.replace('data', 'o')

			# When XED decodes register as offset to ES it also adds the segment
			# register as operand at the end. Remove it so it assembles with NASM properly.
			if operands_len == 2 and decoded_instruction.count(',') == 2:
				decoded_instruction = decoded_instruction.replace(', es', '')

			if 'mem' in operands:
				decoded_instruction = re.sub(r"[xyo][m]{2}word ptr", "", decoded_instruction)

			# check if we need to write the word/dword/qword to the decoded
			# instruction to assemble properly
			if 'word' not in decoded_instruction and 'word' in starting_instruction:
				size = re.findall(r'[dq]?word', starting_instruction)

				# check if we're not looking at an address
				if '[' in decoded_instruction and ']' in decoded_instruction:
					sq_bracks = decoded_instruction[decoded_instruction.find("[")+1:decoded_instruction.find("]")]
					if '0x' not in sq_bracks:
						decoded_instruction = decoded_instruction.replace('0x', f"{size[0]} 0x")
				else:
					decoded_instruction = decoded_instruction.replace('0x', f"{size[0]} 0x")

			if mnemonic in lose_suffix:
				split_di = decoded_instruction.split()
				split_di[0] = split_di[0][:-1]
				decoded_instruction = ' '.join(split_di)

			if(result.stderr.decode('utf-8')):
				print("Error while assembling from insns.xda: ", starting_instruction)
				print("Instruction flags : ", saved_flags, ", ", long)
				print("Error : ", result.stderr.decode('utf-8'))
				exit(0)

			# read the ORIGINAL_NASM listing file
			xed_encoding = []

			# if (result.stderr.decode('utf-8')):
			# 	line_counter += 1
			# 	print(starting_instruction, '\t\t', 'None')
			# 	print("Failed to assemble something from insns.xda")
			# 	continue

			# print("Starting inst: ", starting_instruction)
			nasm_encoding = listing_to_encoding(starting_instruction, result.stderr, line)
			if nasm_encoding == -1:
				return
			# print("NASM encoding: ", nasm_encoding, saved_flags)
			#
			# if (result.stderr.decode('utf-8')):
			# 	if ("implicit DEFAULT ABS is deprecated" in result.stderr.decode('utf-8')):
			# 		nasm_encoding = nasm_encoding.replace('warning:', '')

			# if (not decoded_instruction):
			# 	print("XED didn't run, skipping...")
			# 	fail_counter += 1
			# 	line_counter += 1
			# 	print(fail_counter, skip_counter, line_counter, ':')
			# 	print(starting_instruction, '\t\t', nasm_encoding)
			# 	print(decoded_instruction, '\t\t', 'None')
			# 	continue

			# we need to remove non-NASM stuff from the decoded instruction
			# like 'ptr'
			# print(decoded_instruction)
			decoded_instruction = xed_format_to_nasm(decoded_instruction, starting_instruction)
			# print(decoded_instruction)
			if (not decoded_instruction):
				print("Decoded instruction was empty!\n")
				print(fail_counter, skip_counter, line_counter, ':')
				print(starting_instruction, '\t\t', nasm_encoding)
				exit(0)

			# use regex to fixup bits of syntax - like memory sizes
			for regex,replace in regex_fixes.items():
				decoded_instruction = re.sub(regex, replace, decoded_instruction)

			# re-assemble the xed decoded instruction into another listing file

			result = subprocess.run(['./bash_helper.sh', f'{decoded_instruction}', '', long], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

			# read the REASSEMBLED_XED listing file
			# if (not os.path.exists('/tmp/nasm_output.lst')):
			# 	fail_counter += 1
			# 	line_counter += 1
			# 	print(fail_counter, skip_counter, line_counter, ':')
			# 	print(starting_instruction, '\t\t', nasm_encoding)
			# 	print(decoded_instruction, '\t\t', 'None')
			# 	continue

			# print(result.stderr.decode('utf-8'))
			xed_encoding = listing_to_encoding(decoded_instruction, result.stderr, line)
			if xed_encoding == -1:
				return

			# if (result.stderr.decode('utf-8')):
			# 	if ("implicit DEFAULT ABS is deprecated" in result.stderr.decode('utf-8')):
			# 		xed_encoding = xed_encoding.replace('warning:', '')
			# 	else:
			# 		print("Error while reassembling: ", result.stderr.decode('utf-8'))
			# 		fail_counter += 1
			# 		line_counter += 1
			# 		print(fail_counter, skip_counter, line_counter, ':')
			# 		print(starting_instruction, '\t\t', nasm_encoding)
			# 		print(decoded_instruction, '\t\t', 'None')
			# 		continue

#flip_modrm_modreg
			# print(bin(f"0x{nasm_encoding[-2:]}"), bin(f"0x{xed_encoding[-2:]}"))

			if (nasm_encoding != xed_encoding):
				# try again if the instruction is an alias
				# but flip the modrm just in case that was the issue
				if ("OPT" in saved_flags):
					nasm_encoding = flip_modrm_modreg(nasm_encoding)
				if (nasm_encoding != xed_encoding):
					print(fail_counter, skip_counter, line_counter, ':')
					print(starting_instruction, '\t\t', nasm_encoding)
					print(decoded_instruction, '\t\t', xed_encoding)
					fail_counter += 1
					if (line_counter < 10000):
						return

			if line_counter % 100 == 0:
				print(f"Checked {round((line_counter/7133) * 100, 2)}% instructions ({line_counter} / 7133)...")

			line_counter += 1

print("Checking all instructions in insns.xda against intel-xed...")
main()

with open('saved_output', 'w') as file:
	file.write('\n'.join(output_saved))
