from aoc.models.reader import Reader
from aoc.utils.initalise import initialise


class TestSolutionUtility:
    """
    Utility class for testing Advent of Code puzzle solutions.

    Provides automated testing functionality to verify puzzle solutions against
    example inputs and expected outputs provided in puzzle descriptions.
    """

    @staticmethod
    def run_test(
        day: int,
        is_raw: bool,
        part_num: int,
        expected: int,
    ):
        """
        Run a test case for a specific puzzle solution.

        Automatically loads the appropriate solution class for the given day,
        executes the specified part with test input, and verifies the result
        against the expected answer.

        Args:
            day (int): The day number (1-25) of the puzzle to test.
            is_raw (bool): If `True`, preserves newlines in input. If `False`, strips whitespace.
            part_num (int): The puzzle part number (1 or 2) to test.
            expected (int): The expected result from the example in the puzzle description.

        Raises:
            AssertionError: If the solution output doesn't match the expected result,
                with a detailed error message showing the discrepancy.

        Note:
            - Uses the `initialise()` function to dynamically load the solution class
            - Loads test input from `data/dayXX/test_YY_input.txt`
            - Expects solution classes to have `part1()` and `part2()` methods

        Example:
            >>> TestSolutionUtility.run_test(1, False, 1, 42)
            # Tests day 1, part 1, expecting result 42
            # Raises AssertionError if result != 42
        """
        # Instantiate the solution object with the necessary parameters
        solution = initialise(day)

        # Dynamically select the part method based on `part_num`
        part_method = getattr(solution, f"part{part_num}")

        # Load test input
        test_input = Reader.get_test_input(day, is_raw, part_num)

        # Execute the selected method with the test input
        result = part_method(data=test_input)

        # Assert the result
        assert result == expected, f"Test failed for Day {day}, Part {part_num}: Expected {expected}, got {result}."
