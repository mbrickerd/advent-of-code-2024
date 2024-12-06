from typing import List

from aoc.models.base import SolutionBase


class Solution(SolutionBase):    
    def is_increasing(self, ls: List[int]) -> bool:
        return all(x < y for x, y in zip(ls, ls[1:]))
    
    def is_decreasing(self, ls: List[int]) -> bool:
        return all(x > y for x, y in zip(ls, ls[1:]))
    
    def abs_differences(self, ls: List[int]) -> List[int]:
        return [abs(x - y) for x, y in zip(ls, ls[1:])]
    
    def between_range(self, ls: List[int]) -> bool:
        return all(1 <= x <= 3 for x in self.abs_differences(ls))

    def part1(self, data: List[str]) -> int:
        return sum([
            1 
            for ls in [list(map(int, line.split())) for line in data] 
            if (self.is_increasing(ls) or self.is_decreasing(ls))
            and self.between_range(ls)
        ])
    
    def part2(self, data: List[str]) -> int:
        return sum(
            any(
                (self.is_increasing(ls[:i] + ls[i+1:]) or self.is_decreasing(ls[:i] + ls[i+1:])) 
                and self.between_range(ls[:i] + ls[i+1:])
                for i in range(len(ls))
            ) or (
                (self.is_increasing(ls) or self.is_decreasing(ls)) 
                and self.between_range(ls)
            )
            for ls in [list(map(int, line.split())) for line in data]
        )
