"""Figure s06f06, fig:s06:dispersion: ferromagnetic against antiferromagnetic magnons, (6.8) and (6.9).

Seen from the front, for the chain, z = 2 and gamma(k) = cos ka, both in units of |J| S z:
E_FM = 1 - cos ka (the parabola at k = 0) and E_AFM = |sin ka| (the cone). Two renders: the whole
zone, and the zone center magnified five times along both axes.
"""
import math
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import figlib as F                                                        # noqa: E402

NAME = 's06f06_dispersion'
FM, AFM = F.ACCENT_AQM, F.BROKEN


def plot(kmax, scale, sx, sz, tag):
    ks = [-kmax + 2 * kmax * j / 300 for j in range(301)]
    P = lambda k, e: (sx * k, 0, sz * e)
    F.tube(f'{tag}_fm', [P(k, (1 - math.cos(k)) * scale) for k in ks if (1 - math.cos(k)) * scale <= 2.05], 0.035, FM)
    F.tube(f'{tag}_afm', [P(k, abs(math.sin(k)) * scale) for k in ks if abs(math.sin(k)) * scale <= 2.05], 0.035, AFM)
    F.axis(f'{tag}_ax', P(-kmax - 0.05, 0), P(kmax + 0.3 / sx, 0), r=0.016, head=0.13)
    F.axis(f'{tag}_ay', P(0, 0), P(0, 2.3), r=0.016, head=0.13)
    F.ball(f'{tag}_gold', P(0, 0), 0.07, rgb=F.SITE)
    F.anchor('k', P(kmax + 0.3 / sx, 0))
    F.anchor('E', P(0, 2.3))
    F.anchor('kmax', P(kmax, -0.03))
    F.anchor('kmin', P(-kmax, -0.03))
    F.anchor('fm', P(kmax * 0.62, (1 - math.cos(kmax * 0.62)) * scale))
    F.anchor('afm', P(kmax * 0.3, abs(math.sin(kmax * 0.3)) * scale))
    F.anchor('panel', P(-kmax, 2.35))


def build_main():
    F.studio()
    plot(math.pi, 1.0, 1.15, 1.0, 'm')
    F.camera((0.15, 0.0, 1.1), elev=3.0, ortho=8.6, aspect=8.3 / 3.5)


def build_zoom():
    F.studio()
    plot(math.pi / 5, 5.0, 2.4, 1.0, 'z')
    F.camera((0.15, 0.0, 1.1), elev=3.0, ortho=4.0, aspect=4.0 / 3.5)


F.main_panels(NAME, [('main', build_main), ('zoom', build_zoom)])
