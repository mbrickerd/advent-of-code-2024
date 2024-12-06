from collections import Counter
from typing import List, Tuple

from aoc.models.base import SolutionBase


class Solution(SolutionBase):
    def load_lists(self, data: List[str]) -> Tuple[List[int], List[int]]:
        return map(list, zip(*(map(int, line.split()) for line in data)))

    def part1(self, data: List[str]) -> int:
        ls1, ls2 = self.load_lists(data)
        ls1.sort(), ls2.sort()

        return sum([abs(ls1[i] - ls2[i]) for i in range(len(data))])

    def part2(self, data: List[str]) -> int:
        ls1, ls2 = self.load_lists(data)
        ls1 = list(set(ls1))
        ls2 = dict(Counter(ls2))

        return sum([item * ls2[item] for item in ls1 if item in ls2.keys()])
