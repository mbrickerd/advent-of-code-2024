"""Day 14: Restroom Redoubt.

This module provides the solution for Advent of Code 2024 - Day 14.
It simulates robots moving in a wrapping grid space with specific velocities,
tracking their positions over time to solve spatial puzzles.

Each robot has an initial position and velocity, and moves in a grid where
going beyond boundaries causes wrapping to the opposite side. The solution
tracks collisions and quadrant distributions of robots.

The module contains a Solution class that inherits from SolutionBase and implements
methods to parse robot configurations, calculate positions over time, and solve
various spatial puzzles.
"""

from typing import NamedTuple

from aoc.models.base import SolutionBase


class Position(NamedTuple):
    """Represents a 2D coordinate position.

    Attributes
    ----------
        x: X-coordinate in the grid
        y: Y-coordinate in the grid
    """

    x: int
    y: int


class Robot(NamedTuple):
    """Represents a robot with its current position and velocity.

    Attributes
    ----------
        pos: Position containing the robot's current (x, y) coordinates
        velocity: Position containing the robot's (dx, dy) velocity components
    """

    pos: Position
    velocity: Position


class Solution(SolutionBase):
    """Solution for Advent of Code 2024 - Day 14: Restroom Redoubt.

    This class solves a puzzle involving robots moving in a confined grid space,
    where each robot has an initial position and velocity. The robots move in a
    wrapping grid pattern, and their positions must be tracked over time.

    Input format:
        List of strings where each line represents a robot with:
        - Initial position (p=x,y)
        - Initial velocity (v=x,y)
    """

    def parse_data(self, data: list[str]) -> list[Robot]:
        """Parse input data into a list of Robot objects.

        Args:
            data: List of strings containing robot position and velocity data

        Returns
        -------
            List of Robot objects with initial positions and velocities
        """
        robots = []
        for line in data:
            pos_str, vel_str = line.split(" ")
            x, y = map(int, pos_str[2:].split(","))
            dx, dy = map(int, vel_str[2:].split(","))
            robots.append(Robot(Position(x, y), Position(dx, dy)))
        return robots

    def get_grid_size(self, robots: list[Robot]) -> tuple[int, int]:
        """Determine the size of the grid based on number of robots.

        Different grid sizes are used for the sample input (12 robots)
        versus the actual puzzle input.

        Args:
            robots: List of Robot objects

        Returns
        -------
            Tuple of (width, height) representing grid dimensions
        """
        return (11, 7) if len(robots) == 12 else (101, 103)

    def get_position_at_time(self, robot: Robot, time: int, width: int, height: int) -> Position:
        """Calculate a robot's position after a given amount of time.

        Handles wrapping movement where robots that move beyond grid boundaries
        appear on the opposite side.

        Args:
            robot: Robot object with initial position and velocity
            time: Number of time steps to simulate
            width: Grid width
            height: Grid height

        Returns
        -------
            Position representing robot's location after specified time
        """
        x = (robot.pos.x + time * robot.velocity.x) % width
        y = (robot.pos.y + time * robot.velocity.y) % height
        return Position(x, y)

    def part1(self, data: list[str]) -> int:
        """Calculate product of robots in each quadrant after 100 time steps.

        Divides the grid into four quadrants and counts robots in each,
        excluding robots on the center lines. Returns the product of these counts.

        Args:
            data: List of strings containing robot configurations

        Returns
        -------
            Product of robot counts in each quadrant
        """
        robots = self.parse_data(data)
        width, height = self.get_grid_size(robots)
        mid_x, mid_y = width // 2, height // 2

        quads = [0] * 4
        for robot in robots:
            pos = self.get_position_at_time(robot, 100, width, height)
            if pos.x == mid_x or pos.y == mid_y:
                continue

            quad_idx = (int(pos.x > mid_x)) + (int(pos.y > mid_y) * 2)
            quads[quad_idx] += 1

        return quads[0] * quads[1] * quads[2] * quads[3]

    def part2(self, data: list[str]) -> int:
        """Find first time when robots collide.

        Simulates robot movement until two or more robots occupy the same position,
        indicating a collision.

        Args:
            data: List of strings containing robot configurations

        Returns
        -------
            Time step when the first collision occurs
        """
        robots = self.parse_data(data)
        width, height = self.get_grid_size(robots)

        for time in range(1, 10000):
            positions = set()
            for robot in robots:
                pos = self.get_position_at_time(robot, time, width, height)
                if pos in positions:
                    return time

                positions.add(pos)

        return -1
