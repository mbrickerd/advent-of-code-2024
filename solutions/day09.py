"""Day 9: Disk Fragmenter.

This module provides the solution for Advent of Code 2024 - Day 9.
It handles simulation of disk defragmentation processes and calculates checksums.

The module contains a Solution class that inherits from SolutionBase and implements
methods to parse disk blocks, move files between spaces, and calculate position-based
checksums after reorganization.
"""

from dataclasses import dataclass, field

from aoc.models.base import SolutionBase


@dataclass
class Block:
    """A block representing either a file or empty space on a disk."""

    TYPE_SPACE = 0
    TYPE_FILE = 1

    type: int
    length: int
    file_id: int | None = None
    filled_files: list[int] = field(default_factory=list)


class Solution(SolutionBase):
    """Solution for Advent of Code 2024 - Day 9: Disk Fragmenter.

    Solves puzzles involving disk defragmentation:
    - Part 1: Move files from right to left to minimize fragmentation
    - Part 2: Move files as far left as possible into available spaces
    """

    def parse_blocks(self, disk_map: str) -> list[Block]:
        """Parse disk map string into a list of file and space blocks.

        Args:
            disk_map: String of numbers representing alternating file and space sizes

        Returns
        -------
            List of Block objects representing files and spaces. Even indices are file blocks,
            odd indices are space blocks. Example: "2 1 3" creates blocks:
                [File(2), Space(1), File(3)]
        """
        numbers = [int(x) for x in disk_map]
        blocks = []
        file_id = 0

        for i, length in enumerate(numbers):
            if length == 0:
                continue

            if i % 2 == 0:  # File block
                blocks.append(Block(Block.TYPE_FILE, length, file_id))
                file_id += 1
            else:  # Space block
                blocks.append(Block(Block.TYPE_SPACE, length))

        return blocks

    def calculate_checksum(self, blocks: list[Block]) -> int:
        """Calculate checksum based on file positions after moves.

        Args:
            blocks: List of blocks after file movements

        Returns
        -------
            Checksum calculated as sum of (position * file_id) for each filled position.
            Empty spaces don't contribute to checksum.
        """
        checksum = 0
        position = 0

        for block in blocks:
            if block.type == Block.TYPE_FILE and not block.filled_files:
                for _ in range(block.length):
                    checksum += position * (block.file_id or 0)
                    position += 1
            else:
                for file_id in block.filled_files:
                    checksum += position * file_id
                    position += 1

                if block.type == Block.TYPE_SPACE:
                    position += block.length - len(block.filled_files)

        return checksum

    def part1(self, data: list[str]) -> int:
        """Move files into spaces from right to left to minimize fragmentation.

        Processes files from right to left, moving them into the rightmost
        available spaces that can fit them.

        Args:
            data: Input containing disk map string

        Returns
        -------
            Checksum of final disk state after moves
        """
        blocks = self.parse_blocks(data[0])
        working_blocks = blocks.copy()

        space_indices = [
            i for i, block in enumerate(working_blocks) if block.type == Block.TYPE_SPACE
        ]
        if not space_indices:
            return self.calculate_checksum(working_blocks)

        current_files: list[int] = []
        current_space_idx = 0

        while current_space_idx < len(space_indices):
            if not current_files:
                while (
                    working_blocks
                    and working_blocks[-1].type == Block.TYPE_SPACE
                    and not working_blocks[-1].filled_files
                ):
                    working_blocks.pop()

                if working_blocks and working_blocks[-1].type == Block.TYPE_FILE:
                    file_block = working_blocks.pop()
                    current_files = [file_block.file_id or 0] * file_block.length
                else:
                    break

            space_indices = [
                i for i, block in enumerate(working_blocks) if block.type == Block.TYPE_SPACE
            ]
            if current_space_idx >= len(space_indices):
                break

            space_idx = space_indices[current_space_idx]
            space = working_blocks[space_idx]
            remaining_space = space.length - len(space.filled_files)

            if remaining_space > 0:
                next_file = current_files.pop()
                space.filled_files.append(next_file)

                if len(space.filled_files) == space.length:
                    current_space_idx += 1
            else:
                current_space_idx += 1

        if current_files:
            working_blocks.append(Block(Block.TYPE_FILE, len(current_files), None, current_files))

        return self.calculate_checksum(working_blocks)

    def part2(self, data: list[str]) -> int:
        """Move files as far left as possible in available spaces.

        Processes files from right to left, attempting to move each file into
        the leftmost space that can accommodate it.

        Args:
            data: Input containing disk map string

        Returns
        -------
            Checksum of final disk state after moves
        """
        blocks = self.parse_blocks(data[0])

        for i in range(len(blocks) - 1, -1, -1):
            current = blocks[i]
            if current.type != Block.TYPE_FILE:
                continue

            for j in range(i):
                space = blocks[j]
                if (
                    space.type == Block.TYPE_SPACE
                    and space.length - len(space.filled_files) >= current.length
                ):
                    file_id = current.file_id or 0
                    for _ in range(current.length):
                        space.filled_files.append(file_id)

                    current.type = Block.TYPE_SPACE
                    current.file_id = None
                    current.filled_files = []
                    break

        return self.calculate_checksum(blocks)
