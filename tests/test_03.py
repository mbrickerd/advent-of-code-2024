"""Test suite for Day 3: Mull It Over.

This module contains tests for the Day 3 solution, which handles parsing and
execution of multiplication and control flow instructions. The tests verify:
1. Part 1: Calculation of the sum of all multiplication operations
2. Part 2: Calculation of the sum of enabled multiplication operations based on
   control flow (do/don't) instructions
"""

from aoc.models.tester import TestSolutionUtility


def test_day03_part1() -> None:
    """Test calculating the sum of all multiplication operations.

    Verifies that the solution correctly parses all multiplication instructions
    in the format `mul(x,y)` and calculates the sum of all these multiplications.
    """
    TestSolutionUtility.run_test(
        day=3,
        is_raw=False,
        part_num=1,
        expected=161,
    )


def test_day03_part2() -> None:
    """Test calculating the sum of enabled multiplication operations.

    Verifies that the solution correctly processes multiplication and control
    flow instructions, only including multiplication operations that occur
    while enabled (between `do()` and `don't()`).
    """
    TestSolutionUtility.run_test(
        day=3,
        is_raw=False,
        part_num=2,
        expected=48,
    )
