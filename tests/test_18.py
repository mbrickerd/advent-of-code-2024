"""Test suite for Day 18: RAM Run.

This module contains tests for the Day 18 solution, which involves pathfinding
in a corrupted memory space. The tests verify:
1. Part 1: Finding the shortest path to exit through uncorrupted spaces
2. Part 2: Determining which falling byte first makes the exit unreachable
"""

from aoc.models.tester import TestSolutionUtility


def test_day18_part1() -> None:
    """Test finding shortest path through uncorrupted memory spaces.

    Verifies that the solution correctly calculates the shortest path from
    start to end through uncorrupted memory spaces after initial byte corruption,
    using breadth-first search to find the minimum distance.
    """
    TestSolutionUtility.run_test(
        day=18,
        is_raw=False,
        part_num=1,
        expected=22,
    )


def test_day18_part2() -> None:
    """Test identifying the critical byte that blocks all paths.

    Verifies that the solution correctly determines which falling byte is the first
    to make the exit completely unreachable, using binary search to efficiently find
    the critical corruption point.
    """
    TestSolutionUtility.run_test(
        day=18,
        is_raw=False,
        part_num=2,
        expected="6,1",
    )
