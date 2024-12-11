from collections import Counter
from typing import List

from aoc.models.base import SolutionBase


class Solution(SolutionBase):
    """Solution for Advent of Code 2024 - Day 11: Plutonian Pebbles.

    This class solves a puzzle involving transforming sequences of numbers (stones)
    according to specific rules over multiple iterations (blinks). Each stone undergoes
    one of three transformations based on its characteristics: conversion to 1 if it's
    a single zero, splitting in half if even-length, or multiplication by 2024 if odd-length.

    Input format:
        List containing a single string of space-separated numbers representing the initial
        stone values. Each value is a non-negative integer represented as a string.

    This class inherits from `SolutionBase` and provides methods to process stone
    transformations and calculate the total number of stones after a specified number
    of iterations.
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

        Returns:
            int: Total number of stones after all transformations are complete
        """
        stones = Counter(stones_data.split())
        blinks = 1

        while blinks <= total_blinks:
            new_stones = Counter()
            for stone, count in stones.items():
                if len(stone) == 1 and stone == "0":
                    new_stones["1"] += count

                elif len(stone) % 2 == 0:
                    midpoint = len(stone) // 2
                    left = str(int(stone[:midpoint])) if stone[:midpoint] else "0"
                    right = str(int(stone[midpoint:])) if stone[midpoint:] else "0"

                    new_stones[left] += count
                    new_stones[right] += count

                else:
                    new_stones[str(int(stone) * 2024)] += count

            stones = new_stones
            blinks += 1

        return sum(stones.values())

    def part1(self, data: List[str]) -> int:
        """Calculate total stones after 25 blinks of transformations.

        Args:
            data (List[str]): Input lines containing the initial stone values

        Returns:
            int: Total number of stones after 25 transformation iterations
        """
        return self.split_stones(data[0], 25)

    def part2(self, data: List[str]) -> int:
        """Calculate total stones after 75 blinks of transformations.

        Args:
            data (List[str]): Input lines containing the initial stone values

        Returns:
            int: Total number of stones after 75 transformation iterations
        """
        return self.split_stones(data[0], 75)
