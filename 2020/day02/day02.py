import os
import re

from aocd import get_data
from dotenv import load_dotenv

from utils import generate_readme


def get_session() -> str:
    load_dotenv()
    return os.getenv('SESSION_COOKIE')


def run(day: int, year: int, data: str = None, part: int = None):
    if not data:
        # day, year = get_day_and_year()
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
    count = 0
    for line in data:
        min_count, max_count, char, password = parse_row(line)
        result = min_count <= len(re.findall(char, password)) <= max_count
        if result:
            count += 1
    return count


def parse_row(row):
    rules, password = row.split(": ")
    counts, char = rules.split(" ")
    min_count, max_count = map(
        lambda x: int(x) if x.isdigit else None, counts.split("-")
    )
    return min_count, max_count, char, password


def part2(data):
    count = 0

    def xor(a, b):
        return (a and not b) or (b and not a)

    for line in data:
        min_count, max_count, char, password = parse_row(line)
        result = xor(a=password[min_count - 1] == char,
                     b=password[max_count - 1] == char, )
        if result:
            count += 1
    return count


if __name__ == '__main__':
    print(f'Part 1: {run(data=None, day=2, year=2020, part=1)}')
    print(f'Part 2: {run(data=None, day=2, year=2020, part=2)}')
    generate_readme("README", '2020', '2', '../')
