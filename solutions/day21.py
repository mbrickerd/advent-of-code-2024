from collections import defaultdict
from functools import cache
from itertools import product
from typing import Dict, List, Tuple

from aoc.models.base import SolutionBase


class Solution(SolutionBase):
    """Solution for Advent of Code 2024 - Day 21: Keypad Conundrum.

    This class solves a puzzle about robots translating movement codes on keypads.
    Part 1 calculates movement complexity with 2 robots, while Part 2 extends
    the chain to 25 robots for more complex translations.

    Input format:
        - List of codes, one per line
        - Each code ends with 'A'
        - Codes can be numeric (0-9) or directional (^v<>)
        - Numeric part of code determines weighting in complexity calculation

    This class inherits from `SolutionBase` and provides methods to parse keypad
    layouts, translate movement codes, and calculate total complexity scores.
    """

    numeric_keypad = ["789", "456", "123", "#0A"]
    directional_keypad = ["#^A", "<v>"]

    def add_move(
        self, moves: Dict[Tuple[str, str], List[str]], key1: str, key2: str, movement: str
    ) -> None:
        """Add a valid movement sequence between two keys to the moves dictionary.

        Validates and stores a movement sequence between two keys, excluding any moves
        involving the '#' key or self-moves. Appends 'A' to confirm each movement.

        Args:
            moves: Dictionary mapping key pairs to their valid movement sequences
            key1: Starting key position
            key2: Target key position
            movement: String of directional moves (combination of ^v<>)
        """
        if key1 != "#" and key2 != "#" and key1 != key2:
            moves[(key1, key2)].append(movement + "A")

    def parse_moves(self, keypad_layout: List[str]) -> Dict[Tuple[str, str], List[str]]:
        """Generate all possible moves between keys on a given keypad layout.

        Maps out every valid movement sequence between pairs of keys, considering:
        - Direct horizontal moves using < and >
        - Direct vertical moves using ^ and v
        - Diagonal moves trying both horizontal-then-vertical and vertical-then-horizontal
        - Avoiding the '#' obstacle and invalid positions

        Args:
            keypad_layout: List of strings representing rows of the keypad

        Returns:
            Dictionary mapping key pairs (start, end) to lists of valid movement sequences
        """
        positions = {
            key: (r, c) for r, row in enumerate(keypad_layout) for c, key in enumerate(row)
        }

        moves = defaultdict(list)
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

    def build_combinations(self, arrays: List[List[str]]) -> List[List[str]]:
        """Generate all possible combinations of movement sequences.

        Uses itertools.product to efficiently generate all possible combinations
        of movement sequences for a series of moves.

        Args:
            arrays: List of lists where each inner list contains possible movements
                   for a single step in the sequence

        Returns:
            List of all possible movement sequence combinations
        """
        return list(product(*arrays))

    @cache
    def translate(self, code: str, depth: int) -> int:
        """Calculate minimum moves needed for a chain of robots to input a code.

        Recursively determines the shortest sequence of moves needed for the robot
        chain to input the given code, where each robot translates the movements
        of the previous robot.

        Args:
            code: The input code to translate (either numeric or directional)
            depth: Number of robots in the chain (2 for part 1, 25 for part 2)

        Returns:
            Minimum number of total moves required to input the code
        """
        moves = self.translate_numpad(code) if code[0].isnumeric() else self.translate_keypad(code)

        if depth == 0:
            return min(sum(map(len, move)) for move in moves)

        return min(
            sum(self.translate(curr_code, depth - 1) for curr_code in move) for move in moves
        )

    def translate_numpad(self, code: str) -> List[List[str]]:
        """Convert a numeric code into possible movement sequences.

        Translates a sequence of numeric inputs into all possible movement
        combinations on the numeric keypad.

        Args:
            code: String of numeric characters to translate

        Returns:
            List of possible movement sequence combinations to input the code
        """
        code = "A" + code  # Start from A position
        moves = [self.moves1[(a, b)] for a, b in zip(code, code[1:])]
        return self.build_combinations(moves)

    def translate_keypad(self, code: str) -> List[List[str]]:
        """Convert a directional code into possible movement sequences.

        Translates a sequence of directional inputs into all possible movement
        combinations on the directional keypad, handling self-moves with 'A'.

        Args:
            code: String of directional characters to translate

        Returns:
            List of possible movement sequence combinations to input the code
        """
        code = "A" + code  # Start from A position
        moves = [self.moves2[(a, b)] if a != b else ["A"] for a, b in zip(code, code[1:])]
        return self.build_combinations(moves)

    def part1(self, data: List[str]) -> int:
        """Calculate total complexity with 2-robot chains.

        Processes each code using a chain of 2 robots, where each robot translates
        the movements of the previous robot. Complexity is calculated as the product
        of the minimum moves required and the numeric part of each code.

        Args:
            data: List of input codes, each ending with 'A'

        Returns:
            Total complexity score summed across all codes
        """
        self.moves1 = self.parse_moves(self.numeric_keypad)
        self.moves2 = self.parse_moves(self.directional_keypad)

        total_complexity = 0
        for code in data:
            code = code.strip()
            min_len = self.translate(code, 2)  # Depth 2 for the chain of commands
            numeric_part = int(code[:-1])  # Remove 'A' and convert to int
            total_complexity += min_len * numeric_part

        return total_complexity

    def part2(self, data: List[str]) -> int:
        """Calculate total complexity with 25-robot chains.

        Similar to part 1 but uses chains of 25 robots instead of 2, resulting in
        more complex movement translations and potentially higher complexity scores.

        Args:
            data: List of input codes, each ending with 'A'

        Returns:
            Total complexity score summed across all codes using 25-robot chains
        """
        self.moves1 = self.parse_moves(self.numeric_keypad)
        self.moves2 = self.parse_moves(self.directional_keypad)

        complexities = 0
        for code in data:
            min_len = self.translate(code, 25)  # 25 robots instead of 2
            complexities += min_len * int(code[:-1])

        return complexities
