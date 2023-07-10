from qiskit.circuit import QuantumCircuit, Parameter, QuantumRegister, ClassicalRegister
from qiskit import Aer, transpile, assemble, execute
from qiskit.circuit.library import PauliGate

def local_had_test(params, ansatz_circ, A, B, l, lp, j):
    '''
    Inputs:
    type ansatz_circ: qiskit circuit object, ansatz circuit, n registers
    type l: int
    type lp: int
    type j: int
    type A: list(string) decomposed A matrix
    type B: np array. normalized.
    type nqubits: number of qubits not including ancilla
    rtype: (int, qiskit circuit), int -> expexted value of test; circ -> final circuit of H test
    '''
        
    qr = QuantumRegister(ansatz_circ.num_qubits, 'q')
    anc = QuantumRegister(1, 'anc') #add ancilla register
    meas = ClassicalRegister(1,'meas') #add classical register for measuring
    _circ = QuantumCircuit(qr)
    
    _circ.add_register(anc)
    _circ.initialize([1,0], anc)
    
    bound_ansatz = ansatz_circ.assign_parameters(dict(zip(ansatz_circ.parameters, params)))
    ansatz_inst = bound_ansatz.to_instruction(label='V(w)')
    _circ.append(ansatz_inst, qargs=_circ.qubits[0:-1])
    
    
    _circ.barrier()  
   
    #apply hadamard gate on ancilla
    _circ.h(anc) 

    
    #apply A_l to all qubits, control on ancilla
    U=A[l]
    CU=PauliGate(U).control(1)
    _circ.append(CU,qargs=[anc]+_circ.qubits[0:-1])

    
    qr = QuantumRegister(ansatz_circ.num_qubits, 'q')
    Udg_circ = QuantumCircuit(qr)
    Udg_circ.isometry (B, _circ.qubits[0:-1], [])
    Udg_circ = transpile (Udg_circ, basis_gates = ['u3', 'cx'], optimization_level=3)
    sub_inst = Udg_circ.to_instruction(label='U')
    
    _circ.append(sub_inst.inverse(), qargs=_circ.qubits[0:-1])
    
    
    if j != -1:
        _circ.cz(anc, _circ.qubits[j])
    
    
    _circ.append(sub_inst, qargs=_circ.qubits[0:-1])
    
    
    #apply A_lp, control on ancilla
    U=A[lp]
    CU=PauliGate(U).control(1).inverse()
    _circ.append(CU,qargs=[anc]+_circ.qubits[0:-1])
    
  
    #apply H to ancilla
    _circ.barrier()
    _circ.h(anc)
    
    '''
             ---                                                  ---
    |0>_anc -|H|-------------•---------------•--------------•-----|H|-
             ---             |               |              |     ---
                  ------   ------   -----    |    ----   ------
    |0>_0   ------|    |---|    |---|   |---------|  |---|    |-------
    .             |    |   |    |   |   |    |    |  |   |    |
    .             |V(w)|   |A_l |   |U^†|--|Z_j|--|U |   |A_lp|
    .             |    |   |    |   |   |  -----  |  |   |    |
    |0>_n-1 ------|    |---|    |---|   |---------|  |---|    |-------
                  ------   ------   -----         ----   ------
    '''  
    
   
    _circ.add_register(meas)
    _circ.measure(anc,meas)
    
    nshots=100000
    simulator=Aer.get_backend("qasm_simulator")
    job = execute(_circ, backend=simulator, shots = nshots)
    result = job.result()
    zerocounts = result.get_counts().get('0',1)
    onecounts = result.get_counts().get('1',1)
    P0=zerocounts/nshots
    P1=onecounts/nshots
    val=P0-P1
    
    return val, _circ
