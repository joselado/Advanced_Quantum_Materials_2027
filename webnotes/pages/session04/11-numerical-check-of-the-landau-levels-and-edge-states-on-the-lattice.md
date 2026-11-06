## Numerical check of the Landau levels and edge states on the lattice {#sec-4-11 number="4.11"}

Let us say explicitly how the continuum results of Sections [4.9](#sec-4-9) and [4.10](#sec-4-10) are connected to tight-binding lattices, since this is where the edge states of Section [4.5](#sec-4-5) first appear together with the bulk Landau levels in a single calculation. We take a ribbon of a square lattice with a finite width. The band bottom of this lattice is parabolic, so it plays the role of the Schrödinger 2DEG. We add a uniform orbital field with the Peierls substitution [(4.4)](#eq-4-4), and we put the chemical potential near the bottom of the band, so that the lattice model effectively describes a dilute electron gas that is almost free. The band structure that we obtain shows what the continuum calculation predicted. There is a set of flat bulk bands, the Landau levels, together with dispersive edge bands, with one branch localized at each edge of the ribbon and propagating in opposite directions, which is the chiral pair described in Section [4.5](#sec-4-5). When we repeat the same construction on an armchair ribbon of the honeycomb lattice, where the low-energy physics is a real Dirac equation at the $K$ and $K'$ points, we obtain the $\sqrt{B}$ Landau levels of Section [4.10](#sec-4-10) together with their own chiral edge states. The band structures of both ribbons, shown for a width of 30 in the slides, are figures that exist only in the slides, in the sense that the transcript describes them only in a qualitative way. The plots are the visual evidence, and the notebook box above asks you to build the same ribbons yourself.

![The spectrum of the quantum Hall ribbon, as the numerical check of the continuum result. This panel is computed in the continuum with hard walls. The flat bulk levels are the equally spaced Landau levels of Section [4.9](#sec-4-9). The branches that bend up near the walls and cross the chemical potential are the edge states of Section [4.5](#sec-4-5). The ribbon of the notebook gives the same picture on the lattice.](figures/s04f01_ribbon.svg){panel="a" alt="Flat Landau levels of a ribbon with the edge branches that bend up and cross the gap."}

::: quiz
In the spectrum of the ribbon, a Landau level bends up when its guiding center $x_0=\hbar k_y/B$ gets close to a wall. Why does its energy increase?

- [ ] The wall adds a magnetic field.
- [x] The wall cuts the oscillator well, so the state is squeezed and its energy increases.
- [ ] The wall changes the cyclotron frequency in the bulk.
- [ ] The wall removes the degeneracy of the Landau level.

A state with the guiding center at the wall has part of its wavefunction removed. A squeezed wavefunction has a larger kinetic energy, and this is what gives the dispersive edge branches.
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

- [ ] Because $\mathbf{B}$ is uniform.
- [ ] Because the Landau gauge is the only allowed gauge.
- [x] Because it uses only $[\pi_x,\pi_y]=i\hbar^2/\ell_B^2$, which depends on the field and not on the choice of $\mathbf{A}$.
- [ ] Because $H$ commutes with $p_y$.

The ladder operators are built from the canonical momentum $\boldsymbol{\pi}$. Their commutator is fixed by $\mathbf{B}$, so the oscillator structure is the same in every gauge.
:::

::: {.tryit notebook="session4.ipynb" cell="Bands in the conventional quantum Hall state"}
Run the cell with `W = 40` and `B = 0.02`. The color gives the position across the ribbon. In the gap between the first two flat levels you should find one branch from each edge. The two have opposite slopes, as in the spectrum above.
:::
