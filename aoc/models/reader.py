import os
import sys
from typing import List


class Reader:
    """
    Utility class for reading Advent of Code puzzle and test input files.

    This class handles file reading operations with support for both raw and stripped
    input formats. It maintains consistent file path handling relative to the project root.

    Attributes:
        PROJECT_ROOT (str): Absolute path to the project root directory, determined from
            the `aoc` package location.
    """

    PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__).rsplit("aoc", 1)[0])

    @staticmethod
    def get_path() -> str:
        """
        Get the absolute path to the script's location.

        Returns:
            str: Absolute path to either the directory containing the script or
                the script's directory if it is itself a directory.
        """
        return (
            path if os.path.isdir(path := os.path.realpath(sys.argv[0])) else os.path.dirname(path)
        )

    @staticmethod
    def get_puzzle_input(day: int, is_raw: bool) -> List[str]:
        """
        Read in the puzzle input file for a specific day.

        Args:
            day (int): The day number (1-25) of the puzzle.
            is_raw (bool): If True, preserves newlines. If False, strips all whitespace.

        Returns:
            List[str]: List of input lines, processed according to `is_raw` flag.

        Note:
            Expects input file at: `data/dayXX/puzzle_input.txt`
            where `XX` is the zero-padded day number.
        """
        file_path = os.path.join(Reader.PROJECT_ROOT, f"data/day{day:02d}/puzzle_input.txt")
        with open(file_path, "r") as file:
            return [line.strip("\n") if is_raw else line.strip() for line in file.readlines()]

    @staticmethod
    def get_test_input(day: int, is_raw: bool, part_num: int) -> List[str]:
        """
        Read the test input file for a specific day and puzzle part.

        Args:
            day (int): The day number (1-25) of the puzzle.
            is_raw (bool): If `True`, preserves newlines. If `False`, strips all whitespace.
            part_num (int): The puzzle part number (1 or 2).

        Returns:
            List[str]: List of test input lines, processed according to `is_raw` flag.

        Note:
            Expects input file at: `tests/data/dayXX/test_YY_input.txt`
            where `XX` is the zero-padded day number and `YY` is the zero-padded part number.
        """
        file_path = os.path.join(
            Reader.PROJECT_ROOT,
            f"tests/data/day{day:02d}/test_{part_num:02d}_input.txt",
        )
        with open(file_path, "r") as file:
            return [line.strip("\n") if is_raw else line.strip() for line in file.readlines()]
