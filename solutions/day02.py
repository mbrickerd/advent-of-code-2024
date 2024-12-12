from typing import List

from aoc.models.base import SolutionBase


class Solution(SolutionBase):
    """Solution for Advent of Code 2024 - Day 2: Red-Nosed Reports.

    This class solves a puzzle involving analysis of numeric sequences. Part 1 identifies
    sequences that are strictly increasing or decreasing with adjacent number differences
    between 1 and 3. Part 2 extends this by also considering sequences where removing one
    number creates a valid sequence.

    This class inherits from `SolutionBase` and provides methods to analyze numerical
    sequences for monotonicity and value range constraints.
    """

    def is_increasing(self, ls: List[int]) -> bool:
        """Check if a sequence is strictly increasing.

        Args:
            ls (List[int]): A list of integers to check
                (e.g., [1, 2, 4, 7]).

        Returns:
            bool: True if each number is strictly greater than the previous number,
                False otherwise. For example:
                - [1, 2, 3] returns True
                - [1, 2, 2] returns False
                - [1, 3, 2] returns False
        """
        return all(x < y for x, y in zip(ls, ls[1:]))

    def is_decreasing(self, ls: List[int]) -> bool:
        """Check if a sequence is strictly decreasing.

        Args:
            ls (List[int]): A list of integers to check
                (e.g., [7, 4, 2, 1]).

        Returns:
            bool: True if each number is strictly less than the previous number,
                False otherwise. For example:
                - [3, 2, 1] returns True
                - [3, 2, 2] returns False
                - [3, 1, 2] returns False
        """
        return all(x > y for x, y in zip(ls, ls[1:]))

    def abs_differences(self, ls: List[int]) -> List[int]:
        """Calculate absolute differences between adjacent numbers in a sequence.

        Args:
            ls (List[int]): A list of integers to process
                (e.g., [1, 3, 5, 7]).

        Returns:
            List[int]: A list of absolute differences between consecutive numbers.
                For example:
                - [1, 3, 6] returns [2, 3]
                - [5, 2, 4] returns [3, 2]
        """
        return [abs(x - y) for x, y in zip(ls, ls[1:])]

    def between_range(self, ls: List[int]) -> bool:
        """Check if all adjacent number differences are between 1 and 3 inclusive.

        Args:
            ls (List[int]): A list of integers to check
                (e.g., [1, 3, 5, 7]).

        Returns:
            bool: True if all differences between adjacent numbers are between 1 and 3
                inclusive, False otherwise. For example:
                - [1, 3, 5] returns True (differences: 2, 2)
                - [1, 5, 6] returns False (first difference is 4)
        """
        return all(1 <= x <= 3 for x in self.abs_differences(ls))

    def part1(self, data: List[str]) -> int:
        """Count sequences that are monotonic and have valid differences.

        Counts sequences that are either strictly increasing or strictly decreasing,
        and where all adjacent number differences are between 1 and 3 inclusive.

        Args:
            data (List[str]): A list of strings, where each string contains
                space-separated integers (e.g., ["1 3 5", "7 4 2"]).

        Returns:
            int: The count of valid sequences that satisfy both the monotonicity
                and difference range requirements.
        """
        return sum(
            [
                1
                for ls in [list(map(int, line.split())) for line in data]
                if (self.is_increasing(ls) or self.is_decreasing(ls)) and self.between_range(ls)
            ]
        )

    def part2(self, data: List[str]) -> int:
        """Count sequences that are valid or become valid after removing one number.

        Counts sequences that either (1) are valid according to part1 criteria, or
        (2) become valid when exactly one number is removed from the sequence

        Args:
            data (List[str]): A list of strings, where each string contains
                space-separated integers (e.g., ["1 3 2 5", "7 4 5 2"]).

        Returns:
            int: The count of sequences that are either valid originally or become
                valid after removing exactly one number.
        """
        return sum(
            any(
                (
                    self.is_increasing(ls[:i] + ls[i + 1 :])
                    or self.is_decreasing(ls[:i] + ls[i + 1 :])
                )
                and self.between_range(ls[:i] + ls[i + 1 :])
                for i in range(len(ls))
            )
            or ((self.is_increasing(ls) or self.is_decreasing(ls)) and self.between_range(ls))
            for ls in [list(map(int, line.split())) for line in data]
        )
