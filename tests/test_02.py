from aoc.models.tester import TestSolutionUtility

def test_day02_part1():
    TestSolutionUtility.run_test(
        day=2, 
        is_raw=False, 
        part_num=1, 
        expected=2,
    )

def test_day02_part2():
    TestSolutionUtility.run_test(
        day=2, 
        is_raw=False,  
        part_num=2, 
        expected=4,
    )

