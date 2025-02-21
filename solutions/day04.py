"""Day 4: Ceres Search.

This module provides the solution for Advent of Code 2024 - Day 4.
It implements pattern searching algorithms in 2D character grids.

The module contains a Solution class that inherits from SolutionBase and implements
methods to search for "XMAS" patterns and X-shaped "MAS" patterns in a grid.
"""

from functools import lru_cache
from typing import ClassVar

from aoc.models.base import SolutionBase


class Solution(SolutionBase):
    """Search for text patterns in 2D grids.

    This solution implements directional pattern searching algorithms:
    - Part 1: Find "XMAS" in any of 8 directions (horizontal, vertical, diagonal)
    - Part 2: Locate X-shaped patterns where two "MAS" sequences cross at their 'A's
    """

    DIRECTIONS: ClassVar[list[tuple[int, int]]] = [
        (0, 1),  # right
        (1, 1),  # down-right
        (1, 0),  # down
        (1, -1),  # down-left
        (0, -1),  # left
        (-1, -1),  # up-left
        (-1, 0),  # up
        (-1, 1),  # up-right
    ]

    @staticmethod
    @lru_cache(maxsize=256)
    def _check_pattern(data: tuple, row: int, col: int, dr: int, dc: int, pattern: str) -> bool:
        """Check if a pattern exists from a point in a direction (cached).

        Args:
            data: 2D grid as tuple of strings
            row: Starting row coordinate
            col: Starting column coordinate
            dr: Row direction (-1, 0, or 1)
            dc: Column direction (-1, 0, or 1)
            pattern: The text pattern to search for

        Returns
        -------
            True if pattern exists in the specified direction
        """
        rows, cols = len(data), len(data[0])

        return all(
            0 <= row + i * dr < rows
            and 0 <= col + i * dc < cols
            and data[row + i * dr][col + i * dc] == pattern[i]
            for i in range(len(pattern))
        )

    def part1(self, data: list[str]) -> int:
        """Count occurrences of "XMAS" in all 8 directions.

        Args:
            data: 2D grid represented as list of strings

        Returns
        -------
            Total number of "XMAS" patterns found
        """
        rows, cols = len(data), len(data[0])
        data_tuple = tuple(data)
        count = 0

        for row in range(rows):
            for col in range(cols):
                if data[row][col] != "X":
                    continue

                for dr, dc in self.DIRECTIONS:
                    if self._check_pattern(data_tuple, row, col, dr, dc, "XMAS"):
                        count += 1

        return count

    def part2(self, data: list[str]) -> int:
        """Count X-shaped patterns formed by two crossing "MAS" sequences.

        Args:
            data: 2D grid represented as list of strings

        Returns
        -------
            Number of valid X patterns found
        """
        rows, cols = len(data), len(data[0])
        data_tuple = tuple(data)
        count = 0

        for row in range(1, rows - 1):
            for col in range(1, cols - 1):
                if data[row][col] != "A":
                    continue

                nw_to_se = self._check_pattern(
                    data_tuple, row - 1, col - 1, 1, 1, "MAS"
                ) or self._check_pattern(data_tuple, row + 1, col + 1, -1, -1, "MAS")

                if nw_to_se:
                    ne_to_sw = self._check_pattern(
                        data_tuple, row - 1, col + 1, 1, -1, "MAS"
                    ) or self._check_pattern(data_tuple, row + 1, col - 1, -1, 1, "MAS")

                    if ne_to_sw:
                        count += 1

        return count
