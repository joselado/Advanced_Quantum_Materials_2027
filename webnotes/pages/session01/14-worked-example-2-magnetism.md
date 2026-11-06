## Worked example 2, magnetism {#sec-1-14 number="1.14"}

Let us now include again the spin degree of freedom, and let us change the interaction to an onsite Hubbard term between spin-up and spin-down electrons,

$$H = -t\sum_{n,\sigma}\left(c_{n\sigma}^\dagger c_{n+1,\sigma} + \text{h.c.}\right) + U\sum_n c_{n\uparrow}^\dagger c_{n\uparrow}\, c_{n\downarrow}^\dagger c_{n\downarrow}. \tag{1.7}$$

The sign of $U$ alone decides the physics. An attractive $U<0$ drives superconductivity, which we discuss in Section [1.15](#sec-1-15), and a repulsive $U>0$ drives magnetism, which is the topic of this section.

The mean-field decoupling is done in the same way as before, but now we apply it separately to $\langle c_{\uparrow}^\dagger c_\uparrow\rangle$ and $\langle c_\downarrow^\dagger
c_\downarrow\rangle$, and we obtain a bilinear Hamiltonian with onsite energies that depend on the spin. Let us define the magnetization

$$m = \langle c_\uparrow^\dagger c_\uparrow\rangle - \langle c_\downarrow^\dagger c_\downarrow\rangle. \tag{1.8}$$

Self-consistency gives $m=0$ automatically for $U<0$, and a finite $m$ for $U>0$, which is a real magnetic solution.

::: quiz
For an attractive $U<0$ the self-consistent solution has $m=0$. Why does a finite $m$ not lower the energy?

- [x] An attractive interaction favors double occupation of a site, which has no net spin, so a local moment does not help.
- [ ] The hopping becomes imaginary for $U<0$, which forbids a magnetization.
- [ ] Time reversal is broken explicitly by the sign of $U$.
- [ ] The spin is not conserved for $U<0$.

A negative $U$ rewards a site that holds one electron of each spin. A moment would move electrons away from this configuration, so the energy goes up and not down.
:::

Let us say precisely *which* symmetry is broken here, using the formal definition in [(1.4)](#eq-1-4). Time-reversal symmetry reverses the direction of time and, together with it, every angular momentum in the system, including the spin. On the fermionic operators this means that it exchanges $c_\uparrow^\dagger c_\uparrow \leftrightarrow c_\downarrow^\dagger c_\downarrow$. Since $m$ in [(1.8)](#eq-1-8) changes sign under this exchange, a nonzero $m$ means that the ground state does not pass the invariance test in [(1.4)](#eq-1-4), so it is a magnet by definition. More generally, this is a breaking of the *continuous* spin-rotational symmetry, and this continuous symmetry breaking is what gives rise to the gapless magnon excitations that appear in the table of Section [1.11](#sec-1-11). We will study them in detail in a later session, and in this session we only need the mean-field ground state itself.

Numerically, when we increase $U$ a **Mott gap** opens in the spectrum, which grows linearly with $U$ at large $U$ and is associated with the formation of a real local moment on every site.

![The two-site Hubbard problem, one panel shown again from session 6. With parallel spins the hop is forbidden by the Pauli principle. With antiparallel spins an electron can hop, and it pays the energy $U$ on the doubly occupied site.](figures/s06f02_dimer.svg){panel="a" alt="Two sites with parallel spins and a blocked hop, and two sites with antiparallel spins and an allowed hop."}

::: notebookbox
**Notebook check-in:** [`session1.ipynb`](https://github.com/joselado/Advanced_Quantum_Materials_2027/blob/main/jupyter-notebooks/session1.ipynb), "The interacting Hubbard dimer" (Core), "Magnetic order driven by interactions in a chain" (Core), "Gap opening of the Hubbard model in a chain" (Challenge), and "Gap opening in the Hubbard model on the honeycomb lattice" (Challenge)

Start with the two-site case, the dimer, to see how the self-consistency loop converges in a small system that you can check by hand. Then go to the extended chain and finally to the honeycomb lattice, which uses the same finite-island geometries of Section [1.10](#sec-1-10) but now with interactions, and look at how the Mott gap opens and grows with $U$.
:::

::: {.tryit notebook="session1.ipynb" cell="The interacting Hubbard dimer"}
Run the dimer for $U$ from $0$ to $10$ and read the value of $U$ where the magnetization leaves zero. It is close to $U=2t$. Check that the gap is already $2t$ at $U=0$, since the two levels are at $\pm t$.
:::

## Worked example 3, superconductivity and broken gauge symmetry {#sec-1-15 number="1.15"}

Let us go back to [(1.7)](#eq-1-7) with $U<0$. The mean-field decoupling that we used above always keeps one creation operator and one annihilation operator together, but nothing forces this choice. We can also take an expectation value of two creation operators, or of two annihilation operators,

$$\Delta = \langle c_i c_j\rangle. \tag{1.9}$$

This anomalous term, which is called a "pairing" term, looks qualitatively different from all the terms that we wrote so far, but it is a valid mean-field term. In the self-consistent solution, $\Delta$ is zero for repulsive interactions and can become nonzero for attractive ones, and this is the superconducting order parameter. This worked example is only in the slides, and there is no notebook section for it in this session. The pairing formalism, which is the Bogoliubov-de Gennes formalism that we need to solve it numerically, is left for the session on superconductivity.

Why does this order break gauge symmetry? A gauge transformation acts on the operators as

$$c \to c\, e^{i\varphi}, \qquad c^\dagger \to c^\dagger e^{-i\varphi}. \tag{1.10}$$

Any term built from one creation operator and one annihilation operator, $c^\dagger c$, is invariant under [(1.10)](#eq-1-10), since the two phases cancel. However, the pairing term in [(1.9)](#eq-1-9) is built from *two* annihilation operators, or two creation operators, so under the same transformation it gets a phase $e^{2i\varphi}$, or $e^{-2i\varphi}$, which does not cancel. For this reason a superconductor with $\Delta \neq 0$ breaks the gauge symmetry of the Hamiltonian spontaneously, which is the "broken gauge symmetry" case in the classification of Section [1.11](#sec-1-11). This is directly connected to the puzzle of Section [1.5](#sec-1-5) about a fluctuating number of electrons. To break gauge symmetry and to lose a fixed number of particles are, physically, the same statement. A mean-field superconductor does not have a fixed number of electrons, only a fixed parity.

::: quiz
Under a gauge transformation with $\varphi=\pi/2$, by which factor does the pairing term $c_ic_j$ change?

- [ ] $1$
- [x] $-1$
- [ ] $i$
- [ ] $-i$

Each operator gets a factor $e^{i\varphi}$, so the product gets $e^{2i\varphi}=e^{i\pi}=-1$. Only the values of $\varphi$ that are multiples of $\pi$ leave the term unchanged, and for this reason the pairing term is not gauge invariant.
:::
