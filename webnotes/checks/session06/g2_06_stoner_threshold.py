"""Session 6, the statements of page 06 (Sections 6.6 and 6.7), in the order of the page.

The steps fold is checked on a constant density of states and on the chain at n=0.2, the picture quiz on f(m) with
_g2_stonerquiz.check, the flat-band quiz by its arithmetic, the widget by its semicircular density of states, the caption
of moment_vs_U and the quiz on the double occupancy with _g2_chain.check_moment on the variables of the pyqula script
g2_chain_moment.py, and the problem with the density of states of pyqula. The statements of the page that depend on the
points open for the lecturer ("grows continuously" and Figure 6.1(b)) are not asserted here. pyqula runs in a temporary
folder, so the script writes no file. The lab box quotes 10.4 kOhm, which labsource.py checks."""
import os, sys, tempfile
import numpy as np

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', '..')
sys.path.insert(0, os.path.join(ROOT, 'webnotes', 'figures', 'session06'))
import _g2_chain, _g2_stonerquiz, _mf
from _g2_chain import style, say
from pyqula import geometry

TMP = tempfile.TemporaryDirectory()                # pyqula may write files, so it works in a folder of its own,
os.chdir(TMP.name)                                 # which is removed at the exit

# the opener: the uniform threshold of the half-filled chain is 1/D(0) = 2 pi t = 6.28t, while the staggered moment of the
# gap equation is already finite at U = 0.5t and t, far below it, so the staggered order needs no threshold
mm = [_mf.moment(U) for U in (0.5, 1.0)]
say('opener: the staggered moment is finite at U = 0.5t and t, below the uniform threshold 2 pi t = 6.28t',
    all(m > 0 for m in mm) and round(mm[1], 4) == 0.0299 and round(2 * np.pi, 2) == 6.28, (np.round(mm, 5), 2 * np.pi))

# the steps fold, simplest case: a constant density of states D per spin around E_F. At zero temperature the bracket
# n_F(E - x) - n_F(E + x) is one between E_F - x and E_F + x, so the integral is 2 x D = U m D, linear in m
W, EF = 4.0, 0.0
E = np.linspace(-W / 2, W / 2, 400001)
dE = E[1] - E[0]
ok = True
for U, m in ((2.0, 0.1), (4.0, 0.3), (6.0, 0.05)):
    x = U * m / 2
    bracket = (E < EF + x).astype(float) - (E < EF - x).astype(float)
    ok = ok and abs(np.sum(bracket) * dE / W - U * m / W) < 1e-4
say('fold: with a constant D = 1/W the right-hand side is U m D, a straight line of slope U D', ok, 'W = 4')

# the general case, on the chain -2t cos k at n=0.2: N(E) = arccos(-E/2)/pi is the number of states per spin and per
# site below E, so m = N(E_F + x) - N(E_F - x) and its slope 2 x D(E_F) gives D(E_F) = 1/(pi sqrt(4 - E_F^2)) = 0.515
N = lambda e: np.arccos(-e / 2) / np.pi
EF = -2 * np.cos(np.pi * 0.2 / 2)
D = 1 / (np.pi * np.sqrt(4 - EF ** 2))
x = 1e-5
slope = (N(EF + x) - N(EF - x)) / (2 * x)
drift = (N(EF + x) + N(EF - x) - 2 * N(EF)) / x
say('fold: on the chain at n=0.2 the first-order term is 2 x D(E_F), with D(E_F) = 0.515 per spin and per site',
    abs(slope - D) < 1e-6 and round(D, 3) == 0.515 and abs(D - 1 / (2 * np.pi * np.sin(0.1 * np.pi))) < 1e-12, round(D, 5))
say('fold: the total density does not change at first order in x, so E_F stays where it is', abs(drift) < 1e-3, drift)

# the picture quiz on f(m) = tanh(s m): only m = 0 for s = 0.5 and s = 1, with f(0.5) = 0.24 and 0.46, and the crossing
# m0 = 0.86 for s = 1.5
m0 = _g2_stonerquiz.check()
say('quiz: f(0.5) = 0.24 for s = 0.5 and 0.46 for s = 1, no crossing at m > 0, and m0 = 0.86 for s = 1.5',
    round(m0, 2) == 0.86, round(m0, 4))
# the second option: at s = 1 the linear term is m itself, and the next term of tanh(m) - m is -m^3/3, which bends the
# curve down
cub = [(np.tanh(x) - x) / x ** 3 for x in (1e-2, 3e-3)]
say('quiz: at s = 1 the next term of tanh(m) - m is -m^3/3, so the curve bends down below y = m',
    all(abs(c + 1 / 3) < 1e-4 for c in cub), np.round(cub, 6))

