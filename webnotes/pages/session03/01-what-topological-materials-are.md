## What topological materials are {#sec-3-1 number="3.1"}

Before we go into the formalism, it is useful to have a rough classification in mind, so that the abstract tools that we are going to build have concrete targets. Topological materials are systems with an excitation gap in the bulk that at the same time have protected excitations at their surface or edge. This combination of a gapped bulk and a gapless boundary will appear again and again in this session, and it is the defining feature of these materials. The point is not that the edge happens to have low-energy states. The point is that the topology of the bulk *forces* them to be there.

Within this class, we will see the following systems in this session and in the next one.

- The **quantum Hall effect**, which appears in two-dimensional electron gases and in graphene under a strong perpendicular magnetic field. It is the simplest topological state, and it is our starting point.

- The **quantum anomalous Hall effect**, which is the same physics without any external magnetic field, and which we will construct explicitly in Section [3.10](#sec-3-10).

- **Quantum spin Hall insulators**, which are in practice two copies of a quantum Hall state related by time reversal and put together, as we will see in Section [3.11](#sec-3-11).

- **Topological superconductors**, whose surface excitations are Majorana modes. They are the basis of one route to topological quantum computing, and we will come back to them in detail in session 5.

- **Topological semimetals**, including Weyl semimetals, whose low-energy quasiparticles are Weyl fermions.

- **Topological Kondo insulators**, which are the example given in the lecture this year of topology that survives in a strongly correlated many-body system, "and many others that do not fit on this slide."

This material appears only on the slides and has no counterpart in the notebook. For each entry, the slides name a specific material realization, which is graphene for the quantum Hall effect, Cr-doped (Bi,Sb)$_2$Te$_3$ for the quantum anomalous Hall effect, HgTe/CdTe quantum wells for the quantum spin Hall effect, Fe chains on Pb for a topological superconductor, TaAs for a Weyl semimetal, and SmB$_6$ for the many-body example. These were shown but not explained in detail in the lecture, and the notebook of the course does not simulate any of these specific compounds. The many-body example on the classification slide is the topological Kondo insulator, with SmB$_6$ as the material realization. What we will simulate, with the models that we build in this session, are minimal tight-binding versions of the first three items of the list above.
