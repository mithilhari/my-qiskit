from qiskit import QuantumCircuit
from qiskit_aer import Aer
from qiskit import transpile

def oracle_mark_11():
    # phase-flip |11>
    qc = QuantumCircuit(2)
    qc.cz(0,1)
    return qc

def diffuser(n):
    qc = QuantumCircuit(n)
    qc.h(range(n)); qc.x(range(n))
    qc.h(n-1); qc.mcx(list(range(n-1)), n-1); qc.h(n-1)
    qc.x(range(n)); qc.h(range(n))
    return qc

grover = QuantumCircuit(2,2)
grover.h([0,1])                  # uniform superposition
grover.append(oracle_mark_11().to_gate(label="Oracle"), [0,1])
grover.append(diffuser(2).to_gate(label="Diffuser"), [0,1])
grover.measure([0,1],[0,1])

backend = Aer.get_backend("qasm_simulator")
res = backend.run(transpile(grover, backend), shots=1024).result()
print(res.get_counts())
