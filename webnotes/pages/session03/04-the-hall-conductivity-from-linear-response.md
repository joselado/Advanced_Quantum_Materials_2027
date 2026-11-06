## The Hall conductivity from linear response {#sec-3-4 number="3.4"}

Now we apply [(3.1)](#eq-3-1) to the measurement that will bring us to topology, which is the transverse conductivity, also called the Hall conductivity. We take a two-dimensional material, apply a voltage in the $y$ direction, and ask what current flows in the $x$ direction. In momentum space, a voltage in $y$ enters as a perturbation proportional to $\partial H/\partial k_y$, since it shifts $k_y$ through the Peierls substitution. The current operator in the $x$ direction is, up to the electron charge, the group-velocity operator $\partial H/\partial k_x$. Both are the kind of matrix element that appears in [(3.1)](#eq-3-1).

When we put [(3.1)](#eq-3-1) into the definition of the Hall conductivity, we obtain an expression with two velocity operators and an energy denominator, which is the standard Kubo formula for a filled band $n$ and empty bands $m$,

$$\sigma_{xy} \;\propto\; \sum_{n\ \text{filled}} \sum_{m\ \text{empty}} \int_{\text{BZ}}
\frac{d^2k}{(2\pi)^2}\;
\frac{\langle n|\partial_{k_x}H|m\rangle\langle m|\partial_{k_y}H|n\rangle - (x\leftrightarrow y)}
{(\varepsilon_n - \varepsilon_m)^2}. \tag{3.2}$$

At this point the expression still depends explicitly on the band energies through the denominator, so it seems that it should depend on all the details of the band structure. This is not the case, and the next section shows why.
