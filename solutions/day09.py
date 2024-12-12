from dataclasses import dataclass
from typing import List, Optional

from aoc.models.base import SolutionBase


@dataclass
class Block:
    """A block representing either a file or empty space on a disk.

    Attributes:
        type (int): Block type - either `TYPE_SPACE` (0) or `TYPE_FILE` (1)
        length (int): Length of this block
        file_id (Optional[int]): Identifier for file blocks, None for space blocks
        filled_files (List[int]): List of file IDs stored in this block
    """

    TYPE_SPACE = 0
    TYPE_FILE = 1

    type: int
    length: int
    file_id: Optional[int] = None  # Only used for file blocks
    filled_files: List[int] = None  # Only used for space blocks

    def __post_init__(self) -> None:
        """Initialize empty filled_files list if `None`."""
        if self.filled_files is None:
            self.filled_files = []


class Solution(SolutionBase):
    """Solution for Advent of Code 2024 - Day 9: Disk Fragmenter.

    This class solves a puzzle involving disk defragmentation. Part 1 simulates moving
    files into available spaces from right to left to minimize fragmentation, while
    Part 2 attempts to move files as far left as possible. Both parts calculate a
    checksum based on file positions after moves.

    Input format:
        A string of numbers where even indices represent file sizes and odd indices
        represent space sizes. Zeros are ignored.

    This class inherits from `SolutionBase` and provides methods to parse disk blocks
    and simulate file movements.
    """

    def parse_blocks(self, disk_map: str) -> List[Block]:
        """Parse disk map string into a list of file and space blocks.

        Args:
            disk_map (str): String of numbers representing alternating file and space sizes

        Returns:
            List[Block]: List of Block objects representing files and spaces.
                Even indices are file blocks, odd indices are space blocks.
                Example: "2 1 3" creates blocks [File(2), Space(1), File(3)]
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

    def calculate_checksum(self, blocks: List[Block]) -> int:
        """Calculate checksum based on file positions after moves.

        Args:
            blocks (List[Block]): List of blocks after file movements

        Returns:
            int: Checksum calculated as sum of (position * file_id) for each
                filled position. Empty spaces don't contribute to checksum.
        """
        checksum = 0
        position = 0

        for block in blocks:
            if block.type == Block.TYPE_FILE and not block.filled_files:
                # Original file block that hasn't been moved
                for _ in range(block.length):
                    checksum += position * block.file_id
                    position += 1
            else:
                # Use filled_files for both filled spaces and moved file blocks
                for file_id in block.filled_files:
                    checksum += position * file_id
                    position += 1

                # Skip remaining unfilled space if it's a space block
                if block.type == Block.TYPE_SPACE:
                    position += block.length - len(block.filled_files)

        return checksum

    def part1(self, data: List[str]) -> int:
        """Move files into spaces from right to left to minimize fragmentation.

        Processes files from right to left, moving them into the rightmost
        available spaces that can fit them.

        Args:
            data (List[str]): Input containing disk map string

        Returns:
            int: Checksum of final disk state after moves
        """
        blocks = self.parse_blocks(data[0])

        space_idx = [i for i, block in enumerate(blocks) if block.type == Block.TYPE_SPACE]
        space_count = sum(block.length for block in blocks if block.type == Block.TYPE_SPACE)

        current_block = []
        if space_idx:
            current_space_idx = space_idx.pop(0)

        else:
            current_space_idx = None

        while space_count and current_space_idx is not None:
            if len(current_block) == 0:
                while (
                    blocks and blocks[-1].type == Block.TYPE_SPACE and not blocks[-1].filled_files
                ):
                    blocks.pop()
                    if space_idx:
                        space_idx.pop()

                    continue

                if blocks and blocks[-1].type == Block.TYPE_FILE:
                    current_block = [blocks[-1].file_id] * blocks[-1].length
                    blocks.pop()

            if not current_block:
                break

            item = current_block.pop()
            blocks[current_space_idx].filled_files.append(item)
            space_count -= 1

            if len(blocks[current_space_idx].filled_files) == blocks[current_space_idx].length:
                blocks[current_space_idx].type = Block.TYPE_FILE
                blocks[current_space_idx].file_id = None
                if space_idx:
                    current_space_idx = space_idx.pop(0)

                else:
                    current_space_idx = None

        if current_block:
            new_block = Block(type=Block.TYPE_FILE, length=len(current_block))
            new_block.file_id = None
            new_block.filled_files = current_block
            blocks.append(new_block)

        return self.calculate_checksum(blocks)

    def part2(self, data: List[str]) -> int:
        """Move files as far left as possible in available spaces.

        Processes files from right to left, attempting to move each file into
        the leftmost space that can accommodate it.

        Args:
            data (List[str]): Input containing disk map string

        Returns:
            int: Checksum of final disk state after moves
        """
        blocks = self.parse_blocks(data[0])

        # Process from right to left
        for i in range(len(blocks) - 1, -1, -1):
            current = blocks[i]
            if current.type != Block.TYPE_FILE:
                continue

            # Try to find the leftmost space that can fit this file
            for j in range(i):
                space = blocks[j]
                if (
                    space.type == Block.TYPE_SPACE
                    and space.length >= current.length
                    and len(space.filled_files) + current.length <= space.length
                ):
                    # Fill the space with the current file
                    for _ in range(current.length):
                        space.filled_files.append(current.file_id)

                    # Convert current block to empty space
                    current.type = Block.TYPE_SPACE
                    current.file_id = None
                    current.filled_files = []

                    break

        return self.calculate_checksum(blocks)
