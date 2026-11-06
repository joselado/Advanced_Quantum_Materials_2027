## Metal, gapped and nodal superconductor for one Fermi surface {#sec-5-10 number="5.10"}

Not every pairing function $\Delta(\mathbf k)$ is independent of momentum, and this gives more interesting cases. For a given electronic dispersion $\varepsilon(\mathbf k)$ there are in general three qualitatively different outcomes.

1.  **No superconductivity** ($\Delta = 0$). This is a metal, which is gapless everywhere on the Fermi surface.

2.  **Conventional (s-wave) superconductivity.** Here $\Delta(\mathbf k) \ne 0$ everywhere on the Fermi surface, so $E(\mathbf k)$ in [(5.9)](#eq-5-9) stays away from zero everywhere, and there is a full gap.

3.  **Unconventional, nodal superconductivity.** Here $\Delta(\mathbf k)$ vanishes along some lines or points of the Brillouin zone. Wherever the Fermi surface crosses one of these nodal lines, $E(\mathbf
    k) = 0$ even though $\Delta \ne 0$ nearby. The system is gapped in most of reciprocal space, but it stays gapless, which means metallic, at isolated momenta or along nodal lines.

![One Fermi surface with three outcomes. Each panel shows the Brillouin zone with a small Fermi pocket around $\Gamma$, and the height of the tube standing on the pocket is the minimum of the quasiparticle energy $E(\mathbf k)=\sqrt{\varepsilon(\mathbf
k)^2+|\Delta(\mathbf k)|^2}$ as we go once around it. Since $\varepsilon=0$ on the Fermi surface, this minimum is $|\Delta|$ evaluated there, which is why the pairing function only matters *on* the Fermi surface. (a) Without pairing the whole pocket is at zero energy, which is a metal. (b) A constant $\Delta_0$ lifts every point of it by the same amount, which gives a full gap. (c) The $d$-wave gap [(5.13)](#eq-5-13) vanishes on the zone diagonals, the red lines, and the pocket crosses them in four places, so four gapless points survive in a superconductor that is gapped everywhere else. Nodes in other parts of the zone do not appear in the spectrum, and only nodes that intersect the Fermi surface give gapless quasiparticles.](figures/s05f02_fsgap.svg){#fig:s05:fsgap number="5.2"}

Figure [5.2](#fig:s05:fsgap) shows the three cases next to each other, in the Brillouin zone and also as the gap along the Fermi surface itself, which is the only place where the gap can be read at all. The high-temperature cuprate superconductors are the standard example of scenario 3 in real materials. They are real superconductors, but their gap function has nodes, so parts of their Fermi surface stay gapless even in the superconducting state. This division into three cases holds for any lattice geometry, and the lecture shows it explicitly for the Fermi surfaces of both the square and the triangular lattice.

::: notebookbox
**Notebook check-in:** [`session5.ipynb`](https://github.com/joselado/Advanced_Quantum_Materials_2027/blob/main/jupyter-notebooks/session5.ipynb), "Unconventional singlet superconducting orders" (Challenge), and "Gapped and nodal superconducting orders" (Core)

Build a $\Delta(\mathbf k)$ that depends on momentum and vanishes along a line in the Brillouin zone, for example the d-wave form of section [5.13](#sec-5-13) below. Then check numerically with [(5.9)](#eq-5-9) that the gap closes exactly where the Fermi surface crosses this nodal line, which is different from the uniformly gapped case of section [5.9](#sec-5-9).
:::
