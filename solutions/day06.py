"""Day 6: Guard Gallivant.

This module provides the solution for Advent of Code 2024 - Day 6.
It simulates a guard's movement through a grid following specific rules.

The module tracks a guard that moves along a grid with walls, calculating path
properties for Part 1 (path length) and Part 2 (counting loops created by adding walls).
"""

from typing import ClassVar, Literal, cast

from aoc.models.base import SolutionBase


class Solution(SolutionBase):
    """Guard movement simulation through a grid with walls.

    This solution implements guard movement algorithms:
    - Part 1: Calculate path length until escape/loop
    - Part 2: Count possible loops created by adding walls

    Grid elements:
        - "." : Empty space the guard can move through
        - "#" : Wall that causes the guard to turn right
        - ^>v< : Starting position and initial direction
    """

    moves: ClassVar[dict[str, tuple[int, int]]] = {
        "^": (-1, 0),
        ">": (0, 1),
        "v": (1, 0),
        "<": (0, -1),
    }
    turns: ClassVar[dict[str, str]] = {"^": ">", ">": "v", "v": "<", "<": "^"}

    def simulate(
        self, grid: list[list[str]], detect_loops: Literal[True] | None = None
    ) -> int | bool:
        """Simulate guard's movement through the grid.

        Args:
            grid: 2D grid representing the patrol area
            detect_loops: When True, return whether path forms a loop instead of
                path length

        Returns
        -------
            Number of unique positions visited (detect_loops=None)
            Whether path forms a loop (detect_loops=True)
        """
        # Find starting position
        rows, cols = len(grid), len(grid[0])

        # Fast starting position search
        row, col, direction = -1, -1, ""
        found = False
        for i in range(rows):
            for j in range(cols):
                if grid[i][j] in "^>v<":
                    row, col, direction = i, j, grid[i][j]
                    found = True
                    break

            if found:
                break

        if not found:
            error_message = "No starting position found in grid"
            raise ValueError(error_message)

        seen = {(row, col, direction)}
        path = {(row, col)}

        while True:
            dr, dc = self.moves[direction]
            nr, nc = row + dr, col + dc

            # Check if guard escapes grid bounds
            if not (0 <= nr < rows and 0 <= nc < cols):
                return False if detect_loops is True else len(path)

            # Handle wall collision (turn right)
            if grid[nr][nc] == "#":
                direction = self.turns[direction]
                state = (row, col, direction)
                if state in seen:
                    return True if detect_loops is True else len(path)

            # Move forward
            else:
                row, col = nr, nc
                state = (row, col, direction)
                if state in seen:
                    return True if detect_loops is True else len(path)

            seen.add(state)
            path.add((row, col))

    def part1(self, data: list[str]) -> int:
        """Calculate number of positions visited before guard escapes or loops.

        Args:
            data: Input grid rows as strings

        Returns
        -------
            Number of unique positions visited before escaping or looping
        """
        grid = [list(row) for row in data]
        return cast(int, self.simulate(grid))

    def part2(self, data: list[str]) -> int:
        """Count how many possible wall placements create loops.

        Tests placing a wall at each empty position (except start) and counts
        how many modifications cause the guard's path to loop.

        Args:
            data: Input grid rows as strings

        Returns
        -------
            Number of possible wall placements creating loops
        """
        grid = [list(row) for row in data]
        rows, cols = len(grid), len(grid[0])

        # Find starting position
        start_positions = [(i, j) for i in range(rows) for j in range(cols) if grid[i][j] in "^>v<"]
        start_row, start_col = start_positions[0]

        loops = 0
        for i in range(rows):
            for j in range(cols):
                if grid[i][j] == "." and (i, j) != (start_row, start_col):
                    grid[i][j] = "#"
                    if self.simulate(grid, detect_loops=True) is True:
                        loops += 1

                    grid[i][j] = "."

        return loops
