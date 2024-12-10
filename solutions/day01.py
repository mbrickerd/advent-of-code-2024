from collections import Counter
from typing import List, Tuple

from aoc.models.base import SolutionBase


class Solution(SolutionBase):
    """Solution for Advent of Code 2024 - Day 1: Historian Hysteria.

    This class solves a puzzle involving processing pairs of numbers that represent historical
    data points requiring comparison and reconciliation. Part 1 calculates a total disparity
    between sorted parallel datasets, while Part 2 handles frequency-weighted matches between
    the datasets.

    This class inherits from `SolutionBase` and provides methods to load, compare,
    and perform calculations on paired lists of integers from string input data.
    """

    def load_lists(self, data: List[str]) -> Tuple[List[int], List[int]]:
        """Convert input strings into two parallel lists of integers.

        Takes a list of strings where each string contains two space-separated integers
        and converts them into two separate lists of integers.

        Args:
            data (List[str]): A list of strings, where each string contains two
                space-separated integers (e.g., ["1 2", "3 4", "5 6"]).

        Returns:
            Tuple[List[int], List[int]]: A tuple containing:
                - First list (List[int]): Contains all first numbers from each input line
                - Second list (List[int]): Contains all second numbers from each input line
                Example: For input ["1 2", "3 4"], returns ([1, 3], [2, 4])
        """
        return map(list, zip(*(map(int, line.split()) for line in data)))

    def part1(self, data: List[str]) -> int:
        """Calculate the sum of absolute differences between sorted parallel lists.

        Loads two lists from the input data, sorts them independently, and calculates
        the sum of absolute differences between corresponding elements.

        Args:
            data (List[str]): A list of strings, where each string contains two
                space-separated integers (e.g., ["1 2", "3 4", "5 6"]).

        Returns:
            int: The sum of absolute differences between corresponding elements
                in the sorted lists. For example, if the sorted lists are [1, 2, 3]
                and [2, 3, 5], returns |1-2| + |2-3| + |3-5| = 4.
        """
        ls1, ls2 = self.load_lists(data)
        ls1.sort(), ls2.sort()

        return sum([abs(ls1[i] - ls2[i]) for i in range(len(data))])

    def part2(self, data: List[str]) -> int:
        """Calculate the sum of products between matching elements.

        Loads two lists from the input data, converts the second list to a Counter dictionary,
        and calculates the sum of products between elements that appear in both lists,
        weighted by their frequency in the second list.

        Args:
            data (List[str]): A list of strings, where each string contains two
                space-separated integers (e.g., ["1 2", "3 4", "5 2"]).

        Returns:
            int: The sum of products between matching elements, weighted by their frequency
                in the second list. For example, if ls1=[1, 2, 3] and ls2=[2, 2, 4],
                and 2 appears twice in ls2, then for the element 2 in ls1,
                it contributes 2 * 2 to the sum.
        """
        ls1, ls2 = self.load_lists(data)
        ls2 = dict(Counter(ls2))

        return sum([item * ls2[item] for item in ls1 if item in ls2.keys()])
