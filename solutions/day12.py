from typing import Callable, List, Set

from aoc.models.base import SolutionBase


class Solution(SolutionBase):
    """Solution for Advent of Code 2024 - Day 12: Garden Groups.

    This class solves a puzzle involving analyzing groups of plants in a garden grid.
    Each group (region) of identical plants must be fenced, with the cost depending on
    either the perimeter (part 1) or the number of distinct sides (part 2) multiplied
    by the area of the region.

    Input format:
        List of strings representing a grid where each character represents a different
        type of plant. Adjacent identical characters form regions that need to be fenced.

    This class inherits from `SolutionBase` and provides methods to identify connected
    regions, calculate their perimeters or distinct sides, and determine total fencing costs.
    """

    def find_region(
        self, grid: List[List[str]], start_x: int, start_y: int, char: str, visited: set
    ) -> Set[str]:
        """Find all connected cells containing the same character using depth-first search.

        Args:
            grid: 2D list representing the garden layout
            start_x: Starting x-coordinate to explore from
            start_y: Starting y-coordinate to explore from
            char: Character type to match for region
            visited: Set of already visited coordinates

        Returns:
            Set of (y, x) coordinates that form the connected region
        """
        if (
            not (0 <= start_x < len(grid[0]) and 0 <= start_y < len(grid))
            or grid[start_y][start_x] != char
            or (start_y, start_x) in visited
        ):
            return set()

        region = {(start_y, start_x)}
        visited.add((start_y, start_x))

        for dy, dx in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
            region.update(self.find_region(grid, start_x + dx, start_y + dy, char, visited))

        return region

    def calculate_perimeter(self, grid: List[List[str]], region: Set[str]) -> int:
        """Calculate the total perimeter of a region.

        Counts each cell edge that either borders the grid boundary or
        neighbors a different plant type.

        Args:
            grid: 2D list representing the garden layout
            region: Set of (y, x) coordinates in the region

        Returns:
            Total length of the perimeter
        """
        perimeter = 0
        for y, x in region:
            for dy, dx in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
                new_y, new_x = y + dy, x + dx
                if (new_y, new_x) not in region or not (
                    0 <= new_x < len(grid[0]) and 0 <= new_y < len(grid)
                ):
                    perimeter += 1

        return perimeter

    def in_region(self, y: int, x: int, region: Set[str]) -> bool:
        """Check if given coordinates are part of the region.

        Args:
            y: Y-coordinate to check
            x: X-coordinate to check
            region: Set of (y, x) coordinates in the region

        Returns:
            True if coordinates are in the region, False otherwise
        """
        return (y, x) in region

    def count_sides(self, grid: List[List[str]], region: Set[str]) -> int:
        """Count unique sides of a region, merging adjacent parallel edges.

        A side is a continuous straight line segment that forms part of the region's
        boundary, regardless of its length. Multiple adjacent cell edges in the same
        direction count as a single side.

        Args:
            grid: 2D list representing the garden layout
            region: Set of (y, x) coordinates in the region

        Returns:
            Number of distinct sides in the region's boundary
        """
        edges = set()

        for y, x in sorted(region):
            # Check all four directions for potential edges
            if not self.in_region(y - 1, x, region):
                if not self.in_region(y, x - 1, region) or self.in_region(y - 1, x - 1, region):
                    edges.add(("H", y, x))

            if not self.in_region(y + 1, x, region):
                if not self.in_region(y, x - 1, region) or self.in_region(y + 1, x - 1, region):
                    edges.add(("H", y + 1, x))

            if not self.in_region(y, x - 1, region):
                if not self.in_region(y - 1, x, region) or self.in_region(y - 1, x - 1, region):
                    edges.add(("V", x, y))

            if not self.in_region(y, x + 1, region):
                if not self.in_region(y - 1, x, region) or self.in_region(y - 1, x + 1, region):
                    edges.add(("V", x + 1, y))

        return len(edges)

    def calculate_cost(self, data: List[str], calc_func: Callable) -> int:
        """Process the garden grid and calculate total fencing cost.

        For each unique plant type, identifies all connected regions and calculates
        their price based on area multiplied by either perimeter or number of sides.

        Args:
            data: List of strings representing the garden grid
            calc_func: Function to calculate either perimeter or number of sides

        Returns:
            Total cost of fencing all regions
        """
        grid = [list(line) for line in data]
        chars = {char for row in grid for char in row}
        total_price = 0
        visited = set()

        for char in chars:
            for y in range(len(grid)):
                for x in range(len(grid[0])):
                    if grid[y][x] == char and (y, x) not in visited:
                        region = self.find_region(grid, x, y, char, visited)
                        total_price += len(region) * calc_func(grid, region)

        return total_price

    def part1(self, data: List[str]) -> int:
        """Calculate total fencing cost using perimeter-based pricing.

        Args:
            data: List of strings representing the garden grid

        Returns:
            Total cost when each region's price is `area` * `perimeter`
        """
        return self.calculate_cost(data, self.calculate_perimeter)

    def part2(self, data: List[str]) -> int:
        """Calculate total fencing cost using distinct sides-based pricing.

        Args:
            data: List of strings representing the garden grid

        Returns:
            Total cost when each region's price is `area` * `number_of_sides`
        """
        return self.calculate_cost(data, self.count_sides)
