"""Day 19: Linen Layout.

This module provides the solution for Advent of Code 2024 - Day 19.
It solves a puzzle about arranging towels with colored stripe patterns,
determining which sequences are possible to create and counting
the total number of unique ways to arrange towels for each sequence.
"""

from aoc.models.base import SolutionBase


class Solution(SolutionBase):
    """Solution for Advent of Code 2024 - Day 19: Linen Layout.

    This class solves a puzzle about arranging towels with colored stripe patterns.
    Part 1 determines which sequences are possible to create, while Part 2 counts
    the total number of unique ways to arrange towels for each sequence.

    Input format:
        - First line: comma-separated list of available towel patterns
        - Blank line
        - Remaining lines: sequences to match using available patterns
    """

    def parse_data(self, data: list[str]) -> tuple[list[str], list[str]]:
        """Parse input data into towel patterns and target sequences.

        Args:
            data: Raw input lines

        Returns
        -------
            Tuple of (towel patterns, sequences to match)
        """
        raw_data = "\n".join(data)
        parts = raw_data.split("\n\n")
        towels = parts[0].split(", ")
        sequences = [row for row in parts[1].split("\n") if row]
        return towels, sequences

    def count_ways(self, seq: str, towels: list[str], cache: dict[str, int]) -> int:
        """Count number of unique ways to arrange towels to match a sequence.

        Uses dynamic programming with memoization to efficiently count arrangements.

        Args:
            seq: Target sequence to match
            towels: Available towel patterns
            cache: Memoization cache

        Returns
        -------
            Number of unique ways to arrange towels to match sequence
        """
        if not seq:
            return 1

        if seq in cache:
            return cache[seq]

        total = 0
        for towel in towels:
            if seq.startswith(towel):
                total += self.count_ways(seq[len(towel) :], towels, cache)

        cache[seq] = total
        return total

    def part1(self, data: list[str]) -> int:
        """Count possible towel pattern sequences.

        Determines how many target sequences can be created using available towel patterns.

        Args:
            data: Input data containing towel patterns and target sequences

        Returns
        -------
            Number of sequences that can be created
        """
        towels, sequences = self.parse_data(data)
        cache: dict[str, int] = {}

        return sum(1 for seq in sequences if self.count_ways(seq, towels, cache) > 0)

    def part2(self, data: list[str]) -> int:
        """Sum all possible arrangement combinations across sequences.

        Calculates the total number of unique ways to arrange towels for all sequences.

        Args:
            data: Input data containing towel patterns and target sequences

        Returns
        -------
            Total sum of possible arrangement combinations
        """
        towels, sequences = self.parse_data(data)
        cache: dict[str, int] = {}

        return sum(self.count_ways(seq, towels, cache) for seq in sequences)
