"""Test suite for Day 24: Crossed Wires.

This module contains tests for the Day 24 solution, which analyzes digital circuits
and identifies wire connections. The tests verify:
1. Part 1: Executing a digital circuit to determine the output value
"""

from aoc.models.tester import TestSolutionUtility


def test_day24_part1() -> None:
    """Test simulating the digital circuit to calculate output value.

    Verifies that the solution correctly parses the input to extract initial
    wire values and gate connections, then simulates the execution of the circuit
    by processing gates in order until all wire values are computed, returning
    the binary value represented by the z-wires.
    """
    TestSolutionUtility.run_test(
        day=24,
        is_raw=False,
        part_num=1,
        expected=4,
    )
