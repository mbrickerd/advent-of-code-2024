from collections import deque
from typing import List, Optional, Tuple

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

    The solution finds the shortest path from `S` to `E` and then identifies valid
    cheat moves that save steps by passing through walls.

    This class inherits from `SolutionBase` and implements the required methods
    to parse input data and solve both parts of the puzzle. It provides helpers
    for path finding and cheat detection.
    """

    def parse_data(
        self, data: List[str]
    ) -> Tuple[List[List[str]], Tuple[int, int], Tuple[int, int]]:
        """Parse input data into grid and start/end positions.

        Args:
            data (List[str]): Raw input lines

        Returns:
            Tuple[List[List[str]], Tuple[int, int], Tuple[int, int]]:
                Tuple containing (grid, start_position, end_position)
        """
        grid, start, end = [], None, None
        for row in range(len(data)):
            row_data = list(data[row].strip())
            grid.append(row_data)
            for col in range(len(row_data)):
                if row_data[col] == "S":
                    start = (row, col)
                elif row_data[col] == "E":
                    end = (row, col)

        return grid, start, end

    def find_shortest_path(
        self, grid: List[List[str]], start: Tuple[int, int], end: Tuple[int, int]
    ) -> Optional[List[Tuple[int, int]]]:
        """Find the shortest path from start to end in the grid.

        Uses BFS to find the shortest path while avoiding walls.

        Args:
            grid (List[List[str]]): The maze grid
            start (Tuple[int, int]): Starting position (row, col)
            end (Tuple[int, int]): Ending position (row, col)

        Returns:
            Optional[List[Tuple[int, int]]]: List of positions in shortest path,
                or None if no path exists
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
                    queue.append(((new_row, new_col), steps + 1, path + [(new_row, new_col)]))

        return None

    def find_cheat_pairs(self, path: List[Tuple[int, int]], savings: int, cheat_moves: int) -> int:
        """Find valid cheat moves that save the required number of steps.

        Args:
            path (List[Tuple[int, int]]): The shortest path from start to end
            savings (int): Minimum number of steps a cheat must save
            cheat_moves (int): Maximum number of moves allowed for a cheat

        Returns:
            int: Number of valid cheats found
        """
        coords_steps = {coord: i for i, coord in enumerate(path)}
        cheats = 0

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

    def solve_part(self, data: List[str], cheat_moves: int) -> int:
        """Common solution logic for both parts.

        Args:
            data (List[str]): Input data lines
            cheat_moves (int): Maximum number of moves allowed for cheats

        Returns:
            int: Number of valid cheats found
        """
        grid, start, end = self.parse_data(data)
        path = self.find_shortest_path(grid, start, end)
        if path is None:
            return 0

        return self.find_cheat_pairs(path, savings=2, cheat_moves=cheat_moves)

    def part1(self, data: List[str]) -> int:
        """Count valid cheats using maximum 2-move teleports.

        Finds all valid ways to cheat through walls using at most 2 moves in any direction.
        A valid cheat must return to a normal path position after teleporting and must
        save at least the required number of steps compared to the normal path.

        Args:
            data (List[str]): Input lines containing the maze grid with start 'S' and end 'E'

        Returns:
            int: Number of valid cheats found that save the required minimum steps
        """
        return self.solve_part(data, cheat_moves=2)

    def part2(self, data: List[str]) -> int:
        """Count valid cheats using maximum 20-move teleports.

        Similar to part 1, but allows for longer teleport distances of up to 20 moves.
        This enables finding shortcuts that bypass larger sections of walls, but still
        requires ending on a valid path position and saving the minimum required steps.

        Args:
            data (List[str]): Input lines containing the maze grid with start 'S' and end 'E'

        Returns:
            int: Number of valid cheats found that save the required minimum steps
        """
        return self.solve_part(data, cheat_moves=20)
