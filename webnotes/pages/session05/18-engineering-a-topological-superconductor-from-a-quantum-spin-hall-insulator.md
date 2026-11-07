## Engineering a topological superconductor from a quantum spin Hall insulator {#sec-5-18 number="5.18"}

Chiral and p-wave superconductors of the kind we need are rare in nature, so in practice they are usually *engineered* and not found. One instructive recipe uses directly the quantum spin Hall (QSH) insulator of Section [3.11](#sec-3-11). We take a QSH insulator, for concreteness tungsten ditelluride (WTe$_2$). Its edge has helical modes, meaning that spin-up electrons propagate in one direction and spin-down electrons propagate in the other direction on the same edge. Now we place ordinary ferromagnets on two segments of this edge. A magnet breaks time-reversal symmetry locally, and this opens a gap in the helical edge modes below it. We recall from Section [3.11b](#sec-3-11b) that the protection of the QSH edge relies on time-reversal symmetry through Kramers degeneracy, so if we break this symmetry locally, the protection is lost there. What remains without a gap is a short isolated segment of helical edge between the two magnetic regions.

This isolated segment only has spin-up electrons moving right and spin-down electrons moving left, with no spin-down electrons moving right and no spin-up electrons moving left. If we count states only by their direction of propagation, this segment is *effectively spinless*, which is the ingredient that the Kitaev-chain construction of Section [5.16](#sec-5-16) needs. If we then couple this segment by proximity to an ordinary s-wave superconductor, we reproduce on it the physics of [(5.19)](#eq-5-19). This is a one-dimensional p-wave superconductor, with Majorana zero modes pinned at the two ends of the isolated segment. Figure [5.6](#fig:s05:qsh) shows the whole setup.

![How to build the Kitaev chain from parts that exist. The edge of a quantum spin Hall insulator is helical. On the same edge spin-up electrons move in one direction and spin-down electrons in the other, drawn in a warm and a cold color. A ferromagnet placed on a part of this edge breaks time-reversal symmetry locally and removes the Kramers protection there, which opens a gap in the edge below it, where the channels are drawn faded. With two ferromagnets, one short helical segment survives between them. This segment has only one direction of propagation for each spin, so if we count channels it is a *spinless* one-dimensional wire. This is the ingredient that [(5.19)](#eq-5-19) needs, and nature does not give it to us directly. Coupling it by proximity to an ordinary $s$-wave superconductor gives the pairing. The result is a one-dimensional $p$-wave superconductor with a Majorana zero mode at each end of the segment, which means at the two ferromagnet-superconductor interfaces. Note what was *not* needed. No unconventional superconductor appears in the recipe, only an $s$-wave one, a magnet and a topological insulator.](figures/s05f06_qsh.svg){#fig:s05:qsh number="5.6"}

![The two steps of Figure [5.6](#fig:s05:qsh), computed for an edge with velocity $v=1$. (a) The helical edge, with spin up moving right and spin down moving left, is drawn with dashed lines. A magnet with an exchange field $h$ along $x$ couples the two branches and opens a gap $2h$ at $k=0$, as the solid lines show. (b) The levels at $k=0$ of the BdG Hamiltonian of the edge with both $h$ and an $s$-wave $\Delta$, for $\mu=0$. They are $\pm h\pm\Delta$, and the gap closes at $h=\Delta$. For $h<\Delta$ the gap comes from pairing, and for $h>\Delta$ it comes from the magnet. These are two different phases, and the Majorana zero mode sits at the boundary between them.](figures/web/session05/helical_edge_gap.svg){#sch:s05:helical_edge_gap alt="On the left, two crossing straight lines for the helical edge and a hyperbola with a gap 2h for the edge under a magnet. On the right, four straight lines against h over Delta, two of which cross zero at h equal to Delta."}

::: quiz
The segment of helical edge between the two magnets is called effectively spinless. Why?

- [ ] The magnets remove the spin of the electrons.

    This is false. A magnet only breaks time-reversal symmetry and opens a gap below it. The electrons in the segment between the magnets still have spin, since spin-up moves right and spin-down moves left.

- [x] For each direction of motion only one spin is present, so counting channels gives a single spinless wire.

    This is true. On a helical edge spin-up moves in one direction and spin-down in the other. Each direction has one channel, as in the spinless chain that [(5.19)](#eq-5-19) needs.

- [ ] Spin-up and spin-down electrons move in both directions.

    This is false. That is an ordinary spinful wire with two channels in each direction. Pairing it with an $s$-wave superconductor gives a trivial gap and no Majoranas, so it is not the helical edge.
:::

::: notebookbox
**Notebook check-in:** [`session5.ipynb`](https://github.com/joselado/Advanced_Quantum_Materials_2027/blob/main/jupyter-notebooks/session5.ipynb), "Artificial topological superconductivity" (Challenge), "Edge states of an artificial topological superconductor" (Challenge), and "Topological phase transition as a function of the exchange field"

Build the construction described above, with the QSH edge, the magnets and superconductivity, and check that zero modes localized at the ends emerge as you change the strength of the exchange field. Look at how the system crosses the boundary between the topological and the trivial phase, of the type of [(5.22)](#eq-5-22), as the magnetic gap changes.
:::

::: {.tryit notebook="session5.ipynb" cell="Topological phase transition as a function of the exchange field"}
In the cell, the loop runs over `J` from 0 to 0.6 with `add_swave(0.3)`. Follow the lowest energy near $\mathbf k=0$. It starts at $|\Delta|=0.3$, closes close to `J=0.42` and opens again. Above this value the state is the artificial topological superconductor.
:::

::: comesback
- In Section [5.19](#sec-5-19) the Majorana zero modes at the two ends of such a segment are the building blocks of a topological qubit.
- In Section [6.3](#sec-6-3) we see where the exchange field of a magnet comes from, as the mean-field magnetization of the Hubbard model.
- In Section [9.8](#sec-9-8) a vacancy tells a topological superconductor apart from a trivial one, when the two bulk spectra look the same.
:::
