import os
import re

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


def get_passports(passport):
    values = {}
    for i in passport.split(' '):
        for j in i.split('\n'):
            key, value = j.split(':')
            values[key] = value
    return values


def validate(passport):
    keys = passport.keys()
    return len(keys) == 8 or (len(keys) == 7 and 'cid' not in keys)


def part1(data):
    passports = [get_passports(lines) for lines in data]
    return len([passport for passport in passports if validate(passport)])


def check_range(value, low, high):
    return low <= int(value) <= high


def check_dob(value):
    return check_range(value, 1920, 2002)


def check_issue(value):
    return check_range(value, 2010, 2020)


def check_expiration(value):
    return check_range(value, 2020, 3030)


def check_height(value):
    if value.find("cm") < 0:
        if value.find("in") > 0:
            height = int(value[:value.find("in")])
            return check_range(height, 59, 76)
    else:
        height = int(value[:value.find("cm")])
        return check_range(height, 150, 193)


def check_hair_colour(value: str) -> bool:
    return re.compile(r'#[0-9a-f]{6}').match(value) is not None


def check_eye_colout(value: str) -> bool:
    return value in ['amb', 'blu', 'brn', 'gry', 'grn', 'hzl', 'oth']


def check_pid(value: str) -> bool:
    return re.compile(r'\d{9}$').match(value) is not None


def validate2(passport):
    if not validate(passport):
        return False

    checks = []

    for key, value in passport.items():
        if key == 'byr':
            checks.append(check_dob(value))
        elif key == 'iyr':
            checks.append(check_issue(value))
        elif key == 'eyr':
            checks.append(check_expiration(value))
        elif key == 'hgt':
            checks.append(check_height(value))
        elif key == 'hcl':
            checks.append(check_hair_colour(value))
        elif key == 'ecl':
            checks.append(check_eye_colout(value))
        elif key == 'pid':
            checks.append(check_pid(value))
        elif key == 'cid':
            checks.append(True)

    return all(checks)


def part2(data):
    passports = [get_passports(lines) for lines in data]
    valid = [passport for passport in passports if validate2(passport)]
    return len(valid)


if __name__ == '__main__':
    print(f'Part 1: {run(data=None, part=1)}')
    print(f'Part 2: {run(data=None, part=2)}')
    generate_readme("README", year, day, '../')
