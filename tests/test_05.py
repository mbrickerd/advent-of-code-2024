"""Test suite for Day 5: Print Queue.

This module contains tests for the Day 5 solution, which processes print job
ordering challenges according to specific sequencing rules. The tests verify:
1. Part 1: Finding valid print orders and summing their middle pages
2. Part 2: Fixing invalid print orders and summing their middle pages
"""

from aoc.models.tester import TestSolutionUtility


def test_day05_part1() -> None:
    """Test summing middle pages from valid print orders.

    Verifies that the solution correctly identifies print orders that satisfy
    all sequencing rules and calculates the sum of their middle page numbers.
    """
    TestSolutionUtility.run_test(
        day=5,
        is_raw=False,
        part_num=1,
        expected=143,
    )


def test_day05_part2() -> None:
    """Test summing middle pages from fixed invalid print orders.

    Verifies that the solution correctly fixes invalid print orders by
    reordering pages to satisfy all sequencing rules, then calculates
    the sum of middle page numbers from these fixed orders.
    """
    TestSolutionUtility.run_test(
        day=5,
        is_raw=False,
        part_num=2,
        expected=123,
    )
