"""Day 8: Resonant Collinearity.

This module provides the solution for Advent of Code 2024 - Day 8.
It simulates antenna resonance patterns to find antinodes in a grid.

The module identifies antenna positions and calculates antinodes based on
collinearity, with Part 1 requiring specific distance ratios and Part 2
counting all collinear points as antinodes.
"""

from collections import defaultdict
from itertools import combinations

from aoc.models.base import SolutionBase


class Solution(SolutionBase):
    """Antenna resonance simulation to find antinodes in a grid.

    This solution implements antinode discovery algorithms:
    - Part 1: Find points where one antenna is twice as far as another
    - Part 2: Count all collinear points as antinodes

    Grid elements:
        - "." : Empty space
        - Any other character: Antenna with that frequency
    """

    def find_antennas(self, data: list[str]) -> defaultdict[str, list[tuple[int, int]]]:
        """Find all antenna positions grouped by frequency.

        Scans the grid and identifies all antenna positions, grouping them
        by their frequency (character). Each non-'.' character in the grid
        represents an antenna of that frequency.

        Args:
            data: Grid where non-'.' characters represent antennas

        Returns
        -------
            defaultdict[str, list[tuple[int, int]]]: Dictionary mapping frequency to
                list of positions, where each position is a tuple of (x, y) coordinates
        """
        antennas = defaultdict(list)
        for y, row in enumerate(data):
            for x, char in enumerate(row):
                if char != ".":
                    antennas[char].append((x, y))

        return antennas

    def is_collinear(self, p1: tuple[int, int], p2: tuple[int, int], p3: tuple[int, int]) -> bool:
        """Check if three points lie on the same line using cross product.

        Uses the cross product method to determine if three points are collinear.
        Three points are collinear if the cross product of vectors formed by
        these points is approximately zero (accounting for floating-point precision).

        Args:
            p1: First point coordinates (x, y)
            p2: Second point coordinates (x, y)
            p3: Third point coordinates (x, y)

        Returns
        -------
            bool: True if points are collinear, False otherwise
        """
        cross_product = (p2[1] - p1[1]) * (p3[0] - p1[0]) - (p3[1] - p1[1]) * (p2[0] - p1[0])
        return abs(cross_product) < 1e-10

    def distance_squared(self, p1: tuple[int, int], p2: tuple[int, int]) -> int:
        """Calculate squared Euclidean distance between two points.

        Computes the squared distance between two points, avoiding the
        unnecessary square root calculation for performance optimization.
        This is useful for comparing distances without needing their exact values.

        Args:
            p1: First point coordinates (x, y)
            p2: Second point coordinates (x, y)

        Returns
        -------
            int: Squared Euclidean distance between the points
        """
        return (p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2

    def find_antinodes(
        self, ant1: tuple[int, int], ant2: tuple[int, int], grid_width: int, grid_height: int
    ) -> set[tuple[int, int]]:
        """Find all antinodes created by a pair of antennas.

        Searches the grid for points that form antinodes with the given antenna pair.
        For Part 1, a point is an antinode if:
        1. It's collinear with both antennas
        2. The distance to one antenna is exactly twice the distance to the other
        3. It lies on the line segment between or beyond the antennas

        Args:
            ant1: Position of first antenna (x, y)
            ant2: Position of second antenna (x, y)
            grid_width: Width of the grid
            grid_height: Height of the grid

        Returns
        -------
            set[tuple[int, int]]: Set of antinode positions as (x, y) coordinate tuples
        """
        antinodes = set()

        dx = ant2[0] - ant1[0]
        dy = ant2[1] - ant1[1]
        base_dist_squared = self.distance_squared(ant1, ant2)

        for y in range(grid_height):
            for x in range(grid_width):
                point = (x, y)

                if point in (ant1, ant2):
                    continue

                if not self.is_collinear(ant1, ant2, point):
                    continue

                d1_squared = self.distance_squared(point, ant1)
                d2_squared = self.distance_squared(point, ant2)

                if d1_squared == 0 or d2_squared == 0:
                    continue

                if (
                    abs(d1_squared - 4 * d2_squared) < 1e-6
                    or abs(d2_squared - 4 * d1_squared) < 1e-6
                ):
                    v1x = x - ant1[0]
                    v1y = y - ant1[1]
                    dot_product = dx * v1x + dy * v1y
                    if dot_product * (dot_product - base_dist_squared) >= 0:
                        antinodes.add(point)

        return antinodes

    def part1(self, data: list[str]) -> int:
        """Calculate number of antinodes where one antenna is twice as far as another.

        For each pair of same-frequency antennas, finds all points in the grid
        that satisfy the antinode conditions (collinearity and 2:1 distance ratio).
        Counts unique antinode positions across all antenna pairs.

        Args:
            data: Input grid rows as strings

        Returns
        -------
            int: Number of unique antinode positions in the grid
        """
        antennas = self.find_antennas(data)
        all_antinodes = set()
        grid_height = len(data)
        grid_width = len(data[0]) if data else 0

        for positions in antennas.values():
            for ant1, ant2 in combinations(positions, 2):
                antinodes = self.find_antinodes(ant1, ant2, grid_width, grid_height)
                all_antinodes.update(antinodes)

        return len(all_antinodes)

    def part2(self, data: list[str]) -> int:
        """Count all antinodes formed by collinear antenna pairs.

        For each pair of same-frequency antennas, considers all collinear points
        in the grid as antinodes, including the antenna positions themselves.
        This represents a simplified model where resonance occurs along the entire
        line connecting same-frequency antennas.

        Args:
            data: Input grid rows as strings

        Returns
        -------
            int: Number of unique antinode positions in the grid under the relaxed rules
        """
        antennas = self.find_antennas(data)
        all_antinodes = set()
        grid_height = len(data)
        grid_width = len(data[0]) if data else 0

        for positions in antennas.values():
            if len(positions) < 2:
                continue

            for ant1, ant2 in combinations(positions, 2):
                all_antinodes.add(ant1)
                all_antinodes.add(ant2)

                for y in range(grid_height):
                    for x in range(grid_width):
                        point = (x, y)
                        if self.is_collinear(ant1, ant2, point):
                            all_antinodes.add(point)

        return len(all_antinodes)
