import os
import datatypes
import readline

enum InstructionType {
	inc
	dec
	shiftl
	shiftr
	startl
	endl
	print
	getc
}

fn parse_inst(inst u8) ?InstructionType {
	return match inst {
		`+` { .inc }
		`-` { .dec }
		`<` { .shiftl }
		`>` { .shiftr }
		`[` { .startl }
		`]` { .endl }
		`.` { .print }
		`,` { .getc }
		else { none }
	}
}

fn parse(program []u8) []InstructionType {
	mut parsed := []InstructionType{}
	for inst in program {
		parsed << parse_inst(inst) or { continue }
	}
	return parsed
}

fn interpret(insts []InstructionType) ? {
	mut inst_ptr := 0
	mut memory_ptr := 0

	mut memory := []u8{len: 256*256, init: 0}
	mut brackets_stack := datatypes.Stack[int]{}

	mut r := readline.Readline{}

	for inst_ptr < insts.len {
		match insts[inst_ptr] {
			.inc {
				memory[memory_ptr]++
			}
			.dec {
				memory[memory_ptr]--
			}
			.shiftl {
				memory_ptr--
			}
			.shiftr {
				memory_ptr++
			}
			.startl {
				if memory[memory_ptr] != 0 {
					brackets_stack.push(inst_ptr)
				} else {
					mut bracket_count := 1
					for bracket_count != 0 {
						inst_ptr++
						match insts[inst_ptr] {
							.startl {bracket_count++}
							.endl {bracket_count--}
							else {}
						}
					}
				}
			}
			.endl {
				if memory[memory_ptr] != 0 {
					inst_ptr = brackets_stack.peek() or {inst_ptr}
				} else {
					brackets_stack.pop() or {}
				}
			}
			.print {
				print([memory[memory_ptr]].bytestr())
			}
			.getc {
				memory[memory_ptr] = u8(r.read_char()!)
			}
		}
		inst_ptr++
	}
}

fn main() {
	program := os.read_file_array[u8]('mandelbrot.b')
	interpret(parse(program)) or { println('Failed!') }
}
