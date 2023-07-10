from qiskit.circuit import QuantumCircuit, Parameter, QuantumRegister, Classical


def fixedStructureAnsatz(circ, qubitindices):
    """creates a fixed structure parameterized ansatz on given circuit 'circ',
    on qubits specified by their indices 'qubitindices'. Individual gate rotation angles can be passed as params."""
    # circ: Qiskit circuit object
    # qubits: list of target qubit indices
    
    # no. of layers in ansatz
    nlayers = 3
    nsublayers = 2

    new_circ = QuantumCircuit(*circ.qregs)

    # Base layer: apply Ry on all qubits
    for q in qubitindices:
        new_circ.ry(Parameter(f'L0_{q}'), q)

    ctrlq = []
    trgtq = []
    ctrlq.append(qubitindices[:-1:2])
    ctrlq.append(qubitindices[1:-1:2])
    trgtq.append(qubitindices[1::2])
    trgtq.append(qubitindices[2::2])

    for l in range(1, nlayers + 1):
        for s in range(nsublayers):
            for i in range(len(ctrlq[s])):
                new_circ.cz(ctrlq[s][i], trgtq[s][i])
            for q in list(set(ctrlq[s] + trgtq[s])):
                new_circ.ry(Parameter(f'L{l}S{s}_{q}'), q)

    return new_circ
