from aoc.models.tester import TestSolutionUtility

def test_day05_part1():
    TestSolutionUtility.run_test(
        day=5, 
        is_raw=False, 
        part_num=1, 
        expected=143,
    )

def test_day05_part2():
    TestSolutionUtility.run_test(
        day=5, 
        is_raw=False,  
        part_num=2, 
        expected=123,
    )

