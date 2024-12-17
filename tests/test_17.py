from aoc.models.tester import TestSolutionUtility


def test_day17_part1():
    TestSolutionUtility.run_test(
        day=17,
        is_raw=False,
        part_num=1,
        expected="4,6,3,5,6,3,5,2,1,0",
    )


def test_day17_part2():
    TestSolutionUtility.run_test(
        day=17,
        is_raw=False,
        part_num=2,
        expected=117440,
    )
