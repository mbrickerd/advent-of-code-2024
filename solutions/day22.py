"""Advent of Code 2024 - Day 22: Monkey Market.

This module provides the solution for Day 22 of Advent of Code 2024.
It solves a puzzle about analyzing secret codes and price patterns
in a monkey marketplace.
"""

from collections import defaultdict
from itertools import pairwise

from aoc.models.base import SolutionBase


class Solution(SolutionBase):
    """Solution for the Monkey Market puzzle.

    Methods
    -------
        part1: Calculate the sum of transformed secret codes.
        part2: Find the highest value pattern in price sequences.
    """

    rounds: int = 2000

    def transform_secret(self, secret: int) -> int:
        """Transform a secret code through a series of bitwise operations.

        The transformation consists of three steps:
        1. Multiply the secret by 64, XOR with the original secret, and take modulo 16777216.
        2. Integer divide the result by 32, XOR with the previous result, and take modulo 16777216.
        3. Multiply the result by 2048, XOR with the previous result, and take modulo 16777216.

        The modulo operation ensures that the secret code remains within the range [0, 16777215].

        Args:
            secret: The secret code to be transformed.

        Returns
        -------
            The transformed secret code.
        """
        secret = ((secret * 64) ^ secret) % 16777216
        secret = ((secret // 32) ^ secret) % 16777216
        return ((secret * 2048) ^ secret) % 16777216

    def part1(self, data: list[str]) -> int:
        """Calculate the sum of transformed secret codes.

        Processes each input value through the specified number of rounds using the
        `transform_secret` method.

        Args:
            data: List of strings containing initial secret codes.

        Returns
        -------
            Sum of all transformed secret values.
        """
        secrets = []
        for secret in map(int, data):
            for _ in range(self.rounds):
                secret = self.transform_secret(secret)

            secrets.append(secret)

        return sum(secrets)

    def part2(self, data: list[str]) -> int:
        """Find the highest value pattern in price sequences.

        Generates price sequences by applying the `transform_secret` method to each input value
        and taking the modulo 10 of the result to get price digits.

        Analyzes sequences of 4 consecutive price changes and finds the pattern that leads to
        the highest subsequent price.

        Args:
            data: List of strings containing initial secret codes.

        Returns
        -------
            Maximum price value associated with any 4-change pattern.
        """
        prices = []
        for secret in map(int, data):
            price = []
            for _ in range(self.rounds):
                secret = self.transform_secret(secret)
                price.append(secret % 10)

            prices.append(price)

        changes = [[b - a for a, b in pairwise(p)] for p in prices]
        amounts: defaultdict[tuple[int, ...], int] = defaultdict(int)

        for buyer_idx, change in enumerate(changes):
            keys = set()
            for i in range(len(change) - 3):
                key = tuple(change[i : i + 4])
                if key in keys:
                    continue

                amounts[key] += prices[buyer_idx][i + 4]
                keys.add(key)

        return max(amounts.values())
