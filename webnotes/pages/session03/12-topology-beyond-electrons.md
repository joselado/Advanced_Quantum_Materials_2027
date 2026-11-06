## Topology beyond electrons {#sec-3-12 number="3.12"}

We built all the tools of this session, which are the Chern number, the Zak phase and the bulk-boundary correspondence, around electronic band structures. However, none of the underlying mathematics requires electrons. The same invariants apply to any quantum excitation with a well-defined dispersion relation. Examples are **magnons**, which are the spin-wave excitations of an ordered magnet, and **spinons**, which are the fractionalized spin excitations of a quantum magnet. Both allow exactly the same treatment with Berry curvature and Chern number, and we will do it explicitly for magnon bands in session 6 and for spinon bands in session 8. More generally, the argument only needed a Hamiltonian, or more generally a matrix that describes how a wave propagates, so it applies to any system with a dispersion relation. This includes photonic systems, where light propagates through a periodic medium, and even purely classical mechanical systems, such as coupled pendula, vibrating lattices and electronic circuits, which have all been shown in tabletop experiments to have topologically protected modes. In the end, topology is a statement about the internal structure of the eigenvectors as a function of momentum, and this structure exists wherever there is a wave equation, quantum or classical.

![Why a spinon is half a magnon, which is a first example of the excitations that we meet beyond electrons. In (a) a magnetic order has excitations with $\Delta S=1$, the magnons of session 6. In (b) a quantum magnet has spinons, which have $S=1/2$ each. Both can have bands with a Berry curvature and a Chern number, and we compute them in sessions 6 and 8.](figures/s08f01_magnon_spinon.svg){alt="A chain of spins with one flipped spin, and a chain of singlet pairs with two unpaired sites."}

::: quiz
The Chern number needs Bloch eigenvectors over a Brillouin zone. For which excitations can we define it?

- [x] For any wave with a periodic dispersion relation, such as magnons, photons or coupled pendula.
- [ ] Only for excitations of a two-dimensional metal.
- [ ] Only for electrons, since it needs a charge.
- [ ] Only for fermions.

The argument of the session uses only a matrix that describes how a wave propagates in a periodic medium. It does not use charge or the Pauli principle, so it holds for any wave equation.
:::

The main message of this session is the following. Topological systems have protected edge modes, and these modes are connected to a non-trivial value of a topological invariant that is computed only from the bulk. This happens in one and in two dimensions, and also in higher dimensions, and it is usually protected by a specific symmetry. For the Chern number this is translational symmetry and gauge invariance, and for the quantum spin Hall state it is time-reversal symmetry.
