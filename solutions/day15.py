"""Day 15: Warehouse Woes.

This module provides the solution for Advent of Code 2024 - Day 15.
It simulates the movement of boxes in a warehouse based on directional commands,
tracking the final positions to solve warehouse organization puzzles.

The warehouse is represented as a grid where '@' marks the starting position,
'O' represents boxes (or '[]' in part 2), '#' represents walls, and '.' represents
empty spaces. Movement follows directional commands (^, v, <, >) with special
handling for connected box pairs in part 2.
"""

from typing import ClassVar

from aoc.models.base import SolutionBase


class Solution(SolutionBase):
    """Solution for Advent of Code 2024 - Day 15: Warehouse Woes.

    This class solves a puzzle involving moving boxes in a warehouse using directional
    commands. The warehouse is represented as a grid where '@' marks the starting position,
    'O' represents boxes (or '[]' in part 2), '#' represents walls, and '.' represents
    empty spaces.

    Input format:
        Two sections separated by a blank line:
        - Grid layout with '@' (start), 'O' (boxes), '#' (walls), and '.' (empty)
        - Movement sequence using '^' (up), 'v' (down), '<' (left), '>' (right)

    This class inherits from `SolutionBase` and provides methods to simulate box movement
    in the warehouse, handling both single boxes (part 1) and connected box pairs (part 2),
    calculating final positions and scores based on box locations.
    """

    moves: ClassVar[dict[str, tuple[int, int]]] = {
        "^": (-1, 0),
        "v": (1, 0),
        "<": (0, -1),
        ">": (0, 1),
    }
    maps: ClassVar[dict[str, str]] = {"#": "##", "O": "[]", ".": "..", "@": "@."}

    def scale(self, grid: list[list[str]]) -> list[list[str]]:
        """Convert single boxes to connected box pairs for part 2.

        Args:
            grid: Original warehouse grid layout

        Returns
        -------
            Modified grid with expanded symbols for part 2
        """
        return [list("".join(self.maps[c] for c in line)) for line in grid]

    def scan(self, grid: list[list[str]]) -> tuple[int, int]:
        """Find starting position marked by '@' in the grid.

        Args:
            grid: Warehouse grid layout

        Returns
        -------
            Tuple of (row, col) coordinates of the starting position

        Raises
        ------
            ValueError: If no starting position is found
        """
        error_msg = "No starting position found"
        for i, row in enumerate(grid):
            if "@" in row:
                return i, row.index("@")

        raise ValueError(error_msg)

    def get_line(
        self, grid: list[list[str]], position: tuple[int, int], move: str
    ) -> tuple[list[tuple[int, int]], set[tuple[int, int]]]:
        """Get boxes in a straight line from current position.

        Args:
            grid: Current warehouse grid state
            position: Current position (row, col)
            move: Direction of movement ('^', 'v', '<', '>')

        Returns
        -------
            Tuple of (edge boxes that might block movement, all affected box positions)
        """
        y, x = position
        dy, dx = self.moves[move]
        cells: set[tuple[int, int]] = set()

        while True:
            y, x = y + dy, x + dx
            if grid[y][x] in ".#":
                return [(y - dy, x - dx)], cells

            cells.add((y, x))

    def get_group(
        self, grid: list[list[str]], position: tuple[int, int], move: str
    ) -> tuple[list[tuple[int, int]], set[tuple[int, int]]]:
        """Get connected group of boxes that need to move together.

        Args:
            grid: Current warehouse grid state
            position: Current position (row, col)
            move: Direction of movement ('^', 'v', '<', '>')

        Returns
        -------
            Tuple of (edge boxes that might block movement, all affected box positions)
        """
        dy, dx = self.moves[move]
        edges: list[tuple[int, int]] = []
        cells: set[tuple[int, int]] = set()
        queue: list[tuple[int, int]] = [position]

        while queue:
            y, x = queue.pop(0)
            if (y, x) in cells:
                continue

            cells.add((y, x))
            ny, nx = y + dy, x + dx

            if grid[ny][nx] in ".#":
                edges.append((y, x))

            elif grid[ny][nx] == "[":
                queue.extend([(ny, nx), (ny, nx + 1)])

            elif grid[ny][nx] == "]":
                queue.extend([(ny, nx), (ny, nx - 1)])

        return edges, cells - {position}

    def get_boxes(
        self, grid: list[list[str]], position: tuple[int, int], move: str, part: int
    ) -> tuple[list[tuple[int, int]], set[tuple[int, int]]]:
        """Determine boxes affected by movement based on puzzle part.

        Args:
            grid: Current warehouse grid state
            position: Current position (row, col)
            move: Direction of movement
            part: Puzzle part (1 or 2)

        Returns
        -------
            Tuple of (edge boxes, all affected boxes) based on movement rules
        """
        if part != 2 or move in "<>":
            return self.get_line(grid, position, move)
        return self.get_group(grid, position, move)

    def can_move(
        self, grid: list[list[str]], edges: list[tuple[int, int]], dy: int, dx: int
    ) -> bool:
        """Check if boxes can be moved in the specified direction.

        Args:
            grid: Current warehouse grid state
            edges: List of box positions at movement edges
            dy: Vertical movement direction
            dx: Horizontal movement direction

        Returns
        -------
            True if movement is possible, False if blocked
        """
        return not any(grid[y + dy][x + dx] == "#" for y, x in edges)

    def shift(self, grid: list[list[str]], cells: set[tuple[int, int]], move: str) -> None:
        """Move boxes in the specified direction.

        Args:
            grid: Current warehouse grid state
            cells: Set of box positions to move
            move: Direction of movement
        """

        def get_sort_key(pos: tuple[int, int]) -> int:
            """Get sorting key for box movement order."""
            return pos[0] if move in "^v" else pos[1]

        reverse = move in "v>"
        cells_ordered = sorted(cells, key=get_sort_key, reverse=reverse)

        dy, dx = self.moves[move]
        for y, x in cells_ordered:
            ny, nx = y + dy, x + dx
            grid[ny][nx] = grid[y][x]
            grid[y][x] = "."

    def step(
        self, grid: list[list[str]], position: tuple[int, int], move: str, part: int
    ) -> tuple[int, int]:
        """Process a single movement step.

        Args:
            grid: Current warehouse grid state
            position: Current position
            move: Direction to move
            part: Puzzle part (1 or 2)

        Returns
        -------
            New position after movement
        """
        y, x = position
        dy, dx = self.moves[move]
        ny, nx = y + dy, x + dx

        if grid[ny][nx] == ".":
            return ny, nx

        if grid[ny][nx] == "#":
            return position

        edges, cells = self.get_boxes(grid, position, move, part)
        if self.can_move(grid, edges, dy, dx):
            self.shift(grid, cells, move)
            return y + dy, x + dx

        return position

    def run(
        self, grid: list[list[str]], position: tuple[int, int], seq: str, part: int
    ) -> list[list[str]]:
        """Execute complete movement sequence.

        Args:
            grid: Initial warehouse grid state
            position: Starting position
            seq: Movement sequence
            part: Puzzle part (1 or 2)

        Returns
        -------
            Final grid state after all movements
        """
        y, x = position
        grid[y][x] = "."

        for move in seq:
            position = self.step(grid, position, move, part)

        return grid

    def score(self, grid: list[list[str]], part: int = 1) -> int:
        """Calculate score based on final box positions.

        Args:
            grid: Final warehouse grid state
            part: Puzzle part (1 or 2) to determine box symbol

        Returns
        -------
            Sum of weighted box positions (100 * row + col)
        """
        box = "[" if part == 2 else "O"
        total = 0

        for y, row in enumerate(grid):
            for x, cell in enumerate(row):
                if cell == box:
                    total += 100 * y + x

        return total

    def solve_part(self, data: list[str], part: int) -> int:
        """Solve part for the puzzle.

        Args:
            data: Raw input data
            part: Puzzle part to solve (1 or 2)

        Returns
        -------
            Score based on final box positions
        """
        sections = "\n".join(data).split("\n\n")
        grid = [list(line) for line in sections[0].split("\n")]
        moves = "".join(sections[1].split("\n"))

        if part == 2:
            grid = self.scale(grid)

        position = self.scan(grid)
        grid = self.run(grid, position, moves, part)

        return self.score(grid, part)

    def part1(self, data: list[str]) -> int:
        """Solve part 1: Move single boxes.

        Args:
            data: Raw input data

        Returns
        -------
            Score based on final box positions
        """
        return self.solve_part(data, 1)

    def part2(self, data: list[str]) -> int:
        """Solve part 2: Move connected box pairs.

        Args:
            data: Raw input data

        Returns
        -------
            Score based on final box positions
        """
        return self.solve_part(data, 2)
