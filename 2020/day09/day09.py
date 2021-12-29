import itertools
import os
from typing import List

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


def calc(data: list, n: int = 125) -> int:
    seen: List[int] = []
    for i, line in enumerate(data):
        if i >= n:
            prev_25 = seen[-n:]
            for x, y in itertools.combinations(prev_25, 2):
                if x + y == int(line):
                    break
            else:
                return int(line)
        seen.append(int(line))
    raise NotImplementedError('unreachable')


def part1(data):
    return calc(data)


def part2(data):
    target = calc(data)
    numbers = [int(line) for line in data]
    start = 0
    end = 0
    current = numbers[0]
    while True:
        if current < target:
            end += 1
            current += numbers[end]
        elif current > target:
            current -= numbers[start]
            start += 1
        else:
            r = numbers[start:end + 1]
            return min(r) + max(r)


if __name__ == '__main__':
    print(f'Part 1: {run(data=None, part=1)}')
    print(f'Part 2: {run(data=None, part=2)}')
    generate_readme("README", year, day, '../')
