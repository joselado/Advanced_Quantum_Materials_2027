"""Session 6, the statements of page 04 (Sections 6.4 and 6.5), in the order of the page.

The captions of fm_afm_chain and mf_chain (a), the picture quiz on the bands and the quiz with the dispersions as
options are asserted by _g2_chain.check_meanfield on the variables of the pyqula script g2_chain_meanfield.py, and the
quiz on the 1/U law with its figure ufactor by _g2_chain.check_energy on g2_chain_energy_difference.py. This script
runs both with style.run_script, and it adds the key box, the steps fold, the paramagnet of the picture quiz, the
problem on the saturated ferromagnet, the meshes of the caption of the ferromagnet and the cell of the try-it box.
pyqula runs in temporary folders, so the script writes no file. The lab box quotes 7 nm and 0.3 eV, which
labsource.py checks."""
import os, sys, json, tempfile
import numpy as np

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', '..')
sys.path.insert(0, os.path.join(ROOT, 'webnotes', 'figures', 'session06'))
import _g2_chain, _mf
from _g2_chain import style, say, energy_afm
from pyqula import geometry

TMP = tempfile.TemporaryDirectory()                # pyqula may write files, so it works in a folder of its own,
os.chdir(TMP.name)                                 # which is removed at the exit

# the lab box: 7 nm and 0.3 eV are checked by labsource.py, and the 0.2 eV of "about 0.2 to 0.3 eV" is in the same
# sentence of the stored arXiv abstract, as "0.2 - 0.3 eV"
src = open(os.path.join(ROOT, 'webnotes', 'sources', 'session06', 'magda2014_nature13831.txt')).read()
say('lab: the stored abstract states "narrower than 7 nm reveal a bandgap of about 0.2 - 0.3 eV"',
    'narrower than 7 nm reveal a bandgap of about 0.2 - 0.3 eV' in src, 'found')

# the figures and the band quizzes, on the variables of the download script
d = style.run_script('session06/g2_chain_meanfield.py')
_g2_chain.check_meanfield(d)

# the caption of the ferromagnet: n=0.2 is filling=0.1, and m = 0.200 with the splitting 0.800 also on nk=1000, while
# the odd mesh nk=301 gives 0.1993, a k-point less, which still rounds to 0.20
ms = {}
for nk in (301, 1000):
    h1 = geometry.chain().get_hamiltonian(tij=[-1.])
    seed = h1.copy(); seed.clean(); seed.add_zeeman([0., 0., -0.1])
    hf = h1.get_mean_field_hamiltonian(U=4., filling=0.1, mf=seed, mix=0.9, nk=nk)
    on = np.real(np.diag(hf.intra))
    ms[nk] = (float(np.real(hf.get_vev('mz', nk=nk)[0])), on[1] - on[0])
say('caption: the ferromagnet at filling=0.1 has m = 0.200 and Um = 0.800 on nk=1000, and m = 0.1993 on nk=301',
    abs(ms[1000][0] - 0.2) < 1e-6 and abs(ms[1000][1] - 0.8) < 1e-6 and round(ms[301][0], 4) == 0.1993
    and round(ms[301][0], 2) == 0.20, ms)

# the picture quiz: at U = 0 and half filling every site holds 1/2 electron of each spin, so the Hartree field of the
# paramagnet, U <n_other spin> = U/2, is the same constant everywhere. Its bands are those of U = 0 moved by U/2, the
# same when they are measured from the Fermi level. A loop from a guess with no field does not stay there at U=4t, it
# drifts to the antiferromagnet, since the paramagnet of the half-filled chain is unstable.
h2 = geometry.bichain().get_hamiltonian(tij=[-1.])
nup, ndn = np.real(h2.get_vev('up', nk=200)), np.real(h2.get_vev('dn', nk=200))
hp = h2.copy(); hp.add_onsite(4. / 2)
hk = hp.get_hk_gen()
bp = np.array([np.linalg.eigvalsh(hk([k / np.pi, 0., 0.])) for k in d['ks']])
say('quiz: at U=0 each site has 1/2 electron of each spin, so the paramagnet at U=4t has the bands of U=0 moved by U/2',
    np.allclose(nup, 0.5, atol=1e-6) and np.allclose(ndn, 0.5, atol=1e-6)
    and np.allclose(bp - 2.0, d['bands_pm'], atol=1e-9), (np.round(nup, 6), np.round(ndn, 6)))

