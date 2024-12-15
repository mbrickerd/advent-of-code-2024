from typing import List, NamedTuple, Set, Tuple

from aoc.models.base import SolutionBase


class Position(NamedTuple):
    """Find first time when robots collide.

    Simulates robot movement until two or more robots occupy the same position,
    indicating a collision.

    Args:
        data: List of strings containing robot configurations

    Returns:
        Time step when the first collision occurs
    """

    x: int
    y: int


class Robot(NamedTuple):
    """Represents a robot with its current position and velocity.

    Attributes:
        pos: Position namedtuple containing the robot's current (x, y) coordinates
        velocity: Position namedtuple containing the robot's (dx, dy) velocity components
    """

    pos: Position
    velocity: Position


class Solution(SolutionBase):
    """Solution for Advent of Code 2024 - Day 14: Restroom Redoubt.

    This class solves a puzzle involving robots moving in a confined grid space,
    where each robot has an initial position and velocity. The robots move in a
    wrapping grid pattern, and their positions must be tracked over time to solve
    various spatial puzzles.

    Input format:
        List of strings where each line represents a robot with:
        - Initial position (p=x,y)
        - Initial velocity (V=x,y)
        Example: "p=0,4 v=3,-3"

    The solution uses custom Position and Robot namedtuples to track robot states
    and implements methods to calculate robot positions over time in a wrapping
    grid space.
    """

    def parse_data(self, data: List[str]) -> List[Robot]:
        """Parse input data into a list of Robot objects.

        Args:
            data: List of strings containing robot position and velocity data

        Returns:
            List of Robot objects with initial positions and velocities
        """
        robots = []
        for line in data:
            pos_str, vel_str = line.split(" ")
            x, y = map(int, pos_str[2:].split(","))
            velocity_x, velocity_y = map(int, vel_str[2:].split(","))
            robots.append(Robot(Position(x, y), Position(velocity_x, velocity_y)))

        return robots

    def get_grid_size(self, robots: List[Robot]) -> Tuple[int, int]:
        """Determine the size of the grid based on number of robots.

        Different grid sizes are used for the sample input (12 robots)
        versus the actual puzzle input.

        Args:
            robots: List of Robot objects

        Returns:
            Tuple of (width, height) representing grid dimensions
        """
        return (101, 103) if len(robots) != 12 else (11, 7)

    def get_position_at_time(self, robot: Robot, time: int, width: int, height: int) -> Position:
        """Calculate a robot's position after a given amount of time.

        Handles wrapping movement where robots that move beyond grid boundaries
        appear on the opposite side.

        Args:
            robot: Robot object with initial position and velocity
            time: Number of time steps to simulate
            width: Grid width
            height: Grid height

        Returns:
            Position representing robot's location after specified time
        """
        x = (robot.pos.x + time * (robot.velocity.x + width)) % width
        y = (robot.pos.y + time * (robot.velocity.y + height)) % height
        return Position(x, y)

    def part1(self, data: List[str]) -> int:
        """Calculate product of robots in each quadrant after 100 time steps.

        Divides the grid into four quadrants and counts robots in each,
        excluding robots on the center lines. Returns the product of these counts.

        Args:
            data: List of strings containing robot configurations

        Returns:
            Product of robot counts in each quadrant
        """
        robots = self.parse_data(data)
        width, height = self.get_grid_size(robots)

        quads = [0] * 4

        for robot in robots:
            position = self.get_position_at_time(robot, 100, width, height)

            if position.x == width // 2 or position.y == height // 2:
                continue

            quad_idx = (int(position.x > width // 2)) + (int(position.y > height // 2) * 2)
            quads[quad_idx] += 1

        return quads[0] * quads[1] * quads[2] * quads[3]

    def part2(self, data: List[str]) -> int:
        """Find first time when robots collide.

        Simulates robot movement until two or more robots occupy the same position,
        indicating a collision.

        Args:
            data: List of strings containing robot configurations

        Returns:
            Time step when the first collision occurs
        """
        robots = self.parse_data(data)
        width, height = self.get_grid_size(robots)

        time = 0
        while True:
            time += 1
            position: Set[Position] = set()

            for robot in robots:
                new_pos = self.get_position_at_time(robot, time, width, height)
                if new_pos in position:
                    break

                position.add(new_pos)

            else:  # no breaks occurred - valid solution found
                return time
