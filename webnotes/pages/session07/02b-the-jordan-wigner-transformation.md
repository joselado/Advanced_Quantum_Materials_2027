## The Jordan-Wigner transformation {#sec-7-2b number="7.2b"}

The two languages differ in one sign, and the Jordan-Wigner transformation is the exact rule that fixes it. Let us first look at a single site. A spinless fermionic site has a local Hilbert space of dimension two, empty or full, and a spin-1/2 site also has a local Hilbert space of dimension two, down or up. The first guess is $c_i^\dagger \leftrightarrow S_i^+$ and $c_i \leftrightarrow S_i^-$, and on a single site this guess is exactly right. However, it fails when we have more than one site, since fermion operators on different sites anticommute, while spin operators on different sites commute. As a result, the naive identification gives the wrong relative signs between sites. To fix this, we add to each site an extra phase that depends on the occupations. This phase is a "string" over all the sites to the left, chosen so that the exchange of two fermions gives the minus sign that the spin operators do not have by themselves. This mapping is called the **Jordan-Wigner transformation**, and it reads

$$S_i^+ = c_i^\dagger K_i, \qquad S_i^- = c_i K_i, \qquad S_i^z = n_i - \tfrac{1}{2}, \qquad
K_i = \exp\!\left(i\pi \sum_{j<i} n_j\right), \tag{7.2}$$

where $n_j = c_j^\dagger c_j$ is the fermion number operator on site $j$. The string operator $K_i$ is built only from the occupation numbers to the left of site $i$. For this reason it commutes with all local operators on sites $j \ge i$, and it counts, mod 2, how many fermions are to the left. We can check directly that [(7.2)](#eq-7-2), built in this way, gives the full $SU(2)$ commutation algebra of spin-1/2 operators on every site and between every pair of sites. For this check we only need the fermionic anticommutation relations for $c_i,
c_i^\dagger$ and the string. In the lecture this is summarized as *spin equals fermion times string*, and this statement is correct. Figure [7.1](#fig:s07:jwstring) shows what the string does. It counts the fermions to the left of site $i$ and gives their parity, so a change of a single occupation anywhere in that region changes the sign of $S_i^+$.

![Spin equals fermion times string. On a single site the mapping is trivial, since an empty site is a down spin and an occupied site is an up spin, $S^z_i = n_i -
\tfrac 12$, as the ball and the arrow on each site show. The naive identification gives the wrong *relative* signs between sites, because fermion operators on different sites anticommute while spin operators on different sites commute. The string $K_i$ of [(7.2)](#eq-7-2) corrects exactly this, since it gives a factor $-1$ for every fermion to the left of site $i$, which is the shaded strip. The two chains in the figure differ only in the occupations to the left of the marked site $i=6$, with three fermions in the chain behind and two in the chain in front, and this parity alone changes the sign of $S_6^+ = c_6^\dagger K_6$. The string is nonlocal, and it carries the fermionic exchange sign that spins do not have by themselves.](figures/s07f01_jwstring.svg){#fig:s07:jwstring number="7.1"}

This is the one explicit link in the course between the two languages that we have used. The fermionic operators of sessions 1 to 5 and the spin operators of session 6 and, as we will see, of session 8 are related by [(7.2)](#eq-7-2), and they are not only analogous to each other. It also explains a practical choice that we make for the rest of this session. Since interacting fermionic Hamiltonians and interacting spin Hamiltonians are mathematically equivalent, we can work only in the spin representation from now on, and we will do so. The reason is that spin operators on different sites commute, so there is no fermionic sign to keep track of when we cut the chain, and this makes the counting of entanglement below clean.

::: quiz
In the figure, the chain behind has three fermions to the left of site 6 and the chain in front has two. How do $S_6^+=c_6^\dagger K_6$ of the two chains compare, for the same $c_6^\dagger$?

- [x] They have opposite signs, since $K_6=(-1)^{N_\text{left}}$ is $-1$ for three fermions and $+1$ for two.

    This is true. The string is the parity of the number of fermions to the left. Three fermions give $-1$ and two give $+1$, so the same $c_6^\dagger$ enters with opposite signs.

- [ ] They are equal, since the string only depends on site 6.

    This is false. The string is built from the sites $j<6$. Take one fermion away from the left of the chain behind, and $K_6$ goes from $-1$ to $+1$ while $c_6^\dagger$ stays the same.

- [ ] Both vanish, since the string kills the operator.

    This is false. The string has the eigenvalues $\pm1$ and it is never zero. For the chain in front, $K_6=+1$ and $S_6^+=c_6^\dagger$, which creates a fermion with amplitude one.
:::

::: quiz
What is the string $K_1$ of the first site of a chain, and what does this mean for $S_1^+$?

- [ ] $K_1=-1$, so $S_1^+=-c_1^\dagger$.

    This is false. For a chain of a single site $S_1^+$ must take $|{\downarrow}\rangle$ to $|{\uparrow}\rangle$ with matrix element $+1$. The choice $K_1=-1$ would give $-1$.

- [x] $K_1=1$, so $S_1^+=c_1^\dagger$ with no sign.

    This is true. The sum in [(7.2)](#eq-7-2) runs over $j<i$, which is empty for the first site. An empty sum gives the exponential of zero, which is $1$.

- [ ] $K_1=0$, so $S_1^+$ vanishes.

    This is false. The string is an exponential, so it is never zero. If $S_1^+$ vanished, a chain of one site could not flip a spin from down to up, which $S^+$ does.
:::
