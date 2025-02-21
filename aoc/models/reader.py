"""
Provides utilities for reading input files for Advent of Code puzzles.

This module contains the Reader class which handles loading inputs from the appropriate
file paths based on the day and whether it's test or actual puzzle input.
"""

from pathlib import Path


class Reader:
    """
    Handles reading input files for Advent of Code puzzles.

    This class provides static methods to load puzzle inputs, handling both
    actual inputs and test inputs for different days and parts.
    """

    _current_file_path = Path(__file__).resolve()
    _aoc_dir = _current_file_path.parent.parent
    PROJECT_ROOT = _aoc_dir.parent

    @classmethod
    def get_test_input(cls, day: int, part_num: int, *, raw: bool) -> str | list[str]:
        """
        Read test input for a specific day and part.

        Args:
            day: The day number (1-25)
            raw: If True, preserves newlines. If False, strips whitespace
            part_num: The puzzle part number (1 or 2)

        Returns
        -------
            The test input as a string or list of strings
        """
        file_path = (
            cls.PROJECT_ROOT / "tests" / "data" / f"day{day:02d}" / f"test_{part_num:02d}_input.txt"
        )

        with Path.open(file_path) as f:
            content = f.read()

        if raw:
            return content

        # For non-raw input, split into lines and strip whitespace
        return content.strip().split("\n")

    @classmethod
    def get_puzzle_input(cls, day: int, *, raw: bool = False) -> str | list[str]:
        """
        Read actual puzzle input for a specific day.

        Args:
            day: The day number (1-25)
            raw: If True, preserves newlines. If False, strips whitespace

        Returns
        -------
            The puzzle input as a string or list of strings
        """
        file_path = cls.PROJECT_ROOT / "data" / f"day{day:02d}.txt"

        with Path.open(file_path) as f:
            content = f.read()

        if raw:
            return content

        # For non-raw input, split into lines and strip
        return content.strip().split("\n")
