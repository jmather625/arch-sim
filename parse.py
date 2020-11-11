from typing import List, Tuple

from isa import ISA, Command


def parse_assembly(filename: str) -> Tuple[List[Command], int]:
    f = open(filename, 'r')
    cmds = list()
    last_cmdn = 0
    expected_r0_result = None
    while True:
        l = f.readline().strip()
        if l == "":
            # parse result and break
            l = f.readline().strip()
            expected_prefix = "RESULT R0=="
            if l[:len(expected_prefix)] != expected_prefix:
                f.close()
                raise ValueError(f"expected something of the form {expected_prefix}, got {l}")

            expected_r0_result = int( l[len(expected_prefix):] )
            break

        cmd = ISA.str_to_command(l)
        if cmd is None:
            f.close()
            raise ValueError(f"invalid command: {l}")
        cmd.set_cmdn(last_cmdn)
        last_cmdn += 1
        cmds.append(cmd)

    f.close()
    return cmds, expected_r0_result

