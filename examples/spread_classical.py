"""Plot an example pertaining to quantum walks.

This example looks at the spread over time of the clasical random walk,
implemented using a discrete-time quantum walk on a lattice of qubits,
with decoherence.
"""

import matplotlib.pyplot as plt

# Import quantum walk code
import importer  # noqa # pylint: disable=unused-import
from quantum_walk import quantum_bits as qb  # noqa # pylint: disable=import-error
from quantum_walk import discrete_time_quantum_walk as dtqw  # noqa # pylint: disable=import-error


def main():
    """Run example."""
    # Variable dertermining number of timesteps
    time_steps = 100

    # Construct collection of qubits in one-dimension cartesian lattice
    qubits = qb.OneDimensionQubits(-time_steps, time_steps)

    # Set state of middle qubit to that of equal up and down
    qubits.states[0] = [1, 1j]

    # Perform quantum walk
    for i in range(1, time_steps + 1):

        # Take a step with dtqw
        # We set decoherence to True for classical phenomenon
        dtqw.one_dimension(qubits, decoherence=True)

        # Plot every 10 steps
        if i % 10 == 0:
            ys = list(qubits.probabilities().values())[::2]
            plt.plot(range(-time_steps, (time_steps + 1), 2),
                     ys, color='k', alpha=(i / time_steps))

    # Show fig
    plt.show()


if __name__ == "__main__":
    main()
