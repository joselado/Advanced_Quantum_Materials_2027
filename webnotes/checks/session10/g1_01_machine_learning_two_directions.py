"""Session 10, the numbers and formulas that page 01 (Sections 10.1 and 10.2) quotes, in the steps fold, the quizzes,
the captions of xor and lrate, the problem and the box of the widget netfit.

The fits of the picture quiz, their errors and the shapes that their alt texts state, are asserted in
figures/session10/_g1_netfitquiz.py, and this script runs its check() too. The captions of xor and lrate are asserted
in their figure scripts, and their numbers are asserted here again without drawing. Every formula of the fold and of
the problem is checked by a second route, finite differences or the iteration itself. The widget is also run for H=1
to 12, for the 37 parameters of H=12 and for two open points of the old text of its box, and two networks of two and
ten hidden layers are trained on Ising snapshots, for the third feedback of the quiz on the hidden layer. The template
widgets/blocks/netfit.md is checked to hold the text of the box of the page. It writes no file."""
import os
import sys

import inspect
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', '..', 'figures', 'session10'))
sys.path.insert(0, os.path.join(HERE, '..', '..', 'figures'))
sys.path.insert(0, os.path.join(HERE, '..', '..', 'widgets', 'defs'))
import _g1_netfitquiz  # noqa: E402
import netfit  # noqa: E402


def check(name, ok, value):
    print(('OK     ' if ok else 'FAILED ') + name + ': ' + str(value), flush=True)
    assert ok, name


rng = np.random.default_rng(1)

# --- the steps fold: one neuron, one hidden layer, and the first-order drop of the loss --------------------------
w, b, x, y = 0.7, -0.3, 1.3, 0.4
f = np.tanh(w * x + b)
L1 = lambda w_, b_: (np.tanh(w_ * x + b_) - y) ** 2
d = 1e-6
fd_w = (L1(w + d, b) - L1(w - d, b)) / (2 * d)
fd_b = (L1(w, b + d) - L1(w, b - d)) / (2 * d)
check('one neuron, dL/dw = 2(f-y)(1-f^2)x against finite differences', abs(fd_w - 2 * (f - y) * (1 - f ** 2) * x) < 1e-8,
      (round(fd_w, 9), round(2 * (f - y) * (1 - f ** 2) * x, 9)))
check('one neuron, dL/db is the same without the factor x', abs(fd_b - 2 * (f - y) * (1 - f ** 2)) < 1e-8, round(fd_b, 9))

H = 5
W, B, V, c = rng.normal(size=H), rng.normal(size=H), rng.normal(size=H), 0.2


def loss_layer(W_, B_, V_, c_, x_=x, y_=y):
    return (np.sum(V_ * np.tanh(W_ * x_ + B_)) + c_ - y_) ** 2


a = np.tanh(W * x + B)
delta = 2 * (np.sum(V * a) + c - y)
delta_j = delta * V * (1 - a ** 2)
grads = {'v': delta * a, 'w': delta_j * x, 'b': delta_j}
fd = {k: np.zeros(H) for k in grads}
for j in range(H):
    e = np.zeros(H); e[j] = d
    fd['v'][j] = (loss_layer(W, B, V + e, c) - loss_layer(W, B, V - e, c)) / (2 * d)
    fd['w'][j] = (loss_layer(W + e, B, V, c) - loss_layer(W - e, B, V, c)) / (2 * d)
    fd['b'][j] = (loss_layer(W, B + e, V, c) - loss_layer(W, B - e, V, c)) / (2 * d)
err = max(np.abs(fd[k] - grads[k]).max() for k in grads)
check('one hidden layer, dL/dv_j = delta a_j, dL/dw_j = delta_j x, dL/db_j = delta_j, delta_j = delta v_j (1-a_j^2)',
      err < 1e-7, err)

