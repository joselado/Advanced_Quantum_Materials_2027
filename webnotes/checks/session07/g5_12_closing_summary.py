"""Session 7, the numbers that page 12 (Section 7.12, closing summary) states in its two quizzes.

The page has no figure of its own besides Figure 7.3, a converted figure with no numbers in its caption. This script checks
the quiz on the counting of an MPS and the quiz on the 20 by 20 lattice, with numpy, and the count of an open MPS against
the 2LM^2 of the first quiz, as the conventions sheet of the session gives it (18888 and 19640 for L=100 and M=10). Added on
2026-11-22: the vectors at the two ends, and a gapped chain of free fermions of 200 and 2000 sites for the old feedback that
both need the same M=20.

Run it from anywhere:  python3 webnotes/checks/session07/g5_12_closing_summary.py"""
import numpy as np


def check(name, ok, value):
    print(('OK     ' if ok else 'FAILED ') + name + ': ' + str(value), flush=True)
    assert ok, name


# ---- quiz on the counting: 2 L M^2 against 2^L and M^L
L, M = 100, 10
check('quiz 1: 2 L M^2 = 2e4 for L=100, M=10', 2 * L * M**2 == 20000, 2 * L * M**2)
check('quiz 1: 2^100 is 1.3e30', abs(2.0**100 / 1.3e30 - 1) < 0.03, f'{2.0**100:.3e}')
D = [min(M, 2**i, 2**(L - i)) for i in range(L + 1)]
n_open = sum(2 * D[i - 1] * D[i] for i in range(1, L + 1))
check('quiz 1: the smaller end matrices make the count a bit lower, 18888 < 20000', n_open == 18888 and n_open < 20000, n_open)
D1 = [1] + [M] * (L - 1) + [1]
n_full = sum(2 * D1[i - 1] * D1[i] for i in range(1, L + 1))
check('quiz 1: with every inner bond M the count is 19640, still below 2 L M^2', n_full == 19640, n_full)
# M=1, a product state: two numbers on every site, 2L in all, while M^L = 1
for L1 in (10, 40, 100):
    D = [1] * (L1 + 1)
    n = sum(2 * D[i - 1] * D[i] for i in range(1, L1 + 1))
    check(f'quiz 1: M=1 stores 2L = {2 * L1} numbers on {L1} sites while M^L = 1', n == 2 * L1 and 1**L1 == 1, n)
# a random MPS with M=2 on 6 sites holds 2^6 coefficients built from those numbers, as a check of the form of the ansatz
rng = np.random.default_rng(1)
Ls, Mb = 6, 2
D = [min(Mb, 2**i, 2**(Ls - i)) for i in range(Ls + 1)]
A = [rng.normal(size=(2, D[i], D[i + 1])) for i in range(Ls)]
psi = A[0]
for i in range(1, Ls):
    psi = np.einsum('...a,sab->...sb', psi, A[i])
check('quiz 1: the products of the matrices give all 2^L coefficients', psi.size == 2**Ls, psi.shape)
check('quiz 1: at the two ends the matrices are vectors', A[0].shape[1] == 1 and A[-1].shape[2] == 1, (A[0].shape, A[-1].shape))

# ---- quiz on the 20 by 20 lattice
check('quiz 2: 20^20 is about 1e26', abs(np.log10(20.0**20) - 26) < 0.05, f'{20.0**20:.3e}')
check('quiz 2: a 20 by 20 lattice has 400 sites', 20 * 20 == 400, 400)
nx = ny = 20
cut = sum(1 for y in range(ny) for x in range(nx - 1) if x == nx // 2 - 1)
check('quiz 2: a straight cut through the middle of an open 20 by 20 lattice crosses 20 bonds', cut == 20, cut)
check('quiz 2: 20 times the entropy needs M^20, 20^20 for M=20', np.isclose(20 * np.log(20), np.log(20.0**20)), round(20 * np.log(20), 3))


# ---- quiz 2, old feedback of option 3: a gapped chain of 2000 sites needs the same M=20 as the one of 200. The gapped model
# is the dimerized chain of free fermions at half filling, hoppings 1 on the bonds (2n, 2n+1) and 0.6 on the others, open,
# with the cut in the middle. The Schmidt weights are the products over the modes nu of nu or 1-nu.
def schmidt_drop(nu, M):
    """Weight dropped when only the M largest many-body Schmidt weights are kept, by a best-first walk over the products."""
    import heapq
    p = np.maximum(nu, 1 - nu)
    r = np.sort((1 - p) / p)[::-1]
    heap, tot = [(-np.prod(p), -1)], 0.0
    for _ in range(M):
        w, last = heapq.heappop(heap)
        tot -= w
        if last + 1 < len(r):
            heapq.heappush(heap, (w * r[last + 1], last + 1))
            if last >= 0:
                heapq.heappush(heap, (w / r[last] * r[last + 1], last + 1))
    return 1 - tot


res = {}
for Lg in (200, 2000):
    H = np.zeros((Lg, Lg))
    for i in range(Lg - 1):
        H[i, i + 1] = H[i + 1, i] = -(1.0 if i % 2 == 0 else 0.6)
    w, v = np.linalg.eigh(H)
    Cg = v[:, :Lg // 2] @ v[:, :Lg // 2].T
    nu = np.linalg.eigvalsh(Cg[:Lg // 2, :Lg // 2])
    nu = nu[(nu > 1e-15) & (nu < 1 - 1e-15)]
    res[Lg] = (-np.sum(nu * np.log(nu) + (1 - nu) * np.log(1 - nu)), schmidt_drop(nu, 4), schmidt_drop(nu, 20))
print('gapped chain, half cut: S, dropped weight at M=4 and M=20', res)
check('quiz 2, option 3: the gapped chain of 2000 sites has the entropy of the one of 200 at the middle cut', abs(res[200][0] - res[2000][0]) < 1e-8, round(res[2000][0], 6))
check('quiz 2, option 3: and the same dropped weight with M=4', abs(res[200][1] / res[2000][1] - 1) < 1e-6, f'{res[2000][1]:.4e}')
check('quiz 2, option 3: M=20 drops less than 1e-9 for both, so the same M=20 is enough', res[200][2] < 1e-9 and res[2000][2] < 1e-9, (f'{res[200][2]:.2e}', f'{res[2000][2]:.2e}'))
