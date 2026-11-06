## The Berry curvature, and why the Hall conductivity is an integer {#sec-3-5 number="3.5"}

We take the derivative of the Schrödinger equation $H(k)|u_n(k)\rangle = \varepsilon_n(k)|u_n(k)\rangle$ with respect to $k_\mu$ and project it onto a different band $\langle u_m(k)|$, with $m \neq n$, which gives

$$\langle u_m|\partial_{k_\mu} H|u_n\rangle
= \big(\varepsilon_n(k) - \varepsilon_m(k)\big)\,\langle u_m|\partial_{k_\mu} u_n\rangle. \tag{3.3}$$

This identity is the piece that we need, since it replaces a matrix element of $\partial_k H$ by a matrix element of the $k$-derivative of the wavefunction, divided by the energy difference. When we use [(3.3)](#eq-3-3) to rewrite the numerator and the denominator of [(3.2)](#eq-3-2) together, the explicit dependence on the energies cancels completely. What remains is an object built only from overlaps of wavefunctions, which is called the **Berry curvature** of band $n$,

$$\Omega_n(k) = -2\,\mathrm{Im}\, \langle \partial_{k_x} u_n(k)|\partial_{k_y} u_n(k)\rangle,$$

so that the Hall conductivity of a set of filled bands is

$$\sigma_{xy} = \frac{e^2}{h}\, C, \qquad
C = \sum_{n\ \text{filled}} \frac{1}{2\pi}\int_{\text{BZ}} \Omega_n(k)\, d^2k. \tag{3.4}$$

This is the central result of the session, and there are two important points about [(3.4)](#eq-3-4). First, $\sigma_{xy}$ depends only on how the wavefunctions change across the Brillouin zone, and not on the energies. We can deform the band structure in any way, and as long as the wavefunctions do not change, the Hall conductivity stays the same. Second, and more surprising, for a gapped system, which is an insulator, $C$ is always an integer, regardless of the number of bands and of the shape of the dispersion. This is a topological statement. The Brillouin zone of a two-dimensional system is a compact manifold, which is a torus since opposite edges of the zone are identified, and the integral of a curvature over a closed surface always gives an integer. The same happens for the Gaussian curvature of an ordinary closed surface in differential geometry. This integer $C$ is the **Chern number**, and [(3.4)](#eq-3-4) is the first place in the course where a measurable quantity, the Hall conductivity, is fixed by a topological invariant. As an example, [](#sch:s03:berry_haldane) shows the Berry curvature of two gapped honeycomb lattices, which we build in Section [3.10](#sec-3-10).

![The Berry curvature of the lower band over the Brillouin zone of the honeycomb lattice, computed on a grid. In (a) the gap comes from the Haldane coupling, with second-neighbor hopping $0.1$ in units of the first-neighbor one. In (b) it comes from a staggered sublattice potential of $0.5$. The curvature is concentrated at the two Dirac points, where the gap is smallest. In (a) it has the same sign at both points, and its integral divided by $2\pi$ gives $|C|=1$. In (b) the two signs are opposite and the integral vanishes. Look at the colors, since the integer comes from the sum of the two red spots.](figures/web/session03/berry_haldane.svg){#sch:s03:berry_haldane alt="Two color maps of the Brillouin zone, with two red spots for the Haldane coupling and one red and one blue spot for the staggered potential."}

::: quiz
We deform the dispersion of a gapped Chern insulator, so that all the band energies change. The Bloch wavefunctions stay the same and the gap stays open. What happens to $\sigma_{xy}$ in [(3.4)](#eq-3-4)?

- [ ] It changes in proportion to the gap.
- [x] It does not change.
- [ ] It becomes zero, since the energies are different.
- [ ] It changes in proportion to the bandwidth.

Equation [(3.4)](#eq-3-4) contains only the Berry curvature, which is built from the wavefunctions. The energies canceled when we used [(3.3)](#eq-3-3), and so $\sigma_{xy}$ cannot depend on them.
:::

::: quiz
We integrate the Berry curvature of a gapped band over the Brillouin zone on a coarse k-mesh and obtain $C=0.37$. What is the most likely reason?

- [ ] The band has a fractional Chern number.
- [x] The curvature is peaked and the k-mesh is too coarse to resolve it.
- [ ] The Hall conductivity of this band is fractional.
- [ ] The Brillouin zone is not a torus.

For an isolated gapped band the integral is exactly an integer. A value like $0.37$ means that the sum is not converged, which happens when the curvature is concentrated near a small gap. The remedy is a finer k-mesh.
:::

::: {.tryit notebook="session3.ipynb" cell="Topological states and topological invariants"}
In the cell that plots the Berry curvature, replace `h.add_sublattice_imbalance(0.5)` by `h.add_haldane(0.1)` and run it again. The map now has the same color around K and K', as in panel (a) of [](#sch:s03:berry_haldane). Then call `h.get_chern(nk=60)`. It gives 2, which is the value 1 of each of the two spin species of the default Hamiltonian. With the sublattice imbalance it gives 0.
:::
