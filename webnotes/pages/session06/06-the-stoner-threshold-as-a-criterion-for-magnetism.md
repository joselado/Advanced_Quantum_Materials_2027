## The Stoner threshold as a criterion for magnetism {#sec-6-6 number="6.6"}

A natural question is whether *any* repulsive $U>0$ gives magnetism, or if there is a threshold. We write the mean-field bands as $E_\sigma(\mathbf{k}) = E(\mathbf{k}) - \sigma\, \tfrac{U}{2}m$ for $\sigma=\pm1$, meaning spin up and down, where $m$ is the self-consistent magnetization of [(6.2)](#eq-6-2). At zero temperature, the self-consistency condition is

$$m = \sum_{\mathbf k}\Big[n_F\big(E(\mathbf k)-\tfrac{U}{2}m\big) - n_F\big(E(\mathbf k)+\tfrac{U}{2}m\big)\Big].$$

If we expand the right-hand side for small $m$ we obtain $m \approx U\,m\,D(E_F)$, where $D(E_F)$ is the density of states at the Fermi level. The trivial solution $m=0$ always exists, but a *nontrivial* solution appears when the linear coefficient reaches one, which gives the condition

$$U\, D(E_F) \geq 1. \tag{6.3}$$

This condition is called the Stoner criterion. Below the threshold only $m=0$ is stable, and the system stays nonmagnetic for any perturbation. Above the threshold the nonmagnetic solution becomes unstable, and a finite $m$ appears spontaneously. This is the reason why some metals with a sizable Coulomb repulsion, such as aluminum or lead, stay nonmagnetic, since their density of states at the Fermi level is too small for the product in [(6.3)](#eq-6-3) to reach one. Iron and cobalt, on the other hand, have a large density of states from their narrow $d$ bands together with a sizable effective $U$, so they are clearly above the threshold. In the numerics we see what [(6.3)](#eq-6-3) predicts. The self-consistent magnetization of the chain stays at zero below a critical $U$, and it grows continuously once $U$ is above this threshold. Figure [6.1](#fig:s06:stoner) shows both parts of this statement together. It shows why a nontrivial solution of the self-consistency condition only exists above the threshold, and how the resulting magnetization curve looks.

![A graphical reading of the Stoner criterion [(6.3)](#eq-6-3). (a) The self-consistency condition $m=f(m)$, where $f$ is the right-hand side of the zero-temperature gap equation, drawn here with the shape $\tanh$ for two values of the slope. It is an odd function that saturates once the bands are fully polarized, and its slope at the origin is exactly $U D(E_F)$. If this slope is below one, the only crossing with $y=m$ is the trivial solution $m=0$. Once the slope is above one, a pair of nontrivial solutions $\pm m_0$ appears and the nonmagnetic state becomes unstable. (b) The resulting order parameter, which stays at zero until $U D(E_F)$ reaches one and then grows continuously. For this reason, whether a metal becomes magnetic is not decided by $U$ alone but by the *product* of $U$ with the density of states at the Fermi level. This is why aluminium and lead stay nonmagnetic even with a sizeable Coulomb repulsion, while the narrow $d$ bands of iron and cobalt are clearly above the threshold.](figures/s06f01_stoner.svg){#fig:s06:stoner number="6.1"}

::: notebookbox
**Notebook check-in:** [`session6.ipynb`](https://github.com/joselado/Advanced_Quantum_Materials_2027/blob/main/jupyter-notebooks/session6.ipynb), "(Exercise) Intermediate coupling regime and Stoner instability"

Reproduce the threshold behavior of [(6.3)](#eq-6-3) directly. Compute the self-consistent magnetization as a function of $U$, and find the critical interaction at which $m$ first becomes nonzero.
:::

::: notebookbox
**Notebook check-in:** [`session6.ipynb`](https://github.com/joselado/Advanced_Quantum_Materials_2027/blob/main/jupyter-notebooks/session6.ipynb), "(Exercise) Magnetism in flat bands"

In principle, a flat band has a divergent density of states at $E_F$, so the Stoner product $U D(E_F)$ in [(6.3)](#eq-6-3) is above the threshold for practically any $U>0$. This exercise is not narrated in the transcript, but it is the natural numerical extension of Section [6.6](#sec-6-6), since a flat-band system is the case where it is easiest for magnetism to appear.
:::

One important consequence ends this section and starts the next one. From [(6.3)](#eq-6-3), magnetism in general needs $U D(E_F) \gtrsim 1$, and for a reasonable bandwidth this usually means that $U$ has to be comparable to $t$ or larger, and not smaller. However, mean-field theory itself is only reliable for $U \ll t$, as we saw in Section [6.3](#sec-6-3) So the regime where magnetism appears is, in general, the same regime where the method that we have been using stops working. We need a different approach for $U \gg t$, and we construct it in the rest of this session.
