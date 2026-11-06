## The parton construction with Abrikosov fermions and the single-occupancy constraint {#sec-8-8 number="8.8"}

The construction that allows us to treat QSL excitations does not write each spin as a bosonic fluctuation around an ordered reference state. Instead, it writes each spin with an auxiliary **fermion** field $f_{i\sigma}$ ($\sigma=\uparrow,\downarrow$) on every site. This is a particle with spin $1/2$ and no electric charge, which is the spinon of Section [8.2](#sec-8-2), now written in a formal way. These particles are called **Abrikosov fermions**, and the operator identity that defines the parton transformation is

$$\mathbf S_i = \frac12 \sum_{\alpha\beta} f_{i\alpha}^\dagger\, \boldsymbol\sigma_{\alpha\beta}\,
f_{i\beta}, \tag{8.10}$$

where $\boldsymbol\sigma$ is the vector of Pauli matrices. One can check directly, from the anticommutation relations of the fermions, that [(8.10)](#eq-8-10) gives the correct $SU(2)$ spin algebra $[S_i^a,S_i^b] = i\varepsilon^{abc}S_i^c$ on the full Fock space of $f_{i\uparrow},f_{i\downarrow}$, which has four states, namely empty, singly occupied with spin up, singly occupied with spin down and doubly occupied. No extra input is needed for this. The problem is that this transformation makes the local Hilbert space *artificially larger*, since a physical spin-$1/2$ has only two states, while $f_{i\uparrow},f_{i\downarrow}$ give four. We remove the two extra unphysical states, which are the empty and the doubly occupied ones and which [(8.10)](#eq-8-10) maps to $\mathbf S_i=0$ in any case. We do this by imposing by hand the **single-occupancy constraint**

$$\sum_\sigma f_{i\sigma}^\dagger f_{i\sigma} = 1 \qquad \text{at every site } i. \tag{8.11}$$

This is the fermionic analogue of the Gutzwiller projection [(8.7)](#eq-8-7) that we applied before to the many-body wavefunction. To project the many-body state onto the singly-occupied subspace and to fix the fermion filling to one per site are the same statement, the first one seen from the side of the wavefunction and the second one from the side of the operators. Figure [8.4](#fig:s08:parton)a shows which two states the constraint has to remove, and why they were never spin states in the first place.

When [(8.11)](#eq-8-11) holds, [(8.10)](#eq-8-10) is an *exact* way to write a spin-$1/2$ operator in the language of fermions, and we can put it directly into the Heisenberg Hamiltonian $\mathcal H=\sum_{\langle
ij\rangle}J_{ij}\,\mathbf S_i\cdot\mathbf S_j$. With the Fierz identity for Pauli matrices $\sum_a \sigma^a_{\alpha\beta}\sigma^a_{\gamma\delta} = 2\delta_{\alpha\delta}\delta_{\beta\gamma} -
\delta_{\alpha\beta}\delta_{\gamma\delta}$ and the constraint [(8.11)](#eq-8-11) on both sites, we obtain the simple identity

$$\mathbf S_i \cdot \mathbf S_j = \frac14 - \frac12\, \chi_{ij}^\dagger \chi_{ij}, \qquad \chi_{ij}
\equiv \sum_\sigma f_{i\sigma}^\dagger f_{j\sigma}, \tag{8.12}$$

where $\chi_{ij}$ is the spinon bond operator, or hopping operator, between sites $i$ and $j$. When we insert [(8.12)](#eq-8-12), the original Heisenberg Hamiltonian, which is bilinear in the spins, becomes a Hamiltonian that is *quartic* in the auxiliary fermions,

$$\mathcal H = \sum_{\langle ij\rangle} J_{ij}\left(\frac14 - \frac12\,\chi_{ij}^\dagger\chi_{ij}\right)
= \text{const} - \frac12\sum_{\langle ij\rangle} J_{ij}\, \chi_{ij}^\dagger \chi_{ij}. \tag{8.13}$$

This is the same problem that we had in Sessions 1 and 6 with the Hubbard interaction, which is a quartic term that we cannot diagonalize directly. We treat it in the same way, with a **mean-field decoupling**,

$$\chi_{ij}^\dagger\chi_{ij} \;\approx\; \langle\chi_{ij}^\dagger\rangle\,\chi_{ij} +
\chi_{ij}^\dagger\,\langle\chi_{ij}\rangle - |\langle\chi_{ij}\rangle|^2. \tag{8.14}$$
