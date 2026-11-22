"""Session 10, the numbers that page 04 (Section 10.4, tensor networks for machine learning) quotes.

One check script per page is the rule: every number of a caption, a feedback, a fold or a solution is an assert, here
or in the figure script that draws it. The page has no figure script with numbers, since mps_chain.py is a drawing.
Two sites are written in the order up-up, up-down, down-up, down-down. The pixel map is
phi(x) = (cos(pi x/2), sin(pi x/2)), as on the conventions sheet. It finds the repository from its own path, imports
nothing of it, and writes no file. It reads the text of mps_chain.py for the D and the spins of the drawing, and
does not run it, since that script writes its SVG."""
import ast, os, re
import numpy as np

REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))


def check(name, ok, value):
    print(('OK     ' if ok else 'FAILED ') + name + ': ' + str(value), flush=True)
    assert ok, name


rng = np.random.default_rng(2)
UP, DN = 0, 1

# ---------------------------------------------------------------------------- counting, the fold and the first quiz
L, d, D = 100, 2, 10
check('L d D^2 = 100 x 2 x 100 = 20000', L * d * D ** 2 == 20000, L * d * D ** 2)
check('2^100 is about 1.3e30', round(2.0 ** 100 / 1e30, 1) == 1.3, 2.0 ** 100)
check('which is 26 orders of magnitude more, 25.8', round(np.log10(2.0 ** 100 / 20000)) == 26
      and abs(np.log10(2.0 ** 100 / 20000) - 25.8) < 0.05, np.log10(2.0 ** 100 / 20000))
A1 = rng.normal(size=(L, d, 1, 1))
s1 = rng.integers(0, d, size=L)
c1 = np.trace(np.linalg.multi_dot([A1[i, s1[i]] for i in range(L)]))
check('D = 1, the matrices are numbers, 200 of them for L = 100 and d = 2, and the trace is their product',
      A1.size == 200 and abs(c1 - np.prod([A1[i, s1[i], 0, 0] for i in range(L)])) < 1e-12 * abs(c1), A1.size)
src = open(os.path.join(REPO, 'webnotes', 'figures', 'session10', 'mps_chain.py')).read()
D_drawn = int(re.search(r'^D = (\d+)$', src, re.M).group(1))
s_drawn = ast.literal_eval(re.search(r'^s = (\[.*\])$', src, re.M).group(1))
check('the mps_chain drawing has D = %d and %d spins, with the two matrices A^up and A^down, so 2 D^2 = %d numbers '
      'per site' % (D_drawn, len(s_drawn), 2 * D_drawn ** 2), D_drawn == 3 and len(s_drawn) == 5
      and r'A^{\uparrow}' in src and r'A^{\downarrow}' in src and 2 * D_drawn ** 2 == 18, (D_drawn, s_drawn))
A = rng.normal(size=(L, d, D, D))
check('the matrices of (10.6) for L = 100, d = 2 and D = 10 hold 20000 numbers', A.size == 20000, A.size)


def coefficient(A, s):
    """C(s) of (10.6), with a count of the products of two D x D matrices."""
    M, products = A[0, s[0]], 0
    for i in range(1, len(s)):
        M = M @ A[i, s[i]]
        products += 1
    return np.trace(M), products


s = rng.integers(0, d, size=L)
cs, nprod = coefficient(A / np.sqrt(D), s)
small = rng.normal(size=(6, 2, 3, 3))
s6 = rng.integers(0, 2, size=6)
ein = np.einsum('ab,bc,cd,de,ef,fa->', *[small[i, s6[i]] for i in range(6)])
check('one coefficient takes L - 1 = 99 products of D x D matrices and a trace, and the loop gives the trace of the '
      'product, checked against einsum on 6 sites', nprod == L - 1 == 99 and abs(coefficient(small, s6)[0] - ein)
      < 1e-12 * max(1, abs(ein)), nprod)

