"""Test suite for Day 11: Plutonian Pebbles.

This module contains tests for the Day 11 solution, which handles transforming
sequences of numbers (stones) according to specific rules over multiple iterations.
The tests verify:
1. Part 1: Calculating total stones after 25 blinks of transformations
"""

from aoc.models.tester import TestSolutionUtility


def test_day11_part1() -> None:
    """Test calculating total stones after 25 blinks of transformations.

    Verifies that the solution correctly processes stones through 25 iterations
    of transformations, where each stone follows specific rules:
    1. If stone is "0", it becomes "1"
    2. If stone length is even, split into two equal parts
    3. If stone length is odd, multiply by 2024
    """
    TestSolutionUtility.run_test(
        day=11,
        is_raw=False,
        part_num=1,
        expected=55312,
    )
