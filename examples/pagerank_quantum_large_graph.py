"""Plot an example pertaining to quantum walks.

This example tests QuantumPageRank on a large network, and compares the result
against the regular Google PageRank solution.
"""

import networkx as nx
import matplotlib.pyplot as plt

# import quantum walk code
import importer  # noqa # pylint: disable=unused-import
import quantum_walk as qw  # noqa # pylint: disable=import-error


def plot(classical_solution, quantum_solution):
    """Create plot."""
    fig = plt.figure(constrained_layout=True)
    solution_fig, quantum_fig = fig.subfigures(nrows=2, ncols=1)
    solution_fig.suptitle("classical solution", fontsize=16)
    ax = solution_fig.subplots(1, 1)
    ax.bar(*zip(*classical_solution.items()))
    quantum_fig.suptitle("quantum solution", fontsize=16)
    ax = quantum_fig.subplots(1, 1)
    ax.bar(*zip(*quantum_solution.items()))
    plt.show()


def main():
    """Run example."""
    graph = nx.erdos_renyi_graph(100, 0.1, directed=True)
    quantum_pagerank = qw.QuantumPageRank(graph)
    classical_solution = quantum_pagerank.classical_solution()
    quantum_solution = quantum_pagerank.quantum_solution()
    plot(classical_solution, quantum_solution)


if __name__ == "__main__":
    main()
