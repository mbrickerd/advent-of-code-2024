from aoc.models.tester import TestSolutionUtility


def test_day24_part1():
    TestSolutionUtility.run_test(
        day=24,
        is_raw=False,
        part_num=1,
        expected=4,
    )


def test_day24_part2():
    TestSolutionUtility.run_test(
        day=24,
        is_raw=False,
        part_num=2,
        expected="z00,z01,z02,z05",
    )
