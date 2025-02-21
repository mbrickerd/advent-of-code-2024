"""Day 10: Hoof It.

This module provides the solution for Advent of Code 2024 - Day 10.
It handles finding valid hiking trails on a topographic map and calculating
trailhead scores based on reachable peak positions.

The module contains a Solution class that inherits from SolutionBase and implements
methods to find paths that increase by exactly one height level at each step,
reaching peaks (height 9) from valleys (height 0).
"""

from collections import deque

from aoc.models.base import SolutionBase


class Solution(SolutionBase):
    """Solution for Advent of Code 2024 - Day 10: Hoof It.

    Solves puzzles involving valid hiking trails on a topographic map:
    - Part 1: Calculate sum of scores for all trailheads based on reachable peaks
    - Part 2: Calculate sum of ratings based on unique paths to peaks
    """

    def get_neighbors(
        self, grid: list[list[int]], x: int, y: int, target_height: int
    ) -> list[tuple[int, int]]:
        """Find valid neighboring positions with a specific target height.

        Args:
            grid (List[List[int]]): The height grid
            x (int): Current `x` coordinate
            y (int): Current `y` coordinate
            target_height (int): The height value we're looking for in neighbors

        Returns
        -------
            List[Tuple[int, int]]: List of valid neighbor coordinates (x, y) that have
                the target height. Only considers up, down, left, and right neighbors
                within grid boundaries.
        """
        rows, cols = len(grid), len(grid[0])
        neighbors = []

        for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
            new_x, new_y = x + dx, y + dy
            if 0 <= new_x < rows and 0 <= new_y < cols and grid[new_x][new_y] == target_height:
                neighbors.append((new_x, new_y))

        return neighbors

    def find_paths_to_nine(
        self, grid: list[list[int]], start_x: int, start_y: int
    ) -> set[tuple[int, int]]:
        """Find all height-9 positions reachable via valid hiking trails from a starting position.

        A valid hiking trail must:
        - Start at height 0
        - Increase by exactly 1 at each step
        - Only move up, down, left, or right (no diagonals)
        - End at height 9

        Args:
            grid (List[List[int]]): The height grid
            start_x (int): Starting `x` coordinate
            start_y (int): Starting `y` coordinate

        Returns
        -------
            Set[Tuple[int, int]]: Set of coordinates (x, y) of height-9 positions
                that can be reached via valid hiking trails from the start position.
                Returns empty set if start position isn't height 0.
        """
        if grid[start_x][start_y] != 0:
            return set()

        reachable_nines = set()
        visited = {(start_x, start_y, 0)}
        queue = deque([(start_x, start_y, 0)])

        while queue:
            x, y, height = queue.popleft()

            if height == 9:
                reachable_nines.add((x, y))
                continue

            next_height = height + 1
            for next_x, next_y in self.get_neighbors(grid, x, y, next_height):
                next_state = (next_x, next_y, next_height)
                if next_state not in visited:
                    visited.add(next_state)
                    queue.append(next_state)

        return reachable_nines

    def count_unique_paths(self, grid: list[list[int]], start_x: int, start_y: int) -> int:
        """Count number of unique paths from start position to any height-9 position.

        A valid path must:
        - Start at height 0
        - Increase by exactly 1 at each step
        - Only move up, down, left, or right (no diagonals)
        - End at height 9

        Uses dynamic programming to count paths efficiently by tracking the number
        of paths to each position at each height level.

        Args:
            grid (List[List[int]]): The height grid
            start_x (int): Starting x coordinate
            start_y (int): Starting y coordinate

        Returns
        -------
            int: Number of unique valid paths from start position to any height-9
                position. Returns 0 if start position isn't height 0.
        """
        if grid[start_x][start_y] != 0:
            return 0

        paths = {(start_x, start_y, 0): 1}
        queue = deque([(start_x, start_y, 0)])
        total_paths = 0

        while queue:
            x, y, height = queue.popleft()
            path_count = paths[(x, y, height)]

            if height == 9:
                total_paths += path_count
                continue

            next_height = height + 1
            for next_x, next_y in self.get_neighbors(grid, x, y, next_height):
                next_state = (next_x, next_y, next_height)
                if next_state not in paths:
                    paths[next_state] = path_count
                    queue.append(next_state)

                else:
                    paths[next_state] += path_count

        return total_paths

    def part1(self, data: list[str]) -> int:
        """Calculate the sum of scores for all trailheads on the topographic map.

        A trailhead's score is the number of height-9 positions that can be reached
        from that trailhead via valid hiking trails. A valid trail must increase by
        exactly 1 in height at each step and can only move in cardinal directions.

        Args:
            data (List[str]): Input lines containing the height grid

        Returns
        -------
            int: Sum of scores for all trailheads (positions with height 0)
        """
        grid = [[int(coord) for coord in line.strip()] for line in data]
        rows, cols = len(grid), len(grid[0])

        total_score = 0
        for i in range(rows):
            for j in range(cols):
                if grid[i][j] == 0:
                    reachable = self.find_paths_to_nine(grid, i, j)
                    total_score += len(reachable)

        return total_score

    def part2(self, data: list[str]) -> int:
        """Calculate the sum of ratings for all trailheads on the topographic map.

        A trailhead's rating is the number of distinct hiking trails that begin at
        that trailhead. A valid trail must start at height 0, increase by exactly 1
        at each step, only move in cardinal directions (up, down, left, right), and
        end at height 9.

        Args:
            data (List[str]): Input lines containing the height grid

        Returns
        -------
            int: Sum of ratings (number of unique paths to height 9) for all
                trailheads (positions with height 0)
        """
        grid = [[int(c) for c in line.strip()] for line in data]
        rows, cols = len(grid), len(grid[0])

        total_rating = 0
        for i in range(rows):
            for j in range(cols):
                if grid[i][j] == 0:
                    total_rating += self.count_unique_paths(grid, i, j)

        return total_rating