# the key box and the steps fold: the lower band has the weight (1 + Delta/E)/2 on the favored sublattice, the gap
# equation has a solution for every U > 0, and at large U the expansions m = 1 - 4t^2/U^2, a kinetic energy -4t^2/U and an
# interaction energy 2t^2/U per site, with <eps_k^2> = 2t^2 over |k| < pi/2
ok = True
for k, D in ((0.3, 0.7), (1.2, 1.5), (1.5, 0.2)):
    f = -2 * np.cos(k)
    w, v = np.linalg.eigh(np.array([[-D, f], [f, D]]))
    E = np.sqrt(f * f + D * D)
    ok = ok and abs(w[0] + E) < 1e-12 and abs(v[0, 0] ** 2 - 0.5 * (1 + D / E)) < 1e-12
say('fold: the lower band of [[-Delta, eps],[eps, Delta]] is -E_k with the weight (1 + Delta/E_k)/2 on the first site', ok, 'ok')
say('fold: the average of eps_k^2 over |k| < pi/2 is 2t^2', abs(_mf.avg(lambda e, D: e * e, 0.0) - 2.0) < 1e-10,
    _mf.avg(lambda e, D: e * e, 0.0))
mm = [_mf.moment(U) for U in (0.5, 1.0, 2.0)]
say('key box: the gap equation has a solution with m > 0 at U = 0.5t, t and 2t, so a gap Um for every U > 0',
    all(m > 0 for m in mm) and round(mm[1], 4) == 0.0299, np.round(mm, 5))
ok, rows = True, []
for U in (20.0, 40.0):
    e, kin, inter, m = energy_afm(U)
    rows.append((U, round(m, 6), round(kin, 5), round(inter, 5), round(e, 6)))
    ok = ok and abs(m - (1 - 4 / U ** 2)) < 1e-4 and abs(kin + 4 / U) / (4 / U) < 0.01 \
        and abs(inter - 2 / U) / (2 / U) < 0.01 and abs(e + 2 / U) / (2 / U) < 0.01
say('fold: at 20t and 40t, m, the kinetic energy, the interaction energy and E_AFM are within 1% of the expansions', ok, rows)
say('fold: at U=20t the expansion -2t^2/U is -0.1 per site, and the gap equation gives E_AFM = -0.09975 per site',
    abs(-2 / 20.0 + 0.1) < 1e-12 and round(energy_afm(20.0)[0], 5) == -0.09975, (-2 / 20.0, energy_afm(20.0)[0]))
eu = [(U, round(energy_afm(U)[0], 5), round(-4 / np.pi + U / 4, 5)) for U in (1.0, 2.0, 3.0, 3.9, 4.5, 6.0, 10.0, 20.0)]
say('opener: at half filling the antiferromagnet is below the uniform solution, the paramagnet -4t/pi + U/4 per site '
    'at every U and the saturated ferromagnet, zero, where it exists from 4t on',
    all(e < p and (U < 4 or e < 0) for U, e, p in eu), eu)
say('key box: 2t^2/U per site is 4t^2/U per cell of two sites, the saturated ferromagnet has zero energy',
    abs(2 * (0.0 - energy_afm(40.0)[0]) * 40.0 - 4.0) < 0.01, 2 * (0.0 - energy_afm(40.0)[0]) * 40.0)

# corrected on 2026-11-22, Section 6.5: the lowest uniform state is the paramagnet below 16t/pi = 5.1t and the saturated
# ferromagnet above it. Two routes: the closed forms -4t/pi + U/4 and 0 per site, and a sum over a mesh of the filled bands
# -2t cos k of each spin plus U <n_up><n_dn>, scanned over the uniform moment m from 0 to 1. The saturated state is a
# solution from 4t on (the problem), and its gap U - 4t is the reason why the text compares with "the uniform one" and
# no longer calls it gapless.
from scipy.optimize import brentq
eps_k = np.sort(-2 * np.cos((np.arange(100000) + 0.5) / 100000 * 2 * np.pi - np.pi))


def e_uniform(m, U):
    """Energy per site of the uniform state with the moment m at half filling, on the mesh."""
    nu, nd = (1 + m) / 2, (1 - m) / 2
    Nk = len(eps_k)
    return eps_k[:int(round(nu * Nk))].sum() / Nk + eps_k[:int(round(nd * Nk))].sum() / Nk + U * nu * nd


