from qiskit_aer import AerSimulator
from qiskit_aer.noise import NoiseModel, depolarizing_error
from qiskit import QuantumCircuit, transpile

qc = QuantumCircuit(1,1)
qc.h(0); qc.measure(0,0)

# simple depolarizing noise on 1- and 2-qubit gates
noise = NoiseModel()
noise.add_all_qubit_quantum_error(depolarizing_error(0.01, 1), ['u1','u2','u3','x','h'])
noise.add_all_qubit_quantum_error(depolarizing_error(0.02, 2), ['cx'])

sim = AerSimulator(noise_model=noise)
t_qc = transpile(qc, sim)
res = sim.run(t_qc, shots=2000).result()
print(res.get_counts())