# with many examples the gradient of the sum (10.1) is the sum of the gradients
xs, ys = rng.normal(size=4), rng.normal(size=4)
tot = lambda V_: sum(loss_layer(W, B, V_, c, xx, yy) for xx, yy in zip(xs, ys))
g_sum = sum(2 * (np.sum(V * np.tanh(W * xx + B)) + c - yy) * np.tanh(W * xx + B) for xx, yy in zip(xs, ys))
g_fd = np.array([(tot(V + d * np.eye(H)[j]) - tot(V - d * np.eye(H)[j])) / (2 * d) for j in range(H)])
check('the gradient of the sum over examples is the sum of the gradients', np.abs(g_sum - g_fd).max() < 1e-7,
      np.abs(g_sum - g_fd).max())

# L(theta - eta grad L) = L - eta |grad L|^2 to first order: the ratio of the drop to eta |grad L|^2 goes to 1
theta0 = np.concatenate([W, B, V])
def Lt(t):
    """The loss (10.1) of the hidden layer over the four examples, as a function of all the weights and biases."""
    return sum(loss_layer(t[:H], t[H:2 * H], t[2 * H:], c, xx, yy) for xx, yy in zip(xs, ys))


g = np.array([(Lt(theta0 + d * np.eye(3 * H)[j]) - Lt(theta0 - d * np.eye(3 * H)[j])) / (2 * d) for j in range(3 * H)])
ratios = [(Lt(theta0) - Lt(theta0 - eta * g)) / (eta * g @ g) for eta in (1e-2, 1e-3, 1e-4)]
check('the drop of the loss over eta |grad L|^2 goes to 1 as eta goes to 0', abs(ratios[-1] - 1) < 1e-3
      and abs(ratios[-1] - 1) < abs(ratios[0] - 1), np.round(ratios, 5))
check('a small step lowers the loss', Lt(theta0 - 1e-3 * g) < Lt(theta0), (Lt(theta0), Lt(theta0 - 1e-3 * g)))

# --- XOR, the quiz on the hidden layer and the caption of xor -------------------------------------------------------
X = np.array([(0, 0), (1, 1), (0, 1), (1, 0)], float)
Y = np.array([0, 0, 1, 1])
wl = rng.normal(size=(200000, 2)); bl = rng.normal(size=200000) * 2
s = X @ wl.T + bl
sep = (np.all(s[Y == 1] > 0, 0) & np.all(s[Y == 0] < 0, 0)) | (np.all(s[Y == 1] < 0, 0) & np.all(s[Y == 0] > 0, 0))
check('no line w.x+b separates XOR, the two classes have the same sum of inputs', not sep.any()
      and np.allclose(X[Y == 0].sum(0), X[Y == 1].sum(0)), X[Y == 0].sum(0))
step = lambda z: (z > 0).astype(int)
check('two hidden step neurons on x1+x2=1/2 and x1+x2=3/2, output their difference, give XOR',
      np.array_equal(step(X.sum(1) - 0.5) - step(X.sum(1) - 1.5), Y), Y)

# --- the quiz on the learning rate, the caption of lrate and the problem --------------------------------------------
it = lambda eta, a_, n, t0=1.0: np.array([(1 - eta * a_) ** k * t0 for k in range(n + 1)])


def descend(eta, a_, n, t0=1.0):
    """The iteration of (10.1) itself, with a numerical gradient of a theta^2/2."""
    out, t = [t0], t0
    for _ in range(n):
        gr = (a_ * (t + d) ** 2 / 2 - a_ * (t - d) ** 2 / 2) / (2 * d)
        t = t - eta * gr
        out.append(t)
    return np.array(out)


check('L=theta^2/2, the gradient is theta and the update (1-eta) theta', all(np.allclose(descend(e, 1, 6), it(e, 1, 6),
                                                                                       atol=1e-7) for e in (0.5, 1, 2, 2.5)), True)
