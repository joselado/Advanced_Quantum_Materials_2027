## Emergent quasiparticles and what the lattice gives us {#sec-1-3 number="1.3"}

Let us now state the puzzle that motivates everything that follows. All this phenomenology is built from the same four ingredients, which are electrons, protons, neutrons and photons, and a single isolated atom shows none of it. In a single atom there is no fractionalization, there are no vortices, no magnons and no spinons. So how can a lattice of identical atoms give rise to so many different kinds of collective behavior? Before we build the formalism to answer this question, it is useful to know what we are looking for. Some of the emergent quasiparticles that we will meet are the following.

- **Phonons.** These are lattice vibrations, and they are the simplest quasiparticle of all, since they exist also in classical physics.

- **Magnons.** These are spin-1 excitations of a magnetically ordered state, which are small precessions of the local moment that carry energy and spin through the material. Note that magnons can propagate also in a Mott insulator, where charge cannot propagate, so a magnetic insulator can still carry spin and heat.

- **Spinons.** These are spin-1/2 excitations without charge that live in quantum magnets, where time-reversal symmetry is *not* broken. In some sense a spinon is only the spin part of an electron, without its charge part, and this is an example of electron fractionalization that is called spin-charge separation.

- **Dirac fermions.** These are electrons with a linear dispersion that look massless. They do not come from interactions but from the geometry of the lattice, as in the honeycomb lattice of graphene.

- **Vortices.** These are topological defects in the phase of a superconductor, and they are dynamical quasiparticles themselves. The same superconducting phase gives rise to flux quantization and to the Josephson effect. These two effects are the basis of some of our most precise measurements of the ratio between Planck's constant and the electron charge.

![The phase of the superconducting order parameter, drawn at each point as an arrow in the complex plane. On the left the phase is the same everywhere. On the right there is one vortex. The amplitude goes to zero at the core, and along the red loop the phase winds by $2\pi$. No smooth change of the arrows can remove this winding, and this is why we call a vortex a topological defect.](figures/web/session01/vortex_phase.svg){#sch:s01:vortex_phase alt="Two square grids of arrows. In the first all arrows point to the right. In the second the arrows turn once around a central point, which is marked by a small circle inside a larger red loop."}

Two more emergent particles belong to this list. The first are Majorana fermions, which we meet in Session 5 in connection with chiral superconductors. The second are anyons, which belong to the fractional quantum Hall effect of Session 4, and we mention them here only so that the name is familiar.

![A magnon and a spinon, shown again from Session 8. A magnon flips one spin of the ordered chain, so the total spin changes by one. A spinon carries only spin one half, and spinons are created in pairs when a singlet breaks.](figures/s08f01_magnon_spinon.svg){alt="A chain of spins with one flipped spin, and a chain of singlet pairs with two unpaired spins."}

::: quiz
Breaking one singlet pair of a quantum magnet leaves two unpaired sites. What is the spin of each one?

- [ ] Zero, since the two spins of the singlet cancel.

    This is false. Breaking a singlet creates a triplet excitation with total spin $1$. Two sites with spin zero would give a total spin of zero, so they cannot account for it.

- [x] One half, which is half of the spin of a magnon.

    This is true. Each unpaired site holds one electron, so its spin is $1/2$. The two of them together give the spin $1$ of the magnon, which is why a spinon is a fraction of a magnon.

- [ ] One, the same as a magnon.

    This is false. A site with one electron has only $S_z=\pm 1/2$, so spin one cannot sit there. Two spinons of spin one would also give a total spin of up to $2$, more than the excitation that we created.

Spinons appear in pairs, since a singlet is broken into two unpaired sites.
:::

::: quiz
Charge cannot propagate in a Mott insulator. Why can a magnetic Mott insulator still carry spin and heat?

- [x] Magnons are excitations of the magnetic order, and they move without any motion of charge.

    This is true. A magnon is a precession wave of the local moments. It carries spin and energy while every electron stays on its site.

- [ ] The electrons of a Mott insulator move freely, but only at high temperature.

    This is false. For $U=10t$, putting a second electron on a site costs $10t$. At a temperature well below this, which is the regime of the question, the electrons stay on their sites, and still the magnons carry spin.

    ![The cost $U$ of a second electron on a site. A hop that puts two electrons on one site pays $U$, and a hop between parallel spins is blocked by the Pauli principle.](figures/s06f02_dimer.svg){panel="a" alt="Two sites with parallel spins and a blocked hop, and two sites with antiparallel spins and an allowed hop that costs the energy U."}

- [ ] The phonons of the lattice carry the spin.

    This is false. Phonons are vibrations of the atoms and they carry no spin. In a Heisenberg model with the atoms fixed there are no phonons at all, and spin still propagates as a magnon.

The magnons need no motion of charge, so they exist in an insulator.
:::

::: comesback
- Magnons are built as fluctuations of the order parameter in Section [6.13](#sec-6-13), and Section [6.15](#sec-6-15) gives their dispersion.
- Spinons come back in Section [8.2](#sec-8-2), and the parton construction of Section [8.8](#sec-8-8) writes them as fermions.
- The Dirac fermions of graphene are derived in Section [2.11](#sec-2-11).
- Flux quantization and the Josephson effect are in Section [5.2](#sec-5-2), Majorana fermions in Section [5.15](#sec-5-15), and anyons in Section [4.18](#sec-4-18).
:::