U_x = brentq(lambda U: -4 / np.pi + U / 4, 1, 10)
U_x2 = brentq(lambda U: e_uniform(1.0, U) - e_uniform(0.0, U), 1, 10)
mgrid = np.linspace(0, 1, 201)
lowest = {U: mgrid[np.argmin([e_uniform(m, U) for m in mgrid])] for U in (4.0, 4.5, 5.0, 5.2, 6.0)}
say('6.5: the lowest uniform state is the paramagnet below 16t/pi = 5.1t and the saturated ferromagnet above, by the closed '
    'form and by the mesh', abs(U_x - 16 / np.pi) < 1e-9 and abs(U_x2 - 16 / np.pi) < 1e-3 and round(U_x, 1) == 5.1
    and all(lowest[U] == (0.0 if U < 16 / np.pi else 1.0) for U in lowest), (round(U_x, 4), round(U_x2, 4), lowest))

# the quiz on the 1/U law and its figure
d2 = style.run_script('session06/g2_chain_energy_difference.py')
_g2_chain.check_energy(d2)

# the problem: the saturated ferromagnet needs -2t + U > 2t. A loop started from its field, with spin up below spin down
# as on the page, keeps |m| = 1 with spin up at 4.1t for every mix. At 3.9t it leaves the saturated state, and where it
# ends depends on mix and on maxerror: with mix=0.9 and the default maxerror it stops close to the paramagnet with a moment
# of one or two k-points, 1/40 on nk=40 and 2/41 on nk=41, and with mix 0.5 or 0.3, or with mix=0.9 and maxerror=1e-9, it
# reaches the antiferromagnet of the gap equation, lower in energy. That
# antiferromagnet may point away from z, so |m| is read from the three components. The gap of the saturated state is
# U - 4t. mix is the weight of the new mean field in each step, which mix_mf of pyqula states.
from pyqula.scftk.densitydensity import mix_mf
old, new = {(0, 0, 0): np.array([[1.0]])}, {(0, 0, 0): np.array([[3.0]])}
say('problem: mix is the weight of the new mean field, mix_mf(new, old, 0.9) = 0.1 old + 0.9 new',
    abs(mix_mf(new, old, mix=0.9)[(0, 0, 0)][0, 0] - (0.1 * 1.0 + 0.9 * 3.0)) < 1e-12, mix_mf(new, old, mix=0.9)[(0, 0, 0)])


def moment3(hf, nk):
    """|m| of each site from the three components mx, my and mz."""
    v = [np.real(hf.get_vev(c, nk=nk)) for c in ('mx', 'my', 'mz')]
    return np.sqrt(v[0] ** 2 + v[1] ** 2 + v[2] ** 2)


res = {}
for U, mixes in ((3.9, (0.9, 0.5, 0.3)), (4.1, (0.9, 0.5, 0.3)), (6.0, (0.9,))):
    for nk in (40, 41):
        for mix in mixes:
            h = geometry.bichain().get_hamiltonian(tij=[-1.])
            seed = h.copy(); seed.clean(); seed.add_zeeman([0., 0., -U / 2])
            hf, e = h.get_mean_field_hamiltonian(U=U, mf=seed, mix=mix, nk=nk, return_total_energy=True)
            res[(U, nk, mix)] = (moment3(hf, nk), np.real(hf.get_vev('mz', nk=nk)), e, hf.get_gap())
# corrected on 2026-11-22: the end also depends on maxerror, the change of the mean field below which the loop stops. With
# mix=0.9 and maxerror=1e-9 the same loop at 3.9t reaches the antiferromagnet on nk 40 and 41, so the end of the default
# maxerror is an early stop
for nk in (40, 41):
    h = geometry.bichain().get_hamiltonian(tij=[-1.])
    seed = h.copy(); seed.clean(); seed.add_zeeman([0., 0., -3.9 / 2])
    hf, e = h.get_mean_field_hamiltonian(U=3.9, mf=seed, mix=0.9, nk=nk, maxerror=1e-9, return_total_energy=True)
    res[(3.9, nk, 'tight')] = (moment3(hf, nk), np.real(hf.get_vev('mz', nk=nk)), e, hf.get_gap())
import inspect
from pyqula.scftk import spinspin
from pyqula.scftk.densitydensity import generic_densitydensity
dflt = inspect.signature(spinspin.VJinteraction).parameters['maxerror'].default
src_loop = inspect.getsource(generic_densitydensity)
say('problem: the default maxerror is 1e-5, and the loop stops when the change of the mean field is below it',
    dflt == 1e-5 and 'if diff<maxerror:' in src_loop and 'diff = diff_mf(mfnew,mf)' in src_loop, dflt)
