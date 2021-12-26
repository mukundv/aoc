import os

from aocd import get_data
from dotenv import load_dotenv

from utils import generate_readme


def get_session() -> str:
    load_dotenv()
    return os.getenv('SESSION_COOKIE')


def run(day: int, year: int, data: str = None, part: int = None):
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
    data = get_int_data(data)
    for i in range(len(data)):
        for j in range(i + 1, len(data)):
            if data[i] + data[j] == 2020:
                return data[i] * data[j]


def get_int_data(data):
    return [int(i) for i in data]


def part2(data):
    data = get_int_data(data)
    for i in range(len(data)):
        for j in range(i + 1, len(data)):
            for k in range(j + 1, len(data)):
                if data[i] + data[j] + data[k] == 2020:
                    return data[i] * data[j] * data[k]


if __name__ == '__main__':
    print(f'Part 1: {run(data=None, day=1, year=2020, part=1)}')
    print(f'Part 2: {run(data=None, day=1, year=2020, part=2)}')
    generate_readme("README", '2020', '1', '../')
