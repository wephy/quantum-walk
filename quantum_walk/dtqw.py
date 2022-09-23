"""Implement the discrete-time quantum walk.

This package implements the DTQW for both the standard, one-dimensional lattice
case, and also for a directed graph.
"""
from . import quantum_bits as qb


def one_dimnesion(qubits, decoherence=False):
    """Performs a discrete time step in the discrete-time quantum walk"""
    # perform coin flips
    qubits.coin_flip()

    # shift operator
    _qubits = qb.OneDimensionQubits(qubits.start, qubits.stop)
    for i in range(qubits.start + 1, qubits.stop):
        _qubits.states[i + 1][0] += qubits.states[i][0 if not decoherence
                                                     else 1]
        _qubits.states[i - 1][1] += qubits.states[i][1]
    _qubits.normalise()

    # copy over new states
    for key in qubits.states.keys():
        qubits.states[key] = _qubits.states[key]


def directed_graph(qubits):
    """Performs a discrete time step in the discrete-time quantum walk"""
    # perform coin flips
    qubits.coin_flip()

    # shift operator
    _qubits = qb.GraphQubits(qubits.graph)
    for vertex in qubits.graph:
        _qubits.states[vertex][0] += qubits.states[vertex][0]
        number_of_successors = len(list(qubits.graph.successors(vertex)))

        for successor in qubits.graph.successors(vertex):
            _qubits.states[successor][1] += 0.5 * (
                qubits.states[vertex][1] / number_of_successors)

        for key in qubits.states.keys():
            _qubits.states[key][1] += 0.5 * (
                qubits.states[vertex][1] / qubits.number_of_qubits)
    _qubits.normalise()

    # copy over new states
    for key in qubits.states.keys():
        qubits.states[key] = _qubits.states[key]
