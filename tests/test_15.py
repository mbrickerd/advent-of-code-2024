"""Test suite for Day 15: Warehouse Woes.

This module contains tests for the Day 15 solution, which handles moving boxes
in a warehouse using directional commands. The tests verify:
1. Part 1: Moving single boxes
2. Part 2: Moving connected box pairs
"""

from aoc.models.tester import TestSolutionUtility


def test_day15_part1() -> None:
    """Test calculating score after moving single boxes.

    Verifies that the solution correctly simulates box movement in the warehouse
    according to directional commands, where each non-'#' character represents
    a box that can be pushed. The score is calculated based on final box positions.
    """
    TestSolutionUtility.run_test(
        day=15,
        is_raw=False,
        part_num=1,
        expected=10092,
    )


def test_day15_part2() -> None:
    """Test calculating score after moving connected box pairs.

    Verifies that the solution correctly simulates movement of connected box pairs
    in the warehouse according to directional commands, handling the additional
    complexity of boxes that must move together. The score is calculated based on
    final box positions.
    """
    TestSolutionUtility.run_test(
        day=15,
        is_raw=False,
        part_num=2,
        expected=9021,
    )
