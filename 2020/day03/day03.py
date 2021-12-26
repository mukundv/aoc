import math
import os
from functools import lru_cache

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
            return part1(get_data(get_session(), day=day, year=year))
        else:
            return part2(get_data(get_session(), day=day, year=year))
    else:
        if part == 1:
            return part1(data)
        else:
            return part2(data)


def part1(data):
    return calc(data=data, right=3, down=1)


@lru_cache(maxsize=None)
def calc(data, right, down):
    count = 0
    position = [0, 0]
    lines = data.splitlines()
    width = len(lines[0])
    while position[1] <= len(lines):
        position[0] += right
        position[1] += down
        if position[0] >= width:
            position[0] = position[0] - width
        x, y = position
        if y >= len(lines):
            break
        if lines[y][x] != '.':
            count += 1
    return count


def part2(data):
    slopes = [[1, 1], [3, 1], [5, 1], [7, 1], [1, 2]]
    done = []
    for slope in slopes:
        x, y = slope
        done.append(calc(data=data, right=x, down=y))
    return math.prod(done)


if __name__ == '__main__':
    print(f'Part 1: {run(data=None, part=1)}')
    print(f'Part 2: {run(data=None, part=2)}')
    generate_readme("README", year, day, '../')
