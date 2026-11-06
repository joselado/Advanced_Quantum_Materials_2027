## The SSH model, the Bloch Hamiltonian and the Zak phase {#sec-3-9c number="3.9c"}

So far the topological phase was defined by the end states of a finite chain. We can make this fully precise with the Bloch Hamiltonian. With intracell hopping $t$ and intercell hopping normalized to $1$, the Hamiltonian in momentum space in the $(A,B)$ basis is the $2\times 2$ matrix

$$H(k) = \begin{pmatrix} 0 & d(k) \\ d^*(k) & 0 \end{pmatrix}
= (t + \cos k)\,\sigma_x - \sin k\,\sigma_y, \qquad d(k) = t + e^{ik}, \tag{3.5}$$

with eigenvalues $E_\pm(k) = \pm|d(k)| = \pm\sqrt{1 + t^2 + 2t\cos k}$. The gap closes exactly when $d(k)=0$, which requires $t=1$ and $k=\pi$. This is the topological phase transition point, and it agrees with the qualitative separation between $t<1$ and $t>1$ above, since at $t=0$ the chain is in the limit where the end sites are fully dangling, which is topological, and at $t=1$ it becomes the fully symmetric gapless chain.

::: quiz
For which value of $t$ and at which momentum does the gap of the SSH chain close?

- [ ] $t=0$ and $k=0$.
- [x] $t=1$ and $k=\pi$.
- [ ] $t=2$ and $k=\pi$.
- [ ] $t=1$ and $k=0$.

The gap closes when $d(k)=t+e^{ik}=0$. This requires $e^{ik}=-t$, which has a solution only for $|t|=1$, and for $t=1$ it is $k=\pi$.
:::

The topological invariant here is the one-dimensional Berry phase that the lower-band Bloch state $|u_-(k)\rangle$ accumulates as $k$ goes once around the Brillouin zone, which is called the **Zak phase**,

$$\gamma = i \oint_{\text{BZ}} \langle u_-(k)|\partial_k u_-(k)\rangle\, dk \pmod{2\pi}. \tag{3.6}$$

Geometrically, $\gamma/\pi$ counts how many times $d(k)$ winds around the origin as $k$ goes from $0$ to $2\pi$. From [(3.5)](#eq-3-5), $d(k) = t + e^{ik}$ draws a unit circle centered at $(t,0)$ in the complex plane. This circle encloses the origin exactly when $|t|<1$, and it does not enclose it when $|t|>1$. This agrees with everything above, since $\gamma = \pm\pi$ for $t<1$, which means one winding, a topological insulator and gapless edge modes, and $\gamma = 0$ for $t>1$, which means no winding, a trivial insulator and no edge modes. The value of the Zak phase is in exact one-to-one correspondence with the presence or absence of a zero-energy edge state, and this is the one-dimensional version of the bulk-boundary correspondence of Section [3.7](#sec-3-7). Figure [3.4](#fig:s03:winding) shows this winding together with the bands that it controls, and it shows that the two insulating phases cannot be distinguished from their spectra alone.

![A drawing of the one-dimensional invariant. On the left of each panel is the off-diagonal element $d(k)=t+e^{ik}$ of the SSH Bloch Hamiltonian [(3.5)](#eq-3-5) in the complex plane, as $k$ goes once through the Brillouin zone, and the arrow shows the direction of increasing $k$. It is always the unit circle, but centred at $(t,0)$, so it encloses the origin, the ball, for $t<1$ and does not enclose it for $t>1$. The winding number of this curve around the origin is exactly $\gamma/\pi$, which is the Zak phase [(3.6)](#eq-3-6) in units of $\pi$. On the right of each panel are the corresponding bands $E_\pm(k)=\pm|d(k)|$, with gap $2|1-t|$. The two halves give the same information in two ways. The only way to unwind the curve is to move it across the origin, and $d(k)=0$ is where the gap closes, so the invariant cannot change while the system stays insulating. Note that (a) and (c) have the same gap and look like ordinary spectra. The difference between them cannot be seen in the energies and is only in the wavefunctions, which is the main point of [(3.4)](#eq-3-4). By the bulk-boundary correspondence, $\gamma=\pi$ is also exactly the condition for the zero-energy end modes of figure [3.3](#fig:s03:ssh).](figures/s03f04_winding.svg){#fig:s03:winding number="3.4"}

This material appears only in the lecture and on the slides, and it has no counterpart in the notebook. The notebook `session3.ipynb` does not have a dedicated section on the SSH chain, and its numerical exercises start directly from two-dimensional ribbons, which are the quantum Hall and quantum anomalous Hall constructions of Sections [3.6](#sec-3-6) and [3.10](#sec-3-10). If you want to see the zero modes and the Zak-phase winding of [(3.6)](#eq-3-6) numerically, the direct way is to build by hand the finite chain with $N$ sites from Section [3.9](#sec-3-9), following the same tight-binding diagonalization method that we used for the finite islands in session 1. Then you can see how the two eigenvalues close to zero move away from zero as $t$ is increased above $1$.

::: quiz
The chains with $t=1/2$ and $t=3/2$ have the same gap, $2|1-t|=1$. What is the difference between them?

- [x] Only the chain with $t=1/2$ has a winding of $d(k)$ around the origin and end states.
- [ ] Only the chain with $t=3/2$ is gapless.
- [ ] Both have end states, but at different energies.
- [ ] Only the chain with $t=3/2$ has end states, since its bonds are stronger.

The curve $d(k)=t+e^{ik}$ is a unit circle centered at $(t,0)$. It encloses the origin for $t=1/2$ and not for $t=3/2$. The two gaps look the same in the spectrum, and only the first chain is topological.
:::
