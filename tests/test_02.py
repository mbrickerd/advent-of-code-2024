"""Test suite for Day 2: Red-Nosed Reports.

This module contains tests for the Day 2 solution, which analyzes numeric sequences
with specific monotonicity and difference constraints. The tests verify:
1. Part 1: Identification of strictly increasing/decreasing sequences with adjacent
   differences between 1 and 3
2. Part 2: Handling of sequences where removing one number creates a valid sequence
"""

from aoc.models.tester import TestSolutionUtility


def test_day02_part1() -> None:
    """Test identifying valid monotonic sequences with specific difference constraints.

    Verifies that the solution correctly counts sequences that are either strictly
    increasing or strictly decreasing, and where all adjacent number differences
    are between 1 and 3 inclusive.
    """
    TestSolutionUtility.run_test(
        day=2,
        is_raw=False,
        part_num=1,
        expected=2,
    )


def test_day02_part2() -> None:
    """Test identifying sequences that become valid after removing one number.

    Verifies that the solution correctly counts sequences that either (1) are valid
    according to part1 criteria, or (2) become valid when exactly one number is
    removed from the sequence.
    """
    TestSolutionUtility.run_test(
        day=2,
        is_raw=False,
        part_num=2,
        expected=4,
    )
