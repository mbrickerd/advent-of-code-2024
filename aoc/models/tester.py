"""
Testing utilities for Advent of Code solutions.

This module provides a TestSolutionUtility class that automates the process of testing
puzzle solutions against example inputs and expected outputs from puzzle descriptions.
"""

from aoc.models.base import SolutionBase
from aoc.models.reader import Reader
from aoc.utils.initalise import initialise


class TestSolutionUtility:
    """Utility class for testing Advent of Code puzzle solutions.

    Provides automated testing functionality to verify puzzle solutions against
    example inputs and expected outputs provided in puzzle descriptions.
    """

    @staticmethod
    def run_test(
        day: int,
        part_num: int,
        expected: str | int,
        *,
        is_raw: bool = False,
    ) -> None:
        """Run a test case for a specific puzzle solution.

        Automatically loads the appropriate solution class for the given day,
        executes the specified part with test input, and verifies the result
        against the expected answer.

        Args:
            day: The day number (1-25) of the puzzle to test.
            part_num: The puzzle part number (1 or 2) to test.
            expected: The expected result from the example in the puzzle description.
            is_raw: If `True`, preserves newlines in input. If `False`, strips whitespace.
                Default is False.

        Raises
        ------
            ValueError: If the solution output doesn't match the expected result,
                with a detailed error message showing the discrepancy.

        Note:
            - Uses the `initialise()` function to dynamically load the solution class
            - Loads test input from `tests/data/dayXX/test_YY_input.txt`
            - Expects solution classes to have `part1()` and `part2()` methods
        """
        solution: SolutionBase = initialise(day, skip_test=False)
        part_method = getattr(solution, f"part{part_num}")
        test_input = Reader.get_test_input(day, part_num, raw=is_raw)
        result = part_method(data=test_input)

        if result != expected:
            error_message = (
                f"Test failed for Day {day}, Part {part_num}: Expected {expected}, got {result}."
            )
            raise ValueError(error_message)
