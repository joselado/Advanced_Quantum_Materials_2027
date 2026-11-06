"""Session 6, Section 6.6. The Stoner criterion from the zero-temperature gap equation, for a half-filled band
with a semicircular density of states (half-bandwidth 2t). The density of states has its maximum at E_F, so the
magnetization grows continuously above the threshold."""
META = dict(
    id="stoner", title="The Stoner threshold",
    params=[dict(name="U", label="interaction U (units of t)", min=0.0, max=6.0, step=0.1, value=2.0, fmt=1)],
    packages=["numpy"], pyqula=False,
)


def compute(p):
    import numpy as np
    U = float(p["U"])
    rho0 = 1 / np.pi                                # D(E_F) per spin and per site, rho(E) = sqrt(4 - E^2) / 2 pi

    def F(x):                                       # number of states per site and spin below x
        x = np.clip(x, -2, 2)
        return 0.5 + (x * np.sqrt(4 - x ** 2) / 2 + 2 * np.arcsin(x / 2)) / (2 * np.pi)

    def f(m, U):                                    # m = n_up - n_down for the bands E -+ U m / 2, with E_F = 0
        return F(U * m / 2) - F(-U * m / 2)

    def solve(U):                                   # the largest root of f(m) = m
        m = np.linspace(0, 1, 2001)
        g = f(m, U) - m
        idx = np.where((g[:-1] > 0) & (g[1:] <= 0))[0]
        if len(idx) == 0:
            return 0.0
        i = idx[-1]
        return float(m[i] + (m[i + 1] - m[i]) * g[i] / (g[i] - g[i + 1]))

    m = np.linspace(0, 1, 51)
    Us = np.linspace(0, 6, 31)
    ms = solve(U)
    slope = U * rho0
    if slope < 1:
        text = ("U=%.2f and U D(E_F)=%.2f. The slope of f(m) at the origin is below one, "
                "so m=0 is the only crossing and the metal stays nonmagnetic." % (U, slope))
    else:
        text = ("U=%.2f and U D(E_F)=%.2f. The slope at the origin is above one, so a crossing appears at m=%.2f per site. "
                "The threshold is U=1/D(E_F)=%.2f." % (U, slope, ms, 1 / rho0))
    return dict(
        panels=[
            dict(title="Gap equation m = f(m)", xlabel="m in", ylabel="m out", xlim=[0, 1], ylim=[0, 1],
                 series=[dict(x=m, y=m, kind="dash", color=4, label="y = m"),
                         dict(x=m, y=f(m, U), kind="line", color=0, label="f(m)")],
                 marks=[dict(x=ms, y=ms)] if ms > 0 else []),
            dict(title="Magnetization against U", xlabel="U (units of t)", ylabel="m per site", xlim=[0, 6], ylim=[0, 1],
                 series=[dict(x=Us, y=[solve(u) for u in Us], kind="line", color=1),
                         dict(x=[1 / rho0] * 2, y=[0, 1], kind="dash", color=4, label="U = 1/D(E_F)")],
                 marks=[dict(x=U, y=ms)]),
        ],
        text=text,
    )
