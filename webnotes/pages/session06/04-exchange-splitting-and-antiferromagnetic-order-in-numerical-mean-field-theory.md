## Exchange splitting and antiferromagnetic order in numerical mean-field theory {#sec-6-4 number="6.4"}

Let us now see the method of Section [6.3](#sec-6-3) in a real calculation. First we take the one-dimensional chain [(6.1)](#eq-6-1) with a unit cell of one site at 20% filling, and we solve it self-consistently. The resulting band structure shows an exchange splitting. The spin-up band, which is occupied up to the chemical potential, is at lower energy than the spin-down band, which is empty at this filling. The splitting between them is called the **exchange splitting**, and it grows with $U$. Only spin-up states are occupied, so this is a fully polarized ferromagnetic solution with $m\neq 0$.

Now we take a unit cell with two sites, and we work at half filling. At $U=0$ there are two bands, one per site in the cell, and they cross at one point, so the system is metallic. When we turn on $U>0$ a mean-field gap opens, and in real space the two sublattices get opposite spin polarization, with one site mostly up and its neighbor mostly down. The *net* magnetization is zero, but the *staggered* magnetization is not, and this is antiferromagnetic order. As always when a mean-field gap opens, it lowers the total electronic energy with respect to the state without a gap, because the states that the gap pushes down in energy are the occupied ones.

::: notebookbox
**Notebook check-in:** [`session6.ipynb`](https://github.com/joselado/Advanced_Quantum_Materials_2027/blob/main/jupyter-notebooks/session6.ipynb), "(Reminder) Bandstructure of a tight binding chain with two sites" and "(Exercise) Magnetic order driven by interactions in a chain"

Start from the band structure of the two-site chain without interactions, which is the metallic case with a crossing. Then turn on $U$ and see how the mean-field gap opens and how the spin pattern in real space becomes antiferromagnetic, which reproduces the exchange splitting of [(6.2)](#eq-6-2) directly. The ferromagnetic case with one site per cell at 20% filling, from the same section, is the companion calculation.
:::
