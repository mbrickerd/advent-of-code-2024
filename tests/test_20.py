from aoc.models.tester import TestSolutionUtility


def test_day20_part1():
    TestSolutionUtility.run_test(
        day=20,
        is_raw=False,
        part_num=1,
        expected=44,
    )


def test_day20_part2():
    TestSolutionUtility.run_test(
        day=20,
        is_raw=False,
        part_num=2,
        expected=3081,
    )
