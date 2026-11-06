## Topological magnons {#sec-6-16 number="6.16"}

Once magnons have a real band structure, which is a dispersion $E(\mathbf k)$ over the Brillouin zone, we can ask about *magnon* bands the same question that we have already asked twice about *electronic* bands. Can this band structure have a nontrivial topological invariant? To answer it, we use again the Chern number of sessions 3 and 4, where the Berry curvature $\Omega(\mathbf k)$ of a Bloch band is integrated over the Brillouin zone and gives an integer,

$$C = \frac{1}{2\pi}\int_\text{BZ} \Omega(\mathbf k)\, d^2k, \tag{6.10}$$

and this is the third time that we apply it, now to the bosonic Bogoliubov Hamiltonian of Section [6.15](#sec-6-15) instead of an electronic tight-binding Hamiltonian. We add to the plain Heisenberg exchange a spin-orbit coupling of the Dzyaloshinskii-Moriya type of Section [6.12](#sec-6-12). This term plays the same role as the complex second-neighbor hopping of the Haldane model for electrons in session 4. It introduces complex phases in the magnon hopping amplitudes, which can open a gap in the magnon band structure at finite energy and give the bands on both sides of this gap a nonzero Chern number [(6.10)](#eq-6-10). When we put such a topological magnon Hamiltonian on a ribbon, the bulk-boundary correspondence guarantees chiral magnon edge modes inside the gap. These modes propagate in only one direction along each edge, and they are the magnon analogue of the chiral electronic edge states of a Chern insulator. They carry spin and energy and not charge, but they are topologically protected in the same sense as their electronic counterparts. It is the same tool that we used for electrons in sessions 3 and 4, now applied to magnon bands.

::: notebookbox
**Notebook check-in:** [`session6.ipynb`](https://github.com/joselado/Advanced_Quantum_Materials_2027/blob/main/jupyter-notebooks/session6.ipynb), "(Exercise) Topological magnons in 2D magnets"

Construct a magnon Hamiltonian with a spin-orbit term of Dzyaloshinskii-Moriya type on top of the Heisenberg exchange, compute its Chern number with [(6.10)](#eq-6-10), and look for chiral magnon edge modes on a ribbon. This reproduces directly, for magnons, the argument of the bulk-boundary correspondence above.
:::

Before we stop, a short comment on the scope of these notes. The companion notebook goes further than the lecture of this session in a few places. The most visible ones are its exercises on electronic and magnetic symmetry breaking in graphene multilayers, and its last sections on many-body spin response functions. These are real and useful extensions of the material of this session. However, neither the transcript nor the slides of this session narrate them, so we have not included the corresponding derivations in these notes. They should be taken as independent work with the notebook, and not as material that these notes derive.
