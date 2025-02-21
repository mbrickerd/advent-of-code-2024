"""Test suite for Day 19: Linen Layout.

This module contains tests for the Day 19 solution, which analyzes arranging
towels with colored stripe patterns. The tests verify:
1. Part 1: Determining which sequences are possible to create
2. Part 2: Counting the total number of unique ways to arrange towels
"""

from aoc.models.tester import TestSolutionUtility


def test_day19_part1() -> None:
    """Test counting possible towel pattern sequences.

    Verifies that the solution correctly determines how many of the target
    sequences can be created using the available towel patterns. A sequence
    is possible if it can be formed by combining one or more of the available
    towel patterns in any order.
    """
    TestSolutionUtility.run_test(
        day=19,
        is_raw=False,
        part_num=1,
        expected=6,
    )


def test_day19_part2() -> None:
    """Test summing all possible arrangement combinations.

    Verifies that the solution correctly calculates the total number of unique ways
    to arrange towels to match each target sequence. For each sequence, it counts
    how many different combinations of the available towel patterns can create that
    sequence, then sums these counts across all sequences.
    """
    TestSolutionUtility.run_test(
        day=19,
        is_raw=False,
        part_num=2,
        expected=16,
    )
