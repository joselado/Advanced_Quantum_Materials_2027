## Classifying states of matter by the symmetry that they break {#sec-1-11b number="1.11b"}

Which symmetry does a magnet break, and which one does a ferroelectric or a superconductor break? We will now see that spontaneous symmetry breaking, the topic of Section [1.11a](#sec-1-11), gives us a useful way to classify states of matter, according to *which* symmetry they break spontaneously. Each broken symmetry comes with its own quasiparticle, and broken time reversal gives the definition [(1.4)](#eq-1-4) of a magnet.

- Broken **time-reversal symmetry** gives classical magnets. The magnetization is odd under time reversal, so a magnetic ground state is not invariant when we run the movie backward.

- Broken **inversion symmetry** gives ferroelectrics. These are materials that develop an electric polarization spontaneously, which is the electric analog of a magnetization, and in this way they break the inversion symmetry of the underlying crystal.

- Broken **gauge symmetry** gives superconductors. The phase of the pairing order parameter, or equivalently the phase of the creation and annihilation operators, becomes physical once the order appears. Many observable superconducting phenomena, such as the Josephson effect, are direct consequences of fluctuations of this broken phase, and Section [5.2](#sec-5-2) comes back to them.

This classification by symmetry is useful, but it does not capture everything. Topological materials, such as topological insulators and fractional Chern insulators, can have the same broken or unbroken symmetries as an ordinary trivial material and still behave in a completely different way. The reason for this is that they differ in their topological classification and not in their symmetry classification. This difference is the topic of Session 3. For now, we only keep in mind that the question of "which symmetry is broken" does not give the full description of quantum matter.

Every case of spontaneous symmetry breaking also comes with its own emergent quasiparticle, which is the low-energy fluctuation of the order that has formed. The following table lists three cases.

::: center
  **Broken symmetry**        **Realized in**   **Quasiparticle**    **Spin**   **Charge**  **Gap**
  -------------------------- ----------------- ------------------- ---------- ------------ ----------------------------------
  Continuous translational   Crystals          Acoustic phonon         0           0       Gapless (always)
  Spin-rotational $SO(3)$    Magnets           Magnon                  1           0       Gapless (gapped with anisotropy)
  Gauge                      Superconductors   Higgs mode              0           0       Gapped
:::

Note that magnons and the Higgs mode both have zero charge but very different spin, and that only the acoustic phonon is gapless in every material. Magnons are gapless when the broken spin-rotational symmetry is continuous, and they become gapped when a magnetic anisotropy breaks this symmetry explicitly. The Higgs mode, which is an oscillation of the amplitude of the order parameter, is always gapped.

[](#sch:s01:gapless_gapped) draws the dispersion of the three quasiparticles of the table.

![The quasiparticle of each broken symmetry. The phonon, the acoustic branch of a chain with one mass per cell, is gapless, since it goes to zero at $k=0$. The magnon is gapless as well, and an easy-axis anisotropy lifts it by a gap, shown in red. The Higgs mode is gapped by the size of the order parameter. The curves are $\omega=2|\sin(k/2)|$, $\omega=1-\cos k$ plus $0.45$ for the red one, and $\omega=\sqrt{1.2^2+k^2}$. The momentum $k$ is in units of the inverse lattice constant, and $\omega$ is in arbitrary units, the same in the three panels. The phonon and the magnon are the forms of a chain, and the Higgs curve is the continuum form, drawn on the same range of $k$. Look at the value at $k=0$, which is the gap.](figures/web/session01/gapless_gapped.svg){#sch:s01:gapless_gapped alt="Three dispersions omega against k from minus pi to pi. A phonon that reaches zero at k equal to zero, a magnon that reaches zero and a copy shifted up by a gap of 0.45, and a Higgs mode that stays above a gap of 1.2."}

![The magnon of a ferromagnet, one panel shown again from Session 6. In the ordered state every spin points the same way. A magnon is a precession wave of all the spins, which is the low-energy fluctuation of the order.](figures/s06f05_magnon.svg){panel="side" alt="A row of parallel spins, and below it a row of spins that precess with a phase that advances from site to site."}

::: quiz
A magnet has an easy-axis anisotropy, which breaks the spin-rotational symmetry explicitly. What happens to the magnon?

- [x] It acquires a gap.

    This is true. A gapless mode needs a continuous symmetry that is broken only spontaneously. The anisotropy breaks it by hand, so tilting the spins costs a finite energy.

- [ ] It stays gapless, since the order is still there.

    This is false. In the Ising limit the spins can point only up or down, and the order is perfect. Flipping a single spin still costs a finite energy, so there is a gap.

- [ ] It turns into a phonon.

    This is false. If the atoms are held fixed there are no phonons at all, yet the spin flip of the Ising limit remains, with a finite energy. The anisotropy changes the energy of the magnon and not its nature.

The order stays, and the Goldstone mode is gapped.
:::

::: quiz
Each picture shows a dispersion $\omega(k)$ of a quasiparticle of a chain. Which one is a magnon with an easy-axis anisotropy?

- [ ] ![A curve omega against k that starts at zero at k equal to zero, rises as k squared near zero and flattens at 2 at the edges of the zone.](figures/web/session01/g3_quiz_disp_magnon.svg)

    This is false. The curve is $\omega=1-\cos k$, which is $0$ at $k=0$, so it has no gap. It rises as $k^2/2$, which is the magnon of the ferromagnet with no anisotropy.

- [x] ![A curve omega against k that starts at 0.45 at k equal to zero, rises as k squared near zero and flattens at 2.45 at the edges of the zone.](figures/web/session01/g3_quiz_disp_magnon_gap.svg)

    This is true. The curve is $\omega=1-\cos k+0.45$, which is $0.45$ at $k=0$. This is the gap of the magnon, since with the anisotropy a tilt of all the spins costs a finite energy.

- [ ] ![A curve omega against k that starts at zero at k equal to zero with a sharp V and rises to 2 at the edges of the zone.](figures/web/session01/g3_quiz_disp_phonon.svg)

    This is false. The curve is $\omega=2|\sin(k/2)|$, which is $0$ at $k=0$ and rises linearly, as $|k|$. This is the phonon of a chain of masses, which is a sound wave.

The gap is read at $k=0$, where the curve has its lowest value.
:::

Since we cannot run time backward in the lab to check if a material breaks time-reversal symmetry, we measure instead quantities that are themselves odd under time reversal. Two of them are especially useful. The first one is the **Hall conductivity**, which is a transverse current generated by a longitudinal voltage, in its antisymmetric part $\sigma_{xy}=-\sigma_{yx}$. The second one is the **magneto-optical Kerr effect**, which is a different optical reflection for left-handed and right-handed circularly polarized light. A nonzero signal in either of them at zero applied magnetic field is direct evidence of broken time-reversal symmetry.

::: quiz
A material shows a nonzero Kerr rotation without any applied magnetic field. What do we conclude?

- [x] Time-reversal symmetry is broken in the ground state.

    This is true. The Kerr signal is odd under time reversal, so it can be nonzero only if the state is not invariant under $\hat T$. This is the experimental version of the test in [(1.4)](#eq-1-4).

- [ ] Inversion symmetry is broken in the ground state.

    This is false. A nonmagnetic crystal without inversion, such as GaAs, breaks inversion and keeps $\hat T$. It shows no Kerr rotation at zero field.

- [ ] The material is a superconductor.

    This is false. Iron has a remanent magnetization and a Kerr rotation at zero field, and it is not a superconductor. An ordinary s-wave superconductor, such as aluminum, keeps $\hat T$ and has no Kerr rotation.

The Kerr rotation measures the breaking of time reversal, and not of other symmetries.
:::

With this we can finally give a precise and formal definition of a magnet, which goes beyond "the object that sticks to your fridge".

::: key
A magnet is a many-body state whose wave function is not invariant under the time-reversal operator $\hat T$,

$$\hat T|\Psi\rangle = |\Psi\rangle \;\Rightarrow\; \text{not magnetic}, \qquad
\hat T|\Psi\rangle \neq |\Psi\rangle \;\Rightarrow\; \text{magnetic}. \tag{1.4}$$

So time reversal changes a magnet, and a state that it leaves the same is not magnetic. A magnetization is odd under $\hat T$, so a state with a magnetization fails this test.
:::

In [(1.4)](#eq-1-4) equal means equal up to a phase, and the test is for an even number of electrons, since for an odd number $\hat T^2=-1$ and no state passes.

The north and south poles of a bar magnet are exchanged under time reversal, since a magnetic pole is connected to an orbital angular momentum and angular momenta change sign under $\hat T$. For this reason a bar magnet does not pass the invariance test in [(1.4)](#eq-1-4), and it is magnetic according to this definition. A plain stick that is not magnetic, on the other hand, looks the same under time reversal and passes the test.

::: lab
Magneto-optical Kerr effect microscopy shows that monolayer chromium triiodide, CrI$_3$, is an Ising ferromagnet, with its spins out of the plane. Its Curie temperature is $45$ K, only slightly lower than the $61$ K of the bulk crystal. Our reading is that below $45$ K the monolayer is magnetic in the sense of [(1.4)](#eq-1-4), and that its Kerr rotation probes this broken time reversal when it stays at zero applied field. The measurement is in [this article](https://www.nature.com/articles/nature22391).
:::

:::: problem
Time reversal of one spin is $\hat T=i\sigma_yK$, where $K$ takes the complex conjugate of the coefficients in the basis $|{\uparrow}\rangle$, $|{\downarrow}\rangle$ of $\sigma_z$. On two spins $\hat T$ acts on each spin. Show that the singlet $(|{\uparrow\downarrow}\rangle-|{\downarrow\uparrow}\rangle)/\sqrt2$ passes the test [(1.4)](#eq-1-4), and that the Néel state $|{\uparrow\downarrow}\rangle$ does not.

::: solution
With the Pauli matrix $\sigma_y$, the operator $i\sigma_y$ is the real matrix

$$i\sigma_y=\begin{pmatrix}0&1\\-1&0\end{pmatrix},$$

so $\hat T|{\uparrow}\rangle=-|{\downarrow}\rangle$ and $\hat T|{\downarrow}\rangle=|{\uparrow}\rangle$, since $K$ does nothing to real coefficients. On two spins this gives $\hat T|{\uparrow\downarrow}\rangle=-|{\downarrow\uparrow}\rangle$ and $\hat T|{\downarrow\uparrow}\rangle=-|{\uparrow\downarrow}\rangle$. For the singlet

$$\hat T\,\frac{|{\uparrow\downarrow}\rangle-|{\downarrow\uparrow}\rangle}{\sqrt2}=\frac{-|{\downarrow\uparrow}\rangle+|{\uparrow\downarrow}\rangle}{\sqrt2},$$

which is the singlet again, so it passes the test and it is not magnetic. Its moment $m=n_\uparrow-n_\downarrow$ is zero on each site. The Néel state $|{\uparrow\downarrow}\rangle$ goes to $-|{\downarrow\uparrow}\rangle$, which is orthogonal to it, so it is another state and it fails the test. Its moment is $m=1$ on the first site, and after $\hat T$ it is $m=-1$.

This is the difference between the exact ground state of the Hubbard dimer and its mean-field state in [](#sch:s01:dimer_meanfield). The exact ground state is a singlet with $m=0$ for every $U$, and at large $U$ it has one electron on each site, with the spins in this singlet. The antiferromagnetic mean field gives a moment $m$ on the first site and $-m$ on the second for $U>2t$, and $\hat T$ changes the sign of $m$. So the mean-field state breaks time reversal, while the exact ground state of two sites does not, as Section [1.11a](#sec-1-11) explains for a finite system.
:::
::::

Let us now build this general picture explicitly, three times.

::: {.tryit notebook="session1.ipynb" cell="Magnetic order driven by interactions in a chain"}
Run the cell and look at the arrows in the panel of the antiferromagnetic guess, which show the exchange field, so each arrow points against the moment of its site. Check that they alternate in sign from one site to the next. Time reversal flips every arrow, which gives another state with the same energy.
:::

::: comesback
- The magnon of the table is built in Section [6.13](#sec-6-13), and Section [6.15](#sec-6-15) shows that it is gapless, since it is the Goldstone mode of the broken spin rotation.
- The materials with the same symmetries and a different topology are the topic of Session 3, with the bulk-boundary correspondence of Section [3.7](#sec-3-7).
- The Hall conductivity comes back in Section [3.4](#sec-3-4), where linear response gives it, and in Session 4, where it is quantized.
:::
