"""Session 2, Section 2.5. The band of the chain with a second-neighbor hopping t2, from the Bloch Hamiltonian."""
META = dict(
    id="chainband", title="The band of the chain with a second-neighbor hopping",
    params=[dict(name="t2", label="second-neighbor hopping t2", min=0.0, max=1.0, step=0.05, value=0.3, fmt=2)],
    packages=["numpy"], pyqula=False,
)


def compute(p):
    import numpy as np
    t, t2 = 1.0, float(p["t2"])
    phi = np.linspace(-np.pi, np.pi, 121)
    # H(phi) = sum over the hopping dictionary {distance: amplitude} of -amp * 2 cos(distance * phi)
    hop = {1: t, 2: t2}
    e = -sum(a * 2 * np.cos(d * phi) for d, a in hop.items())
    e0 = -2 * t * np.cos(phi)
    if t2 > 0.25:
        k = np.arccos(-1 / (4 * t2))
        text = ("t2=%.2f is above t/4. The point phi=pi is now a local minimum, and two new maxima appear at "
                "phi=+-%.2f, so the band has a second extremum and a second Van Hove singularity." % (t2, k))
    else:
        text = ("t2=%.2f is below t/4. The band has one minimum at phi=0 and one maximum at phi=pi, "
                "as for the chain with nearest-neighbor hopping." % t2)
    return dict(
        panels=[dict(title="Band of the chain", xlabel="phi (quasi-momentum)", ylabel="energy (units of t)",
                     xlim=[-np.pi, np.pi],
                     ylim=[-4.2, 4.2],
                     xticks=[[-np.pi, "-pi"], [-np.pi / 2, "-pi/2"], [0, "0"], [np.pi / 2, "pi/2"], [np.pi, "pi"]],
                     series=[dict(x=phi, y=e0, kind="dash", color=4, label="t2=0"),
                             dict(x=phi, y=e, kind="line", color=0, label="t2=%.2f" % t2)])],
        text=text,
    )
