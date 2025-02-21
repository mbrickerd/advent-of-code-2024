"""Test suite for Day 12: Garden Groups.

This module contains tests for the Day 12 solution, which handles analyzing groups
of plants in a garden grid where each connected region must be fenced. The tests verify:
1. Part 1: Calculating total cost using perimeter-based pricing
2. Part 2: Calculating total cost using distinct sides-based pricing
"""

from aoc.models.tester import TestSolutionUtility


def test_day12_part1() -> None:
    """Test calculating total fencing cost using perimeter-based pricing.

    Verifies that the solution correctly identifies all connected plant regions,
    calculates their areas and perimeters, and determines the total fencing cost
    as the sum of area x perimeter for each region.
    """
    TestSolutionUtility.run_test(
        day=12,
        is_raw=False,
        part_num=1,
        expected=1930,
    )


def test_day12_part2() -> None:
    """Test calculating total fencing cost using distinct sides-based pricing.

    Verifies that the solution correctly identifies all connected plant regions,
    calculates their areas and counts their unique sides (merging adjacent parallel edges),
    then determines the total fencing cost as the sum of area x number_of_sides for each region.
    """
    TestSolutionUtility.run_test(
        day=12,
        is_raw=False,
        part_num=2,
        expected=1206,
    )
