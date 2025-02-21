"""Test suite for Day 20: Race Condition.

This module contains tests for the Day 20 solution, which finds shortcuts in a
racetrack maze. The tests verify:
1. Part 1: Finding valid 2-move cheats that save steps
2. Part 2: Finding valid 20-move cheats that save steps
"""

from aoc.models.tester import TestSolutionUtility


def test_day20_part1() -> None:
    """Test counting valid cheats using maximum 2-move teleports.

    Verifies that the solution correctly identifies all valid ways to cheat
    through walls using at most 2 moves in any direction. A valid cheat must
    return to a normal path position after teleporting and must save at least
    the required number of steps compared to the normal path.
    """
    TestSolutionUtility.run_test(
        day=20,
        is_raw=False,
        part_num=1,
        expected=44,
    )


def test_day20_part2() -> None:
    """Test counting valid cheats using maximum 20-move teleports.

    Verifies that the solution correctly identifies all valid ways to cheat
    through walls using at most 20 moves in any direction. This allows for
    longer teleport distances that bypass larger sections of walls, while
    still requiring the cheat to end on a valid path position and save the
    minimum required steps.
    """
    TestSolutionUtility.run_test(
        day=20,
        is_raw=False,
        part_num=2,
        expected=3081,
    )
