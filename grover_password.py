# grover_password.py
from qiskit import QuantumCircuit, transpile
from qiskit_aer import Aer

def ccz(qc, a, b, c):
    qc.h(c); qc.mcx([a, b], c); qc.h(c)  # CCZ via H-CCX-H

def mark_state(qc, bits):
    # bits like '011' for (q2 q1 q0). Map that state to |111|, apply CCZ, uncompute.
    if bits[0] == '0': qc.x(2)  # q2
    if bits[1] == '0': qc.x(1)  # q1
    if bits[2] == '0': qc.x(0)  # q0
    ccz(qc, 0, 1, 2)            # CCZ on (q0, q1 -> target q2)
    if bits[2] == '0': qc.x(0)
    if bits[1] == '0': qc.x(1)
    if bits[0] == '0': qc.x(2)

def oracle_password():
    qc = QuantumCircuit(3)
    mark_state(qc, "011")
    mark_state(qc, "101")
    return qc

def diffuser(n):
    qc = QuantumCircuit(n)
    qc.h(range(n)); qc.x(range(n))
    qc.h(n-1); qc.mcx(list(range(n-1)), n-1); qc.h(n-1)
    qc.x(range(n)); qc.h(range(n))
    return qc

if __name__ == "__main__":
    n = 3
    circ = QuantumCircuit(n, n)
    circ.h(range(n))  # uniform superposition
    circ.append(oracle_password().to_gate(label="Oracle"), range(n))
    circ.append(diffuser(n).to_gate(label="Diffuser"), range(n))
    circ.measure(range(n), range(n))

    backend = Aer.get_backend("qasm_simulator")
    result = backend.run(transpile(circ, backend), shots=2048).result()
    print(result.get_counts())  # '011' and '101' should dominate
