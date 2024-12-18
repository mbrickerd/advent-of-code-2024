from aoc.models.tester import TestSolutionUtility


def test_day18_part1():
    TestSolutionUtility.run_test(
        day=18,
        is_raw=False,
        part_num=1,
        expected=22,
    )


def test_day18_part2():
    TestSolutionUtility.run_test(
        day=18,
        is_raw=False,
        part_num=2,
        expected="6,1",
    )
