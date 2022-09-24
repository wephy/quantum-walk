"""Implement the discrete-time quantum walk.

This package implements the DTQW for both the standard, one-dimensional lattice
case, and also for a directed graph.
"""
from . import quantum_bits as qb


def one_dimension(qubits, decoherence=False):
    """Performs a discrete time step in the discrete-time quantum walk"""
    # Perform coin flips
    qubits.coin_flip()

    # Shift operator
    tmp_qubits = qb.OneDimensionQubits(qubits.start, qubits.stop)
    for i in range(qubits.start + 1, qubits.stop):
        tmp_qubits.states[i + 1][0] += qubits.states[i][0 if not decoherence
                                                     else 1]
        tmp_qubits.states[i - 1][1] += qubits.states[i][1]
    tmp_qubits.normalise()

    # Copy over new states
    for key in qubits.states.keys():
        qubits.states[key] = tmp_qubits.states[key]


def directed_graph(qubits):
    """Performs a discrete time step in the discrete-time quantum walk"""
    # Perform coin flips
    qubits.coin_flip()

    # Shift operator
    tmp_qubits = qb.GraphQubits(qubits.graph)
    for vertex in qubits.graph:
        tmp_qubits.states[vertex][0] += qubits.states[vertex][0]
        number_of_successors = len(list(qubits.graph.successors(vertex)))

        for successor in qubits.graph.successors(vertex):
            tmp_qubits.states[successor][1] += 0.5 * (
                qubits.states[vertex][1] / number_of_successors)

        for key in qubits.states.keys():
            tmp_qubits.states[key][1] += 0.5 * (
                qubits.states[vertex][1] / qubits.number_of_qubits)
    tmp_qubits.normalise()

    # Copy over new states
    for key in qubits.states.keys():
        qubits.states[key] = tmp_qubits.states[key]
