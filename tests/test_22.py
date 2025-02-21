"""Test suite for Day 22: Monkey Market.

This module contains tests for the Day 22 solution, which analyzes secret codes
and price patterns in a monkey marketplace. The tests verify:
1. Part 1: Calculating transformed secret values
2. Part 2: Analyzing price change patterns to find profitable trading opportunities
"""

from aoc.models.tester import TestSolutionUtility


def test_day22_part1() -> None:
    """Test calculating the sum of transformed secret codes.

    Verifies that the solution correctly processes each input value through
    2000 rounds of transformations using a specific sequence of mathematical
    operations:
    1. Multiply by 64 and XOR with original
    2. Integer divide by 32 and XOR with result
    3. Multiply by 2048 and XOR with result
    """
    TestSolutionUtility.run_test(
        day=22,
        is_raw=False,
        part_num=1,
        expected=37327623,
    )


def test_day22_part2() -> None:
    """Test finding the highest value pattern in price sequences.

    Verifies that the solution correctly generates price sequences from transformed
    values, analyzes sequences of 4 consecutive price changes, tracks the frequency
    of price patterns for each buyer, and finds the pattern that leads to the highest
    subsequent price.
    """
    TestSolutionUtility.run_test(
        day=22,
        is_raw=False,
        part_num=2,
        expected=23,
    )
