"""Shared checks of the mean-field Hubbard chain of Sections 6.4 to 6.7, for the figures and the page checks of g2.

The data come from the downloadable pyqula scripts of webnotes/scripts/session06/, g2_chain_meanfield.py (U=4t, the
ferromagnet at n=0.2 and the antiferromagnet at half filling), g2_chain_energy_difference.py (E_FM - E_AFM at large U)
and g2_chain_moment.py (the moment against U). The second route is _mf.py, the gap equation 1 = (U/2) <1/E_k> of the
half-filled chain solved with scipy, and the closed forms of the bands. Each check asserts the numbers that the
captions, the quizzes and the key box of pages 04 and 06 quote. Nothing here writes a file."""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
import style, _mf


def say(name, ok, value):
    print(('OK     ' if ok else 'FAILED ') + name + ': ' + str(value), flush=True)
    assert ok, name


def energy_afm(U):
    """E_AFM per site from the gap equation, with its kinetic part, its interaction part and the moment, as in
    mf_chain.py. The kinetic energy -<eps^2/E> counts both spins, and the interaction is U <n_up><n_dn>."""
    D = _mf.gap_parameter(U)
    m = 2 * D / U
    kin = -_mf.avg(lambda e, D: e * e / np.sqrt(e * e + D * D), D)
    inter = U * (1 - m * m) / 4
    return kin + inter, kin, inter, m


def check_meanfield(d):
    """The chain at U=4t of g2_chain_meanfield.py, the captions of fm_afm_chain and mf_chain (a) and the band quizzes."""
    U, ks = d['U'], d['ks']
    say('the script runs U=4t on the momenta -pi to pi', U == 4.0 and abs(ks[0] + np.pi) < 1e-12 and abs(ks[-1] - np.pi) < 1e-12
        and np.any(np.abs(ks) < 1e-12) and np.any(np.abs(ks - np.pi / 2) < 1e-12), len(ks))
    # the ferromagnet at n=0.2: every electron has spin up, m = n = 0.2, and the splitting is U m = 0.8
    hfm = d['hfm']
    nup, ndn = np.real(hfm.get_vev('up', nk=300))[0], np.real(hfm.get_vev('dn', nk=300))[0]
    say('ferromagnet: n_up = 0.2 and n_dn = 0, so m = 0.200 and the filled band is spin up',
        abs(nup - 0.2) < 1e-6 and abs(ndn) < 1e-6 and abs(d['m_fm'] - 0.2) < 1e-6, (nup, ndn, d['m_fm']))
    say('ferromagnet: the exchange splitting is U m = 0.800, spin down above spin up',
        abs(d['splitting'] - U * 0.2) < 1e-6 and d['onsite'][0] < d['onsite'][1], d['splitting'])
    off = max(abs(d['hk1']([k, 0., 0.])[0, 1]) for k in (0.0, 0.13, 0.37))
    say('ferromagnet: the Bloch Hamiltonian is diagonal in spin, so each band has one spin', off < 1e-12, off)
    bfm = d['bands_fm']
    mu = -2 * np.cos(np.pi * 0.2)                        # the Fermi level of n=0.2 in the frame of -2t cos k
    ref_up, ref_dn = -2 * np.cos(ks) - mu, -2 * np.cos(ks) + U * 0.2 - mu
    say('ferromagnet: the bands are -2t cos k and -2t cos k + Um, measured from mu = -2t cos(pi n) = -1.618',
        np.allclose(bfm[:, 0], ref_up, atol=1e-9) and np.allclose(bfm[:, 1], ref_dn, atol=1e-9), round(mu, 3))
    lo, hi = bfm[:, 0].min(), bfm[:, 1].min()
    say('ferromagnet: the band bottoms are -0.38 and 0.42 from mu, 0.8 apart, both at k=0',
        round(lo, 2) == -0.38 and round(hi, 2) == 0.42 and abs(hi - lo - 0.8) < 1e-9
        and ks[np.argmin(bfm[:, 0])] == 0.0, (round(lo, 4), round(hi, 4)))
    say('ferromagnet: the lower band is partly filled, so the Fermi level cuts it, and the upper band is empty',
        bfm[:, 0].min() < 0 < bfm[:, 0].max() and bfm[:, 1].min() > 0, (round(bfm[:, 0].max(), 3), round(hi, 3)))
    # the antiferromagnet at half filling: |m| = 0.769 against the gap equation, the gap U|m| = 3.08
    m = np.abs(np.real(d['m_afm']))
    say('antiferromagnet: |m| = 0.769 on both sites with opposite signs, as the gap equation gives',
        abs(m[0] - m[1]) < 1e-9 and np.real(d['m_afm'][0]) * np.real(d['m_afm'][1]) < 0
        and abs(m[0] - _mf.moment(U)) < 1e-4 and round(m[0], 2) == 0.77, (round(m[0], 5), round(_mf.moment(U), 5)))
    say('antiferromagnet: the gap is U|m| = 3.08', abs(d['gap'] - U * m[0]) < 1e-3 and round(d['gap'], 2) == 3.08,
        round(d['gap'], 4))
    Delta = U * m[0] / 2
    baf, bpm = d['bands_afm'], d['bands_pm']
    e = np.sqrt(4 * np.cos(ks) ** 2 + Delta ** 2)
    say('antiferromagnet: the bands are +-sqrt(eps_k^2 + (Um/2)^2), each twice, with eps_k = -2t cos k',
        np.allclose(baf, np.stack([-e, -e, e, e], axis=1), atol=1e-6), round(Delta, 4))
    say('antiferromagnet: the gap edges +-Um/2 = +-1.54 sit at k = +-pi/2, the zone boundary of the cell of two sites',
        round(Delta, 2) == 1.54 and abs(abs(ks[np.argmin(baf[:, 2])]) - np.pi / 2) < 1e-9, round(Delta, 4))
    say('U=0: the bands of the cell of two sites are +-2t|cos k|, which cross at the Fermi level at k = +-pi/2',
        np.allclose(bpm, np.stack([-2 * np.abs(np.cos(ks))] * 2 + [2 * np.abs(np.cos(ks))] * 2, axis=1), atol=1e-9)
        and abs(bpm[np.argmin(np.abs(ks - np.pi / 2)), 3]) < 1e-9, 'ok')
    # the quiz with equations as options: eps_k +- Um/2 at |m|=0.77 overlap by 0.46 on each side, and +-|eps_k| + Um/2
    # meet at eps_k=0, at Um/2, so neither has the gap of the antiferromagnet
    top_lower, bottom_upper = 2 - Delta, -2 + Delta
    say('quiz: eps_k - Um/2 ends at 0.46 and eps_k + Um/2 starts at -0.46, so the two copies overlap',
        round(top_lower, 2) == 0.46 and round(bottom_upper, 2) == -0.46, (round(top_lower, 3), round(bottom_upper, 3)))


