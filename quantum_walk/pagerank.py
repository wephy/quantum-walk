"""Implement both quantum and classical PageRank algorithms.

This package implements two implementation of the PageRank algorithm, developed by
Google. One involves a classical random walker on the graph, and the other
involves a quantum walker on the graph.
"""

import numpy as np
import networkx as nx
from . import quantum_bits as qb
from . import discrete_time_quantum_walk as dtqw


class PageRank:
    """Base class for PageRank."""
    
    def __init__(self, graph):
        """Initialise attributes."""
        self.graph = graph
        self.steps = 0
        self.number_of_vertices = graph.number_of_nodes()
        self.vertices = range(self.number_of_vertices)

    def classical_solution(self):
        """Return the Google solution to PageRank using power method."""
        return nx.pagerank(self.graph)


class QuantumPageRank(PageRank):
    """An algorithm for QuantumPageRank."""
    
    def __init__(self, graph):
        """Initialise attributes."""
        self.graph = graph
        self.qubits = qb.GraphQubits(graph)
        for qubit in self.graph:
            self.qubits.states[qubit] = [1, 1j]
        PageRank.__init__(self, graph)

    def step(self):
        """Take a step on the graph."""
        dtqw.directed_graph(self.qubits)
        self.steps += 1

    def result(self):
        """Returns the result of PageRank with values corresponding to importance."""
        return self.qubits.probabilities()

    def quantum_solution(self):
        """Return the (steady-state) solutionto QuantumPageRank."""
        qpr = QuantumPageRank(self.graph)
        previous_values = [0 for _ in range(self.number_of_vertices)]
        current_values = list(qpr.result().values())
        while not np.allclose(previous_values, current_values):
            previous_values = current_values
            qpr.step()
            current_values = list(qpr.result().values())
        print(f"quantum solution took {qpr.steps} steps to complete")
        return qpr.result()


class ClassicalPageRank(PageRank):
    """An algorithm for standard PageRank using Monte Carlo method."""
    
    def __init__(self, graph, alpha=0.85):
        """Initialise attributes."""
        self.graph = graph
        self.alpha = alpha
        self.counts = {vertex: 0 for vertex in self.graph}
        self.successors = {vertex: list(self.graph.successors(vertex))
                           for vertex in self.graph}
        self.current_vertex = np.random.choice(self.vertices)
        PageRank.__init__(self, graph)

    def step(self):
        """Take a step on the graph."""
        successors = self.successors[self.current_vertex]
        if len(successors) == 0 or np.random.random() > self.alpha:
            self.current_vertex = np.random.choice(self.vertices)
        else:
            self.current_vertex = np.random.choice(successors)
        self.counts[self.current_vertex] += 1
        self.steps += 1

    def result(self):
        """Returns the result of PageRank with values corresponding to importance."""
        normalised_values = self.counts.copy()
        for key in normalised_values.keys():
            normalised_values[key] = normalised_values[key] / self.steps
        return normalised_values
