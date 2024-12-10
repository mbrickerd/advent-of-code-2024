import re
from typing import List

from aoc.models.base import SolutionBase


class Solution(SolutionBase):
    """Solution for Advent of Code 2024 - Day 3: Mull It Over.

    This class solves a puzzle involving parsing and processing multiplication instructions
    in a specific format. Part 1 processes simple multiplication instructions, while Part 2
    adds control flow instructions that can enable or disable the multiplication operations.

    Instructions are in the format:
        - mul(x,y): Multiply two numbers x and y
        - do(): Enable multiplication operations (Part 2 only)
        - don't(): Disable multiplication operations (Part 2 only)

    This class inherits from `SolutionBase` and provides methods to parse and execute
    these instructions from the input data.
    """

    def part1(self, data: List[str]) -> int:
        """Calculate sum of all multiplication operations in the input.

        Parses all multiplication instructions in the format `mul(x,y)` where `x` and `y`
        are 1-3 digit numbers, and returns the sum of all these multiplications.

        Args:
            data (List[str]): A list of strings containing multiplication instructions
                (e.g., ["mul(2,3)", "mul(10,20)"] or ["mul(2,3)mul(4,5)"]).

        Returns:
            int: The sum of all multiplication results. For example:
                - "mul(2,3)mul(4,5)" returns 26 (2*3 + 4*5)
                - "mul(10,20)" returns 200 (10*20)
        """
        pattern = r"mul\((\d{1,3}),(\d{1,3})\)"
        instructions = re.findall(pattern, "".join(data))

        return sum(int(x) * int(y) for x, y in instructions)

    def part2(self, data: List[str]) -> int:
        """Calculate sum of enabled multiplication operations.

        Processes multiplication and control flow instructions:
        - `mul(x,y)`: Multiply numbers `x` and `y` (if enabled)
        - `do()`: Enable multiplication operations
        - `don't()`: Disable multiplication operations

        Only multiplication operations that occur while enabled (between `do()` and `don't()`)
        are included in the final sum.

        Args:
            data (List[str]): A list of strings containing multiplication and control
                instructions (e.g., ["do()mul(2,3)don't()mul(4,5)"]).

        Returns:
            int: The sum of multiplication results that occurred while enabled.
                For example:
                - "do()mul(2,3)don't()mul(4,5)" returns 6 (only 2*3 is counted)
                - "mul(2,3)do()mul(4,5)" returns 20 (only 4*5 is counted)
        """
        pattern = r"(mul\((\d{1,3}),(\d{1,3})\)|do\(\)|don't\(\))"
        instructions = re.findall(pattern, "".join(data))

        enabled = True
        result = 0

        for step in instructions:
            match step[0]:
                case "do()":
                    enabled = True

                case "don't()":
                    enabled = False

                case _ if enabled:
                    result += int(step[1]) * int(step[2])

        return result
