from aoc.models.tester import TestSolutionUtility


def test_day23_part1():
    TestSolutionUtility.run_test(
        day=23,
        is_raw=False,
        part_num=1,
        expected=7,
    )


def test_day23_part2():
    TestSolutionUtility.run_test(
        day=23,
        is_raw=False,
        part_num=2,
        expected="co,de,ka,ta",
    )