check('eta=1 reaches the minimum in one step', abs(descend(1, 1, 1)[1]) < 1e-8, descend(1, 1, 1))
check('eta=2 jumps between +1 and -1', np.allclose(descend(2, 1, 4), [1, -1, 1, -1, 1], atol=1e-6), descend(2, 1, 4))
t25 = descend(2.5, 1, 4)
check('eta=2.5 multiplies theta by -1.5 and the loss by 2.25', np.allclose(t25[1:] / t25[:-1], -1.5, atol=1e-6)
      and np.allclose(t25[1:] ** 2 / t25[:-1] ** 2, 2.25, atol=1e-6), np.round(t25, 4))
check('eta=0.5 halves theta at every step, the caption has four steps', np.allclose(descend(0.5, 1, 4),
                                                                                  0.5 ** np.arange(5), atol=1e-7), descend(0.5, 1, 4))
check('a large eta makes |theta| and the gradient grow', abs(t25[-1]) > abs(t25[0]), abs(t25[-1]))

a4 = 4.0
conv = {e: abs(descend(e, a4, 1000)[-1]) for e in (0.05, 0.25, 0.3, 0.49, 0.5, 0.51, 0.6)}
check('a=4, theta_n = (1 - eta a)^n theta_0', all(np.allclose(descend(e, a4, 10, 0.7), it(e, a4, 10, 0.7), atol=1e-6)
                                                  for e in (0.1, 0.3, 0.6)), True)
check('a=4, the iteration goes to zero for eta below 2/a=0.5 and not at or above it',
      all(conv[e] < 1e-6 for e in (0.05, 0.25, 0.3, 0.49)) and conv[0.5] > 0.99 and conv[0.51] > 1, conv)
check('a=4, eta=1/a=0.25 reaches the minimum in one step', abs(descend(0.25, a4, 1)[1]) < 1e-8, descend(0.25, a4, 1))
check('a=4, eta=0.5 jumps between theta_0 and -theta_0', np.allclose(descend(0.5, a4, 4), [1, -1, 1, -1, 1], atol=1e-6),
      descend(0.5, a4, 4))
t6 = descend(0.6, a4, 5)
check('a=4, eta=0.6 multiplies theta by -1.4 at every step', np.allclose(t6[1:] / t6[:-1], -1.4, atol=1e-6), np.round(t6, 3))
t3 = descend(0.3, a4, 5)
check('a=4, between 1/a and 2/a theta changes sign at every step and goes to zero', np.all(t3[1:] * t3[:-1] < 0)
      and conv[0.3] < 1e-6, np.round(t3, 3))

# many parameters: a quadratic loss with curvatures 4 and 0.1 along two rotated directions
R = np.array([[np.cos(0.6), -np.sin(0.6)], [np.sin(0.6), np.cos(0.6)]])
Hm = R @ np.diag([4.0, 0.1]) @ R.T


def descend2(eta, n):
    t = np.array([1.0, 1.0])
    for _ in range(n):
        t = t - eta * Hm @ t
    return t


check('two directions with curvatures 4 and 0.1, the largest curvature sets the limit 2/a_max = 0.5',
      np.linalg.norm(descend2(0.49, 2000)) < 1e-6 and np.linalg.norm(descend2(0.51, 2000)) > 1,
      (np.linalg.norm(descend2(0.49, 2000)), np.linalg.norm(descend2(0.51, 2000))))
flat = R @ np.array([0, 1.0])
check('at eta=0.49 the flat direction shrinks only by 1 - eta a = 0.951 per step', abs((flat @ descend2(0.49, 51)) /
                                                                                       (flat @ descend2(0.49, 50)) - 0.951) < 1e-9,
      (flat @ descend2(0.49, 51)) / (flat @ descend2(0.49, 50)))

# --- the picture quiz and the box of the widget -------------------------------------------------------------------
out = _g1_netfitquiz.check()
check('picture quiz, the errors 0.46, 0.23 and 2.3e-4, and 0, 2 and 6 extrema', [round(out[h][2], 6) for h in (1, 3, 12)]
      == [0.46, 0.23, 2.3e-4], [out[h][2] for h in (1, 3, 12)])
