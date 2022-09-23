"""Implement a class for quantum bits.

This package implements classes that allows for operations and calculations
with quantum bits, to further be used in quantum algorithms.

"""

import numpy as np


def hadamard(qubit):
    """Perform the Hadamard gate on a single qubit.

    The hadamard gate rotates the quantum state of the qubit by 90 degrees around
    the y-axis and then 180 degrees around the x-axis when pictured on a Bloch
    sphere.

    The Hadamard gate, when applied to a qubit in either a perfect up or
    down state will then cause the new state to give up or down with equal
    probability---thus somewhat equivalent to a coin flip. More information at:
    [Wikipedia](https://en.wikipedia.org/wiki/Hadamard_transform).

    """
    hadamard_matrix = 2**(-0.5) * np.array([[1, 1], [1, -1]])
    transformed_qubit = list(np.matmul(hadamard_matrix, np.transpose(qubit)))
    return transformed_qubit


def construct_qubits(keys):
    """Create a one-dimension cartesian lattice of qubits.

    Each qubit is represented with 2 complex numbers, as they are not
    restriced to the surface of the Bloch sphere.

    """
    return {i: [complex(), complex()] for i in keys}


class Qubits:
    """A base class for qubits."""

    def __init__(self, states):
        """Initialise attributes."""
        self.states = states
        self.number_of_qubits = len(states.keys())

    def probabilities(self):
        """Calculate probabilities from amplitudes for each qubit."""
        return {key: sum((abs(x) ** 2 for x in self.states[key]))
                for key in self.states.keys()}

    def normalise(self):
        """Normalise amplitudes of qubits as to form a valid probibility distribution."""
        values = list(self.probabilities().values())
        normalising_constant = np.sum(values)**0.5
        for state in self.states.keys():
            self.states[state] = self.states[state] / normalising_constant

    def coin_flip(self):
        """Flip all qubits with the Hadamard gate."""
        for key in self.states.keys():
            self.states[key] = hadamard(self.states[key])


class OneDimensionQubits(Qubits):
    """"""
    def __init__(self, start, stop):
        self.start = start
        self.stop = stop
        self.states = construct_qubits(range(start, stop + 1))
        Qubits.__init__(self, self.states)


class GraphQubits(Qubits):
    """"""
    def __init__(self, graph):
        self.graph = graph
        self.states = construct_qubits(graph.nodes)
        Qubits.__init__(self, self.states)