# ---------------------------------------------------------------------------- the opener, the range of (10.6)
for Ls in (8, 10):
    psi = rng.normal(size=2 ** Ls) + 1j * rng.normal(size=2 ** Ls)
    r = np.linalg.matrix_rank(psi.reshape(2 ** (Ls // 2), 2 ** (Ls // 2)))
    check('a random state of %d spins has the Schmidt rank 2^(L/2) = %d at the middle cut%s' % (Ls, 2 ** (Ls // 2),
          ', the 32 of the fold' if Ls == 10 else ''), r == 2 ** (Ls // 2), r)
# corrected on 2026-11-22, the fold says "an even number L of spins": for odd L the middle cut into L//2 and the rest
# gives 2^((L-1)/2), which is not 2^(L/2)
odd = {}
for Ls in (7, 9, 11):
    psi = rng.normal(size=2 ** Ls) + 1j * rng.normal(size=2 ** Ls)
    odd[Ls] = np.linalg.matrix_rank(psi.reshape(2 ** (Ls // 2), 2 ** (Ls - Ls // 2)))
check('for odd L = 7, 9 and 11 the rank at the middle cut is 2^((L-1)/2) = 8, 16 and 32, not 2^(L/2)',
      odd == {7: 8, 9: 16, 11: 32} and all(2 ** (Ls / 2) != odd[Ls] for Ls in odd), odd)


def trace_state(Ls, Db):
    B = rng.normal(size=(Ls, 2, Db, Db))
    out = np.zeros(2 ** Ls)
    for k in range(2 ** Ls):
        out[k] = coefficient(B, [(k >> (Ls - 1 - i)) & 1 for i in range(Ls)])[0]
    return out


for Db in (2, 3):
    r = np.linalg.matrix_rank(trace_state(8, Db).reshape(16, 16))
    check('the trace of (10.6) on 8 sites with D = %d has the rank D^2 = %d at the middle, so a generic state of L '
          'spins needs D^2 >= 2^(L/2), exponential in L' % (Db, Db ** 2), r == Db ** 2, r)
Bo = [rng.normal(size=(2, 1, 3))] + [rng.normal(size=(2, 3, 3)) for _ in range(6)] + [rng.normal(size=(2, 3, 1))]
op8 = np.array([np.linalg.multi_dot([Bo[i][(k >> (7 - i)) & 1] for i in range(8)])[0, 0] for k in range(2 ** 8)])
check('the open form with D = 3 has the rank at most D at the middle, so there D >= 2^(L/2)',
      np.linalg.matrix_rank(op8.reshape(16, 16)) == 3, np.linalg.matrix_rank(op8.reshape(16, 16)))


# ---------------------------------------------------------------------------- the quiz on the three expressions
prod_err, sum_err, trace_rank = [], [], []
for _ in range(5):
    A1, A2 = rng.normal(size=(2, 2, 2, 2))              # two sites, each with a matrix 2 x 2 for up and for down
    trace_form = np.array([np.trace(A1[a] @ A2[b]) for a in (UP, DN) for b in (UP, DN)])
    prod_form = np.array([np.trace(A1[a]) * np.trace(A2[b]) for a in (UP, DN) for b in (UP, DN)])
    sum_form = np.array([np.trace(A1[a]) + np.trace(A2[b]) for a in (UP, DN) for b in (UP, DN)])
    prod_err.append(abs(prod_form[1] * prod_form[2] - prod_form[0] * prod_form[3]))
    sum_err.append(abs(sum_form[0] + sum_form[3] - sum_form[1] - sum_form[2]))
    trace_rank.append(np.linalg.matrix_rank(trace_form.reshape(2, 2)))
check('product of traces, C(ud) C(du) = C(uu) C(dd) for random matrices, a product state', max(prod_err) < 1e-12,
      max(prod_err))
check('sum of traces, C(uu) + C(dd) = C(ud) + C(du) for random matrices', max(sum_err) < 1e-12, max(sum_err))
# The sum of traces is C(s1, s2) = t1(s1) + t2(s2), a linear map from (t1u, t1d, t2u, t2d) to (uu, ud, du, dd).
Msum = np.array([[1, 0, 1, 0], [1, 0, 0, 1], [0, 1, 1, 0], [0, 1, 0, 1]], dtype=float)
sol, *_ = np.linalg.lstsq(Msum[:3], np.array([1.0, 0.0, 0.0]), rcond=None)
null = np.linalg.svd(Msum[:3])[2][-1]
resid = np.linalg.lstsq(Msum, np.array([1.0, 0.0, 0.0, 0.0]), rcond=None)[0]
check('with C(uu) = 1 and C(ud) = C(du) = 0 the sum of traces gives C(dd) = -1 for every solution, so |uu> is out '
      'of reach', abs(Msum[3] @ sol + 1) < 1e-12 and abs(Msum[3] @ null) < 1e-12 and np.linalg.matrix_rank(Msum) == 3
      and np.linalg.norm(Msum @ resid - [1, 0, 0, 0]) > 0.4, (Msum[3] @ sol, np.linalg.norm(Msum @ resid - [1, 0, 0, 0])))
check('the trace of a product of random 2 x 2 matrices is entangled across the cut, Schmidt rank 2',
      min(trace_rank) == 2, trace_rank)
singlet = np.array([0, 1, -1, 0]) / np.sqrt(2)
check('the singlet has C(ud) C(du) = -1/2 and C(uu) C(dd) = 0', abs(singlet[1] * singlet[2] * 2 + 1) < 1e-14
      and singlet[0] * singlet[3] == 0, (singlet[1] * singlet[2], singlet[0] * singlet[3]))
Atr = [np.diag([1.0, 0.0]), np.diag([0.0, 1.0])]
Btr = [-np.diag([0.0, 1.0]), np.diag([1.0, 0.0])]
tr = np.array([np.trace(Atr[a] @ Btr[b]) for a in (UP, DN) for b in (UP, DN)])
check('the trace form with diag(1,0), diag(0,1) and -diag(0,1), diag(1,0) gives 0, 1, -1, 0, sqrt2 times the singlet',
      np.allclose(tr, [0, 1, -1, 0]) and np.allclose(tr, np.sqrt(2) * singlet), tr)
sym = []
for Db in (2, 4):
    P = rng.normal(size=(2, Db, Db))
    sym.append(abs(np.trace(P[UP] @ P[DN]) - np.trace(P[DN] @ P[UP])))
check('the same pair of matrices on both sites gives C(ud) = C(du), since the trace does not change under the swap',
      max(sym) < 1e-12, max(sym))

# ---------------------------------------------------------------------------- the problem
a = [np.array([1.0, 0.0]), np.array([0.0, 1.0])]
b = [np.array([0.0, -1.0]), np.array([1.0, 0.0])]
op = np.array([a[x] @ b[y] for x in (UP, DN) for y in (UP, DN)])
check('the open form with a_up = (1,0), a_dn = (0,1), b_up = (0,-1), b_dn = (1,0) gives 0, 1, -1, 0',
      np.allclose(op, [0, 1, -1, 0]), op)
d1_err = []
for _ in range(5):
    a1, b1 = rng.normal(size=2), rng.normal(size=2)
    c = np.array([a1[x] * b1[y] for x in (UP, DN) for y in (UP, DN)])
    d1_err.append(abs(c[1] * c[2] - c[0] * c[3]))
check('D = 1, C(s1,s2) = a(s1) b(s2) has C(ud) C(du) = C(uu) C(dd)', max(d1_err) < 1e-12, max(d1_err))
sv = np.linalg.svd(singlet.reshape(2, 2), compute_uv=False)
check('the singlet has two Schmidt values 1/sqrt2, so a cut needs D = 2', np.allclose(sv, [1 / np.sqrt(2)] * 2), sv)

# ---------------------------------------------------------------------------- the classifier and its quiz
def phi(x):
    return np.array([np.cos(np.pi * x / 2), np.sin(np.pi * x / 2)])


def tensor_product(x):
    v = np.array([1.0])
    for xi in x:
        v = np.kron(v, phi(xi))
    return v


def tree_output(x, T):
    """A binary tree on 8 pixels with bond 3 and a label leg of 2 on the top tensor."""
    legs = [phi(xi) for xi in x]
    level = 0
    while len(legs) > 1:
        legs = [np.einsum('a,b,abc->c', legs[2 * i], legs[2 * i + 1], T[level][i]) for i in range(len(legs) // 2)]
        level += 1
    return legs[0]


Dt = 3
T = [[rng.normal(size=(2, 2, Dt)) for _ in range(4)], [rng.normal(size=(Dt, Dt, Dt)) for _ in range(2)],
     [rng.normal(size=(Dt, Dt, 2))]]
W = np.zeros((2 ** 8, 2))
for k in range(2 ** 8):
    bits = [(k >> (7 - i)) & 1 for i in range(8)]
    level, cur = 0, [np.eye(2)[bt] for bt in bits]
    while len(cur) > 1:
        cur = [np.einsum('a,b,abc->c', cur[2 * i], cur[2 * i + 1], T[level][i]) for i in range(len(cur) // 2)]
        level += 1
    W[k] = cur[0]
x = rng.uniform(size=8)
v = tensor_product(x)
check('the tensor product of 8 pixels has 2^8 = 256 components and norm 1', v.size == 256 and abs(np.linalg.norm(v) - 1)
      < 1e-12, (v.size, np.linalg.norm(v)))
check('the output of the tree is the 256 x 2 matrix W applied to the tensor product, linear in it',
      np.allclose(tree_output(x, T), v @ W), np.max(np.abs(tree_output(x, T) - v @ W)))
y_out = tree_output(x, T)
legs2 = [2 * phi(x[0])] + [phi(xi) for xi in x[1:]]
cur, level = legs2, 0
while len(cur) > 1:
    cur = [np.einsum('a,b,abc->c', cur[2 * i], cur[2 * i + 1], T[level][i]) for i in range(len(cur) // 2)]
    level += 1
check('2 phi(x_1) in place of phi(x_1) multiplies the output by 2', np.allclose(cur[0], 2 * y_out), cur[0] / y_out)
check('N = 100 pixels, 2^N is about 1e30', round(np.log10(2.0 ** 100)) == 30, np.log10(2.0 ** 100))


def tree_count(n, D=10, dd=2, label=2, separate=False, halving=False):
    def bond(top):
        return label if (top and not separate) else D
    if halving:
        def rec(m, top):
            if m == 1:
                return 0, dd
            ta, la = rec(m // 2, False)
            tb, lb = rec(m - m // 2, False)
            out = bond(top)
            return ta + tb + la * lb * out, out
        total, top = rec(n, True)
    else:
        legs, total = [dd] * n, 0
        while len(legs) > 1:
            new = []
            for i in range(0, len(legs) - 1, 2):
                out = bond(len(legs) == 2)
                total += legs[i] * legs[i + 1] * out
                new.append(out)
            if len(legs) % 2:
                new.append(legs[-1])
            legs = new
        top = legs[0]
    return total + (top * label if separate else 0)


counts = [tree_count(100), tree_count(100, separate=True), tree_count(100, halving=True)]
check('a binary tree on 100 pixels with D = 10 has between 1e4 and 1e5 parameters, three shapes',
      counts == [50200, 51020, 41240] and all(1e4 < c < 1e5 for c in counts), counts)
# decided on 2026-11-22: the Fashion-MNIST numbers are those of the slides of the lecture, the stored source
# slides_prerecordings/lecture10.pdf, page 31, read with pdftotext; they are the numbers of Section VI of arXiv 1801.00315,
# a classifier of ten labels
import subprocess
slide = subprocess.run(['pdftotext', '-f', '31', '-l', '31', '-layout',
                        os.path.join(REPO, 'slides_prerecordings', 'lecture10.pdf'), '-'],
                       capture_output=True, text=True).stdout
page04 = open(os.path.join(REPO, 'webnotes', 'pages', 'session10', '04-tensor-networks-for-machine-learning-and-the-many-'
                           'body-wavefunction-as-a-big-data-problem.md')).read()
check('the page gives 95.38% and 88.97%, as page 31 of the slides of the lecture, training and test',
      '95.38% accuracy in training' in slide and '88.97% accuracy in testing' in slide
      and '95.38% accuracy on the training set and 88.97% on the test set' in page04, 'slides page 31')
# decided on 2026-11-22, the sentence after the key box: (7.5) of Section 7.4 is the open form, with vectors at the ends
page74 = open(os.path.join(REPO, 'webnotes', 'pages', 'session07', '04-the-matrix-product-state-ansatz.md')).read()
check('(7.5) is the open product M^s1 ... M^sL with vectors at the two ends, and (10.6) the trace',
      'M^{s_1}_{1}\\, M^{s_2}_{2}\\, \\cdots\\, M^{s_L}_{L}, \\tag{7.5}' in page74 and 'with vectors at the two ends' in page74
      and '\\mathrm{Tr}\\left[A^{s_1} A^{s_2}\\cdots A^{s_L}\\right], \\tag{10.6}' in page04, 'pages 7.4 and 10.4')
print('all checks of page 04 hold')
