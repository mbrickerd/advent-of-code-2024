"""Day 12: Garden Groups.

This module provides the solution for Advent of Code 2024 - Day 12.
It handles analyzing groups of plants in a garden grid where each connected
region of identical plants must be fenced.

Each region's fencing cost depends on:
- The region's area multiplied by its perimeter (part 1)
- The region's area multiplied by the number of distinct sides (part 2)

The module contains a Solution class that inherits from SolutionBase and implements
methods to identify connected regions, calculate their boundaries, and determine
total fencing costs.
"""

from aoc.models.base import SolutionBase


class Solution(SolutionBase):
    """Solution for Advent of Code 2024 - Day 12: Garden Groups.

    Solves puzzles involving fencing costs for garden regions:
    - Part 1: Calculate total cost using perimeter-based pricing
    - Part 2: Calculate total cost using distinct sides-based pricing
    """

    def find_region(
        self, grid: list[list[str]], start_x: int, start_y: int, char: str, visited: set
    ) -> set[tuple[int, int]]:
        """Find all connected cells containing the same character using depth-first search.

        Args:
            grid: 2D list representing the garden layout
            start_x: Starting x-coordinate to explore from
            start_y: Starting y-coordinate to explore from
            char: Character type to match for region
            visited: Set of already visited coordinates

        Returns
        -------
            Set of (y, x) coordinates that form the connected region
        """
        rows, cols = len(grid), len(grid[0])
        if (
            not (0 <= start_x < cols and 0 <= start_y < rows)
            or grid[start_y][start_x] != char
            or (start_y, start_x) in visited
        ):
            return set()

        region = set()
        stack = [(start_y, start_x)]

        while stack:
            y, x = stack.pop()
            if (y, x) in visited:
                continue

            visited.add((y, x))
            region.add((y, x))

            for dy, dx in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
                new_y, new_x = y + dy, x + dx
                if (
                    0 <= new_x < cols
                    and 0 <= new_y < rows
                    and grid[new_y][new_x] == char
                    and (new_y, new_x) not in visited
                ):
                    stack.append((new_y, new_x))

        return region

    def calculate_perimeter(self, region: set[tuple[int, int]], rows: int, cols: int) -> int:
        """Calculate the total perimeter of a region.

        Counts each cell edge that either borders the grid boundary or
        neighbors a different plant type.

        Args:
            region: Set of (y, x) coordinates in the region
            rows: Number of rows in the grid
            cols: Number of columns in the grid

        Returns
        -------
            Total length of the perimeter
        """
        perimeter = 0
        directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]

        for y, x in region:
            for dy, dx in directions:
                new_y, new_x = y + dy, x + dx
                if not (0 <= new_x < cols and 0 <= new_y < rows and (new_y, new_x) in region):
                    perimeter += 1

        return perimeter

    def count_sides(self, region: set[tuple[int, int]], rows: int, cols: int) -> int:
        """Count unique sides of a region, merging adjacent parallel edges.

        A side is a continuous straight line segment that forms part of the region's
        boundary, regardless of its length. Multiple adjacent cell edges in the same
        direction count as a single side.

        Args:
            region: Set of (y, x) coordinates in the region
            rows: Number of rows in the grid
            cols: Number of columns in the grid

        Returns
        -------
            Number of distinct sides in the region's boundary
        """
        edges = set()

        for y, x in region:
            north = (y - 1, x) in region
            east = (y, x + 1) in region
            south = (y + 1, x) in region
            west = (y, x - 1) in region

            if not north and (not west or (y - 1, x - 1) in region):
                edges.add(("H", y, x))

            if not south and (not west or (y + 1, x - 1) in region):
                edges.add(("H", y + 1, x))

            if not west and (not north or (y - 1, x - 1) in region):
                edges.add(("V", x, y))

            if not east and (not north or (y - 1, x + 1) in region):
                edges.add(("V", x + 1, y))

        return len(edges)

    def calculate_cost(self, data: list[str], calc_method: str) -> int:
        """Process the garden grid and calculate total fencing cost.

        For each unique plant type, identifies all connected regions and calculates
        their price based on area multiplied by either perimeter or number of sides.

        Args:
            data: List of strings representing the garden grid
            calc_method: Which calculation method to use ('perimeter' or 'sides')

        Returns
        -------
            Total cost of fencing all regions
        """
        grid = [list(line) for line in data]
        rows, cols = len(grid), len(grid[0])
        visited: set = set()
        total_price = 0

        for y in range(rows):
            for x in range(cols):
                if (y, x) not in visited:
                    char = grid[y][x]
                    region = self.find_region(grid, x, y, char, visited)

                    if region:
                        if calc_method == "perimeter":
                            metric = self.calculate_perimeter(region, rows, cols)

                        else:
                            metric = self.count_sides(region, rows, cols)

                        total_price += len(region) * metric

        return total_price

    def part1(self, data: list[str]) -> int:
        """Calculate total fencing cost using perimeter-based pricing.

        Args:
            data: List of strings representing the garden grid

        Returns
        -------
            Total cost when each region's price is `area` * `perimeter`
        """
        return self.calculate_cost(data, "perimeter")

    def part2(self, data: list[str]) -> int:
        """Calculate total fencing cost using distinct sides-based pricing.

        Args:
            data: List of strings representing the garden grid

        Returns
        -------
            Total cost when each region's price is `area` * `number_of_sides`
        """
        return self.calculate_cost(data, "sides")
