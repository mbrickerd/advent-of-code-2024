from aoc.models.tester import TestSolutionUtility


def test_day07_part1():
    TestSolutionUtility.run_test(
        day=7,
        is_raw=False,
        part_num=1,
        expected=3749,
    )


def test_day07_part2():
    TestSolutionUtility.run_test(
        day=7,
        is_raw=False,
        part_num=2,
        expected=11387,
    )
