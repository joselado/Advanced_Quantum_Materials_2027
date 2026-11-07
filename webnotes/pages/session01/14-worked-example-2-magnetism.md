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

    This is true. A negative $U$ in [(1.7)](#eq-1-7) rewards a site that holds one electron of each spin. A moment moves electrons away from this configuration, so the energy goes up.

- [ ] Time reversal is broken explicitly by the sign of $U$.

    This is false. The Hamiltonian [(1.7)](#eq-1-7) is real for both signs of $U$, so it is invariant under time reversal in both cases. For $U>0$ the same Hamiltonian has $m\neq 0$ as a spontaneous solution.

- [ ] The spin is not conserved for $U<0$.

    This is false. The hopping does not flip the spin, and the interaction depends only on the densities. So $S_z$ commutes with $H$ for any $U$, positive or negative.

The sign of $U$ decides whether the spins of a site prefer to be unpaired or paired.
:::

Let us now say *which* symmetry is broken here, using the formal definition in [(1.4)](#eq-1-4). Time-reversal symmetry reverses the direction of time and, together with it, every angular momentum in the system, including the spin. On the fermionic operators this means that it exchanges $c_\uparrow^\dagger c_\uparrow \leftrightarrow c_\downarrow^\dagger c_\downarrow$. Since $m$ in [(1.8)](#eq-1-8) changes sign under this exchange, a nonzero $m$ means that the ground state does not pass the invariance test in [(1.4)](#eq-1-4), so it is a magnet by definition. More generally, this is a breaking of the *continuous* spin-rotational symmetry, and this continuous symmetry breaking is what gives rise to the gapless magnon excitations that appear in the table of Section [1.11b](#sec-1-11b). We will study them in detail in Section [6.13](#sec-6-13), and in this session we only need the mean-field ground state itself.

Numerically, when we increase $U$ a **Mott gap** opens in the spectrum. It grows linearly with $U$ at large $U$, and it comes with the formation of a real local moment on every site. [](#sch:s01:afm_gap) shows both, computed from the mean-field equations of this section.

![The antiferromagnetic mean-field solution of [(1.7)](#eq-1-7) at half filling, in units of $t$. On the left, the local moment $m$ of [(1.8)](#eq-1-8) is exponentially small for small $U$ and goes to $1$ when $U\gg t$. On the right, the gap is $Um$, so it grows linearly with $U$ and approaches $U$, the dashed line. The self-consistency is solved for the chain with two sites per cell and checked on a ring of 120 sites at $U=3t$.](figures/web/session01/afm_gap.svg){#sch:s01:afm_gap alt="Two curves against U. The local moment rises from zero and saturates at one. The gap rises from zero and follows the line equal to U at large U."}

![The two-site Hubbard problem, one panel shown again from Session 6. With parallel spins the hop is forbidden by the Pauli principle. With antiparallel spins an electron can hop, and it pays the energy $U$ on the doubly occupied site.](figures/s06f02_dimer.svg){panel="a" alt="Two sites with parallel spins and a blocked hop, and two sites with antiparallel spins and an allowed hop."}

::: notebookbox
**Notebook check-in:** [`session1.ipynb`](https://github.com/joselado/Advanced_Quantum_Materials_2027/blob/main/jupyter-notebooks/session1.ipynb), "The interacting Hubbard dimer" (Core) and "Magnetic order driven by interactions in a chain" (Core). The two challenges are "Gap opening of the Hubbard model in a chain" (Challenge) and "Gap opening in the Hubbard model on the honeycomb lattice" (Challenge).

Start with the two-site case, the dimer, to see how the self-consistency loop converges in a small system that you can check by hand. Then go to the extended chain and finally to the honeycomb lattice, which uses the finite islands of Section [1.10](#sec-1-10) with interactions. Look at how the Mott gap opens and grows with $U$.
:::

::: {.tryit notebook="session1.ipynb" cell="The interacting Hubbard dimer"}
Run the dimer for $U$ from $0$ to $10$ and read the value of $U$ where the magnetization leaves zero. It is close to $U=2t$. Check that the gap is already $2t$ at $U=0$, since the two levels are at $\pm t$.
:::

## Worked example 3, superconductivity and broken gauge symmetry {#sec-1-15 number="1.15"}

Let us go back to [(1.7)](#eq-1-7) with $U<0$. The mean-field decoupling that we used above always keeps one creation operator and one annihilation operator together, but nothing forces this choice. We can also take an expectation value of two creation operators, or of two annihilation operators,

$$\Delta = \langle c_i c_j\rangle. \tag{1.9}$$

This anomalous term, which is called a "pairing" term, looks qualitatively different from all the terms that we wrote so far, but it is a valid mean-field term. In the self-consistent solution, $\Delta$ is zero for repulsive interactions and can become nonzero for attractive ones, and this is the superconducting order parameter. The notebook of this session has no section on this example. To solve it numerically we need the Bogoliubov-de Gennes formalism, which we build in Section [5.8](#sec-5-8).

Why does this order break gauge symmetry? A gauge transformation acts on the operators as

$$c \to c\, e^{i\varphi}, \qquad c^\dagger \to c^\dagger e^{-i\varphi}. \tag{1.10}$$

Any term built from one creation operator and one annihilation operator, $c^\dagger c$, is invariant under [(1.10)](#eq-1-10), since the two phases cancel. However, the pairing term in [(1.9)](#eq-1-9) is built from *two* annihilation operators, or two creation operators, so under the same transformation it gets a phase $e^{2i\varphi}$, or $e^{-2i\varphi}$, which does not cancel. For this reason a superconductor with $\Delta \neq 0$ breaks the gauge symmetry of the Hamiltonian spontaneously, which is the case of broken gauge symmetry in the classification of Section [1.11b](#sec-1-11b). This is directly connected to the puzzle of Section [1.5](#sec-1-5) about a fluctuating number of electrons. To break gauge symmetry and to lose a fixed number of particles are, physically, the same statement. A mean-field superconductor does not have a fixed number of electrons, only a fixed parity. [](#sch:s01:gauge_phase) shows the two cases in the complex plane.

![The phase of a term under the gauge transformation [(1.10)](#eq-1-10). In (a), the factors $e^{i\varphi}$ of $c$ and $e^{-i\varphi}$ of $c^\dagger$ cancel, so $c^\dagger c$ does not move. In (b), the two factors of $c_ic_j$ add, so $\Delta$ turns by the angle $2\varphi$. For $\varphi=\pi/2$ it ends at $-\Delta$.](figures/web/session01/gauge_phase.svg){#sch:s01:gauge_phase alt="Two unit circles in the complex plane. In the first, the factors of c and of c dagger are opposite rotations and the product stays at one. In the second, the pairing amplitude turns by twice the angle, to minus Delta for a quarter turn."}

::: quiz
Under a gauge transformation with $\varphi=\pi/2$, by which factor does the pairing term $c_ic_j$ change?

- [ ] $1$

    This is false. Each operator gets $e^{i\pi/2}=i$, so the product gets $i^2=-1$. The factor $1$ appears only for $\varphi=0$ or $\varphi=\pi$.

- [x] $-1$

    This is true. Each operator gets a factor $e^{i\varphi}$, so the product gets $e^{2i\varphi}=e^{i\pi}=-1$. Only multiples of $\pi$ leave the term unchanged, so the pairing term is not gauge invariant.

- [ ] $i$

    This is false. The factor $i$ is what one operator gets at $\varphi=\pi/2$. The term has two operators, and for $\varphi=\pi/4$ we would get $e^{i\pi/2}=i$, and not for $\pi/2$.

The pairing term changes by $e^{2i\varphi}$, so its phase is a physical quantity.
:::

::: comesback
- The Hubbard model [(1.7)](#eq-1-7) and its mean-field magnet are solved again in Section [6.3](#sec-6-3), and Section [6.6](#sec-6-6) gives the Stoner criterion for the onset of magnetism.
- At large $U$ the local moments of this section couple through superexchange, and Section [6.8](#sec-6-8) derives the Heisenberg model that describes them.
- The pairing term [(1.9)](#eq-1-9) is the start of Session 5. Section [5.7](#sec-5-7) writes the gauge transformation [(1.10)](#eq-1-10) in explicit form, and Section [5.8](#sec-5-8) builds the BdG Hamiltonian.
:::
