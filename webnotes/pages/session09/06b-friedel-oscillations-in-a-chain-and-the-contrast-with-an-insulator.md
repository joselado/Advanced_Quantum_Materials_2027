## Friedel oscillations in a chain, and the contrast with an insulator {#sec-9-6b number="9.6b"}

In the first part we derived the Friedel oscillation from the singularity of $\chi_0(q)$. Let us now look at it in a chain.

For a concrete example, let us take a one-dimensional tight-binding chain with an impurity at site $0$. The local density of states oscillates around the impurity with wavelength $\pi/k_F$, which is half of the Fermi wavelength $\lambda_F=2\pi/k_F$, since the modulation is set by $2k_F$ and not by $k_F$. If we raise the chemical potential, $k_F^{-1}$ becomes shorter and the oscillation becomes faster in the same way. The same phenomenon, with the same physical content, appears in a two-dimensional square lattice. This real-space LDOS modulation around impurities is what an STM measures in practice, and it is quasiparticle interference again, seen this time in real space and not in reciprocal space. In [](#sch:s09:friedel) we see the density along the chain at two fillings, and the oscillation is faster for the larger $k_F$. The same is seen in two dimensions in [](#sch:s09:friedel2d) of the first part. As a complementary check, the notebook also shows the *insulating* case. An impurity placed in a gapped 1D chain gives an LDOS that converges very quickly to its uniform value, instead of oscillating with a slow power-law envelope. This is a first view of the diagnostic that separates gapped and gapless systems, which we will make fully general in Section [9.9](#sec-9-9) and draw in Figure [9.5](#fig:s09:decay).

![The density induced by one impurity of strength $v_0=t$ in a chain of 4001 sites, from exact diagonalization, for two chemical potentials. The period is $\pi/k_F$, so the lower filling on the left gives the longer period. The grey lines are an envelope $1/x$, as [(9.9)](#eq-9-9) gives for $d=1$, and the points follow it after the first few sites.](figures/web/session09/friedel.svg){#sch:s09:friedel alt="Two plots of the density change along a chain, an oscillation with a decaying envelope, slower in the left plot and faster in the right plot."}

::: quiz
In a gapped chain the LDOS around an impurity converges to its bulk value within a few sites. Why is there no slowly decaying oscillation?

- [ ] The impurity is screened completely by the electrons at the Fermi level.

    This is false. A metal screens the impurity well, and it still has Friedel oscillations at $2k_F$. Screening does not remove the tail, and in the gap there are no electrons at the Fermi level to screen.

- [x] There is no Fermi surface, so $\chi_0(q)$ has no singularity and its Fourier transform decays exponentially.

    This is true. A gap makes $\chi_0(q)$ analytic for all $q$, so its Fourier transform decays as $e^{-x/\xi}$. For $\xi\approx2.5$ sites the response at ten sites is $e^{-4}\approx0.02$ of its starting value.

- [ ] A gapped chain has no translational symmetry.

    This is false. A dimerized chain with hoppings $t_1\neq t_2$ is gapped and has translational symmetry with a two-site cell. Its LDOS around an impurity still decays exponentially.
:::

::: {.tryit notebook="session9.ipynb" cell="Impurity in a 1d metal"}
The cell uses `mus = [1.95,1.7]`. The Fermi level is close to the bottom of the band, so $k_F$ is measured from the minimum. The ripples have a period of about 14 sites for `1.95` and about 5.7 sites for `1.7`, which is $\pi/k_F$. Replace `1.7` by `1.0` and check that the period becomes 3 sites.
:::

::: notebookbox
**Notebook check-in:** [`session9.ipynb`](https://github.com/joselado/Advanced_Quantum_Materials_2027/blob/main/jupyter-notebooks/session9.ipynb), "Impurity in a 1d metal" (Core), "Impurities in a 2d metal" (Core), and "Impurity in an electronic insulator" (Core)

Place a single impurity in a 1D chain, and then in a 2D square lattice, and look at how the LDOS oscillates as in [(9.9)](#eq-9-9). Change the chemical potential and check that the wavelength of the oscillation follows $\pi/k_F$, as predicted. This is the clearest place in the whole session to see a response formula and a numerical experiment agree digit by digit. The third section repeats the exercise with the chemical potential inside a gap, instead of in a partially filled band. Check that the LDOS now converges to its bulk value within one or two sites, without an oscillating tail that decays slowly. This is the contrast between gapped and gapless systems that Section [9.9](#sec-9-9) makes fully general.
:::

::: comesback
- In Section [9.9](#sec-9-9) the contrast between the metal and the insulator becomes a general diagnostic, a power law for a gapless state and an exponential for a gapped one.
- In Section [9.10](#sec-9-10) a quasiperiodic or random onsite potential on every site changes the eigenstates of the chain themselves.
:::
