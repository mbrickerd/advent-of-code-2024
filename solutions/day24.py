"""Day 24: Crossed Wires.

Analyze digital circuits and identify wire connections.

This module solves a puzzle about examining circuit structures and connections,
finding the output of wires, and identifying which wires need to be swapped.
"""

from collections.abc import Callable
from dataclasses import dataclass, field
import re

from aoc.models.base import SolutionBase


@dataclass
class Connection:
    """Represents a logic gate connection in the circuit.

    Args:
        input1: First input wire identifier
        gate: Gate operation type (AND, OR, XOR)
        input2: Second input wire identifier
        output: Output wire identifier

    Returns
    -------
        Connection instance representing a single logic gate connection
    """

    input1: str
    gate: str
    input2: str
    output: str

    def __str__(self) -> str:
        """Generate string representation of the connection.

        Returns
        -------
            String in format 'input1 gate input2 -> output'
        """
        return f"{self.input1} {self.gate} {self.input2} -> {self.output}"


@dataclass
class Circuit:
    """Represents a digital circuit with wires and logic gate connections.

    Args:
        wires: Dictionary mapping wire identifiers to their values
        connections: List of Connection objects representing logic gates
        operators: Dictionary mapping gate types to their logic functions

    Returns
    -------
        Circuit instance representing the complete digital circuit
    """

    wires: dict[str, int]
    connections: list[Connection] = field(default_factory=list)
    operators: dict[str, Callable[[int, int], int]] = field(
        default_factory=lambda: {
            "OR": lambda x, y: x | y,
            "AND": lambda x, y: x & y,
            "XOR": lambda x, y: x ^ y,
        }
    )

    def calc(self, wire: str) -> int:
        """Calculate the value of a wire based on its inputs and gate operation.

        Args:
            wire: Identifier of the wire to calculate

        Returns
        -------
            Computed value for the wire

        Raises
        ------
            ValueError: If no connection is found for the wire
        """
        if self.wires[wire] != -1:
            return self.wires[wire]

        for conn in self.connections:
            if conn.output == wire:
                x = self.calc(conn.input1)
                y = self.calc(conn.input2)
                self.wires[wire] = self.operators[conn.gate](x, y)
                return self.wires[wire]

        error_message = f"No connection found for wire {wire}"
        raise ValueError(error_message)

    def execute(self) -> list[int]:
        """Execute the circuit and return the z-wire values.

        Returns
        -------
            List of z-wire values in reverse order
        """
        z_values = []
        i = 0

        while True:
            key = f"z{i:02}"
            if key not in self.wires or all(conn.output != key for conn in self.connections):
                break

            z_values.append(self.calc(key))
            i += 1

        return z_values[::-1]  # Reverse for correct order


class CircuitValidator:
    """Helper class for verifying circuit connections in part 2."""

    def __init__(self, formulas: dict[str, tuple[str, str, str]]):
        self.formulas = formulas

    def make_wire(self, char: str, num: int) -> str:
        """Create a wire ID with the given character and number.

        Args:
            char: Character prefix for the wire ('x', 'y', or 'z')
            num: Wire number to append

        Returns
        -------
            Wire identifier in format 'char##'
        """
        return f"{char}{num:02}"

    def validate_z(self, wire: str, num: int) -> bool:
        """Validate a z-wire in the circuit.

        Args:
            wire: Wire identifier to validate
            num: Expected bit position for the wire

        Returns
        -------
            True if wire is correctly connected, False otherwise
        """
        if wire not in self.formulas:
            return False

        op, x, y = self.formulas[wire]
        if op != "XOR":
            return False

        if num == 0:
            return sorted([x, y]) == ["x00", "y00"]

        return (
            self.validate_intermediate_xor(x, num)
            and self.validate_carry_bit(y, num)
            or self.validate_intermediate_xor(y, num)
            and self.validate_carry_bit(x, num)
        )

    def validate_intermediate_xor(self, wire: str, num: int) -> bool:
        """Validate an intermediate XOR gate in the circuit.

        Args:
            wire: Wire identifier to validate
            num: Expected bit position for the wire

        Returns
        -------
            True if gate is correctly configured, False otherwise
        """
        if wire not in self.formulas:
            return False

        op, x, y = self.formulas[wire]
        if op != "XOR":
            return False

        return sorted([x, y]) == [self.make_wire("x", num), self.make_wire("y", num)]

    def validate_carry_bit(self, wire: str, num: int) -> bool:
        """Validate a carry bit in the circuit.

        Args:
            wire: Wire identifier to validate
            num: Expected bit position for the wire

        Returns
        -------
            True if carry bit is correctly configured, False otherwise
        """
        if wire not in self.formulas:
            return False

        op, x, y = self.formulas[wire]
        if num == 1:
            if op != "AND":
                return False

            return sorted([x, y]) == ["x00", "y00"]

        if op != "OR":
            return False

        return (
            self.validate_direct_carry(x, num - 1)
            and self.validate_recarry(y, num - 1)
            or self.validate_direct_carry(y, num - 1)
            and self.validate_recarry(x, num - 1)
        )

    def validate_direct_carry(self, wire: str, num: int) -> bool:
        """Validate a direct carry gate in the circuit.

        Args:
            wire: Wire identifier to validate
            num: Expected bit position for the wire

        Returns
        -------
            True if direct carry is correctly configured, False otherwise
        """
        if wire not in self.formulas:
            return False

        op, x, y = self.formulas[wire]
        if op != "AND":
            return False

        return sorted([x, y]) == [self.make_wire("x", num), self.make_wire("y", num)]

    def validate_recarry(self, wire: str, num: int) -> bool:
        """Validate a recarry gate in the circuit.

        Args:
            wire: Wire identifier to validate
            num: Expected bit position for the wire

        Returns
        -------
            True if recarry is correctly configured, False otherwise
        """
        if wire not in self.formulas:
            return False

        op, x, y = self.formulas[wire]
        if op != "AND":
            return False

        return (
            self.validate_intermediate_xor(x, num)
            and self.validate_carry_bit(y, num)
            or self.validate_intermediate_xor(y, num)
            and self.validate_carry_bit(x, num)
        )

    def validate(self, num: int) -> bool:
        """Validate the circuit at a specific bit position.

        Args:
            num: Bit position to validate

        Returns
        -------
            True if bit position is correctly configured, False otherwise
        """
        return self.validate_z(self.make_wire("z", num), num)

    def progress(self) -> int:
        """Determine how many bits are correctly validated in sequence.

        Returns
        -------
            Number of consecutive valid bit positions from zero
        """
        i = 0
        while self.validate(i):
            i += 1

        return i


