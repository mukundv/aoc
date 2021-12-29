import os
from typing import List, Tuple, Any

from aocd import get_data
from dotenv import load_dotenv

from utils import generate_readme

day = int(os.getcwd()[-2:])
year = int(os.getcwd()[-10:][:4])


def get_session() -> str:
    load_dotenv()
    return os.getenv('SESSION_COOKIE')


def run(data: str = None, part: int = None):
    if not data:
        if part == 1:
            return part1(get_data(get_session(), day=day, year=year).splitlines())
        else:
            return part2(get_data(get_session(), day=day, year=year).splitlines())
    else:
        if part == 1:
            return part1(data.splitlines())
        else:
            return part2(data.splitlines())


def calc(data):
    return get_accumulator_value(get_code(data))


def get_accumulator_value(code: list[tuple[Any, int]]) -> int:
    visited = set()
    n = 0
    pc = 0
    while pc not in visited:
        visited.add(pc)
        opc, value = code[pc]
        if opc == 'acc':
            n += value
            pc += 1
        elif opc == 'jmp':
            pc += value
        elif opc == 'nop':
            pc += 1
    return n


def get_code(data: list) -> list[tuple[Any, int]]:
    code = []
    for line in data:
        opc, n_s = line.split()
        n = int(n_s)
        code.append((opc, n))
    return code


def part1(data):
    return calc(data)


def get_flip():
    return {'nop': 'jmp', 'jmp': 'nop'}


flip = get_flip()


def get_acc_after_termination(code: List[Tuple[str, int]], flip: int) -> int:
    visited = set()
    n = 0
    pc = 0
    while pc not in visited and pc < len(code):
        visited.add(pc)
        opc, value = code[pc]

        if pc == flip:
            opc = get_flip()[opc]

        if opc == 'acc':
            n += value
            pc += 1
        elif opc == 'jmp':
            pc += value
        elif opc == 'nop':
            pc += 1
        else:
            raise NotImplementedError(opc)

    if pc == len(code):
        return n
    else:
        raise RuntimeError(visited)


def part2(data):
    code = get_code(data)
    try:
        get_acc_after_termination(code, -1)
    except RuntimeError as e:
        visited, = e.args
    else:
        raise AssertionError('unreachable')

    for i in visited:
        if code[i][0] in {'nop', 'jmp'}:
            try:
                return get_acc_after_termination(code, i)
            except RuntimeError:
                pass

    raise NotImplementedError('wat')


if __name__ == '__main__':
    print(f'Part 1: {run(data=None, part=1)}')
    print(f'Part 2: {run(data=None, part=2)}')
    generate_readme("README", year, day, '../')
