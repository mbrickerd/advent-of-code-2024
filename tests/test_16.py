from aoc.models.tester import TestSolutionUtility


def test_day16_part1():
    TestSolutionUtility.run_test(
        day=16,
        is_raw=False,
        part_num=1,
        expected=7036,
    )


def test_day16_part2():
    TestSolutionUtility.run_test(
        day=16,
        is_raw=False,
        part_num=2,
        expected=45,
    )
