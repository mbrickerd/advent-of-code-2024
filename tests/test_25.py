"""Test suite for Day 25: Code Chronicle.

This module contains tests for the Day 25 solution, which analyzes lock and key
combinations to determine valid pairings. The tests verify:
1. Part 1: Counting the number of valid lock-key pairs
"""

from aoc.models.tester import TestSolutionUtility


def test_day25_part1() -> None:
    """Test counting the number of valid lock-key pairs.

    Verifies that the solution correctly parses lock and key patterns, computes
    their height profiles (count of '#' symbols per column), and determines how
    many combinations satisfy the opening criteria (combined height ≤ 5 for each
    column).

    The algorithm:
    1. Separates input into lock and key patterns
    2. Converts each pattern into a height profile
    3. Tests each lock-key combination against the criteria
    """
    TestSolutionUtility.run_test(
        day=25,
        is_raw=False,
        part_num=1,
        expected=3,
    )
