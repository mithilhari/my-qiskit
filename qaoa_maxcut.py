# qaoa_maxcut.py
import networkx as nx
from qiskit_optimization import QuadraticProgram
from qiskit_optimization.algorithms import MinimumEigenOptimizer
from qiskit_optimization.converters import QuadraticProgramToQubo
from qiskit_algorithms import QAOA
from qiskit_algorithms.optimizers import COBYLA
from qiskit_aer.primitives import Estimator as AerEstimator
from qiskit_aer.primitives import Sampler as AerSampler
def maxcut_qubo_from_graph(G: nx.Graph) -> QuadraticProgram:
    """Build Max-Cut as a QuadraticProgram:
       maximize sum_{(i,j) in E} w_ij * x_i (1 - x_j) + x_j (1 - x_i)
       which becomes a quadratic objective over binary vars.
    """
    qp = QuadraticProgram()
    for v in G.nodes():
        qp.binary_var(f"x_{v}")
    # Max-Cut standard quadratic form: (1 - z_i z_j)/2 using z_i in {+1,-1}
    # We’ll use x in {0,1} and convert; easiest is rely on converter to QUBO.
    # Construct objective: sum w_ij * (x_i + x_j - 2 x_i x_j)
    linear = {}
    quadratic = {}
    constant = 0.0
    for (i,j, w) in G.edges.data("weight", default=1.0):
        linear[f"x_{i}"] = linear.get(f"x_{i}", 0.0) + w
        linear[f"x_{j}"] = linear.get(f"x_{j}", 0.0) + w
        quadratic[(f"x_{i}", f"x_{j}")] = quadratic.get((f"x_{i}", f"x_{j}"), 0.0) - 2.0 * w
    qp.maximize(linear=linear, quadratic=quadratic, constant=constant)
    return qp

def bitstring_to_cut(bitstring, nodes):
    left, right = [], []
    for b, v in zip(bitstring, nodes):
        (left if b == "0" else right).append(v)
    return left, right

def cut_value(G, bitstring):
    val = 0.0
    for u, v, w in G.edges.data("weight", default=1.0):
        if bitstring[u] != bitstring[v]:
            val += w
    return val

if __name__ == "__main__":
    # 1) Build a small weighted graph
    G = nx.Graph()
    G.add_weighted_edges_from([
        (0,1,1.0), (1,2,1.0), (2,3,1.0), (3,0,1.0),  # a 4-cycle
        (0,2,0.6)                                    # diagonal
    ])

    # 2) Formulate Max-Cut as QUBO
    qp = maxcut_qubo_from_graph(G)
    qubo = QuadraticProgramToQubo().convert(qp)

    # 3) QAOA (p=2 is a good start)
    estimator = AerEstimator()  # simulator-based expectation values
    sampler = AerSampler()
    qaoa = QAOA(sampler=sampler, optimizer=COBYLA(maxiter=100), reps=2)
    solver = MinimumEigenOptimizer(qaoa)

    # 4) Solve
    result = solver.solve(qubo)

    # 5) Report
    bitstr = "".join(str(int(result.x[i])) for i in range(len(G.nodes)))
    nodes = list(G.nodes)
    left, right = bitstring_to_cut(bitstr, nodes)

    # remap bitstring index -> node if nodes aren’t 0..n-1
    assign = {nodes[i]: bitstr[i] for i in range(len(nodes))}
    print("Best bitstring:", assign)
    print("Cut partitions: LEFT", left, "RIGHT", right)
    print("Objective (QAOA):", result.fval)
    print("Cut value recomputed:", cut_value(G, assign))
