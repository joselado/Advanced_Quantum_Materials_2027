## Properties of an electronic dispersion {#sec-2-9 number="2.9"}

Once we have a dispersion $E(\mathbf{k})$, from [(2.8)](#eq-2-8), [(2.13)](#eq-2-13), [(2.14)](#eq-2-14) or from a more complicated model, several quantities that we derive from it have a direct physical meaning.

The **density of states**,

$$g(\omega) = \int_{\text{BZ}} \frac{d^dk}{(2\pi)^d}\; \delta\!\left(\omega-E(\mathbf{k})\right), \tag{2.16}$$

counts how many states there are at energy $\omega$. It controls how strongly a material responds to interactions. A large or divergent density of states means that even a weak interaction can drive an instability toward magnetism, a charge density wave or superconductivity, which are the three cases of the last session. A vanishing density of states means that interactions can hardly have any effect, however strong they are.

The **group velocity**,

$$v(\mathbf{k}) = \frac{1}{\hbar}\nabla_{\mathbf{k}} E(\mathbf{k}), \tag{2.17}$$

is the local slope of the dispersion. Where $v(\mathbf{k})=0$, electrons at that $\mathbf{k}$ do not move in practice. Where $v(\mathbf{k})$ is large, they propagate quickly through the lattice.

The **effective mass**,

$$\left(\frac{1}{m^\ast}\right)_{ij} = \frac{1}{\hbar^2}\,
\frac{\partial^2 E(\mathbf{k})}{\partial k_i\,\partial k_j}, \tag{2.18}$$

is the curvature of the dispersion, and it is the mass that is measured in essentially every transport or cyclotron-resonance experiment, since the bare electron mass cannot be observed directly inside a solid. Depending on the band, $m^\ast$ can go from nearly zero to very large values. For a Dirac dispersion, as we will see soon, it is formally not defined at the point where the bands touch.

Finally, the **Fermi surface** is the set of $\mathbf{k}$-points that have the same energy as the highest occupied state. Its shape controls which electronic instabilities are favoured and how a material responds to an external magnetic field, and it is one of the quantities that ARPES (Section [2.12](#sec-2-12)) can map directly.

::: notebookbox
**Notebook check-in:** [`session2.ipynb`](https://github.com/joselado/Advanced_Quantum_Materials_2027/blob/main/jupyter-notebooks/session2.ipynb), "Density of states of the honeycomb lattice" (Core), and "Fermi surface of the honeycomb lattice" (Challenge)

Once you have the honeycomb dispersion of Section [2.11](#sec-2-11), these two sections let you compute [(2.16)](#eq-2-16) and the Fermi surface directly, and see how both change when the Fermi level is tuned through the Dirac point.
:::