say('problem: the bands -2t cos k and -2t cos k + U do not overlap only for U > 4t', (-2 + 4.1 > 2) and not (-2 + 3.9 > 2), 'ok')
say('problem: add_zeeman([0, 0, -U/2]) is the field of spin up, and at 4.1t the loop keeps m = 1 with spin up and zero '
    'energy on nk 40 and 41, with mix 0.9, 0.5 and 0.3',
    all(np.allclose(res[(4.1, nk, mix)][0], 1, atol=1e-6) and np.allclose(res[(4.1, nk, mix)][1], 1, atol=1e-6)
        and abs(res[(4.1, nk, mix)][2]) < 1e-8 for nk in (40, 41) for mix in (0.9, 0.5, 0.3)),
    {(nk, mix): np.round(res[(4.1, nk, mix)][1], 6) for nk in (40, 41) for mix in (0.9, 0.5, 0.3)})
m40, m41 = res[(3.9, 40, 0.9)][0], res[(3.9, 41, 0.9)][0]
e_pm = 2 * (-4 / np.pi + 3.9 / 4)                  # the paramagnet per cell of two sites, -0.5965
say('problem: at 3.9t with mix=0.9 the loop stops close to the paramagnet, |m| = 0.025 = 1/40 on nk=40 and 0.049 = 2/41 '
    'on nk=41, one or two k-points',
    np.allclose(m40, m40[0]) and np.allclose(m41, m41[0]) and round(m40[0], 3) == 0.025 and round(m41[0], 3) == 0.049
    and abs(m40[0] * 40 - 1) < 1e-3 and abs(m41[0] * 41 - 2) < 1e-3
    and all(abs(res[(3.9, nk, 0.9)][2] - e_pm) < 5e-3 for nk in (40, 41)),
    (round(m40[0], 5), round(m41[0], 5), round(res[(3.9, 40, 0.9)][2], 5), round(res[(3.9, 41, 0.9)][2], 5), round(e_pm, 5)))
e_af = 2 * energy_afm(3.9)[0]                      # the antiferromagnet of the gap equation per cell, -0.959
say('problem: at 3.9t with mix 0.5 or 0.3 the loop reaches the antiferromagnet of the gap equation, lower in energy than '
    'the end of mix=0.9, on nk 40 and 41',
    all(np.allclose(res[(3.9, nk, mix)][0], _mf.moment(3.9), atol=1e-3) and abs(res[(3.9, nk, mix)][2] - e_af) < 1e-3
        and res[(3.9, nk, mix)][2] < res[(3.9, nk, 0.9)][2] - 0.3 for nk in (40, 41) for mix in (0.5, 0.3)),
    {(nk, mix): (np.round(res[(3.9, nk, mix)][0], 4), round(res[(3.9, nk, mix)][2], 5)) for nk in (40, 41) for mix in (0.5, 0.3)})
say('problem: at 3.9t with mix=0.9 and maxerror=1e-9 the loop reaches the antiferromagnet on nk 40 and 41, so the end of '
    'the default maxerror is an early stop',
    all(np.allclose(res[(3.9, nk, 'tight')][0], _mf.moment(3.9), atol=1e-3) and abs(res[(3.9, nk, 'tight')][2] - e_af) < 1e-3
        for nk in (40, 41)),
    {nk: (np.round(res[(3.9, nk, 'tight')][0], 5), round(res[(3.9, nk, 'tight')][2], 5)) for nk in (40, 41)})
say('problem: in these runs the moment of the antiferromagnet ends in the plane xy, m_z below 1e-4 with |m| = 0.758',
    all(np.all(np.abs(res[(3.9, nk, k)][1]) < 1e-4) and round(res[(3.9, nk, k)][0][0], 3) == 0.758
        for nk in (40, 41) for k in (0.5, 0.3, 'tight')),
    {(nk, k): np.round(res[(3.9, nk, k)][1], 6) for nk in (40, 41) for k in (0.5, 0.3, 'tight')})
# Section 6.5: the saturated ferromagnet of the half-filled chain has the gap U - 4t, 0.1 at 4.1t and 2 at 6t, so above
# 16t/pi the lowest uniform state has a gap too, and the text compares with "the uniform one" (corrected on 2026-11-22)
say('6.5: the saturated ferromagnet at half filling has the gap U - 4t', all(abs(res[(U, nk, 0.9)][3] - (U - 4)) < 1e-6
    for U in (4.1, 6.0) for nk in (40, 41)), {k: round(v[3], 4) for k, v in res.items() if k[0] > 4 and k[2] == 0.9})
