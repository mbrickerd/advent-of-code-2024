"""Day 2: Red-Nosed Reports.

This module provides the solution for Advent of Code 2024 - Day 2.
It handles analysis of numeric sequences with specific monotonicity and
difference constraints.

The module contains a Solution class that inherits from SolutionBase and implements
methods to check if sequences are strictly increasing/decreasing and if differences
between adjacent values fall within required ranges.
"""

from collections.abc import Iterable
import functools
import itertools
from typing import TypeVar

from aoc.models.base import SolutionBase


T = TypeVar("T")


class Solution(SolutionBase):
    """Analyze numeric sequences for monotonicity and difference constraints.

    This solution identifies sequences that follow specific patterns:
    Part 1 finds strictly increasing/decreasing sequences with adjacent
    differences between 1 and 3.
    Part 2 extends this to include sequences where removing one number
    creates a valid sequence.
    """

    def is_increasing(self, ls: list[int]) -> bool:
        """Check if a sequence is strictly increasing.

        Args:
            ls: A list of integers to check.

        Returns
        -------
            True if each number is strictly greater than the previous number,
            False otherwise.
        """
        return all(x < y for x, y in itertools.pairwise(ls))

    def is_decreasing(self, ls: list[int]) -> bool:
        """Check if a sequence is strictly decreasing.

        Args:
            ls: A list of integers to check.

        Returns
        -------
            True if each number is strictly less than the previous number,
            False otherwise.
        """
        return all(x > y for x, y in itertools.pairwise(ls))

    def abs_differences(self, ls: list[int]) -> list[int]:
        """Calculate absolute differences between adjacent numbers in a sequence.

        Args:
            ls: A list of integers to process.

        Returns
        -------
            A list of absolute differences between consecutive numbers.
        """
        return [abs(x - y) for x, y in itertools.pairwise(ls)]

    def between_range(self, ls: list[int]) -> bool:
        """Check if all adjacent number differences are between 1 and 3 inclusive.

        Args:
            ls: A list of integers to check.

        Returns
        -------
            True if all differences between adjacent numbers are between 1 and 3
            inclusive, False otherwise.
        """
        return all(1 <= abs(x - y) <= 3 for x, y in itertools.pairwise(ls))

    def is_valid_sequence(self, ls: Iterable[int]) -> bool:
        """Check if a sequence meets all validity criteria.

        Args:
            ls: An iterable of integers to check.

        Returns
        -------
            True if the sequence is valid (monotonic with proper differences),
            False otherwise.
        """
        # Convert to list to ensure we can use it multiple times
        ls_list = list(ls)
        return (self.is_increasing(ls_list) or self.is_decreasing(ls_list)) and self.between_range(
            ls_list
        )

    @staticmethod
    @functools.lru_cache(maxsize=128)
    def _cached_is_valid(sequence: tuple[int, ...]) -> bool:
        """Validate a sequence with caching for performance.

        Args:
            sequence: A tuple of integers.

        Returns
        -------
            True if the sequence is valid, False otherwise.
        """
        # Check if sequence is increasing or decreasing
        is_increasing = all(x < y for x, y in itertools.pairwise(sequence))
        is_decreasing = all(x > y for x, y in itertools.pairwise(sequence))

        # Check differences within range
        differences_in_range = all(1 <= abs(x - y) <= 3 for x, y in itertools.pairwise(sequence))

        return (is_increasing or is_decreasing) and differences_in_range

    def part1(self, data: list[str]) -> int:
        """Count sequences that are monotonic and have valid differences.

        Counts sequences that are either strictly increasing or strictly decreasing,
        and where all adjacent number differences are between 1 and 3 inclusive.

        Args:
            data: A list of strings, where each string contains space-separated integers.

        Returns
        -------
            The count of valid sequences that satisfy both the monotonicity
            and difference range requirements.
        """
        valid_count = 0
        for line in data:
            sequence = tuple(map(int, line.split()))
            if self._cached_is_valid(sequence):
                valid_count += 1

        return valid_count

    def part2(self, data: list[str]) -> int:
        """Count sequences that are valid or become valid after removing one number.

        Counts sequences that either (1) are valid according to part1 criteria, or
        (2) become valid when exactly one number is removed from the sequence.

        Args:
            data: A list of strings, where each string contains space-separated integers.

        Returns
        -------
            The count of sequences that are either valid originally or become
            valid after removing exactly one number.
        """
        valid_count = 0

        for line in data:
            sequence = tuple(map(int, line.split()))

            # Check if original sequence is valid
            if self._cached_is_valid(sequence):
                valid_count += 1
                continue

            # Check if removing one element makes it valid
            if any(
                self._cached_is_valid(sequence[:i] + sequence[i + 1 :])
                for i in range(len(sequence))
            ):
                valid_count += 1

        return valid_count
