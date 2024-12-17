import re
from typing import List, Tuple

from aoc.models.base import SolutionBase


class ThreeBitComputer:
    """Simulates a 3-bit computer with three registers and eight instructions.

    This class implements a virtual machine that executes programs consisting of 3-bit
    instructions (0-7). The computer has three registers (A, B, C) and supports both
    literal and combo operands. Instructions include arithmetic operations, bitwise
    operations, jumps, and output generation.

    Attributes:
        registers (dict): Dictionary storing values for registers A, B, and C
        instruction_pointer (int): Current position in the program
        output (list): List storing output values generated during program execution
    """

    def __init__(self, a: int = 0, b: int = 0, c: int = 0):
        """Initialize the computer with specified register values.

        Args:
            a (int, optional): Initial value for register A. Defaults to 0.
            b (int, optional): Initial value for register B. Defaults to 0.
            c (int, optional): Initial value for register C. Defaults to 0.
        """
        self.registers = {"A": a, "B": b, "C": c}
        self.instruction_pointer = 0
        self.output = []

    def get_combo_value(self, operand: int) -> int:
        """Resolve the value of a combo operand based on its code.

        Args:
            operand (int): The combo operand code (0-6)
                0-3: Return literal value
                4: Return value in register A
                5: Return value in register B
                6: Return value in register C

        Returns:
            int: The resolved value of the combo operand

        Raises:
            ValueError: If the operand is invalid (7 or out of range)
        """
        if 0 <= operand <= 3:
            return operand
        
        elif operand == 4:
            return self.registers["A"]
        
        elif operand == 5:
            return self.registers["B"]
        
        elif operand == 6:
            return self.registers["C"]
        
        else:
            raise ValueError(f"Invalid combo operand: {operand}")

    def execute_instruction(self, program: List[int]) -> bool:
        """Execute the next instruction in the program.

        Executes the instruction at the current instruction_pointer position.
        Supported instructions:
            0 (adv): Divide A by 2^(combo operand), store in A
            1 (bxl): XOR B with literal operand
            2 (bst): Store combo operand mod 8 in B
            3 (jnz): Jump to operand if A is non-zero
            4 (bxc): XOR B with C
            5 (out): Output combo operand mod 8
            6 (bdv): Divide A by 2^(combo operand), store in B
            7 (cdv): Divide A by 2^(combo operand), store in C

        Args:
            program (List[int]): List of integers representing the program instructions

        Returns:
            bool: False if program should halt, True if execution should continue
        """
        if self.instruction_pointer >= len(program):
            return False

        opcode = program[self.instruction_pointer]
        operand = program[self.instruction_pointer + 1]

        if opcode == 0:  # adv
            self.registers["A"] //= 1 << self.get_combo_value(operand)

        elif opcode == 1:  # bxl
            self.registers["B"] ^= operand

        elif opcode == 2:  # bst
            self.registers["B"] = self.get_combo_value(operand) % 8

        elif opcode == 3:  # jnz
            if self.registers["A"] != 0:
                self.instruction_pointer = operand
                return True
            
        elif opcode == 4:  # bxc
            self.registers["B"] ^= self.registers["C"]

        elif opcode == 5:  # out
            self.output.append(self.get_combo_value(operand) % 8)

        elif opcode == 6:  # bdv
            self.registers["B"] = self.registers["A"] // (1 << self.get_combo_value(operand))

        elif opcode == 7:  # cdv
            self.registers["C"] = self.registers["A"] // (1 << self.get_combo_value(operand))

        self.instruction_pointer += 2
        return True

    def run(self, program: List[int]) -> List[int]:
        """Run the entire program until completion.

        Args:
            program (List[int]): List of integers representing the program instructions

        Returns:
            List[int]: List of output values generated during execution
        """
        self.output = []  # Reset output before running
        while self.execute_instruction(program):
            pass

        return self.output

    def check_output(self, program: List[int], partial: bool = False) -> bool:
        """Check if the program's output matches its own instructions.

        Args:
            program (List[int]): List of integers representing the program instructions
            partial (bool, optional): If True, allow checking partial output matches.
                Defaults to False.

        Returns:
            bool: True if program output exactly matches the input program
                (or matches partially if partial=True), False otherwise
        """
        output = self.run(program)
        if len(output) > len(program):
            return False
        
        if partial:
            return output == program[: len(output)]
        
        return output == program


class Solution(SolutionBase):
    """Solution for Advent of Code 2024 - Day 17: Chronospatial Computer.

    This class solves a puzzle involving a 3-bit computer simulation. The computer
    has three registers and eight instructions, processing programs of 3-bit numbers.
    Part 1 executes the program with given register values to produce output, while
    Part 2 finds the lowest value for register A that makes the program output itself.

    Input format:
        - Multiple lines where:
            First three lines contain initial register values (A, B, C)
            One line contains the program as comma-separated 3-bit numbers

    This class inherits from `SolutionBase` and provides methods to parse input,
    execute programs, and analyze program behavior.
    """

    def parse_data(self, data: List[str]) -> Tuple[int, int, int, List[int]]:
        """Parse input data to extract register values and program instructions.

        Args:
            data (List[str]): Input lines containing register values and program

        Returns:
            Tuple containing:
                - int: Initial value for register A
                - int: Initial value for register B
                - int: Initial value for register C
                - List[int]: List of program instructions
        """
        reg_a = int(re.search(r"Register A: (\d+)", data[0]).group(1))
        reg_b = int(re.search(r"Register B: (\d+)", data[1]).group(1))
        reg_c = int(re.search(r"Register C: (\d+)", data[2]).group(1))

        program_line = next(line for line in data if line.startswith("Program:"))
        program = [int(x) for x in program_line.split(": ")[1].split(",")]

        return reg_a, reg_b, reg_c, program

    def part1(self, data: List[str]) -> str:
        """Execute the program with given register values and return its output.

        Args:
            data (List[str]): Input lines containing register values and program

        Returns:
            str: Comma-separated string of values output by the program
        """
        reg_a, reg_b, reg_c, program = self.parse_data(data)
        computer = ThreeBitComputer(reg_a, reg_b, reg_c)
        return ",".join(map(str, computer.run(program)))

    def part2(self, data: List[str]) -> int:
        """Find lowest positive value for register A that makes program output itself.

        Uses mathematical patterns based on powers of 8 to efficiently find the solution.
        Each digit in the output corresponds to a power of 8, allowing us to adjust the
        input value A systematically rather than trying every possibility.

        Args:
            data (List[str]): Input lines containing register values and program

        Returns:
            int: Lowest positive value for register A that causes program to output
                a copy of its own instructions

        Raises:
            ValueError: If the program generates output longer than itself
        """
        _, reg_b, reg_c, program = self.parse_data(data)

        # Calculate initial value based on program length and powers of 8
        a = sum(7 * 8**i for i in range(len(program) - 1)) + 1

        while True:
            computer = ThreeBitComputer(a, reg_b, reg_c)
            output = computer.run(program)

            if len(output) > len(program):
                raise ValueError("Output longer than program")

            if output == program:
                return a

            # Find position of first mismatch and adjust A accordingly
            for i in range(len(output) - 1, -1, -1):
                if output[i] != program[i]:
                    a += 8**i  # Adjust A by power of 8 at mismatch position
                    break
