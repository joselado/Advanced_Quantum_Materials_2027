## Worked example 1, the charge density wave {#sec-1-13 number="1.13"}

Let us take the simplest interacting case, which is a spinless one-dimensional chain with nearest-neighbor hopping $t$ and a nearest-neighbor Coulomb repulsion $V$,

$$H = -t\sum_n \left(c_n^\dagger c_{n+1} + \text{h.c.}\right) + V\sum_n c_n^\dagger c_n\, c_{n+1}^\dagger c_{n+1}. \tag{1.6}$$

In this form, every site is equivalent because of translational symmetry. The quartic term is the difficult one, so mean-field theory factorizes it. We replace one pair of operators by its expectation value, and we keep the rest as it is. This is an *uncontrolled* approximation, and a more rigorous way exists with a path integral and a saddle-point approximation, but it is the practical method that we will use in the whole course. As a result, the interaction term becomes a single-particle onsite energy that depends on the position. Nothing forces the expectation value $\langle c_n^\dagger c_n\rangle$ to be the same at every site, so even if the bare Hamiltonian [(1.6)](#eq-1-6) is translationally symmetric, the mean-field solution does not have to be. This difference, a symmetric Hamiltonian with an asymmetric ground state, *is* the charge density wave, and it is the same difference that Section [1.11](#sec-1-11) described in the abstract.

More rigorously, mean-field theory is a variational search over single-particle product states, where we minimize $\langle H\rangle$ with respect to the bilinear expectation values $\langle
c_i^\dagger c_j\rangle$ that define the mean-field Hamiltonian. Since the Hamiltonian depends on these expectation values and the expectation values depend on the Hamiltonian, we solve the problem self-consistently. We guess a Hamiltonian, we compute the expectation values that it gives, we build a new Hamiltonian from them, and we repeat until the process converges. Figure [1.4](#fig:s01:mfloop) shows this loop, and every worked example below and every notebook box in this chapter uses it.

![The mean-field self-consistency loop. We guess the bilinear expectation values, build the single-particle Hamiltonian that they give, and diagonalize it. Then we compute the new expectation values and repeat until they do not change anymore. The four stations are one pass of the loop, computed for the charge density wave of [(1.6)](#eq-1-6) on a periodic chain of four sites with $V=3t$. The guessed charges $0.6$ and $0.4$, drawn as columns, raise the onsite energy of the neighboring sites, so the sites of the mean-field Hamiltonian stand at two heights. Filling its two lowest levels gives the new charges $0.82$ and $0.18$, which are not the guess, so the loop goes round again. The three worked examples of this session and every notebook box in this chapter use this same loop.](figures/s01f05_selfconsistency.svg){#fig:s01:mfloop number="1.4"}

::: quiz
In the figure the guessed charges are $0.6$ and $0.4$, and the loop gives $0.82$ and $0.18$. What do we do next?

- [ ] We stop, since the charge is conserved.

    This is false. The total charge is $1$ in both, but the Hamiltonian built from $0.6$ and $0.4$ has a ground state with $0.82$ and $0.18$. The state is not the ground state of its own Hamiltonian, so it is not a solution.

- [x] We use $0.82$ and $0.18$ as the new guess and repeat until the charges do not change.

    This is true. The new charges differ from the guess, so the guess was not self-consistent. We build the Hamiltonian again from the new charges and repeat until the input and the output agree.

- [ ] We change $V$ until the output equals the guess.

    This is false. In the figure $V=3t$ is a parameter of the model. If we tune it until the loop closes, we solve a different Hamiltonian, for another $V$, and not the one that we want.

The loop stops when the charges that we put in are the charges that we get out.
:::

Numerically, at $V=0$ the spectrum is gapless, which is a metal. When $V$ grows, a gap opens in the single-particle spectrum and becomes larger, and at the same time the charge imbalance between even and odd sites grows from zero toward its maximal value, where it is fully polarized. Figure [1.5](#fig:s01:cdw) shows the two limits in real space, together with the spectrum of each one.

![The charge density wave of the chain [(1.6)](#eq-1-6), solved in mean field for a periodic chain of eight sites at half filling. The height of the liquid in each cup is the charge $\langle n_i\rangle$, and next to each chain is its single-particle spectrum, with an electron on every occupied level and degenerate levels side by side. In front, at $V=0$, every site has the same charge and the spectrum is gapless, since the Fermi level is inside a pair of degenerate levels. Behind, the nearest-neighbor repulsion drives the mean-field instability (here $V=3t$), and the charge accumulates on alternating sites, which doubles the unit cell, drawn as the translucent slab, and opens a gap in the spectrum. The Hamiltonian is translationally symmetric in both cases, but the ground state behind is not.](figures/s01f04_cdw.svg){#fig:s01:cdw number="1.5"}

::: quiz
The charge density wave of the chain has charges that alternate from site to site. How many degenerate ground states does the mean-field solution have?

- [ ] One.

    This is false. A translation by one site maps the charges $(0.8,0.2,0.8,0.2)$ to $(0.2,0.8,0.2,0.8)$. This is a different state with the same energy, so there are at least two.

    ![A translation by one site exchanges the two patterns. The area of the dark disc on each site is the charge $\langle n_i\rangle$, and the two chains have the same energy.](figures/web/session01/cdw_patterns.svg){alt="Two chains of six sites, with large and small charges alternating, where the second is the first shifted by one site."}

- [x] Two.

    This is true. The charge can sit on the even sites or on the odd sites. These two patterns are exchanged by a translation of one site, so they have the same energy and the translational symmetry is broken.

- [ ] Four.

    This is false. A pattern of period two returns to itself after two translations, so the translations give only two different states. We would need a period of four, such as $(0.9,0.5,0.1,0.5)$, for four states.

The number of degenerate states equals the number of different patterns that the broken symmetry generates.
:::

::: notebookbox
**Notebook check-in:** [`session1.ipynb`](https://github.com/joselado/Advanced_Quantum_Materials_2027/blob/main/jupyter-notebooks/session1.ipynb), "Symmetry breaking in the spinless fermionic chain" (Core), and "Gap opening in a spinless interacting model" (Challenge)

Run the self-consistency loop of Section [1.13](#sec-1-13) yourself. Start from an unbiased guess, iterate, and look at how the charge imbalance on each site grows with $V$, together with the opening of the gap in the spectrum and in the density of states.
:::

::: {.tryit notebook="session1.ipynb" cell="Symmetry breaking in the spinless fermionic chain"}
Run the loop and plot the charge imbalance against $V$. Check that it grows from zero and saturates close to $1$ for large $V$, where one sublattice is almost full. Then set `cdw=0.1` and check that the imbalance is finite even at $V=0$.
:::
