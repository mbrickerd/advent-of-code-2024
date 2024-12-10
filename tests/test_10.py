from aoc.models.tester import TestSolutionUtility


def test_day10_part1():
    TestSolutionUtility.run_test(
        day=10,
        is_raw=False,
        part_num=1,
        expected=36,
    )


def test_day10_part2():
    TestSolutionUtility.run_test(
        day=10,
        is_raw=False,
        part_num=2,
        expected=81,
    )
