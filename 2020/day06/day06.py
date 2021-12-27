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
            return part1(get_data(get_session(), day=day, year=year).split('\n\n'))
        else:
            return part2(get_data(get_session(), day=day, year=year).split('\n\n'))
    else:
        if part == 1:
            return part1(data.split('\n\n'))
        else:
            return part2(data.split('\n\n'))


def part1(data):
    count = 0
    for line in data:
        count += len(set(line) - {' ', '\n'})
    return count


def part2(data):
    count = 0
    for group in data:
        line = group.splitlines()
        counted = set(line[0])
        for not_counted in line[1:]:
            counted &= set(not_counted)
        count += len(counted)
    return count


if __name__ == '__main__':
    print(f'Part 1: {run(data=None, part=1)}')
    print(f'Part 2: {run(data=None, part=2)}')
    generate_readme("README", year, day, '../')
