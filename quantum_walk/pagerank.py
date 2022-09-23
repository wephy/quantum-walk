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
    def __init__(self, graph):
        self.graph = graph
        self.steps = 0
        self.number_of_vertices = graph.number_of_nodes()
        self.vertices = range(self.number_of_vertices)

    def classical_solution(self):
        return nx.pagerank(self.graph)


class QuantumPageRank(PageRank):
    def __init__(self, graph):
        PageRank.__init__(self, graph)
        self.graph = graph
        self.qubits = qb.GraphQubits(graph)
        for qubit in self.graph:
            self.qubits.states[qubit] = [1, 1j]

    def step(self):
        dtqw.directed_graph(self.qubits)
        self.steps += 1

    def result(self):
        return self.qubits.probabilities()

    def quantum_solution(self):
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
    def __init__(self, graph, alpha=0.85):
        PageRank.__init__(self, graph)
        self.graph = graph
        self.alpha = alpha
        self.counts = {vertex: 0 for vertex in self.graph}
        self.successors = {vertex: list(self.graph.successors(vertex))
                           for vertex in self.graph}
        self.current_vertex = np.random.choice(self.vertices)

    def step(self):
        successors = self.successors[self.current_vertex]
        if len(successors) == 0 or np.random.random() > self.alpha:
            self.current_vertex = np.random.choice(self.vertices)
        else:
            self.current_vertex = np.random.choice(successors)
        self.counts[self.current_vertex] += 1
        self.steps += 1

    def result(self):
        normalised_values = self.counts.copy()
        for key in normalised_values.keys():
            normalised_values[key] = normalised_values[key] / self.steps
        return normalised_values
