"""Test suite for Day 7: Bridge Repair.

This module contains tests for the Day 7 solution, which handles processing
numerical equations for bridge repair calculations. The tests verify:
1. Part 1: Finding valid equations using addition and multiplication
2. Part 2: Finding valid equations using addition, multiplication, and digit concatenation
"""

from aoc.models.tester import TestSolutionUtility


def test_day07_part1() -> None:
    """Test summing totals of valid equations using addition and multiplication.

    Verifies that the solution correctly identifies equations where some
    combination of addition and multiplication operations between sequential
    numbers reaches the target total.
    """
    TestSolutionUtility.run_test(
        day=7,
        is_raw=False,
        part_num=1,
        expected=3749,
    )


def test_day07_part2() -> None:
    """Test summing totals of valid equations with addition, multiplication, and concatenation.

    Verifies that the solution correctly identifies equations where some combination
    of addition, multiplication, and digit concatenation operations between sequential
    numbers reaches the target total without exceeding it.
    """
    TestSolutionUtility.run_test(
        day=7,
        is_raw=False,
        part_num=2,
        expected=11387,
    )
