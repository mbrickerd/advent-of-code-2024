from itertools import combinations
from typing import List

import networkx as nx

from aoc.models.base import SolutionBase


class Solution(SolutionBase):
    """Solution for Advent of Code 2024 - Day 23: LAN Party.

    This class solves a puzzle about analyzing LAN party connections and finding
    gaming groups. Part 1 identifies valid gaming trios including teachers, while
    Part 2 finds the largest possible gaming group.

    Input format:
        - List of connections, one per line
        - Each line contains two node IDs separated by a hyphen
        - Node IDs starting with 't' represent teachers
        - All other nodes represent students
        - Connections indicate which players can directly play together

    This class inherits from `SolutionBase` and uses NetworkX to analyze the
    connection graph and find valid gaming groups of different sizes.
    """

    def construct_graph(self, data: List[str]) -> nx.Graph:
        """Construct a NetworkX graph from the input connection data.

        Creates an undirected graph where nodes represent players and edges
        represent possible direct connections for gaming.

        Args:
            data: List of strings, each containing two node IDs separated by a hyphen

        Returns:
            NetworkX Graph object representing the connection network
        """
        G = nx.Graph()
        for line in data:
            parts = line.split("-")
            G.add_edge(parts[0], parts[1])

        return G

    def part1(self, data: List[str]) -> int:
        """Count valid gaming trios that include at least one teacher.

        Analyzes the connection graph to find all possible groups of three
        players that:
        1. Are fully connected (form a clique)
        2. Include at least one teacher (node starting with 't')
        3. Can play together based on direct connections

        Args:
            data: List of strings representing player connections

        Returns:
            Number of unique valid gaming trios
        """
        G = self.construct_graph(data)
        cliques = [
            clique
            for clique in nx.find_cliques(G)
            if len(clique) >= 3 and any(node[0] == "t" for node in clique)
        ]
        sets = set()

        for clique in cliques:
            for nodes in combinations(clique, 3):
                if any(node[0] == "t" for node in nodes):
                    sets.add(tuple(sorted(nodes)))

        return len(sets)

    def part2(self, data: List[str]) -> int:
        """Find the largest possible gaming group.

        Identifies the maximum clique in the connection graph, representing
        the largest group of players that can all play together directly.
        Returns the players in alphabetical order as a comma-separated string.

        Args:
            data: List of strings representing player connections

        Returns:
            Comma-separated string of player IDs in the largest gaming group,
            sorted alphabetically
        """
        G = self.construct_graph(data)
        cliques = nx.find_cliques(G)
        LAN = sorted(sorted(cliques, key=len, reverse=True)[0])

        return ",".join(LAN)
