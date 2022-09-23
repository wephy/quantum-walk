"""Plot an example pertaining to quantum walks.

This example investigates QuantumPageRank and the classical analog (a random
walk along the graph), comparing their results at different stages.
"""

import networkx as nx
import matplotlib.pyplot as plt
import importer  # noqa # pylint: disable=unused-import
import quantum_walk as qw  # noqa # pylint: disable=import-error


def plot(q_results, c_results, plot_points):
    """Create plot."""
    fig = plt.figure(constrained_layout=True)
    classical_fig, quantum_fig = fig.subfigures(nrows=2, ncols=1)
    classical_fig.suptitle("classical", fontsize=16)
    axs = classical_fig.subplots(nrows=1, ncols=len(plot_points), sharey=True)
    plt.ylim((0, 0.3))
    for i, result in enumerate(c_results):
        axs[i].bar(*zip(*result.items()))
        axs[i].set_title(f"{plot_points[i]} steps")
    quantum_fig.suptitle("quantum", fontsize=16)
    axs = quantum_fig.subplots(nrows=1, ncols=len(plot_points), sharey=True)
    plt.ylim((0, 0.3))
    for i, result in enumerate(q_results):
        axs[i].bar(*zip(*result.items()))
        axs[i].set_title(f"{plot_points[i]} steps")
    plt.show()


def main():
    """Run example.

    We construct a directed graph to perform both classical and quantum PageRank
    implementations on. Then, we take five stages in the algorithms (after 1, 10,
    100, 1000 and 10000 steps) and plot them together.
    """
    plot_points = [1, 10, 100, 1000, 10000]

    graph = nx.DiGraph()
    graph.add_edges_from([
        (0, 1), (0, 2), (0, 3), (0, 5), (1, 0), (1, 2),
        (1, 3), (2, 1), (2, 6), (3, 5), (4, 1), (4, 5),
        (5, 2), (6, 4), (7, 1), (7, 2), (7, 6)
        ])

    classical_pagerank = qw.ClassicalPageRank(graph)
    quantum_pagerank = qw.QuantumPageRank(graph)
    classical_results = []
    quantum_results = []
    for i in range(1, plot_points[-1] + 1):
        classical_pagerank.step()
        quantum_pagerank.step()
        if i in plot_points:
            classical_results.append(classical_pagerank.result())
            quantum_results.append(quantum_pagerank.result())

    plot(quantum_results, classical_results, plot_points)


if __name__ == "__main__":
    main()
