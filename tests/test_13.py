"""Test suite for Day 13: Claw Contraption.

This module contains tests for the Day 13 solution, which solves a puzzle involving
a claw machine game where two buttons control movement. The tests verify:
1. Part 1: Calculating minimum tokens needed with standard prize coordinates
"""

from aoc.models.tester import TestSolutionUtility


def test_day13_part1() -> None:
    """Test calculating minimum tokens needed to reach prize coordinates.

    Verifies that the solution correctly calculates the minimum number of tokens
    needed to reach prize coordinates using button presses, where:
    - Button A costs 3 tokens per press
    - Button B costs 1 token per press
    - Each button moves the claw by specific X and Y coordinates
    """
    TestSolutionUtility.run_test(
        day=13,
        is_raw=False,
        part_num=1,
        expected=480,
    )
