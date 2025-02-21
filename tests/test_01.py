"""Test suite for Day 1: Historian Hysteria.

This module contains tests for the Day 1 solution, which handles processing and
comparing pairs of historical data points. The tests verify:
1. Part 1: Calculation of total disparity between sorted parallel datasets
2. Part 2: Handling of frequency-weighted matches between datasets
"""

from aoc.models.tester import TestSolutionUtility


def test_day01_part1() -> None:
    """Test calculating total disparity between sorted parallel lists.

    Verifies that the solution correctly calculates the sum of absolute
    differences between corresponding elements in sorted lists.
    """
    TestSolutionUtility.run_test(
        day=1,
        is_raw=False,
        part_num=1,
        expected=11,
    )


def test_day01_part2() -> None:
    """Test calculating frequency-weighted matches between datasets.

    Verifies that the solution correctly calculates the sum of products
    between matching elements weighted by their frequency.
    """
    TestSolutionUtility.run_test(
        day=1,
        is_raw=False,
        part_num=2,
        expected=31,
    )
