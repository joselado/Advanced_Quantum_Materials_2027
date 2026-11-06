## Edge states and why an insulating bulk still conducts {#sec-4-5 number="4.5"}

There is an obvious puzzle. If the chemical potential is in a gap between two Landau levels, the bulk of the sample is by definition an insulator, since there is no partially filled band and there are no bulk states at the Fermi energy. So how can such a system carry a finite, quantized current?

The answer is the same as in the general bulk-boundary argument of session 3. A nonzero Chern number cannot end without consequences. At any interface where the Chern number changes, which here is the boundary between a sample with Chern number $N$ and the vacuum, which has $C=0$, there must be $N$ protected, gapless and chiral edge modes. A chiral mode propagates in only one direction, and the number of edge modes at an interface is equal to the difference in Chern number across it. Every real sample is finite, so it always has an edge, and the edge states are always there, even when we do not think about them. When we apply a voltage between the top edge and the bottom edge of the sample, we create an imbalance between the edge electrons that move to the right and the ones that move to the left, and this imbalance is the quantized Hall current.

The band structure of a ribbon, which is a sample that is infinite in $y$ and finite in $x$, shows this picture in a completely explicit way. Next to the flat bulk Landau levels without dispersion, we find a set of dispersive states localized at the left edge, which all propagate in one direction, and a mirror set localized at the right edge, which propagate in the opposite direction. Each propagation direction is tied to a *location*, the left edge or the right edge, so an impurity on the left edge cannot scatter a left-moving electron into a right-moving one, because the right edge is at a macroscopic distance. There is no available final state, so there is no backscattering, and the edge transport has no dissipation. Figure [4.1](#fig:s04:ribbon) shows the ribbon spectrum next to its real-space picture, together with the chiral modes that cross the chemical potential.

![The quantum Hall ribbon. (a) The spectrum of a strip that is infinite along $y$ and finite along $x$, computed for a width of $12\,\ell_B$ with hard walls. In the bulk the Landau levels [(4.6)](#eq-4-6) are exactly flat, so they carry no current at all, but near each boundary the guiding centre $x_0=\hbar k_y/B$ is pushed into the wall and the level bends up strongly. These bending branches are the edge states, and each of them crosses the chemical potential, the translucent plane, exactly once per edge, at the balls, so the number of chiral modes at a given edge is equal to the number $N$ of filled Landau levels, here $N=2$. (b) The same statement in real space, seen from above. The branches with $k_y>0$ have $v_y=\hbar^{-1}\partial_{k_y}E>0$ and live on the right edge, and the branches with $k_y<0$ move in the opposite direction and live on the left edge. To reverse the velocity of an electron we would therefore have to move it to the other side of the sample, which no local impurity can do, and this is why the edge transport has no dissipation.](figures/s04f01_ribbon.svg){#fig:s04:ribbon number="4.1"}

::: quiz
An impurity sits on the left edge of a quantum Hall ribbon. Why can it not backscatter an edge electron?


- [x] The only states that move in the opposite direction at the same energy are on the other edge, which is far away.
- [ ] The impurity is always too weak to scatter.
- [ ] The bulk Landau levels are full and block the scattering.
- [ ] Time-reversal symmetry forbids it.

On one edge all the modes propagate in the same direction. A state that propagates the other way is on the other side of the sample, and a local impurity cannot connect the two.
:::

::: quiz
The chemical potential moves from the gap above the first Landau level to the gap above the third. How do the number of chiral modes at one edge and $\sigma_{xy}$ change?

- [ ] The number of modes stays at one, and $\sigma_{xy}$ changes from $e^2/h$ to $3e^2/h$.
- [x] From one to three, and from $e^2/h$ to $3e^2/h$.
- [ ] From one to two, and from $e^2/h$ to $2e^2/h$.
- [ ] From one to three, and $\sigma_{xy}$ stays at $e^2/h$.

The number of chiral modes at an edge is equal to the Chern number of the bulk, which counts the filled Landau levels. The Hall conductance is this number times $e^2/h$.
:::

::: notebookbox
**Notebook check-in:** [`session4.ipynb`](https://github.com/joselado/Advanced_Quantum_Materials_2027/blob/main/jupyter-notebooks/session4.ipynb), "Localization of the edge states in the quantum Hall effect in a ribbon" (Challenge), and "Localization of the edge states in the quantum Hall effect in an island" (Challenge)

Build a finite ribbon and a finite island in a magnetic field and look directly at where the edge-state wavefunctions are in real space. This confirms the separation between the left and the right edge, or along the perimeter of the island, which is the basis of the argument above for the absence of backscattering.
:::

::: {.tryit notebook="session4.ipynb" cell="Localization of the edge states in the quantum Hall effect in a ribbon"}
Run the cell and look at the four maps of the local density of states. At the two energies inside the gap above the zero mode, the weight sits at the edges and not in the middle. Change `0.01` in `h.add_orbital_magnetic_field(0.01)` to `0.02`. The gap grows, and the edge weight stays at the boundary.
:::
