"""Session 4, the numbers that page 10 (Section 4.10, the Landau levels of Dirac electrons) quotes and that no figure
script asserts. One check script per page is the rule: every number of a caption, a feedback, a fold, a solution or a
lab box is an assert, here or in the figure script that draws it. The figure scripts assert their own captions:
dirac_levels.py (the weights 1 and 1/2, E_4 = 2 E_1, the 60 oscillator states), g3_dirac_fan.py (E_1 of the lattice
within one percent of (4.7) at the flux 0.0032, 0.51 against 0.52 at 0.0096, the cells N = 10 to 60) and _g3_ladders.py
(the feedback of the picture quiz). This script checks the fold by a second route, the Dirac Hamiltonian of the Landau
gauge written with x and p_x in an oscillator basis, also for qB < 0, the energies of graphene in the quizzes and in the
lab box, the sentences of the lab box in the stored source, the plateaus of the problem by counting and with the Chern
numbers of pyqula, for the honeycomb and the square lattice, the area of a hexagon in units of the flux, the widths of
the levels of the fan on a k-mesh and the sublattice of the zero level on the lattice.
It finds the repository from its own path and writes no file, since pyqula runs in a temporary folder.

The blocks marked "corrected on 2026-11-22" back the sentences of the old text that were corrected on that day, after
the lecturer chose to fix the errors of the old text."""
import os
import tempfile

import numpy as np

h = 6.62607015e-34          # J s
hbar = h / (2 * np.pi)
e = 1.602176634e-19         # C


def check(name, ok, value):
    print(('OK     ' if ok else 'FAILED ') + name + ': ' + str(value), flush=True)
    assert ok, name


