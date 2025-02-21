"""Day 18: RAM Run.

This module provides the solution for Advent of Code 2024 - Day 18.
It solves a pathfinding problem in a corrupted memory grid where bytes fall and block
specific coordinates. The solution finds paths through uncorrupted spaces and
determines which falling byte first makes the exit unreachable.
"""

from collections import deque

from aoc.models.base import SolutionBase


class Solution(SolutionBase):
    """Solution for Advent of Code 2024 - Day 18: RAM Run.

    This class solves a puzzle involving pathfinding in a corrupted memory grid.
    The grid represents a memory space where falling bytes corrupt specific coordinates.
    Part 1 finds the shortest path from start to exit through uncorrupted spaces, while
    Part 2 determines which falling byte first makes the exit unreachable.

    Input format:
        - Multiple lines where:
            Each line contains a coordinate pair "x,y" representing where a byte falls
            Coordinates start from (0,0) at the top-left corner

    This class inherits from `SolutionBase` and provides methods to construct grids,
    find paths, and analyze byte corruption patterns using breadth-first search.
    """

    def _parse_coordinates(self, data: list[str]) -> tuple[list[tuple[int, int]], int]:
        """Parse input data and determine grid size.

        Args:
            data: Input lines containing byte fall coordinates

        Returns
        -------
            tuple[list[tuple[int, int]], int]: Tuple containing coordinates list and grid size
        """
        coordinates: list[tuple[int, int]] = []
        for row in data:
            x, y = map(int, row.split(","))
            coordinates.append((x, y))

        grid_size = max(max(x, y) for x, y in coordinates) + 1

        return coordinates, grid_size

    def construct_grid(
        self,
        size: int,
        coordinates: list[tuple[int, int]],
        limit: int,
    ) -> list[list[bool]]:
        """Construct a grid representation using booleans for efficient access.

        Args:
            size: Size of the grid (both width and height)
            coordinates: List of (x,y) coordinates where bytes fall
            limit: Number of coordinates to process

        Returns
        -------
            Grid where False represents safe cells and True represents corrupted cells
        """
        # Using boolean grid for faster access (True = corrupted)
        grid = [[False] * size for _ in range(size)]

        for col, row in coordinates[:limit]:
            grid[row][col] = True

        return grid

    def has_path(self, grid: list[list[bool]]) -> bool:
        """Check if there exists any path from start to end.

        Args:
            grid: Current state of the memory space

        Returns
        -------
            True if a path exists to the exit, False otherwise
        """
        size = len(grid)

        # Early checks
        if grid[0][0] or grid[size - 1][size - 1]:
            return False

        directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
        queue = deque([(0, 0)])
        seen = {(0, 0)}

        while queue:
            x, y = queue.popleft()

            if x == size - 1 and y == size - 1:
                return True

            for dx, dy in directions:
                nx, ny = x + dx, y + dy
                pos = (nx, ny)

                if 0 <= nx < size and 0 <= ny < size and not grid[ny][nx] and pos not in seen:
                    seen.add(pos)
                    queue.append(pos)

        return False

    def find_shortest_path(self, grid: list[list[bool]]) -> int:
        """Find the shortest path from start to end.

        Args:
            grid: Current state of the memory space

        Returns
        -------
            Length of shortest path to exit, or -1 if no path exists
        """
        size = len(grid)

        # Early checks
        if grid[0][0] or grid[size - 1][size - 1]:
            return -1

        directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
        queue = deque([(0, 0, 0)])  # (x, y, distance)
        seen = {(0, 0)}

        while queue:
            x, y, dist = queue.popleft()

            if x == size - 1 and y == size - 1:
                return dist

            for dx, dy in directions:
                nx, ny = x + dx, y + dy
                pos = (nx, ny)

                if 0 <= nx < size and 0 <= ny < size and not grid[ny][nx] and pos not in seen:
                    seen.add(pos)
                    queue.append((nx, ny, dist + 1))

        return -1

    def part1(self, data: list[str]) -> int:
        """Find shortest path to exit after initial byte corruption.

        Args:
            data: Input lines containing byte fall coordinates

        Returns
        -------
            Length of shortest path to exit, or -1 if no path exists
        """
        coordinates, grid_size = self._parse_coordinates(data)
        limit = 12 if len(coordinates) <= 25 else 1024
        grid = self.construct_grid(grid_size, coordinates, limit)
        return self.find_shortest_path(grid)

    def part2(self, data: list[str]) -> str:
        """Find coordinates of first byte that makes exit unreachable.

        Args:
            data: Input lines containing byte fall coordinates

        Returns
        -------
            Coordinates of blocking byte as "x,y" string
        """
        coordinates, grid_size = self._parse_coordinates(data)

        # Binary search to find critical byte
        left, right = 0, len(coordinates)

        # Early termination if no initial path exists
        if not self.has_path(self.construct_grid(grid_size, coordinates, 0)):
            return "No initial path exists"

        while right - left > 1:
            mid = (left + right) // 2
            if self.has_path(self.construct_grid(grid_size, coordinates, mid)):
                left = mid
            else:
                right = mid

        blocking_coord = coordinates[right - 1]
        return f"{blocking_coord[0]},{blocking_coord[1]}"
