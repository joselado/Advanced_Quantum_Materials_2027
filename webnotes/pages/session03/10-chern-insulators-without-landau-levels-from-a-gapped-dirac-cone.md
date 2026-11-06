## Chern insulators without Landau levels from a gapped Dirac cone {#sec-3-10 number="3.10a"}

Now we come back to the question from the beginning of the session. A Chern insulator needs a broken time-reversal symmetry. In fact, one can show directly from [(3.4)](#eq-3-4) that $\sigma_{xy}\equiv 0$ whenever time-reversal symmetry holds, since time reversal changes the sign of the Berry curvature. However, nothing in the derivation of the Chern number required a magnetic field or Landau levels. So the question is if we can obtain a finite Chern number from an ordinary lattice band structure, using only terms that break time-reversal symmetry and that are entirely inside the lattice itself.

The method is to look for a lattice that has a **massive Dirac equation** in its low-energy expansion. Several two-dimensional lattices have massless Dirac points in their band structure, such as the honeycomb lattice, the kagome lattice and a square lattice with $\pi$-flux, and this is the same Dirac cone that we derived for graphene in session 2. Close to one such point, the low-energy Hamiltonian has the form

$$H(k) = k_x\,\sigma_x + \lambda\, k_y\,\sigma_y + m\,\sigma_z, \tag{3.7}$$

with $\lambda = \pm 1$ fixed by the chirality of the lattice at this Dirac point, and $m$ a mass term that opens a gap, $E_\pm(k) = \pm\sqrt{k_x^2+k_y^2+m^2}$. We compute the Berry curvature of the lower band and integrate it, with the same procedure as in [(3.4)](#eq-3-4) but now over the small region of momentum space where the curvature is concentrated. This gives the Chern number of this single gapped Dirac cone,

$$C_{\text{Dirac}} = \frac{1}{2}\,\mathrm{sgn}(m)\,\mathrm{sgn}(\lambda). \tag{3.8}$$

Let us see what [(3.8)](#eq-3-8) means for one cone, in [](#sch:s03:dirac_mass). The bands do not know the sign of $m$, but the Berry curvature does.

![A single gapped Dirac cone $H=k_x\sigma_x+\lambda k_y\sigma_y+m\sigma_z$ of [(3.7)](#eq-3-7) with $\lambda=+1$, in units of $|m|$. In (a) the bands are $\pm\sqrt{k^2+m^2}$, the same for both signs of $m$, and the dotted lines are the massless cone. In (b) the Berry curvature of the lower band is $\Omega=\lambda m/2(k^2+m^2)^{3/2}$, and its integral over the plane divided by $2\pi$ is $\pm\tfrac12$, as in [(3.8)](#eq-3-8). Look at how the same bands give opposite curvature, since the sign of $C$ is in the wavefunctions and not in the energies.](figures/web/session03/dirac_mass.svg){#sch:s03:dirac_mass alt="Left, the two bands of a gapped Dirac cone. Right, the Berry curvature of the lower band, a positive peak for positive mass and a negative peak for negative mass."}

The half-integer in [(3.8)](#eq-3-8) is not an inconsistency. A real lattice always has an even number of Dirac points related by time-reversal symmetry, and the honeycomb lattice has two, which are usually called $K$ and $K'$. Only the *sum* of their contributions needs to be an integer.

::: quiz
A massive Dirac cone with $\lambda=+1$ has Chern number $+\tfrac12$ for $m>0$. What is its Chern number for $m<0$ with the same $\lambda$?

- [ ] $-1$.

    This is false. The jump of $C$ from $m>0$ to $m<0$ is one, since the value goes from $+\tfrac12$ to $-\tfrac12$. The value of a single cone is never larger than $\tfrac12$ in size.

- [ ] $+\tfrac12$, since the gap has the same size.

    This is false. The curvature is proportional to $m$, so it is odd in $m$. The gap $2|m|$ is the same for $m=0.1$ and $m=-0.1$, but the Berry curvature has the opposite sign and so does $C$.

- [x] $-\tfrac12$.

    This is true. The Chern number [(3.8)](#eq-3-8) is $\tfrac12\,\mathrm{sgn}(m)\,\mathrm{sgn}(\lambda)$. It depends on the sign of the mass and not on its size, so a change of sign of $m$ changes the sign of $C$.

:::

![The two Dirac cones of the honeycomb lattice, at $K$ and $K'$, drawn over the Brillouin zone. These are the points where a mass term of [(3.7)](#eq-3-7) opens a gap. Look at the two cones, since a staggered potential gives the same mass at both, while $\lambda$ has opposite signs.](figures/s02f04_dirac.svg){panel="c" alt="Two Dirac cones at the corners of the hexagonal Brillouin zone of the honeycomb lattice."}

::: quiz
A lattice model has a single massive Dirac cone at low energy and no other states close to the gap. Can its filled band have $\sigma_{xy}=e^2/2h$?

- [ ] Yes, since [(3.8)](#eq-3-8) gives the value $1/2$.

    This is false. Take the two-band model with $\mathbf d=(\sin k_x,\sin k_y,m+\cos k_x+\cos k_y)$ and $m=-1.9$. It has one cone at $\Gamma$ with mass $0.1$, and its Chern number is exactly $|C|=1$. The curvature of the rest of the zone supplies the other half.

- [ ] No, since a single Dirac cone cannot have a gap.

    This is false. The term $m\sigma_z$ gives the spectrum $\pm\sqrt{k^2+m^2}$ with a gap $2|m|$ for a single cone. The reason is not the gap, but the integer quantization of $C$ on a lattice.

- [x] No, since on a lattice the Chern number of a filled band is an integer, so the half of one cone is completed elsewhere in the zone.

    This is true. The Chern number of a filled band on a lattice is an integer. The half of [(3.8)](#eq-3-8) is completed by the rest of the zone, either by a second cone, like $K$ and $K'$ in the honeycomb lattice, or by the massive part of the band, as in the model above.

:::

This is where the choice of the mass term matters, and we will work out the two natural choices explicitly, because they give qualitatively different physics. At $K$ and $K'$ the chirality $\lambda$ has opposite sign, since the two points are time-reversal partners. Let us first open the gap with a staggered sublattice potential, which raises the onsite energy on one honeycomb sublattice and lowers it on the other. This mass term is an ordinary scalar potential, so it has the *same* sign $m$ at both $K$ and $K'$. From [(3.8)](#eq-3-8), the two Dirac points then give Chern numbers of opposite sign, $+\tfrac12\,\mathrm{sgn}(m)$ and $-\tfrac12\,\mathrm{sgn}(m)$, which cancel. The result is $C=0$, which is an ordinary insulator that is topologically trivial, and this is the same kind of gap as in boron nitride. 

::: {.tryit notebook="session3.ipynb" cell="Topological states and topological invariants"}
Run the cell with `h.add_sublattice_imbalance(0.5)` and look at the Berry curvature, which has opposite colors around K and K'. Change the value to `-0.5`. Both colors are exchanged, and `h.get_chern(nk=60)` still gives 0, as the cancellation of [(3.8)](#eq-3-8) predicts.
:::
