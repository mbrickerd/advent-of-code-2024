from typing import List

from aoc.models.base import SolutionBase


class Solution(SolutionBase):
    def check_mas(self, data: List[str], r: int, c: int, dr: int, dc: int) -> bool:
        rows, cols = len(data), len(data[0])
        pattern = "MAS"
        return all(
            0 <= r + i * dr < rows
            and 0 <= c + i * dc < cols
            and data[r + i * dr][c + i * dc] == pattern[i]
            for i in range(3)
        )

    def part1(self, data: List[str]) -> int:
        rows, cols = len(data), len(data[0])
        directions = [
            (0, 1),
            (1, 1),
            (1, 0),
            (1, -1),
            (0, -1),
            (-1, -1),
            (-1, 0),
            (-1, 1),
        ]
        count = 0

        for r in range(rows):
            for c in range(cols):
                for dr, dc in directions:
                    if all(
                        0 <= r + i * dr < rows
                        and 0 <= c + i * dc < cols
                        and data[r + i * dr][c + i * dc] == "XMAS"[i]
                        for i in range(4)
                    ):
                        count += 1

        return count

    def part2(self, data: List[str]) -> int:
        count = 0
        rows, cols = len(data), len(data[0])

        for r in range(1, rows - 1):
            for c in range(1, cols - 1):
                if data[r][c] != "A":
                    continue

                # Only check one diagonal direction - it's enough to find all X patterns
                dr, dc = 1, 1
                if (
                    self.check_mas(data, r - dr, c - dc, dr, dc)
                    or self.check_mas(data, r + dr, c + dc, -dr, -dc)
                ) and (
                    self.check_mas(data, r - dr, c + dc, dr, -dc)
                    or self.check_mas(data, r + dr, c - dc, -dr, dc)
                ):
                    count += 1

        return count
