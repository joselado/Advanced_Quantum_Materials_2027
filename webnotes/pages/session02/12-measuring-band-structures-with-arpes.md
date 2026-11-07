## Measuring band structures with ARPES {#sec-2-12 number="2.12"}

Once we have all this formalism, a natural question is whether any of it can be observed. The energy eigenvalue $E(\mathbf{k})$ is clearly physical, but the quasi-momentum $\mathbf{k}$ itself was introduced as a symmetry eigenvalue in Section [2.6](#sec-2-6). So we ask whether we can measure it directly, and whether we can measure the *relation* between the two.

The answer is yes, with **angle-resolved photoemission spectroscopy (ARPES)**. The idea is simple in principle. We send photons of known energy and momentum onto a material, and each photon can remove an electron from the material completely, which is the photoelectric effect. Conservation of momentum and energy relates the momentum and kinetic energy of the electron, which are both measured directly outside the material, to its momentum and energy when it was still inside. So when we scan the emission angle and the kinetic energy of the emitted electrons, we map $E(\mathbf{k})$ directly. This is how the band structure and the Fermi surface of graphene are measured in practice, and the measured Dirac cone agrees well with the tight-binding derivation of Section [2.11](#sec-2-11).

The component of the momentum along the surface does not change when the electron leaves the material, so $\hbar k_\parallel=\sqrt{2mE_\text{kin}}\,\sin\theta$ for an emission angle $\theta$. [](#sch:s02:arpes_geometry) shows the geometry and this relation.

![The geometry of ARPES. On the left, a photon removes an electron, which leaves at the angle $\theta$ from the normal with the kinetic energy $E_\text{kin}$, and the momentum $k_\parallel$ along the surface is kept. On the right, $k_\parallel$ against $\theta$ for $E_\text{kin}=20$ eV, with $\hbar^2/2m=3.81$ eV\,\AA$^2$. The angles $10^\circ$ and $20^\circ$ give $4.0$ and $7.8$ nm$^{-1}$.](figures/web/session02/arpes_geometry.svg){#sch:s02:arpes_geometry alt="A photon hitting a material and an electron leaving at an angle theta from the normal, and a curve of the parallel momentum against the angle."}

![The Dirac cone of graphene, one panel shown again. This cone is the band structure that ARPES maps, since the experiment gives the energy and the momentum of the electrons inside the material.](figures/s02f04_dirac.svg){panel="c" alt="A hexagonal Brillouin zone with a Dirac cone at two of its corners."}

::: quiz
In ARPES we measure the kinetic energy and the emission angle of the electrons that leave the material. What do we obtain from them?

- [x] The energy and the quasi-momentum of the electron inside the material, which gives $E(\mathbf k)$.

    This is true. Conservation of energy and of the momentum along the surface relates the measured values to the ones inside. Scanning the angle and the energy then maps the band structure directly.

- [ ] Only the density of states, since the angle is averaged out.

    This is false. The angle is not averaged out. For electrons of $20$ eV, an angle of $10^\circ$ gives $k_\parallel\approx 4.0\ \text{nm}^{-1}$ and $20^\circ$ gives $7.8\ \text{nm}^{-1}$, so each angle is a different momentum.

- [ ] The hopping $t$ only, with no information on the momentum.

    This is false. For the chain $\epsilon=-2t\cos(ka)$ the electrons seen at $k=0$ have energy $-2t$, and at $ka=\pi/2$ they have $0$. The energy depends on the angle, so we get the momentum too.

The angle gives the momentum along the surface, and the energy gives the band.
:::

## Closing summary {#sec-2-13 number="2.13"}

From Session 1 this session used the single-particle part of the Hamiltonian [(1.5)](#eq-1-5), the hopping of second quantization, with the interactions left aside or already treated in mean field as in Section [1.12](#sec-1-12). With it we saw the following.

- **Symmetry as a tool to simplify.** When the ground state shares the symmetry of the Hamiltonian, we can use a symmetry operator that commutes with it, $[H,S]=0$ in [(2.3)](#eq-2-3). We then find the eigenbasis of $H$ by finding the eigenbasis of $S$ instead, as we did for rings of three and five sites in Section [2.4](#sec-2-4).

- **Bloch's theorem** is this same idea applied to translational symmetry on an infinite lattice. Eigenstates have a definite phase $\varphi$ under translation, which is the quasi-momentum of [(2.10)](#eq-2-10). This turns one infinite-dimensional diagonalization into a continuous family of finite ones, given by the **Bloch Hamiltonian** $H(\varphi)$.

- We derived the band structure of the one-dimensional chain explicitly, $\epsilon_\varphi=-2t\cos\varphi$ in [(2.8)](#eq-2-8). We generalized the same method to second-neighbor hopping [(2.9)](#eq-2-9), to several orbitals per unit cell with the matrix Bloch Hamiltonian $H(\varphi)=t+\gamma e^{i\varphi}+\gamma^\dagger e^{-i\varphi}$ in [(2.12)](#eq-2-12) and [(2.13)](#eq-2-13), and to higher spatial dimensions, [(2.14)](#eq-2-14) and [(2.15)](#eq-2-15).

- A dispersion $E(\mathbf{k})$ directly determines the measurable properties of a material, which are the density of states [(2.16)](#eq-2-16), the group velocity [(2.17)](#eq-2-17), the effective mass [(2.18)](#eq-2-18) and the Fermi surface. Every real dispersion is built locally from three types, which are parabolic, Dirac and flat.

- The **Dirac cone** of the honeycomb lattice of graphene, $H(\mathbf{q})\approx\hbar v_F(q_x\sigma_x+
    q_y\sigma_y)$ with $E_\pm=\pm\hbar v_F|\mathbf{q}|$ in [(2.20)](#eq-2-20) and [(2.21)](#eq-2-21), is the most important example of this session. We derived it directly from the vanishing of the off-diagonal Bloch Hamiltonian [(2.19)](#eq-2-19) at the points $K,K'$. The Lieb and kagome lattices realize flat bands with interference in real space, and with no fine-tuning.

- All of this band-structure method generalizes directly to phonons, magnons and Bogoliubov-de Gennes quasiparticles, and not only to electrons. It is tested against real materials in experiments with ARPES.

The spectra of periodic systems are computed with band-structure theory, by choosing the common eigenbasis of the symmetry operator and the Hamiltonian. The dispersion relation $E(\mathbf{k})$ alone then determines many of the electronic properties of a material, before interactions are included again.

::: quiz
A unit cell has four orbitals. What is the size of $H(\varphi)$, and how many bands do we get?

- [x] A $4\times 4$ matrix, and four bands.

    This is true. The Bloch Hamiltonian has one row and one column for every orbital of the cell. At each $\varphi$ it has four eigenvalues, and they form the four bands.

- [ ] A $2\times 2$ matrix, and two bands.

    This is false. A $2\times 2$ matrix describes a cell with two orbitals, such as the chain of [(2.13)](#eq-2-13). With four orbitals, the rows of $H(\varphi)$ run over four orbitals.

- [ ] A $4\times 4$ matrix, and one band.

    This is false. Take the uniform chain with a cell of four sites. At $\varphi=0$ the four eigenvalues are $-2t$, $0$, $0$ and $2t$, so there are four bands and not one.

The size of the Bloch Hamiltonian is the number of orbitals in the cell.
:::

::: comesback
- In Session 3 the Dirac cone of Section [2.11](#sec-2-11) is gapped, which gives the Chern insulator of Section [3.10](#sec-3-10). The two-orbital chain of [(2.13)](#eq-2-13) becomes the SSH model of Section [3.9](#sec-3-9).
- The Bloch Hamiltonian is the object whose Berry curvature gives the Chern number in Section [3.5](#sec-3-5).
- The flat bands of this session lead to the Landau levels of Session 4, which are flat bands with Chern number one in Section [4.4](#sec-4-4).
- The density of states at the Fermi level decides the Stoner criterion of Section [6.6](#sec-6-6), and nesting drives the instabilities of Section [9.4b](#sec-9-4b).
- In Section [10.7](#sec-10-7) an ARPES spectrum is one of the observables from which a Hamiltonian is learned.
:::
