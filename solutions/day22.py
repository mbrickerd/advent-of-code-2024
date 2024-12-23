from collections import defaultdict
from typing import List

from aoc.models.base import SolutionBase


class Solution(SolutionBase):
    """Solution for Advent of Code 2024 - Day 22: Monkey Market.

    This class solves a puzzle about analyzing secret codes and price patterns in a
    monkey marketplace. Part 1 calculates transformed secret values, while Part 2
    analyzes price change patterns to find the most profitable trading opportunities.

    Input format:
        - List of integers, one per line
        - Each integer represents an initial secret code or starting price
        - Values are transformed through a series of mathematical operations
        - In Part 2, transformed values are used to generate price sequences

    This class inherits from `SolutionBase` and provides methods to transform secret
    codes and analyze price patterns in the monkey marketplace.
    """

    def part1(self, data: List[str]) -> int:
        """Calculate the sum of transformed secret codes.

        Processes each input value through 2000 rounds of transformations using
        a specific sequence of mathematical operations:
        1. Multiply by 64 and XOR with original
        2. Integer divide by 32 and XOR with result
        3. Multiply by 2048 and XOR with result
        All operations are performed modulo 16777216.

        Args:
            data: List of strings containing initial secret codes

        Returns:
            Sum of all final transformed secret values
        """
        secrets = []
        for secret in map(int, data):
            for _ in range(2000):
                secret = ((secret * 64) ^ secret) % 16777216
                secret = ((secret // 32) ^ secret) % 16777216
                secret = ((secret * 2048) ^ secret) % 16777216

            secrets.append(secret)

        return sum(secrets)

    def part2(self, data: List[str]) -> int:
        """Find the highest value pattern in price sequences.

        Generates price sequences for each input value using the same transformation
        sequence as part1, but additionally:
        1. Takes modulo 10 of each transformed value to get price digits
        2. Analyzes sequences of 4 consecutive price changes
        3. Tracks the frequency of price patterns for each buyer
        4. Finds the pattern that leads to the highest subsequent price

        Args:
            data: List of strings containing initial secret codes

        Returns:
            Maximum price value associated with any 4-change pattern
        """
        prices = []
        for secret in map(int, data):
            price = []
            for _ in range(2000):
                secret = ((secret * 64) ^ secret) % 16777216
                secret = ((secret // 32) ^ secret) % 16777216
                secret = ((secret * 2048) ^ secret) % 16777216
                price.append(secret % 10)

            prices.append(price)

        changes = [[b - a for a, b in zip(p, p[1:])] for p in prices]
        amounts = defaultdict(int)

        for buyer_idx, change in enumerate(changes):
            keys = set()
            for i in range(len(change) - 3):
                key = tuple(change[i : i + 4])
                if key in keys:
                    continue

                amounts[key] += prices[buyer_idx][i + 4]
                keys.add(key)

        return max(amounts.values())
