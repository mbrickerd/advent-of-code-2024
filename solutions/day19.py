from typing import Dict, List, Tuple

from aoc.models.base import SolutionBase


class TowelSorter:
    """Solution helper for arranging towel patterns.

    This class processes towel arrangements where each towel has a specific pattern of
    colored stripes. It determines whether sequences can be created using available
    towel patterns and counts the number of unique ways to arrange towels to match
    desired sequences.

    Attributes:
        towels (List[str]): Available towel patterns
        sequences (List[str]): Desired stripe sequences to match
        cache (Dict[str, int]): Memoization cache for sequence arrangements
    """

    def __init__(self, towels: List[str], sequences: List[str]) -> None:
        """Initialize TowelSorter with available patterns and target sequences.

        Args:
            towels (List[str]): List of available towel patterns
            sequences (List[str]): List of sequences to match
        """
        self.towels = towels
        self.sequences = sequences
        self.cache: Dict[str, int] = {}

    def count_ways(self, seq: str) -> int:
        """Count number of unique ways to arrange towels to match a sequence.

        Uses dynamic programming with memoization to efficiently count arrangements
        without building complete arrangement lists.

        Args:
            seq (str): Target sequence to match

        Returns:
            int: Number of unique ways to arrange towels to match sequence
        """
        if not seq:
            return 1

        if seq in self.cache:
            return self.cache[seq]

        total = 0
        for towel in self.towels:
            if seq.startswith(towel):
                total += self.count_ways(seq[len(towel) :])

        self.cache[seq] = total
        return total

    def is_possible(self, seq: str) -> bool:
        """Check if a sequence can be created using available towel patterns.

        Args:
            seq (str): Sequence to check

        Returns:
            bool: True if sequence can be created, False otherwise
        """
        return self.count_ways(seq) > 0

    def part1(self) -> int:
        """Count how many sequences are possible with available towel patterns.

        Returns:
            int: Number of sequences that can be created
        """
        return sum(1 for seq in self.sequences if self.is_possible(seq))

    def part2(self) -> int:
        """Sum up the number of unique ways each sequence can be created.

        Returns:
            int: Total number of possible arrangements across all sequences
        """
        return sum(self.count_ways(seq) for seq in self.sequences)


class Solution(SolutionBase):
    """Solution for Advent of Code 2023 - Day 19: Linen Layout.

    This class solves a puzzle about arranging towels with colored stripe patterns.
    Part 1 determines which sequences are possible to create, while Part 2 counts
    the total number of unique ways to arrange towels for each sequence.

    Input format:
        - First line: comma-separated list of available towel patterns
        - Blank line
        - Remaining lines: sequences to match using available patterns

    This class inherits from `SolutionBase` and provides methods to parse input data,
    check sequence possibility, and count unique arrangements.
    """

    def parse_data(self, data: List[str]) -> Tuple[List[str], List[str]]:
        """Parse input data into towel patterns and target sequences.

        Args:
            data (List[str]): Raw input lines

        Returns:
            Tuple[List[str], List[str]]: Tuple of (towel patterns, sequences to match)
        """
        towels, seq = "\n".join(data).split("\n\n")
        return towels.split(", "), [row for row in seq.split("\n") if row]

    def part1(self, data: List[str]) -> int:
        """Count possible towel pattern sequences.

        This method determines how many of the target sequences can be created using
        the available towel patterns. A sequence is possible if it can be formed by
        combining one or more of the available towel patterns in any order. The method
        uses a TowelSorter helper class to analyze each sequence and count those that
        are possible to create.

        Args:
            data (List[str]): Input data containing towel patterns and target sequences.
                First line has comma-separated patterns, followed by a blank line, then
                target sequences.

        Returns:
            int: Number of sequences that can be created using the available towel patterns.
        """
        towels, seq = self.parse_data(data)
        towel_sorter = TowelSorter(towels, seq)
        return towel_sorter.part1()

    def part2(self, data: List[str]) -> int:
        """Sum all possible arrangement combinations across sequences.

        This method calculates the total number of unique ways to arrange towels to match
        each target sequence. For each sequence, it counts how many different combinations
        of the available towel patterns can create that sequence. The final result is the
        sum of possible arrangements across all sequences, using dynamic programming to
        handle overlapping subproblems efficiently.

        Args:
            data (List[str]): Input data containing towel patterns and target sequences.
                First line has comma-separated patterns, followed by a blank line, then
                target sequences.

        Returns:
            int: Total sum of possible arrangement combinations for all sequences.
        """
        towels, seq = self.parse_data(data)
        towel_sorter = TowelSorter(towels, seq)
        return towel_sorter.part2()
