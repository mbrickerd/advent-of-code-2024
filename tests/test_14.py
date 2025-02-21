"""Test suite for Day 14: Restroom Redoubt.

This module contains tests for the Day 14 solution, which simulates robots
moving in a confined grid space. The tests verify:
1. Part 1: Calculating product of robots in each quadrant after 100 time steps
"""

from aoc.models.tester import TestSolutionUtility


def test_day14_part1() -> None:
    """Test calculating product of robots in each quadrant.

    Verifies that the solution correctly simulates robot movement through
    a wrapping grid over 100 time steps, divides the grid into four quadrants,
    counts robots in each quadrant (excluding those on center lines), and
    calculates the product of these counts.
    """
    TestSolutionUtility.run_test(
        day=14,
        is_raw=False,
        part_num=1,
        expected=12,
    )
