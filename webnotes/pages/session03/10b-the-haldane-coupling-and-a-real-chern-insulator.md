## The Haldane coupling and a real Chern insulator {#sec-3-10b number="3.10b"}

The staggered potential gave $C=0$, so it remains to see the second choice of the mass term. Now let us instead open the gap with a purely imaginary second-neighbor hopping, which is called the **Haldane coupling**. Physically, this term is a pattern of local orbital currents that circulate inside each hexagon, and it is odd under time reversal. This mass term changes sign between $K$ and $K'$ *relative to* $\lambda$, so the two Dirac points now give Chern numbers of the *same* sign, which add and do not cancel. The result is $C = \pm 1$, a real Chern insulator, built only from lattice hoppings and without any external magnetic field. This was the first model with a finite and quantized Hall conductivity and zero net flux. It is the mechanism to open a gap in the Dirac cone of Section [2.11](#sec-2-11) that we were looking for. Figure [3.5](#fig:s03:masses) shows the two cases side by side, each on the lattice and in the spectrum of a ribbon, where only the Haldane case has edge states that cross the gap. A gap can also be opened by combining an ordinary magnetization with spin-orbit coupling, which gives the same sign pattern as the Haldane term and an equivalent quantum anomalous Hall state. Both routes have material realizations. Physics similar to the Haldane model has been realized in twisted graphene bilayers on boron nitride, and the route with magnetism and spin-orbit coupling has been realized and measured in Cr-doped (Bi,Sb)$_2$Te$_3$.

