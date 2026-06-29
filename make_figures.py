#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Generowanie wykresów p-t i x-t z danych sond (eksport ParaView).
Uzyty do wygenerowania assets/fig_pt.pdf i assets/fig_xt.pdf w raporcie
raport_detonacja.pdf.

Wymaga pliku z sondami `p_combined_probes.csv` (eksport ParaView) w katalogu
roboczym. Uruchamiac w kontenerze `cantera` (ma matplotlib):
    python make_figures.py
"""
import csv
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

CSV = "p_combined_probes.csv"

# Wspolrzedne x sond osiowych + klin
X = {1: 1.096, 2: 1.346, 3: 1.594, 4: 1.722, 5: 1.846, 6: 1.92718}

# --- wczytanie danych ---
with open(CSV, newline="") as f:
    rows = [r for r in csv.reader(f)][1:]
data = np.array([r for r in rows if r and r[0].strip()], dtype=float)
t = data[:, 0] * 1e3        # czas [ms]
P = {i: data[:, i] for i in range(1, 7)}

plt.rcParams.update({
    "font.size": 11,
    "font.family": "serif",
    "axes.grid": True,
    "grid.alpha": 0.3,
    "figure.dpi": 140,
})

# ============================================================
# Fig 1: przebiegi p-t
# ============================================================
fig, ax = plt.subplots(figsize=(6.3, 3.8))

cols = {2: "#1b9e77", 3: "#7570b3", 4: "#d95f02", 5: "#e7298a", 6: "#1f78b4"}
for i in [2, 3, 4, 5, 6]:
    ax.semilogy(t, P[i] / 1e5, lw=1.1, color=cols[i],
                label=f"sonda {i} (x={X[i]:.3f} m)")

ax.axhline(2.54, ls="--", lw=0.8, color="0.4")
ax.text(0.18, 2.7,
        r"plateau za falą padającą ($P_2\approx2{,}5$ bar)",
        fontsize=8, color="0.3")

ax.set_xlabel("czas [ms]")
ax.set_ylabel("ciśnienie [bar]")
ax.set_xlim(0, 1.3)
ax.set_ylim(0.8, 200)
ax.legend(fontsize=8, loc="upper left", framealpha=0.9)
fig.tight_layout()
fig.savefig("assets/fig_pt.pdf")
plt.close(fig)
print("Zapisano assets/fig_pt.pdf")

# ============================================================
# Fig 2: diagram x-t
# ============================================================
def first_rise(p, dp=30000.0):
    """Czas pierwszego narastania cisnienia o dp [Pa] ponad baseline."""
    base = np.median(p[:200])
    idx = np.where(p >= base + dp)[0]
    return t[idx[0]] if len(idx) else None

def t_peak(p):
    """Czas szczytu cisnienia."""
    return t[np.argmax(p)]

# Fala padajaca: pierwsze narastanie, sondy 2-5
inc_t = [first_rise(P[i]) for i in [2, 3, 4, 5]]
inc_x = [X[i] for i in [2, 3, 4, 5]]

# Detonacja: czas piku, klin(6)->5->4
det_t = [t_peak(P[i]) for i in [6, 5, 4]]
det_x = [X[i] for i in [6, 5, 4]]

fig, ax = plt.subplots(figsize=(6.3, 3.8))

ax.plot(inc_t, inc_x, "o", color="#1b9e77", ms=6,
        label="fala padająca (pierwsze narastanie)")
ax.plot(det_t, det_x, "s", color="#d95f02", ms=6,
        label="detonacja (czas piku)")

# dopasowanie liniowe i predkosci
ci = np.polyfit(inc_t, inc_x, 1);  W = ci[0] * 1e3   # m/s
cd = np.polyfit(det_t, det_x, 1);  D = abs(cd[0]) * 1e3

tt  = np.linspace(0, 1.1, 10)
tt2 = np.linspace(1.0, 1.25, 10)
ax.plot(tt,  np.polyval(ci, tt),  "-", color="#1b9e77", lw=1)
ax.plot(tt2, np.polyval(cd, tt2), "-", color="#d95f02",  lw=1)

ax.text(0.45, 1.45, f"$W\\approx{W:.0f}$ m/s", color="#1b9e77", fontsize=10)
ax.text(1.02, 1.80, f"$D\\approx{D:.0f}$ m/s", color="#d95f02",  fontsize=10)

ax.set_xlabel("czas [ms]")
ax.set_ylabel("położenie x [m]")
ax.set_xlim(0, 1.3)
ax.legend(fontsize=8, loc="lower right", framealpha=0.9)
fig.tight_layout()
fig.savefig("assets/fig_xt.pdf")
plt.close(fig)
print(f"Zapisano assets/fig_xt.pdf  |  W_fit={W:.0f} m/s  D_fit={D:.0f} m/s")
