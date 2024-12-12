from aoc.models.tester import TestSolutionUtility


def test_day12_part1():
    TestSolutionUtility.run_test(
        day=12,
        is_raw=False,
        part_num=1,
        expected=1930,
    )


def test_day12_part2():
    TestSolutionUtility.run_test(
        day=12,
        is_raw=False,
        part_num=2,
        expected=1206,
    )
