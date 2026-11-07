## Numerical check of the Landau levels and edge states on the lattice {#sec-4-11 number="4.11"}

Let us say how the continuum results of Sections [4.9](#sec-4-9) and [4.10](#sec-4-10) are connected to tight-binding lattices. This is where the edge states of Section [4.5](#sec-4-5) first appear together with the bulk Landau levels in a single calculation. We take a ribbon of a square lattice with a finite width. The band bottom of this lattice is parabolic, so it plays the role of the Schrödinger 2DEG. We add a uniform orbital field with the Peierls substitution [(4.4)](#eq-4-4). We put the chemical potential near the bottom of the band, so that the lattice model describes a dilute electron gas that is almost free. The band structure that we obtain shows what the continuum calculation predicted. There is a set of flat bulk bands, the Landau levels, together with dispersive edge bands. One branch is localized at each edge of the ribbon, and the two propagate in opposite directions, which is the chiral pair of Section [4.5](#sec-4-5). Then we repeat the same construction on an armchair ribbon of the honeycomb lattice, where the low-energy physics is a real Dirac equation at the $K$ and $K'$ points. We obtain the $\sqrt{B}$ Landau levels of Section [4.10](#sec-4-10), together with their own chiral edge states. The notebook box of Section [4.10](#sec-4-10) asks you to build both ribbons yourself, for example with a width of 30 sites.

![The spectrum of the quantum Hall ribbon, as the numerical check of the continuum result. This panel is computed in the continuum with hard walls. The flat bulk levels are the equally spaced Landau levels of Section [4.9](#sec-4-9). The branches that bend up near the walls and cross the chemical potential are the edge states of Section [4.5](#sec-4-5). The ribbon of the notebook gives the same picture on the lattice.](figures/s04f01_ribbon.svg){panel="a" alt="Flat Landau levels of a ribbon with the edge branches that bend up and cross the gap."}

![The two lattice calculations of this section, a ribbon of the square lattice and an armchair ribbon of the honeycomb lattice, both in the Landau gauge. In (a) the lowest bands of the square lattice are flat in the bulk and sit on the levels $-4t+\hbar\omega_c(n+\tfrac12)$ of [(4.6)](#eq-4-6), the dashed lines. In (b) the levels of the honeycomb ribbon sit at $0$ and $\pm\sqrt{|n|}\,E_1$ of [(4.7)](#eq-4-7), with the level at zero energy that only Dirac electrons have. In both panels the blue branches sit at the left edge and the red ones at the right edge. Every level bends into one branch of each color. In (b) the guiding center decreases when $k_y$ grows, so the left edge is on the right of the panel.](figures/web/session04/lattice_ribbons.svg){#sch:s04:lattice_ribbons alt="Two ribbon spectra against the momentum, with flat grey levels on dashed lines and blue and red branches that bend away at the two ends of each level."}

::: quiz
In the spectrum of the ribbon, a Landau level bends up when its guiding center $x_0=\hbar k_y/B$ gets close to a wall. Why does its energy increase?

- [ ] The wall adds a magnetic field.

    This is false. The flux per plaquette is the same on the last row as in the bulk, since we use the same bond phases. The levels far from the wall stay flat at the same energies.

- [x] The wall cuts the oscillator well, so the state is squeezed and its energy increases.

    This is true. A state with the guiding center at the wall has part of its wavefunction removed. A squeezed wavefunction has a larger kinetic energy, and this is what gives the dispersive edge branches.

    ![The lowest level of the oscillator of one $k_y$ with a hard wall at $x=0$. The energy grows from $0.50$ to $0.73$ and to $1.50$ as the center of the well goes to the wall.](figures/web/session04/wall_squeeze.svg){alt="Three oscillator wells with a wall at the left, the wavefunction squeezed against the wall as the center of the well comes closer, and the energy of the level growing."}

- [ ] The wall changes the cyclotron frequency in the bulk.

    This is false. The flat levels far from the wall stay at $\hbar\omega_c(n+\tfrac12)$ in a ribbon that is wider than a few $\ell_B$. Only the states within about $\ell_B$ of the wall move.

:::

::: {.widget name="landaufan"}
Move the number of plaquettes per flux quantum $q$, so that the flux per plaquette is $\phi=1/q$. The solid curves are the lowest bands of the square lattice, and the dashed lines are the Landau levels $(n+\tfrac12)\hbar\omega_c$ with $\hbar\omega_c=4\pi\phi t$ of Section [4.9](#sec-4-9). For small flux the two agree, and each band is flat in $k_y$, which is the degeneracy of the Landau level. For large flux the lattice bends the levels away from the continuum result.
:::


## Ladder operators and the many-body Landau Hamiltonian {#sec-4-12 number="4.12"}

In Sections [4.9](#sec-4-9) and [4.10](#sec-4-10) we found the structure of a harmonic oscillator by working in a specific gauge. We can show this structure in a way that does not depend on the gauge, if we define the ladder operators directly from the canonical momentum,

$$a = \frac{\ell_B}{\sqrt{2}\hbar}(\pi_x + i\pi_y), \qquad a^\dagger = \frac{\ell_B}{\sqrt{2}\hbar}(\pi_x-i\pi_y),$$

which satisfy the canonical bosonic commutation relation $[a,a^\dagger]=1$. For this we only use $[\pi_x,\pi_y]=i\hbar^2/\ell_B^2$, which depends on the field and not on the gauge. In terms of these operators the *full* quantum Hall Hamiltonian for a Schrödinger electron becomes

$$H = \hbar\omega_c\left(a^\dagger a + \frac{1}{2}\right), \tag{4.8}$$

which is clearly a harmonic oscillator, with eigenvalues that give [(4.6)](#eq-4-6) directly, without any reference to a gauge. This is the clearest way to see that the statement "Landau levels behave like a harmonic oscillator" is not an artifact of the Landau gauge. It is a structural property of any electron in a uniform field.

::: quiz
Why does the form [(4.8)](#eq-4-8), $H=\hbar\omega_c(a^\dagger a+\tfrac12)$, not depend on the gauge?

- [ ] Because the Landau gauge is the only allowed gauge.

    This is false. The symmetric gauge $\mathbf{A}=(-By,Bx,0)/2$ is equally allowed, and we use it in the section on the lowest Landau level. It gives the same oscillator.

- [ ] Because $H$ commutes with $p_y$.

    This is false. In the symmetric gauge $H$ does not commute with $p_y$, since $A_x=-By/2$ depends on $y$. The form $\hbar\omega_c(a^\dagger a+\tfrac12)$ holds there too.

- [x] Because it uses only $[\pi_x,\pi_y]=i\hbar^2/\ell_B^2$, which depends on the field and not on the choice of $\mathbf{A}$.

    This is true. The ladder operators are built from the canonical momentum $\boldsymbol{\pi}$. Their commutator is fixed by $\mathbf{B}$, so the oscillator structure is the same in every gauge.

:::

::: {.tryit notebook="session4.ipynb" cell="Bands in the conventional quantum Hall state"}
Run the cell with `W = 40` and `B = 0.02`. The color gives the position across the ribbon. In the gap between the first two flat levels you should find one branch from each edge. The two have opposite slopes, as in the spectrum above.
:::

::: comesback
- In Section [4.19](#sec-4-19) the notebook follows the same edge branch while the magnetic field is replaced by the Haldane coupling.
- In Section [5.14](#sec-5-14) a ribbon of a chiral p-wave superconductor has edge branches of the same kind, and in Section [6.16](#sec-6-16) a ribbon of a topological magnet has chiral magnon edge modes.
- In Section [4.13](#sec-4-13) the ladder operators of [(4.8)](#eq-4-8) give the wavefunctions of the lowest Landau level.
:::
