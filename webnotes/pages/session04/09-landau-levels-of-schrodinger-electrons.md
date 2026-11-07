## Landau levels of Schrödinger electrons {#sec-4-9 number="4.9"}

Let us now solve for the spectrum, and let us start with the simplest case. These are free electrons with no lattice and no potential apart from the field itself, and with dispersion $p^2/2m$ before we switch on the field. With minimal coupling and the Landau gauge $\mathbf{A}=(0,Bx,0)$ we have

$$H = \frac{\pi_x^2+\pi_y^2}{2m} = \frac{p_x^2}{2m} + \frac{(p_y-Bx)^2}{2m}. \tag{4.5}$$

We take the charge of the carriers to be $+e$ in [(4.3)](#eq-4-3) and we set $e=1$ in all this session, while we keep $\hbar$ explicit. This is a choice of convention, but it has consequences, since it fixes $[\pi_x,\pi_y]=+i\hbar^2/\ell_B^2$. The ladder operators of Section [4.10](#sec-4-10) and the holomorphic wavefunctions of Section [4.13](#sec-4-13) are built on this convention. For an electron, which has charge $-e$, every cyclotron orbit and every edge current below goes around in the other direction, and nothing else changes.

Since $\mathbf{A}$ does not depend on $y$, we have $[H,p_y]=0$, so we can look for eigenstates of the form $\psi(x,y) = e^{ik_y y}\phi(x)$. With the replacement $p_y\to\hbar k_y$, the Hamiltonian [(4.5)](#eq-4-5) becomes a one-dimensional problem in $x$,

$$H\phi(x) = \left[\frac{p_x^2}{2m} + \frac{B^2}{2m}\Big(x-\frac{\hbar k_y}{B}\Big)^2\right]\phi(x),$$

which is exactly the Hamiltonian of a quantum harmonic oscillator centered at $x_0 = \hbar
k_y/B$, with frequency $\omega_c = B/m$, the cyclotron frequency. The shift of the center is removed with the change of variable $x\to x-x_0$. When we solve it with the same ladder operators as the ordinary harmonic oscillator we obtain

$$E_n = \hbar\omega_c\left(n+\frac{1}{2}\right), \qquad n=0,1,2,\dots, \tag{4.6}$$

which does not depend on $k_y$ at all. Every value of $k_y$, or in other words every choice of the guiding center $x_0$, gives the same energy. This is the reason why the Landau levels are flat bands, and why each of them has a macroscopic degeneracy that is proportional to the area of the sample. Figure [4.3](#fig:s04:guidingcenter) shows this mechanism directly, with the same well placed at different positions, and with the degeneracy counted as one orbital for each flux quantum through the sample. When we put in the real physical constants for a field typical of GaAs, we obtain the millielectronvolt scale that we gave in Section [4.1](#sec-4-1).

![Why the Landau levels are flat. (a) In the Landau gauge each $k_y$ reduces [(4.5)](#eq-4-5) to a one-dimensional harmonic oscillator in $x$, which is the same in every respect except that it is centred on the guiding centre $x_0=\hbar k_y/B$. When $k_y$ increases, the whole well moves to the right without changing its curvature. Every well therefore has the same ladder $E_n=\hbar\omega_c(n+\tfrac 12)$, drawn here as the horizontal guides, and the ground-state wavepacket of each well, the red bump, has the same shape at a different position. (b) As a function of $k_y$, this is a set of bands with no dispersion at all, and the three balls are the three values of $k_y$ of (a). The flatness is not an artefact of the gauge. It means that the energy does not depend on the position of the electron in the sample, and this is also the origin of the very large degeneracy of the Landau levels.](figures/s04f03_guidingcenter.svg){#fig:s04:guidingcenter number="4.3"}

::: quiz
The energy [(4.6)](#eq-4-6) does not depend on $k_y$. What does $k_y$ fix instead?

- [ ] The cyclotron frequency.

    This is false. The frequency $\omega_c=B/m$ depends on the field and the mass. Two states with $k_y=0$ and $k_y=5/\ell_B$ have the same $\omega_c$.

- [ ] The Landau level index $n$.

    This is false. For a fixed $n$ all the values of $k_y$ give the same energy, which is the degeneracy of the level. Then $k_y$ cannot decide $n$.

- [x] The position $x_0=\hbar k_y/B$ of the center of the oscillator.

    This is true. A change of $k_y$ shifts the oscillator well along $x$ and does not change its curvature. The same ladder of levels is then found at every position.

:::

::: quiz
A sample has the area $A$. How does the number of states in one Landau level depend on $A$ and $B$?

- [ ] It is proportional to $A$ and independent of $B$.

    This is false. For $A=1\,\mu\mathrm{m}^2$ there are about 242 flux quanta at 1 T and about 484 at 2 T. The number of states doubles when the field doubles.

- [ ] It is proportional to $A/B$.

    This is false. This law gives half of the states when the field doubles, about 121 instead of 484 for the sample of $1\,\mu\mathrm{m}^2$ going from 1 T to 2 T. A stronger field gives more flux quanta.

- [x] It is proportional to $AB$, which is one orbital for each flux quantum through the sample.

    This is true. A stronger field gives more flux quanta through the same area, and every flux quantum adds one orbital. This is why the degeneracy grows with the area and with the field.

:::

::: {.tryit notebook="session4.ipynb" cell="Magnetic field dependence of Landau levels"}
Run the cell, which shows the density of states of the bulk for the three fields. Measure the distance between the first two peaks in each panel. It grows roughly in proportion to `B`, as the cyclotron energy of [(4.6)](#eq-4-6) does.
:::

::: comesback
- In Section [4.12](#sec-4-12) the same oscillator appears without any choice of gauge, as [(4.8)](#eq-4-8).
- In Section [4.16](#sec-4-16) the large degeneracy of a Landau level, one orbital per flux quantum, is what lets a fractional filling form the Laughlin state.
- In Section [6.6](#sec-6-6) a flat band, with its large density of states, makes the Stoner criterion easy to satisfy.
:::
