## Topological zero modes with periodic and open boundaries {#sec-5-17 number="5.17"}

If we diagonalize [(5.19)](#eq-5-19) on a *periodic* chain, we obtain a fully gapped spectrum, with a superconducting gap set by $\Delta$ and a nontrivial topological invariant of the bulk. This is the same kind of $\mathbb{Z}_2$ or winding invariant that classified the two phases of the SSH model through the Zak phase [(3.6)](#eq-3-6) in Session 3. Here it is computed from the BdG bands instead of an ordinary Bloch Hamiltonian. On an *open* chain, for example with $N=100$ sites and the two ends disconnected, the bulk spectrum keeps essentially the same gap. However, two extra states appear, at zero energy and localized at the left end and at the right end of the chain. These are the unpaired Majoranas $\gamma_1$ and $\gamma_{2N}$ from [(5.21)](#eq-5-21), which we now see as real mid-gap states of the open chain. Schematic [](#sch:s05:zero_mode_profile) shows where the lowest state sits. In the topological phase its weight is at the two ends, and in the trivial phase it is spread over the chain.

![The weight of the lowest state of an open Kitaev chain with $N=40$, $\Delta=0.5t$ and two values of $\mu$. (a) For $\mu=t$ the weight is at the two ends and decays into the bulk. (b) For $\mu=2.5t$ the state is spread over the chain, and its energy is $0.51t$.](figures/web/session05/zero_mode_profile.svg){#sch:s05:zero_mode_profile alt="Two bar plots of the weight of the lowest state on each site. In the first the weight is at both ends of the chain, and in the second it is spread over the middle."}

These zero modes are very robust. When we move away from the fine-tuned point, with $\Delta \ne t$ and finite $\mu$, the zero modes survive as long as we stay in the same topological phase. The standard criterion for the general Kitaev chain [(5.19)](#eq-5-19) with $\Delta \ne 0$ is

$$|\mu| < 2t \quad \Longrightarrow \quad \text{topological phase (unpaired end Majoranas)}, \qquad |\mu| > 2t \quad \Longrightarrow \quad \text{trivial phase.} \tag{5.22}$$

In the trivial phase, a large chemical potential fixes each site to be either empty or occupied, since the chain is spinless. The two Majoranas that form the electron of each site then combine again locally into an ordinary confined fermion, so nothing is left to deconfine. In the topological phase, on the other hand, p-wave pairing dominates over the trivial onsite physics. The two Majoranas at each site pair with the Majoranas of the neighboring sites instead of with each other, which leaves the two end Majoranas without any partner. This is the same contrast between the dimerized strong-coupling limit and the atomic weak-coupling limit that distinguished the topological and trivial phases of the SSH model in Section [3.9b](#sec-3-9b). The Kitaev chain reproduces it because, as we saw in Section [5.16](#sec-5-16), it is the SSH model with new labels.

![The lowest levels of an open Kitaev chain with $N=60$ sites and $\Delta=0.7t$, as a function of $\mu$. For $|\mu|<2t$ a pair of levels sits at zero energy, which belongs to the two end Majoranas, and the bulk levels stay above a gap. At $|\mu|=2t$ the bulk gap closes, as in [(5.22)](#eq-5-22).](figures/web/session05/kitaev_spectrum.svg){#sch:s05:kitaev_spectrum alt="Lowest energy levels of an open Kitaev chain against the chemical potential. A level stays at zero between minus 2t and 2t, and outside this window all levels rise away from zero."}

::: quiz
An open Kitaev chain with $\Delta=0.5t$ and $\mu=t$ has two Majoranas at its ends. We change the chemical potential to $\mu=-t$. What happens to them?

- [x] They stay, since [(5.22)](#eq-5-22) depends only on $|\mu|$.

    This is true. In both cases $|\mu|=t<2t$, so the chain stays in the topological phase of [(5.22)](#eq-5-22). The end Majoranas remain, and only the position of the bulk band changes.

- [ ] They disappear, since the sign of $\mu$ matters.

    This is false. The gap of the chain closes only at $|\mu|=2t$, where $k=0$ or $k=\pi$ has $E=0$. Going from $\mu=t$ to $\mu=-t$ never crosses $\pm2t$, so no transition happens.

- [ ] They double, since the band bottom changes.

    This is false. Two Majoranas on the same end can couple, since $i\gamma_1\gamma_1'$ is an allowed term, so they would gap out. A single Kitaev chain has one Majorana per end in any case.
:::

::: quiz
A Kitaev chain with $N=8$ sites, $\Delta=0.5t$ and $\mu=t$ is in the topological phase. Are its two end modes at exactly zero energy?

- [ ] Yes, since the topological phase protects them for any $N$.

    This is false. Take $\Delta=0.5t$ and $\mu=t$ with $N=8$. The BdG spectrum has the lowest level at $E\approx0.011t$ and not at zero. For $N=20$ it falls to $2\times10^{-5}t$.

- [x] No, they sit at a small energy that decreases exponentially with $N$.

    This is true. The end modes have a finite localization length, so for a short chain they overlap and hybridize. For $\Delta=0.5t$ and $\mu=t$ the splitting is $0.011t$ at $N=8$ and $2\times10^{-5}t$ at $N=20$.

    ![The lowest level of the open chain against its length, for $\Delta=0.5t$ and $\mu=t$. It falls roughly exponentially with oscillations, and the first bulk level stays near $0.8t$.](figures/web/session05/majorana_splitting.svg){alt="The lowest energy of a Kitaev chain on a logarithmic scale against the number of sites, falling by many orders of magnitude, and a flat line for the first bulk level."}

- [ ] No, they sit at the energy of the bulk gap.

    This is false. For $\Delta=0.5t$ and $\mu=t$ the bulk gap is $0.82t$, while the end modes of an $N=8$ chain are at $0.011t$. They are inside the gap, close to zero.
:::

::: {.tryit notebook="session5.ipynb" cell="Emergence of Majorana modes as a function of the size of the superconductor"}
In the cell, the line `mu = 0.3` sets the chemical potential. With `mu = 1.0` the two states near zero energy stay. With `mu = 2.5` they disappear, and for $L=40$ the lowest energy is about 0.5, in line with [(5.22)](#eq-5-22).
:::

::: {.widget name="kitaevbdg"}
Move the chemical potential $\mu$ of an open Kitaev chain with $t=\Delta=1$ and 30 sites. For $|\mu|<2t$ two levels sit at zero energy inside the gap, and their weight is at the two ends of the chain. For $|\mu|>2t$ no level stays at zero, and the lowest state is spread over the whole chain. At $|\mu|=2t$ the gap closes, which is the topological transition of [(5.22)](#eq-5-22).
:::

::: comesback
- In Section [5.18](#sec-5-18) a transition of the type of [(5.22)](#eq-5-22) is crossed by changing the exchange field of a magnet on a quantum spin Hall edge.
- In Section [9.8](#sec-9-8) the bulk-boundary correspondence that gives these end modes also gives a bound state at a single vacancy.
- In Section [10.6](#sec-10-6) the Zak phase is one of the topological invariants that are set against local order parameters when phases are classified.
:::
