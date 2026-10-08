"""
Style check: the same elements as Fig. 2 of the draft, drawn with
paper_style.  Curves are schematic (the analysis code is not in this
container) -- this figure is for comparing fonts, weights and colours
against the compiled paper, not for physics.
"""
import numpy as np
import paper_style as ps

fig, (a, b) = ps.double()

# ---- left: cumulative distributions with threshold markers --------------
E = np.logspace(0.5, 3, 500)

cases = [
    ("XENONnT $pp$",        16.5,  69.,  170., ps.C[0], "-"),
    ("PandaX-4T Run 0$+$2", 82.2, 102., 192., ps.C[1], ps.DASH),
    ("Borexino Phase-II",   335.,  336., 350., ps.C[2], ps.DASHD),
]

for lab, emin, edet, p5, col, ls in cases:
    F = np.clip((np.log(np.maximum(E, emin) / emin) / np.log(22.0))**0.9, 0, 1)
    F[E < emin] = 0.0
    a.plot(E, F, color=col, lw=ps.LW_MAIN, ls=ls, label=lab)
    a.plot([emin, emin], [0, 0.06], color=col, lw=ps.LW_THIN, ls=(0, (2, 2)))
    k = np.argmin(abs(E - p5))
    a.plot(p5, F[k], "o", color=col, ms=7, mfc="white", mew=1.8, zorder=5)

a.set_xscale("log")
a.set_xlim(3, 1000)
a.set_ylim(0, 1.02)
a.set_xlabel(r"$E_\nu$ [keV]")
a.set_ylabel(r"$F(E_\nu)$")
a.legend(loc="lower right")
ps.annotate(a, 3.6, 0.90, "circles: 5th percentile\nticks: $E_\\nu^{\\min}$",
            size=12.5, color="0.35")

# ---- right: distribution of the lowest detected energy ------------------
x = np.linspace(20, 130, 600)
pdf = np.exp(-0.5 * ((x - 69.) / 15.5)**2) * (1 + 0.35 * np.tanh((x - 69) / 40))
pdf /= pdf.max()

b.fill_between(x, 0, pdf, color=ps.GREY, alpha=0.25, lw=0)
b.plot(x, pdf, color=ps.C[0], lw=ps.LW_FAT, label=r"$N=1032$")
b.axvline(69., color=ps.C[2], lw=ps.LW_MAIN, ls=ps.DASH)
b.axvline(16.5, color="k", lw=ps.LW_THIN, ls=ps.DOT)

ps.annotate(b, 71, 0.80, r"$E_\nu^{\rm det}=69^{+23}_{-27}\,$keV", size=14.5,
            color=ps.C[2])
ps.annotate(b, 18.5, 0.42, r"$E_\nu^{\min}=17\,$keV", size=14.5, rotation=90,
            color="0.25")

b.set_xlim(10, 130)
b.set_ylim(0, 1.12)
b.set_xlabel(r"lowest detected $E_\nu$ [keV]")
b.set_ylabel("probability density [arb.]")
b.legend(loc="upper right")

fig.tight_layout()
ps.save(fig, "style_check.pdf")
ps.save(fig, "style_check.png", dpi=150)
print("ok")
