"""Test suite for Day 4: Ceres Search.

This module contains tests for the Day 4 solution, which implements pattern
searching algorithms in 2D character grids. The tests verify:
1. Part 1: Finding "XMAS" patterns in any of 8 directions (horizontal, vertical, diagonal)
2. Part 2: Locating X-shaped patterns where two "MAS" sequences cross at their 'A's
"""

from aoc.models.tester import TestSolutionUtility


def test_day04_part1() -> None:
    """Test counting occurrences of "XMAS" in all 8 directions.

    Verifies that the solution correctly finds and counts all instances of the
    "XMAS" pattern in any direction (horizontal, vertical, or diagonal) within
    the 2D grid.
    """
    TestSolutionUtility.run_test(
        day=4,
        is_raw=False,
        part_num=1,
        expected=18,
    )


def test_day04_part2() -> None:
    """Test counting X-shaped patterns formed by crossing "MAS" sequences.

    Verifies that the solution correctly identifies and counts X-shaped patterns
    where two "MAS" sequences cross at their 'A' character, forming a distinctive
    pattern in the grid.
    """
    TestSolutionUtility.run_test(
        day=4,
        is_raw=False,
        part_num=2,
        expected=9,
    )
