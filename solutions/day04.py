from typing import List

from aoc.models.base import SolutionBase


class Solution(SolutionBase):
    """Solution for Advent of Code 2024 - Day 4: Ceres Search.

    This class solves a puzzle involving searching for text patterns in a 2D grid.
    Part 1 searches for "XMAS" in all 8 directions, while Part 2 looks for crossed
    "MAS" patterns forming an X shape with a shared 'A' at the center.

    This class inherits from `SolutionBase` and provides methods to search for text
    patterns in grid data with directional traversal.
    """

    def check_mas(self, data: List[str], row: int, col: int, dr: int, dc: int) -> bool:
        """Check if "MAS" exists starting from a point in a given direction.

        Args:
            data (List[str]): 2D grid represented as list of strings
            row (int): Starting row coordinate
            col (int): Starting column coordinate
            dr (int): Row direction (-1, 0, or 1)
            dc (int): Column direction (-1, 0, or 1)

        Returns:
            bool: True if "MAS" exists starting from (r,c) in direction (dr,dc),
                and all coordinates stay within grid bounds. For example:
                - Returns True if "MAS" is found completely within bounds
                - Returns False if path goes out of bounds
                - Returns False if letters don't match "MAS" pattern
        """
        rows, cols = len(data), len(data[0])
        pattern = "MAS"
        return all(
            0 <= row + i * dr < rows and 0 <= col + i * dc < cols and data[row + i * dr][col + i * dc] == pattern[i]
            for i in range(3)
        )

    def part1(self, data: List[str]) -> int:
        """Count occurrences of "XMAS" in all 8 directions.

        Searches for "XMAS" from each grid position in all 8 possible directions:
        horizontal, vertical, and diagonal.

        Args:
            data (List[str]): 2D grid represented as list of strings where each
                character is a letter that could be part of "XMAS".

        Returns:
            int: Total number of "XMAS" patterns found. Each pattern may overlap
                with others and is counted separately.
        """
        rows, cols = len(data), len(data[0])
        directions = [
            (0, 1),  # right
            (1, 1),  # down-right
            (1, 0),  # down
            (1, -1),  # down-left
            (0, -1),  # left
            (-1, -1),  # up-left
            (-1, 0),  # up
            (-1, 1),  # up-right
        ]
        count = 0

        for r in range(rows):
            for c in range(cols):
                for dr, dc in directions:
                    if all(
                        0 <= r + i * dr < rows and 0 <= c + i * dc < cols and data[r + i * dr][c + i * dc] == "XMAS"[i]
                        for i in range(4)
                    ):
                        count += 1

        return count

    def part2(self, data: List[str]) -> int:
        """Count X-shaped patterns formed by two crossing "MAS" sequences.

        Searches for locations where two "MAS" sequences cross at their 'A's
        to form an X shape. Only checks one diagonal direction since that's
        sufficient to find all valid patterns.

        Args:
            data (List[str]): 2D grid represented as list of strings where each
                character is a letter that could be part of "MAS".

        Returns:
            int: Number of valid X patterns found, where each X consists of two
                "MAS" sequences crossing at their shared 'A'.
        """
        count = 0
        rows, cols = len(data), len(data[0])

        for row in range(1, rows - 1):
            for col in range(1, cols - 1):
                if data[row][col] != "A":
                    continue

                # Only check one diagonal direction - it's enough to find all X patterns
                dr, dc = 1, 1
                if (
                    self.check_mas(data, row - dr, col - dc, dr, dc)
                    or self.check_mas(data, row + dr, col + dc, -dr, -dc)
                ) and (
                    self.check_mas(data, row - dr, col + dc, dr, -dc)
                    or self.check_mas(data, row + dr, col - dc, -dr, dc)
                ):
                    count += 1

        return count
