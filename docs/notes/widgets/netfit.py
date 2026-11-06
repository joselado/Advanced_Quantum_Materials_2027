"""Session 10, Section 10.2. A network with one hidden layer of tanh units, trained by gradient descent (Adam) on y=sin(3 pi x)."""
META = dict(
    id="netfit", title="A small network fits a function",
    params=[dict(name="H", label="hidden neurons H", min=1, max=12, step=1, value=3, fmt=0)],
    packages=["numpy"], pyqula=False,
)


def compute(p):
    import numpy as np
    H = int(round(p["H"]))
    rng = np.random.default_rng(7)
    x = np.linspace(-1, 1, 41)[:, None]
    y = np.sin(3 * np.pi * x)
    w1 = rng.normal(0, 1.5, (1, H)); b1 = rng.normal(0, 0.5, H)
    w2 = rng.normal(0, 0.5, (H, 1)); b2 = np.zeros(1)
    params = [w1, b1, w2, b2]
    m = [np.zeros_like(a) for a in params]; s = [np.zeros_like(a) for a in params]
    lr, b_1, b_2, steps = 0.02, 0.9, 0.999, 4000
    loss = []
    for t in range(1, steps + 1):
        a = np.tanh(x @ w1 + b1)                  # hidden layer
        out = a @ w2 + b2                         # linear output
        r = out - y
        if t % 100 == 0:
            loss.append(float((r ** 2).mean()))
        d_out = 2 * r / len(x)                    # gradient of the mean squared error, backpropagated by hand
        d_a = (d_out @ w2.T) * (1 - a ** 2)
        grads = [x.T @ d_a, d_a.sum(0), a.T @ d_out, d_out.sum(0)]
        for i, (a_, g_) in enumerate(zip(params, grads)):
            m[i] = b_1 * m[i] + (1 - b_1) * g_
            s[i] = b_2 * s[i] + (1 - b_2) * g_ ** 2
            a_ -= lr * (1 - 0.95 * t / steps) * (m[i] / (1 - b_1 ** t)) / (np.sqrt(s[i] / (1 - b_2 ** t)) + 1e-8)
    xf = np.linspace(-1, 1, 101)[:, None]
    fit = np.tanh(xf @ w1 + b1) @ w2 + b2
    final = loss[-1]
    return dict(
        panels=[
            dict(title="Network output", xlabel="x", ylabel="y", xlim=[-1, 1], ylim=[-1.6, 1.6],
                 series=[dict(x=xf[:, 0], y=np.sin(3 * np.pi * xf[:, 0]), kind="dash", color=4, label="target sin(3 pi x)"),
                         dict(x=x[:, 0], y=y[:, 0], kind="points", color=4, label="training points"),
                         dict(x=xf[:, 0], y=fit[:, 0], kind="line", color=0, label="network")]),
            dict(title="Training loss", xlabel="training step", ylabel="log10 of the mean squared error",
                 series=[dict(x=np.arange(1, len(loss) + 1) * 100, y=np.log10(np.array(loss) + 1e-12), kind="line", color=1)]),
        ],
        text="H=%d hidden neurons, %d parameters. After %d steps the mean squared error is %.1e."
             % (H, 3 * H + 1, steps, final),
    )
