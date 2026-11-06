## Two classes of magnets and their excitations {#sec-6-1 number="6.1"}

Let us start with a map of where we are going, since this lecture first previews material from two later sessions and only then moves to its own topic. There are two big classes of magnetic systems.

The first class contains the magnets that break time-reversal symmetry. These materials have a net magnetization on every site, or a staggered one, and a finite spin angular momentum is what makes a system look different when we play its "movie" backwards, which is the definition of broken time-reversal symmetry. Ferromagnets, antiferromagnets and noncollinear spin spirals are in this class. Iron and cobalt are the two materials that the lecture names, several times, as concrete examples of this family. In this session we spend all our time on this class.

The second class contains the magnets that do *not* break time-reversal symmetry, at least not classically. These are quantum magnets, and quantum spin liquids are among them. They have a local moment on every site, but the spins are in a quantum superposition and do not form a static classical arrangement, so time-reversal symmetry does not need to be broken overall. A related case, which is also mentioned only briefly in this lecture, is the heavy-fermion Kondo system. It is a combination of local moments in a quantum superposition with a sea of itinerant metallic electrons. The "Classical and quantum magnetism" slide shows the three families with photographs of materials, which are iron for the ferromagnet and antiferromagnet family, herbertsmithite for quantum spin liquids and samarium hexaboride SmB$_6$ for heavy-fermion insulators. None of these three compound names is said in this year's narration. They are only labels on the slide, which are good to know but which the lecture does not say out loud.

Each class has its own emergent excitation. Magnets that break time-reversal symmetry have **magnons**, which are spin-1 and charge-neutral fluctuations of the order parameter, and they are the direct magnetic analogue of a phonon. Magnons have no charge, so electric fields do not affect them at all, and they can propagate in materials that are electronic insulators. A ferromagnetic or antiferromagnetic Mott insulator does not let any current through, but a magnon can still carry spin and heat across it. Quantum magnets have instead **spinons**, which are spin-$1/2$ and charge-neutral excitations. They are sometimes described informally as "half an electron," since the spin and the charge degrees of freedom of the electron have in practice separated. In the rest of this session we will construct magnons in detail. Spinons and the Kondo lattice model only appear here as a name and a spin quantum number. Their full construction is the material of a later session, session 8, and this lecture does not come back to them.


![The two kinds of excitation of a magnet. (a) A magnon changes the spin by $\Delta S=1$. (b) A spinon is an unpaired site of $S=1/2$, so it is half a magnon. Spinons are the subject of session 8.](figures/s08f01_magnon_spinon.svg){alt="At the top a row of arrows with one flipped spin, and at the bottom pairs of sites bound in capsules with two unpaired sites."}

::: quiz
A Mott insulator carries no charge current. Which statement about magnons in it is correct?

- [ ] Magnons cannot exist, since they need free charge carriers.

    This is false. Take the Hubbard dimer at half filling and large $U$. Its triplet lies above the singlet by $J=4t^2/U$, and it is a magnon-like excitation that moves no charge, since every site keeps one electron.

- [x] Magnons are neutral spin-1 excitations, so they carry spin and heat but no charge.

    This is true. A magnon is a fluctuation of the order parameter, created by $S^-$, so the number of electrons does not change. It carries one unit of spin and the energy of the excitation.

- [ ] Magnons carry spin $1/2$ and charge $e$.

    This is false. Applying $S^-$ to one site changes $S^z$ by $1$ and leaves the number of electrons the same. The excitation is therefore neutral with spin $1$, and a charge $e$ would need to add or remove an electron.
:::