def check_energy(d):
    """E_FM - E_AFM of g2_chain_energy_difference.py, the figure ufactor and the quiz on the 1/U law."""
    Us, diff, prod = d['Us'], d['difference'], d['product']
    mf = np.array([np.real(x) for x in d['m_fm']])
    ma = np.array([np.real(x) for x in d['m_afm']])
    say('ferromagnet: the seeded loop stays saturated, m = 1 on both sites, so spin up as on the page, with zero energy, '
        'at every U', np.allclose(mf, 1.0, atol=1e-6) and np.allclose(d['e_fm'], 0.0, atol=1e-8), list(Us))
    ok = True
    for U, x, a in zip(Us, diff, ma):
        e, kin, inter, m = energy_afm(U)
        ok = ok and abs(x - 2 * (0.0 - e)) < 2e-4 and abs(abs(a[0]) - m) < 1e-4 and a[0] * a[1] < 0
    say('E_FM - E_AFM per cell of two sites agrees with twice minus E_AFM per site of the gap equation', ok,
        np.round(diff, 4))
    D = dict(zip(Us, diff))
    P = dict(zip(Us, prod))
    # the product is 3.9975 at 40t on both routes, at the edge of the third digit, so the page quotes only "close to 4"
    say('quiz: 0.1995 at U=20t and 0.0999 at U=40t, and U times it is 3.99 and 4.00, close to 4t^2',
        round(D[20.0], 4) == 0.1995 and round(D[40.0], 4) == 0.0999 and round(P[20.0], 2) == 3.99
        and round(P[40.0], 2) == 4.00, (round(D[20.0], 5), round(D[40.0], 5), round(P[20.0], 4), round(P[40.0], 4)))
    say('the difference falls with U and stays below 4t^2/U, the line of the figure',
        np.all(np.diff(diff) < 0) and np.all(diff < 4 / Us), np.round(prod, 3))
    say('quiz: 4t^2/U is 0.2 at 20t and 0.1 at 40t, doubling would give 0.4, a 1/U^2 law would give 0.05',
        4 / 20 == 0.2 and 4 / 40 == 0.1 and 2 * 0.2 == 0.4 and 0.2 / 4 == 0.05, 'ok')


def check_moment(d):
    """The moment of g2_chain_moment.py against the gap equation, the caption of moment_vs_U and the quiz of 6.7."""
    Us, mo, dbl = d['Us'], d['moment'], d['double']
    ref = np.array([_mf.moment(U) for U in Us])
    say('the moment of pyqula agrees with the gap equation within 1e-3 at every U from t to 24t',
        Us[0] == 1.0 and Us[-1] == 24.0 and np.max(np.abs(mo - ref)) < 1e-3, round(np.max(np.abs(mo - ref)), 6))
    say('the moment grows with U and the double occupancy 1 - m^2 falls', np.all(np.diff(mo) > 0) and np.all(np.diff(dbl) < 0)
        and np.allclose(dbl, 1 - mo ** 2), 'ok')
    M = dict(zip(Us, mo))
    say('caption: |m| = 0.03 at U=t, 0.77 at 4t and 0.98 at 16t', round(M[1.0], 2) == 0.03 and round(M[4.0], 2) == 0.77
        and round(M[16.0], 2) == 0.98, (round(M[1.0], 4), round(M[4.0], 4), round(M[16.0], 4)))
    say('quiz: |m| = 0.984 at 16t, so 1 - m^2 = 0.03, m^2 = 0.97 and 1 - |m| = 0.016',
        round(M[16.0], 3) == 0.984 and round(_mf.moment(16.0), 3) == 0.984 and round(1 - 0.984 ** 2, 2) == 0.03
        and round(1 - M[16.0] ** 2, 2) == 0.03 and round(0.984 ** 2, 2) == 0.97 and round(1 - 0.984, 3) == 0.016,
        round(1 - M[16.0] ** 2, 4))
    say('quiz: at 4t, |m| = 0.77 gives 1 - m^2 = 0.41 and 1 - |m| = 0.23',
        round(1 - M[4.0] ** 2, 2) == 0.41 and round(1 - M[4.0], 2) == 0.23, (round(1 - M[4.0] ** 2, 4), round(1 - M[4.0], 4)))
