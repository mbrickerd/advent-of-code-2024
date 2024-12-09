from aoc.models.tester import TestSolutionUtility


def test_day04_part1():
    TestSolutionUtility.run_test(
        day=4,
        is_raw=False,
        part_num=1,
        expected=18,
    )


def test_day04_part2():
    TestSolutionUtility.run_test(
        day=4,
        is_raw=False,
        part_num=2,
        expected=9,
    )