class Solution(SolutionBase):
    """Solution for Advent of Code 2024 - Day 24: Crossed Wires.

    This class solves a puzzle about analyzing digital circuits and identifying wire connections.
    Part 1 executes a digital circuit to determine the output value, while Part 2 analyzes the
    circuit structure to identify wires that need to be swapped to fix an incorrectly wired adder.

    Input format:
        - Initial wire values section: lines with format "wireId: value" (0 or 1)
        - Blank line separator
        - Gate connections section: lines with format "input1 OPERATION input2 -> output"
        - Operations include AND, OR, and XOR
        - Wire IDs starting with 'x' and 'y' are inputs, those starting with 'z' are outputs
    """

    def parse_data(self, data: list[str]) -> Circuit:
        """Parse input data into a Circuit object.

        Args:
            data: List of strings containing initial wire values and gate connections

        Returns
        -------
            Circuit object with initialized wires and connections
        """
        separator_idx = data.index("")
        wires = {}

        for line in data[:separator_idx]:
            wire, val = line.split(": ")
            wires[wire] = int(val)

        connections = []
        for line in data[separator_idx + 1 :]:
            match = re.match(r"(\w+) (OR|AND|XOR) (\w+) -> (\w+)", line)
            if match:
                input1, gate, input2, output = match.groups()

                for wire in [input1, input2, output]:
                    if wire not in wires:
                        wires[wire] = -1

                connections.append(Connection(input1, gate, input2, output))

        return Circuit(wires, connections)

    def part1(self, data: list[str]) -> int:
        """Simulate the digital circuit to calculate the final output value.

        Parses the input to extract initial wire values and gate connections,
        then simulates the execution of the circuit by processing gates in order
        until all wire values are computed. Returns the binary value represented
        by the z-wires.

        Args:
            data: List of strings containing initial wire values and gate connections

        Returns
        -------
            Integer value represented by the binary output of z-wires
        """
        circuit = self.parse_data(data)
        z_values = circuit.execute()
        return int("".join(map(str, z_values)), 2)

    def part2(self, data: list[str]) -> str:
        """Identify misconnected wires in the full adder circuit.

        Analyzes the circuit structure to find z-wires that need to be swapped
        to correctly implement a full adder.

        Args:
            data: List of strings containing gate connections

        Returns
        -------
            Comma-separated string of z-wire IDs that need to be swapped,
            sorted alphabetically
        """
        formulas = {}
        separator_idx = data.index("")

        for line in data[separator_idx + 1 :]:
            match = re.match(r"(\w+) (OR|AND|XOR) (\w+) -> (\w+)", line)
            if match:
                input1, gate, input2, output = match.groups()
                formulas[output] = (gate, input1, input2)

        validator = CircuitValidator(formulas)
        swaps = []

        for _ in range(4):
            baseline = validator.progress()
            for x in formulas:
                for y in formulas:
                    if x == y:
                        continue
                    formulas[x], formulas[y] = formulas[y], formulas[x]
                    if validator.progress() > baseline:
                        break
                    formulas[x], formulas[y] = formulas[y], formulas[x]
                else:
                    continue
                break
            swaps += [x, y]

        return ",".join(sorted(swaps))
