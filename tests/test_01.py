from aoc.models.tester import TestSolutionUtility


def test_day01_part1():
    TestSolutionUtility.run_test(
        day=1,
        is_raw=False,
        part_num=1,
        expected=11,
    )


def test_day01_part2():
    TestSolutionUtility.run_test(
        day=1,
        is_raw=False,
        part_num=2,
        expected=31,
    )
