import re

from aoc.models.base import SolutionBase


class Solution(SolutionBase):
    def part1(self, data):
        pattern = r"mul\((\d{1,3}),(\d{1,3})\)"
        matches = re.findall(pattern, "".join(data))

        return sum(int(x) * int(y) for x, y in matches)

    def part2(self, data):
        pattern = r"(mul\((\d{1,3}),(\d{1,3})\)|do\(\)|don't\(\))"
        instructions = re.findall(pattern, "".join(data))

        enabled = True
        result = 0

        for step in instructions:
            match step[0]:
                case "do()":
                    enabled = True

                case "don't()":
                    enabled = False

                case _ if enabled:
                    result += int(step[1]) * int(step[2])

        return result
