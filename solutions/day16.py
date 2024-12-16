from typing import List, Tuple

from aoc.models.base import SolutionBase


class Solution(SolutionBase):
    """Solution for Advent of Code 2024 - Day 16: Reindeer Maze.

    This class solves a puzzle involving finding optimal paths through a maze with
    movement costs. Reindeer start facing east and can move forward (cost 1) or rotate
    90 degrees (cost 1000). Part 1 finds the minimum cost to reach the end, while Part 2
    counts all tiles that are part of any optimal path.

    Input format:
        - Grid of characters where:
            '#' represents walls
            'S' represents the starting position
            'E' represents the ending position
            '.' represents empty space

    This class inherits from `SolutionBase` and provides methods to find and analyze
    optimal paths through the maze considering movement and rotation costs.
    """

    def find_start_end(self, grid: List[List[str]]) -> Tuple[Tuple[int, int], Tuple[int, int]]:
        """Find the start and end positions in the maze.

        Args:
            grid (List[List[str]]): 2D grid representation of the maze where 'S' marks
                the start and 'E' marks the end.

        Returns:
            Tuple containing:
                - Tuple[int, int]: Coordinates (y, x) of start position
                - Tuple[int, int]: Coordinates (y, x) of end position
        """
        start = end = None
        for y, row in enumerate(grid):
            for x, cell in enumerate(row):
                if cell == "S":
                    start = (y, x)

                elif cell == "E":
                    end = (y, x)

                if start and end:
                    return start, end

        return start, end

    def find_routes(self, data: List[str]) -> List[Tuple[List[Tuple[int, int]], int]]:
        """Find all possible routes through the maze and their costs.

        Args:
            data (List[str]): Input lines representing the maze grid.

        Returns:
            List[Tuple[List[Tuple[int, int]], int]]: List of tuples where each contains:
                - List[Tuple[int, int]]: List of coordinates representing the path
                - int: Total cost of the path (1 per forward move, 1000 per rotation)

        The function uses a breadth-first search approach, tracking:
            - Complete path history for each route
            - Movement costs (forward=1, rotation=1000)
            - Direction facing (0=right, 1=up, 2=left, 3=down)
            - Previously visited states to avoid cycles
        """
        # Convert input to grid
        grid = [list(row) for row in data]
        start, end = self.find_start_end(grid)

        # Direction vectors: right, up, left, down
        directions = [(0, 1), (-1, 0), (0, -1), (1, 0)]
        routes = []
        visited = {}  # (pos, direction) -> min_score

        # Queue: (position, path_history, current_score, current_direction)
        queue = [(start, [start], 0, 0)]  # Start facing right (0)

        while queue:
            pos, history, curr_score, curr_dir = queue.pop(0)
            y, x = pos

            # Check if we reached the end
            if pos == end:
                routes.append((history, curr_score))
                continue

            # Check if we've seen this state with a better score
            state = (pos, curr_dir)
            if state in visited and visited[state] < curr_score:
                continue

            visited[state] = curr_score

            # Try each direction
            for new_dir, (dy, dx) in enumerate(directions):
                # Skip reverse direction
                if (curr_dir + 2) % 4 == new_dir:
                    continue

                new_y, new_x = y + dy, x + dx
                
                # Check if new position is valid
                if (
                    0 <= new_y < len(grid)
                    and 0 <= new_x < len(grid[0])
                    and grid[new_y][new_x] != "#"
                    and (new_y, new_x) not in history
                ):

                    if new_dir == curr_dir:
                        # Moving forward
                        queue.append(
                            ((new_y, new_x), history + [(new_y, new_x)], curr_score + 1, new_dir)
                        )
                    else:
                        # Turning (stay in same position)
                        queue.append((pos, history, curr_score + 1000, new_dir))

        return routes

    def part1(self, data: List[str]) -> int:
        """Find the minimum cost to reach the end of the maze.

        Args:
            data (List[str]): Input lines representing the maze grid.

        Returns:
            int: Minimum total cost (moves + rotations) to reach the end position
                while starting facing east.
        """
        possible_routes = self.find_routes(data)
        return min(route[1] for route in possible_routes)

    def part2(self, data: List[str]) -> int:
        """Count tiles that are part of any optimal (minimum cost) path through the maze.

        Args:
            data (List[str]): Input lines representing the maze grid.

        Returns:
            int: Number of unique tiles (positions) that appear in any path that
                reaches the end with minimum total cost.
        """
        possible_routes = self.find_routes(data)
        min_score = min(route[1] for route in possible_routes)
        best_routes = [route for route in possible_routes if route[1] == min_score]
        optimal_tiles = {tile for route in best_routes for tile in route[0]}
        return len(optimal_tiles)
