import cProfile
import io
import os
import pstats
import shutil
from datetime import datetime
from functools import wraps
from os.path import exists
from time import time

import markdown
import requests
import snakemd
from bs4 import BeautifulSoup
from dotenv import load_dotenv


## Profiling functions

# from https://towardsdatascience.com/bite-sized-python-recipes-52cde45f1489


def timeit(func):
    """
    :param func: Decorated function
    :return: Execution time for the decorated function
    """

    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time()
        result = func(*args, **kwargs)
        end = time()
        print(f'Timeit: {func.__name__} executed in {end - start:.6f} seconds')
        return result

    return wrapper


def profile(func):
    def wrapper(*args, **kwargs):
        pr = cProfile.Profile()
        pr.enable()
        retval = func(*args, **kwargs)
        pr.disable()
        s = io.StringIO()
        sort_by = pstats.SortKey.CUMULATIVE  # 'cumulative'
        ps = pstats.Stats(pr, stream=s).sort_stats(sort_by)
        ps.print_stats()
        print(s.getvalue())
        return retval

    return wrapper


## Markdown generator functions
load_dotenv()
CURRENT_DIR = os.getcwd()
SESSION_COOKIE = os.getenv('SESSION_COOKIE')
HEADERS = {"cookie": f"session={SESSION_COOKIE}", }
readme_table = {}


def read_readme(directory, year):
    if not exists(f'{directory}README.md'):
        return None
    else:
        if not readme_table:
            soup = BeautifulSoup(markdown.markdown(
                open(f"{directory}README.md", "r", encoding='utf-8', errors="ignore"
                     ).read()), "html.parser")
            a = soup.findAll('a')
            i = 1
            for row in (a[1:]):
                if 'md' in str(row):
                    title = row.text
                    readme_table[year, i] = title
                    i += 1
        return readme_table


def get_puzzle_name(directory, year, day):
    return read_readme(directory, year).get((str(year), day))


def fetch_puzzle_name(year, day):
    url = f"https://adventofcode.com/{year}/day/{day}"
    ret = requests.get(url).text.strip()
    x = BeautifulSoup(ret, "html.parser")
    name = x.article.contents[0].contents[0]
    name = name.strip().split(':')[1].strip()[:-4]
    return name


def get_table_body(year, upto, directory):
    base_url = "https://github.com/mukundv/aoc/"
    body = []
    for i in range(1, int(upto) + 1):
        name = get_puzzle_name(directory, year, i)
        a = str(i).zfill(2)
        if name:
            puzzle = snakemd.InlineText(name, url=f"{base_url}blob/main/{year}/day{a}/day{a}.md")
        else:
            puzzle = snakemd.InlineText(fetch_puzzle_name(year, i), url=f"{base_url}blob/main/day{a}/day{a}.md")
        aoc_input = snakemd.InlineText(f"day{a}_input.txt", url=f"{base_url}blob/main/{year}/day{a}/day{a}_input.txt")
        solution = snakemd.InlineText(f"day{a}.py", url=f"{base_url}blob/main/{year}/day{a}/day{a}.py")
        tag = snakemd.InlineText(f"day{a}", url=f"{base_url}releases/tag/day{a}")
        body.append([a, puzzle, aoc_input, solution, tag])
    return body


def generate_readme(name, year, day, directory):
    readme = snakemd.Document(name)
    readme.add_header(f"AOC {year}")
    readme.add_element(
        snakemd.Paragraph(
            [snakemd.InlineText("stars", url="https://img.shields.io/badge/stars%20-42-yellow", image=True)]))
    readme.add_element(
        snakemd.Paragraph(
            [snakemd.InlineText("days", url="https://img.shields.io/badge/days%20completed-21-red", image=True)]))
    readme.add_paragraph(f"Fun with Python :snake: - aoc {year}") \
        .insert_link(f"aoc {year}", f"https://adventofcode.com/{year}")
    header = ["Day", "Puzzle", "Input", "Solution", "Tag"]
    readme.add_element(snakemd.Table(header=header, body=get_table_body(year, day, directory)))
    now = datetime.today().strftime('%d-%m-%Y %H:%M:%S')
    readme.add_paragraph(f"This document was automatically rendered on {now} using SnakeMD") \
        .insert_link("SnakeMD", url="https://github.com/TheRenegadeCoder/SnakeMD")
    readme.output_page(dump_dir=directory)
    print(f'Readme Generated {directory}README.md')


def generate_dirs(day, year):
    if not os.path.exists(f'{os.getcwd()}/{year}'):
        os.mkdir(f'{os.getcwd()}/{year}')
    if len(str(day)) == 1:
        day = '0' + str(day)
    path = f'{os.getcwd()}/{year}/day{day}'
    if os.path.exists(path):
        print(f' Directory already exists')
    else:
        os.mkdir(path)
        print(f'Directory {path} created')
        copy_template(path, f'day{day}.py')
        print(f'File {path}/day{day}.py created')


def copy_template(path, target):
    source = f'{os.getcwd()}/template.py'
    target = f'{path}/{target}'
    shutil.copyfile(source, target)


def setup_year(year):
    for day in range(1, 26):
        generate_dirs(day, year)


if __name__ == '__main__':
    setup_year(2020)
