"""Day 1: Historian Hysteria.

This module provides the solution for Advent of Code 2024 - Day 1.
It handles processing and comparing pairs of historical data points.

The module contains a Solution class that inherits from SolutionBase and implements
methods to load integer pairs from input strings and perform calculations for both
parts of the puzzle.
"""

from collections import Counter

from aoc.models.base import SolutionBase


class Solution(SolutionBase):
    """Process historical data pairs for comparison and reconciliation.

    This solution handles pairs of numbers representing historical data points.
    Part 1 calculates total disparity between sorted parallel datasets.
    Part 2 handles frequency-weighted matches between datasets.
    """

    def load_lists(self, data: list[str]) -> tuple[list[int], list[int]]:
        """Convert input strings into two parallel lists of integers.

        Args:
            data: A list of strings, each containing two space-separated integers
                (e.g., ["1 2", "3 4", "5 6"]).

        Returns
        -------
            A tuple containing two lists of integers:
                - First list containing all first numbers from each input line
                - Second list containing all second numbers from each input line
        """
        ls1, ls2 = map(list, zip(*(map(int, line.split()) for line in data), strict=False))
        return ls1, ls2

    def part1(self, data: list[str]) -> int:
        """Calculate sum of absolute differences between sorted parallel lists.

        Loads two lists from input data, sorts them independently, and calculates
        the sum of absolute differences between corresponding elements.

        Args:
            data: A list of strings, each containing two space-separated integers.

        Returns
        -------
            The sum of absolute differences between corresponding elements
            in the sorted lists.
        """
        ls1, ls2 = self.load_lists(data)
        ls1.sort()
        ls2.sort()

        return sum(abs(ls1[i] - ls2[i]) for i in range(len(ls1)))

    def part2(self, data: list[str]) -> int:
        """Calculate sum of products between matching elements.

        Loads two lists from input data, converts second list to a Counter,
        and calculates sum of products between elements appearing in both lists,
        weighted by their frequency in the second list.

        Args:
            data: A list of strings, each containing two space-separated integers.

        Returns
        -------
            Sum of products between matching elements, weighted by frequency
            in the second list.
        """
        ls1, ls2 = self.load_lists(data)
        frequency_map = Counter(ls2)

        return sum(item * frequency_map[item] for item in ls1 if item in frequency_map)
