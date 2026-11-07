## The SSH model, the Bloch Hamiltonian and the Zak phase {#sec-3-9c number="3.9c"}

So far the topological phase was defined by the end states of a finite chain. We can make this fully precise with the Bloch Hamiltonian of Section [2.5](#sec-2-5). With the lattice constant $a=1$ the phase $\varphi$ of Session 2 is the quasi-momentum $k$, by [(2.10)](#eq-2-10). With intracell hopping $t$ and intercell hopping normalized to $1$, the Hamiltonian in momentum space in the $(A,B)$ basis is the $2\times 2$ matrix

$$H(k) = \begin{pmatrix} 0 & d(k) \\ d^*(k) & 0 \end{pmatrix}
= (t + \cos k)\,\sigma_x - \sin k\,\sigma_y, \qquad d(k) = t + e^{ik}, \tag{3.5}$$

with eigenvalues $E_\pm(k) = \pm|d(k)| = \pm\sqrt{1 + t^2 + 2t\cos k}$. The gap closes only where $d(k)=0$, which requires $t=1$ and $k=\pi$. This is the topological phase transition point. It agrees with the separation between $t<1$ and $t>1$ above, since at $t=0$ the end sites are fully dangling, which is topological. At $t=1$ the chain becomes the fully symmetric gapless chain.

::: quiz
For which value of $t$ and at which momentum does the gap of the SSH chain close?

- [ ] $t=2$ and $k=\pi$.

    This is false. At $k=\pi$ we get $d=t+e^{i\pi}=2-1=1$, which is not zero. The energy there is $\pm1$.

- [x] $t=1$ and $k=\pi$.

    This is true. The gap closes when $d(k)=t+e^{ik}=0$. This requires $e^{ik}=-t$, which has a solution only for $|t|=1$, and for $t=1$ it is $k=\pi$.

- [ ] $t=1$ and $k=0$.

    This is false. At $k=0$ we get $d=1+1=2$, so the energy is $\pm2$, which is the top of the band and not a crossing.

:::

The topological invariant here is the one-dimensional Berry phase that the lower-band Bloch state $|u_-(k)\rangle$ accumulates as $k$ goes once around the Brillouin zone, which is called the **Zak phase**,

$$\gamma = i \oint_{\text{BZ}} \langle u_-(k)|\partial_k u_-(k)\rangle\, dk \pmod{2\pi}. \tag{3.6}$$

Geometrically, $\gamma/\pi$ counts how many times $d(k)$ winds around the origin as $k$ goes from $0$ to $2\pi$. From [(3.5)](#eq-3-5), $d(k) = t + e^{ik}$ draws a unit circle centered at $(t,0)$ in the complex plane. This circle encloses the origin when $|t|<1$, and it does not enclose it when $|t|>1$. This agrees with everything above, since $\gamma = \pm\pi$ for $t<1$, which means one winding, a topological insulator and gapless edge modes, and $\gamma = 0$ for $t>1$, which means no winding, a trivial insulator and no edge modes. The value of the Zak phase is in exact one-to-one correspondence with the presence or absence of a zero-energy edge state, and this is the one-dimensional version of the bulk-boundary correspondence of Section [3.7](#sec-3-7). Figure [3.4](#fig:s03:winding) shows this winding together with the bands that it controls, and it shows that the two insulating phases cannot be distinguished from their spectra alone.

![A drawing of the one-dimensional invariant. On the left of each panel is the off-diagonal element $d(k)=t+e^{ik}$ of the SSH Bloch Hamiltonian [(3.5)](#eq-3-5) in the complex plane, as $k$ goes once through the Brillouin zone. The arrow shows the direction of increasing $k$. It is always the unit circle, but centred at $(t,0)$, so it encloses the origin, the ball, for $t<1$ and does not enclose it for $t>1$. The winding number of this curve around the origin is $\gamma/\pi$, which is the Zak phase [(3.6)](#eq-3-6) in units of $\pi$. On the right of each panel are the corresponding bands $E_\pm(k)=\pm|d(k)|$, with gap $2|1-t|$. The two halves give the same information in two ways. The only way to unwind the curve is to move it across the origin, and $d(k)=0$ is where the gap closes, so the invariant cannot change while the system stays insulating. Note that (a) and (c) have the same gap and look like ordinary spectra. The difference between them cannot be seen in the energies and is only in the wavefunctions, which is the main point of [(3.4)](#eq-3-4). By the bulk-boundary correspondence, $\gamma=\pi$ is also the condition for the zero-energy end modes of Figure [3.3](#fig:s03:ssh).](figures/s03f04_winding.svg){#fig:s03:winding number="3.4"}

The notebook `session3.ipynb` has no section on the SSH chain. Its exercises start directly from the two-dimensional ribbons of the quantum Hall and quantum anomalous Hall states, in Sections [3.6](#sec-3-6) and [3.10](#sec-3-10). To see the zero modes and the winding of [(3.6)](#eq-3-6) numerically, you can build by hand the finite chain with $N$ sites of Section [3.9](#sec-3-9). The method is the same tight-binding diagonalization that we used for the finite islands of Section [1.10](#sec-1-10). Then you can see how the two eigenvalues close to zero move away from zero as $t$ is increased above $1$.

::: quiz
The chains with $t=1/2$ and $t=3/2$ have the same gap, $2|1-t|=1$. What is the difference between them?

- [x] Only the chain with $t=1/2$ has a winding of $d(k)$ around the origin and end states.

    This is true. The curve $d(k)=t+e^{ik}$ is a unit circle centered at $(t,0)$. It encloses the origin for $t=1/2$ and not for $t=3/2$, and the two gaps look the same in the bulk spectrum.

- [ ] Only the chain with $t=3/2$ is gapless.

    This is false. For $t=3/2$ the smallest value of $|d|$ is $|1-t|=0.5$, so there are no levels between $-0.5$ and $0.5$. Numerically, the open chain of 40 sites has its lowest levels at $\pm0.53$.

- [ ] Only the chain with $t=3/2$ has end states, since its bonds are stronger.

    This is false. For the open chain of 40 sites we get two levels at $\pm7\times10^{-7}$ for $t=1/2$, inside the gap, and the lowest levels are at $\pm0.53$ for $t=3/2$. The weaker intracell bond gives the end states.

:::

::: comesback
- In Section [5.17](#sec-5-17) the Kitaev chain has a bulk invariant of the same kind, and its zero modes appear only with open boundaries.
- In Section [4.18](#sec-4-18) a Berry phase around a closed loop, now of a quasihole, gives a fractional charge.
- In Section [10.6](#sec-10-6) the Zak phase is one of the invariants that separate phases with no local order parameter, and Section [10.6b](#sec-10-6b) shows why this makes them hard to classify.
- In Section [9.8](#sec-9-8) a vacancy probes a bulk invariant through an in-gap mode, for the Haldane model and for a chiral p-wave superconductor.
:::
