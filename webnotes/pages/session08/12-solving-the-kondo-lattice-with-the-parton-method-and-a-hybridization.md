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
