import timeit

from loguru import logger

from aoc.models.reader import Reader


class SolutionBase:
    """
    Base class for implementing Advent of Code puzzle solutions with benchmarking capabilities.

    This class provides a framework for solving daily AoC challenges, supporting both test and
    puzzle inputs, with optional performance benchmarking. Each puzzle solution should inherit
    from this class and implement `part1()` and `part2()` methods.

    Attributes:
        day (int): The Advent of Code day number (-1 by default)
        part_num (int): The puzzle part number (1 or 2)
        is_raw (bool): Flag indicating whether to use raw input format
        skip_test (bool): Flag indicating whether to use actual puzzle input instead of test input
        _benchmark (bool): Flag for enabling solution timing measurements
        benchmark_times (list): List storing benchmark timestamps
        data: Puzzle input data loaded from either test or actual input files
    """

    def __init__(
        self,
        day: int = -1,
        part_num: int = 1,
        is_raw: bool = False,
        skip_test: bool = True,
        benchmark: bool = False,
    ) -> None:
        """
        Initialize a solution instance for an Advent of Code puzzle.

        Args:
            day (int, optional): The day number of the puzzle (1-25). Defaults to -1.
            part_num (int, optional): Which part of the day's puzzle (1 or 2). Defaults to 1.
            is_raw (bool, optional): Whether to load input as raw text. Defaults to `False`.
            skip_test (bool, optional): Whether to use puzzle input instead of test input. Defaults to `True`.
            benchmark (bool, optional): Whether to measure solution execution time. Defaults to `False`.
        """
        self.day = day
        self.part_num = part_num
        self.is_raw = is_raw
        self.skip_test = skip_test
        self._benchmark = benchmark
        self.benchmark_times = []
        self.data = (
            Reader.get_puzzle_input(self.day, self.is_raw)
            if self.skip_test
            else Reader.get_test_input(self.day, self.is_raw, self.part_num)
        )

    def check_is_raw(self) -> None:
        """
        Verify if raw input mode is enabled for puzzles that require it.

        Some Advent of Code puzzles require preserving whitespace or special characters
        in the input. This method ensures raw mode is enabled for such puzzles.

        Exits the program with a warning message if raw input mode is not enabled.
        """
        if self.is_raw is False:
            logger.info("Please use --raw flag in this puzzle")
            exit()

    def benchmark(self, _print: bool = False) -> None:
        """
        Record or display solution execution time benchmarks.

        When called with `_print=False`, records a timestamp. When called with `_print=True`,
        calculates and displays the elapsed time since the last timestamp in appropriate
        units (`s`, `ms`, `µs`, or `ns`).

        Args:
            _print (bool, optional): Whether to print the elapsed time. Defaults to `False`.
        """
        if (
            _print
            and len(self.benchmark_times) > 0
            and len(self.benchmark_times) % 2 == 0
        ):
            t = self.benchmark_times[-1] - self.benchmark_times[-2]
            units = ["s", "ms", "µs", "ns"]
            unit_idx = 0

            while t < 1:
                t *= 1000
                unit_idx += 1

            logger.info(f"Benchmarking: {t:.2f} {units[unit_idx]}")

        elif self._benchmark:
            self.benchmark_times.append(timeit.default_timer())

    def solve(self, part_num: int) -> int:
        """
        Execute the solution for a specified puzzle part.

        Calls either `part1()` or `part2()` method based on the `part_num` parameter,
        with optional execution time measurement.

        Args:
            part_num (int): Which part of the puzzle to solve (1 or 2)

        Returns:
            int: The solution result for the specified puzzle part

        Note:
            Inheriting classes must implement `part1()` and `part2()` methods.
        """
        func = getattr(self, f"part{part_num}")
        self.benchmark()

        result = func(self.data)
        self.benchmark()

        return result
