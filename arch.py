'''
Base computer arch class.

TODO: actually compute the values so that we know the arch is correct?
'''


from typing import List
from dataclasses import dataclass

from isa import Command


@dataclass
class Stats:
    cycles: int
    cmdn_to_cycle: List[int]
    r0_final: int


class Arch:
    def __init__(self):
        pass


    def issue(self, cmd: Command):
        '''
        Issue `cmd` to the architecture
        '''
        raise NotImplementedError()


    def do_cycle(self):
        '''
        Do one cycle in the architecture
        '''
        raise NotImplementedError()


    def check_cmd_done(self, cmdn: int) -> bool:
        '''
        Check if the `cmdn` command is done
        '''
        raise NotImplementedError()


    def get_r0(self) -> int:
        '''
        Gets the value in R0
        '''
        raise NotImplementedError()


class ArchSim:
    def __init__(self, arch: Arch):
        self.arch = arch


    def execute(self, cmds: List[Command]) -> Stats:
        stats = Stats(0, [0 for _ in range(len(cmds))], -1)

        last_cmdn = 0
        for cmd in cmds:
            self.arch.issue(cmd)

            # one cycle goes, then see if a cmd is done
            self.arch.do_cycle()
            stats.cycles += 1
            if self.arch.check_cmd_done(last_cmdn):
                stats.cmdn_to_cycle[last_cmdn] = stats.cycles
                last_cmdn += 1


        while last_cmdn != len(cmds):
            # one cycle goes, then see if a cmd is done
            self.arch.do_cycle()
            stats.cycles += 1
            if self.arch.check_cmd_done(last_cmdn):
                stats.cmdn_to_cycle[last_cmdn] = stats.cycles
                last_cmdn += 1


        # get the final value of r0
        r0_result = self.arch.get_r0()
        stats.r0_final = r0_result
        return stats
