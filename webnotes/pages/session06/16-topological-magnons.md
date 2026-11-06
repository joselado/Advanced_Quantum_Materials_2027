## Topological magnons {#sec-6-16 number="6.16"}

Once magnons have a real band structure, which is a dispersion $E(\mathbf k)$ over the Brillouin zone, we can ask about *magnon* bands the same question that we have already asked twice about *electronic* bands. Can this band structure have a nontrivial topological invariant? To answer it, we use again the Chern number of sessions 3 and 4, where the Berry curvature $\Omega(\mathbf k)$ of a Bloch band is integrated over the Brillouin zone and gives an integer,

$$C = \frac{1}{2\pi}\int_\text{BZ} \Omega(\mathbf k)\, d^2k, \tag{6.10}$$

and this is the third time that we apply it, now to the bosonic Bogoliubov Hamiltonian of Section [6.15](#sec-6-15) instead of an electronic tight-binding Hamiltonian. We add to the plain Heisenberg exchange a spin-orbit coupling of the Dzyaloshinskii-Moriya type of Section [6.12](#sec-6-12). This term plays the same role as the complex second-neighbor hopping of the Haldane model for electrons in session 4. It introduces complex phases in the magnon hopping amplitudes, which can open a gap in the magnon band structure at finite energy and give the bands on both sides of this gap a nonzero Chern number [(6.10)](#eq-6-10). When we put such a topological magnon Hamiltonian on a ribbon, the bulk-boundary correspondence guarantees chiral magnon edge modes inside the gap. These modes propagate in only one direction along each edge, and they are the magnon analogue of the chiral electronic edge states of a Chern insulator. They carry spin and energy and not charge, but they are topologically protected in the same sense as their electronic counterparts. It is the same tool that we used for electrons in sessions 3 and 4, now applied to magnon bands.

![The chiral edge states of a Chern insulator, seen from above. The topological magnon bands have the same edge structure, with spin and energy carried by the magnons instead of charge.](figures/s03f01_chiraledge.svg){alt="A sample with arrows that skip along the edge in one direction on each edge, and an impurity that the edge mode goes around."}

::: quiz
A magnon band gap has bands with Chern numbers $\pm1$. What do we find on the edges of a ribbon?

- [ ] Nothing, since magnons are neutral.

    This is false. The bulk-boundary correspondence counts Chern numbers and does not use charge. In the Haldane model with $C=\pm1$ the same counting gives one chiral branch, and for magnons it carries spin and heat.

- [x] One chiral magnon branch crosses the gap on each edge, and the two edges have opposite directions.

    This is true. The chiral edge branches carry spin and energy, one per unit of Chern number. On the two edges of a ribbon they run in opposite directions.

- [ ] Branches in both directions on the same edge.

    This is false. Two branches of opposite direction on one edge give a net chirality of zero. They could backscatter into each other and gap out, so they cannot be required by $C=\pm1$.
:::

::: quiz
We reverse the sign of the Dzyaloshinskii-Moriya vector. What happens to the topological magnon bands?

- [ ] The gap closes for good.

    This is false. Reversing the vector is a mirror operation, so the spectrum is the same. In the Haldane model the phases $+\pi/2$ and $-\pi/2$ give identical gaps, and only $C$ changes sign.

- [x] The Chern numbers change sign, and the edge branches run the other way.

    This is true. This term plays the role of the complex hopping of the Haldane model, and reversing its sign reverses the phases. The Berry curvature changes sign, so the Chern numbers change sign too.

- [ ] Nothing, since the term is quadratic.

    This is false. In the Haldane model the phase $\varphi=+\pi/2$ gives $C=+1$ and $\varphi=-\pi/2$ gives $C=-1$. The direction of the edge branch follows this sign, so it does change.
:::

::: notebookbox
**Notebook check-in:** [`session6.ipynb`](https://github.com/joselado/Advanced_Quantum_Materials_2027/blob/main/jupyter-notebooks/session6.ipynb), "(Exercise) Topological magnons in 2D magnets"

Construct a magnon Hamiltonian with a spin-orbit term of Dzyaloshinskii-Moriya type on top of the Heisenberg exchange, compute its Chern number with [(6.10)](#eq-6-10), and look for chiral magnon edge modes on a ribbon. This reproduces directly, for magnons, the argument of the bulk-boundary correspondence above.
:::

::: {.tryit notebook="session6.ipynb" cell="Topological magnons in 2D magnets"}
In the cell, `h.add_haldane(0.1)` sets the complex hopping that plays the role of the Dzyaloshinskii-Moriya term. Change it to `-0.1` and compute `h.get_chern()` before building the ribbon. The Chern number changes sign.
:::

Before we stop, a short comment on the scope of these notes. The companion notebook goes further than the lecture of this session in a few places. The most visible ones are its exercises on electronic and magnetic symmetry breaking in graphene multilayers, and its last sections on many-body spin response functions. These are real and useful extensions of the material of this session. However, neither the transcript nor the slides of this session narrate them, so we have not included the corresponding derivations in these notes. They should be taken as independent work with the notebook, and not as material that these notes derive.
