import os

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


def part1(data):
    return calc(data)


def calc(data):
    maximum = 0
    for line in data:
        line = refactor_line(line)
        maximum = max(maximum, int(line, 2))
    return maximum


def refactor_line(line):
    line = line.replace('F', '0').replace('B', '1')
    line = line.replace('R', '1').replace('L', '0')
    return line


def part2(data):
    possible = set(range(1024))
    for line in data:
        line = refactor_line(line)
        possible.discard(int(line, 2))
    for candidate in possible:
        if candidate - 1 not in possible and candidate + 1 not in possible:
            return candidate


if __name__ == '__main__':
    print(f'Part 1: {run(data=None, part=1)}')
    print(f'Part 2: {run(data=None, part=2)}')
    generate_readme("README", year, day, '../')
