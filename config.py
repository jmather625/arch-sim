'''
Defines how many cycles an instruction takes.

TODO: handle branches
'''


from isa import Instruction


INSTRUCTION_TO_EX_CYCLES = {
    Instruction.ADD: 1,
    Instruction.OR: 1,
    Instruction.XOR: 1,
    Instruction.NOT: 1,

    Instruction.ADD: 1,
    Instruction.SUB: 1,
    Instruction.MUL: 3,
    Instruction.DIV: 5,

    Instruction.FADD: 5,
    Instruction.FSUB: 5,
    Instruction.FMUL: 10,
    Instruction.FDIV: 20,

    Instruction.LD: 1,
    Instruction.SD: 1,
}

#     Instruction.BE: 2,
#     Instruction.BG: 2,
#     Instruction.BL: 2,
# }