mono = []
for _ in range(2000):
    v_, w_, b_, c_ = rng.normal(size=4) * 3
    yy = v_ * np.tanh(w_ * np.linspace(-1, 1, 401) + b_) + c_
    dy = np.diff(yy)
    mono.append(np.all(dy >= -1e-15) or np.all(dy <= 1e-15))
check('one neuron v tanh(wx+b)+c is monotonic for every choice of v, w, b, c (2000 random draws)', all(mono), sum(mono))
d1 = netfit.compute(dict(H=1))
check('the widget trains for 4000 steps on 41 points of sin(3 pi x)', 'After 4000 steps' in d1['text']
      and len(d1['panels'][0]['series'][1]['x']) == 41, d1['text'])

# the 37 parameters of H=12 in the picture quiz, counted on the arrays that compute() of the widget trains, and in
# the text that the widget prints
seen = {}


def _grab(frame, event, arg):
    if event == 'return' and frame.f_code is netfit.compute.__code__:
        seen['sizes'] = [p.size for p in frame.f_locals['params']]


sys.setprofile(_grab)
try:
    d12 = netfit.compute(dict(H=12))
finally:
    sys.setprofile(None)
check('the fit with H=12 has 37 parameters, on the arrays w1, b1, w2, b2 of the widget and in its text',
      sum(seen['sizes']) == 37 and 'H=12 hidden neurons, 37 parameters.' in d12['text'], seen['sizes'])

# the widget for H=1 to 12, the run that it draws. The text of its box was corrected on 2026-11-22: one to three
# neurons do not follow the six extrema, from four on every fit does, and the error falls on the whole but not at every
# step of H. The code takes 4000 steps of Adam on the mean of the squared error, read in its source
srcw = inspect.getsource(netfit.compute)
check('the widget code: 4000 steps of Adam, with moments m and s, on the gradient of the mean squared error',
      'steps = 0.02, 0.9, 0.999, 4000' in srcw.replace('lr, b_1, b_2, ', '') and 'm[i] = b_1 * m[i]' in srcw
      and 's[i] = b_2 * s[i]' in srcw and 'd_out = 2 * r / len(x)' in srcw and '(r ** 2).mean()' in srcw, 'source')
fits = {h: _g1_netfitquiz.fit(h) for h in range(1, 13)}
nex = {h: _g1_netfitquiz.extrema(fits[h][1]) for h in fits}
err = {h: fits[h][2] for h in fits}
check('the widget: one and two neurons give a curve with no extremum', nex[1] == 0 and nex[2] == 0, (nex[1], nex[2]))
check('the widget: three neurons give two extrema, and from H=4 on every fit has the six extrema of the target',
      nex[3] == 2 and all(nex[h] == 6 for h in range(4, 13)), nex)
check('the widget: the error is 3.0e-3, 3.4e-3 and 5.0e-3 for H=5, 6 and 7, so it rises from H=5 to H=7',
      [err[h] for h in (5, 6, 7)] == [3.0e-3, 3.4e-3, 5.0e-3], [err[h] for h in (5, 6, 7)])
check('the widget: the error is 0.46 for H=1 and 2.3e-4 for H=12, lower overall', err[1] == 0.46 and err[12] == 2.3e-4,
      err)
# decided on 2026-11-22: the template webnotes/widgets/blocks/netfit.md holds the same text as the box of page 01, so
# that a new conversion of the widget box gives the corrected text, with the numbers asserted above
import re  # noqa: E402
page01 = open(os.path.join(HERE, '..', '..', 'pages', 'session10',
                           '01-machine-learning-and-many-body-physics-in-two-directions.md'), encoding='utf-8').read()
