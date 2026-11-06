## Linear response and perturbation theory in detail {#sec-9-3 number="9.3"}

Let us now build the quantum version of this idea, since everything that follows is based on it. We split the full Hamiltonian into an unperturbed part $H_0$, which can be a metal, a superconductor, a quantum magnet or any system that we study, and a perturbation $V$. We also add a coupling constant $\lambda$ that helps us keep track of the orders, and at the end we will set it to one.

$$H(\lambda) = H_0 + \lambda V, \qquad \lambda = 0 \;\text{(pristine)}, \quad \lambda = 1\;\text{(full perturbation)}. \tag{9.2}$$

Every observable of the system, such as energies, densities, magnetizations and the wavefunctions themselves, becomes a function of $\lambda$ once we fix $H(\lambda)$. If this function is smooth enough to make a Taylor expansion around $\lambda=0$, and later we will see when this assumption fails, then for any observable $A$ we have

$$A(\lambda) = A^{(0)} + \lambda\, \chi_A + O(\lambda^2), \qquad
\chi_A \equiv \left.\frac{\partial A}{\partial \lambda}\right|_{\lambda=0},$$

and by definition $\chi_A$, the first-order coefficient, *is* the response function that we have been talking about in this session. To compute $\chi_A$ for a generic observable, we first need the perturbed wavefunctions. We expand an unperturbed eigenstate $|n\rangle$ of $H_0$, with energy $E_n^{(0)}$, in the full basis $\{|m\rangle\}$ of $H_0$. Standard Rayleigh-Schrödinger perturbation theory then gives, to first order in $\lambda$ and away from any degeneracy,

$$|n(\lambda)\rangle = |n\rangle + \lambda \sum_{m \neq n} \frac{\langle m|V|n\rangle}{E_n^{(0)} - E_m^{(0)}} \, |m\rangle + O(\lambda^2). \tag{9.3}$$

The structure of [(9.3)](#eq-9-3) is the basis of every derivation in the rest of this session. A perturbation mixes a state $|n\rangle$ with every other state $|m\rangle$. The weight of the mixing is the matrix element of $V$ between the two states, and it is suppressed by the inverse of the energy gap between them. States that are close in energy mix strongly, and states that are far apart in energy almost do not mix. Once we have [(9.3)](#eq-9-3), we can write any observable, in particular any density or magnetization, to first order in $\lambda$ by using the perturbed states.

**When does this break down?** The construction in [(9.3)](#eq-9-3) assumes that $A(\lambda)$ is an analytic function of $\lambda$ close to $\lambda=0$, and this assumption is not always true. There are three paradigmatic quantum states that are known to be intrinsically non-perturbative in this sense, and we mention them explicitly since they mark the limit of everything that we derive below.

- **An impurity in a metal, the orthogonality catastrophe.** In the thermodynamic limit, the full many-body wavefunction of a metal with the impurity switched on becomes exactly orthogonal to the wavefunction with the impurity switched off, for any strength of the impurity potential, even a very weak one.

- **A quantum spin in a metal, the Kondo effect.** The emergent Kondo temperature is a non-perturbative function of the Kondo coupling, since it contains an essential singularity in the coupling constant and not a power series.

- **Superconductivity in the BCS limit.** In the same way, the superconducting gap is non-perturbative in the attractive coupling constant.

In the rest of this session we stay in the regime where perturbation theory *does* work, which is the regime where [(9.2)](#eq-9-2) and [(9.3)](#eq-9-3) give a controlled and systematic way to compute responses.
