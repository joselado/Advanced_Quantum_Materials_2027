## The Berry curvature, and why the Hall conductivity is an integer {#sec-3-5 number="3.5"}

We take the derivative of the Schrödinger equation $H(k)|u_n(k)\rangle = \varepsilon_n(k)|u_n(k)\rangle$ with respect to $k_\mu$ and project it onto a different band $\langle u_m(k)|$, with $m \neq n$, which gives

$$\langle u_m|\partial_{k_\mu} H|u_n\rangle
= \big(\varepsilon_n(k) - \varepsilon_m(k)\big)\,\langle u_m|\partial_{k_\mu} u_n\rangle. \tag{3.3}$$

This identity is the piece that we need, since it replaces a matrix element of $\partial_k H$ by a matrix element of the $k$-derivative of the wavefunction, divided by the energy difference. When we use [(3.3)](#eq-3-3) to rewrite the numerator and the denominator of [(3.2)](#eq-3-2) together, the explicit dependence on the energies cancels completely. What remains is an object built only from overlaps of wavefunctions, which is called the **Berry curvature** of band $n$,

$$\Omega_n(k) = -2\,\mathrm{Im}\, \langle \partial_{k_x} u_n(k)|\partial_{k_y} u_n(k)\rangle,$$

so that the Hall conductivity of a set of filled bands is

$$\sigma_{xy} = \frac{e^2}{h}\, C, \qquad
C = \sum_{n\ \text{filled}} \frac{1}{2\pi}\int_{\text{BZ}} \Omega_n(k)\, d^2k. \tag{3.4}$$

This is the central result of the session, and there are two important points about [(3.4)](#eq-3-4). First, $\sigma_{xy}$ depends only on how the wavefunctions change across the Brillouin zone, and not on the energies. We can deform the band structure in any way, and as long as the wavefunctions do not change, the Hall conductivity stays the same. Second, and more surprising, for a gapped system, which is an insulator, $C$ is always an integer, regardless of the number of bands and of the shape of the dispersion. This is a topological statement. The Brillouin zone of a two-dimensional system is a compact manifold, which is a torus since opposite edges of the zone are identified, and the integral of a curvature over a closed surface always gives an integer. The same happens for the Gaussian curvature of an ordinary closed surface in differential geometry. This integer $C$ is the **Chern number**, and [(3.4)](#eq-3-4) is the first place in the course where a measurable quantity, the Hall conductivity, is fixed by a topological invariant.
