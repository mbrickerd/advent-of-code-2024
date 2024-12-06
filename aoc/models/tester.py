from aoc.models.reader import Reader
from aoc.utils.initalise import initialise


class TestSolutionUtility:
    @staticmethod
    def run_test(
        day: int,
        is_raw: bool,
        part_num: int,
        expected: int,
    ):
        # Instantiate the solution object with the necessary parameters
        solution = initialise(day)

        # Dynamically select the part method based on `part_num`
        part_method = getattr(solution, f"part{part_num}")

        # Load test input
        test_input = Reader.get_test_input(day, is_raw, part_num)

        # Execute the selected method with the test input
        result = part_method(data=test_input)

        # Assert the result
        assert (
            result == expected
        ), f"Test failed for Day {day}, Part {part_num}: Expected {expected}, got {result}."
