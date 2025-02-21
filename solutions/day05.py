"""Day 5: Print Queue.

This module provides the solution for Advent of Code 2024 - Day 5.
It processes print job ordering challenges according to specific sequencing rules.

The solution validates print orders against rules specifying which pages must be
printed before others, calculates middle pages of valid orders (Part 1), and
fixes invalid orders before calculating their middle pages (Part 2).
"""

from aoc.models.base import SolutionBase


class Solution(SolutionBase):
    """Print job ordering with sequencing rules.

    This solution implements print queue validation and correction algorithms:
    - Part 1: Find valid print orders and sum their middle pages
    - Part 2: Fix invalid print orders and sum their middle pages

    Input format:
        - Rules section: Lines of "page1|page2" meaning `page1` must print before `page2`
        - Orders section: Lines of comma-separated page numbers representing print orders
    """

    def parse_data(self, data: list[str]) -> tuple[list[tuple[int, int]], list[list[int]]]:
        """Parse input into rules and print orders.

        Args:
            data (list[str]): Raw input lines containing rules section followed by
                orders section, separated by blank line.

        Returns
        -------
            tuple containing:
                - list[tuple[int, int]]: Pairs of (before, after) page numbers from rules
                - list[list[int]]: Lists of page numbers representing print orders
        """
        parts = "\n".join(data).split("\n\n")
        rules = [(int(a), int(b)) for rule in parts[0].splitlines() for a, b in [rule.split("|")]]
        ordering = [[int(x) for x in line.split(",")] for line in parts[1].splitlines()]
        return rules, ordering

    def is_valid_order(self, pages: list[int], rules: list[tuple[int, int]]) -> bool:
        """Check if a print order satisfies all sequencing rules.

        Args:
            pages (list[int]): List of page numbers in their print order
            rules (list[tuple[int, int]]): List of (before, after) pairs specifying
                required ordering

        Returns
        -------
            bool: `True` if all rules are satisfied (each 'before' page appears before its
                corresponding 'after' page), `False` otherwise. For example:
                - pages=[1,2,3], rules=[(1,2), (2,3)] returns True
                - pages=[2,1,3], rules=[(1,2)] returns False
        """
        position = {num: i for i, num in enumerate(pages)}
        return all(
            position.get(before, float("inf")) < position.get(after, float("-inf"))
            for before, after in rules
            if before in position and after in position
        )

    def fix_order(self, pages: list[int], rules: list[tuple[int, int]]) -> list[int]:
        """Fix an invalid print order by swapping pages until all rules are satisfied.

        Args:
            pages (list[int]): List of page numbers in their current order
            rules (list[tuple]): List of (before, after) pairs specifying required ordering

        Returns
        -------
            list[int]: New list with pages reordered to satisfy all rules. For example:
                - pages=[2,1,3], rules=[(1,2)] returns [1,2,3]
                - pages=[3,1,2], rules=[(1,2), (2,3)] returns [1,2,3]
        """
        result = pages.copy()
        changed = True

        while changed:
            changed = False
            for before, after in rules:
                if before in result and after in result:
                    i, j = result.index(before), result.index(after)
                    if i > j:
                        result[j], result[i] = result[i], result[j]
                        changed = True

        return result

    def part1(self, data: list[str]) -> int:
        """Sum middle pages from valid print orders.

        Args:
            data (list[str]): Raw input containing rules and print orders.

        Returns
        -------
            int: Sum of middle page numbers from all valid print orders
                (orders that already satisfy all rules).
        """
        rules, ordering = self.parse_data(data)
        return sum(
            pages[len(pages) // 2] for pages in ordering if self.is_valid_order(pages, rules)
        )

    def part2(self, data: list[str]) -> int:
        """Sum middle pages from fixed invalid print orders.

        Args:
            data (list[str]): Raw input containing rules and print orders.

        Returns
        -------
            int: Sum of middle page numbers from all fixed invalid orders
                (only considering orders that initially violated rules).
        """
        rules, ordering = self.parse_data(data)
        return sum(
            self.fix_order(pages, rules)[len(pages) // 2]
            for pages in ordering
            if not self.is_valid_order(pages, rules)
        )
