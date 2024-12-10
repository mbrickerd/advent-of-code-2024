from aoc.models.tester import TestSolutionUtility


def test_day08_part1():
    TestSolutionUtility.run_test(
        day=8,
        is_raw=False,
        part_num=1,
        expected=14,
    )


def test_day08_part2():
    TestSolutionUtility.run_test(
        day=8,
        is_raw=False,
        part_num=2,
        expected=34,
    )