# corrected after the independent check of 2026-11-22 (k4): the reason of the text. Below 16t/pi the lowest uniform state is
# the paramagnet, with no gap, and above it the saturated ferromagnet, with the gap U - 4t, and there the antiferromagnet is
# lower by about 2t^2/U per site (mf_chain.py asserts the ratio above 0.96 above the kink). This is the second-order energy
# of the virtual hops: on a bond of the classical Neel state |up, dn> each spin can hop to the other site and back through
# the doubly occupied state at U, -t^2/U each, so -2t^2/U per bond, one bond per site on the chain, while on |up, up> the
# hop is blocked by the Pauli principle and gives zero. Checked on the two-site Hubbard model with the six states.
c2 = []
for i_ in range(4):                                                  # Jordan-Wigner, modes 0 up, 0 dn, 1 up, 1 dn
    op_ = np.array([[1.0]])
    for j_ in range(4):
        op_ = np.kron(op_, np.array([[0, 1.], [0, 0]]) if j_ == i_ else (np.diag([1., -1.]) if j_ < i_ else np.eye(2)))
    c2.append(op_)
n2 = [x.T @ x for x in c2]
Ht2 = -sum(c2[s].T @ c2[2 + s] + c2[2 + s].T @ c2[s] for s in (0, 1))
Hu2 = sum(n2[2 * i_] @ n2[2 * i_ + 1] for i_ in (0, 1))
vac = np.zeros(16); vac[0] = 1.0
neel = c2[0].T @ c2[3].T @ vac
ferro = c2[0].T @ c2[2].T @ vac
second = {}
for name, st in (('neel', neel), ('ferro', ferro)):
    v1 = Ht2 @ st
    second[name] = -(v1 @ v1) / 1.0                                  # the intermediate states have the energy U = 1 above
    second[name + '_U'] = float(v1 @ Hu2 @ v1) if v1 @ v1 > 0 else 0.0
say('6.5: the virtual hops give -2t^2/U per bond on the classical Neel bond and zero on the parallel one, blocked by Pauli, '
    'and above 16t/pi the antiferromagnet is the lower one', abs(second['neel'] + 2) < 1e-12 and abs(second['ferro']) < 1e-12
    and abs(second['neel_U'] - 2) < 1e-12 and 16 / np.pi < 6.0 and all(abs(res[(6.0, nk, 0.9)][3] - 2.0) < 1e-6 for nk in (40, 41)),
    (second['neel'], second['ferro']))

# corrected on 2026-11-22, the text of Section 6.4 and its notebook box: the ferromagnet of one site per cell has n = 0.2,
# which is filling=0.1 (asserted with the caption above), and it is in the cell "Intermediate coupling regime and Stoner
# instability", while the cell "Magnetic order driven by interactions in a chain" is the bichain at half filling
nb4 = json.load(open(os.path.join(ROOT, 'jupyter-notebooks', 'session6.ipynb')))['cells']


def cell_code(title):
    i = [j for j, c in enumerate(nb4) if c['cell_type'] == 'markdown' and ''.join(c['source']).startswith('## ' + title)]
    return len(i), next(''.join(c['source']) for c in nb4[i[0] + 1:] if c['cell_type'] == 'code')


n21, c21 = cell_code('Intermediate coupling regime and Stoner instability')
n6, c6 = cell_code('Magnetic order driven by interactions in a chain')
say('notebook box: the one-site chain with filling=0.1 is in the Stoner cell, and the chain cell is the bichain with no filling',
    n21 == 1 and n6 == 1 and 'geometry.chain()' in c21 and 'filling=0.1' in c21 and 'geometry.bichain()' in c6
    and 'filling' not in c6, 'ok')

# the try-it box: the cell "The strongly interacting limit" runs Us = np.linspace(20.,60,30) with the ferro guess and the
# default mesh, and U (E_FE - E_AF) is close to 4 there
nb = json.load(open(os.path.join(ROOT, 'jupyter-notebooks', 'session6.ipynb')))
cells = nb['cells']
head = [i for i, c in enumerate(cells) if c['cell_type'] == 'markdown' and ''.join(c['source']).startswith('## The strongly interacting limit')]
code = next(''.join(c['source']) for c in cells[head[0] + 1:] if c['cell_type'] == 'code')
prods = []
for U in (20.0, 40.0, 60.0):
    h = geometry.bichain().get_hamiltonian()
    (hfe, efe) = h.get_mean_field_hamiltonian(U=U, return_total_energy=True, mf="ferro", mix=0.9)
    (haf, eaf) = h.get_mean_field_hamiltonian(U=U, return_total_energy=True, mf="antiferro", mix=0.9)
    prods.append(U * (efe - eaf))
say('try-it: the cell runs U from 20 to 60, and U (E_FE - E_AF) is within 0.02 of 4 at 20, 40 and 60',
    len(head) == 1 and 'np.linspace(20.,60,30)' in code and all(abs(p - 4) < 0.02 for p in prods), np.round(prods, 4))
print('all the statements of page 04 hold')
