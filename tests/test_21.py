"""Test suite for Day 21: Keypad Conundrum.

This module contains tests for the Day 21 solution, which solves puzzles about
robots translating movement codes on keypads. The tests verify:
1. Part 1: Calculating movement complexity with 2-robot chains
2. Part 2: Calculating movement complexity with 25-robot chains
"""

from aoc.models.tester import TestSolutionUtility


def test_day21_part1() -> None:
    """Test calculating total complexity with 2-robot chains.

    Verifies that the solution correctly processes each code using a chain of
    2 robots, where each robot translates the movements of the previous robot.
    Complexity is calculated as the product of the minimum moves required and
    the numeric part of each code.
    """
    TestSolutionUtility.run_test(
        day=21,
        is_raw=False,
        part_num=1,
        expected=126384,
    )


def test_day21_part2() -> None:
    """Test calculating total complexity with 25-robot chains.

    Verifies that the solution correctly processes each code using a chain of
    25 robots instead of 2, resulting in more complex movement translations.
    Complexity is still calculated as the product of minimum moves required
    and the numeric part of each code.
    """
    TestSolutionUtility.run_test(
        day=21,
        is_raw=False,
        part_num=2,
        expected=154115708116294,
    )
