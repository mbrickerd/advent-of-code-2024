"""Day 7: Bridge Repair.

This module provides the solution for Advent of Code 2024 - Day 7.
It handles processing numerical equations for bridge repair calculations.

The module contains a Solution class that inherits from SolutionBase and implements
methods to evaluate equation combinations using different allowed operations to
reach target totals.
"""

from collections.abc import Callable

from aoc.models.base import SolutionBase


class Solution(SolutionBase):
    """Solution for Advent of Code 2024 - Day 7: Bridge Repair.

    Solves puzzles involving mathematical operations:
    - Part 1: Find valid equations using addition and multiplication
    - Part 2: Find valid equations using addition, multiplication, and digit concatenation
    """

    def parse_data(self, data: list[str]) -> list[tuple[int, list[int]]]:
        """Parse input strings into equations with targets and values.

        Args:
            data: Input lines in format "total: num1 num2 num3..."

        Returns
        -------
            List of tuples containing (target_total, list_of_values)

        Example:
            For input "10: 2 3 4" returns [(10, [2, 3, 4])]
        """
        result = []
        for line in data:
            if ":" not in line:
                continue

            total, values = line.split(":", 1)
            try:
                target = int(total)
                nums = [int(v) for v in values.strip().split()]
                result.append((target, nums))

            except ValueError:
                continue

        return result

    def solve_part(
        self,
        data: list[str],
        ops: list[Callable[[int, int], int]],
        *,
        check_limit: bool | None = None,
    ) -> int:
        """Solve the puzzle part using specified operations.

        For each equation, tries all possible combinations of operations between
        numbers in sequential order. Counts equations where some combination
        reaches the target total.

        Args:
            data: Input equations in string format
            ops: List of operations to apply between sequential numbers
            check_limit: Whether to limit results to not exceed target value

        Returns
        -------
            Sum of target totals from valid equations

        Example:
            With addition and multiplication ops:
            - "10: 2 3 4" is valid (2*3+4=10)
            - "7: 2 3 4" is invalid (no combination equals 7)
        """
        valid_sum = 0
        check_limit = bool(check_limit) if check_limit is not None else False

        for target, nums in self.parse_data(data):
            if not nums:
                continue

            results = {nums[0]}

            for num in nums[1:]:
                new_results = set()
                for prev in results:
                    for op in ops:
                        result = op(prev, num)
                        if not check_limit or result <= target:
                            new_results.add(result)

                results = new_results

            if target in results:
                valid_sum += target

        return valid_sum

    def part1(self, data: list[str]) -> int:
        """Sum totals of valid equations using addition and multiplication.

        Tries all possible combinations of addition and multiplication operations
        between numbers in order. Counts equations where some combination reaches
        the target total.

        Args:
            data: Input lines containing equations

        Returns
        -------
            Sum of target totals from valid equations
        """
        return self.solve_part(data, [lambda x, y: x + y, lambda x, y: x * y])

    def part2(self, data: list[str]) -> int:
        """Sum totals of valid equations with addition, multiplication, and concatenation.

        Similar to part1 but adds digit concatenation as a valid operation.
        For example, 2||3 = 23 (where || represents concatenation).
        Only counts results that don't exceed the target total.

        Args:
            data: Input lines containing equations

        Returns
        -------
            Sum of target totals from valid equations
        """
        return self.solve_part(
            data,
            [lambda x, y: x + y, lambda x, y: x * y, lambda x, y: int(f"{x}{y}")],
            check_limit=True,
        )