# the fold, by a route that does not use a and a^dagger: H = v [[0, pi_x - i pi_y], [pi_x + i pi_y, 0]] with
# pi_x = p_x and pi_y = hbar k_y - B x, for the charge +e, written with x and p_x in a basis of M oscillator states,
# in units hbar = B = v = 1, so l_B = 1 and (4.7) is E_n = sgn(n) sqrt(2 |n|)
M = 120
b = np.diag(np.sqrt(np.arange(1, M)), 1)
X = (b + b.T) / np.sqrt(2)
P = 1j * (b.T - b) / np.sqrt(2)
for ky in (0.0, 0.7):
    pim = P - 1j * (ky * np.eye(M) - X)          # pi_x - i pi_y
    H = np.block([[np.zeros((M, M)), pim], [pim.conj().T, np.zeros((M, M))]])
    w, v = np.linalg.eigh(H)
    # the truncation adds one spurious zero mode, a^dagger of the cut basis kills its last state, which sits in the
    # lower component at the highest oscillator states; the physical zero mode is the other one
    Z = v[:, np.abs(w) < 1e-6]
    pw, pv = np.linalg.eigh(Z[:M].conj().T @ Z[:M])     # the weight in the upper component, within the zero modes
    phys = Z @ pv[:, -1]
    spur = Z @ pv[:, 0]
    ok = Z.shape[1] == 2 and abs(pw[-1] - 1) < 1e-8 and abs(pw[0]) < 1e-8
    ok &= np.sum(np.abs(phys[:20]) ** 2) > 0.99 and np.sum(np.abs(spur[M + M // 2:]) ** 2) > 0.99
    check('fold: one level at zero energy for k_y = %.1f, fully in the upper component (and one spurious mode of the '
          'cut basis at its top)' % ky, ok, (Z.shape[1], np.round(pw, 8)))
    nonzero = np.sort(np.abs(w[np.abs(w) > 1e-6]))
    check('fold: no other level below sqrt(2) for k_y = %.1f' % ky, abs(nonzero[0] - np.sqrt(2)) < 1e-6, nonzero[0])
    for n in (1, 2, 3, 4):
        for s in (1, -1):
            i = np.argmin(np.abs(w - s * np.sqrt(2 * n)))
            upn = np.sum(np.abs(v[:M, i]) ** 2)
            ok = abs(w[i] - s * np.sqrt(2 * n)) < 1e-6 and abs(upn - 0.5) < 1e-6
            check('fold: level %+d at %+.4f = sgn(n) sqrt(2|n|) hbar v / l_B, weight 1/2 in each component' % (s * n, w[i]),
                  ok, upn)
# the picture quiz: the zero mode is in the upper component for the valley K and qB > 0, the charge +e of the page,
# which the loop above checks, and in the lower component for qB < 0, with pi_y = hbar k_y + B x
for ky in (0.0, 0.7):
    pim = P - 1j * (ky * np.eye(M) + X)
    H = np.block([[np.zeros((M, M)), pim], [pim.conj().T, np.zeros((M, M))]])
    w, v = np.linalg.eigh(H)
    Z = v[:, np.abs(w) < 1e-6]
    pw, pv = np.linalg.eigh(Z[M:].conj().T @ Z[M:])     # the weight in the lower component, within the zero modes
    phys = Z @ pv[:, -1]
    ok = Z.shape[1] == 2 and abs(pw[-1] - 1) < 1e-8 and np.sum(np.abs(phys[M:M + 20]) ** 2) > 0.99
    check('quiz: for qB < 0 the zero mode is fully in the lower component, k_y = %.1f' % ky, ok, np.round(pw, 8))
# the commutator of the fold in this representation, [pi_x, pi_y] = i hbar B, away from the truncation
pix, piy = P, 0.7 * np.eye(M) - X
comm = pix @ piy - piy @ pix
check('fold: [pi_x, pi_y] = i hbar B in the basis', np.allclose(comm[:M - 2, :M - 2], 1j * np.eye(M)[:M - 2, :M - 2]),
      comm[0, 0])

# the energies of graphene, E_1 = v sqrt(2 hbar e B) with v = 1e6 m/s, in meV
E1 = lambda B, v=1e6: v * np.sqrt(2 * hbar * e * B) / e * 1e3
check('quiz: E_1 about 36 meV at 1 T', round(E1(1)) == 36, E1(1))
check('quiz: E_1 = 109 meV at 9 T, a factor 3', round(E1(9)) == 109 and abs(E1(9) / E1(1) - 3) < 1e-12, E1(9))
check('quiz: the linear law would give 327 meV at 9 T', round(9 * E1(1)) == 327, 9 * E1(1))
check('quiz: E_1 = 36.3 meV at 1 T, the value of the feedback of the ratio quiz', round(E1(1), 1) == 36.3, E1(1))
check('quiz: a linear ladder gives E_4 = 145 meV at 1 T', round(4 * E1(1)) == 145 and round(4 * 36.3) == 145,
      4 * E1(1))
check('quiz: the square-root law gives E_4 = 73 meV at 1 T', round(2 * E1(1)) == 73 and abs(np.sqrt(4) - 2) < 1e-12,
      2 * E1(1))
check('quiz: E_n proportional to n^2 gives E_4 = 581 meV at 1 T', round(16 * E1(1)) == 581 and round(16 * 36.3) == 581,
      16 * E1(1))
check('lab box, ours: E_1 = 169 meV at 18 T for v = 1.1e6 m/s', round(E1(18, 1.1e6)) == 169, E1(18, 1.1e6))
check('lab box: the transition energies of (4.7) scale as sqrt(B)',
      abs((E1(18) + E1(18) * np.sqrt(2)) / (E1(4.5) + E1(4.5) * np.sqrt(2)) - 2) < 1e-12, 'E_1 + E_2 at 18 T and 4.5 T')
# the text after (4.7) and the caption of Figure 4.4, corrected on 2026-11-22 from "two orders of magnitude" to "one
# order of magnitude": E_1 of graphene over hbar omega_c = hbar e B / m* of GaAs, m* = 0.067 m_e, for 1 to 10 T, by the SI
# constants and by the rates of the conventions sheet, 36.28 meV sqrt(B/T) and 1.728 meV B/T
fields = np.linspace(1, 10, 91)
wc_gaas = hbar * e * fields / (0.067 * 9.1093837015e-31) / e * 1e3
ratio, ratio2 = E1(fields) / wc_gaas, 36.28 * np.sqrt(fields) / (1.728 * fields)
check('text and Figure 4.4: E_1 / hbar omega_c is 21 at 1 T and 6.6 at 10 T, within half a decade of 10 and far from 100',
      round(ratio[0]) == 21 and round(ratio[-1], 1) == 6.6 and np.allclose(ratio, ratio2, rtol=1e-3)
      and np.all(np.abs(np.log10(ratio) - 1) < 0.5) and ratio.max() < 100 / 4, (round(ratio[0], 2), round(ratio[-1], 2)))
# the same sentence, which since 2026-11-22 names v_F = 1e6 m/s and m* = 0.067 m_e as what sets the ratio, and says that the
# ratio falls as 1/sqrt(B): E_1 / hbar omega_c = m* v_F sqrt(2/(hbar e B)), which is 1 only at 2 m*^2 v_F^2/(hbar e), 440 T
b_equal = 2 * (0.067 * 9.1093837015e-31 * 1e6) ** 2 / (hbar * e)
check('text: the ratio is m* v_F sqrt(2/(hbar e B)), it falls as 1/sqrt(B), and it is 1 only at 440 T',
      np.allclose(ratio, 0.067 * 9.1093837015e-31 * 1e6 * np.sqrt(2 / (hbar * e * fields)), rtol=1e-9)
      and np.allclose(ratio * np.sqrt(fields), ratio[0], rtol=1e-9) and round(b_equal, -1) == 440
      and abs(E1(b_equal) / (hbar * e * b_equal / (0.067 * 9.1093837015e-31) / e * 1e3) - 1) < 1e-9, round(b_equal, 1))
# the lab box: every sentence that it takes from the source is in the stored text, also the velocity 1.1e6 m/s, which
# the lint does not read since m/s is not one of its units
REPO = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', '..')
with open(os.path.join(REPO, 'webnotes', 'sources', 'session04', 'jiang2007_arxivcond-mat-0703822.txt')) as fh:
    source = fh.read()
for quote in ('Infrared transmission is measured in magnetic fields up to B=18 T',
              'Resonances between hole LLs and electron LLs, as well as resonances between hole and electron LLs are '
              'resolved', 'proportional to √B', 'c≈1.1×10^6 m/s', 'The lack of precise scaling between different LL '
              'transitions indicates considerable contributions of many-particle effects',
              'show in situ half-integer quantum Hall plateaus'):
    check('lab box: the stored source says "%s"' % quote, quote in source, 'found')

# the fan caption: a hexagon of bond length 1 has the area 3 sqrt(3)/2 = 2.60
check('fan: a hexagon holds the flux 2.60 phi', round(3 * np.sqrt(3) / 2, 2) == 2.60, 3 * np.sqrt(3) / 2)

# the problem: four states per flux quantum, the level n = 0 half filled at zero density
plateaus = [4 * (n + 0.5) for n in range(3)]
count = [2 + 4 * n for n in range(3)]
check('problem: 4 (n + 1/2) = 2 + 4n = 2, 6 and 10', plateaus == count == [2, 6, 10], plateaus)
# second route: the Chern numbers of pyqula in the gaps of the honeycomb lattice in a field, spinless, times two spins.
# The magnetic cell of 80 sites with one flux quantum, phi = 0.0096, has the levels 0, +-0.509, +-0.70, +-0.835.
cwd = os.getcwd()
with tempfile.TemporaryDirectory() as d:
    os.chdir(d)
    try:
        from pyqula import geometry
        n = 20
        g = geometry.honeycomb_lattice_square_cell().rotate(90).get_supercell((n, 1))
        cs = []
        for mu in (0.25, -0.25, -0.6, -0.77):     # below the zero level, above it, above n = 1, above n = 2
            hh = g.get_hamiltonian(has_spin=False)
            hh.add_orbital_magnetic_field(1 / (3 * np.sqrt(3) * n))
            hh.add_onsite(mu)                     # moves the levels up by mu, so zero energy sits at -mu
            cs.append(int(round(hh.get_chern(nk=8))))
        # the problem, the parabolic band: the square lattice with the flux 1/15 per plaquette, spinless, in the gaps
        # above the levels n = 0, 1, 2, as on the conventions sheet
        q = 15
        gs = geometry.square_lattice().get_supercell((1, q))
        hs = gs.get_hamiltonian(has_spin=False, tij=[-1.])
        hs.add_orbital_magnetic_field(1 / q)
        es = np.sort(np.linalg.eigvalsh(hs.get_hk_gen()([0., 0., 0.])))[:4]
        csq = []
        for gap in range(3):
            hs = gs.get_hamiltonian(has_spin=False, tij=[-1.])
            hs.add_orbital_magnetic_field(1 / q)
            hs.add_onsite(-0.5 * (es[gap] + es[gap + 1]))   # zero energy in the gap above the level gap
            csq.append(int(round(hs.get_chern(nk=8))))
        # the fan caption: the cell has 4N sites, and its levels at the strongest flux are bands, on an 18 x 18 k-mesh, where the widths have converged
        sites = [len(geometry.honeycomb_lattice_square_cell().rotate(90).get_supercell((nn, 1)).r) for nn in (10, 20)]
        widths = {}
        for nn in (10, 20):
            gw = geometry.honeycomb_lattice_square_cell().rotate(90).get_supercell((nn, 1))
            hw = gw.get_hamiltonian(has_spin=False)
            hw.add_orbital_magnetic_field(1 / (3 * np.sqrt(3) * nn))
            hk = hw.get_hk_gen()
            ks = np.linspace(0, 1, 18, endpoint=False)
            ee = []
            for k1 in ks:
                for k2 in ks:
                    ev = np.linalg.eigvalsh(hk([k1, k2, 0.]))
                    ee.append(np.sort(ev[np.argsort(np.abs(ev))[:14]]))
            ee = np.array(ee)
            widths[nn] = [np.ptp(ee[:, j:j + 2]) for j in (8, 10, 12)]   # the levels n = 1, 2, 3, two states each
        # the picture quiz: in the zero level of the cell of 80 sites, one state lives on each sublattice, for both
        # signs of the field, so the two valleys have their zero modes on opposite sublattices
        split = []
        gz = geometry.honeycomb_lattice_square_cell().rotate(90).get_supercell((20, 1))
        for sgn in (1, -1):
            hz = gz.get_hamiltonian(has_spin=False)
            hz.add_orbital_magnetic_field(sgn / (3 * np.sqrt(3) * 20))
            ez, vz = np.linalg.eigh(hz.get_hk_gen()([0., 0., 0.]))
            Zl = vz[:, np.abs(ez) < 1e-3]
            PA = np.diag((np.array(gz.sublattice) > 0).astype(float))
            split.append(np.linalg.eigvalsh(Zl.conj().T @ PA @ Zl))
    finally:
        os.chdir(cwd)
check('problem: pyqula spinless C = -1, 1, 3, 5 in the gaps below n = 0 and above n = 0, 1, 2', cs == [-1, 1, 3, 5], cs)
check('problem: with two spins the plateaus are -2 and 2, 6, 10, the sequence +-2, +-6, +-10',
      [2 * c for c in cs] == [-2, 2, 6, 10], [2 * c for c in cs])
check('problem: a parabolic band with two spins per level gives 2(n+1) = 2, 4 and 6 by counting',
      [2 * (n + 1) for n in range(3)] == [2, 4, 6], [2 * (n + 1) for n in range(3)])
check('problem: pyqula, the square lattice with the flux 1/15 has |C| = 1, 2, 3 spinless, so 2, 4, 6 with two spins',
      [2 * abs(c) for c in csq] == [2, 4, 6], csq)
check('fan: the magnetic cell has 4N sites, 40 for N = 10 and 80 for N = 20', sites == [40, 80], sites)
check('fan: at phi = 0.0192 the levels n = 1, 2, 3 are bands about 0.02, 0.08 and 0.12 t wide on an 18 x 18 k-mesh',
      [round(x, 2) for x in widths[10]] == [0.02, 0.08, 0.12], np.round(widths[10], 4))
check('fan: at phi = 0.0096 the three widths are below 0.005 t', max(widths[20]) < 0.005, np.round(widths[20], 5))
check('quiz: in the zero level of the honeycomb cell one state is on each sublattice, for both signs of the field',
      all(np.allclose(s, [0, 1], atol=1e-6) for s in split) and all(len(s) == 2 for s in split), np.round(split, 6))
