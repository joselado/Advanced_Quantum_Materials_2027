"""Session 8, Section 8.13. The bands of the Kondo lattice per spin: a conduction band hybridized with a flat f band."""
META = dict(
    id="kondobands", title="The Kondo lattice opens a gap",
    params=[dict(name="g", label="hybridization gamma_K (units of t)", min=0.0, max=1.2, step=0.05, value=0.5, fmt=2)],
    packages=["numpy"], pyqula=False,
)


def compute(p):
    import numpy as np
    g = float(p["g"])
    k = np.linspace(-np.pi, np.pi, 121)
    eps = -2 * np.cos(k)                         # conduction band
    # H(k) = [[eps, g], [g, 0]]: the f band is flat at E=0 when g=0
    r = np.sqrt((eps / 2) ** 2 + g ** 2)
    ep, em = eps / 2 + r, eps / 2 - r
    gap = ep.min() - em.max()                    # indirect gap, the Fermi level is between the two bands
    direct = (ep - em).min()
    if g < 1e-9:
        text = "gamma_K=0. The two bands cross at the Fermi level and the system is a metal."
    else:
        text = ("gamma_K=%.2f. The bands repel at the crossing. The indirect gap is %.3f t, and the direct gap is %.2f t, "
                "so the lower band is full and the system is a Kondo insulator." % (g, gap, direct))
    return dict(
        panels=[dict(title="Bands of the Kondo lattice", xlabel="k", ylabel="energy (units of t)", xlim=[-np.pi, np.pi],
                     ylim=[-3, 3], xticks=[[-np.pi, "-pi"], [0, "0"], [np.pi, "pi"]],
                     series=[dict(x=k, y=eps, kind="dash", color=4, label="gamma_K = 0"),
                             dict(x=[-np.pi, np.pi], y=[0, 0], kind="dash", color=4),
                             dict(x=k, y=ep, kind="line", color=0, label="bands"),
                             dict(x=k, y=em, kind="line", color=0)])],
        text=text,
    )
