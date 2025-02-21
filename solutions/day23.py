"""Day 23: LAN Party.

Analyze player connections and find gaming groups in a network.

This module solves a puzzle about identifying gaming configurations
based on network connections and group composition rules.
"""

from itertools import combinations

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
    """

    def construct_graph(self, data: list[str]) -> nx.Graph:
        """Construct a NetworkX graph from the input connection data.

        Creates an undirected graph where nodes represent players and edges
        represent possible direct connections for gaming.

        Args:
            data: List of strings, each containing two node IDs separated by a hyphen

        Returns
        -------
            NetworkX Graph object representing the connection network
        """
        graph: nx.Graph = nx.Graph()
        edges = []
        for line in data:
            source, target = line.split("-")
            edges.append((source, target))
        graph.add_edges_from(edges)
        return graph

    def part1(self, data: list[str]) -> int:
        """Count valid gaming trios that include at least one teacher.

        Analyzes the connection graph to find all possible groups of three
        players that:
        1. Are fully connected (form a clique)
        2. Include at least one teacher (node starting with 't')
        3. Can play together based on direct connections

        Args:
            data: List of strings representing player connections

        Returns
        -------
            Number of unique valid gaming trios
        """
        graph = self.construct_graph(data)
        teacher_cliques = [
            clique
            for clique in nx.find_cliques(graph)
            if len(clique) >= 3 and any(node.startswith("t") for node in clique)
        ]

        return len(
            {
                tuple(sorted(nodes))
                for clique in teacher_cliques
                for nodes in combinations(clique, 3)
                if any(node.startswith("t") for node in nodes)
            }
        )

    def part2(self, data: list[str]) -> str:
        """Find the largest possible gaming group.

        Identifies the maximum clique in the connection graph, representing
        the largest group of players that can all play together directly.
        Returns the players in alphabetical order as a comma-separated string.

        Args:
            data: List of strings representing player connections

        Returns
        -------
            Comma-separated string of player IDs in the largest gaming group,
            sorted alphabetically
        """
        graph = self.construct_graph(data)
        largest_clique = max(nx.find_cliques(graph), key=len)
        return ",".join(sorted(largest_clique))
