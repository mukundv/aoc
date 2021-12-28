import collections
import os
import re
from typing import Any, Match

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


def get_pattern():
    return re.compile('^([^ ]+ [^ ]+) bags contain (.*)$')


pattern = get_pattern()


def get_bag():
    return re.compile(r'(\d+) ([^ ]+ [^ ]+)')


bag = get_bag()


def part1(data: list) -> int:
    parents = collections.defaultdict(list)
    for line in data:
        get_parents(line, parents)
    total_colours = set()
    todo = parents['shiny gold']
    while todo:
        colour = todo.pop()
        if colour not in total_colours:
            total_colours.add(colour)
            todo.extend(parents[colour])
    return len(total_colours)


def get_parents(line: str, parents: collections.defaultdict[Any, list]):
    k, match = get_match(line)
    targets = get_targets(match)
    for _, colour in targets:
        parents[colour].append(k)


def get_match(line: str) -> tuple[str | Any, Match[str] | None]:
    match = pattern.match(line)
    assert match
    k = match[1]
    return k, match


def get_targets(match: Match[str]) -> list:
    return [(int(n), tp) for n, tp in bag.findall(match[2])]


def part2(data: list) -> int:
    colours = {}
    for line in data:
        k, match = get_match(line)
        colours[k] = get_targets(match)
    total_bags = 0
    todo = [(1, 'shiny gold')]
    while todo:
        n, colour = todo.pop()
        total_bags += n
        for n_i, colour_i in colours[colour]:
            todo.append((n * n_i, colour_i))
    total_bags -= 1
    return total_bags


if __name__ == '__main__':
    print(f'Part 1: {run(data=None, part=1)}')
    print(f'Part 2: {run(data=None, part=2)}')
    generate_readme("README", year, day, '../')