![Two ways to gap the Dirac cones of the honeycomb lattice, on the lattice and in the spectrum of a zigzag ribbon. Equation [(3.8)](#eq-3-8) gives each gapped Dirac point a Chern number $\tfrac 12\,\mathrm{sgn}(m)\,\mathrm{sgn}(\lambda)$, and the two Dirac points of the honeycomb lattice are time-reversal partners with opposite chirality, $\lambda=+1$ at $K$ and $\lambda=-1$ at $K'$. So the result depends only on how the mass term itself behaves under time reversal. (a) A staggered sublattice potential, $+m$ on the large dark sites and $-m$ on the small light ones, is an ordinary scalar potential. It is even under time reversal, so $m$ has the same sign at both valleys. The two half-integers are then opposite and they cancel, which gives an ordinary insulator with the same kind of gap as boron nitride. The ribbon spectrum below it has a gap with nothing in it. (b) The Haldane coupling, the second-neighbor hoppings drawn as arrows around one hexagon, is a pattern of circulating orbital currents, which is odd under time reversal, so $m$ changes sign between the valleys. The two half-integers are then equal and they add, which gives $C=\pm 1$. This is a real Chern insulator with quantized $\sigma_{xy}$ and chiral edge states, built only from lattice hoppings, with no external magnetic field and zero net flux. In the ribbon spectrum one branch from each edge, the dark and the light tube, crosses the gap. The two gaps look the same in the bulk spectrum, and the difference appears only in the wavefunctions. The spectra are computed for ribbons 16 cells wide, with $m=0.5$ and $t_2=0.1$ in units of the first-neighbor hopping.](figures/s03f05_masses.svg){#fig:s03:masses number="3.5"}

::: quiz
We keep the Haldane coupling fixed and increase a staggered potential until it is larger than the Haldane mass. What happens to the Chern number?

- [ ] It stays at $\pm 1$, since the Haldane coupling is still there.

    This is false. Take a Haldane mass $0.5$ and a staggered mass $1$. The masses at the two valleys are $1.5$ and $0.5$, both positive, so $C=\tfrac12-\tfrac12=0$.

- [ ] It goes to $\pm 2$, since both masses add.

    This is false. The two masses add at one valley and subtract at the other, and each Dirac point gives at most $\pm\tfrac12$.

- [x] It goes to $0$, since the gap closes at one valley and the two valleys then cancel.

    This is true. The net masses of the two valleys are $m_s+m_H$ and $m_s-m_H$. When the staggered one wins both have the same sign, and the two half-integers of [(3.8)](#eq-3-8) are opposite and cancel.

:::

We can follow this cancellation on the lattice. In [](#sch:s03:haldane_phase) we keep the Haldane coupling fixed and we increase the staggered potential $M$. The staggered potential $M$, which Figure [3.5](#fig:s03:masses) writes as $m$, gives the mass $m$ of [(3.7)](#eq-3-7) with the same sign at both valleys. The Haldane coupling instead gives masses of opposite sign at $K$ and $K'$, and only this one gives $C=\pm1$.

![The honeycomb lattice with the Haldane coupling $t_2=0.1$ and a staggered potential $M$, computed on the lattice. At the top is the gap of the bulk. At the bottom is the Chern number of the lower band, from a grid of 60 by 60 points. The gap closes at $M=\pm m_H$, with $m_H=3\sqrt{3}\,t_2\approx0.52$, which is where the mass of one valley changes sign, and $|C|$ jumps from $1$ to $0$ there. Look at the zeros of the gap, since a Chern number can change only where the gap closes.](figures/web/session03/haldane_phase.svg){#sch:s03:haldane_phase alt="The bulk gap against the staggered potential, with two zeros, and below it the Chern number, equal to one between the zeros and to zero outside."}

::: notebookbox
**Notebook check-in:** [`session3.ipynb`](https://github.com/joselado/Advanced_Quantum_Materials_2027/blob/main/jupyter-notebooks/session3.ipynb), "The quantum anomalous Hall effect" (Core), "Edge states of the quantum anomalous Hall state" (Core) and "Topological phase transitions in the edge" (Core). Two more sections are challenges, "Topological states and topological invariants" (Challenge) and "Topological phase transitions in the bulk" (Challenge).

Build the honeycomb ribbon with the Haldane coupling and without magnetic field, and check that the same chiral edge states of Section [3.6](#sec-3-6) appear, as the argument above predicts. Then, in the exercise on the Berry curvature, integrate the curvature separately for the Haldane coupling and for a sublattice imbalance. You should find a non-zero net Chern number for the Haldane case and a vanishing one for the sublattice imbalance, which is the difference between cancellation and addition that we worked out around [(3.8)](#eq-3-8). Then combine both terms and change their relative strength, and follow where the bulk gap closes and then where the edge states do. This is the numerical version of the phase transition at $t=1$ of Section [3.9](#sec-3-9), now in two dimensions. The Berry curvature of [](#sch:s03:berry_haldane) and the ribbon spectra of Figure [3.5](#fig:s03:masses) come from this same computation.
:::

::: quiz
The Haldane coupling has zero net magnetic flux through the unit cell, and yet it gives $C\neq 0$. Why?

- [ ] A small net flux remains in every hexagon.

    This is false. Take the loop of the six first-neighbor bonds around one hexagon. The hoppings are real, so the phase is zero. The complex phases are on the second-neighbor bonds and add to zero over the unit cell.

- [x] A quantized Hall conductivity needs broken time-reversal symmetry, and the complex hopping does this with local currents and zero net flux.

    This is true. What matters is that time reversal is broken, and not that the field is nonzero. The imaginary second-neighbor hopping gives currents that circulate inside each hexagon and cancel on average.

- [ ] The honeycomb lattice is bipartite.

    This is false. The staggered potential lives on the same bipartite honeycomb lattice and gives $C=0$, as in Figure [3.5](#fig:s03:masses). The lattice alone cannot decide the Chern number.

:::

::: {.tryit notebook="session3.ipynb" cell="Topological phase transitions in the bulk"}
The cell fixes the Haldane coupling at 0.05 and increases the sublattice imbalance. The title of each panel gives the Chern number. It is 2 for the first two values of the imbalance and 0 for the last two, because both spin species count. Double the Haldane coupling to 0.1 and run the cell again. The jump of the Chern number needs about twice the imbalance, since the Haldane mass is twice as large.
:::

::: comesback
- In Section [4.19](#sec-4-19) the Haldane model is connected to the quantum Hall state without closing the gap, so the two are the same phase.
- In Section [4.20](#sec-4-20) Cr-doped (Bi,Sb)$_2$Te$_3$ and twisted graphene on boron nitride realize this Chern insulator.
- In Section [6.16](#sec-6-16) a Dzyaloshinskii-Moriya interaction gives the magnons of a honeycomb magnet the same complex second-neighbor hopping.
- In Section [9.8](#sec-9-8) a vacancy in the Haldane model binds a state inside the gap.
:::
