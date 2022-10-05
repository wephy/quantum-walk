"""Plot an example pertaining to quantum walks.

This example tests QuantumPageRank on a large network, and compares the result
against the regular Google PageRank solution.
"""

import networkx as nx
import matplotlib.pyplot as plt

# Import quantum walk code
import importer  # noqa # pylint: disable=unused-import
from quantum_walk import pagerank  # noqa # pylint: disable=import-error


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

    # Show fig
    plt.show()


def main():
    """Run example
    
    We construct a random large directed graph with the Erdős-Rényi model (we specify
    the number of nodes desired, and provide an edge creation probability to be used
    for every possible edge). We then compare the classical and quantum performance.
    """
    # Use the Erdős-Rényi model to generate a random directed graph
    graph = nx.erdos_renyi_graph(100, 0.1, directed=True)

    qpr = pagerank.QuantumPageRank(graph)
    classical_solution = qpr.classical_solution()
    quantum_solution = qpr.quantum_solution()
    plot(classical_solution, quantum_solution)


if __name__ == "__main__":
    main()
