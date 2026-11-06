"""Session 1, Section 1.10. The eigenstates of a finite tight-binding chain, computed with pyqula."""
META = dict(
    id="island", title="A finite chain is a particle in a box",
    params=[dict(name="N", label="number of sites N", min=2, max=40, step=1, value=12, fmt=0)],
    packages=["numpy", "scipy", "matplotlib"], pyqula=True,
)


def compute(p):
    import numpy as np
    from pyqula import geometry
    N = int(round(p["N"]))
    g = geometry.chain().get_supercell(N)  # N sites in the unit cell
    g.dimensionality = 0                   # cut the chain, so that the island is finite
    h = g.get_hamiltonian(has_spin=False)
    (e, v) = h.get_eigenvectors()          # energies in units of the hopping t, one eigenvector per column
    order = np.argsort(e)
    e = np.array(e)[order]
    v = np.array(v)[:, order]
    x = np.arange(1, N + 1)
    levels = []
    for j in range(min(3, N)):
        levels.append(dict(x=x, y=np.abs(v[:, j]) ** 2, kind="both", color=j, label="level %d" % (j + 1)))
    box = np.sin(np.pi * x / (N + 1)) ** 2 * 2 / (N + 1)
    levels.append(dict(x=x, y=box, kind="dash", color=3, label="box, level 1"))
    spacing = e[1] - e[0] if N > 1 else 0.0
    return dict(
        panels=[
            dict(title="Energy levels", xlabel="level index", ylabel="energy (units of t)",
                 series=[dict(x=np.arange(1, N + 1), y=e, kind="points", color=0)]),
            dict(title="Probability density of the lowest levels", xlabel="site", ylabel="|psi|^2",
                 series=levels),
        ],
        text="N=%d. The lowest level is at E=%.3f t, the first spacing is %.3f t, and the lowest state has no node. "
             "Level j has j-1 nodes, as in a box of length N+1." % (N, e[0], spacing),
    )
