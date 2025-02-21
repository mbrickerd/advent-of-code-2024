"""Test suite for Day 17: Chronospatial Computer.

This module contains tests for the Day 17 solution, which simulates a 3-bit
computer with three registers and eight instructions. The tests verify:
1. Part 1: Executing the program with given register values
2. Part 2: Finding the lowest value for register A that makes the program output itself
"""

from aoc.models.tester import TestSolutionUtility


def test_day17_part1() -> None:
    """Test executing the program and obtaining its output.

    Verifies that the solution correctly simulates the 3-bit computer,
    executing instructions with the given register values and returning
    the program's output as a comma-separated string.
    """
    TestSolutionUtility.run_test(
        day=17,
        is_raw=False,
        part_num=1,
        expected="4,6,3,5,6,3,5,2,1,0",
    )


def test_day17_part2() -> None:
    """Test finding lowest register A value for self-output.

    Verifies that the solution correctly identifies the lowest positive value
    for register A that causes the program to output a copy of its own instructions.
    """
    TestSolutionUtility.run_test(
        day=17,
        is_raw=False,
        part_num=2,
        expected=117440,
    )
