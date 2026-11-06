## Topological zero modes with periodic and open boundaries {#sec-5-17 number="5.17"}

If we diagonalize [(5.19)](#eq-5-19) on a *periodic* chain, we obtain a fully gapped spectrum, with a superconducting gap set by $\Delta$ and a nontrivial topological invariant of the bulk. This is the same kind of $\mathbb{Z}_2$ or winding invariant that classified the two phases of the SSH model through the Zak phase in the topological-band-structure session, now computed from the BdG bands instead of an ordinary Bloch Hamiltonian. On an *open* chain, for example with $N=100$ sites and the two ends disconnected, the bulk spectrum keeps essentially the same gap, but two extra states appear, pinned exactly at zero energy and localized at the left end and at the right end of the chain. These are the unpaired Majoranas $\gamma_1$ and $\gamma_{2N}$ from [(5.21)](#eq-5-21), which we now see as real mid-gap states of the open chain.

These zero modes are very robust. When we move away from the fine-tuned point, with $\Delta \ne t$ and finite $\mu$, the zero modes survive as long as we stay in the same topological phase. The standard criterion for the general Kitaev chain [(5.19)](#eq-5-19) with $\Delta \ne 0$ is

$$|\mu| < 2t \quad \Longrightarrow \quad \text{topological phase (unpaired end Majoranas)}, \qquad |\mu| > 2t \quad \Longrightarrow \quad \text{trivial phase.} \tag{5.22}$$

In the trivial phase, a large chemical potential effectively fixes each site to be either empty or occupied in the fermionic language, since the chain is spinless, and the two Majoranas that form the electron of each site combine again locally into an ordinary confined fermion, so nothing is left to deconfine. In the topological phase, on the other hand, p-wave pairing dominates over the trivial onsite physics, and the two Majoranas at each site pair with the Majoranas of the neighboring sites instead of with each other, which leaves the two end Majoranas without any partner. This is the same contrast between the dimerized strong-coupling limit and the atomic weak-coupling limit that distinguished the topological and trivial phases of the SSH model. The Kitaev chain reproduces it because, as we saw in section [5.16](#sec-5-16), it is the SSH model with new labels.

![The lowest levels of an open Kitaev chain with $N=60$ sites and $\Delta=0.7t$, as a function of $\mu$. For $|\mu|<2t$ a pair of levels sits at zero energy, which belongs to the two end Majoranas, and the bulk levels stay above a gap. At $|\mu|=2t$ the bulk gap closes, as in [(5.22)](#eq-5-22).](figures/web/session05/kitaev_spectrum.svg){#sch:s05:kitaev_spectrum alt="Lowest energy levels of an open Kitaev chain against the chemical potential. A level stays at zero between minus 2t and 2t, and outside this window all levels rise away from zero."}

::: quiz
An open Kitaev chain with $\Delta=0.5t$ and $\mu=t$ has two Majoranas at its ends. We change the chemical potential to $\mu=-t$. What happens to them?

- [x] They stay, since [(5.22)](#eq-5-22) depends only on $|\mu|$.
- [ ] They disappear, since the sign of $\mu$ matters.
- [ ] They move into the bulk.
- [ ] They double, since the band bottom changes.

In both cases $|\mu|=t<2t$, so the chain stays in the topological phase. The end Majoranas remain, and only the position of the bulk band moves.
:::

::: quiz
A Kitaev chain with $N=8$ sites is in the topological phase. Are its two end modes at exactly zero energy?

- [ ] Yes, since the topological phase protects them for any $N$.
- [x] No, they sit at a small energy that decreases exponentially with $N$.
- [ ] No, they sit at the energy of the bulk gap.
- [ ] Yes, but only at $\Delta=t$.

The end modes have a finite localization length. For a short chain their wave functions overlap, and they hybridize into one ordinary level, split from zero by an energy of order $e^{-N/\xi}$.
:::

::: {.tryit notebook="session5.ipynb" cell="Emergence of Majorana modes as a function of the size of the superconductor"}
In the cell, the line `mu = 0.3` sets the chemical potential. With `mu = 1.0` the two states near zero energy stay. With `mu = 2.5` they disappear, and for $L=40$ the lowest energy is about 0.5, in line with [(5.22)](#eq-5-22).
:::

::: {.widget name="kitaevbdg"}
Move the chemical potential $\mu$ of an open Kitaev chain with $t=\Delta=1$ and 30 sites. For $|\mu|<2t$ two levels sit at zero energy inside the gap, and their weight is at the two ends of the chain. For $|\mu|>2t$ no level stays at zero, and the lowest state is spread over the whole chain. At $|\mu|=2t$ the gap closes, which is the topological transition of [(5.22)](#eq-5-22).
:::

