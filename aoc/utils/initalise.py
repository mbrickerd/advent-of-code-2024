"""
Utility to dynamically load puzzle solution modules.

This module provides functionality to dynamically import solution
classes for Advent of Code puzzles based on the day number.
"""

from importlib import import_module
from typing import TypeVar

from aoc.models.base import SolutionBase


S = TypeVar("S", bound=SolutionBase)


def initialise(
    day: int,
    part: int = 1,
    *,
    raw: bool = False,
    skip_test: bool = True,
    benchmark: bool = False,
) -> SolutionBase:
    """
    Dynamically load and instantiate the `Solution` class for a specific puzzle day.

    Args:
        day (int): The day number (1-25) of the puzzle to initialize.
        part (int, optional): Part number (1 or 2) to solve. Defaults to 1.
        raw (bool, optional): Whether to use raw input. Defaults to False.
        skip_test (bool, optional): Whether to skip test input. Defaults to True.
        benchmark (bool, optional): Whether to benchmark performance. Defaults to False.

    Returns
    -------
        SolutionBase: An instance of the day's `Solution` class, initialized with the
            specified parameters.

    Note:
        - Expects solution modules to be named `dayXX.py` where `XX` is zero-padded day number
        - Expects each solution module to have a `Solution` class
        - Solution modules should be in the `solutions` package
        - Parameters match those expected by SolutionBase.__init__
    """
    module_name = f"solutions.day{day:02d}"
    solution_module = import_module(module_name)

    solution_class: type[SolutionBase] = solution_module.Solution

    if not issubclass(solution_class, SolutionBase):
        error_message = f"Solution class for day {day} must inherit from SolutionBase"
        raise TypeError(error_message)

    return solution_class(
        day=day, part_num=part, is_raw=raw, skip_test=skip_test, benchmark=benchmark
    )
