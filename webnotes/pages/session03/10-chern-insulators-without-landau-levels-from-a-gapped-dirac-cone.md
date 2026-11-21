## Chern insulators without Landau levels from a gapped Dirac cone {#sec-3-10 number="3.10a"}

Can an ordinary band structure on a lattice have a finite Chern number, with no magnetic field and no Landau levels? We will now see that the answer is in the gapped Dirac cones of the lattice. Each cone gives half an integer, with a sign set by its mass, and the way in which the halves of the two cones add decides whether the lattice is a Chern insulator.

::: {.recall eq="3.4"}
This is the Hall conductivity of Section [3.5](#sec-3-5). The integer $C$ is the Chern number, and $\Omega_n(k)=-2\,\mathrm{Im}\,\langle\partial_{k_x}u_n|\partial_{k_y}u_n\rangle$ is the Berry curvature of the filled band $n$, which is built from its Bloch states $|u_n(k)\rangle$.
:::

Now we come back to the question from the beginning of the session. A Chern insulator needs a broken time-reversal symmetry. In fact, one can show directly from [(3.4)](#eq-3-4) that $\sigma_{xy}\equiv 0$ whenever time-reversal symmetry holds, since time reversal changes the sign of the Berry curvature. However, nothing in the derivation of the Chern number required a magnetic field or Landau levels. So the question is if we can obtain a finite Chern number from an ordinary lattice band structure, using only terms that break time-reversal symmetry and that are entirely inside the lattice itself.

The method is to look for a lattice that has a **massive Dirac equation** in its low-energy expansion. Several two-dimensional lattices have massless Dirac points in their band structure, such as the honeycomb lattice, the kagome lattice and a square lattice with $\pi$-flux. This is the same Dirac cone that we derived for graphene in Section [2.11](#sec-2-11). Close to one such point, the low-energy Hamiltonian has the form

$$H(k) = k_x\,\sigma_x + \lambda\, k_y\,\sigma_y + m\,\sigma_z, \tag{3.7}$$

with $\lambda = \pm 1$ fixed by the chirality of the lattice at this Dirac point, and $m$ a mass term that opens a gap, $E_\pm(k) = \pm\sqrt{k_x^2+k_y^2+m^2}$. We compute the Berry curvature of the lower band and integrate it, with the same procedure as in [(3.4)](#eq-3-4) but now over the small region of momentum space where the curvature is concentrated.

::: key
The Chern number of a single gapped Dirac cone [(3.7)](#eq-3-7) is

$$C_{\text{Dirac}} = \frac{1}{2}\,\mathrm{sgn}(m)\,\mathrm{sgn}(\lambda). \tag{3.8}$$

It is half an integer. Its sign is the sign of the mass $m$ times the chirality $\lambda$, and it does not depend on the size of the gap $2|m|$.
:::

::: {.steps title="From the massive Dirac Hamiltonian (3.7) to the half-integer (3.8)"}
The first step is to write the Berry curvature $\Omega=-2\,\mathrm{Im}\,\langle\partial_{k_x}u|\partial_{k_y}u\rangle$ with matrix elements of the derivatives of $H$. The Hamiltonian [(3.7)](#eq-3-7) has two bands, the lower one $|-\rangle$ and the upper one $|+\rangle$, with the energies $\mp\epsilon$ and $\epsilon=\sqrt{k^2+m^2}$. We insert the two bands between the two derivatives. The term with the band itself is real, so it drops from the imaginary part, and [(3.3)](#eq-3-3) turns the other term into matrix elements of $\partial_{k_x}H=\sigma_x$ and $\partial_{k_y}H=\lambda\,\sigma_y$, divided by the energy difference $2\epsilon$. The curvature of the lower band is then

$$\Omega_-(k) = -2\,\mathrm{Im}\,\frac{\langle -|\sigma_x|+\rangle\,\langle +|\lambda\,\sigma_y|-\rangle}{(2\epsilon)^2}.$$

The simplest point is the Dirac point, $k=0$, with $m>0$. There $H=m\,\sigma_z$, so the lower state is $|-\rangle=(0,1)$ and the upper state is $|+\rangle=(1,0)$. The two matrix elements are $\langle-|\sigma_x|+\rangle=1$ and $\langle+|\sigma_y|-\rangle=-i$, and

$$\Omega_-(0) = -2\,\mathrm{Im}\,\frac{\lambda\,(-i)}{4m^2} = \frac{\lambda}{2m^2}.$$

For $m<0$ the two states are exchanged, the second matrix element is $+i$, and $\Omega_-(0)$ changes sign.

The second step is a point away from the Dirac point. A rotation of $k$ by any angle is the same as a rotation of the Pauli matrices around the $z$ axis, which does not change $m\,\sigma_z$. The curvature then depends only on the size of $k$, and it is enough to take $k=(k,0)$, where $H=k\,\sigma_x+m\,\sigma_z$ is a real matrix. With the angle $\theta$ defined by $\cos\theta=m/\epsilon$ and $\sin\theta=k/\epsilon$, its eigenvectors are

$$|+\rangle = \begin{pmatrix}\cos\frac{\theta}{2}\\[2pt] \sin\frac{\theta}{2}\end{pmatrix}, \qquad
|-\rangle = \begin{pmatrix}-\sin\frac{\theta}{2}\\[2pt] \cos\frac{\theta}{2}\end{pmatrix}.$$

The two matrix elements are $\langle-|\sigma_x|+\rangle=\cos^2\frac{\theta}{2}-\sin^2\frac{\theta}{2}=\cos\theta$ and $\langle+|\sigma_y|-\rangle=-i$, which gives

$$\Omega_-(k) = \frac{\lambda\cos\theta}{2\,\epsilon^2} = \frac{\lambda\,m}{2\,(k^2+m^2)^{3/2}}.$$

This is a peak at the Dirac point, with the height $1/2m^2$, a width of the order of $|m|$ and the sign of $\lambda m$.

The last step is the integral over the plane, with $d^2k=2\pi k\,dk$,

$$C_{\text{Dirac}} = \frac{1}{2\pi}\int\Omega_-\,d^2k = \frac{\lambda m}{2}\int_0^\infty\frac{k\,dk}{(k^2+m^2)^{3/2}}
= \frac{\lambda m}{2}\left[-\frac{1}{\sqrt{k^2+m^2}}\right]_0^\infty = \frac{\lambda\,m}{2\,|m|},$$

which is [(3.8)](#eq-3-8). The same integral up to a finite radius $K$ gives $\tfrac12\,\mathrm{sgn}(\lambda m)\,\big(1-|m|/\sqrt{K^2+m^2}\big)$. So $90\%$ of the half-integer is inside $K\approx10\,|m|$, and the Dirac form [(3.7)](#eq-3-7) has to hold up to these momenta. This is a small part of the Brillouin zone only when the gap is small compared with the width of the bands.
:::

Let us see what [(3.8)](#eq-3-8) means for one cone, in [](#sch:s03:dirac_mass). The bands do not know the sign of $m$, but the Berry curvature does.

![A single gapped Dirac cone $H=k_x\sigma_x+\lambda k_y\sigma_y+m\sigma_z$ of [(3.7)](#eq-3-7) with $\lambda=+1$, in units of $|m|$. In (a) the bands are $\pm\sqrt{k^2+m^2}$, the same for both signs of $m$, and the dotted lines are the massless cone. In (b) the Berry curvature of the lower band is $\Omega=\lambda m/2(k^2+m^2)^{3/2}$, and its integral over the plane divided by $2\pi$ is $\pm\tfrac12$, as in [(3.8)](#eq-3-8). Look at how the same bands give opposite curvature, since the sign of $C$ is in the wavefunctions and not in the energies.](figures/web/session03/dirac_mass.svg){#sch:s03:dirac_mass alt="Left, the two bands of a gapped Dirac cone. Right, the Berry curvature of the lower band, a positive peak for positive mass and a negative peak for negative mass."}

The half-integer in [(3.8)](#eq-3-8) is not an inconsistency. A real lattice always has an even number of Dirac points related by time-reversal symmetry, and the honeycomb lattice has two, which are usually called $K$ and $K'$. Only the *sum* of their contributions needs to be an integer.

![The two Dirac cones of the honeycomb lattice, at $K$ and $K'$, drawn over the Brillouin zone. These are the points where a mass term of [(3.7)](#eq-3-7) opens a gap. Look at the two cones, since a staggered potential gives the same mass at both, while $\lambda$ has opposite signs.](figures/s02f04_dirac.svg){panel="c" alt="Two Dirac cones at the corners of the hexagonal Brillouin zone of the honeycomb lattice."}

This is where the choice of the mass term matters, and we will work out the two natural choices explicitly, because they give qualitatively different physics. At $K$ and $K'$ the chirality $\lambda$ has opposite sign, since the two points are time-reversal partners. Let us first open the gap with a staggered sublattice potential, which raises the onsite energy on one honeycomb sublattice and lowers it on the other. This mass term is an ordinary scalar potential, so it has the *same* sign $m$ at both $K$ and $K'$. From [(3.8)](#eq-3-8), the two Dirac points then give Chern numbers of opposite sign, $+\tfrac12\,\mathrm{sgn}(m)$ and $-\tfrac12\,\mathrm{sgn}(m)$, which cancel. The result is $C=0$, which is an ordinary insulator that is topologically trivial, and this is the same kind of gap as in boron nitride.

::: lab
A gap of this trivial kind has been reported in graphene itself. In graphene grown epitaxially on a SiC substrate a gap of about $0.26$ eV appears in the electronic spectrum, and it decreases as the number of layers grows. The authors propose that the gap comes from the breaking of the sublattice symmetry by the substrate. This is the staggered potential of this page, and with [(3.7)](#eq-3-7) the gap is $2|m|\approx0.26$ eV. Such a gap has $C=0$, so it gives no quantized Hall conductivity. The measurement is in [this article](https://www.nature.com/articles/nmat2003).
:::

::: quiz
A gapped Dirac cone has the Hamiltonian

$$H(k) = k_x\,\sigma_x + \lambda\, k_y\,\sigma_y + m\,\sigma_z,$$

with the mass $m$ and the chirality $\lambda=\pm1$. For $\lambda=+1$ and $m>0$ its lower band has the Chern number $+\tfrac12$. What is the Chern number for $m<0$ and the same $\lambda$?

- [ ] $-1$.

    This is false. The jump of $C$ from $m>0$ to $m<0$ is one, since the value goes from $+\tfrac12$ to $-\tfrac12$. The value of a single cone is never larger than $\tfrac12$ in size.

- [ ] $+\tfrac12$, since the gap has the same size.

    This is false. The curvature is proportional to $m$, so it is odd in $m$. The gap $2|m|$ is the same for $m=0.1$ and $m=-0.1$, but the Berry curvature has the opposite sign and so does $C$.

- [x] $-\tfrac12$.

    This is true. The Chern number of one cone is $\tfrac12\,\mathrm{sgn}(m)\,\mathrm{sgn}(\lambda)$. It depends on the sign of the mass and not on its size, so a change of sign of $m$ changes the sign of $C$.

:::

::: quiz
The Berry curvature of the lower band of a gapped Dirac cone is

$$\Omega(k) = \frac{m}{2\,(k^2+m^2)^{3/2}},$$

where $m$ is the mass and $k$ is the distance to the Dirac point. We make the mass ten times smaller, from $m=1$ to $m=0.1$. What happens to the integral of $\Omega$ over the plane?

- [ ] It becomes ten times smaller, as the gap does.

    This is false. For $m=1$ the peak has the height $0.5$, and for $m=0.1$ it has the height $50$. The integral over the plane is $\pi$ for both, which is $C=\tfrac12$.

- [ ] It becomes a hundred times larger, as the height of the peak does.

    This is false. The peak is $100$ times higher, but its width is $|m|$, so the area where it sits is $100$ times smaller. For both masses one half of the integral is inside the radius $k=\sqrt3\,|m|$, which is $1.73$ for $m=1$ and $0.173$ for $m=0.1$.

- [x] It does not change.

    This is true. The integral is $\pi\,\mathrm{sgn}(m)$ for any size of the mass. A smaller mass gives a higher and narrower peak with the same area, so a small gap needs a fine k-mesh around the Dirac point.

:::

::: quiz
One gapped Dirac cone gives the Chern number

$$C_{\text{Dirac}} = \tfrac12\,\mathrm{sgn}(m)\,\mathrm{sgn}(\lambda),$$

with the mass $m$ and the chirality $\lambda$. A staggered potential gives $m=0.5$ at both cones of the honeycomb lattice. The two cones have $\lambda=+1$ and $\lambda=-1$. What is the total Chern number?

- [ ] $C=\tfrac12+\tfrac12=1$

    This is false. The cone with $\lambda=-1$ gives $\tfrac12\cdot(+1)\cdot(-1)=-\tfrac12$ and not $+\tfrac12$. On the lattice with a staggered potential of $0.5$, the sum of the Berry curvature over a mesh of 60 by 60 points gives $C=0.000$.

- [x] $C=\tfrac12-\tfrac12=0$

    This is true. The mass has the same sign at both cones and the chirality has opposite signs, so the two halves cancel. This is an ordinary insulator, with the same kind of gap as boron nitride.

- [ ] $C=\tfrac12$

    This is false. Both cones have a gap, so both give their half, and the Chern number of a filled band of a lattice is an integer. A total of $\tfrac12$ would need the second cone to give $0$, but a cone with $m=0.5$ gives $\pm\tfrac12$.

:::

::: quiz
A lattice model has one gapped Dirac cone and no other states near the gap. The cone alone gives the Chern number $\tfrac12$. Can the filled band have $\sigma_{xy}=e^2/2h$?

- [ ] Yes, since the cone gives the value $\tfrac12$.

    This is false. Take the two-band model with $\mathbf d=(\sin k_x,\sin k_y,m+\cos k_x+\cos k_y)$ and $m=-1.9$. It has one cone at $\Gamma$ with mass $0.1$, and its Chern number is $|C|=1$. The curvature of the rest of the zone supplies the other half.

- [ ] No, since a single Dirac cone cannot have a gap.

    This is false. The term $m\sigma_z$ gives the spectrum $\pm\sqrt{k^2+m^2}$ with a gap $2|m|$ for a single cone. The reason is not the gap, but the integer quantization of $C$ on a lattice.

- [x] No, since the Chern number of a filled band of a lattice is an integer.

    This is true. The half of the cone is completed by the rest of the zone. This is either a second cone, like $K$ and $K'$ in the honeycomb lattice, or the part of the band far from the cone. An example of the second case is the model with $\mathbf d=(\sin k_x,\sin k_y,m+\cos k_x+\cos k_y)$ and $m=-1.9$, where one cone with mass $0.1$ comes with $|C|=1$.

:::

:::: problem
For electrons without spin, time-reversal symmetry means that the Bloch Hamiltonian obeys $H(-k)=H(k)^*$. Show that the Berry curvature of a band is then odd, $\Omega_n(-k)=-\Omega_n(k)$, and that the Chern number of [(3.4)](#eq-3-4) vanishes.

::: solution
We take the complex conjugate of $H(k)|u_n(k)\rangle=\varepsilon_n(k)|u_n(k)\rangle$ and we use $H(k)^*=H(-k)$. This gives $H(-k)\,|u_n(k)\rangle^*=\varepsilon_n(k)\,|u_n(k)\rangle^*$. For a band that is not degenerate, the state at $-k$ is then the complex conjugate of the state at $k$, with the same energy,

$$|u_n(-k)\rangle = |u_n(k)\rangle^* ,$$

up to a phase, which does not change the curvature. Now we take the derivative with respect to $k_\mu$. The left side depends on $k$ through $-k$, so the chain rule gives a minus sign, and the derivative of the state at $-k$ is $-\big(|\partial_\mu u_n(k)\rangle\big)^*$. In the overlap of two derivatives the two minus signs cancel and the complex conjugation stays,

$$\langle\partial_x u_n|\partial_y u_n\rangle\big|_{-k} = \Big(\langle\partial_x u_n|\partial_y u_n\rangle\big|_{k}\Big)^* .$$

The curvature is $-2$ times the imaginary part of this overlap, and the imaginary part changes sign under complex conjugation, so $\Omega_n(-k)=-\Omega_n(k)$. The Brillouin zone contains $-k$ for every $k$, so the integral of an odd function over it is zero, and $C=0$ for every band.

This is the reason why a Chern insulator needs magnetism or a magnetic field, and why a material with time-reversal symmetry has no Hall conductivity at zero field. It is also a check for a calculation. The two Dirac points of the honeycomb lattice are at $K$ and $K'=-K$, and a staggered potential is real, so the Berry curvature that we compute at $K'$ must be minus the one at $K$.
:::
::::

::: {.tryit notebook="session3.ipynb" cell="Topological states and topological invariants"}
Run the cell with `h.add_sublattice_imbalance(0.5)` and look at the Berry curvature, which has opposite colors around K and K'. Change the value to `-0.5`. Both colors are exchanged, and `h.get_chern(nk=60)` still gives 0, as the cancellation of [(3.8)](#eq-3-8) predicts.
:::

::: comesback
- In Section [3.10b](#sec-3-10b) the second choice of the mass term, the Haldane coupling, makes the two halves add.
- In Section [4.10](#sec-4-10) the same Dirac Hamiltonian is put in a magnetic field, and its Landau levels include a level at zero energy.
- In Section [8.9](#sec-8-9) the square lattice with $\pi$-flux comes back, now for spinons, with Dirac points at half filling.
:::
