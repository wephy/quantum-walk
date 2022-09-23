"""Plot an example pertaining to quantum walks.

This example looks at the spread over time of the quantum random walk,
implemented using a discrete-time quantum walk on a lattice of qubits.
"""

import matplotlib.pyplot as plt

# import quantum walk code
import importer  # noqa # pylint: disable=unused-import
import quantum_walk as qw  # noqa # pylint: disable=import-error


def main():
    """Run example."""
    number_of_flips = 100
    qubits = qw.OneDimensionQubits(-number_of_flips, number_of_flips)
    qubits.states[0] = [1, 1j]
    for i in range(1, number_of_flips + 1):
        qw.one_dimnesion(qubits, decoherence=False)
        if i % 10 == 0:
            ys = list(qubits.probabilities().values())[::2]
            plt.plot(range(-number_of_flips, (number_of_flips + 1), 2),
                     ys, color='k', alpha=(i / number_of_flips))
    plt.show()


if __name__ == "__main__":
    main()
