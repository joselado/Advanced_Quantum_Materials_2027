## A tour of the quantum materials we will meet {#sec-1-2 number="1.2"}

Let us first give a short preview of the materials that this formalism will allow us to understand, so that the abstract tools of this session have concrete targets.

- **Insulators**, such as magnesium oxide, sodium chloride or boron nitride, where a finite band gap does not allow electrons to propagate. *Topological* insulators look the same in the bulk, but they behave in a completely different way at the edge, and we will need one full session to explain this difference.

- **Semiconductors**, such as gallium nitride, silicon and gallium arsenide, which have the same single-particle description as insulators but are lightly doped. For this reason they have free carriers, and these carriers are the ones that do the work in electronics and solar cells.

- **Magnets.** Ferromagnets, antiferromagnets and spin spirals are all *correlated* materials, in the sense that they exist only because electrons repel each other through the Coulomb interaction. A different and more exotic case is the *quantum magnet*, where there are local moments at every site but they are so strongly entangled with each other that the material has no net magnetization at all at the microscopic level, and every site forms a singlet with its neighbors. We will come back to these systems in detail later in the course.

- **Dirac and topological matter.** The prototype is graphene, which is a single honeycomb layer of carbon, where electrons propagate with a topologically protected phase that is called a Berry phase. The same family includes quantum spin Hall insulators, which have helical edge states, Chern insulators, which have chiral edge states, and chiral superconductors, which host Majorana excitations.

- **Superconductors.** These go from conventional superconductors mediated by phonons, such as aluminum, to *correlated* superconductors such as the cuprates and the pnictides, whose mechanism is still one of the biggest open problems in the field.

- **Fractional quantum matter.** Here the fundamental excitations are real fractions of an electron. The fractional quantum Hall state is the best established example, and it has been observed for decades in materials such as gallium arsenide. Fractional Chern insulators are a newer and more accessible way to obtain the same physics, and they are a promising building block for new quantum devices.

![The Dirac cone of graphene. The two bands touch at one point and rise linearly around it, which is why the electrons behave as massless particles. We derive this cone in session 2.](figures/s02f04_dirac.svg){panel="c" alt="A hexagonal Brillouin zone with a Dirac cone at two of its corners."}

::: quiz
A topological insulator and an ordinary insulator both have a gap in the bulk. How do we tell them apart in an experiment?

- [x] By the states at the edge, which conduct inside the gap in the topological case.
- [ ] By the size of the bulk gap, which is always larger in the topological case.
- [ ] By the density of states of the bulk, which is different in the two cases.
- [ ] By the atoms of the material, since only heavy atoms give a topological insulator.

The bulk gap is present in both cases, so the bulk does not decide. The difference appears at the edge, where the topological insulator has states inside the gap that carry current.
:::

::: quiz
A doped semiconductor conducts, while the undoped one with the same bands does not. What does the doping do?

- [x] It puts a few carriers in the conduction band or removes a few from the valence band.
- [ ] It closes the band gap, so the material becomes a metal.
- [ ] It makes the electrons interact strongly, so the material becomes a magnet.
- [ ] It changes the lattice into a topological one.

The bands stay the same, and only the filling changes. A few free carriers in the conduction band, or a few holes in the valence band, are enough to carry a current.
:::
