"""Day 16: Reindeer Maze.

This module provides the solution for Advent of Code 2024 - Day 16.
It finds optimal paths through a maze with different movement costs,
tracking both minimum cost paths and tiles used in optimal routes.

The maze is represented as a grid where '#' marks walls, 'S' marks the
starting position, 'E' marks the ending position, and '.' represents
empty spaces. Reindeer start facing east and can move forward (cost 1)
or rotate 90 degrees (cost 1000).
"""

from collections import deque
from typing import ClassVar

from aoc.models.base import SolutionBase


class Solution(SolutionBase):
    """Solution for Advent of Code 2024 - Day 16: Reindeer Maze.

    Solves a maze routing problem with specific movement costs:
    - Forward movement costs 1 unit
    - 90-degree rotation costs 1000 units
    - Can't move backward without rotating first

    Input format:
        Grid of characters where:
        - '#' represents walls
        - 'S' represents the starting position
        - 'E' represents the ending position
        - '.' represents empty space
    """

    directions: ClassVar[list[tuple[int, int]]] = [
        (0, 1),  # right
        (-1, 0),  # up
        (0, -1),  # left
        (1, 0),  # down
    ]

    def find_start_end(self, grid: list[list[str]]) -> tuple[tuple[int, int], tuple[int, int]]:
        """Find the start and end positions in the maze.

        Args:
            grid: 2D grid representation of the maze

        Returns
        -------
            Tuple of (start_coordinates, end_coordinates)
        """
        start: tuple[int, int] | None = None
        end: tuple[int, int] | None = None

        for y, row in enumerate(grid):
            for x, cell in enumerate(row):
                if cell == "S":
                    start = (y, x)

                elif cell == "E":
                    end = (y, x)

                if start and end:
                    return start, end

        if not start or not end:
            error_message = "Could not find start or end position"
            raise ValueError(error_message)

        return start, end

    def find_routes(self, data: list[str]) -> list[tuple[list[tuple[int, int]], int]]:
        """Find all possible routes through the maze and their costs.

        Uses breadth-first search to explore the maze, tracking:
        - Complete path history for each route
        - Movement costs (forward=1, rotation=1000)
        - Direction facing (0=right, 1=up, 2=left, 3=down)
        - Previously visited states to avoid cycles

        Args:
            data: Input lines representing the maze grid

        Returns
        -------
            List of tuples containing (path_coordinates, total_cost)
        """
        grid = [list(row) for row in data]
        start, end = self.find_start_end(grid)
        routes: list[tuple[list[tuple[int, int]], int]] = []
        visited: dict[tuple[tuple[int, int], int], int] = {}

        queue = deque([(start, [start], 0, 0)])  # Start facing right (0)

        while queue:
            pos, history, curr_score, curr_dir = queue.popleft()
            y, x = pos

            if pos == end:
                routes.append((history, curr_score))
                continue

            state = (pos, curr_dir)
            if state in visited and visited[state] < curr_score:
                continue

            visited[state] = curr_score

            for new_dir, (dy, dx) in enumerate(self.directions):
                if (curr_dir + 2) % 4 == new_dir:
                    continue

                new_y, new_x = y + dy, x + dx
                new_pos = (new_y, new_x)

                if (
                    0 <= new_y < len(grid)
                    and 0 <= new_x < len(grid[0])
                    and grid[new_y][new_x] != "#"
                    and new_pos not in history
                ):
                    if new_dir == curr_dir:
                        queue.append(
                            (
                                new_pos,
                                [*history, new_pos],
                                curr_score + 1,
                                new_dir,
                            )
                        )

                    else:
                        queue.append((pos, history, curr_score + 1000, new_dir))

        return routes

    def part1(self, data: list[str]) -> int:
        """Find the minimum cost to reach the end of the maze.

        Args:
            data: Input lines representing the maze grid

        Returns
        -------
            Minimum total cost (moves + rotations) to reach the end
        """
        possible_routes = self.find_routes(data)
        return min(route[1] for route in possible_routes)

    def part2(self, data: list[str]) -> int:
        """Count tiles that are part of any optimal path through the maze.

        Args:
            data: Input lines representing the maze grid

        Returns
        -------
            Number of unique tiles in any minimum-cost path
        """
        possible_routes = self.find_routes(data)
        min_score = min(route[1] for route in possible_routes)
        best_routes = [route for route in possible_routes if route[1] == min_score]
        optimal_tiles = {tile for route in best_routes for tile in route[0]}
        return len(optimal_tiles)
