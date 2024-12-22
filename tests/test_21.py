from aoc.models.tester import TestSolutionUtility


def test_day21_part1():
    TestSolutionUtility.run_test(
        day=21,
        is_raw=False,
        part_num=1,
        expected=126384,
    )


def test_day21_part2():
    TestSolutionUtility.run_test(
        day=21,
        is_raw=False,
        part_num=2,
        expected=154115708116294,
    )
