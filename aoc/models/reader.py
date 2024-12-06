import os
import sys
from typing import List


class Reader:
    PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__).rsplit("aoc", 1)[0])

    @staticmethod
    def get_path() -> str:
        return (
            path
            if os.path.isdir(path := os.path.realpath(sys.argv[0]))
            else os.path.dirname(path)
        )

    @staticmethod
    def get_puzzle_input(day: int, is_raw: bool) -> List[str]:
        file_path = os.path.join(
            Reader.PROJECT_ROOT, f"data/day{day:02d}/puzzle_input.txt"
        )
        with open(file_path, "r") as file:
            return [
                line.strip("\n") if is_raw else line.strip()
                for line in file.readlines()
            ]

    @staticmethod
    def get_test_input(day: int, is_raw: bool, part_num: int) -> List[str]:
        file_path = os.path.join(
            Reader.PROJECT_ROOT, f"data/day{day:02d}/test_{part_num:02d}_input.txt"
        )
        with open(file_path, "r") as file:
            return [
                line.strip("\n") if is_raw else line.strip()
                for line in file.readlines()
            ]
