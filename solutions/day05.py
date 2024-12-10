from typing import List, Tuple

from aoc.models.base import SolutionBase


class Solution(SolutionBase):
    """Solution for Advent of Code 2024 - Day 5: Print Queue.

    This class solves a puzzle involving print job ordering with specific sequencing rules.
    Part 1 sums middle pages from valid print orders, while Part 2 fixes invalid orders
    and sums their middle pages. Rules specify which pages must be printed before others.

    Input format:
        - Rules section: Lines of "page1|page2" meaning `page1` must print before `page2`
        - Orders section: Lines of comma-separated page numbers representing print orders

    This class inherits from `SolutionBase` and provides methods to validate and fix
    print job orderings according to sequencing rules.
    """

    def parse_data(
        self, data: List[str]
    ) -> Tuple[List[Tuple[int, int]], List[List[int]]]:
        """Parse input into rules and print orders.

        Args:
            data (List[str]): Raw input lines containing rules section followed by
                orders section, separated by blank line.

        Returns:
            Tuple containing:
                - List[Tuple[int, int]]: Pairs of (before, after) page numbers from rules
                - List[List[int]]: Lists of page numbers representing print orders

                Example:
                For input:
                    "1|2"
                    "2|3"

                    "1,2,3"
                    "3,1,2"
                Returns: ([(1,2), (2,3)], [[1,2,3], [3,1,2]])
        """
        rules, ordering = [part.splitlines()
                           for part in "\n".join(data).split("\n\n")]
        rules = [(int(a), int(b))
                 for a, b in (rule.split("|") for rule in rules)]
        ordering = [[int(x) for x in line.split(",")] for line in ordering]

        return rules, ordering

    def is_valid_order(self, pages: List[int], rules: List[Tuple[int, int]]) -> bool:
        """Check if a print order satisfies all sequencing rules.

        Args:
            pages (List[int]): List of page numbers in their print order
            rules (List[Tuple[int, int]]): List of (before, after) pairs specifying required ordering

        Returns:
            bool: `True` if all rules are satisfied (each 'before' page appears before its
                corresponding 'after' page), `False` otherwise. For example:
                - pages=[1,2,3], rules=[(1,2), (2,3)] returns True
                - pages=[2,1,3], rules=[(1,2)] returns False
        """
        position = {num: i for i, num in enumerate(pages)}
        return all(
            position[before] < position[after]
            for before, after in rules
            if before in position and after in position
        )

    def fix_order(self, pages: List[int], rules: List[tuple]) -> List[int]:
        """Fix an invalid print order by swapping pages until all rules are satisfied.

        Args:
            pages (List[int]): List of page numbers in their current order
            rules (List[tuple]): List of (before, after) pairs specifying required ordering

        Returns:
            List[int]: New list with pages reordered to satisfy all rules. For example:
                - pages=[2,1,3], rules=[(1,2)] returns [1,2,3]
                - pages=[3,1,2], rules=[(1,2), (2,3)] returns [1,2,3]
        """
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
        """Sum middle pages from valid print orders.

        Args:
            data (List[str]): Raw input containing rules and print orders.

        Returns:
            int: Sum of middle page numbers from all valid print orders
                (orders that already satisfy all rules).
        """
        rules, ordering = self.parse_data(data)
        return sum(
            pages[len(pages) // 2]
            for pages in ordering
            if self.is_valid_order(pages, rules)
        )

    def part2(self, data: List[str]) -> int:
        """Sum middle pages from fixed invalid print orders.

        Args:
            data (List[str]): Raw input containing rules and print orders.

        Returns:
            int: Sum of middle page numbers from all fixed invalid orders
                (only considering orders that initially violated rules).
        """
        rules, ordering = self.parse_data(data)
        return sum(
            self.fix_order(pages, rules)[len(pages) // 2]
            for pages in ordering
            if not self.is_valid_order(pages, rules)
        )
