
from aoc.models.base import SolutionBase


class Solution(SolutionBase):
    """Solution for Advent of Code 2024 - Day 25: Code Chronicle.

    This class solves a puzzle about analyzing lock and key combinations to determine
    valid pairings. Each lock and key is represented as a pattern of symbols, and
    the solution counts how many lock-key pairs will successfully open based on their
    combined patterns.

    Input format:
        - Multiple blocks separated by blank lines
        - Each block represents either a lock or a key pattern
        - Locks have 5 '#' symbols in their first row
        - Keys have a different number of '#' symbols in their first row
        - Each pattern consists of '#' and other symbols arranged in a grid

    The challenge involves analyzing the height profiles of locks and keys
    to determine which combinations will successfully open.
    """

    def part1(self, data: list[str]) -> int:
        """Count the number of valid lock-key pairs.

        Parses the input to extract lock and key patterns, computes their height
        profiles, and then determines how many combinations satisfy the opening
        criteria (combined height ≤ 5 for each column).

        The algorithm works by:
        1. Separating the input into individual lock and key patterns
        2. Converting each pattern into a height profile (count of '#' symbols per column)
        3. Testing each lock-key combination to see if their combined profiles meet the criteria

        Args:
            data: List of strings containing lock and key patterns separated by blank lines

        Returns
        -------
            Integer count of valid lock-key combinations that will successfully open
        """
        data = "\n".join(data).split("\n\n")
        locks = []
        keys = []

        for item in data:
            item = item.split("\n")
            cols = [[row[c] for row in item] for c in range(len(item[0]))]
            heights = [col.count("#") - 1 for col in cols]

            if item[0].count("#") == 5:
                locks.append(heights)
            else:
                keys.append(heights)

        count = sum(
            all(c <= 5 for c in [a + b for a, b in zip(lock, key, strict=False)])
            for lock in locks
            for key in keys
        )
        return count
