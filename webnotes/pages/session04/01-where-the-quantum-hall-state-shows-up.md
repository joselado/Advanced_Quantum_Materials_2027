## Where the quantum Hall state shows up {#sec-4-1 number="4.1"}

Why does the same quantized Hall conductance appear in GaAs and in graphene, but up to very different temperatures? We will see that the value of the plateau is fixed by topology. The material sets the spin and valley degeneracy of the Landau levels and their spacing, which grows as $B$ in GaAs and as $\sqrt{B}$ in graphene.

::: {.recall eq="3.4"}
This is the Hall conductivity of a set of filled bands, from Section [3.5](#sec-3-5). The Chern number $C$ is the integral of the Berry curvature $\Omega_n$ of the filled bands over the Brillouin zone, divided by $2\pi$. It is built from the wavefunctions only, and for a gapped system it is an integer.
:::

The quantum Hall state is not the property of one specific material. It is a state of matter that a whole family of two-dimensional electron systems can realize, and each of these systems has its own energy scale and temperature scale.

- **Semiconductor quantum wells**, historically gallium arsenide (GaAs), were the first platform. In these systems the electrons are essentially parabolic electrons, with the ordinary quadratic dispersion, and the relevant energy scale grows linearly with the magnetic field. For the fields that we can reach in a laboratory this gives roughly one millielectronvolt, and this is the reason why quantum Hall physics in GaAs needs temperatures of the order of one kelvin.

- **Two-dimensional materials**, and graphene above all, realize the same physics but with the Dirac electrons of Section [2.11](#sec-2-11) instead of parabolic ones. As we derive in Section [4.10](#sec-4-10), the energy scale then grows as the square root of the field and not linearly. It is roughly one order of magnitude larger, around 100 millielectronvolts at 10 T. This is high enough that the quantum Hall plateaus of graphene survive up to about 100 K, and in the best samples up to almost room temperature.

For all these platforms the common point is the one of equation [(3.4)](#eq-3-4). An observable, the Hall conductance, is quantized to an integer times $e^2/h$, and this quantization comes from topology and not from the chemistry of a specific material.

![The two platforms of this section, seen through the energy scale of their Landau levels. In (a) the levels of parabolic electrons grow linearly with the field. In (b) the levels of Dirac electrons grow as the square root of the field, and the level at zero energy does not move. Look at how the levels of (b) are more widely spaced than a straight line would give at small field. We derive both ladders in Sections [4.9](#sec-4-9) and [4.10](#sec-4-10).](figures/s04f04_ladders.svg){alt="Two fans of Landau levels against the magnetic field, straight lines for parabolic electrons and square-root curves for Dirac electrons."}

To put numbers on the two ladders, [](#sch:s04:g1_energy_scales) shows the spacing of the levels of GaAs and the first level of graphene against the field, with the constants of the two materials.

![The energy scale of the Landau levels of the two platforms against the magnetic field $B$, with the energies in meV and the field in tesla. For GaAs it is the level spacing $\hbar\omega_c=\hbar eB/m^*$, with the effective mass $m^*=0.067\,m_e$, which grows linearly, from $1.73$ meV at $1$ T to $17.3$ meV at $10$ T. For graphene it is the first level $E_1=v\sqrt{2\hbar eB}$ above the level at zero energy, with the velocity $v=10^6$ m/s, which grows as $\sqrt{B}$, from $36.3$ meV at $1$ T to $115$ meV at $10$ T. Look at the ratio of the two curves, which is $21$ at $1$ T and $6.6$ at $10$ T, since it falls as $1/\sqrt{B}$.](figures/web/session04/g1_energy_scales.svg){#sch:s04:g1_energy_scales alt="Two curves of the energy against the magnetic field from 0 to 10 T, a straight blue line for GaAs that reaches 17 meV and a red square-root curve for graphene that reaches 115 meV, with dots at 1, 4 and 10 T."}

::: lab
In graphene the spacing of the lowest levels is large, and the abstract of the article below calls this promising for a standard of electrical resistance. In a large device of graphene grown on SiC, the Hall resistance is quantized within $1\times10^{-9}$ for fields down to $3.5$ T, and also at temperatures as high as $10$ K. The abstract lists these as separate conditions, and it does not say that they hold at the same time. That this spacing is the $E_1$ of [](#sch:s04:g1_energy_scales) is our reading. The measurement is in [this article](https://arxiv.org/abs/1504.06511).
:::

::: quiz
The two energy scales of the Landau levels are

$$\hbar\omega_c=\frac{\hbar eB}{m^*}\ \text{(GaAs)},\qquad E_1=v\sqrt{2\hbar eB}\ \text{(graphene)}.$$

Here $m^*$ is the effective mass of GaAs and $v$ the velocity of graphene. We multiply $B$ by 4. How do the two scales change?

- [ ] $\hbar\omega_c\to2\hbar\omega_c$ and $E_1\to2E_1$

    This is false. For $m^*=0.067\,m_e$ the GaAs spacing $\hbar\omega_c$ is about $1.7$ meV at 1 T and $6.9$ meV at 4 T, which is a factor 4 and not 2.

- [x] $\hbar\omega_c\to4\hbar\omega_c$ and $E_1\to2E_1$

    This is true. A linear law multiplies the spacing by the same factor as the field, and a square-root law by its square root. For graphene with $v=10^6$ m/s, $E_1$ goes from about 36 meV at 1 T to 73 meV at 4 T.

- [ ] $\hbar\omega_c\to2\hbar\omega_c$ and $E_1\to4E_1$

    This is false. This swaps the two laws. The graphene level $E_1\approx 36\,\mathrm{meV}\sqrt{B/\mathrm{T}}$, for $v=10^6$ m/s, is 36 meV at 1 T and 73 meV at 4 T, a factor 2 and not 4.

:::

## Measuring the Hall conductance {#sec-4-2 number="4.2"}

The experiment itself is simple to describe. We take a two-dimensional system, apply a voltage along one in-plane direction, which we call $y$, and measure the current that flows along the perpendicular in-plane direction, $x$. The ratio of this transverse current to the applied voltage is the Hall conductance, and this is the quantity that becomes quantized in the quantum Hall regime.

The geometry that we have in mind is the one in [](#sch:s04:hall_setup), a square sample with four contacts.

![The geometry of the measurement, for a square sample with four contacts and a field into the page. A voltage $V_y$ is applied between the top and the bottom contact, and the current $I_x$ is read in the left contact. With $N$ filled Landau levels the current is carried by the $N$ chiral channels of the edge, which circulate around the sample in one sense. The channels that leave the top contact end in the next contact, so $I_x=N(e^2/h)V_y$. Look at the sense of the arrows, which reverses when the field reverses.](figures/web/session04/hall_setup.svg){#sch:s04:hall_setup alt="A square sample with four contacts, a voltage applied between the top and the bottom contact, a current leaving the left contact and arrows that circulate along the edge."}

A real device for this measurement is a two-dimensional electron gas (2DEG) with several finger gates in contact with it. A voltage is applied between a top gate and a bottom gate, and the current is measured between two gates placed along $x$, with all the connections made through metallic leads. The geometry of the device does not add new physics beyond what we need for the concepts, so we will not discuss it further. From here on we work with the ideal two-dimensional system.

::: quiz
The quantum Hall plateaus of graphene survive to much higher temperatures than those of GaAs. Why?

- [ ] The Hall conductance of graphene is larger.

    This is false. The plateau at $2e^2/h$ has the same value in GaAs and in graphene, and the value is an integer times $e^2/h$ in both. What differs is the temperature up to which it survives.

- [x] The spacing between its Landau levels is several times larger. A much higher thermal energy is then needed to mix the levels.

    This is true. At 10 T the GaAs spacing is about 17 meV and the first graphene gap is about 115 meV, roughly seven times larger. The plateau needs the thermal energy to be small compared with the gap.

- [ ] Graphene has no disorder.

    This is false. Graphene on a substrate has charge puddles and impurities, and the plateaus survive anyway. What matters is a large gap to the next level, and not the absence of disorder.

:::

:::: problem
Compute the level spacing $\hbar\omega_c=\hbar eB/m^*$ of GaAs, with $m^*=0.067\,m_e$, and the first level $E_1=v\sqrt{2\hbar eB}$ of graphene, with $v=10^6$ m/s, both at $B=10$ T. Give each one in meV and as a temperature $E/k_B$, and give their ratio.

::: solution
For GaAs we put the numbers in SI units,

$$\hbar\omega_c=\frac{(1.055\times10^{-34}\,\mathrm{J\,s})(1.602\times10^{-19}\,\mathrm{C})(10\,\mathrm{T})}{0.067\times9.109\times10^{-31}\,\mathrm{kg}}=2.77\times10^{-21}\,\mathrm{J}=17.3\,\mathrm{meV}.$$

With $k_B=8.617\times10^{-5}$ eV/K this is $201$ K. For graphene the square root is $\sqrt{2\hbar eB}=1.84\times10^{-26}$ kg m/s, and we multiply it by $v$,

$$E_1=(10^6\,\mathrm{m/s})(1.84\times10^{-26}\,\mathrm{kg\,m/s})=1.84\times10^{-20}\,\mathrm{J}=115\,\mathrm{meV},$$

which is about $1330$ K. The ratio is $115/17.3=6.6$.

These temperatures are not the temperatures where the plateaus disappear. A plateau needs the thermal energy to be much smaller than the gap, and disorder broadens the levels, so the plateaus are lost far below them. What the numbers give is the ratio, meaning that at 10 T the gap of graphene is 6.6 times larger than the spacing of GaAs, and this is why its plateaus survive to higher temperatures.
:::
::::

::: comesback
- In Sections [4.9](#sec-4-9) and [4.10](#sec-4-10) we derive the two ladders of Landau levels, linear in $B$ and as $\sqrt{B}$.
- In Section [4.20](#sec-4-20) the quantized Hall conductance appears at zero field, in real materials.
- In Section [5.2](#sec-5-2) the flux quantum $h/2e$ of a superconductor is a second macroscopic readout of $e$ and $h$, next to the plateaus of this section.
:::
