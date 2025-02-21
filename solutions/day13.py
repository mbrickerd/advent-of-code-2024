"""Day 13: Claw Contraption.

This module provides the solution for Advent of Code 2024 - Day 13.
It handles calculating the minimum number of tokens needed to win prizes in a
claw machine game, where two buttons control the movement of the claw.

Each button press moves the claw by specific X and Y coordinates, and the goal
is to reach prize locations using the minimum number of button presses.

The module contains a Solution class that inherits from SolutionBase and implements
methods to parse machine configurations, calculate required button presses using
Cramer's rule, and determine the minimum number of tokens needed to win prizes.
"""

import re

from aoc.models.base import SolutionBase


class Solution(SolutionBase):
    """Solution for Advent of Code 2024 - Day 13: Claw Contraption.

    This class solves a puzzle involving a claw machine game where two buttons control
    the movement of a claw. Each button press moves the claw by specific X and Y
    coordinates, and the goal is to reach prize locations using the minimum number
    of button presses.

    Input format:
        Groups of three lines representing claw machines, where each group contains:
        - Button A's movement coordinates (X+n, Y+n)
        - Button B's movement coordinates (X+n, Y+n)
        - Prize coordinates (X=n, Y=n)

    This class inherits from `SolutionBase` and provides methods to parse machine
    configurations, calculate required button presses using Cramer's rule, and
    determine the minimum number of tokens needed to win prizes.
    """

    BUTTON_REGEX = r"Button [AB]: X\+(\d+), Y\+(\d+)"
    PRIZE_REGEX = r"Prize: X=(\d+), Y=(\d+)"
    OFFSET = 10**13

    def extract(self, coord: str, pattern: str) -> tuple[int, int]:
        """Extract X and Y coordinates from button or prize position strings.

        Args:
            coord: String containing coordinate information
            pattern: Regular expression pattern to match coordinates

        Returns
        -------
            Tuple of (x, y) coordinates extracted from the string
        """
        match = re.findall(pattern, coord)
        if match:
            return (int(match[0][0]), int(match[0][1]))

        return (0, 0)

    def solve_machine(
        self,
        btn_a: tuple[int, int],
        btn_b: tuple[int, int],
        prize: tuple[int, int],
    ) -> int | None:
        """Calculate minimum tokens needed to reach prize coordinates using button presses.

        Uses Cramer's rule to solve the system of linear equations that determine
        how many times each button needs to be pressed to reach the prize coordinates.

        Args:
            btn_a: Tuple of (x, y) movement per Button A press
            btn_b: Tuple of (x, y) movement per Button B press
            prize: Tuple of (x, y) target prize coordinates

        Returns
        -------
            Total tokens needed (3 per Button A press + 1 per Button B press),
            or None if no valid solution exists
        """
        ax, ay = btn_a
        bx, by = btn_b
        px, py = prize

        denominator = by * ax - bx * ay
        if denominator == 0:
            return None

        times_b = (py * ax - px * ay) / denominator
        times_a = (px - bx * times_b) / ax

        if times_a.is_integer() and times_b.is_integer() and times_a >= 0 and times_b >= 0:
            return int(times_a * 3 + times_b)

        return None

    def calculate_coins(self, data: list[str], offset: int = 0) -> int:
        """Process all claw machines and calculate total tokens needed.

        Parses input data into individual machine configurations and calculates
        the minimum tokens needed for each winnable prize.

        Args:
            data: List of strings containing machine configurations
            offset: Coordinate offset to apply to prize locations (default: 0)

        Returns
        -------
            Total tokens needed to win all possible prizes
        """
        coins = 0

        for machine in ("\n".join(data)).split("\n\n"):
            btn_a, btn_b, prize = map(str.strip, machine.split("\n"))

            btn_a_coords = self.extract(btn_a, self.BUTTON_REGEX)
            btn_b_coords = self.extract(btn_b, self.BUTTON_REGEX)
            prize_coords = (
                self.extract(prize, self.PRIZE_REGEX)[0] + offset,
                self.extract(prize, self.PRIZE_REGEX)[1] + offset,
            )

            result = self.solve_machine(btn_a_coords, btn_b_coords, prize_coords)
            coins += result if result is not None else 0

        return coins

    def part1(self, data: list[str]) -> int:
        """Calculate minimum tokens needed with standard prize coordinates.

        Args:
            data: List of strings containing machine configurations

        Returns
        -------
            Total tokens needed when each button press is limited to 100
        """
        return self.calculate_coins(data)

    def part2(self, data: list[str]) -> int:
        """Calculate minimum tokens needed with offset prize coordinates.

        Args:
            data: List of strings containing machine configurations

        Returns
        -------
            Total tokens needed when prizes are offset by 10^13 units
        """
        return self.calculate_coins(data, self.OFFSET)
