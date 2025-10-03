from qiskit import QuantumCircuit
from qiskit_aer import Aer
from qiskit import transpile

# 2 qubits, 2 classical bits
qc = QuantumCircuit(2, 2)
qc.h(0)          # put qubit 0 in superposition
qc.cx(0, 1)      # entangle with qubit 1
qc.measure([0,1],[0,1])
print(qc.draw())

backend = Aer.get_backend("qasm_simulator")
t_qc = transpile(qc, backend)
result = backend.run(t_qc, shots=2048).result()
print(result.get_counts())
