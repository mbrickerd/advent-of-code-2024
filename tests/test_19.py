from aoc.models.tester import TestSolutionUtility


def test_day19_part1():
    TestSolutionUtility.run_test(
        day=19,
        is_raw=False,
        part_num=1,
        expected=6,
    )


def test_day19_part2():
    TestSolutionUtility.run_test(
        day=19,
        is_raw=False,
        part_num=2,
        expected=16,
    )
