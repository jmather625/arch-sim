'''
Defines a simple ISA.

TODO: add float load/store, float branch
TODO: add int->float and float->int?
'''


from enum import Enum


class Instruction(Enum):
    # logical
    AND = 0
    OR = 1
    XOR = 2
    NOT = 3

    # integer
    ADD = 4
    SUB = 5
    MUL = 6
    DIV = 7

    # float
    FADD = 8
    FSUB = 9
    FMUL = 10
    FDIV = 11

    # load
    LD = 12
    SD = 13

    # branch
    BE = 14
    BG = 15
    BL = 16


_STR_TO_INSTR = {
    "AND": Instruction.AND,
    "OR": Instruction.OR,
    "XOR": Instruction.XOR,
    "NOT": Instruction.NOT,

    "ADD": Instruction.ADD,
    "SUB": Instruction.SUB,
    "MUL": Instruction.MUL,
    "DIV": Instruction.DIV,

    "FADD": Instruction.FADD,
    "FSUB": Instruction.FSUB,
    "FMUL": Instruction.FMUL,
    "FDIV": Instruction.FDIV,

    "LD": Instruction.LD,
    "SD": Instruction.SD,

    "BE": Instruction.BE,
    "BG": Instruction.BG,
    "BL": Instruction.BL,
}


class Reg(Enum):
    # integer regs
    R0 = 0
    R1 = 1
    R2 = 2
    R3 = 3
    R4 = 4

    FR0 = 5
    FR1 = 6
    FR2 = 7
    FR3 = 8
    FR4 = 9


    def __repr__(self) -> str:
        return self.name


_STR_TO_REG = {
    "R0": Reg.R0,
    "R1": Reg.R1,
    "R2": Reg.R2,
    "R3": Reg.R3,
    "R4": Reg.R4,
    
    "FR0": Reg.FR0,
    "FR1": Reg.FR1,
    "FR2": Reg.FR2,
    "FR3": Reg.FR3,
    "FR4": Reg.FR4,
}


class Literal:
    def __init__(self, val):
        self.val = val


    def __repr__(self) -> str:
        return str(self.val)


class Operand:
    REG_TYPE = 0
    LITERAL_TYPE = 1

    def __init__(self, val, typ):
        assert typ in [Operand.REG_TYPE, Operand.LITERAL_TYPE]
        self.val = val
        self.typ = typ

    
    def __repr__(self) -> str:
        return self.val.__repr__()


class Command:
    def __init__(self, instr: Instruction, operand1, operand2: Operand, operand3: Operand):
        self.instr = instr
        self.operand1 = operand1
        self.operand2 = operand2
        self.operand3 = operand3

    
    def __repr__(self) -> str:
        return f"Command({self.instr}, {self.operand1}, {self.operand2}, {self.operand3})"


class ISA:
    @staticmethod
    def str_to_instr(s: str) -> Instruction:
        if s in _STR_TO_INSTR:
            return _STR_TO_INSTR[s]
        return None

    
    @staticmethod
    def str_to_reg(s: str) -> Reg:
        if s in _STR_TO_REG:
            return _STR_TO_REG[s]
        return None


    @staticmethod
    def str_to_literal(s: str, is_float: bool) -> Literal:
        if len(s) == 0:
            return None
        elif s[0] != "$":
            # all literals must be of the form $abcd
            return None

        if is_float:
            return Literal(float(s[1:]))
        else:
            return Literal(int(s[1:]))


    @staticmethod
    def str_to_operand(s: str, is_float: bool) -> Operand:
        reg = ISA.str_to_reg(s)
        if reg is None:
            literal = ISA.str_to_literal(s, is_float)
            if literal is None:
                return None # failed to convert to reg or literal

            return Operand(literal, Operand.LITERAL_TYPE)
        
        if is_float:
            if reg not in {Reg.FR0, Reg.FR1, Reg.FR2, Reg.FR3, Reg.FR4}:
                return None # must be a floating reg
        else:
            if reg not in {Reg.R0, Reg.R1, Reg.R2, Reg.R3, Reg.R4}:
                return None # must be an int reg

        return Operand(reg, Operand.REG_TYPE)


    @staticmethod
    def str_to_command(s: str) -> Command:
        pieces = s.split(" ")
        if len(pieces) <= 1 or len(pieces) >= 5:
            return None
        instr = ISA.str_to_instr(pieces[0])
        if instr is None:
            return None

        if instr in {Instruction.BE, Instruction.BG, Instruction.BL}:
            # branch instruction
            if len(pieces) != 2:
                return None # must be only one operand

            operand = ISA.str_to_operand(pieces[1], False)
            if operand is None:
                return None # invalid input
            elif operand.typ != Operand.REG_TYPE:
                return None # must be reg type
            
            return Command(instr, operand, None, None)

        else:
            # regular instruction
            if len(pieces) != 4:
                return None # must be two operands
            
            is_float = instr in {Instruction.FADD, Instruction.FSUB, Instruction.FMUL, Instruction.FDIV}
            operand1 = ISA.str_to_operand(pieces[1], is_float)
            operand2 = ISA.str_to_operand(pieces[2], is_float)
            operand3 = ISA.str_to_operand(pieces[3], is_float)
        
            if operand1 is None or operand2 is None or operand3 is None:
                return None
            elif operand2.typ != Operand.REG_TYPE or operand3.typ != Operand.REG_TYPE:
                return None # the second and third operand must be a reg

            return Command(instr, operand1, operand2, operand3)

