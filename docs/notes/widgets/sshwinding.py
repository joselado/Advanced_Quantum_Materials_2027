"""Session 3, Section 3.9. The SSH model: the winding of d(k) and the edge states of an open chain."""
META = dict(
    id="sshwinding", title="The winding of the SSH model",
    params=[dict(name="t", label="intracell hopping t (intercell hopping is 1)", min=0.0, max=2.0, step=0.1,
                 value=0.5, fmt=1)],
    packages=["numpy"], pyqula=False,
)


def compute(p):
    import numpy as np
    t = float(p["t"])
    k = np.linspace(-np.pi, np.pi, 121)
    d = t + np.exp(1j * k)                       # d(k) = t + e^{ik}
    gap = abs(1 - t)                             # the smallest |d(k)|, at k = pi
    if gap > 1e-9:
        ang = np.unwrap(np.angle(d))
        w = int(round((ang[-1] - ang[0]) / (2 * np.pi)))
        text = ("t=%.1f. The curve d(k) goes %d time%s around the origin, so the winding is %d and the bulk gap is %.1f. "
                % (t, w, "" if w == 1 else "s", w, 2 * gap))
        text += ("The open chain has two states at the middle of the gap, one at each end." if w == 1
                 else "The open chain has no state in the gap.")
    else:
        text = "t=1. The curve d(k) touches the origin at k=pi, the bulk gap closes and the winding is not defined."
    # open chain of M cells, intracell hopping t, intercell hopping 1, basis (A1,B1,A2,B2,...)
    M = 20
    h = np.zeros((2 * M, 2 * M))
    for n in range(2 * M - 1):
        h[n, n + 1] = h[n + 1, n] = t if n % 2 == 0 else 1.0
    e = np.linalg.eigvalsh(h)
    return dict(
        panels=[
            dict(title="d(k) in the plane", xlabel="Re d", ylabel="Im d", equal=True, xlim=[-1.2, 3.2], ylim=[-1.7, 1.7],
                 series=[dict(x=np.real(d), y=np.imag(d), kind="line", color=0)],
                 marks=[dict(x=0, y=0, label="origin")]),
            dict(title="Open chain, 20 cells", xlabel="level index", ylabel="energy (units of the intercell hopping)",
                 ylim=[-3.2, 3.2], series=[dict(x=np.arange(1, 2 * M + 1), y=e, kind="points", color=1)]),
        ],
        text=text,
    )