# the lab box: 10.4 kOhm is checked by labsource.py, and "three-quarters filling" is in the stored arXiv abstract
src = open(os.path.join(ROOT, 'webnotes', 'sources', 'session06', 'sharpe2019_science.aaw3780.txt')).read()
abstract = src.split('[abstract, from https://export.arxiv.org')[1]
say('lab: the stored arXiv abstract states "near three-quarters (3/4) filling of the conduction miniband"',
    'near three-quarters (3/4) filling of the conduction miniband' in abstract, 'found')

# the flat-band quiz: a band of width W = 0.1t has D about 1/W = 10/t, and U = 0.1t gives U D = 1, far below 4t
say('quiz: W = 0.1t gives D = 10/t, and U = 0.1t gives U D = 1', abs(1 / 0.1 - 10) < 1e-12 and abs(0.1 * 10 - 1) < 1e-12, 'ok')

# the widget: a semicircular density of states of half-bandwidth 2t, normalized, has D(0) = 1/(pi t), threshold pi t
R = 2.0
Es = np.linspace(-R, R, 200001)
rho = 2 / (np.pi * R ** 2) * np.sqrt(np.clip(R ** 2 - Es ** 2, 0, None))
say('widget: the semicircle of half-bandwidth 2t holds one state and has D(E_F) = 1/(pi t) = 0.3183 at half filling',
    abs(np.sum(rho) * (Es[1] - Es[0]) - 1) < 1e-4 and abs(rho[100000] - 1 / np.pi) < 1e-12, round(rho[100000], 4))

# the caption of moment_vs_U and the quiz on the double occupancy, on the variables of the download script
d = style.run_script('session06/g2_chain_moment.py')
_g2_chain.check_moment(d)
# the alt text: the curve starts at U = t with |m| close to zero and 1 - m^2 close to one, and at its end, 24t, |m| is
# close to one and 1 - m^2 close to zero
say('alt: at U = t, |m| = 0.03 and 1 - m^2 = 0.999, and at 24t, |m| above 0.99 and 1 - m^2 below 0.02',
    d['Us'][0] == 1.0 and d['moment'][0] < 0.05 and d['double'][0] > 0.99 and d['moment'][-1] > 0.99
    and d['double'][-1] < 0.02, (round(d['moment'][0], 4), round(d['double'][0], 4), round(d['moment'][-1], 4),
                                round(d['double'][-1], 4)))
# the caption: the curve starts at U = t, where the mesh of 400 cells agrees with the gap equation also when it is odd,
# while at U = 0.5t the mesh gives a moment many times the value 0.0001 of the gap equation
mesh = {}
for U, nk in ((1.0, 401), (0.5, 400)):
    h = geometry.bichain().get_hamiltonian(tij=[-1.])
    hmf = h.get_mean_field_hamiltonian(U=U, mf="antiferro", mix=0.9, nk=nk)
    mesh[(U, nk)] = abs(float(np.real(hmf.get_vev('mz', nk=nk)[0])))
say('caption: at U=t the mesh of 401 cells gives 0.03 too, and at U=0.5t the mesh of 400 cells misses the gap equation',
    abs(mesh[(1.0, 401)] - _mf.moment(1.0)) < 1e-3 and round(mesh[(1.0, 401)], 2) == 0.03
    and mesh[(0.5, 400)] > 10 * _mf.moment(0.5), (mesh, round(_mf.moment(0.5), 6)))
say('quiz: 0.03 is 3 percent of the value 1 of independent spins at U = 0, where 4 * (1/2)(1/2) = 1',
    round(0.03 * 100) == 3 and 4 * 0.5 * 0.5 == 1.0, 'ok')

# the problem: D = 1/W is normalized, the slope is U/W and U_c = W, so 4t for W = 4t. The D(E_F) of pyqula per spin and
# per site is h.get_dos() of the spinful Hamiltonian divided by 2 and by the number of sites of the cell: the spinful
# chain gives twice the spinless one, 1/pi at the center of the band, and the bichain with two sites gives the same per cell
say('problem: D = 1/W holds one state per spin and per site, and U D = 1 at U_c = W, which is 4t for W = 4t',
    abs(W * (1 / W) - 1) < 1e-12 and abs(4.0 * (1 / 4.0) - 1) < 1e-12, 'ok')
