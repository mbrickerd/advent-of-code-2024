from collections import defaultdict
from typing import List, Set, Tuple

from aoc.models.base import SolutionBase


class Solution(SolutionBase):
    """Solution for Advent of Code 2024 - Day 8: Resonant Collinearity.

    This class solves a puzzle involving finding resonant antinodes created by antennas
    in a grid. Part 1 finds antinodes where one antenna is twice as far away as another,
    while Part 2 considers all collinear points as antinodes.

    Input format:
        Grid of characters where each non-'.' character represents an antenna of that
        frequency. Same characters (frequencies) interact to create antinodes.

    This class inherits from `SolutionBase` and provides methods to find and analyze
    antenna positions and their resulting antinodes.
    """

    def find_antennas(self, data: List[str]) -> defaultdict:
        """Find all antenna positions grouped by frequency.

        Args:
            data (List[str]): Grid of characters where non-'.' represents antennas

        Returns:
            defaultdict: Dictionary mapping frequency to list of positions.
                Example: {'A': [(1, 2), (3, 4)], '0': [(0, 1), (2, 3)]}
        """
        antennas = defaultdict(list)
        for y, row in enumerate(data):
            for x, char in enumerate(row):
                if char != ".":
                    antennas[char].append((x, y))

        return antennas

    def is_collinear(self, p1: Tuple[int, int], p2: Tuple[int, int], p3: Tuple[int, int]) -> bool:
        """Check if three points lie on the same line.

        Uses cross product to determine collinearity. Points are collinear if
        the cross product is approximately zero.

        Args:
            p1: First point coordinates (x, y)
            p2: Second point coordinates (x, y)
            p3: Third point coordinates (x, y)

        Returns:
            bool: `True` if points are collinear, `False` otherwise
        """
        x1, y1 = p1
        x2, y2 = p2
        x3, y3 = p3

        # Calculate cross product
        cross_product = (y2 - y1) * (x3 - x1) - (y3 - y1) * (x2 - x1)
        return abs(cross_product) < 1e-10

    def distance(self, p1: Tuple[int, int], p2: Tuple[int, int]) -> float:
        """Calculate Euclidean distance between two points.

        Args:
            p1: First point coordinates (x, y)
            p2: Second point coordinates (x, y)

        Returns:
            float: Euclidean distance between the points
        """
        return ((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2) ** 0.5

    def find_antinodes(self, ant1: Tuple[int, int], ant2: Tuple[int, int], data: List[str]) -> Set[Tuple[int, int]]:
        """Find all antinodes created by a pair of antennas.

        For Part 1, antinodes occur at points where one antenna is twice as far
        away as the other. Points must be collinear and satisfy the distance ratio.

        Args:
            ant1: Position of first antenna (x, y)
            ant2: Position of second antenna (x, y)
            data: Grid data for boundary checking

        Returns:
            Set[Tuple[int, int]]: Set of antinode positions
        """
        x1, y1 = ant1
        x2, y2 = ant2
        antinodes = set()

        # Vector between antennas
        dx = x2 - x1
        dy = y2 - y1

        # Base distance between antennas
        base_dist = self.distance(ant1, ant2)

        # Check each integer point in the grid
        for y in range(len(data)):
            for x in range(len(data[0])):
                point = (x, y)

                # Skip if the point is not collinear with the antennas
                if not self.is_collinear(ant1, ant2, point):
                    continue

                # Calculate distances
                d1 = self.distance(point, ant1)
                d2 = self.distance(point, ant2)

                # Skip if point coincides with either antenna
                if d1 < 0.0001 or d2 < 0.0001:
                    continue

                # Check for 2:1 ratio with very small tolerance
                ratio = max(d1, d2) / min(d1, d2)
                if abs(ratio - 2.0) < 0.0001:
                    # Verify the point is on the line between or beyond the antennas
                    v1x = x - x1
                    v1y = y - y1
                    dot_product = dx * v1x + dy * v1y
                    if dot_product * (dot_product - base_dist * base_dist) >= 0:
                        antinodes.add(point)

        return antinodes

    def part1(self, data: List[str]) -> int:
        """Count antinodes where one antenna is twice as far as another.

        Finds all pairs of same-frequency antennas and identifies points where
        one antenna is exactly twice as far away as the other. Only counts
        points that are collinear with the antenna pair.

        Args:
            data: Grid of antenna positions

        Returns:
            int: Number of unique antinode positions
        """
        antennas = self.find_antennas(data)
        all_antinodes = set()

        # For each frequency
        for positions in antennas.values():
            # For each pair of same-frequency antennas
            for i, ant1 in enumerate(positions):
                for ant2 in positions[i + 1 :]:
                    # Find antinodes for this pair
                    antinodes = self.find_antinodes(ant1, ant2, data)
                    all_antinodes.update(antinodes)

        return len(all_antinodes)

    def part2(self, data: List[str]) -> int:
        """Count all antinodes formed by collinear antenna pairs.

        Similar to part1 but considers all points collinear with same-frequency
        antenna pairs as antinodes, regardless of distance. Also includes antenna
        positions themselves when they are collinear with other antennas of the
        same frequency.

        Args:
            data: Grid of antenna positions

        Returns:
            int: Number of unique antinode positions including antenna positions
        """
        antennas = self.find_antennas(data)
        all_antinodes = set()

        # For each frequency
        for positions in antennas.values():
            # Skip if there's only one antenna of this frequency
            if len(positions) < 2:
                continue

            # For each pair of same-frequency antennas
            for i, ant1 in enumerate(positions):
                for j, ant2 in enumerate(positions[i + 1 :], start=i + 1):
                    # Add both antenna positions as they are collinear with at least two antennas
                    all_antinodes.add(ant1)
                    all_antinodes.add(ant2)

                    # Check each integer point in the grid
                    for y in range(len(data)):
                        for x in range(len(data[0])):
                            point = (x, y)

                            # If point is collinear with these antennas, it's an antinode
                            if self.is_collinear(ant1, ant2, point):
                                all_antinodes.add(point)

        return len(all_antinodes)
