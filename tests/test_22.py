from aoc.models.tester import TestSolutionUtility


def test_day22_part1():
    TestSolutionUtility.run_test(
        day=22,
        is_raw=False,
        part_num=1,
        expected=37327623,
    )


def test_day22_part2():
    TestSolutionUtility.run_test(
        day=22,
        is_raw=False,
        part_num=2,
        expected=23,
    )
