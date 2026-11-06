"""Session 5, Section 5.17. The BdG spectrum of an open Kitaev chain as a function of the chemical potential mu."""
META = dict(
    id="kitaevbdg", title="The BdG spectrum of the Kitaev chain",
    params=[dict(name="mu", label="chemical potential mu (t = Delta = 1)", min=-3.0, max=3.0, step=0.1, value=0.5, fmt=1)],
    packages=["numpy"], pyqula=False,
)


def compute(p):
    import numpy as np
    mu = float(p["mu"])
    N, t, D = 30, 1.0, 1.0
    h = -mu * np.eye(N)                          # normal part: -t hopping and -mu onsite
    d = np.zeros((N, N))                         # pairing, antisymmetric for spinless fermions
    for n in range(N - 1):
        h[n, n + 1] = h[n + 1, n] = -t
        d[n + 1, n], d[n, n + 1] = D, -D
    H = np.block([[h, d], [d.T, -h]])            # Nambu basis (c_1..c_N, c_1^+..c_N^+)
    e, v = np.linalg.eigh(H)
    j = np.argsort(np.abs(e))[:2]                # the two levels closest to E=0
    w = sum(v[:N, i] ** 2 + v[N:, i] ** 2 for i in j) / 2
    e0 = np.abs(e[j]).max()
    gap = min(abs(mu - 2 * t), abs(mu + 2 * t))
    if abs(mu) < 2 * t:
        ends = w[:3].sum() + w[-3:].sum()
        at = "at zero energy (|E|<1e-8 t)" if e0 < 1e-8 else "at |E|=%.1e t" % e0
        text = ("mu=%.1f is inside |mu|<2t. The bulk gap is %.1f, and the two levels closest to zero are %s. "
                "A total weight %.2f of them sits on the three outer sites at each end." % (mu, gap, at, ends))
    elif abs(abs(mu) - 2 * t) < 1e-9:
        text = "mu=%.1f. The bulk gap closes at the transition between the two phases." % mu
    else:
        text = ("mu=%.1f is outside |mu|<2t. The bulk gap is %.1f, the levels closest to zero are at |E|=%.2f t, "
                "and their states are spread over the whole chain." % (mu, gap, e0))
    return dict(
        panels=[
            dict(title="BdG levels, 30 sites", xlabel="level index", ylabel="energy (units of t)", ylim=[-3.2, 3.2],
                 series=[dict(x=np.arange(1, 2 * N + 1), y=e, kind="points", color=0)]),
            dict(title="Weight of the two levels closest to E=0", xlabel="site", ylabel="|u|^2+|v|^2",
                 series=[dict(x=np.arange(1, N + 1), y=w, kind="line", color=1)]),
        ],
        text=text,
    )
