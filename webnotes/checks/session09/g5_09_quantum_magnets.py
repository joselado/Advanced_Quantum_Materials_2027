"""Session 9, the numbers that page 09 (Section 9.9, screening in quantum magnets) states and that no figure script asserts.

The caption of spinon_impurity (the sign that changes on every site, n|m_n| between 0.0038 and 0.0045, the gap 0.8, the
partner of site 0 with 0.66 of the moment off site 0, the two straight lines) is asserted in
webnotes/figures/session09/spinon_impurity.py, and the facts of each picture of the picture quiz in g5_quiz_spinon_*.py, both
on the output of the pyqula script g5_spinon_chain_field.py. This script checks the steps fold, with the same open chain in
numpy, and a short pyqula chain against it, then the gaps and the order of the decay rates of the picture quiz, the first
quiz and the problem. The lab box quotes 8(1) and 0.1 K from its stored source, which labsource.py --check 9 shows.

The fold ends at the moment <S^z_n> induced by a field on one site, which is what the figure computes. Whether (9.11) is
written for this moment or for the correlation <S_0 . S_n> is the third point of "For the lecturer" in
webnotes/plans/session09.md, and nothing here depends on it.

Run it from anywhere:  python3 webnotes/checks/session09/g5_09_quantum_magnets.py"""
import os, sys, tempfile
sys.dont_write_bytecode = True
import numpy as np
from scipy.linalg import eigh_tridiagonal


def check(name, ok, value):
    print(('OK     ' if ok else 'FAILED ') + name + ': ' + str(value), flush=True)
    assert ok, name


