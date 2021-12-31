import os
from collections import Counter

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


def part1(data: list) -> int:
    numbers = get_numbers(data)
    numbers = [numbers[i] - numbers[i - 1] for i in range(1, len(numbers))]
    counts = Counter(numbers)
    return counts[1] * counts[3]


def get_numbers(data):
    return sorted([0] + [int(line) for line in data] + [max([int(line) for line in data]) + 3])


def part2(data):
    numbers = get_numbers(data)
    reverse = get_reverse(numbers)
    temp = {0: 1}
    for i, number in list(enumerate(numbers))[1:]:
        temp[i] = 0
        for diff in [1, 2, 3]:
            if number - diff in reverse:
                temp[i] += temp[reverse[number - diff]]
    return temp[len(numbers) - 1]


def get_reverse(numbers):
    return {i: n for n, i in enumerate(numbers)}


if __name__ == '__main__':
    print(f'Part 1: {run(data=None, part=1)}')
    print(f'Part 2: {run(data=None, part=2)}')
    generate_readme("README", year, day, '../')
