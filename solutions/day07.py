from typing import List, Tuple

from aoc.models.base import SolutionBase


class Solution(SolutionBase):
    def parse_data(self, data: List[str]) -> Tuple[int, List[int]]:
        equations = []
        for line in data:
            total, values = line.split(":")
            equations.append((int(total), [*map(int, values.strip().split())]))

        return equations

    def part1(self, data: List[str]) -> int:
        equations = self.parse_data(data)
        result = []

        for total, values in equations:
            possibles = [values.pop(0)]
            while values:
                current = values.pop(0)
                tmp = []
                for p in possibles:
                    tmp.append(p + current)
                    tmp.append(p * current)

                possibles = tmp

            if total in possibles:
                result.append(total)

        return sum(result)

    def part2(self, data: List[str]) -> int:
        equations = self.parse_data(data)
        result = []

        for total, values in equations:
            possibles = [values.pop(0)]
            while values:
                current = values.pop(0)
                tmp = []
                for p in possibles:
                    next_values = [  # +, * and ||
                        p + current,
                        p * current,
                        int(str(p) + str(current)),
                    ]
                    tmp.extend([v for v in next_values if v <= total])

                possibles = tmp

            if total in possibles:
                result.append(total)

        return sum(result)
