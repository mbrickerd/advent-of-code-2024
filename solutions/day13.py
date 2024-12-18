import re
from typing import List, Tuple

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

    button_regex = r"Button [AB]: X\+(\d+), Y\+(\d+)"
    prize_regex = r"Prize: X=(\d+), Y=(\d+)"
    OFFSET = 10000000000000

    def extract(self, coord: str, ext_type: str) -> Tuple[int, int]:
        """Extract X and Y coordinates from button or prize position strings.

        Args:
            coord: String containing coordinate information
            ext_type: Type of coordinates to extract ("button" or "prize")

        Returns:
            Tuple of (x, y) coordinates extracted from the string
        """
        pattern = self.button_regex if ext_type == "button" else self.prize_regex
        return tuple(map(int, re.findall(pattern, coord)[0]))

    def solve_machine(
        self,
        btn_a: Tuple[int, int],
        btn_b: Tuple[int, int],
        prize: Tuple[int, int],
        limit: int | None = 100,
    ) -> int | None:
        """Calculate minimum tokens needed to reach prize coordinates using button presses.

        Uses Cramer's rule to solve the system of linear equations that determine
        how many times each button needs to be pressed to reach the prize coordinates.

        Args:
            btn_a: Tuple of (x, y) movement per Button A press
            btn_b: Tuple of (x, y) movement per Button B press
            prize: Tuple of (x, y) target prize coordinates
            limit: Maximum allowed button presses (None for unlimited)

        Returns:
            Total tokens needed (3 per Button A press + 1 per Button B press),
            or None if no valid solution exists
        """
        denominator = btn_b[1] * btn_a[0] - btn_b[0] * btn_a[1]
        if denominator == 0:
            return None

        times_b = (prize[1] * btn_a[0] - prize[0] * btn_a[1]) / denominator
        times_a = (prize[0] - btn_b[0] * times_b) / btn_a[0]

        if times_a.is_integer() and times_b.is_integer():
            if limit is None or (0 <= times_a <= limit and 0 <= times_b <= limit):
                return int(times_a) * 3 + int(times_b)

        return None

    def calculate_coins(self, data: List[str], part2: bool = False) -> int:
        """Process all claw machines and calculate total tokens needed.

        Parses input data into individual machine configurations and calculates
        the minimum tokens needed for each winnable prize.

        Args:
            data: List of strings containing machine configurations
            part2: Whether to apply the large coordinate offset for part 2

        Returns:
            Total tokens needed to win all possible prizes
        """
        machines = ("\n".join(data)).split("\n\n")
        coins = 0

        for machine in machines:
            btn_a, btn_b, prize = machine.split("\n")

            btn_a_coords = self.extract(btn_a, "button")
            btn_b_coords = self.extract(btn_b, "button")
            prize_coords = self.extract(prize, "prize")

            if part2:
                prize_coords = (
                    prize_coords[0] + self.OFFSET,
                    prize_coords[1] + self.OFFSET,
                )

            if result := self.solve_machine(
                btn_a_coords, btn_b_coords, prize_coords, None if part2 else 100
            ):
                coins += result

        return coins

    def part1(self, data: List[str]) -> int:
        """Calculate minimum tokens needed with standard prize coordinates.

        Args:
            data: List of strings containing machine configurations

        Returns:
            Total tokens needed when each button press is limited to 100
        """
        return self.calculate_coins(data)

    def part2(self, data: List[str]) -> int:
        """Calculate minimum tokens needed with offset prize coordinates.

        Args:
            data: List of strings containing machine configurations

        Returns:
            Total tokens needed when prizes are offset by 10^13 units
        """
        return self.calculate_coins(data, True)
