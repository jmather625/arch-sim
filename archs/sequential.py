from typing import List

import sys
sys.path.append("..")
from arch import Arch, Stats
from isa import Command, Reg
from config import INSTRUCTION_TO_EX_CYCLES


class Sequential(Arch):
    def __init__(self):
        super().__init__()
        
        self.cmd_queue = list()
        self.cmd_cycles = list()
        self.cmdn_done = set()
        self.r0_value = -1


    def issue(self, cmd: Command):
        '''
        Issue `cmd` to the architecture.
        '''
        self.cmd_queue.append(cmd)
        expected_cycles = INSTRUCTION_TO_EX_CYCLES[cmd.instr]
        self.cmd_cycles.append(expected_cycles)


    def do_cycle(self):
        '''
        Do one cycle in the architecture.

        In sequential, this is trivial.
        '''

        if len(self.cmd_queue) == 0:
            return # no commands left

        self.cmd_cycles[0] -= 1
        if self.cmd_cycles[0] == 0:
            # pop
            if self.cmd_queue[0].operand3 == Reg.R0:
                # TODO: actually compute and save value
                self.r0_value = -1

            self.cmdn_done.add( self.cmd_queue[0].cmdn )
            self.cmd_queue = self.cmd_queue[1:]
            self.cmd_cycles = self.cmd_cycles[1:]


    def check_cmd_done(self, cmdn: int) -> bool:
        '''
        Check if the `cmdn` command is done.
        '''
        return cmdn in self.cmdn_done


    def get_r0(self) -> int:
        '''
        Gets the value in R0.
        '''
        return self.r0_value
