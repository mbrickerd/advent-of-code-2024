"""Test suite for Day 10: Hoof It.

This module contains tests for the Day 10 solution, which handles finding
valid hiking trails on a topographic map and calculating trailhead scores
based on reachable peak positions. The tests verify:
1. Part 1: Calculating total score based on reachable peaks from all trailheads
2. Part 2: Calculating total rating based on unique paths to peaks
"""

from aoc.models.tester import TestSolutionUtility


def test_day10_part1() -> None:
    """Test calculating sum of scores for all trailheads.

    Verifies that the solution correctly identifies all possible height-9 positions
    reachable from each trailhead via valid hiking trails, and calculates the sum
    of scores across all trailheads.
    """
    TestSolutionUtility.run_test(
        day=10,
        is_raw=False,
        part_num=1,
        expected=36,
    )


def test_day10_part2() -> None:
    """Test calculating sum of ratings based on unique paths to peaks.

    Verifies that the solution correctly counts the number of distinct hiking
    trails from each trailhead to any height-9 position, and calculates the sum
    of these counts across all trailheads.
    """
    TestSolutionUtility.run_test(
        day=10,
        is_raw=False,
        part_num=2,
        expected=81,
    )
