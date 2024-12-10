from aoc.models.tester import TestSolutionUtility


def test_day09_part1():
    TestSolutionUtility.run_test(
        day=9,
        is_raw=False,
        part_num=1,
        expected=1928,
    )


def test_day09_part2():
    TestSolutionUtility.run_test(
        day=9,
        is_raw=False,
        part_num=2,
        expected=2858,
    )
