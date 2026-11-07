## What topological materials are {#sec-3-1 number="3.1"}

Before we go into the formalism, it is useful to have a rough classification in mind, so that the abstract tools that we are going to build have concrete targets. Topological materials are systems with an excitation gap in the bulk that at the same time have protected excitations at their surface or edge. This combination of a gapped bulk and a gapless boundary will appear again and again in this session, and it is the defining feature of these materials. The point is not that the edge happens to have low-energy states. The point is that the topology of the bulk *forces* them to be there.

![The picture to keep in mind for all the materials of this session. In the bulk the electrons move on closed orbits and the bulk is gapped. At the boundary the orbits skip along the edge, and this edge carries current even though the bulk is an insulator. Look at the arrows, which have opposite directions on the two edges. We study this picture in Section [3.6](#sec-3-6).](figures/s03f01_chiraledge.svg){alt="A sample seen from above with closed orbits in the bulk and orbits that skip along the edge in opposite directions on the two edges."}

::: quiz
A material has a gapped bulk and edge states inside the gap. A change of the edge potential, which keeps the bulk gap open, removes these states. Is this material topological in the sense of this session?

- [ ] No, because a gapped bulk cannot have edge states.

    This is false. The SSH chain with $t=1/2$ has a gapped bulk and a state at zero energy at each end, and the ribbon of the Haldane model has edge branches inside the bulk gap. The reason given here fails, even if the answer "No" is right for this material.

- [x] No, because in a topological material the bulk forces the edge states to exist for every edge.

    This is true. The bulk invariant forces the edge states, so a change of the edge can move them in energy but cannot remove them. Here the states disappear, so they belong to this particular edge.

- [ ] Yes, because any edge state inside a bulk gap signals topology.

    This is false. Take a trivial insulator and change the potential of the last site. A state is pushed out of the valence band into the gap, and it disappears when the potential goes back to zero, as in this question.

Edge states that a change of the edge can remove belong to one particular edge and are not protected.
:::

Within this class, we will see the following systems in this session and in the next one.

- The **quantum Hall effect**, which appears in two-dimensional electron gases and in graphene under a strong perpendicular magnetic field. It is the simplest topological state, and it is our starting point.

- The **quantum anomalous Hall effect**, which is the same physics without any external magnetic field, and which we will construct explicitly in Section [3.10](#sec-3-10).

- **Quantum spin Hall insulators**, which are in practice two copies of a quantum Hall state related by time reversal and put together, as we will see in Section [3.11](#sec-3-11).

- **Topological superconductors**, whose surface excitations are Majorana modes. They are the basis of one route to topological quantum computing, and we will come back to them in detail in Session 5.

- **Topological semimetals**, including Weyl semimetals, whose low-energy quasiparticles are Weyl fermions.

- **Topological Kondo insulators**, which are an example of topology that survives in a strongly correlated many-body system.

Each entry has a material realization. These are graphene for the quantum Hall effect, Cr-doped (Bi,Sb)$_2$Te$_3$ for the quantum anomalous Hall effect and HgTe/CdTe quantum wells for the quantum spin Hall effect. For a topological superconductor one example is a chain of Fe atoms on Pb, for a Weyl semimetal it is TaAs, and for the topological Kondo insulator it is SmB$_6$. The notebook of the course does not simulate any of these compounds. What we will simulate, with the models that we build in this session, are minimal tight-binding versions of the first three items of the list above.

![A gapped bulk with states at its boundary, computed on a finite disk of the honeycomb lattice with about 860 sites. In (a) we compare two flakes with the same bulk gap, which is the grey band. The blue flake has the Haldane hopping $t_2=0.1$ of Section [3.10b](#sec-3-10b), and the grey one has a staggered potential instead. Only the blue spectrum has states inside the gap. In (b) we draw the weight of these states on the sites of the blue flake. About 97 percent of it sits within two lattice constants of the boundary. This is the combination that defines the materials of this session, an insulator in the bulk and a metal at the edge.](figures/web/session03/haldane_flake.svg){#sch:s03:haldane_flake alt="Left, the energies of two finite flakes in increasing order, with a shaded gap that only the blue spectrum crosses. Right, a disk of the honeycomb lattice with blue dots on the sites of its boundary."}

::: comesback
- In Section [4.20](#sec-4-20) the quantum anomalous Hall state of Cr-doped (Bi,Sb)$_2$Te$_3$ comes back, together with fractional Chern states at zero field.
- In Section [5.15](#sec-5-15) we build the Majorana modes of a topological superconductor, and in Section [5.14](#sec-5-14) its chiral edge looks like the edge of the figure above.
- In Section [8.13](#sec-8-13) we see how a Kondo lattice becomes an insulator, with SmB$_6$ as the material.
:::
