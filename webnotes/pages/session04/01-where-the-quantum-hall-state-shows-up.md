## Where the quantum Hall state shows up {#sec-4-1 number="4.1"}

The quantum Hall state is not the property of one specific material. It is a state of matter that a whole family of two-dimensional electron systems can realize, and each of these systems has its own energy scale and temperature scale.

- **Semiconductor quantum wells**, historically gallium arsenide (GaAs), were the first platform. In these systems the electrons are essentially parabolic electrons, with the ordinary quadratic dispersion, and the relevant energy scale grows linearly with the magnetic field. For the fields that we can reach in a laboratory this gives roughly one millielectronvolt, and this is the reason why quantum Hall physics in GaAs needs temperatures of the order of one kelvin.

- **Two-dimensional materials**, and graphene above all, realize the same physics but with Dirac electrons instead of parabolic ones. As we will derive explicitly below, the energy scale then grows as the square root of the field and not linearly. The slides give the concrete numbers, which are roughly two orders of magnitude larger, around 100 millielectronvolts. This is high enough that the quantum Hall plateaus of graphene survive up to about 100 K, and in the best samples up to almost room temperature.

For all these platforms the common point is the one we already saw in the last session. An observable, the Hall conductance, is exactly quantized, and this quantization comes from topology and not from the chemistry of a specific material.

![The two platforms of this section, seen through the energy scale of their Landau levels. In (a) the levels of parabolic electrons grow linearly with the field. In (b) the levels of Dirac electrons grow as the square root of the field, and the level at zero energy does not move. Look at how the levels of (b) are more widely spaced than a straight line would give at small field. We derive both ladders in Sections [4.9](#sec-4-9) and [4.10](#sec-4-10).](figures/s04f04_ladders.svg){alt="Two fans of Landau levels against the magnetic field, straight lines for parabolic electrons and square-root curves for Dirac electrons."}

::: quiz
The Landau level spacing of GaAs grows as $B$ and that of graphene as $\sqrt{B}$. By which factors do the two spacings grow if we multiply the field by 4?

- [x] By 4 for GaAs and by 2 for graphene.
- [ ] By 2 for GaAs and by 2 for graphene.
- [ ] By 4 for GaAs and by 4 for graphene.
- [ ] By 2 for GaAs and by 4 for graphene.

A linear law multiplies the spacing by the same factor as the field. A square-root law multiplies it by the square root of that factor.
:::

## Measuring the Hall conductance {#sec-4-2 number="4.2"}

The experiment itself is simple to describe. We take a two-dimensional system, apply a voltage along one in-plane direction, which we call $y$, and measure the current that flows along the perpendicular in-plane direction, $x$. The ratio of this transverse current to the applied voltage is the Hall conductance, and this is the quantity that becomes quantized in the quantum Hall regime.

A real device for this measurement is a two-dimensional electron gas (2DEG) with several finger gates in contact with it. A voltage is applied between a top gate and a bottom gate, and the current is measured between two gates placed along $x$, with all the connections made through metallic leads. The geometry of the device does not add new physics beyond what we need for the concepts, so we will not discuss it further. The device figures in the slides are useful to see how a real experiment looks, but from here on the notes work with the ideal two-dimensional system.

::: quiz
Why do the quantum Hall plateaus of graphene survive to a much higher temperature than those of a GaAs quantum well?

- [x] The spacing between its Landau levels is about two orders of magnitude larger. A much higher thermal energy is then needed to mix the levels.
- [ ] The Hall conductance of graphene is larger.
- [ ] Graphene has more Landau levels below the chemical potential.
- [ ] Graphene has no disorder.

A plateau needs the thermal energy to be small compared with the gap between Landau levels. The larger gap of graphene, around 100 meV, keeps this true up to about 100 K.
:::
