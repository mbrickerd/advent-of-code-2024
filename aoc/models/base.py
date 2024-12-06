import timeit

from loguru import logger

from aoc.models.reader import Reader


class SolutionBase:
    def __init__(
        self,
        day: int = -1,
        part_num: int = 1,
        is_raw: bool = False,
        skip_test: bool = True,
        benchmark: bool = False,
    ) -> None:
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
        if self.is_raw is False:
            logger.info("Please use --raw flag in this puzzle")
            exit()

    def benchmark(self, _print: bool = False) -> None:
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
        func = getattr(self, f"part{part_num}")
        self.benchmark()

        result = func(self.data)
        self.benchmark()

        return result
