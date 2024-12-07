from copy import deepcopy
from typing import List, Tuple

from aoc.models.base import SolutionBase


class Solution(SolutionBase):
    moves = {"^": (-1, 0), ">": (0, 1), "v": (1, 0), "<": (0, -1)}
    turns = {"^": ">", ">": "v", "v": "<", "<": "^"}

    def find_start(self, grid: List[List[str]]) -> Tuple[int, int, str]:
        return next(
            (i, j, char)
            for i, row in enumerate(grid)
            for j, char in enumerate(row)
            if char in "^>v<"
        )

    def get_next_pos(self, row: int, col: int, dir: str) -> Tuple[int, int]:
        dr, dc = self.moves[dir]
        return row + dr, col + dc

    def is_valid(self, row: int, col: int, grid: List[List[str]]) -> bool:
        return 0 <= row < len(grid) and 0 <= col < len(grid[0])

    def simulate(self, grid: List[List[str]], find_loops: bool = False) -> int:
        row, col, dir = self.find_start(grid)
        seen = {(row, col, dir)}
        path = {(row, col)}

        while True:
            nr, nc = self.get_next_pos(row, col, dir)
            if not self.is_valid(nr, nc, grid):
                return len(path) if not find_loops else False

            if grid[nr][nc] == "#":
                dir = self.turns[dir]
                if (row, col, dir) in seen:
                    return len(path) if not find_loops else True

            else:
                row, col = nr, nc
                if (row, col, dir) in seen:
                    return len(path) if not find_loops else True

            seen.add((row, col, dir))
            path.add((row, col))

    def part1(self, data: List[str]) -> int:
        return self.simulate([list(row) for row in data])

    def part2(self, data: List[str]) -> int:
        grid = [list(row) for row in data]
        row, col, _ = self.find_start(grid)
        loops = 0

        for i in range(len(grid)):
            for j in range(len(grid[0])):
                if grid[i][j] == "." and (i, j) != (row, col):
                    test_grid = deepcopy(grid)
                    test_grid[i][j] = "#"
                    loops += self.simulate(test_grid, True)

        return loops
