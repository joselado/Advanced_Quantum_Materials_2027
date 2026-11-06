## Worked example 3, superconductivity and broken gauge symmetry {#sec-1-15 number="1.15"}

Let us go back to [(1.7)](#eq-1-7) with $U<0$. The mean-field decoupling that we used above always keeps one creation operator and one annihilation operator together, but nothing forces this choice. We can also take an expectation value of two creation operators, or of two annihilation operators,

$$\Delta = \langle c_i c_j\rangle. \tag{1.9}$$

This anomalous term, which is called a "pairing" term, looks qualitatively different from all the terms that we wrote so far, but it is a valid mean-field term. In the self-consistent solution, $\Delta$ is zero for repulsive interactions and can become nonzero for attractive ones, and this is the superconducting order parameter. This worked example is only in the slides, and there is no notebook section for it in this session. The pairing formalism, which is the Bogoliubov-de Gennes formalism that we need to solve it numerically, is left for the session on superconductivity.

Why does this order break gauge symmetry? A gauge transformation acts on the operators as

$$c \to c\, e^{i\varphi}, \qquad c^\dagger \to c^\dagger e^{-i\varphi}. \tag{1.10}$$

Any term built from one creation operator and one annihilation operator, $c^\dagger c$, is invariant under [(1.10)](#eq-1-10), since the two phases cancel. However, the pairing term in [(1.9)](#eq-1-9) is built from *two* annihilation operators, or two creation operators, so under the same transformation it gets a phase $e^{2i\varphi}$, or $e^{-2i\varphi}$, which does not cancel. For this reason a superconductor with $\Delta \neq 0$ breaks the gauge symmetry of the Hamiltonian spontaneously, which is the "broken gauge symmetry" case in the classification of Section [1.11](#sec-1-11). This is directly connected to the puzzle of Section [1.5](#sec-1-5) about a fluctuating number of electrons. To break gauge symmetry and to lose a fixed number of particles are, physically, the same statement. A mean-field superconductor does not have a fixed number of electrons, only a fixed parity.
