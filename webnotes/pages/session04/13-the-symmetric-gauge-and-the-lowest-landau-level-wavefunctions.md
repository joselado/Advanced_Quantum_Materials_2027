## The symmetric gauge and the lowest-Landau-level wavefunctions {#sec-4-13 number="4.13"}

To go from single-particle Landau levels to a real many-body quantum Hall wavefunction, we change to the symmetric gauge, $\mathbf{A}=\tfrac{B}{2}(-y,x,0)$, and to the complex coordinate $z=x+iy$. We write $\partial_z = \tfrac12(\partial_x-i\partial_y)$ and $\partial_{\bar z} =
\tfrac12(\partial_x+i\partial_y)$, and then the ladder operator of Section [4.12](#sec-4-12) in this gauge is proportional to $\partial_{\bar z} + z/4\ell_B^2$. The condition for the lowest Landau level (LLL), $a\psi=0$, is therefore the first-order differential equation

$$\left(\partial_{\bar z} + \frac{z}{4\ell_B^2}\right)\psi(z,\bar z) = 0
\quad\Longrightarrow\quad
\psi(z,\bar z) = f(z)\, e^{-|z|^2/4\ell_B^2}, \tag{4.9}$$

where $f(z)$ is an *arbitrary holomorphic function*, meaning any function built only from powers of $z$ and never from $\bar z$. This is the precise form of the statement "any power $z^m$ times a Gaussian is a zeroth-Landau-level wavefunction". Holomorphicity is not an extra assumption, since it follows directly when we solve the LLL condition in the symmetric gauge. The single-particle LLL orbitals are then

$$\psi_m(z) = z^m\, e^{-|z|^2/4\ell_B^2}, \qquad m=0,1,2,\dots, \tag{4.10}$$

and each of them has an angular momentum $m$, which is the eigenvalue of $L_z$ in this gauge. All of them have the same Gaussian envelope, but the polynomial prefactor $z^m$ moves the probability density of the orbital further from the origin when $m$ grows. The reason is that $|\psi_m|^2$ has its maximum where $\tfrac{d}{d|z|}\big(|z|^{2m}e^{-|z|^2/2\ell_B^2}\big)=0$, which is at the radius $r_m = \sqrt{2m}\,\ell_B$.

::: quiz
What is the radius of the maximum of $|\psi_m|^2$ for $m=8$, in units of $\ell_B$?

- [ ] $2\sqrt{2}$.

    This is false. A ring of radius $2\sqrt2\,\ell_B$ encloses $r^2/(2\ell_B^2)=4$ flux quanta, while the state $m=8$ has the angular momentum of $8$.

- [x] $4$.

    This is true. The maximum is at $r_m=\sqrt{2m}\,\ell_B$, which is $\sqrt{16}\,\ell_B=4\,\ell_B$ for $m=8$. The ring encloses $m$ flux quanta.

    ![The density $|\psi_m|^2$ for $m=4$, $8$ and $32$, each divided by its maximum. The radius $2\sqrt{2}\,\ell_B$ of the first option belongs to $m=4$, and $8\,\ell_B$ of the third option belongs to $m=32$.](figures/web/session04/lll_radius.svg){alt="Three bell-shaped curves of the density against the radius, with maxima at 2 times the square root of 2, at 4 and at 8 for three values of the angular momentum."}

- [ ] $8$.

    This is false. A ring of radius $8\ell_B$ encloses $r^2/(2\ell_B^2)=32$ flux quanta, which would be the state $m=32$ and not $m=8$.

:::

## The many-body wavefunction of the filled lowest Landau level {#sec-4-14 number="4.14"}

Now we look for the many-body ground state of $N$ electrons in which *every* LLL orbital is occupied. Two conditions fix this state completely. It must be built only from LLL orbitals [(4.10)](#eq-4-10), and it must be antisymmetric under the exchange of any two electrons, as fermion statistics requires. Both conditions are satisfied by

$$\Psi_1(z_1,\dots,z_N) = \prod_{i<j}(z_i-z_j)\; \exp\!\left(-\sum_i \frac{|z_i|^2}{4\ell_B^2}\right). \tag{4.11}$$

The Vandermonde product $\prod_{i<j}(z_i-z_j)$ does two things at the same time. First, it is antisymmetric by construction, since the exchange of two coordinates $z_i\leftrightarrow z_j$ changes the sign of exactly one factor $(z_i-z_j)$, and this gives the overall minus sign that the Pauli principle requires. Second, it is exactly the Slater determinant of the single-particle orbitals $1,z,z^2,\dots,z^{N-1}$, because of the standard identity for the Vandermonde determinant, $\det\!\big(z_i^{\,j-1}\big) = \prod_{i<j}(z_j-z_i)$. So [(4.11)](#eq-4-11) is the Slater determinant of the $N$ lowest LLL orbitals, times their common Gaussian envelope, where the Gaussians of the single electrons combine into the collective exponential shown above. This is the exact many-body ground state of $N$ electrons that fill the lowest Landau level completely, which is the integer quantum Hall state at filling $\nu=1$.

## Angular momentum, enclosed flux, and the uniform electron gas {#sec-4-15 number="4.15"}

In Section [4.13](#sec-4-13) we saw that a larger angular momentum $m$ moves the maximum of an orbital further from the origin, to the radius $r_m=\sqrt{2m}\,\ell_B$. In other words, this orbital encloses a larger area, and so a larger magnetic flux. We will use this link between angular momentum and enclosed flux in Section [4.17](#sec-4-17) to find how much charge a quasiparticle has. For now, the important consequence is about [(4.11)](#eq-4-11) itself. When we sum over the full Slater determinant, we find a density profile that is essentially uniform, or flat, up to a radius set by the highest occupied angular momentum $m=N-1$, and that drops sharply to zero beyond this radius. In other words, the filled lowest Landau level is a uniform two-dimensional electron gas without any structure, and this is the property that we will now ask also from a Landau level with *fractional* filling. Figure [4.5](#fig:s04:droplet) shows both parts of this statement, with the single orbitals as nested rings of growing radius, and the flat droplet that they give when we add them.

![Angular momentum fixes the radius. (a) The lowest-Landau-level orbitals [(4.10)](#eq-4-10), $|\psi_m|^2\propto r^{2m}e^{-r^2/2\ell_B^2}$, for $m=0,2,4,6,8$, each renormalized here to the same peak height and cut open over half a turn. They are nested rings, and when $m$ increases the ring moves outward, to $r_m=\sqrt{2m}\,\ell_B$, and encloses more flux. (b) When we add every orbital from $m=0$ to $m=N-1$ we therefore fill a disc, and the rings overlap in such a way that the total density is flat inside the disc and falls off sharply at the edge. The filled lowest Landau level is a uniform electron droplet without structure, with one electron per flux quantum. The Laughlin state [(4.12)](#eq-4-12) at $\nu=1/3$ is the second profile. The same $N$ electrons now use orbitals up to $m=3(N-1)$, so the radius of the droplet grows by $\sqrt{3}$ and the density becomes a third, while the droplet stays as uniform as before. The Laughlin construction is built to keep this uniformity, and the profiles of (b) are schematic.](figures/s04f05_droplet.svg){#fig:s04:droplet number="4.5"}

::: quiz
In the filled lowest Landau level the density is flat up to the radius set by $m=N-1$. How does this radius change if we double the number of electrons?

- [ ] It doubles.

    This is false. The radius is $\sqrt{2(N-1)}\,\ell_B$. It is $7.1\,\ell_B$ for $N=26$ and $10.1\,\ell_B$ for $N=52$, a factor $1.4$ and not $2$. A factor $2$ needs four times as many electrons.

- [x] It grows by a factor $\sqrt{2}$.

    This is true. The radius is $r=\sqrt{2(N-1)}\,\ell_B$, so for large $N$ it grows as $\sqrt{N}$. For $N=100$ and $N=200$ we get $14.1\,\ell_B$ and $20.0\,\ell_B$.

- [ ] It does not change, since the density is uniform.

    This is false. A uniform density means that each electron takes the same area, so more electrons need more area. For $N=100$ the radius is $14.1\,\ell_B$ and for $N=200$ it is $20.0\,\ell_B$.

:::
