## Where the quantum Hall state shows up {#sec-4-1 number="4.1"}

The quantum Hall state is not the property of one specific material. It is a state of matter that a whole family of two-dimensional electron systems can realize, and each of these systems has its own energy scale and temperature scale.

- **Semiconductor quantum wells**, historically gallium arsenide (GaAs), were the first platform. In these systems the electrons are essentially parabolic electrons, with the ordinary quadratic dispersion, and the relevant energy scale grows linearly with the magnetic field. For the fields that we can reach in a laboratory this gives roughly one millielectronvolt, and this is the reason why quantum Hall physics in GaAs needs temperatures of the order of one kelvin.

- **Two-dimensional materials**, and graphene above all, realize the same physics but with Dirac electrons instead of parabolic ones. As we will derive explicitly below, the energy scale then grows as the square root of the field and not linearly. The slides give the concrete numbers, which are roughly one order of magnitude larger, around 100 millielectronvolts at 10 T. This is high enough that the quantum Hall plateaus of graphene survive up to about 100 K, and in the best samples up to almost room temperature.

For all these platforms the common point is the one we already saw in the last session. An observable, the Hall conductance, is exactly quantized, and this quantization comes from topology and not from the chemistry of a specific material.

![The two platforms of this section, seen through the energy scale of their Landau levels. In (a) the levels of parabolic electrons grow linearly with the field. In (b) the levels of Dirac electrons grow as the square root of the field, and the level at zero energy does not move. Look at how the levels of (b) are more widely spaced than a straight line would give at small field. We derive both ladders in Sections [4.9](#sec-4-9) and [4.10](#sec-4-10).](figures/s04f04_ladders.svg){alt="Two fans of Landau levels against the magnetic field, straight lines for parabolic electrons and square-root curves for Dirac electrons."}

::: quiz
The Landau level spacing of GaAs grows as $B$ and that of graphene as $\sqrt{B}$. By which factors do the two spacings grow if we multiply the field by 4?

- [ ] By 2 for GaAs and by 2 for graphene.

    This is false. The GaAs spacing $\hbar\omega_c$ is about $1.7$ meV at 1 T and $6.9$ meV at 4 T, which is a factor 4 and not 2.

- [x] By 4 for GaAs and by 2 for graphene.

    This is true. A linear law multiplies the spacing by the same factor as the field, and a square-root law by its square root. For graphene, $E_1$ goes from about 36 meV at 1 T to 73 meV at 4 T.

- [ ] By 2 for GaAs and by 4 for graphene.

    This is false. This swaps the two laws. The graphene level $E_1\approx 36\,\mathrm{meV}\sqrt{B/\mathrm{T}}$, for $v=10^6$ m/s, is 36 meV at 1 T and 73 meV at 4 T, a factor 2 and not 4.

:::

## Measuring the Hall conductance {#sec-4-2 number="4.2"}

The experiment itself is simple to describe. We take a two-dimensional system, apply a voltage along one in-plane direction, which we call $y$, and measure the current that flows along the perpendicular in-plane direction, $x$. The ratio of this transverse current to the applied voltage is the Hall conductance, and this is the quantity that becomes quantized in the quantum Hall regime.

The geometry that we have in mind is the one in [](#sch:s04:hall_setup), a square sample with four contacts.

![The geometry of the measurement, for a square sample with four contacts and a field into the page. A voltage $V_y$ is applied between the top and the bottom contact, and the current $I_x$ is read in the left contact. With $N$ filled Landau levels the current is carried by the $N$ chiral channels of the edge, which circulate around the sample in one sense. The channels that leave the top contact end in the next contact, so $I_x=N(e^2/h)V_y$. Look at the sense of the arrows, which reverses when the field reverses.](figures/web/session04/hall_setup.svg){#sch:s04:hall_setup alt="A square sample with four contacts, a voltage applied between the top and the bottom contact, a current leaving the left contact and arrows that circulate along the edge."}

A real device for this measurement is a two-dimensional electron gas (2DEG) with several finger gates in contact with it. A voltage is applied between a top gate and a bottom gate, and the current is measured between two gates placed along $x$, with all the connections made through metallic leads. The geometry of the device does not add new physics beyond what we need for the concepts, so we will not discuss it further. The device figures in the slides are useful to see how a real experiment looks, but from here on the notes work with the ideal two-dimensional system.

::: quiz
Why do the quantum Hall plateaus of graphene survive to a much higher temperature than those of a GaAs quantum well?

- [ ] The Hall conductance of graphene is larger.

    This is false. The plateau at $2e^2/h$ has the same value in GaAs and in graphene, and the value is an integer times $e^2/h$ in both. What differs is the temperature up to which it survives.

- [x] The spacing between its Landau levels is several times larger. A much higher thermal energy is then needed to mix the levels.

    This is true. At 10 T the GaAs spacing is about 17 meV and the first graphene gap is about 115 meV, roughly seven times larger. The plateau needs the thermal energy to be small compared with the gap.

- [ ] Graphene has no disorder.

    This is false. Graphene on a substrate has charge puddles and impurities, and the plateaus survive anyway. What matters is a large gap to the next level, and not the absence of disorder.

:::
