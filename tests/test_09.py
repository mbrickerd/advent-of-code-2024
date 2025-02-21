"""Test suite for Day 9: Disk Fragmenter.

This module contains tests for the Day 9 solution, which handles simulation
of disk defragmentation processes and calculates checksums. The tests verify:
1. Part 1: Moving files from right to left to minimize fragmentation
2. Part 2: Moving files as far left as possible into available spaces
"""

from aoc.models.tester import TestSolutionUtility


def test_day09_part1() -> None:
    """Test calculating checksum after moving files from right to left.

    Verifies that the solution correctly processes files by moving them into
    the rightmost available spaces when defragmenting from right to left,
    then calculates the appropriate position-based checksum.
    """
    TestSolutionUtility.run_test(
        day=9,
        is_raw=False,
        part_num=1,
        expected=1928,
    )


def test_day09_part2() -> None:
    """Test calculating checksum after moving files as far left as possible.

    Verifies that the solution correctly processes files by moving each one
    into the leftmost available space that can accommodate it, then calculates
    the appropriate position-based checksum.
    """
    TestSolutionUtility.run_test(
        day=9,
        is_raw=False,
        part_num=2,
        expected=2858,
    )
