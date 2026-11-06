"""Session 4, Section 4.11. The lowest Landau levels of the square lattice with flux phi = 1/q per plaquette."""
META = dict(
    id="landaufan", title="Landau levels on the lattice",
    params=[dict(name="q", label="plaquettes per flux quantum q (flux 1/q)", min=6, max=40, step=1, value=16, fmt=0)],
    packages=["numpy"], pyqula=False,
)


def compute(p):
    import numpy as np
    q = int(round(p["q"]))
    phi = 1.0 / q
    nlev = 6
    ky = np.linspace(0, 2 * np.pi, 41)
    bands = np.zeros((len(ky), nlev))
    x = np.arange(q)
    for i, k in enumerate(ky):
        # Landau gauge, magnetic unit cell of q sites, Bloch phase kx=0 across the cell
        h = np.diag(-2 * np.cos(2 * np.pi * phi * x + k))
        for n in range(q):
            h[n, (n + 1) % q] += -1.0
            h[(n + 1) % q, n] += -1.0
        bands[i] = np.linalg.eigvalsh(h)[:nlev]
    wc = 4 * np.pi * phi                       # hbar omega_c = 4 pi t phi, with hbar^2/2m = t a^2
    series = [dict(x=ky, y=bands[:, j], kind="line", color=0, label="lattice" if j == 0 else None) for j in range(nlev)]
    for j in range(nlev):
        series.append(dict(x=[0, 2 * np.pi], y=[-4 + wc * (j + 0.5)] * 2, kind="dash", color=4,
                           label="(n+1/2) hbar omega_c" if j == 0 else None))
    width0 = bands[:, 0].max() - bands[:, 0].min()
    mean = bands.mean(axis=0)
    text = ("q=%d, flux %.3f per plaquette. The first spacing is %.3f t and the continuum value hbar omega_c = 4 pi phi t is %.3f t. "
            "The lowest level is flat as a function of ky, with a width of %.1e t, which is the degeneracy of the Landau level."
            % (q, phi, mean[1] - mean[0], wc, width0))
    return dict(
        panels=[dict(title="Lowest six bands, kx=0", xlabel="ky", ylabel="energy (units of t)", xlim=[0, 2 * np.pi],
                     xticks=[[0, "0"], [np.pi, "pi"], [2 * np.pi, "2pi"]],
                     ylim=[-4.05, -4 + wc * 6.2], series=series)],
        text=text,
    )
