## Engineering a topological superconductor from a quantum spin Hall insulator {#sec-5-18 number="5.18"}

Chiral and p-wave superconductors of the kind we need are rare in nature, so in practice they are usually *engineered* and not found. One instructive recipe uses directly the quantum spin Hall (QSH) insulator from the topological-band-structure session. We take a QSH insulator, and the concrete material used in the lecture is tungsten ditelluride (WTe$_2$), whose edge has helical modes, meaning that spin-up electrons propagate in one direction and spin-down electrons propagate in the other direction on the same edge. Now we place ordinary ferromagnets on two segments of this edge. A magnet breaks time-reversal symmetry locally, and this opens a gap in the helical edge modes below it. We recall from the topological-band-structure session that the protection of the QSH edge relies on time-reversal symmetry through Kramers degeneracy, so if we break this symmetry locally, the protection is lost there. What remains without a gap is a short isolated segment of helical edge between the two magnetic regions.

This isolated segment only has spin-up electrons moving right and spin-down electrons moving left, with no spin-down electrons moving right and no spin-up electrons moving left. If we count states only by their direction of propagation, this segment is *effectively spinless*, which is the ingredient that the Kitaev-chain construction of section [5.16](#sec-5-16) needs. If we then couple this segment by proximity to an ordinary s-wave superconductor, we reproduce on this effectively spinless one-dimensional system the physics of [(5.19)](#eq-5-19), which is a one-dimensional p-wave superconductor with Majorana zero modes pinned at the two ends of the isolated segment. Figure [5.6](#fig:s05:qsh) shows the whole setup.

![How to build the Kitaev chain from parts that exist. The edge of a quantum spin Hall insulator is helical, which means that on the same edge spin-up electrons move in one direction and spin-down electrons in the other, drawn in a warm and a cold color. A ferromagnet placed on a part of this edge breaks time-reversal symmetry locally and removes the Kramers protection there, which opens a gap in the edge below it, where the channels are drawn faded. With two ferromagnets, one short helical segment survives between them. This segment has only one direction of propagation for each spin, so if we count channels it is a *spinless* one-dimensional wire. This is the ingredient that [(5.19)](#eq-5-19) needs, and nature does not give it to us directly. Coupling it by proximity to an ordinary $s$-wave superconductor gives the pairing, and the result is a one-dimensional $p$-wave superconductor with a Majorana zero mode at each end of the segment, which means at the two ferromagnet-superconductor interfaces. Note what was *not* needed. No unconventional superconductor appears in the recipe, only an $s$-wave one, a magnet and a topological insulator.](figures/s05f06_qsh.svg){#fig:s05:qsh number="5.6"}

::: quiz
The segment of helical edge between the two magnets is called effectively spinless. Why?

- [ ] The magnets remove the spin of the electrons.
- [x] For each direction of motion only one spin is present, so counting channels gives a single spinless wire.
- [ ] Spin-up and spin-down electrons move in both directions.
- [ ] The superconductor removes the spin by pairing.

On a helical edge spin-up moves in one direction and spin-down in the other. Each direction carries one spin, which is the channel count of the spinless chain that [(5.19)](#eq-5-19) needs.
:::

::: notebookbox
**Notebook check-in:** [`session5.ipynb`](https://github.com/joselado/Advanced_Quantum_Materials_2027/blob/main/jupyter-notebooks/session5.ipynb), "Artificial topological superconductivity" (Challenge), "Edge states of an artificial topological superconductor" (Challenge), and "Topological phase transition as a function of the exchange field"

Build the construction described above, with the QSH edge, the magnets and superconductivity, and check that zero modes localized at the ends emerge as you change the strength of the exchange field. Look at how the system crosses the boundary between the topological and the trivial phase, of the type of [(5.22)](#eq-5-22), as the magnetic gap changes.
:::

::: {.tryit notebook="session5.ipynb" cell="Topological phase transition as a function of the exchange field"}
In the cell, the loop runs over `J` from 0 to 0.6 with `add_swave(0.3)`. Follow the lowest energy near $\mathbf k=0$. It starts at $|\Delta|=0.3$, closes close to `J=0.42` and opens again. Above this value the state is the artificial topological superconductor.
:::
