from typing import List, Set, Tuple

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

    moves = {
        "^": (-1, 0),
        "v": (1, 0),
        "<": (0, -1),
        ">": (0, 1),
    }
    maps = {"#": "##", "O": "[]", ".": "..", "@": "@."}

    def scale(self, grid: List[List[str]]) -> List[List[str]]:
        """Convert single boxes to connected box pairs for part 2.

        Args:
            grid: Original warehouse grid layout

        Returns:
            Modified grid with expanded symbols for part 2
        """
        return [list("".join(self.maps[c] for c in line)) for line in grid]

    def scan(self, grid: List[List[str]]) -> Tuple[int, int]:
        """Find starting position marked by '@' in the grid.

        Args:
            grid: Warehouse grid layout

        Returns:
            Tuple of (row, col) coordinates of the starting position

        Raises:
            ValueError: If no starting position is found
        """
        for i, row in enumerate(grid):
            for j, cell in enumerate(row):
                if cell == "@":
                    return (i, j)

        raise ValueError("No @ found")

    def get_line(
        self, grid: List[List[str]], position: Tuple[int, int], move: str
    ) -> Tuple[List[Tuple[int, int]], Set[Tuple[int, int]]]:
        """Get boxes in a straight line from current position.

        Args:
            grid: Current warehouse grid state
            position: Current position (row, col)
            move: Direction of movement ('^', 'v', '<', '>')

        Returns:
            Tuple of (edge boxes that might block movement, all affected box positions)
        """
        y, x = position
        dir_y, dir_x = self.moves[move]
        cells = set()

        while True:
            new_y, new_x = y + dir_y, x + dir_x
            if grid[new_y][new_x] in ".#":
                return [(new_y - dir_y, new_x - dir_x)], cells
            y, x = new_y, new_x
            cells.add((y, x))

    def get_group(
        self, grid: List[List[str]], position: Tuple[int, int], move: str
    ) -> Tuple[List[Tuple[int, int]], Set[Tuple[int, int]]]:
        """Get connected group of boxes that need to move together.

        Args:
            grid: Current warehouse grid state
            position: Current position (row, col)
            move: Direction of movement ('^', 'v', '<', '>')

        Returns:
            Tuple of (edge boxes that might block movement, all affected box positions)
        """
        dir_y, dir_x = self.moves[move]
        edges = []
        cells = set()

        q = [(position[0], position[1])]
        while q:
            y, x = q.pop(0)
            if (y, x) in cells:
                continue

            cells.add((y, x))
            new_y, new_x = y + dir_y, x + dir_x

            if grid[new_y][new_x] in ".#":
                edges.append((y, x))

            elif grid[new_y][new_x] == "[":
                q.extend([(new_y, new_x), (new_y, new_x + 1)])

            elif grid[new_y][new_x] == "]":
                q.extend([(new_y, new_x), (new_y, new_x - 1)])

        return edges, cells - {position}

    def get_boxes(
        self, grid: List[List[str]], position: Tuple[int, int], move: str, part: int
    ) -> Tuple[List[Tuple[int, int]], Set[Tuple[int, int]]]:
        """Determine boxes affected by movement based on puzzle part.

        Args:
            grid: Current warehouse grid state
            position: Current position (row, col)
            move: Direction of movement
            part: Puzzle part (1 or 2)

        Returns:
            Tuple of (edge boxes, all affected boxes) based on movement rules
        """
        return (
            self.get_line(grid, position, move)
            if not part == 2 or move in "<>"
            else self.get_group(grid, position, move)
        )

    def can_move(
        self,
        grid: List[List[str]],
        edges: List[Tuple[int, int]],
        dir_y: int,
        dir_x: int,
    ) -> bool:
        """Check if boxes can be moved in the specified direction.

        Args:
            grid: Current warehouse grid state
            edges: List of box positions at movement edges
            dir_y: Vertical movement direction
            dir_x: Horizontal movement direction

        Returns:
            `True` if movement is possible, `False` if blocked
        """
        return not any(grid[box[0] + dir_y][box[1] + dir_x] == "#" for box in edges)

    def get_sort_key(self, coord: Tuple[int, int], move: str) -> int:
        """Get sorting key for box movement order.

        Args:
            coord: Box position coordinates
            move: Movement direction

        Returns:
            Integer key for sorting boxes in movement order
        """
        return coord[0] if move in "^v" else coord[1]

    def shift(self, grid: List[List[str]], cells: Set[Tuple[int, int]], move: str) -> None:
        """Move boxes in the specified direction.

        Args:
            grid: Current warehouse grid state
            cells: Set of box positions to move
            move: Direction of movement
        """
        reverse = move in "v>"
        sorted_cells = sorted(cells, key=lambda x: self.get_sort_key(x, move), reverse=reverse)
        dir_y, dir_x = self.moves[move]

        for y, x in sorted_cells:
            new_y, new_x = y + dir_y, x + dir_x
            grid[new_y][new_x] = grid[y][x]
            grid[y][x] = "."

    def step(
        self, grid: List[List[str]], position: Tuple[int, int], move: str, part: int
    ) -> Tuple[int, int]:
        """Process a single movement step.

        Args:
            grid: Current warehouse grid state
            position: Current position
            move: Direction to move
            part: Puzzle part (1 or 2)

        Returns:
            New position after movement
        """
        dir_y, dir_x = self.moves[move]
        new_y, new_x = position[0] + dir_y, position[1] + dir_x

        if grid[new_y][new_x] == ".":
            return (new_y, new_x)

        if grid[new_y][new_x] == "#":
            return position

        edges, cells = self.get_boxes(grid, position, move, part)
        if self.can_move(grid, edges, dir_y, dir_x):
            self.shift(grid, cells, move)
            return (position[0] + dir_y, position[1] + dir_x)

        return position

    def run(
        self, grid: List[List[str]], position: Tuple[int, int], seq: str, part: int
    ) -> List[List[str]]:
        """Execute complete movement sequence.

        Args:
            grid: Initial warehouse grid state
            position: Starting position
            seq: Movement sequence
            part: Puzzle part (1 or 2)

        Returns:
            Final grid state after all movements
        """
        grid[position[0]][position[1]] = "."

        for move in seq:
            position = self.step(grid, position, move, part)

        return grid

    def score(self, grid: List[List[str]], part: int = 1) -> int:
        """Calculate score based on final box positions.

        Args:
            grid: Final warehouse grid state
            part: Puzzle part (1 or 2) to determine box symbol

        Returns:
            Sum of weighted box positions (100 * row + col)
        """
        box = "[" if part == 2 else "O"
        return sum(
            100 * y + x for y, row in enumerate(grid) for x, cell in enumerate(row) if cell == box
        )

    def solve_part(self, data: List[str], part: int) -> int:
        """Common solving logic for both puzzle parts.

        Args:
            data: Raw input data
            part: Puzzle part to solve (1 or 2)

        Returns:
            Score based on final box positions
        """
        grid, moves = "\n".join(data).split("\n\n")
        grid = [list(row) for row in grid.split("\n")]
        moves = list("".join(moves.split("\n")))

        if part == 2:
            grid = self.scale(grid)

        position = self.scan(grid)
        grid = self.run(grid, position, moves, part)

        return self.score(grid, part)

    def part1(self, data: List[str]) -> int:
        """Solve part 1: Move single boxes.

        Args:
            data: Raw input data

        Returns:
            Score based on final box positions
        """
        return self.solve_part(data, 1)

    def part2(self, data: List[str]) -> int:
        """Solve part 2: Move connected box pairs.

        Args:
            data: Raw input data

        Returns:
            Score based on final box positions
        """
        return self.solve_part(data, 2)
