"""Test suite for Day 16: Reindeer Maze.

This module contains tests for the Day 16 solution, which finds optimal paths
through a maze with movement costs. The tests verify:
1. Part 1: Finding the minimum cost to reach the end
2. Part 2: Counting all tiles that are part of any optimal path
"""

from aoc.models.tester import TestSolutionUtility


def test_day16_part1() -> None:
    """Test finding minimum cost to reach the end of the maze.

    Verifies that the solution correctly calculates the minimum total cost to reach
    the end position, considering that reindeer start facing east and can move forward
    (cost 1) or rotate 90 degrees (cost 1000).
    """
    TestSolutionUtility.run_test(
        day=16,
        is_raw=False,
        part_num=1,
        expected=7036,
    )


def test_day16_part2() -> None:
    """Test counting tiles that are part of any optimal path.

    Verifies that the solution correctly identifies all possible paths with the
    minimum cost and counts the unique tiles (positions) that appear in any of
    these optimal paths.
    """
    TestSolutionUtility.run_test(
        day=16,
        is_raw=False,
        part_num=2,
        expected=45,
    )
