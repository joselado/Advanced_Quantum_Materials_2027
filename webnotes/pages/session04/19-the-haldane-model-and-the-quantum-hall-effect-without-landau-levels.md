## The Haldane model and the quantum Hall effect without Landau levels {#sec-4-19 number="4.19"}

This last section goes back on purpose to a model that we already know, and it is not new material. In session 3 we already built the Haldane model, as an example of a Chern insulator obtained by opening a gap in a Dirac cone without any external field. We come back to it here because it closes the argument that we started in this session. Everything above needed a real magnetic field to give Landau levels, so we want to confirm explicitly that the quantized Hall conductance itself never needed one.

Let us recall the construction. We start from the honeycomb lattice with first-neighbor hopping only, which has a Dirac cone without a gap at $K$ and $K'$, and we add a second-neighbor hopping that is purely imaginary, which breaks time-reversal symmetry. In the Bloch Hamiltonian this term appears as a mass at $K$ and $K'$. An ordinary staggered onsite potential also gives a mass at both valleys, but the two masses enter with opposite relative sign between the valleys. For the staggered potential the Berry curvatures of the two valleys have opposite sign and cancel, which gives $C=0$. For the Haldane term, the imaginary second-neighbor hopping, the Berry curvatures of the two valleys have the *same* sign, so when we integrate over the Brillouin zone the two valley contributions add and do not cancel, which gives $C=\pm1$. The result is a net nonzero Chern number, an insulating bulk gap and a chiral edge state, all with $B=0$.

![The ribbon spectra of the two gapped honeycomb lattices of session 3. On the left a staggered potential gives a gap with nothing inside. On the right the Haldane coupling gives one branch per edge that crosses the gap, with no magnetic field. Look at the dark and the light branch, which live on opposite edges.](figures/s03f05_masses.svg){panel="spec" alt="Two ribbon spectra, one with an empty gap and one with a branch from each edge crossing the gap."}

What is really new in our version of this story is the explicit **adiabatic connection** between the Haldane model and the ordinary quantum Hall state of this session, which is driven by the field. We start in the Haldane model, with imaginary second-neighbor hopping and no field. Then we switch on a real magnetic field while we keep the Haldane coupling, and Landau levels develop from the bands that were dispersive before. Finally we switch off the Haldane coupling, and the system is left in the ordinary quantum Hall state built only from Landau levels. At every step of this path the bulk gap stays open and the chiral edge state never disappears. Since we can connect the two end points without closing the gap, the Chern insulator of the Haldane model and the quantum Hall state of the Landau levels are *topologically equivalent*. They are the same phase of matter, reached by two completely different physical routes, one that needs a magnetic field and one that does not.

::: quiz
Along the path from the Haldane model to the quantum Hall state, which condition has to hold at every step?

- [ ] The magnetic field is zero.

    This is false. The path starts at zero field and then switches on a real magnetic field. At the end of the path the field is not zero.

- [x] The bulk gap stays open.

    This is true. The Chern number can change only if the gap closes. If the gap stays open all along the path, the two end points have the same Chern number.

- [ ] The Haldane coupling stays at the same value.

    This is false. The path ends by switching off the Haldane coupling, so at the end it is zero. If it stayed fixed, the end point would not be the ordinary quantum Hall state.

:::

::: notebookbox
**Notebook check-in:** [`session4.ipynb`](https://github.com/joselado/Advanced_Quantum_Materials_2027/blob/main/jupyter-notebooks/session4.ipynb), "Topological equivalence between the Quantum Hall state and a Chern insulator" (Challenge), and "Topological domains in the quantum Hall state" (Challenge)

Build the Haldane model, switch a magnetic field on and off numerically together with the Haldane coupling, and follow the bulk gap and the Chern number along the adiabatic path described above. The "topological domains" exercise lets you study spatial regions where the two couplings compete directly, which is a practical version of the equivalence argument that we just gave.
:::

::: quiz
One system has a field and Landau levels, and the other has no field. Why do we call them the same phase?

- [ ] Because the magnetic field is only a gauge choice.

    This is false. The flux through a plaquette is gauge invariant, and the field cannot be removed by a gauge change. In the Haldane model the flux through the unit cell is zero while it is finite for the Landau levels, and the phase is the same.

- [x] Because they are connected without closing the bulk gap, so they have the same Chern number and the same chiral edge state.

    This is true. A phase is defined by what cannot change without closing the gap. The Chern number is the same for both, and the field is only one of the two routes to it.

- [ ] Because both have Landau levels.

    This is false. The Haldane model at zero field has dispersive bands and no flat Landau levels, yet its Chern number is $\pm1$, as the quantum Hall state with one filled level.

:::

::: {.tryit notebook="session4.ipynb" cell="Topological equivalence between the Quantum Hall state and a Chern insulator"}
Run the cell, which interpolates between the Chern insulator at `nu = 0` and the quantum Hall state at `nu = 1`. Follow the branch that crosses the gap in the first panel. It stays connected to the edge branch of the last panel, and it does not disappear at any step of the path.
:::
