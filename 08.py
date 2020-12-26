from dataclasses import dataclass


@dataclass
class CmdValPair:
    cmd: str
    val: int


def command_generator(path):
    with open(path) as f:
        for line in f:
            cmd, val = line.rstrip().split()
            yield CmdValPair(cmd, int(val))


def run_boot_seq(seq):
    visited = set()
    accumulator = 0
    max_i = len(seq) - 1
    i = 0
    while True:
        assert 0 <= i <= max_i + 1
        if i == max_i + 1:
            return accumulator, True
        if i in visited:
            return accumulator, False

        curr_cmd = seq[i]
        visited.add(i)

        if curr_cmd.cmd == "nop":
            i += 1
        elif curr_cmd.cmd == "acc":
            i += 1
            accumulator += curr_cmd.val
        else:
            i += curr_cmd.val


def swap_nop_jmp(seq):
    for cmd_val in seq:
        cmd_before = cmd_val.cmd
        if cmd_before == "nop":
            cmd_val.cmd = "jmp"
        elif cmd_before == "jmp":
            cmd_val.cmd = "nop"
        else:
            continue

        acc, terminated = run_boot_seq(seq)
        if terminated:
            return acc

        cmd_val.cmd = cmd_before


input_seq = list(command_generator("inputs/08.txt"))
print(run_boot_seq(input_seq)[0])
print(swap_nop_jmp(input_seq))
