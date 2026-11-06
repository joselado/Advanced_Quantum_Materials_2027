"""Session 10, the order parameter m of Eq. (10.9) for the 2D Ising model, from the exact result of Onsager."""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
import numpy as np
import matplotlib.pyplot as plt
import style

Tc = 2 / np.log(1 + np.sqrt(2))                      # in units of J, with k_B = 1
T = np.linspace(0.05, 3.6, 800)
m = np.zeros_like(T)
lo = T < Tc
m[lo] = (1 - np.sinh(2 / T[lo]) ** -4) ** (1 / 8)

fig, ax = plt.subplots(figsize=(style.WIDTH_CM * style.CM, 5.2 * style.CM))
style.arrows(ax, xlabel=r'$T/J$', ylabel=r'$|m|$')
ax.set_xlim(0, 3.7); ax.set_ylim(0, 1.15)
ax.plot(T[lo], m[lo], color=style.ACCENT)
ax.plot(T[~lo], m[~lo], color=style.ACCENT)
style.guide(ax, x=Tc)
style.label(ax, Tc, -0.07, r'$T_c=2.27J$', fontsize=8.5)
style.label(ax, 1.0, 0.76, r'ordered, $|m|\to1$', color=style.ACCENT, fontsize=8.5)
style.label(ax, 3.0, 0.1, r'disordered, $|m|\to0$', color=style.ACCENT, fontsize=8.5)
style.save(fig, __file__)
print(Tc)