e0 = np.array([-0.3, 0.0, 0.3])
(e, d1) = geometry.chain().get_hamiltonian().get_dos(energies=e0, mode="Green", delta=1e-3)
(e, d0) = geometry.chain().get_hamiltonian(has_spin=False).get_dos(energies=e0, mode="Green", delta=1e-3)
(e, d2) = geometry.bichain().get_hamiltonian().get_dos(energies=e0, mode="Green", delta=1e-3)
ref = 1 / (np.pi * np.sqrt(4 - e0 ** 2))
say('problem: h.get_dos() of the spinful chain is 2 D(E) per site, and of the spinful bichain 2 * 2 D(E) per cell',
    np.allclose(np.array(d1) / 2, ref, rtol=2e-3) and np.allclose(np.array(d0), ref, rtol=2e-3)
    and np.allclose(np.array(d2) / 4, ref, rtol=2e-3), (np.round(np.array(d1) / 2, 4), np.round(ref, 4)))
# the call that the page names, h.get_dos(nk=2000, delta=0.02) in its default mode, gives the same D(E) per spin and per
# site on the chain and on the bichain, also on its own grid of energies (checked for |E| < 0.5t, the center of the
# band), while the default nk=100 with delta=5/nk is off by more than 10 percent close to the center of the band of the
# chain, above at E=0 and at the grid point 0.01 of the default energies, and below at E=+-0.3
(e, a1) = geometry.chain().get_hamiltonian().get_dos(energies=e0, nk=2000, delta=0.02, write=False)
(e, a2) = geometry.bichain().get_hamiltonian().get_dos(energies=e0, nk=2000, delta=0.02, write=False)
(eg, ag) = geometry.chain().get_hamiltonian().get_dos(nk=2000, delta=0.02, write=False)
eg, ag = np.array(eg), np.array(ag)
near = np.abs(eg) < 0.5
(edef, adef) = geometry.chain().get_hamiltonian().get_dos(write=False)     # the default call, on its own energies
edef, adef = np.array(edef), np.array(adef)
i0 = int(np.argmin(np.abs(edef)))                                            # the grid point closest to E=0, 0.01
ed = np.array([0.0, -0.3, 0.3])
(e, a0) = geometry.chain().get_hamiltonian().get_dos(energies=ed, write=False)
err = 100 * (np.concatenate([np.array(a0), [adef[i0]]]) / 2 / (1 / (np.pi * np.sqrt(4 - np.append(ed, edef[i0]) ** 2))) - 1)
say('problem: h.get_dos(nk=2000, delta=0.02) divided by 2 and by the sites of the cell is D(E) within 0.5 percent, and '
    'the default call is off by more than 10 percent close to the center, above at E=0 and 0.01, below at E=+-0.3',
    np.allclose(np.array(a1) / 2, ref, rtol=5e-3) and np.allclose(np.array(a2) / 4, ref, rtol=5e-3)
    and np.allclose(ag[near] / 2, 1 / (np.pi * np.sqrt(4 - eg[near] ** 2)), rtol=5e-3)
    and abs(edef[i0]) < 0.02 and np.all(np.abs(err) > 10) and err[0] > 0 and err[3] > 0 and err[1] < 0 and err[2] < 0,
    (np.round(np.array(a1) / 2, 4), np.round(np.array(a2) / 4, 4), round(float(edef[i0]), 4), np.round(err, 1)))
# the chain of the same width 4t: D(E) = 1/(pi sqrt(4t^2 - E^2)) is lowest at the center, D(0) = 1/(2 pi t) = 0.159/t,
# below 1/W = 0.25/t, so its uniform threshold at half filling is 2 pi t, about 6.3t, and not 4t
Ec = np.linspace(-1.99, 1.99, 4001)
Dc = 1 / (np.pi * np.sqrt(4 - Ec ** 2))
say('problem: the chain of width 4t has its largest D at the band edges and its lowest at the center, D(0) = 1/(2 pi t) '
    'below 1/W, and U_c = 2 pi t = 6.3t',
    np.argmin(Dc) == 2000 and set(np.argsort(Dc)[-2:]) == {0, 4000} and abs(Dc[2000] - 1 / (2 * np.pi)) < 1e-12 and Dc[2000] < 1 / 4.0 and round(2 * np.pi, 1) == 6.3
    and abs(1 / Dc[2000] - 2 * np.pi) < 1e-12, (round(Dc[2000], 4), round(2 * np.pi, 3)))
print('all the statements of page 06 hold')
