from local_had_test import local_had_test

def psi_norm(params, ansatz_circ, A, B, c):
    '''
    Inputs:
    type ansatz_circ: qiskit circuit object, ansatz circuit, n registers
    type A: list(string) decomposed A matrix
    type B: np array. normalized.
    type c: list(int) coeff of decomposed A
    type nqubits: number of qubits not including ancilla
    rtype: float , <¥|¥>
    '''
    norm = 0.0
    
    for l in range(len(c)):
        for lp in range(len(c)):
            norm += c[l] * c[lp] * local_had_test(params, ansatz_circ, A, B, l, lp, -1)[0]
    
    return abs(norm)

def cost_loc(params, ansatz_circ, A, B, c, cost_history):
    '''
    Inputs:
    type ansatz_circ: qiskit circuit object, ansatz circuit, n registers
    type A: list(string) decomposed A matrix
    type B: np array. normalized.
    type c: list(float) coeff of decomposed A
    type nqubits: number of qubits not including ancilla
    rtype: float 
    '''
    mu_sum = 0.0

    for l in range(len(c)):
        for lp in range(len(c)):
            for j in range(ansatz_circ.num_qubits):
                mu_sum += c[l] * c[lp] * local_had_test(params, ansatz_circ, A, B, l, lp, j)[0]

    mu_sum = abs(mu_sum)
    
    cost = 0.5 - 0.5 * mu_sum / (ansatz_circ.num_qubits * psi_norm(params, ansatz_circ, A, B, c))
    
    print("Cost_L = {:9.7f}".format(cost))
    cost_history.append(cost)
    
    return cost
