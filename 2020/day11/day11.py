import os
from functools import cache
from typing import Optional, Tuple

from aocd import get_data
from dotenv import load_dotenv

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


def _index(lines, y, x):
    if y < 0:
        return ' '
    elif y >= len(lines):
        return ' '
    elif x < 0:
        return ' '
    elif x >= len(lines[0]):
        return ' '
    return lines[y][x]


@cache
def _adjacent(lines, y, x):
    @cache
    def _inner():
        for y_i in range(y - 1, y + 2):
            for x_i in range(x - 1, x + 2):
                if (y_i, x_i) != (y, x):
                    yield _index(lines, y_i, x_i)

    return tuple(_inner())


def part1(data):
    lines = tuple(data.splitlines())
    prev: Optional[Tuple[str, ...]] = None
    while lines != prev:
        prev = lines
        new_lines = []
        for y, line in enumerate(lines):
            line_c = []
            for x, c in enumerate(line):
                if c == 'L':
                    if _adjacent(lines, y, x).count('#') == 0:
                        line_c.append('#')
                    else:
                        line_c.append('L')
                elif c == '#':
                    if _adjacent(lines, y, x).count('#') >= 4:
                        line_c.append('L')
                    else:
                        line_c.append('#')
                else:
                    line_c.append(c)

                new_lines.append(''.join(line_c))

                lines = tuple(new_lines)

    return sum(line.count('#') for line in lines)


def part2(data):
    return data


if __name__ == '__main__':
    print(f'Part 1: {run(data=None, part=1)}')
    # print(f'Part 2: {run(data=None, part=2)}')
    # generate_readme("README", year, day, '../')
