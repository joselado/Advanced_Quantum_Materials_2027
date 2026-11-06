"""Session 9, Section 9.6. Friedel oscillations of the density around an impurity in a ring of 201 sites."""
META = dict(
    id="friedel", title="Friedel oscillations around an impurity",
    params=[dict(name="Ne", label="number of electrons Ne (odd)", min=11, max=91, step=2, value=41, fmt=0)],
    packages=["numpy"], pyqula=False,
)


def compute(p):
    import numpy as np
    Ne = int(round(p["Ne"]))
    N, v0 = 201, 1.5                              # ring, impurity strength in units of t
    h = np.zeros((N, N))
    for n in range(N):
        h[n, (n + 1) % N] = h[(n + 1) % N, n] = -1.0
    e, _ = np.linalg.eigh(h)
    h[0, 0] = v0                                  # the impurity, at site 0
    e, v = np.linalg.eigh(h)
    n_imp = (v[:, :Ne] ** 2).sum(axis=1)
    dn = n_imp - Ne / N                           # density change, relative to the clean ring
    x = np.arange(1, 101)
    y = dn[x]
    kf = np.pi * Ne / N                           # spinless chain, filling Ne/N
    c = np.abs(x[10:] * y[10:]).max()
    env = c / x
    text = ("Ne=%d, kF=%.2f, so 2kF=%.2f and the period of the oscillation is pi/kF=%.1f sites. "
            "The envelope decays as 1/x, as expected for d=1." % (Ne, kf, 2 * kf, np.pi / kf))
    return dict(
        panels=[dict(title="Density change around the impurity", xlabel="distance x (sites)", ylabel="change of density",
                     xlim=[0, 100], ylim=[-1.25 * np.abs(y).max(), 1.25 * np.abs(y).max()],
                     series=[dict(x=x, y=env, kind="dash", color=4, label="+-c/x"),
                             dict(x=x, y=-env, kind="dash", color=4),
                             dict(x=x, y=y, kind="both", color=0)])],
        text=text,
    )