def densities(N, chi2, v, sign=1.0):
    """Spinons per site of one species on an open chain of N sites with the hoppings sign*1 and sign*chi2 in turn, the
    strong one first, the onsite energy v on the central site, at half filling."""
    hop = sign * np.array([1.0 if i % 2 == 0 else chi2 for i in range(N - 1)])
    d = np.zeros(N); d[N // 2] = v
    e, w = eigh_tridiagonal(d, hop)
    assert np.sum(e < 0) == N // 2                        # no level at zero, so half filling is the lower half
    return (w[:, e < 0] ** 2).sum(axis=1)


N, c, h = 2000, 1000, 0.1

# ---- the fold: the field on S^z_0 = (n_up - n_dn)/2 is -h/2 for the up spinons and +h/2 for the down ones
nup, ndn = np.diag([1., 0., 1., 0.]), np.diag([0., 1., 1., 0.])      # the four states |up>, |dn>, |up dn>, |0>
Sz = (nup - ndn) / 2
check('fold: -h S^z_0 = -(h/2) n_up + (h/2) n_dn on the four states of one site', np.allclose(-h * Sz, -h / 2 * nup + h / 2 * ndn), True)
# half filling of the band 2 chi cos k: k_F = pi/2
k = 2 * np.pi * np.arange(4000) / 4000
check('fold: half filling of 2 chi cos k fills |k| > pi/2, so k_F = pi/2 and 2 k_F = pi', abs(np.mean(2 * np.cos(k) < 0) - 0.5) < 1e-3
      and np.all(np.cos(np.pi * np.arange(10)) == (-1.0) ** np.arange(10)), round(np.mean(2 * np.cos(k) < 0), 4))
# the two species change by opposite amounts, so <S^z_n> = delta n_up
n0 = densities(N, 1.0, 0.0)
dup, ddn = densities(N, 1.0, -h / 2) - n0, densities(N, 1.0, +h / 2) - n0
check('fold: delta n_dn = -delta n_up at half filling, on every site', np.abs(dup + ddn).max() < 1e-12, np.abs(dup + ddn).max())
m = (dup - ddn) / 2
check('fold: <S^z_n> = delta n_up', np.abs(m - dup).max() < 1e-12, np.abs(m - dup).max())
ns = np.arange(1, 32)
check('fold: the moment changes sign from site to site, n = 0 to 40', all(m[c + n] * m[c + n + 1] < 0 for n in range(40)), True)
nm = ns[1:] * np.abs(m[c + ns[1:]])
check('fold: its envelope falls as 1/n, n|m_n| between 0.0037 and 0.0045 for n = 2 to 31', 0.0037 < nm.min() and nm.max() < 0.0045,
      (round(nm.min(), 5), round(nm.max(), 5)))
m2 = (densities(N, 1.0, -h / 4) - densities(N, 1.0, h / 4)) / 2
ratio = m2[c + ns] / m[c + ns]
check('fold: the moment is linear in h, half the field gives half the moment to 0.2 percent, n = 1 to 31',
      np.abs(ratio - 0.5).max() < 1e-3, round(np.abs(ratio - 0.5).max(), 6))
mneg = (densities(N, 1.0, -h / 2, sign=-1) - densities(N, 1.0, h / 2, sign=-1)) / 2
check('fold: the sign of chi does not change the moment', np.abs(mneg - m).max() < 1e-12, np.abs(mneg - m).max())
md = (densities(N, 0.6, -h / 2) - densities(N, 0.6, h / 2)) / 2
n = np.arange(4, 17, 2)
rate = -np.polyfit(n, np.log(np.abs(md[c + n])), 1)[0]
check('fold: in the dimerized chain the moment decays exponentially, at about 0.6 per site', 0.5 < rate < 0.7, round(rate, 3))

# ---- the pyqula chain of the figure has the hopping +1, and it gives the same moment as the numpy chain with -1
cwd = os.getcwd()
with tempfile.TemporaryDirectory() as tmp:
    os.chdir(tmp)
    try:
        from pyqula import geometry, algebra
        Ns = 200
        mp = {}
        for chi2 in (1.0, 0.6):
            h0 = geometry.bichain().get_hamiltonian(has_spin=False)
            h0.inter = chi2 * h0.inter
            h0 = h0.set_finite_system(n=Ns // 2)
            dens = {}
            for s in (1, -1):
                hh = h0.copy()
                v = np.zeros(Ns); v[Ns // 2] = -s * h / 2
                hh.add_onsite(v)
                e, w = np.linalg.eigh(algebra.todense(hh.intra).real)
                dens[s] = np.sum(w[:, e < 0] ** 2, axis=1)
            mp[chi2] = (dens[1] - dens[-1]) / 2
    finally:
        os.chdir(cwd)
mn = {chi2: (densities(200, chi2, -h / 2, sign=-1) - densities(200, chi2, h / 2, sign=-1)) / 2 for chi2 in (1.0, 0.6)}
check('figure: the pyqula chain of 200 sites gives the numpy moments to 1e-14', max(np.abs(mp[x] - mn[x]).max() for x in mp) < 1e-14,
      max(np.abs(mp[x] - mn[x]).max() for x in mp))

# ---- the picture quiz: the gaps 2(1 - chi_2) and the order of the decay rates
kk = np.linspace(-np.pi, np.pi, 4001)
gaps = {chi2: 2 * np.min(np.abs(1 + chi2 * np.exp(1j * kk))) for chi2 in (0.6, 0.8, 0.9)}
check('picture quiz: the gaps are 0.8, 0.4 and 0.2, and 0.4 is twice the smallest',
      all(abs(gaps[x] - 2 * (1 - x)) < 1e-9 for x in gaps) and abs(gaps[0.8] - 2 * gaps[0.9]) < 1e-9, {x: round(g, 4) for x, g in gaps.items()})
rates = {}
for chi2 in (0.6, 0.8, 0.9):
    mm = (densities(N, chi2, -h / 2) - densities(N, chi2, h / 2)) / 2
    n = np.arange(10, 21, 2)
    rates[chi2] = -np.polyfit(n, np.log(np.abs(mm[c + n])), 1)[0]
check('picture quiz: the smaller the gap, the slower the decay, rates per site from n = 10 to 20 on the even sites',
      rates[0.6] > rates[0.8] > rates[0.9] > 0, {x: round(r, 3) for x, r in rates.items()})
# the closing line of the picture quiz: the exponential tends to a straight line far from the impurity. For chi_2 = 0.9 the
# rate per site on the even sites falls over n = 10 to 40 and tends to ln(1/0.9) = 0.105 far away (n = 100 to 200, before the
# round-off floor), so the line of the correct picture still bends a little, by less than 0.1 of a decade from its fit
m9 = (densities(N, 0.9, -h / 2) - densities(N, 0.9, h / 2)) / 2
a9 = np.abs(m9[c:c + 201])
loc = [np.log(a9[lo] / a9[hi]) / (hi - lo) for lo, hi in ((10, 20), (20, 30), (30, 40), (100, 200))]
n9 = np.arange(10, 41, 2)
bend = np.abs(np.polyval(np.polyfit(n9, np.log10(a9[n9]), 1), n9) - np.log10(a9[n9])).max()
check('picture quiz: for chi_2 = 0.9 the rate falls 0.19, 0.16, 0.14 over n = 10 to 40 and is within 10 percent of ln(1/0.9) at n = 100 to 200',
      loc[0] > loc[1] > loc[2] > loc[3] and abs(loc[3] / np.log(1 / 0.9) - 1) < 0.1 and bend < 0.1,
      ([round(x, 4) for x in loc], round(np.log(1 / 0.9), 4), round(bend, 3)))

# ---- the first quiz
check('quiz 1: 1/n falls by 2 from n = 10 to 20, e^{-n/2.5} by e^{-4} = 0.018, about 0.02',
      abs(10 / 20 - 0.5) < 1e-15 and abs(np.exp(-20 / 2.5) / np.exp(-10 / 2.5) - np.exp(-4)) < 1e-15 and abs(round(np.exp(-4), 2) - 0.02) < 1e-12,
      round(np.exp(-4), 4))

# ---- the problem
r_exp, r_pow = np.exp(-24 / 8) / np.exp(-8 / 8), 8 / 24
check('problem: e^{-2} = 0.14 against 1/3 = 0.33, a factor of about 2.5',
      abs(round(r_exp, 2) - 0.14) < 1e-12 and abs(round(r_pow, 2) - 0.33) < 1e-12 and abs(round(r_pow / r_exp, 1) - 2.5) < 1e-12,
      (round(r_exp, 4), round(r_pow, 4), round(r_pow / r_exp, 3)))
# the solution: two points fix the two constants of either law, so a power law A/n^p goes through the two points of the
# exponential, and the exponential A e^{-n/xi} through the two points of 1/n
p = np.log(r_exp) / np.log(8 / 24)
xi_fit = 16 / np.log(1 / r_pow)
check('problem: a power law n^-p with p = 1.82 and an exponential with xi = 14.6 go through the same two points',
      abs((24 / 8) ** (-p) - r_exp) < 1e-12 and abs(np.exp(-16 / xi_fit) - r_pow) < 1e-12, (round(p, 3), round(xi_fit, 3)))

# ---- Figure 9.5, a converted figure: its caption says "drawn for xi = 2.5", the XI of its Blender script
import re
ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', '..'))
blend = open(os.path.join(ROOT, 'lecture_notes', 'src', 'figures', 'blender', 's09f05_decay.py')).read()
mx = re.search(r'^N, STEP, XI = (\S+), (\S+), (\S+)$', blend, re.M)
check('Figure 9.5: the exponential is drawn for xi = 2.5, as its caption says', mx is not None and float(mx.group(3)) == 2.5,
      mx.group(0) if mx else None)

# ---- the try-it box. The cell "Impurity in an electronic insulator" has gaps = [0.1,0.3] and add_sublattice_imbalance(gap),
# so 0.1 and 0.3 are the onsite energies +-m, and the gaps are 2m = 0.2 and 0.6, as its plot titles print. The LDOS change
# at E = 0 decays as e^{-x/xi}, with 1/xi = 2 asinh(m/2t), the lengths 10.0 and 3.35 sites of the conventions sheet, which
# the box gives as about 10 and 3.3 sites. Route 1 is a fit of G(E = 0)^2 of an open chain of 400 sites, route 2 the
# closed form. The cell itself, run with pyqula, gives 9.96 and 3.34 in webnotes/checks/session09/g4_06b_friedel_chain.py.
import json
cells = json.load(open(os.path.join(ROOT, 'jupyter-notebooks', 'session9.ipynb')))['cells']
hd = [i for i, cl in enumerate(cells) if cl['cell_type'] == 'markdown' and ''.join(cl['source']).startswith('## Impurity in an electronic insulator')]
src = ''.join(cells[hd[0] + 1]['source'])
check('try-it: the cell has gaps = [0.1,0.3] given to add_sublattice_imbalance, and titles "Gap = " 2*gap',
      len(hd) == 1 and 'gaps = [0.1,0.3]' in src and 'h.add_sublattice_imbalance(gap)' in src and '"Gap = "+str(2*gap)' in src, hd)
kap = {}
for mm in (0.1, 0.3):
    Nb = 400
    Hb = np.diag([mm if i % 2 == 0 else -mm for i in range(Nb)]) + np.diag(np.ones(Nb - 1), 1) + np.diag(np.ones(Nb - 1), -1)
    G = np.linalg.inv(-Hb)                                         # G(E = 0) of the gapped open chain
    j = np.arange(20, 61, 2)
    kap[mm] = -2 * np.polyfit(j, np.log(np.abs(G[Nb // 2, Nb // 2 + j])), 1)[0]   # LDOS change ~ G^2
check('try-it: the gaps are 0.2 and 0.6, and the decay lengths of the LDOS change are about 10 and 3.3 sites',
      all(abs(kap[mm] - 2 * np.arcsinh(mm / 2)) < 1e-3 for mm in kap) and abs(round(1 / kap[0.1], 1) - 10.0) < 1e-12
      and abs(round(1 / kap[0.3], 2) - 3.35) < 1e-12 and round(1 / kap[0.1]) == 10 and round(1 / kap[0.3], 1) == 3.3,
      {mm: (2 * mm, round(1 / kap[mm], 3)) for mm in kap})
# ---- the notebook box: the cell "The impact of a strong impurity" puts one impurity of growing strength into three gapped
# chains built on bichain, an s-wave superconductor, an insulator with a sublattice imbalance and a p-wave superconductor,
# and plots the density of states with an embedding. Read from its code. The equal hoppings of bichain are checked with
# pyqula in webnotes/checks/session09/g3_05b_stoner_instability.py.
hs_ = [i for i, cl in enumerate(cells) if cl['cell_type'] == 'markdown' and ''.join(cl['source']).startswith('## The impact of a strong impurity')]
src6 = ''.join(cells[hs_[0] + 1]['source'])
check('notebook box: the cell sweeps one impurity over three bichain systems, s-wave, sublattice imbalance and p-wave, and plots the DOS',
      len(hs_) == 1 and 'geometry.bichain()' in src6 and 'mode="swave"' in src6 and 'add_sublattice_imbalance' in src6
      and 'mode="pwave"' in src6 and 'potentials.impurity' in src6 and 'multidos' in src6 and 'np.linspace(0.,15.,60)' in src6, hs_)
# the density of states that the cell plots is summed over four sites, the impurity site and the next three sites of the
# chain: the cell embeds H.get_supercell(2) of bichain, puts the impurity on H.geometry.r[0], and Embedding.multidos sums
# the LDOS of get_ldos over the sites of the embedded cell. Run on the insulator of the cell with the impurity 5.
check('notebook box: the cell embeds get_supercell(2) and puts the impurity on r[0], with multidos and no nsuper',
      'H = H.get_supercell(2)' in src6 and 'potentials.impurity(H.geometry.r[0],v=w)' in src6 and 'nsuper' not in src6,
      'read from the cell')
cwd = os.getcwd()
with tempfile.TemporaryDirectory() as d:
    os.chdir(d)
    try:
        from pyqula import geometry, potentials, embedding
        hi_ = geometry.bichain().get_hamiltonian(); hi_.add_sublattice_imbalance(-0.6)
        Hs = hi_.get_supercell(2)
        fimp = potentials.impurity(Hs.geometry.r[0], v=5.0)
        Hm = Hs.copy(); Hm.add_onsite(fimp)
        eb_ = embedding.Embedding(Hs, m=Hm)
        es_, ds_ = eb_.multidos(es=[0.3], delta=4e-2, operator="electron")
        xl, yl, dl = eb_.get_ldos(energy=0.3, delta=4e-2, operator="electron")
        onsite_ = [fimp(r) for r in Hs.geometry.r]
    finally:
        os.chdir(cwd)
check('notebook box: the plotted DOS is the LDOS summed over the four sites of the cell, the impurity site at its end and the '
      'next three sites', len(xl) == 4 and np.allclose(np.sort(xl), [-1.5, -0.5, 0.5, 1.5])
      and abs(Hs.geometry.r[0][0] - min(xl)) < 1e-12 and abs(ds_[0] - np.sum(dl)) < 1e-8 * abs(ds_[0])
      and onsite_[0] != 0 and all(o == 0 for o in onsite_[1:]),
      (np.round(xl, 2).tolist(), round(float(ds_[0]), 6), round(float(np.sum(dl)), 6), onsite_))

# ---- the solution of the problem: the exponential of the problem, (-1)^n e^{-n/8}, is a straight line of slope -1/8 on a
# logarithmic axis at every n, and 1/n is not
nn_ = np.arange(1, 60)
fit_e = np.polyfit(nn_, np.log(np.exp(-nn_ / 8)), 1)
fit_p = np.polyfit(nn_, np.log(1 / nn_), 1)
check('problem: ln|m_n| of the problem is a straight line of slope -1/xi = -0.125, and ln(1/n) bends away from any line',
      abs(fit_e[0] + 0.125) < 1e-12 and np.abs(np.polyval(fit_e, nn_) + nn_ / 8).max() < 1e-12
      and np.abs(np.polyval(fit_p, nn_) - np.log(1 / nn_)).max() > 0.5, (fit_e[0], np.abs(np.polyval(fit_p, nn_) - np.log(1 / nn_)).max()))
print('all checks of page 09 hold')
