from fs_ansatz import fixedStructureAnsatz
from local_had_test import local_had_test
from local_cost import psi_norm, cost_loc

from qiskit.circuit import QuantumCircuit, Parameter, QuantumRegister, ClassicalRegister
from qiskit.circuit.library import RealAmplitudes
from qiskit.quantum_info.operators import Operator
from qiskit.algorithms.optimizers import COBYLA
from scipy.optimize import minimize
import matplotlib.pyplot as plt
import numpy as np
import random


def main():
    # ## Test case #1

    #using fixedStructureAnsatz
    nqubits=3
    qr = QuantumRegister(nqubits, 'q')

    ansatz_circ = QuantumCircuit(qr)
    ansatz_circ = fixedStructureAnsatz(ansatz_circ,[i for i in range(nqubits)])

    x0=[float(random.randint(0,3000))/1000 for i in range(len(ansatz_circ.parameters))]
    print("initial ansatz for fsa:\n", x0)

    B = np.ones(2**nqubits)
    B /= np.linalg.norm(B)

    A = ['ZIX']

    c = [1]

    cost_history = []
    out = minimize(cost_loc, x0, method="COBYLA", options={'maxiter':200})
    print(out)
    print('end of results')

    x = np.arange(0,len(cost_history),1)
    plt.scatter(x,cost_history, color="g")
    plt.show()


    #using RealAmplitudes
    nqubits=3
    qr = QuantumRegister(nqubits, 'q')

    ansatz_circ = QuantumCircuit(qr)
    ansatz_circ = RealAmplitudes(nqubits)

    x0=[float(random.randint(0,3000))/1000 for i in range(len(ansatz_circ.parameters))]
    print('initial ansatz for ra:\n', x0)

    cost_history = []
    out = minimize(cost_loc, x0, method="COBYLA", options={'maxiter':200})
    print(out)
    print('end of results')

    x = np.arange(0,len(cost_history),1)
    plt.scatter(x,cost_history, color="g")
    plt.show()


    # ### Verifying results for test case #1



    zerovec=np.array([1]+[0 for i in range(2**len(A[0])-1)])


    # In[824]:


    #using fixedStructureAnsatz
    x_fsa = [3.03497294,3.68059907,-0.10831805,1.21603981,1.08343375,2.66673045,
             -0.11051581,1.16625124,2.30077884,0.96587777,2.61451164,0.90462484,
             3.02522104,1.62499983,2.07045172]


    qr = QuantumRegister(nqubits, 'q')
    temp1 = QuantumCircuit(qr)
    temp1 = fixedStructureAnsatz(temp1,[i for i in range(nqubits)])
    V1=Operator(temp1.bind_parameters(dict(zip(temp1.parameters, x_fsa)))).to_matrix()

    x_pos1 = np.real(V1@zerovec)


    #using RealAmplitudes
    x_ra = [2.24503078,1.21717133,2.38979191,0.51223279,1.29820821,1.896024,
            2.44890952,-0.07307036,1.67421469,2.07174518,1.18755991,3.59931302]

    qr = QuantumRegister(nqubits, 'q')
    temp2 = QuantumCircuit(qr)
    temp2 = RealAmplitudes(nqubits)
    V2=Operator(temp2.bind_parameters(dict(zip(temp2.parameters, x_ra)))).to_matrix()

    x_pos2 = np.real(V2@zerovec)


    A_mat=PauliGate(A[0]).to_matrix()

    print('original |b>:\n', B)
    print('|b> using x_fsa:\n',np.real(A_mat@x_pos1))
    print('|b> using x_ra:\n',np.real(A_mat@x_pos2))
    
if __name__ == "__main__":
    main()
