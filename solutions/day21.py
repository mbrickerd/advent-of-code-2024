"""Day 21: Keypad Conundrum.

This module provides the solution for Advent of Code 2024 - Day 21.
It solves a puzzle about robots translating movement codes on keypads.

The solution involves simulating robot chains that translate movement between
two different keypads - one with digits and one with directional symbols.
Each robot interprets the previous robot's movements, creating progressively
more complex translations through the chain.

The module contains a Solution class that inherits from SolutionBase and
implements methods to calculate movement complexity for chains of different lengths.
"""

from collections import defaultdict
from itertools import pairwise, product
from typing import Any, ClassVar

from aoc.models.base import SolutionBase


class Solution(SolutionBase):
    """Robot movement translation through keypad chains.

    This solution implements robot translation algorithms:
    - Part 1: Calculate movement complexity with 2-robot chains
    - Part 2: Calculate movement complexity with 25-robot chains
    """

    numeric_keypad: ClassVar[list[str]] = ["789", "456", "123", "#0A"]
    directional_keypad: ClassVar[list[str]] = ["#^A", "<v>"]

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        """Initialize the solution with empty move dictionaries and translation cache."""
        super().__init__(*args, **kwargs)
        self.moves1: dict[tuple[str, str], list[str]] = {}
        self.moves2: dict[tuple[str, str], list[str]] = {}
        self.translation_cache: dict[tuple[str, int], int] = {}

    def add_move(
        self, moves: dict[tuple[str, str], list[str]], key1: str, key2: str, movement: str
    ) -> None:
        """Add a valid movement sequence between two keys to the moves dictionary.

        Args:
            moves: Dictionary mapping key pairs to their valid movement sequences
            key1: Starting key position
            key2: Target key position
            movement: String of directional moves (combination of ^v<>)
        """
        if key1 != "#" and key2 != "#" and key1 != key2:
            moves[(key1, key2)].append(movement + "A")

    def parse_moves(self, keypad_layout: list[str]) -> dict[tuple[str, str], list[str]]:
        """Generate all possible moves between keys on a given keypad layout.

        Maps out every valid movement sequence between pairs of keys, considering:
        - Direct horizontal moves using < and >
        - Direct vertical moves using ^ and v
        - Diagonal moves trying both horizontal-then-vertical and vertical-then-horizontal
        - Avoiding the '#' obstacle and invalid positions

        Args:
            keypad_layout: List of strings representing rows of the keypad

        Returns
        -------
            Dictionary mapping key pairs (start, end) to lists of valid movement sequences
        """
        positions = {
            key: (r, c) for r, row in enumerate(keypad_layout) for c, key in enumerate(row)
        }

        moves: dict[tuple[str, str], list[str]] = defaultdict(list)
        keys = sorted(positions.keys())

        for key1, key2 in product(keys, repeat=2):
            if key1 == "#" or key2 == "#" or key1 == key2:
                continue

            r1, c1 = positions[key1]
            r2, c2 = positions[key2]
            r_hash, c_hash = positions["#"]

            if r1 == r2:
                self.add_move(moves, key1, key2, (">" if c2 > c1 else "<") * abs(c2 - c1))

            elif c1 == c2:
                self.add_move(moves, key1, key2, ("v" if r2 > r1 else "^") * abs(r2 - r1))

            else:
                if r1 != r_hash or c2 != c_hash:
                    self.add_move(
                        moves,
                        key1,
                        key2,
                        (">" if c2 > c1 else "<") * abs(c2 - c1)
                        + ("v" if r2 > r1 else "^") * abs(r2 - r1),
                    )

                if c1 != c_hash or r2 != r_hash:
                    self.add_move(
                        moves,
                        key1,
                        key2,
                        ("v" if r2 > r1 else "^") * abs(r2 - r1)
                        + (">" if c2 > c1 else "<") * abs(c2 - c1),
                    )

        return moves

    def build_combinations(self, arrays: list[list[str]]) -> list[tuple[str, ...]]:
        """Generate all possible combinations of movement sequences.

        Args:
            arrays: List of lists where each inner list contains possible movements
                   for a single step in the sequence

        Returns
        -------
            List of all possible movement sequence combinations
        """
        return list(product(*arrays))

    def translate_numpad(self, code: str) -> list[tuple[str, ...]]:
        """Convert a numeric code into possible movement sequences.

        Args:
            code: String of numeric characters to translate

        Returns
        -------
            List of possible movement sequence combinations to input the code
        """
        code = "A" + code
        moves = [self.moves1[(a, b)] for a, b in pairwise(code)]
        return self.build_combinations(moves)

    def translate_keypad(self, code: str) -> list[tuple[str, ...]]:
        """Convert a directional code into possible movement sequences.

        Args:
            code: String of directional characters to translate

        Returns
        -------
            List of possible movement sequence combinations to input the code
        """
        code = "A" + code
        moves = [self.moves2[(a, b)] if a != b else ["A"] for a, b in pairwise(code)]
        return self.build_combinations(moves)

    def translate(self, code: str, depth: int) -> int:
        """Calculate minimum moves needed for a chain of robots to input a code.

        Args:
            code: The input code to translate (either numeric or directional)
            depth: Number of robots in the chain (2 for part 1, 25 for part 2)

        Returns
        -------
            Minimum number of total moves required to input the code
        """
        cache_key = (code, depth)
        if cache_key in self.translation_cache:
            return self.translation_cache[cache_key]

        moves = self.translate_numpad(code) if code[0].isnumeric() else self.translate_keypad(code)

        if depth == 0:
            result = min(sum(len(move_part) for move_part in move) for move in moves)
            self.translation_cache[cache_key] = result
            return result

        min_cost = float("inf")
        for move in moves:
            move_cost = sum(self.translate(curr_code, depth - 1) for curr_code in move)
            min_cost = min(min_cost, move_cost)

        result = int(min_cost)
        self.translation_cache[cache_key] = result
        return result

    def solve_part(self, data: list[str], depth: int) -> int:
        """Solve puzzle by calculating complexity for robot chains.

        Args:
            data: List of input codes, each ending with 'A'
            depth: Robot chain depth (2 for part 1, 25 for part 2)

        Returns
        -------
            Total complexity score summed across all codes
        """
        if not self.moves1:
            self.moves1 = self.parse_moves(self.numeric_keypad)
            self.moves2 = self.parse_moves(self.directional_keypad)

            # Clear the translation cache
            self.translation_cache.clear()

        total = 0
        for code in data:
            code = code.strip()
            min_len = self.translate(code, depth)
            numeric_part = int(code[:-1])
            total += min_len * numeric_part

        return total

    def part1(self, data: list[str]) -> int:
        """Calculate total complexity with 2-robot chains.

        Processes each code using a chain of 2 robots, where each robot translates
        the movements of the previous robot. Complexity is calculated as the product
        of the minimum moves required and the numeric part of each code.

        Args:
            data: List of input codes, each ending with 'A'

        Returns
        -------
            Total complexity score summed across all codes
        """
        return self.solve_part(data, 2)

    def part2(self, data: list[str]) -> int:
        """Calculate total complexity with 25-robot chains.

        Similar to part 1 but uses chains of 25 robots instead of 2, resulting in
        more complex movement translations and potentially higher complexity scores.

        Args:
            data: List of input codes, each ending with 'A'

        Returns
        -------
            Total complexity score summed across all codes using 25-robot chains
        """
        return self.solve_part(data, 25)
