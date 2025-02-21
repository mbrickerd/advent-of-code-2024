"""Day 20: Race Condition.

This module provides the solution for Advent of Code 2024 - Day 20.
It solves a puzzle about finding shortcuts in a racetrack maze,
identifying valid cheat moves that save a minimum number of steps.
"""

from collections import deque

from aoc.models.base import SolutionBase


class Solution(SolutionBase):
    """Solution for Advent of Code 2024 - Day 20: Race Condition.

    This class solves a puzzle about finding shortcuts in a racetrack maze.
    Part 1 finds valid 2-move cheats, while Part 2 finds valid 20-move cheats.
    Both parts count cheats that save a minimum number of steps.

    Input format:
        - Grid representation of the racetrack where:
            * '#' represents walls
            * '.' represents valid path positions
            * 'S' marks the start position
            * 'E' marks the end position
    """

    def parse_data(
        self, data: list[str]
    ) -> tuple[list[list[str]], tuple[int, int], tuple[int, int]]:
        """Parse input data into grid and start/end positions.

        Args:
            data: Raw input lines

        Returns
        -------
            Tuple containing (grid, start_position, end_position)
        """
        grid: list[list[str]] = []
        start: tuple[int, int] | None = None
        end: tuple[int, int] | None = None
        for row in range(len(data)):
            row_data = list(data[row].strip())
            grid.append(row_data)
            for col in range(len(row_data)):
                if row_data[col] == "S":
                    start = (row, col)
                elif row_data[col] == "E":
                    end = (row, col)

        if start is None or end is None:
            error_message = "Start or end position not found in grid"
            raise ValueError(error_message)

        return grid, start, end

    def find_shortest_path(
        self, grid: list[list[str]], start: tuple[int, int], end: tuple[int, int]
    ) -> list[tuple[int, int]] | None:
        """Find the shortest path from start to end in the grid.

        Uses BFS to find the shortest path while avoiding walls.

        Args:
            grid: The maze grid
            start: Starting position (row, col)
            end: Ending position (row, col)

        Returns
        -------
            List of positions in shortest path, or None if no path exists
        """
        rows, cols = len(grid), len(grid[0])
        queue = deque([(start, 0, [start])])
        visited = {start}

        while queue:
            position, steps, path = queue.popleft()
            if position == end:
                return path

            row, col = position
            for dr, dc in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
                new_row, new_col = row + dr, col + dc
                if (
                    0 <= new_row < rows
                    and 0 <= new_col < cols
                    and grid[new_row][new_col] != "#"
                    and (new_row, new_col) not in visited
                ):
                    visited.add((new_row, new_col))
                    queue.append(((new_row, new_col), steps + 1, [*path, (new_row, new_col)]))

        return None

    def find_cheat_pairs(self, path: list[tuple[int, int]], savings: int, cheat_moves: int) -> int:
        """Find valid cheat moves that save the required number of steps.

        Args:
            path: The shortest path from start to end
            savings: Minimum number of steps a cheat must save
            cheat_moves: Maximum number of moves allowed for a cheat

        Returns
        -------
            Number of valid cheats found
        """
        # Optimize by pre-computing position indices in the path
        coords_steps = {coord: i for i, coord in enumerate(path)}
        cheats = 0

        # Pre-compute all possible cheat move ranges
        possible_ranges = [
            (dy, dx, abs(dy) + abs(dx))
            for dy in range(-cheat_moves, cheat_moves + 1)
            for dx in range(-cheat_moves, cheat_moves + 1)
            if 0 < abs(dy) + abs(dx) <= cheat_moves
        ]

        for y, x in path:
            for dy, dx, manhattan in possible_ranges:
                ny, nx = y + dy, x + dx
                if (ny, nx) in coords_steps:
                    steps_saved = coords_steps[(ny, nx)] - coords_steps[(y, x)] - manhattan
                    if steps_saved >= savings:
                        cheats += 1

        return cheats

    def solve_part(self, data: list[str], cheat_moves: int) -> int:
        """Solve the puzzle for the given cheat move limit.

        Args:
            data: Input data lines
            cheat_moves: Maximum number of moves allowed for cheats

        Returns
        -------
            Number of valid cheats found
        """
        grid, start, end = self.parse_data(data)
        path = self.find_shortest_path(grid, start, end)
        if path is None:
            return 0

        return self.find_cheat_pairs(path, savings=2, cheat_moves=cheat_moves)

    def part1(self, data: list[str]) -> int:
        """Count valid cheats using maximum 2-move teleports.

        Args:
            data: Input lines containing the maze grid with start 'S' and end 'E'

        Returns
        -------
            Number of valid 2-move cheats that save at least 2 steps
        """
        return self.solve_part(data, cheat_moves=2)

    def part2(self, data: list[str]) -> int:
        """Count valid cheats using maximum 20-move teleports.

        Args:
            data: Input lines containing the maze grid with start 'S' and end 'E'

        Returns
        -------
            Number of valid 20-move cheats that save at least 2 steps
        """
        return self.solve_part(data, cheat_moves=20)
