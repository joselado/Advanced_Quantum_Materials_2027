## Fractional filling and the Laughlin wavefunction {#sec-4-16 number="4.16"}

Let us now say that we want to occupy only a fraction of the available LLL orbitals, for example two out of every three, but in a way that keeps the electron gas uniform. If we only leave some orbitals empty, we obtain a density that is clearly not uniform and has lumps, since each empty orbital is at its own fixed radius. We look for a many-body wavefunction with three properties. First, it still lives only in the LLL, so it is built only from the coordinates $z_i$ and never from $\bar z_i$. Second, it is still antisymmetric, since the particles are still electrons. Third, in a heuristic sense, it keeps the electrons as far from each other as possible, since this is what a repulsive Coulomb interaction favors when we minimize its energy.

The construction that satisfies the three conditions at the same time is very simple. We take the wavefunction of the filled LLL [(4.11)](#eq-4-11) and we raise the Vandermonde factor to a power,

$$\Psi_m(z_1,\dots,z_N) = \prod_{i<j}(z_i-z_j)^m\; \exp\!\left(-\sum_i \frac{|z_i|^2}{4\ell_B^2}\right), \tag{4.12}$$

which is called the **Laughlin wavefunction**. The exponent $m$ must be an odd integer, since an even power would make the wavefunction *symmetric* and not antisymmetric under exchange, and this is not allowed for fermions. A larger exponent makes the electrons avoid each other more, since the wavefunction now vanishes to $m$-th order, and not only linearly, when two electrons are at the same point, and this is the correlation effect that we wanted. When we compute the electron density that follows from it, we obtain the filling factor

$$\nu = \frac{1}{m}, \tag{4.13}$$

which we can also see directly by counting. The maximum power of any single coordinate in the fully expanded polynomial [(4.12)](#eq-4-12) is $m(N-1)$, so the wavefunction uses the angular-momentum orbitals up to $m(N-1)$. This means that $N$ electrons are spread over $\approx m(N-1)+1 \approx
mN$ available LLL orbitals, which gives a filling fraction of $N/(mN)=1/m$, in agreement with [(4.13)](#eq-4-13). So we start only from the single-particle LLL orbitals, the Pauli exclusion principle and a heuristic argument about correlations, and we arrive at the exact ground state of a strongly interacting many-body problem, which will give us fractional charge in the next section.
