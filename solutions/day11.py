"""Day 11: Plutonian Pebbles.

This module provides the solution for Advent of Code 2024 - Day 11.
It handles transforming sequences of numbers (stones) according to specific rules
over multiple iterations (blinks).

Each stone undergoes one of three transformations based on its characteristics:
- Conversion to 1 if it's a single zero
- Splitting in half if even-length
- Multiplication by 2024 if odd-length

The module contains a Solution class that inherits from SolutionBase and implements
methods to process stone transformations and calculate the total number of stones
after specified iterations.
"""

from collections import Counter

from aoc.models.base import SolutionBase


class Solution(SolutionBase):
    """Solution for Advent of Code 2024 - Day 11: Plutonian Pebbles.

    Solves puzzles involving stone transformations:
    - Part 1: Calculate total stones after 25 blinks
    - Part 2: Calculate total stones after 75 blinks
    """

    def split_stones(self, stones_data: str, total_blinks: int) -> int:
        """Process stones through multiple iterations of transformations.

        Each stone undergoes one of three transformations in each blink:
        1. If stone is "0", it becomes "1"
        2. If stone length is even, split into two equal parts (removing leading zeros)
        3. If stone length is odd, multiply by 2024

        Args:
            stones_data (str): Space-separated string of initial stone values
            total_blinks (int): Number of transformation iterations to perform

        Returns
        -------
            int: Total number of stones after all transformations are complete
        """
        stones = Counter(stones_data.split())

        for _ in range(total_blinks):
            new_stones: Counter = Counter()
            for stone, count in stones.items():
                if stone == "0":
                    new_stones["1"] += count

                elif len(stone) % 2 == 0:
                    midpoint = len(stone) // 2
                    left = stone[:midpoint].lstrip("0") or "0"
                    right = stone[midpoint:].lstrip("0") or "0"

                    new_stones[left] += count
                    new_stones[right] += count

                else:
                    new_stones[str(int(stone) * 2024)] += count

            stones = new_stones

        return sum(stones.values())

    def part1(self, data: list[str]) -> int:
        """Calculate total stones after 25 blinks of transformations.

        Args:
            data (List[str]): Input lines containing the initial stone values

        Returns
        -------
            int: Total number of stones after 25 transformation iterations
        """
        return self.split_stones(data[0], 25)

    def part2(self, data: list[str]) -> int:
        """Calculate total stones after 75 blinks of transformations.

        Args:
            data (List[str]): Input lines containing the initial stone values

        Returns
        -------
            int: Total number of stones after 75 transformation iterations
        """
        return self.split_stones(data[0], 75)
