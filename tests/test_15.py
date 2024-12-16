from aoc.models.tester import TestSolutionUtility


def test_day15_part1():
    TestSolutionUtility.run_test(
        day=15,
        is_raw=False,
        part_num=1,
        expected=10092,
    )


def test_day15_part2():
    TestSolutionUtility.run_test(
        day=15,
        is_raw=False,
        part_num=2,
        expected=9021,
    )
