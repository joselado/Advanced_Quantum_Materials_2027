## Topological zero modes with periodic and open boundaries {#sec-5-17 number="5.17"}

Do the end Majoranas of the Kitaev chain survive away from $\Delta=t$ and $\mu=0$, and what ends the phase where they exist? We will now see that they survive in the whole window $|\mu|<2t$, which ends where the bulk gap closes. On a finite chain the two end modes are split by an energy that falls exponentially with the length of the chain.

::: {.recall eq="5.19"}
This is the Kitaev chain of Section [5.16](#sec-5-16), a chain of spinless fermions $c_n$ with the hopping $t$, the chemical potential $\mu$ and the pairing $\Delta$ between neighboring sites. At $\Delta=t$ and $\mu=0$ it has a free Majorana at each end.
:::

If we diagonalize [(5.19)](#eq-5-19) on a *periodic* chain with $\Delta\neq0$ and $|\mu|<2t$, we obtain a fully gapped spectrum, with a superconducting gap set by $\Delta$ and $\mu$ and a nontrivial topological invariant of the bulk. This is the same kind of $\mathbb{Z}_2$ or winding invariant that classified the two phases of the SSH model through the Zak phase [(3.6)](#eq-3-6) in Session 3. Here it is computed from the BdG bands instead of an ordinary Bloch Hamiltonian.

On an *open* chain, for example with $N=100$ sites and the two ends disconnected, the bulk spectrum keeps essentially the same gap. However, two extra states appear, at zero energy and localized at the left end and at the right end of the chain. These are the unpaired Majoranas $\gamma_1$ and $\gamma_{2N}$ from [(5.21)](#eq-5-21), which we now see as real mid-gap states of the open chain. [](#sch:s05:zero_mode_profile) shows where the lowest state sits. In the topological phase its weight is at the two ends, and in the trivial phase it is spread over the chain.

![The weight of the lowest state of an open Kitaev chain with $N=40$, $\Delta=0.5t$ and two values of $\mu$, computed from [(5.19)](#eq-5-19) in numpy. The weight on site $n$ is $|u_n|^2+|v_n|^2$, with $u_n$ and $v_n$ the electron and the hole part of the state, and the two panels share the scale. (a) For $\mu=t$ the weight is at the two ends and decays into the bulk. (b) For $\mu=2.5t$ the state is spread over the chain, and its energy is $0.51t$.](figures/web/session05/zero_mode_profile.svg){#sch:s05:zero_mode_profile alt="Two bar plots of the weight of the lowest state on each site. In the first the weight is at both ends of the chain, and in the second it is spread over the middle."}

These zero modes are very robust. When we move away from the fine-tuned point, with $\Delta \ne t$ and finite $\mu$, the zero modes survive as long as we stay in the same topological phase.

::: key
The standard criterion for the general Kitaev chain [(5.19)](#eq-5-19) with $\Delta \ne 0$ is

$$|\mu| < 2t \quad \Longrightarrow \quad \text{topological phase (unpaired end Majoranas)}, \qquad |\mu| > 2t \quad \Longrightarrow \quad \text{trivial phase.} \tag{5.22}$$

The bulk gap closes only at $|\mu|=2t$, at $k=0$ for $\mu=-2t$ and at $k=\pi$ for $\mu=2t$. So for $\Delta>0$ the end Majoranas of the point $\Delta=t$, $\mu=0$ stay in the whole window $|\mu|<2t$. For $\Delta<0$ the same holds with the point $\Delta=-t$, where the free halves are $\gamma_2$ and $\gamma_{2N-1}$.
:::

::: {.steps title="Where the bulk gap of the Kitaev chain closes"}
We start from the bulk energy of the periodic chain. It uses only the modulus of the pairing of [(5.20)](#eq-5-20), $|\Delta(k)|=2|\Delta\sin k|$, and not its sign,

$$E(k)^2=\varepsilon(k)^2+|\Delta(k)|^2=\left(2t\cos k+\mu\right)^2+4\Delta^2\sin^2k.$$

The simplest case is $\Delta=t$ and $\mu=0$ of Section [5.16](#sec-5-16), where $E(k)^2=4t^2(\cos^2k+\sin^2k)=4t^2$, so the bulk is flat at $2t$ and far from zero.

In general $E(k)^2$ is a sum of two squares, so it vanishes only where both vanish. For $\Delta\neq0$ the second square vanishes only at $\sin k=0$, which is $k=0$ or $k=\pi$. At $k=0$ the first square is $(2t+\mu)^2$, which vanishes at $\mu=-2t$, and at $k=\pi$ it is $(\mu-2t)^2$, which vanishes at $\mu=2t$. So the bulk gap closes only at $|\mu|=2t$, for any $\Delta\neq0$.

Inside the window $|\mu|<2t$ we can then go from any point with $\Delta>0$ to $\Delta=t$ and $\mu=0$ without closing the gap. We first move $\mu$ to zero and then $\Delta$ to $t$, and this works as long as $\Delta$ keeps its sign. For $\Delta<0$ we go in the same way to $\Delta=-t$, where the chain is $-it\sum_n\gamma_{2n-1}\gamma_{2n+2}$ and the free halves are $\gamma_2$ and $\gamma_{2N-1}$. Both signs give the same levels, since $c_n\to ic_n$ changes $\Delta$ into $-\Delta$ and leaves the hopping and $\mu$ as they are. The BdG levels come in pairs $\pm E$, so a single end Majorana cannot move away from zero by itself, and the end Majoranas of [(5.21)](#eq-5-21) stay on the way. Outside the window we can go in the same way to a very large $|\mu|$, where each site is empty or full and nothing is left at the ends. At $\Delta=0$ the chain with $|\mu|<2t$ is a metal, with the gap closed at its two Fermi points.
:::

In the trivial phase, a large chemical potential fixes each site to be either empty or occupied, since the chain is spinless. The two Majoranas that form the electron of each site then combine again locally into an ordinary confined fermion, so nothing is left to deconfine. In the topological phase, on the other hand, the hopping dominates over the onsite term, $|\mu|<2t$, and any $\Delta\neq0$ is enough. The two Majoranas at each site pair with the Majoranas of the neighboring sites instead of with each other, which leaves the two end Majoranas without any partner. This is the same contrast between the dimerized strong-coupling limit and the atomic weak-coupling limit that distinguished the topological and trivial phases of the SSH model in Section [3.9b](#sec-3-9b). The Kitaev chain reproduces it because, as we saw in Section [5.16](#sec-5-16), it is the SSH model with new labels.

![The three lowest levels $E\geq0$ of an open Kitaev chain with $N=60$ sites and $\Delta=0.7t$, as a function of $\mu$, computed from [(5.19)](#eq-5-19) in numpy, with $E$ and $\mu$ in units of $t$. For $|\mu|<2t$ a pair of levels sits at zero energy, which belongs to the two end Majoranas, and the bulk levels stay above a gap, with the lowest one at $1.4t$ for $\mu=0$. On 60 sites the pair stays below $0.003t$ up to $|\mu|=1.9t$. At $|\mu|=2t$ the bulk gap of the infinite chain closes, as in [(5.22)](#eq-5-22), and on 60 sites the lowest level is $0.04t$ at $|\mu|=2t$.](figures/web/session05/kitaev_spectrum.svg){#sch:s05:kitaev_spectrum alt="Lowest energy levels of an open Kitaev chain against the chemical potential. A level stays at zero between about minus 1.9t and 1.9t and rises from there, and outside the window from minus 2t to 2t all levels rise away from zero."}

::: lab
The measurement uses InSb nanowires with one normal contact of gold and one superconducting contact of NbTiN. The probe is an electrical measurement on the wire, and gate voltages vary the electron density and define a tunnel barrier between the two contacts. In magnetic fields of order $100$ mT the measurement shows bound, mid-gap states at zero bias voltage. These states stay at zero bias when the field and the gate voltages are changed over considerable ranges. The authors write that their observations support the hypothesis of Majorana fermions in such nanowires. The measurement is in [this article](https://www.science.org/doi/10.1126/science.1222360). In our reading, the nanowire is not the chain [(5.19)](#eq-5-19) itself, but a gate that changes the electron density changes $\mu$. The abstract does not say which of the gates were changed. We then read a level that stays at zero while the gate voltages change as the analog of [(5.22)](#eq-5-22), where the end Majoranas stay in a whole window of $\mu$. In our reading this window is not $|\mu|<2t$, which is the window of the chain [(5.19)](#eq-5-19) with its hopping $t$, and the wire has no such $t$. For a wire the window is set by the magnetic field together with $\mu$, as Section [5.18](#sec-5-18) shows for an edge.
:::

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

    ![The lowest level of the open chain against its length, for $\Delta=0.5t$ and $\mu=t$. It falls roughly exponentially with oscillations, and the first bulk level comes down from $1.02t$ at $N=4$ to $0.83t$ at $N=30$, close to the bulk value $0.82t$.](figures/web/session05/majorana_splitting.svg){alt="The lowest energy of a Kitaev chain on a logarithmic scale against the number of sites, falling by many orders of magnitude, and a nearly flat line close to 1 for the first bulk level."}

- [ ] No, they sit at the energy of the bulk gap.

    This is false. For $\Delta=0.5t$ and $\mu=t$ the smallest bulk energy is $0.82t$, while the end modes of an $N=8$ chain are at $0.011t$. They are inside the gap, close to zero.
:::

::: quiz
Each picture is an open Kitaev chain of 40 sites, with $\Delta=0.5t$. The bars are the weight of its lowest state on each site. Which chain is in the trivial phase?

- [ ] ![Bars of the weight on the sites, high on the first and on the last site and close to zero in between.](figures/web/session05/g5_quiz_profile_mu0.svg)

    This is false. The weight sits on the first and the last few sites, as for a pair of end Majoranas. This chain has $\mu=0$, inside the window $|\mu|<2t$, and its lowest level is below $10^{-9}t$.

- [ ] ![Bars of the weight on the sites, on the first few and on the last few sites and close to zero in between.](figures/web/session05/g5_quiz_profile_mu15.svg)

    This is false. The weight is again on the first and the last few sites. This chain has $\mu=-1.5t$, and the window $|\mu|<2t$ depends only on $|\mu|$, so it is topological too, with its lowest level below $10^{-9}t$.

- [x] ![Low bars of the weight spread over the whole chain, highest in the middle.](figures/web/session05/g5_quiz_profile_mu30.svg)

    This is true. The weight is spread over the middle of the chain, and the eight sites at the two ends hold only $2\%$ of it together. This chain has $\mu=3t$, outside the window $|\mu|<2t$, and its lowest level is a bulk state at $1.01t$.
:::

:::: problem
The bulk energy of the Kitaev chain is $E(k)^2=(2t\cos k+\mu)^2+4\Delta^2\sin^2k$. Find the smallest bulk energy for $\Delta=0.5t$ and $\mu=t$, and the momentum where it sits.

::: solution
With $\Delta=0.5t$ we have $4\Delta^2=t^2$. We write $x=\cos k$ and $\sin^2k=1-x^2$, so that

$$\frac{E^2}{t^2}=(2x+1)^2+1-x^2=3x^2+4x+2.$$

This parabola has its minimum at $x=-2/3$, which is inside the range $-1\le x\le1$ of a cosine. So the smallest energy sits at $\cos k=-2/3$, which is $k=\pm2.30$, and there

$$\frac{E^2}{t^2}=\frac43-\frac83+2=\frac23,\qquad E=\sqrt{2/3}\;t=0.82t.$$

This is the smallest quasiparticle energy, and the two branches $\pm E$ are $1.63t$ apart at this momentum. The first bulk level of an open chain comes down to this value as the chain grows, $0.89t$ at $N=8$ and $0.83t$ at $N=20$, while the end modes of $N=8$ are at $0.011t$. So in a measurement at the end of the chain, the end modes sit far below the energy where the bulk states start.
:::
::::

::: {.tryit notebook="session5.ipynb" cell="Emergence of Majorana modes as a function of the size of the superconductor"}
In the cell, the line `mu = 0.3` sets the chemical potential through `h.add_onsite`, which is $\mu=-0.3$ in [(5.19)](#eq-5-19). With `mu = 1.0` the two states near zero energy stay. With `mu = 2.5` they disappear, and for $L=40$ the lowest energy is about 0.5, in line with [(5.22)](#eq-5-22).
:::

::: {.widget name="kitaevbdg"}
Move the chemical potential $\mu$ of an open Kitaev chain with $t=\Delta=1$ and 30 sites. For $|\mu|<2t$ two levels sit at zero energy inside the gap, and their weight is at the two ends of the chain. On 30 sites this holds away from $|\mu|=2t$, since near it the two end modes overlap and the two levels move away from zero. For $|\mu|>2t$ no level stays at zero, and the lowest state is spread over the whole chain. At $|\mu|=2t$ the gap closes, which is the topological transition of [(5.22)](#eq-5-22).
:::

::: comesback
- In Section [5.18](#sec-5-18) a transition of the type of [(5.22)](#eq-5-22) is crossed by changing the exchange field of a magnet on a quantum spin Hall edge.
- In Section [9.8](#sec-9-8) the bulk-boundary correspondence that gives these end modes also gives a bound state at a single vacancy.
- In Section [10.6](#sec-10-6) the Zak phase is one of the topological invariants that are set against local order parameters when phases are classified.
:::
