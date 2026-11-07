## Landau levels of Dirac electrons {#sec-4-10 number="4.10"}

Now we repeat the same calculation for a Dirac Hamiltonian, $H_0 = v_F(p_x\sigma_x+p_y\sigma_y)$, which is the low-energy effective description of graphene near the $K$ point, from Section [2.11](#sec-2-11). With the same minimal coupling and the same Landau gauge, $\pi_x=p_x$, $\pi_y=p_y-Bx$, the Hamiltonian is now an *off-diagonal* $2\times2$ matrix,

$$H = v_F\begin{pmatrix}0 & \pi_x-i\pi_y\\ \pi_x+i\pi_y & 0\end{pmatrix}.$$

The matrix $H$ is not diagonal and we cannot solve it by inspection, but its square is. We introduce the magnetic length $\ell_B=\sqrt{\hbar/B}$ and the ladder operators $a =
\frac{\ell_B}{\sqrt{2}\hbar}(\pi_x+i\pi_y)$ and $a^\dagger=\frac{\ell_B}{\sqrt{2}\hbar}(\pi_x-i\pi_y)$. Since $[\pi_x,\pi_y]=i\hbar^2/\ell_B^2$, these operators satisfy the ordinary bosonic commutation relation $[a,a^\dagger]=1$. In terms of $a,a^\dagger$ we have

$$H = \frac{\sqrt{2}\hbar v_F}{\ell_B}\begin{pmatrix}0 & a^\dagger\\ a & 0\end{pmatrix}
\quad\Longrightarrow\quad
H^2 = \frac{2\hbar^2v_F^2}{\ell_B^2}\begin{pmatrix}a^\dagger a & 0\\ 0 & aa^\dagger\end{pmatrix}
= \frac{2\hbar^2v_F^2}{\ell_B^2}\begin{pmatrix}N & 0\\ 0 & N+1\end{pmatrix},$$

where $N=a^\dagger a$ is the number operator of the harmonic oscillator. In other words, $H^2$ has the form $p^2+B^2x^2+\text{const}$, which is a harmonic oscillator. Since $H^2$ is diagonal and has the form of a harmonic oscillator, its eigenvalues are $2\hbar^2v_F^2 n/\ell_B^2$ for $n=0,1,2,\dots$, and the energy itself is the square root,

$$E_n = \text{sgn}(n)\, v_F\sqrt{2\hbar B|n|}, \qquad n = 0,\pm1,\pm2,\dots, \tag{4.7}$$

with a real mode at exactly zero energy for $n=0$. For this mode the lower spinor component vanishes identically, so there is no partner state to pair it with. This is the origin of the $\sqrt{B}$ scaling in graphene. The spectrum is the *square root* of a harmonic-oscillator spectrum and not the spectrum itself, so both the dependence on the field and the level spacing change their behavior. For Schrödinger electrons the levels are equally spaced and grow linearly. For Dirac electrons the levels are spaced as $\sqrt{n}$ and grow as $\sqrt{B}$. This is the reason why, at the same field, the Landau levels of graphene are roughly two orders of magnitude higher in energy than the ones of a GaAs 2DEG. Figure [4.4](#fig:s04:ladders) shows how the two ladders move with the field, linearly in one case and as a square root in the other. The ladder at one field is a cut through each fan, and it includes the zero mode, which has no counterpart in the Schrödinger case.

The two ladders at one field are drawn again in [](#sch:s04:dirac_levels), now with the two components of the spinor. The zero mode lives in the upper component only, which is what it means that its lower component vanishes.

![The Landau levels at one fixed field. In (a) the parabolic electrons have the levels $\hbar\omega_c(n+\tfrac12)$ of [(4.6)](#eq-4-6), equally spaced. In (b) the Dirac electrons have the levels $\mathrm{sgn}(n)\sqrt{|n|}\,E_1$ of [(4.7)](#eq-4-7), with $E_1=\sqrt{2}\hbar v_F/\ell_B$. Each level is colored by the weight of the upper and of the lower component of the spinor, from the diagonalization of $H$ in an oscillator basis. Look at the level $n=0$, which is fully in the upper component, and at $E_4=2E_1$.](figures/web/session04/dirac_levels.svg){#sch:s04:dirac_levels alt="Left, equally spaced levels of parabolic electrons. Right, levels of Dirac electrons that come closer together at high energy, each drawn in two colors, with the zero level in one color only."}

![The same magnetic field with two dispersions gives two completely different ladders, drawn here as functions of the field. (a) Schrödinger electrons give the harmonic-oscillator spectrum [(4.6)](#eq-4-6), where every level is a constant $\hbar\omega_c=\hbar B/m$ above the one below it. So every level is a straight line through the origin, and the whole ladder grows linearly in $B$. (b) Dirac electrons give the square root of that spectrum, equation [(4.7)](#eq-4-7). The levels come closer together as $\sqrt{n}$, they come in a particle-hole symmetric pair for every $|n|\ge 1$, and the overall scale grows only as $\sqrt{B}$. This is still enough to put the level spacing of graphene about two orders of magnitude above the one of a GaAs quantum well at the same field. The $n=0$ level is the qualitatively new feature. It stays at zero energy for every field strength, which is the flat line, because it is the only solution with no partner in the other spinor component. The translucent plane at the field $B_0$ cuts each fan. The short rods where it cuts are the ladder of levels at that field, so the ladder at a fixed field is the vertical cut through the fan. The two vertical scales are independent of each other, since what we compare is the pattern of spacings and not the absolute energies.](figures/s04f04_ladders.svg){#fig:s04:ladders number="4.4"}

::: quiz
The field of a graphene sample is multiplied by 9. By which factor does the energy of the first Landau level above zero change?

- [ ] It does not change.

    This is false. The first level is $E_1\approx36\,\mathrm{meV}$ at 1 T and $109\,\mathrm{meV}$ at 9 T. It grows with the field.

- [ ] By 9.

    This is false. A factor 9 is the law of the parabolic band, where $\hbar\omega_c\propto B$. For graphene it would give $327\,\mathrm{meV}$ at 9 T, and not the $109\,\mathrm{meV}$ of the square-root law.

- [x] By 3.

    This is true. The energy [(4.7)](#eq-4-7) is proportional to $\sqrt{|n|B}$, so a factor 9 in the field gives a factor 3 in the energy.

:::

::: notebookbox
**Notebook check-in:** [`session4.ipynb`](https://github.com/joselado/Advanced_Quantum_Materials_2027/blob/main/jupyter-notebooks/session4.ipynb), in two groups. The parabolic case starts with "The dispersion of the square lattice" (Reminder) and "Bands in the conventional quantum Hall state" (Reminder). Then it has "Landau levels of conventional electrons" (Core), "Magnetic field dependence of Landau levels" (Core) and "Imaging the magnetic field dependence in the Landau levels" (Core). The Dirac case starts with "The dispersion of the honeycomb lattice" (Reminder) and "Bands in the Dirac quantum Hall state" (Reminder). Then it has "Landau levels of the Dirac equation" (Core), "Magnetic field dependence of Dirac Landau levels" (Core) and "Imaging the magnetic field dependence in the Dirac Landau levels" (Core).

Build a ribbon of the square lattice, which has a parabolic band bottom, and an armchair ribbon of the honeycomb lattice, which has a Dirac cone. Switch on the Peierls substitution [(4.4)](#eq-4-4) and check both spectra. For the square lattice you should find equally spaced flat Landau levels that grow linearly in $B$, as in [(4.6)](#eq-4-6). For the honeycomb lattice you should find levels with unequal spacing that grow as $\sqrt{B}$, as in [(4.7)](#eq-4-7). The "imaging" sections let you follow the energy of each level as a function of the field strength, which is the most direct numerical check of the linear and square-root scaling that we derived above.
:::

::: quiz
At a fixed field, what is the ratio $E_4/E_1$ of the Dirac Landau levels of [(4.7)](#eq-4-7)?

- [ ] $4$.

    This is false. This is the ratio of a linear ladder with no offset. With $E_1=36\,\mathrm{meV}$ at 1 T it would give $E_4=145\,\mathrm{meV}$, while the square-root law gives $73\,\mathrm{meV}$.

- [x] $2$.

    This is true. The levels go as $\sqrt{n}$, so $E_4/E_1=\sqrt{4}=2$.

- [ ] $16$.

    This is false. This would need $E_n\propto n^2$. With $E_1=36\,\mathrm{meV}$ it gives $E_4=580\,\mathrm{meV}$ at 1 T, which is far above the $73\,\mathrm{meV}$ of [(4.7)](#eq-4-7).

:::

::: {.tryit notebook="session4.ipynb" cell="Magnetic field dependence of Dirac Landau levels"}
Run the cell for `B = 0.005, 0.01, 0.02`. Read the position of the first peak above zero energy in each panel. From the first panel to the last the field grows by a factor 4. The peak moves by a factor close to 2, as in [(4.7)](#eq-4-7).
:::

::: comesback
- In Section [4.11](#sec-4-11) the honeycomb ribbon gives these $\sqrt{B}$ levels on the lattice, with their own chiral edge states.
- In Section [4.19](#sec-4-19) the same honeycomb lattice gives a quantized Hall conductance without any field, through the Haldane coupling.
- In Section [10.7](#sec-10-7) Landau levels are one of the tools that go from a Hamiltonian to an observable, which Hamiltonian learning tries to invert.
:::
