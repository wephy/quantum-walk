"""Plot an example pertaining to quantum walks.

This example investigates QuantumPageRank and the classical analog (a random
walk along the graph), comparing their results at different stages.
"""

import networkx as nx
import matplotlib.pyplot as plt
import scienceplots

plt.style.use("science")

# Import quantum walk code
import importer  # noqa # pylint: disable=unused-import
from quantum_walk import pagerank  # noqa # pylint: disable=import-error


def plot(q_results, c_results, plot_points):
    """Create plot."""
    fig = plt.figure(constrained_layout=True, figsize=(8, 4))
    classical_fig, quantum_fig = fig.subfigures(nrows=2, ncols=1)

    classical_fig.suptitle("classical", fontsize=16)
    axs = classical_fig.subplots(nrows=1, ncols=len(plot_points), sharey=True)
    plt.ylim((0, 0.3))
    for i, result in enumerate(c_results):
        axs[i].bar(*zip(*result.items()))
        axs[i].set_title(f"{plot_points[i]} steps")
        axs[i].get_xaxis().set_ticks([])
        axs[i].get_yaxis().set_ticks([])

    quantum_fig.suptitle("quantum", fontsize=16)
    axs = quantum_fig.subplots(nrows=1, ncols=len(plot_points), sharey=True)
    plt.ylim((0, 0.3))
    for i, result in enumerate(q_results):
        axs[i].bar(*zip(*result.items()))
        axs[i].set_title(f"{plot_points[i]} steps")
        axs[i].get_xaxis().set_ticks([])
        axs[i].get_yaxis().set_ticks([])

    # Show fig
    plt.savefig("example_quantum_vs_classical.png", dpi=600)
    plt.show()


def main():
    """Run example.

    We construct a directed graph to perform both classical and quantum PageRank
    implementations on. Then, we take five stages in the algorithms (after 1, 10,
    100, 1000 and 10000 steps) and plot them together.
    """
    plot_points = [1, 10, 100, 1000, 10000]

    # Construct graph
    graph = nx.DiGraph()
    graph.add_edges_from(
        [
            (0, 1),
            (0, 2),
            (0, 3),
            (0, 5),
            (1, 0),
            (1, 2),
            (1, 3),
            (2, 1),
            (2, 6),
            (3, 5),
            (4, 1),
            (4, 5),
            (5, 2),
            (6, 4),
            (7, 1),
            (7, 2),
            (7, 6),
        ]
    )

    # Create PageRank objects
    classical_pagerank = pagerank.ClassicalPageRank(graph)
    quantum_pagerank = pagerank.QuantumPageRank(graph)

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
