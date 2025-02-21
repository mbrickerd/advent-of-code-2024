"""Test suite for Day 8: Resonant Collinearity.

This module contains tests for the Day 8 solution, which simulates antenna
resonance patterns to find antinodes in a grid. The tests verify:
1. Part 1: Finding points where one antenna is twice as far as another
2. Part 2: Counting all collinear points as antinodes
"""

from aoc.models.tester import TestSolutionUtility


def test_day08_part1() -> None:
    """Test counting antinodes with specific distance ratios.

    Verifies that the solution correctly identifies grid positions that form
    antinodes when they are collinear with two antennas and the distance to
    one antenna is exactly twice the distance to the other.
    """
    TestSolutionUtility.run_test(
        day=8,
        is_raw=False,
        part_num=1,
        expected=14,
    )


def test_day08_part2() -> None:
    """Test counting all collinear points as antinodes.

    Verifies that the solution correctly identifies all grid positions that
    are collinear with any pair of same-frequency antennas, counting them
    as antinodes under the relaxed rules.
    """
    TestSolutionUtility.run_test(
        day=8,
        is_raw=False,
        part_num=2,
        expected=34,
    )
