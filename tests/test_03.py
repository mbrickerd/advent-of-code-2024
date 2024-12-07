from aoc.models.tester import TestSolutionUtility

def test_day03_part1():
    TestSolutionUtility.run_test(
        day=3, 
        is_raw=False, 
        part_num=1, 
        expected=161,
    )

def test_day03_part2():
    TestSolutionUtility.run_test(
        day=3, 
        is_raw=False,  
        part_num=2, 
        expected=48,
    )

