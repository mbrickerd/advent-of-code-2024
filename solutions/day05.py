from typing import List, Tuple

from aoc.models.base import SolutionBase


class Solution(SolutionBase):
    def parse_data(self, data: List[str]) -> Tuple[List[Tuple[int, int]], List[int]]:
        rules, ordering = [part.splitlines() for part in "\n".join(data).split("\n\n")]
        rules = [(int(a), int(b)) for a, b in (rule.split("|") for rule in rules)]
        ordering = [[int(x) for x in line.split(",")] for line in ordering]

        return rules, ordering

    def is_valid_order(self, pages: List[int], rules: List[tuple]) -> bool:
        pos = {num: i for i, num in enumerate(pages)}
        return all(
            pos[before] < pos[after]
            for before, after in rules
            if before in pos and after in pos
        )

    def fix_order(self, pages: List[int], rules: List[tuple]) -> List[int]:
        pages = pages.copy()
        changed = True
        while changed:
            changed = False
            for before, after in rules:
                if before in pages and after in pages:
                    i, j = pages.index(before), pages.index(after)
                    if i > j:  # wrong order
                        pages[j], pages[i] = pages[i], pages[j]
                        changed = True
        return pages

    def part1(self, data: List[str]) -> int:
        rules, ordering = self.parse_data(data)
        return sum(
            pages[len(pages) // 2]
            for pages in ordering
            if self.is_valid_order(pages, rules)
        )

    def part2(self, data: List[str]) -> int:
        rules, ordering = self.parse_data(data)
        return sum(
            self.fix_order(pages, rules)[len(pages) // 2]
            for pages in ordering
            if not self.is_valid_order(pages, rules)
        )
