## The Nambu spinor and the Bogoliubov-de Gennes Hamiltonian {#sec-5-8 number="5.8"}

The pairing term creates a technical problem. We cannot diagonalize [(5.4)](#eq-5-4) with an ordinary vector of orbital operators, because the anomalous term mixes creation and annihilation operators, instead of pairing them up in the way of every Hamiltonian that we diagonalized in sessions 1-4. The solution is to *enlarge* the operator basis, so that both the creation and the annihilation operators of the original problem become entries of a bigger spinor that behave like annihilation operators. We work in momentum space, with a single orbital and both spins, and we define the **Nambu spinor**

$$\Psi_{\mathbf{k}} = \begin{pmatrix} c_{\mathbf{k}\uparrow} \\ c_{\mathbf{k}\downarrow} \\ c_{-\mathbf{k}\downarrow}^\dagger \\ -c_{-\mathbf{k}\uparrow}^\dagger \end{pmatrix}, \tag{5.6}$$

which has an electron sector, formed by the first two components and containing ordinary annihilation operators, and a hole sector, formed by the last two components and containing creation operators at $-\mathbf{k}$, with the spins exchanged and with an extra minus sign on the last entry. This sign has a real role. It is what is needed so that, when we write $H_{\text{MF}}$ in terms of $\Psi_{\mathbf k}$, the pairing term gives two identical and decoupled copies of the same $2\times 2$ problem, instead of mixing the two spin blocks through a Pauli matrix. For a spin-singlet pairing $\Delta(\mathbf k)$, which does not depend on momentum and is equal to $\Delta$ for the Fourier transform of the onsite case of [(5.4)](#eq-5-4), one can check directly, using the fermionic anticommutation relations to reorder operators where needed, that the mean-field Hamiltonian can be written exactly as

$$H_{\text{MF}} = \frac{1}{2}\sum_{\mathbf{k}} \Psi_{\mathbf{k}}^\dagger\, H_{\text{BdG}}(\mathbf{k})\, \Psi_{\mathbf{k}} + \text{const.}, \qquad H_{\text{BdG}}(\mathbf{k}) = \begin{pmatrix} \varepsilon(\mathbf{k}) & 0 & \Delta(\mathbf k) & 0 \\ 0 & \varepsilon(\mathbf k) & 0 & \Delta(\mathbf k) \\ \Delta(\mathbf k)^* & 0 & -\varepsilon(\mathbf{k}) & 0 \\ 0 & \Delta(\mathbf k)^* & 0 & -\varepsilon(\mathbf k) \end{pmatrix}, \tag{5.7}$$

where $\varepsilon(\mathbf k) = -2t(\cos k_x + \cos k_y) - \mu$ is the ordinary band dispersion, which we assume to be inversion symmetric, $\varepsilon(-\mathbf k) = \varepsilon(\mathbf k)$. This $4\times 4$ matrix is called the **Bogoliubov-de Gennes (BdG) Hamiltonian**, and in a concrete sense it is the most important object to describe the excitations of a superconductor. Note that the two diagonal entries in the lower-right part have $-\varepsilon(\mathbf k)$ and not $+\varepsilon(\mathbf k)$. This comes directly from writing $c_{-\mathbf k\sigma}^\dagger
c_{-\mathbf k\sigma}$ in terms of $c_{-\mathbf k\sigma}c_{-\mathbf k\sigma}^\dagger = 1 -
c_{-\mathbf k\sigma}^\dagger c_{-\mathbf
k\sigma}$ with the anticommutation relations. This is also where the name hole comes from, since a missing electron at $-\mathbf k$ behaves like a particle with opposite energy.

Since the spinor [(5.6)](#eq-5-6) was built with this extra minus sign, the $4\times 4$ problem in [(5.7)](#eq-5-7) is already block-diagonal. There is one $2\times 2$ block built from $(c_{\mathbf k\uparrow},
c_{-\mathbf k\downarrow}^\dagger)$ and an identical one built from $(c_{\mathbf k\downarrow},
-c_{-\mathbf
k\uparrow}^\dagger)$, and each of them has the reduced BdG matrix

$$h_{\text{BdG}}(\mathbf k) = \begin{pmatrix} \varepsilon(\mathbf k) & \Delta(\mathbf k) \\ \Delta(\mathbf k)^* & -\varepsilon(\mathbf k)\end{pmatrix}. \tag{5.8}$$

This is the structure that is shown on the slides and quoted in the lecture, a $4\times 4$ matrix for a single orbital with two spins, with diagonal entries $\varepsilon(\mathbf k)$, $\varepsilon(\mathbf k)$, $-\varepsilon(\mathbf k)$, $-\varepsilon(\mathbf k)$ and off-diagonal entries $\Delta$, but now we have derived it instead of only stating it. If we diagonalize [(5.8)](#eq-5-8), we obtain the standard BCS quasiparticle dispersion

$$E(\mathbf k) = \pm\sqrt{\varepsilon(\mathbf k)^2 + |\Delta(\mathbf k)|^2}. \tag{5.9}$$

![The Nambu doubling for a chain. (a) Without pairing the hole band is the mirror image of the electron band, and the two cross at the Fermi points. (b) A nonzero $\Delta$ opens a gap of $2|\Delta|$ at each crossing, and the two new bands mix electron and hole, which the blend of the colors shows.](figures/web/session05/nambu_bands.svg){#sch:s05:nambu_bands alt="Two panels of a cosine band. On the left an electron band and its mirrored hole band cross at two points. On the right the crossings are replaced by a gap of size two Delta."}

::: quiz
In [(5.9)](#eq-5-9) the quasiparticle energy is $E=\pm\sqrt{\varepsilon^2+|\Delta|^2}$. Where is $|E|$ smallest, and how large is it?

- [x] On the original Fermi surface, where $\varepsilon=0$, and it is $|\Delta|$.
- [ ] At the bottom of the band, and it is $|\Delta|$.
- [ ] On the original Fermi surface, and it is $2|\Delta|$.
- [ ] It has no minimum, since $E$ grows with $\Delta$ everywhere.

The energy depends on $\varepsilon$ only through $\varepsilon^2$, so $|E|$ is smallest where $\varepsilon=0$. There it is $|\Delta|$ in each branch, and the full gap between the two branches is $2|\Delta|$.
:::

::: notebookbox
**Notebook check-in:** [`session5.ipynb`](https://github.com/joselado/Advanced_Quantum_Materials_2027/blob/main/jupyter-notebooks/session5.ipynb), "Nambu electronic structure without superconductivity" and "Nambu electronic structure with superconductivity" (both Reminder)

First build the Nambu-doubled Hamiltonian of [(5.6)](#eq-5-6)-[(5.7)](#eq-5-7) with $\Delta = 0$, and check that you get exactly two copies of the same band structure. One is the physical copy, which is the electron sector, and the other is a spurious mirror copy, which is the hole sector, with dispersion $-\varepsilon(\mathbf k)$. Then turn on $\Delta$ and look at how the gap in [(5.9)](#eq-5-9) opens at every crossing between the two copies.
:::

::: {.tryit notebook="session5.ipynb" cell="Nambu electronic structure with superconductivity"}
In the cell, change `h.add_swave(0.8)` to `0.4` and then to `0.2`. The electron and hole bands anticross at the Fermi points. The smallest energy is $|\Delta|$, so the gap between the two branches is $2|\Delta|$, as in [(5.9)](#eq-5-9).
:::
