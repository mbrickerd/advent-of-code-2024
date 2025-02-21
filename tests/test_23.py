"""Test suite for Day 23: LAN Party.

This module contains tests for the Day 23 solution, which analyzes LAN party
connections and finds gaming groups. The tests verify:
1. Part 1: Identifying valid gaming trios including teachers
2. Part 2: Finding the largest possible gaming group
"""

from aoc.models.tester import TestSolutionUtility


def test_day23_part1() -> None:
    """Test counting valid gaming trios that include at least one teacher.

    Verifies that the solution correctly identifies all possible groups of
    three players that:
    1. Are fully connected (form a clique)
    2. Include at least one teacher (node starting with 't')
    3. Can play together based on direct connections
    """
    TestSolutionUtility.run_test(
        day=23,
        is_raw=False,
        part_num=1,
        expected=7,
    )


def test_day23_part2() -> None:
    """Test finding the largest possible gaming group.

    Verifies that the solution correctly identifies the maximum clique in
    the connection graph, representing the largest group of players that
    can all play together directly. Returns the players in alphabetical
    order as a comma-separated string.
    """
    TestSolutionUtility.run_test(
        day=23,
        is_raw=False,
        part_num=2,
        expected="co,de,ka,ta",
    )
