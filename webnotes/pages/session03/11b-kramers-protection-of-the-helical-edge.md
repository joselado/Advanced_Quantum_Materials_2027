## Kramers protection of the helical edge {#sec-3-11b number="3.11b"}

So far we have treated the two spin sectors as independent. There is a subtle point that we should state precisely. If spin were perfectly conserved, we could speak separately of the Chern number for spin-up and the Chern number for spin-down. Real materials have terms that mix spin, and spin-orbit coupling itself mixes spin to some degree, so one may worry that these terms could smoothly remove the protection of the helical edge states. They cannot, as long as time-reversal symmetry survives, and the reason is Kramers' theorem. For spin-1/2 electrons the time-reversal operator squares to $-1$, which forces an exact twofold degeneracy at every momentum that is its own time-reversal partner. These are the time-reversal-invariant momenta, which are $\Gamma$ and $X$ in this setup. This degeneracy exists with or without spin-mixing terms, so the crossing of the edge states at these momenta cannot be gapped by any perturbation that respects time-reversal symmetry, but only by one that breaks it. This protection mechanism is different from, and stronger than, what the picture of two independent Chern insulators would suggest by itself. Figure [3.6](#fig:s03:helical) compares the chiral and helical edge dispersions and shows what a term that breaks time-reversal symmetry does to the protected crossing.

![Schematic edge dispersions for the two topological classes of Section [3.8](#sec-3-8). The grey slabs are the bulk bands, and the branches that cross the bulk gap are the edge states, plotted as a function of the momentum along the edge. (a) A Chern insulator has a single branch per edge. At any energy in the gap there is one state and it moves in one direction, so a scatterer has no state to send it back into. (b) A quantum spin Hall insulator has two branches, one for each spin, drawn in a warm and a cold color, which propagate in opposite directions on the *same* edge, and this is what **helical** means. The total Chern number vanishes, but the spin Chern number does not [(3.9)](#eq-3-9). (c) The crossing is not protected because the two spin sectors are separately conserved. It is protected by Kramers' theorem, since the crossing is at a time-reversal-invariant momentum, where a twofold degeneracy is guaranteed for spin-$1/2$ electrons for any perturbation that respects time reversal. Disorder that preserves time reversal can therefore deform the branches but cannot gap them. Only a perturbation that breaks time reversal opens the gap $\Delta$ in (c), and then the protection is lost.](figures/s03f06_helical.svg){#fig:s03:helical number="3.6"}

::: quiz
Which perturbation can open a gap at the crossing of the helical edge states of a wide ribbon?

- [ ] A spin-mixing term such as Rashba spin-orbit coupling.

    This is false. Rashba coupling mixes the spins but keeps time-reversal symmetry. The crossing is at $k=0$, a time-reversal invariant momentum, so Kramers theorem keeps the two states degenerate there for any strength of the coupling.

- [x] A magnetic field or a magnetic impurity that breaks time-reversal symmetry.

    This is true. Kramers theorem protects the crossing as long as time-reversal symmetry holds. A term that breaks it can open the gap $\Delta$ of panel (c).

- [ ] A random potential that is the same for both spins.

    This is false. A spin-independent potential $V$ gives $\langle -k,\downarrow|V|k,\uparrow\rangle=0$, so it cannot backscatter between the two partners. The crossing stays closed for any strength of the disorder.

:::

Disorder makes this difference concrete. Helical edge states survive disorder that preserves time-reversal symmetry, since the band structure changes but the gapless crossing at the edge remains. On the other hand, disorder that breaks time-reversal symmetry opens a real gap in the edge spectrum and removes the protection completely.

::: notebookbox
**Notebook check-in:** [`session3.ipynb`](https://github.com/joselado/Advanced_Quantum_Materials_2027/blob/main/jupyter-notebooks/session3.ipynb), "The quantum spin Hall state" (Core), "The robustness of the quantum spin Hall state" (Core), "Topological invariant of the quantum spin Hall state", and "Finite size effects in topological systems" (Challenge, using exchange coupling plus Rashba spin-orbit coupling)

Build the model with two copies of a Chern insulator and identify the helical pair of edge states by their spin projection and their propagation direction, which is the pattern in [(3.9)](#eq-3-9). Then add disorder that preserves or breaks time-reversal symmetry, and check that the gap only opens in the second case. The note "in the lab" in this notebook section points to the measurement in 1T$'$-WTe$_2$ that we mentioned above.
:::

::: {.tryit notebook="session3.ipynb" cell="The robustness of the quantum spin Hall state"}
Run the three panels, without disorder, with non-magnetic disorder and with magnetic disorder. Change the amplitude `1.` in `hd.add_onsite(lambda r: 1.*(np.random.random()-0.5))` to `1.5`. The crossing at the center stays gapless. In the third panel the amplitude `1.` of `add_exchange` opens a gap at zero energy.
:::