box = re.search(r'^::: \{\.widget name="netfit"\}\n.*?\n:::\n', page01, re.S | re.M)
template = open(os.path.join(HERE, '..', '..', 'widgets', 'blocks', 'netfit.md'), encoding='utf-8').read()
check('the template blocks/netfit.md is the box of page 01, with Adam, one to three neurons and the loss on the whole',
      box is not None and template == box.group(0) and '4000 steps of Adam' in template
      and 'With one to three neurons' in template and 'not at every step of $H$' in template, 'same text')

# --- the third feedback of the quiz on the hidden layer: the same Ising snapshots fitted with two hidden layers or
# with ten. Metropolis snapshots of the Ising model (10.9) with J=1 on 8x8 periodic sites, 100 at k_BT=1.5 (ordered,
# with both signs of m) and 100 at k_BT=3.5, the temperatures of igt_hist, with a one-hot label. A network of tanh
# layers of width 8 and a linear output of two nodes, trained by the plain update of (10.1) on the mean of the
# squared error, 2000 steps with eta=0.05. Fitted means every training snapshot classified right.
mc = np.random.default_rng(5)
Lsite = 8
ii, jj = np.indices((Lsite, Lsite))
masks = [(ii + jj) % 2 == 0, (ii + jj) % 2 == 1]


def snapshots(T, n, ordered):
    s = np.ones((n, Lsite, Lsite)) if ordered else mc.choice([-1., 1.], (n, Lsite, Lsite))
    for _ in range(300):
        for m_ in masks:
            nb = np.roll(s, 1, 1) + np.roll(s, -1, 1) + np.roll(s, 1, 2) + np.roll(s, -1, 2)
            flip = (mc.random(s.shape) < np.exp(-2 * s * nb / T)) & m_
            s = np.where(flip, -s, s)
    if ordered:
        s = s * mc.choice([-1., 1.], (n, 1, 1))
    return s.reshape(n, -1)


Xi = np.vstack([snapshots(1.5, 100, True), snapshots(3.5, 100, False)])
Yi = np.vstack([np.tile([1., 0.], (100, 1)), np.tile([0., 1.], (100, 1))])
check('Ising snapshots, mean |m| near 1 at k_BT=1.5 and small at 3.5, with both signs of m below T_c',
      np.abs(Xi[:100].mean(1)).mean() > 0.9 and np.abs(Xi[100:].mean(1)).mean() < 0.4
      and (Xi[:100].mean(1) > 0).any() and (Xi[:100].mean(1) < 0).any(),
      (np.abs(Xi[:100].mean(1)).mean(), np.abs(Xi[100:].mean(1)).mean()))


def train_depth(nh, width=8, steps=2000, eta=0.05):
    r = np.random.default_rng(0)
    sizes = [Xi.shape[1]] + [width] * nh + [2]
    Ws = [r.normal(0, 1 / np.sqrt(p), (p, q)) for p, q in zip(sizes[:-1], sizes[1:])]
    Bs = [np.zeros(q) for q in sizes[1:]]

    def forward(Xin):
        acts = [Xin]
        for k in range(len(Ws)):
            z = acts[-1] @ Ws[k] + Bs[k]
            acts.append(np.tanh(z) if k < len(Ws) - 1 else z)
        return acts
    for _ in range(steps):
        acts = forward(Xi)
        dz = 2 * (acts[-1] - Yi) / len(Xi)
        for k in range(len(Ws) - 1, -1, -1):
            gW, gB = acts[k].T @ dz, dz.sum(0)
            if k > 0:
                dz = (dz @ Ws[k].T) * (1 - acts[k] ** 2)
            Ws[k] -= eta * gW
            Bs[k] -= eta * gB
    out = forward(Xi)[-1]
    return float(((out - Yi) ** 2).sum(1).mean()), float((out.argmax(1) == Yi.argmax(1)).mean())


fit_depth = {nh: train_depth(nh) for nh in (2, 10)}
check('the same Ising snapshots are fitted with two hidden layers and with ten, every snapshot classified right',
      all(acc == 1.0 and lo < 1e-2 for lo, acc in fit_depth.values()), fit_depth)
