## Real materials realizing Chern and fractional Chern physics {#sec-4-20 number="4.20"}

*This survey, like Sections [4.17](#sec-4-17)-[4.18](#sec-4-18), comes from the transcript and the slides and has no counterpart in the notebook. There is no numerical exercise in `session4.ipynb` built around any of the specific compounds below.*

The Chern insulator at zero field is not only a theoretical idea. Chromium-doped $(\text{Bi,Sb})_2\text{Te}_3$, which is a magnetically doped topological insulator, breaks time-reversal symmetry through real magnetism and realizes an integer quantized Hall conductance with no applied field. Twisted graphene bilayers aligned with a boron nitride substrate realize the same physics with a different mechanism, which is based on orbital currents and not on magnetic moments. On the fractional side, twisted two-dimensional materials can host topological flat bands with a mathematical structure similar to the one of an artificial pseudo-magnetic field, which comes from the elastic reconstruction of the lattice and not from a real field. Twisted bilayers of molybdenum ditelluride (MoTe$_2$) are a recent and striking example, and they show real fractional quantum Hall physics at zero magnetic field.

![The fractional charge and the anyon statistics of Section [4.18](#sec-4-18). A fractional Chern state at zero field has to realize the same physics. In (a) the quasihole has the charge $e/m$. In (b) the exchange phase $\pi/m$ is strictly between the bosonic and the fermionic value. Look at the bottom of (b), where the phase for $m=3$ is drawn.](figures/s04f06_quasihole.svg){alt="A dimple in a flat density profile for a quasihole, and a loop of one quasihole around another with the exchange phase."}

::: quiz
In twisted bilayers of MoTe$_2$ there is no applied magnetic field. What plays the role of the lowest Landau level?

- [ ] The spin-orbit coupling of the substrate.
- [ ] A magnetic field of a few tesla from the substrate.
- [ ] A superconducting gap.
- [x] A topological flat band with nonzero Chern number that the twisted lattice itself produces.

The flat band has a Chern number and a structure similar to a Landau level. It comes from the lattice and not from a field. With interactions, a partially filled band can then give fractional states.
:::

## Closing summary {#sec-4-21 number="4.21"}

- The Hall conductivity is a topological invariant, the Chern number of the occupied bands, as we derived in more detail in session 3. Equation [(4.1)](#eq-4-1) is the same result, which we confirm here and do not derive again from the beginning.

- A magnetic field turns a two-dimensional electron gas into a set of flat Landau levels, each with Chern number one, so the Hall conductivity is quantized to $N e^2/h$ for $N$ filled Landau levels, equation [(4.2)](#eq-4-2).

- An insulating bulk still conducts because a nonzero Chern number gives chiral edge states without backscattering at the boundary of the sample (Section [4.5](#sec-4-5)), which we can see directly in the band structures of ribbons.

- Landau levels come from minimal coupling [(4.3)](#eq-4-3) or, on a lattice, from the Peierls substitution [(4.4)](#eq-4-4). Schrödinger electrons give equally spaced levels $E_n=\hbar\omega_c(n+\tfrac12)$, equation [(4.6)](#eq-4-6), while Dirac electrons give $E_n\propto\sqrt{nB}$, equation [(4.7)](#eq-4-7), and this explains the much higher temperature scale of the quantum Hall effect in graphene.

- In the symmetric gauge, the wavefunctions of the lowest Landau level are holomorphic, $\psi_m(z)\propto z^m e^{-|z|^2/4\ell_B^2}$, equation [(4.10)](#eq-4-10). The many-body state of the filled LLL is the Vandermonde determinant times a collective Gaussian, equation [(4.11)](#eq-4-11).

- When we raise the Vandermonde factor to an odd power $m$ we obtain the Laughlin wavefunction, equation [(4.12)](#eq-4-12), with filling factor $\nu=1/m$, equation [(4.13)](#eq-4-13). Its quasihole excitations, equation [(4.14)](#eq-4-14), have fractional charge $e/m$, equation [(4.15)](#eq-4-15), and follow anyonic statistics. They get a phase $2\pi/m$ for a full braid, equation [(4.16)](#eq-4-16), which is an exchange phase $\pi/m$ strictly between the bosonic $0$ and the fermionic $\pi$, and this is the simplest case of fractionalization that we will meet.

- The Haldane model shows that the quantized Hall conductance never strictly needed a magnetic field, and that it is adiabatically and topologically equivalent to the quantum Hall state driven by the field. This is a return to session 3 and not new theory.

In this session the order was driven only by a magnetic field, which is an external symmetry-breaking parameter that we switched on by hand. In the next session we will see a completely different route to order, which is the attractive interaction between the electrons themselves. This interaction drives the system to become a superconductor without any external field, and we will see that the same classification into trivial and chiral topological states, which we built here and in session 3, comes back to sort superconducting order parameters into conventional and topological classes. It is also useful to keep in mind the form of fractionalization that we just built, since we will soon meet a second example of it, which looks quite different. Here, the correlations inside a partially filled topological flat band split the charge of the electron and made its exchange statistics anyonic. In the next session, pairing correlations in a superconductor will split the electron into two Majorana halves instead. The underlying idea is the same, which is a correlated topological state with excitations that are not the electron itself, but it is reached by two really different mechanisms.

::: quiz
The Laughlin quasihole of this session and the Majorana halves of session 5 are both fractionalization. What do they share?

- [x] In both, correlations give excitations that are not the electron, with only a part of its charge or of its degrees of freedom.
- [ ] Both need a magnetic field.
- [ ] Both appear in a system of weakly interacting electrons.
- [ ] Both are bosons.

The mechanisms are different, since one comes from correlations in a flat band and the other from pairing in a superconductor. In both cases the excitations are not the electron itself.
:::
