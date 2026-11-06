## From a single Kondo impurity to the Kondo lattice {#sec-8-11 number="8.11"}

Now that we have the method for quantum spin liquids, the lecture moves to a second physical system, which is quite different but which can be solved with the same method. This is the **Kondo lattice model**, which appears whenever a metal and a correlated system of local moments exist together.

Let us start with the simplest case, which is a single spin-$1/2$ magnetic impurity in a non-interacting two-dimensional electron gas. The total Hamiltonian is a free kinetic term with a dispersion for the conduction electrons, plus a Heisenberg-like coupling between the spin of the impurity and the local spin density of the conduction electrons at the impurity site,

$$H = -t\sum_{\langle ij\rangle,\sigma}\Big(c^\dagger_{i\sigma}c_{j\sigma} + \text{h.c.}\Big) +
H_K, \qquad H_K = J_K\sum_{\alpha\beta}\Big(c^\dagger_{0\beta}\,\boldsymbol\sigma_{\beta\alpha}\,
c_{0\alpha}\Big)\cdot \mathbf S, \tag{8.17}$$

where $H_K$ is the **Kondo coupling**. To solve this problem exactly is hard. However, we can describe the ground state in a simple way, even without the full solution. The spin of the impurity forms a singlet, which has the same structure as [(8.3)](#eq-8-3), with an effective conduction electron close to it,

$$|GS\rangle \sim \frac{1}{\sqrt2}\Big(|{\Uparrow\downarrow}\rangle -
|{\Downarrow\uparrow}\rangle\Big),$$

and the rest of the electron gas behaves as a Fermi sea without interactions. This is a good approximation to the many-body ground state. The resulting state has total spin zero and does not break time-reversal symmetry, so even if it has a real local moment, it is already a quantum magnet in the sense of Section [8.1](#sec-8-1).

Let us now generalize this to a whole **lattice** of magnetic impurities, with one impurity per site, where each impurity is coupled to the same bath of conduction electrons,

$$H = -t\sum_{\langle ij\rangle,\sigma}\Big(c^\dagger_{i\sigma}c_{j\sigma} + \text{h.c.}\Big) +
J_K\sum_{j,\alpha\beta}\Big(c^\dagger_{j\beta}\,\boldsymbol\sigma_{\beta\alpha}\,c_{j\alpha}\Big)\cdot
\mathbf S_j. \tag{8.18}$$

Every impurity again tends to form a singlet with a conduction electron close to it. Since many impurities compete for the same sea of electrons, the electrons that screen the impurities are shared, in a fractional way, between the singlets of different impurities. The result is a state with a large entanglement over the whole lattice, between all the magnetic sites and the electron gas, while the total spin stays exactly zero.

::: notebookbox
**Notebook check-in:** [`session8.ipynb`](https://github.com/joselado/Advanced_Quantum_Materials_2027/blob/main/jupyter-notebooks/session8.ipynb), "Magnetization of a large Heisenberg model with a magnetic impurity" (Challenge) and "Magnetization of a dimerized Heisenberg model with a magnetic impurity" (Challenge)

These exercises show, numerically and in real space, how the local field of a single magnetic impurity decays with the distance in a quantum magnet that is otherwise gapless or dimerized. The gapless chain shows an algebraic and staggered decay, which follows the correlation profile of a critical spin liquid. The dimerized chain of Section [8.5](#sec-8-5), which is a valence bond solid, shows instead an exponential decay over a finite correlation length, because its ground state is gapped. This is the same physics of the screening cloud as in [(8.17)](#eq-8-17), seen from the side of a single chain in real space and not from the side of itinerant electrons.
:::

## Solving the Kondo lattice with the parton method and a hybridization {#sec-8-12 number="8.12"}

The lecture makes the parallel with Section [8.8](#sec-8-8) explicit, since we solve this problem in the same way as we solved the QSL. We replace every impurity spin by an Abrikosov fermion, $\mathbf S_j = \tfrac12
f_{j\alpha}^\dagger \boldsymbol\sigma_{\alpha\beta} f_{j\beta}$, with the same single-occupancy constraint [(8.11)](#eq-8-11), which we write here in the equivalent traceless form

$$S_{\alpha\beta}(j) = f^\dagger_{j\alpha}f_{j\beta} - \frac{n_f(j)}{2}\delta_{\alpha\beta}. \tag{8.19}$$

When we insert this into [(8.18)](#eq-8-18), the Kondo coupling becomes a real quartic interaction. Now it does not couple the auxiliary $f$ fermions to the $f$ fermion of another site, as in [(8.13)](#eq-8-13), but to the *real* conduction electrons $c_{j\sigma}$ on the same site,

$$H \sim \sum_{\mathbf k\alpha} \varepsilon_{\mathbf k}\, c^\dagger_{\mathbf k\alpha}c_{\mathbf
k\alpha} \;-\; J_K\sum_{j,\alpha\beta}\Big(c^\dagger_{j\beta}f_{j\beta}\Big)\Big(f^\dagger_{j\alpha}
c_{j\alpha}\Big). \tag{8.20}$$

As in [(8.14)](#eq-8-14), we decouple this quartic term at the mean-field level, with the expectation value $\langle c^\dagger_j f_j\rangle$, and we do a Fourier transform to momentum space. This gives a bilinear Hamiltonian that mixes real electrons and auxiliary fermions,

$$H \sim \sum_{\mathbf k\alpha} \varepsilon_{\mathbf k}\, c^\dagger_{\mathbf k\alpha} c_{\mathbf
k\alpha} \;-\; \gamma_K \sum_{\mathbf k,\alpha} f^\dagger_{\mathbf k\alpha}c_{\mathbf k\alpha} +
\text{h.c.}, \tag{8.21}$$

where $\varepsilon_{\mathbf k}$ is the **conduction band dispersion** and $\gamma_K$ is the **Kondo hybridization**. The hybridization is the only mean-field parameter, it is determined self-consistently, and it contains all the information about the strength of the original Kondo coupling $J_K$.

![The result of the parton method for the Kondo lattice, which we obtain in the second part of this page. In panel (a) the flat band of the $f$ levels crosses the conduction band, and in panel (b) the hybridization $\gamma_K$ of [(8.21)](#eq-8-21) opens a gap at the crossing.](figures/s08f06_kondo_bands.svg){alt="A dispersive conduction band crossing a flat band without hybridization, and the same bands with a gap at the crossing when the hybridization is finite."}

::: quiz
In the Kondo lattice [(8.18)](#eq-8-18) every impurity wants a singlet with a conduction electron close to it. What is the consequence of having many impurities?

- [x] The screening electrons are shared between the singlets of different impurities.
- [ ] Each impurity gets its own electron, so the electron density doubles.
- [ ] The impurities form singlets with each other and decouple from the metal.
- [ ] The conduction electrons localize.

The number of conduction electrons is not larger than the number of impurities, and all impurities draw from the same sea. The singlets are then fractional and entangled over the lattice.
:::

::: quiz
In [(8.21)](#eq-8-21) with $\gamma_K=0$, what is the energy of the $f$ band?

- [ ] $\varepsilon_{\mathbf k}$, the same as the conduction band.
- [x] Zero for every $\mathbf k$, a flat band.
- [ ] $-\gamma_K$ for every $\mathbf k$.
- [ ] It does not exist, since the $f$ fermions are removed.

The auxiliary fermions have no hopping of their own, and the only term that involves them is the hybridization. Without it their levels sit at zero energy, which is the chemical potential of the constraint.
:::

::: {.tryit notebook="session8.ipynb" cell="Quantum magnetism in the Kondo lattice"}
Run the three values of `JK` and follow the flat band. Check that the crossing with the conduction band is replaced by a gap, and that the gap grows from $J_K=0.25$ to $J_K=0.5$. Then change `add_onsite(-2.0)` and see if the gap stays at the Fermi level.
:::
