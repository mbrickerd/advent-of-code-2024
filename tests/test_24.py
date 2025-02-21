"""Test suite for Day 24: Crossed Wires.

This module contains tests for the Day 24 solution, which analyzes digital circuits
and identifies wire connections. The tests verify:
1. Part 1: Executing a digital circuit to determine the output value
2. Part 2: Analyzing circuit structure to identify wires that need to be swapped
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


def test_day24_part2() -> None:
    """Test identifying misconnected wires in the full adder circuit.

    Verifies that the solution correctly analyzes the circuit structure to find
    z-wires that need to be swapped to correctly implement a full adder, handling
    special cases for simplified test circuits and returning a comma-separated
    list of wires that need to be swapped.
    """
    TestSolutionUtility.run_test(
        day=24,
        is_raw=False,
        part_num=2,
        expected="z00,z01,z02,z05",
    )
