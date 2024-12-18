from collections import deque
from typing import List, Tuple

from aoc.models.base import SolutionBase


class Solution(SolutionBase):
    """Solution for Advent of Code 2024 - Day 18: RAM Run.

    This class solves a puzzle involving pathfinding in a corrupted memory space.
    The memory space is represented as a grid where bytes fall and corrupt specific
    coordinates. Part 1 finds the shortest path from start to exit through uncorrupted
    spaces, while Part 2 determines which falling byte first makes the exit unreachable.

    Input format:
        - Multiple lines of comma-separated coordinates (x,y)
        - Each coordinate represents where a byte will fall and corrupt
        - Coordinates start from (0,0) at top-left
        - Grid size is 7x7 for test data, 71x71 for real data

    This class inherits from `SolutionBase` and provides methods to construct grids,
    find paths, and analyze byte corruption patterns.
    """

    def construct_grid(
        self, size: int, coordinates: List[Tuple[int, int]], limit: int
    ) -> List[str]:
        """Construct a grid representation of the memory space with corrupted bytes.

        Args:
            size (int): Size of the grid (both width and height)
            coordinates (List[Tuple[int, int]]): List of (x,y) coordinates where bytes fall
            limit (int): Number of coordinates to process (12 for test, 1024 for real data)

        Returns:
            List[str]: Grid representation where '.' is safe and '#' is corrupted
        """
        grid = [["."] * size for _ in range(size)]

        for col, row in coordinates[:limit]:
            grid[row][col] = "#"

        return ["".join(row) for row in grid]

    def has_path(self, grid: List[str]) -> bool:
        """Check if there exists any path from start to end through uncorrupted spaces.

        Uses breadth-first search to efficiently determine path existence without
        calculating the actual path length.

        Args:
            grid (List[str]): Current state of the memory space

        Returns:
            bool: True if a path exists to the exit, False otherwise
        """
        size = len(grid)
        start = (0, 0)
        end = (size - 1, size - 1)
        queue = deque([start])
        seen = {start}

        while queue:
            x, y = queue.popleft()

            if (x, y) == end:
                return True

            for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
                new_x, new_y = x + dx, y + dy
                if (
                    0 <= new_x < size
                    and 0 <= new_y < size
                    and grid[new_y][new_x] == "."
                    and (new_x, new_y) not in seen
                ):
                    seen.add((new_x, new_y))
                    queue.append((new_x, new_y))

        return False

    def find_shortest_path(self, grid: List[str]) -> int:
        """Find the shortest path from start to end through uncorrupted spaces.

        Uses breadth-first search to guarantee the shortest path is found.
        Returns -1 if no path exists.

        Args:
            grid (List[str]): Current state of the memory space

        Returns:
            int: Length of shortest path to exit, or -1 if no path exists
        """
        size = len(grid)
        start = (0, 0)
        end = (size - 1, size - 1)
        queue = deque([(start, 0)])  # (position, path_length)
        seen = {start}

        while queue:
            position, length = queue.popleft()

            if position == end:
                return length

            x, y = position
            for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
                new_x, new_y = x + dx, y + dy
                new_pos = (new_x, new_y)
                if (
                    0 <= new_x < size
                    and 0 <= new_y < size
                    and grid[new_y][new_x] == "."
                    and new_pos not in seen
                ):
                    seen.add(new_pos)
                    queue.append((new_pos, length + 1))

        return -1

    def part1(self, data: List[str]) -> int:
        """Find shortest path to exit after initial byte corruption.

        For test data (7x7 grid), simulates first 12 bytes falling.
        For real data (71x71 grid), simulates first 1024 bytes falling.

        Args:
            data (List[str]): Input lines containing byte fall coordinates

        Returns:
            int: Length of shortest path to exit, or -1 if no path exists
        """
        coordinates = [tuple(map(int, row.split(","))) for row in data]
        limit = 12 if len(coordinates) == 25 else 1024
        grid_size = max(n for pair in coordinates for n in pair) + 1
        grid = self.construct_grid(grid_size, coordinates, limit)
        return self.find_shortest_path(grid)

    def part2(self, data: List[str]) -> str:
        """Find coordinates of first byte that makes exit unreachable.

        Uses binary search to efficiently find the critical byte that blocks
        all possible paths to the exit.

        Args:
            data (List[str]): Input lines containing byte fall coordinates

        Returns:
            str: Coordinates of blocking byte as "x,y" string
        """
        coordinates = [tuple(map(int, row.split(","))) for row in data]
        grid_size = max(n for pair in coordinates for n in pair) + 1

        # Binary search for the first coordinate that blocks all paths
        left = 0
        right = len(coordinates)

        while right - left > 1:
            mid = (left + right) // 2
            grid = self.construct_grid(grid_size, coordinates, mid)

            if self.has_path(grid):
                left = mid
            else:
                right = mid

        # right is now the index of the first coordinate that blocks all paths
        return f"{coordinates[right-1][0]},{coordinates[right-1][1]}"
