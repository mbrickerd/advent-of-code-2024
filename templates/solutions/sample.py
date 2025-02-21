"""Boilerplate solution template for Advent of Code daily challenges.

This module provides a template class for solving Advent of Code puzzle problems.
It includes a base structure with two method stubs (part1 and part2) that can be
implemented for specific day's challenges.

The template follows the SolutionBase pattern used across the Advent of Code solutions,
allowing for consistent handling of input parsing and solution execution.
"""

from aoc.models.base import SolutionBase


class Solution(SolutionBase):
    """Solution template for Advent of Code daily puzzle.

    This class provides a standardized structure for implementing solutions to
    daily Advent of Code challenges. It inherits from SolutionBase and includes
    method stubs for part1 and part2 of the puzzle.

    Subclasses should override these methods with specific implementation logic
    for parsing input and solving the puzzle requirements.
    """

    def part1(self, data: list[str]) -> int:
        """Solve the first part of the daily puzzle.

        Args:
            data: List of input strings to be processed

        Returns
        -------
            int: Solution for part 1 of the puzzle
        """
        return 0

    def part2(self, data: list[str]) -> int:
        """Solve the second part of the daily puzzle.

        Args:
            data: List of input strings to be processed

        Returns
        -------
            int: Solution for part 2 of the puzzle
        """
        return 0
