from collections import deque
from typing import Dict, List, Set, Tuple

from aoc.models.base import SolutionBase


class Solution(SolutionBase):
    """Solution for Advent of Code 2024 - Day 10: Hoof It.

    This class solves a puzzle involving finding valid hiking trails on a topographic
    map. A valid hiking trail must start at height 0, end at height 9, and increase
    by exactly 1 at each step. The solution calculates scores for each trailhead based
    on how many height-9 positions can be reached via valid hiking trails.

    Input format:
        List of strings where each string represents a row in the grid and each character
        is a single digit (0-9) representing the height at that position in the grid.
        All rows have the same length, forming a rectangular grid.

    This class inherits from `SolutionBase` and provides methods to find valid paths
    and calculate trailhead scores.
    """

    def get_neighbors(self, grid: List[List[int]], x: int, y: int, target_height: int) -> List[Tuple[int, int]]:
        """Find valid neighboring positions with a specific target height.

        Args:
            grid (List[List[int]]): The height grid
            x (int): Current `x` coordinate
            y (int): Current `y` coordinate
            target_height (int): The height value we're looking for in neighbors

        Returns:
            List[Tuple[int, int]]: List of valid neighbor coordinates (x, y) that have
                the target height. Only considers up, down, left, and right neighbors
                within grid boundaries.
        """
        neighbors = []
        for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]:  # right, down, left, up
            new_x, new_y = x + dx, y + dy
            if 0 <= new_x < len(grid) and 0 <= new_y < len(grid[0]) and grid[new_x][new_y] == target_height:
                neighbors.append((new_x, new_y))

        return neighbors

    def find_paths_to_nine(self, grid: List[List[int]], start_x: int, start_y: int) -> Set[Tuple[int, int]]:
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

        Returns:
            Set[Tuple[int, int]]: Set of coordinates (x, y) of height-9 positions
                that can be reached via valid hiking trails from the start position.
                Returns empty set if start position isn't height 0.
        """
        if grid[start_x][start_y] != 0:  # Must start at height 0
            return set()

        reachable_nines = set()
        queue = deque([(start_x, start_y, 0)])  # (x, y, current_height)
        visited = set()

        while queue:
            x, y, height = queue.popleft()
            current_state = (x, y, height)

            if current_state in visited:
                continue

            visited.add(current_state)

            if height == 9:  # Found a path to height 9
                reachable_nines.add((x, y))
                continue

            # Look for positions with height + 1
            next_height = height + 1
            for next_x, next_y in self.get_neighbors(grid, x, y, next_height):
                queue.append((next_x, next_y, next_height))

        return reachable_nines

    def count_unique_paths(self, grid: List[List[int]], start_x: int, start_y: int) -> int:
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

        Returns:
            int: Number of unique valid paths from start position to any height-9
                position. Returns 0 if start position isn't height 0.
        """
        if grid[start_x][start_y] != 0:
            return 0

        # paths[(x, y, h)] represents the number of paths to (x,y) at height h
        paths: Dict[Tuple[int, int, int], int] = {(start_x, start_y, 0): 1}
        queue = deque([(start_x, start_y, 0)])  # (x, y, current_height)
        total_paths = 0

        while queue:
            x, y, height = queue.popleft()
            current_paths = paths[(x, y, height)]

            if height == 9:
                total_paths += current_paths
                continue

            next_height = height + 1
            for next_x, next_y in self.get_neighbors(grid, x, y, next_height):
                next_state = (next_x, next_y, next_height)
                if next_state not in paths:
                    queue.append((next_x, next_y, next_height))
                    paths[next_state] = current_paths

                else:
                    paths[next_state] += current_paths

        return total_paths

    def part1(self, data: List[str]) -> int:
        """Calculate the sum of scores for all trailheads on the topographic map.

        A trailhead's score is the number of height-9 positions that can be reached
        from that trailhead via valid hiking trails. A valid trail must increase by
        exactly 1 in height at each step and can only move in cardinal directions.

        Args:
            data (List[str]): Input lines containing the height grid

        Returns:
            int: Sum of scores for all trailheads (positions with height 0)
        """
        # Parse input into grid
        grid = [[int(coord) for coord in line.strip()] for line in data]
        rows, cols = len(grid), len(grid[0])

        # Find all starting positions (height 0)
        total_score = 0
        for i in range(rows):
            for j in range(cols):
                if grid[i][j] == 0:
                    reachable = self.find_paths_to_nine(grid, i, j)
                    total_score += len(reachable)

        return total_score

    def part2(self, data: List[str]) -> int:
        """Calculate the sum of ratings for all trailheads on the topographic map.

        A trailhead's rating is the number of distinct hiking trails that begin at
        that trailhead. A valid trail must start at height 0, increase by exactly 1
        at each step, only move in cardinal directions (up, down, left, right), and
        end at height 9.

        Args:
            data (List[str]): Input lines containing the height grid

        Returns:
            int: Sum of ratings (number of unique paths to height 9) for all
                trailheads (positions with height 0)
        """
        grid = [[int(c) for c in line.strip()] for line in data]
        rows, cols = len(grid), len(grid[0])

        total_rating = 0
        for i in range(rows):
            for j in range(cols):
                if grid[i][j] == 0:
                    rating = self.count_unique_paths(grid, i, j)
                    total_rating += rating

        return total_rating
