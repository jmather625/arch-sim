from typing import List

from isa import ISA, Command


def parse_assembly(filename: str) -> List[Command]:
    f = open(filename, 'r')
    cmds = list()
    while True:
        l = f.readline().strip()
        if l == "":
            break
        cmd = ISA.str_to_command(l)
        if cmd is None:
            f.close()
            raise ValueError(f"invalid command: {l}")
        cmds.append(cmd)

    f.close()
    return cmds


if __name__ == '__main__':
    cmds = parse_assembly("assembly/simple.txt")
    print(cmds)
