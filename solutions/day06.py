from copy import deepcopy
from typing import List, Tuple

from aoc.models.base import SolutionBase


class Solution(SolutionBase):
    """Solution for Advent of Code 2024 - Day 6: Guard Gallivant.

    This class simulates a guard's movement through a grid following specific rules.
    The guard starts at a position with a direction (^>v<) and moves forward until
    hitting a wall (#), which causes them to turn right. Part 1 calculates path length
    until escape/loop, while Part 2 counts possible loops created by adding walls.

    Grid elements:
        - "." : Empty space the guard can move through
        - "#" : Wall that causes the guard to turn right
        - ^>v< : Starting position and initial direction

    This class inherits from `SolutionBase` and provides methods to simulate
    guard movement and analyze possible paths.
    """

    moves = {"^": (-1, 0), ">": (0, 1), "v": (1, 0), "<": (0, -1)}  # Direction vectors
    turns = {"^": ">", ">": "v", "v": "<", "<": "^"}  # Right turn mappings

    def find_start(self, grid: List[List[str]]) -> Tuple[int, int, str]:
        """Find guard's starting position and direction in the grid.

        Args:
            grid (List[List[str]]): 2D grid where each cell is ".", "#", or a direction

        Returns:
            Tuple[int, int, str]: Row index, column index, and direction character
                of the guard's start position.
        """
        return next((i, j, char) for i, row in enumerate(grid) for j, char in enumerate(row) if char in "^>v<")

    def get_next_position(self, row: int, col: int, dir: str) -> Tuple[int, int]:
        """Calculate next position based on current position and direction.

        Args:
            row (int): Current row index
            col (int): Current column index
            dir (str): Current direction ("^", ">", "v", or "<")

        Returns:
            Tuple[int, int]: Next row and column indices after moving one step
                in the current direction.
        """
        dr, dc = self.moves[dir]
        return row + dr, col + dc

    def is_valid(self, row: int, col: int, grid: List[List[str]]) -> bool:
        """Check if a position is within grid bounds.

        Args:
            row (int): Row index to check
            col (int): Column index to check
            grid (List[List[str]]): 2D grid

        Returns:
            bool: True if position is within grid bounds, False otherwise
        """
        return 0 <= row < len(grid) and 0 <= col < len(grid[0])

    def simulate(self, grid: List[List[str]], find_loops: bool = False) -> int:
        """Simulate guard's movement through the grid.

        Args:
            grid (List[List[str]]): 2D grid representing the patrol area
            find_loops (bool): If True, return whether path forms a loop instead
                of path length

        Returns:
            If find_loops is `False`:
                int: Number of unique positions visited before escaping or looping
            If find_loops is `True`:
                bool: `True` if path forms a loop, `False` if guard escapes
        """
        row, col, dir = self.find_start(grid)
        seen = {(row, col, dir)}  # Track visited positions with direction
        path = {(row, col)}  # Track unique positions visited

        while True:
            nr, nc = self.get_next_position(row, col, dir)
            if not self.is_valid(nr, nc, grid):
                return len(path) if not find_loops else False

            if grid[nr][nc] == "#":
                dir = self.turns[dir]  # Turn right at wall
                if (row, col, dir) in seen:
                    return len(path) if not find_loops else True

            else:
                row, col = nr, nc
                if (row, col, dir) in seen:
                    return len(path) if not find_loops else True

            seen.add((row, col, dir))
            path.add((row, col))

    def part1(self, data: List[str]) -> int:
        """Calculate number of positions visited before guard escapes or loops.

        Args:
            data (List[str]): Input grid rows as strings

        Returns:
            int: Number of unique positions the guard visits before either
                escaping the grid or entering a loop.
        """
        return self.simulate([list(row) for row in data])

    def part2(self, data: List[str]) -> int:
        """Count how many possible wall placements create loops.

        Tests placing a wall at each empty position (except start) and counts
        how many of these modifications cause the guard's path to loop.

        Args:
            data (List[str]): Input grid rows as strings

        Returns:
            int: Number of possible wall placements that result in the guard's
                path forming a loop.
        """
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
