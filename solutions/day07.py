from typing import List, Tuple

from aoc.models.base import SolutionBase


class Solution(SolutionBase):
    """Solution for Advent of Code 2024 - Day 7: Bridge Repair.

    This class solves a puzzle involving numerical equations for bridge repair calculations.
    Part 1 finds valid equations using addition and multiplication, while Part 2 adds
    digit concatenation as a valid operation. Each equation must evaluate to a target total
    using all values in order.

    Input format:
        Lines of "total: num1 num2 num3..." where `total` is the target sum and the numbers
        must be combined in order using allowed operations to reach that total.

    This class inherits from `SolutionBase` and provides methods to parse and evaluate
    possible equation combinations.
    """

    def parse_data(self, data: List[str]) -> List[Tuple[int, List[int]]]:
        """Parse input strings into equations with targets and values.

        Args:
            data (List[str]): Input lines in format "total: num1 num2 num3..."

        Returns:
            List[Tuple[int, List[int]]]: List of tuples containing:
                - Target total (int)
                - List of numbers to combine

                Example:
                For input "10: 2 3 4" returns [(10, [2, 3, 4])]
        """
        equations = []
        for line in data:
            total, values = line.split(":")
            equations.append((int(total), [*map(int, values.strip().split())]))

        return equations

    def part1(self, data: List[str]) -> int:
        """Sum totals of valid equations using addition and multiplication.

        For each equation, tries all possible combinations of addition and
        multiplication operations between numbers in order. Counts equations
        where some combination reaches the target total.

        Args:
            data (List[str]): Input lines containing equations

        Returns:
            int: Sum of target totals from valid equations. For example:
                - "10: 2 3 4" is valid (2*3+4=10)
                - "12: 2 3 4" is valid (2*3*4=24)
                - "7: 2 3 4" is invalid (no combination equals 7)
        """
        equations = self.parse_data(data)
        result = []

        for total, values in equations:
            possibles = [values.pop(0)]
            while values:
                current = values.pop(0)
                tmp = []
                for p in possibles:
                    tmp.append(p + current)  # Addition
                    tmp.append(p * current)  # Multiplication

                possibles = tmp

            if total in possibles:
                result.append(total)

        return sum(result)

    def part2(self, data: List[str]) -> int:
        """Sum totals of valid equations with addition, multiplication, and concatenation.

        Similar to part1 but adds digit concatenation as a valid operation.
        For example, 2 || 3 = 23 (where || represents concatenation).
        Only counts results that don't exceed the target total.

        Args:
            data (List[str]): Input lines containing equations

        Returns:
            int: Sum of target totals from valid equations. For example:
                - "23: 2 3" is valid (2||3=23)
                - "8: 2 3 4" is valid (2+3+3=8)
                - "234: 2 3 4" is valid (2||3||4=234)
        """
        equations = self.parse_data(data)
        result = []

        for total, values in equations:
            possibles = [values.pop(0)]
            while values:
                current = values.pop(0)
                tmp = []
                for p in possibles:
                    next_values = [  # Addition, multiplication, and concatenation
                        p + current,
                        p * current,
                        int(str(p) + str(current)),
                    ]
                    tmp.extend([v for v in next_values if v <= total])

                possibles = tmp

            if total in possibles:
                result.append(total)

        return sum(result)
