"""Day 3: Mull It Over.

This module provides the solution for Advent of Code 2024 - Day 3.
It handles parsing and execution of multiplication and control flow instructions.

The module contains a Solution class that inherits from SolutionBase and implements
methods to process instructions in two different modes:
1. Part 1: Simple multiplication of number pairs
2. Part 2: Conditional multiplication based on control flow instructions
"""

import re

from aoc.models.base import SolutionBase


class Solution(SolutionBase):
    """Process multiplication and control flow instructions.

    This solution parses and executes instructions in a specific format:
    - mul(x,y): Multiply two numbers x and y
    - do(): Enable multiplication operations (Part 2 only)
    - don't(): Disable multiplication operations (Part 2 only)

    Part 1 processes all multiplication instructions.
    Part 2 only processes multiplications when they're enabled by control flow.
    """

    MULTIPLY_PATTERN = re.compile(r"mul\((\d{1,3}),(\d{1,3})\)")
    INSTRUCTION_PATTERN = re.compile(r"(mul\((\d{1,3}),(\d{1,3})\)|do\(\)|don't\(\))")

    def part1(self, data: list[str]) -> int:
        """Calculate sum of all multiplication operations in the input.

        Parses all multiplication instructions in the format `mul(x,y)` where `x` and `y`
        are 1-3 digit numbers, and returns the sum of all these multiplications.

        Args:
            data: A list of strings containing multiplication instructions.

        Returns
        -------
            The sum of all multiplication results.
        """
        input_text = "".join(data)
        return sum(int(x) * int(y) for x, y in self.MULTIPLY_PATTERN.findall(input_text))

    def part2(self, data: list[str]) -> int:
        """Calculate sum of enabled multiplication operations.

        Processes multiplication and control flow instructions:
        - `mul(x,y)`: Multiply numbers `x` and `y` (if enabled)
        - `do()`: Enable multiplication operations
        - `don't()`: Disable multiplication operations

        Only multiplication operations that occur while enabled (between `do()` and `don't()`)
        are included in the final sum.

        Args:
            data: A list of strings containing multiplication and control instructions.

        Returns
        -------
            The sum of multiplication results that occurred while enabled.
        """
        input_text = "".join(data)
        instructions = self.INSTRUCTION_PATTERN.findall(input_text)

        enabled = True
        total = 0

        for instruction in instructions:
            cmd = instruction[0]

            if cmd == "do()":
                enabled = True

            elif cmd == "don't()":
                enabled = False

            elif enabled and cmd.startswith("mul"):
                total += int(instruction[1]) * int(instruction[2])

        return total
