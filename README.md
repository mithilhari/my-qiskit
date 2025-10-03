# my-qiskit
FUN


# grover_password

# Grover's Algorithm: Oracle for Password Search

## What is the Oracle?

In **Grover’s algorithm**, the **oracle** is the quantum component that encodes the problem we want to solve.  
For a password search, imagine we have all possible candidate passwords (e.g., all 4-bit strings `0000` → `1111`).  

The oracle is a quantum circuit that:
- Checks if a candidate password is correct.
- **Marks** the correct one by flipping its phase (multiplying the quantum state by -1).
- Leaves all incorrect candidates unchanged.

Formally, the oracle operates as:

\[
O|x⟩ =
\begin{cases}
-|x⟩ & \text{if } x \text{ is the solution (correct password)} \\
|x⟩ & \text{otherwise}
\end{cases}
\]

This “marking” does not reveal the password but allows Grover’s amplification process to increase the probability of measuring the correct state.

---

## Why is the Oracle Important?

- Grover’s algorithm alternates between:
  1. **Oracle step** → Marks the correct password.
  2. **Diffusion step** → Amplifies the probability of measuring the marked state.
- The oracle acts like a **quantum version of**:

```python
if candidate == password:
    mark(candidate)
