"""Test suite for Day 6: Guard Gallivant.

This module contains tests for the Day 6 solution, which simulates a guard's
movement through a grid following specific rules. The tests verify:
1. Part 1: Calculation of path length until escape/loop
2. Part 2: Counting possible loops created by adding walls
"""

from aoc.models.tester import TestSolutionUtility


def test_day06_part1() -> None:
    """Test calculating path length until the guard escapes or loops.

    Verifies that the solution correctly simulates guard movement through
    the grid with walls, counting unique positions visited before escaping
    or creating a loop.
    """
    TestSolutionUtility.run_test(
        day=6,
        is_raw=False,
        part_num=1,
        expected=41,
    )


def test_day06_part2() -> None:
    """Test counting wall placements that create guard movement loops.

    Verifies that the solution correctly tests placing walls at each empty
    position and counts how many modifications cause the guard's path to loop.
    """
    TestSolutionUtility.run_test(
        day=6,
        is_raw=False,
        part_num=2,
        expected=6,
    )
