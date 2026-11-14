"""Report diagrams (Figures 7, 8, 11, 12, 18). Run: python3 tools/diagrams/report_diagrams.py"""
import datetime as dt

import matplotlib
matplotlib.use("Agg")
import matplotlib.dates as mdates
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch, Polygon, Rectangle

import os
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "docs", "assets", "")
GREEN = "#1b5e20"
LGREEN = "#e8f5e9"
AMBER = "#f9a825"
LAMBER = "#fff8e1"
RED = "#c62828"
LRED = "#fdecea"
BLUE = "#1565c0"
LBLUE = "#e3f2fd"
GREY = "#455a64"
LGREY = "#eceff1"
plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 11})


def box(ax, x, y, w, h, text, fc, ec, size=10.5, bold_first=True, weight=None):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.02,rounding_size=0.12",
                                fc=fc, ec=ec, lw=1.6))
    lines = text.split("\n")
    if bold_first and len(lines) > 1:
        ax.text(x + w / 2, y + h - 0.22, lines[0], ha="center", va="top", fontsize=size + 0.5,
                fontweight="bold", color=ec)
        ax.text(x + w / 2, y + (h - 0.45) / 2, "\n".join(lines[1:]), ha="center", va="center",
                fontsize=size - 0.5, color="#212121", linespacing=1.35)
    else:
        ax.text(x + w / 2, y + h / 2, text, ha="center", va="center", fontsize=size,
                color=ec, fontweight=weight or "bold", linespacing=1.3)


def arrow(ax, p0, p1, color=GREY, style="-|>", ls="-", lw=1.8, rad=0.0):
    ax.add_patch(FancyArrowPatch(p0, p1, arrowstyle=style, mutation_scale=16, color=color,
                                 lw=lw, linestyle=ls, connectionstyle=f"arc3,rad={rad}"))


def canvas(w, h):
    fig, ax = plt.subplots(figsize=(w, h))
    ax.set_xlim(0, w)
    ax.set_ylim(0, h)
    ax.axis("off")
    return fig, ax


# ---------------------------------------------------------------- D1 problem framing
def problem_framing():
    fig, ax = canvas(15, 6.2)
    box(ax, 0.2, 2.0, 2.8, 2.2, "Root cause\nLack of spatially resolved\nthermal data and validated\nthermal models", LRED, RED)
    box(ax, 3.8, 3.5, 3.3, 2.2, "Design stage\nFan number and placement\nchosen without evaluating\nairflow and heat distribution", LAMBER, "#e65100")
    box(ax, 3.8, 0.5, 3.3, 2.2, "Operation stage\nSingle monitoring point misses\ncrop-zone hotspots; fans run\n24/7 regardless of conditions", LAMBER, "#e65100")
    box(ax, 7.9, 2.0, 2.4, 2.2, "Shared GH1 model\nGeometry, boundary\nconditions and\nsensor data", LGREY, GREY)
    box(ax, 11.1, 3.5, 3.7, 2.2, "Application 1: Design evaluation\nOffline CFD compares fan number,\nposition, orientation and speed\n(structure fixed)", LBLUE, BLUE)
    box(ax, 11.1, 0.5, 3.7, 2.2, "Application 2: Digital twin\nLive sensor grid, thermal map,\ncrop-zone hotspot control\nand dashboard", LGREEN, GREEN)
    arrow(ax, (3.0, 3.4), (3.8, 4.4))
    arrow(ax, (3.0, 2.8), (3.8, 1.8))
    arrow(ax, (7.1, 4.4), (7.9, 3.6))
    arrow(ax, (7.1, 1.6), (7.9, 2.6))
    arrow(ax, (10.3, 3.6), (11.1, 4.4))
    arrow(ax, (10.3, 2.6), (11.1, 1.6))
    arrow(ax, (12.95, 3.5), (12.95, 2.7), color=BLUE, ls="--")
    ax.text(13.05, 3.1, "recommended\nfan layout", fontsize=9, color=BLUE, va="center")
    fig.savefig(OUT + "fig-problem-framing.png", dpi=130, bbox_inches="tight", facecolor="white")


# ---------------------------------------------------------------- D2 farmer desirability
def farmer_value():
    fig = plt.figure(figsize=(15, 6.2))
    ax = fig.add_axes([0.0, 0.0, 0.56, 1.0])
    ax.set_xlim(0, 8.4)
    ax.set_ylim(0, 6.2)
    ax.axis("off")
    box(ax, 0.1, 3.7, 2.6, 2.2, "Thermal performance\nReduce crop-zone\nhotspots and\nheat stress", LGREEN, GREEN, size=13)
    box(ax, 2.9, 3.7, 2.6, 2.2, "Operating cost\nFan energy,\nmaintenance and\ncooling hardware", LRED, RED, size=13)
    box(ax, 5.7, 3.7, 2.6, 2.2, "Crop value\nMarketable yield,\nquality and\nconsistency", LAMBER, "#e65100", size=13)
    box(ax, 1.5, 0.4, 5.4, 2.0, "Commercial viability\nCrop value gained, minus the cost\nof cooling and operating the greenhouse", LGREY, GREY, size=13)
    for x in (1.4, 4.2, 7.0):
        arrow(ax, (x, 3.7), (4.2 + (x - 4.2) * 0.45, 2.4))
    ax.text(4.2, 3.05, "balance, not maximise any one", ha="center", fontsize=12, style="italic", color=GREY)

    ax2 = fig.add_axes([0.62, 0.14, 0.36, 0.76])
    import numpy as np
    e = np.linspace(0.05, 1.0, 200)
    ax2.plot(e, 0.08 + 0.9 * np.exp(-3.2 * e), color=GREY, lw=2)
    pts = {"Baseline\n(fans 24/7)": (0.42, 0.08 + 0.9 * np.exp(-3.2 * 0.42) + 0.17),
           "Targeted fan\ncontrol (aim)": (0.30, 0.08 + 0.9 * np.exp(-3.2 * 0.30)),
           "Air-conditioning\n(not viable)": (0.95, 0.08 + 0.9 * np.exp(-3.2 * 0.95))}
    colors = [RED, GREEN, GREY]
    offs = [(0.06, 0.06), (-0.02, -0.17), (-0.32, 0.12)]
    for (k, (x, y)), c, (dx, dy) in zip(pts.items(), colors, offs):
        ax2.scatter([x], [y], s=110, color=c, zorder=3, edgecolor="white", lw=1.5)
        ax2.text(x + dx, y + dy, k, fontsize=9.5, color=c, fontweight="bold")
    arrow(ax2, (0.42, pts["Baseline\n(fans 24/7)"][1] - 0.03), (0.32, pts["Targeted fan\ncontrol (aim)"][1] + 0.04), color=GREEN)
    ax2.set_xlabel("Cooling energy and operating cost  →", fontsize=10.5)
    ax2.set_ylabel("Crop-zone hotspot exceedance  →", fontsize=10.5)
    ax2.set_xticks([])
    ax2.set_yticks([])
    ax2.set_xlim(0, 1.1)
    ax2.set_ylim(0, 1.05)
    for s in ("top", "right"):
        ax2.spines[s].set_visible(False)
    ax2.set_title("Conceptual trade-off (illustrative, not measured)", fontsize=10.5, color=GREY)
    fig.savefig(OUT + "fig-farmer-value.png", dpi=130, bbox_inches="tight", facecolor="white")


# ---------------------------------------------------------------- D3 architecture
def architecture():
    fig, ax = canvas(15, 7.2)
    ax.set_ylim(-1.0, 7.3)
    box(ax, 0.2, 2.6, 2.4, 2.0, "Physical GH1\nCrops, cooling\nequipment, weather", LGREY, GREY)
    box(ax, 3.3, 2.6, 2.4, 2.0, "S1 Sense\nT/RH + canopy\nthermal nodes,\nRS-485 to gateway", LGREEN, GREEN)
    ax.add_patch(FancyBboxPatch((6.3, 1.0), 4.3, 5.4, boxstyle="round,pad=0.02,rounding_size=0.15",
                                fc="#f5f9ff", ec=BLUE, lw=1.6, ls="--"))
    ax.text(6.55, 6.1, "S2 Map & Model", ha="left", fontsize=12, fontweight="bold", color=BLUE)
    box(ax, 6.55, 3.9, 3.8, 1.8, "Live digital twin (edge)\nThermal map with uncertainty,\ncrop-zone hotspot index", LBLUE, BLUE)
    box(ax, 6.55, 1.3, 3.8, 1.8, "CFD evaluation (offline)\nBaseline model and fan\nconfiguration comparison", LBLUE, BLUE)
    box(ax, 11.3, 3.9, 3.5, 1.8, "S3 Decide\nCrop-aware hotspot\ncontrol, fail-safe rules", LAMBER, "#e65100")
    box(ax, 11.3, 1.3, 3.5, 1.8, "S4 Actuate\nProcured floor\ncirculation fans", LRED, RED)
    box(ax, 5.9, 6.65, 5.1, 0.55, "Dashboard: thermal map, hotspots, fan status", LGREY, GREY, size=10.5)
    arrow(ax, (2.6, 3.6), (3.3, 3.6))
    arrow(ax, (5.7, 3.9), (6.55, 4.6))
    arrow(ax, (5.7, 3.2), (6.55, 2.3), ls="--")
    ax.text(5.75, 1.95, "validation\ndata", fontsize=9, color=GREY, ha="left")
    arrow(ax, (10.35, 4.8), (11.3, 4.8))
    arrow(ax, (13.05, 3.9), (13.05, 3.1))
    arrow(ax, (10.35, 2.2), (11.3, 2.2), color=BLUE, ls="--")
    ax.text(10.82, 2.4, "fan\nlayout", fontsize=9, color=BLUE, ha="center")
    arrow(ax, (8.45, 5.7), (8.45, 6.65))
    arrow(ax, (13.05, 1.3), (1.4, 2.6), rad=-0.32, color=GREEN)
    ax.text(7.2, -0.75, "Feedback: fan operation changes greenhouse conditions, measured again by S1",
            ha="center", fontsize=9.5, color=GREEN)
    fig.savefig(OUT + "fig-system-architecture.png", dpi=130, bbox_inches="tight", facecolor="white")


# ---------------------------------------------------------------- D4 trapped hot air
def trapped_hot_air():
    fig, ax = plt.subplots(figsize=(14, 6.4))
    ax.set_xlim(-1.2, 19.5)
    ax.set_ylim(-0.6, 6.2)
    ax.set_aspect("equal")
    ax.axis("off")
    W, H, P = 12.5, 3.0, 4.35
    shell = [(0, 0), (0, H), (W / 2, P), (W, H), (W, 0)]
    import numpy as np
    from matplotlib.colors import LinearSegmentedColormap
    cmap = LinearSegmentedColormap.from_list("t", ["#90caf9", "#fff59d", "#ef6c00", "#c62828"])
    grad = np.linspace(0, 1, 100).reshape(-1, 1) ** 1.8
    im = ax.imshow(grad, extent=(0, W, 0, P), origin="lower", cmap=cmap, alpha=0.55, aspect="auto")
    im.set_clip_path(Polygon(shell, closed=True, transform=ax.transData))
    ax.add_patch(Polygon(shell, closed=True, fill=False, ec="#37474f", lw=2.2))
    for x0 in (1.0, 4.6, 8.2):
        ax.add_patch(Rectangle((x0, 0.75), 3.0, 0.12, color="#78909c"))
        for k in range(7):
            ax.add_patch(plt.Circle((x0 + 0.25 + k * 0.42, 1.0), 0.17, color="#43a047"))
    ax.text(W / 2, 1.45, "crop canopy (~1 m)", ha="center", fontsize=10, color="#2e7d32", fontweight="bold")
    ax.text(W / 2, 3.45, "warm air trapped\nunder the roof", ha="center", fontsize=11, color="#b71c1c",
            fontweight="bold")
    # option A: roof vent (out of scope)
    ax.add_patch(Rectangle((W / 2 - 0.5, P - 0.05), 1.0, 0.18, color="#9e9e9e"))
    arrow(ax, (W / 2, P + 0.1), (W / 2, P + 1.0), color="#9e9e9e")
    for (tx, ty, t, c) in ((W / 2 - 0.9, P + 0.55, "A", "#9e9e9e"), (W - 0.75, 3.15, "B", BLUE), (1.95, 2.75, "C", GREEN)):
        ax.add_patch(plt.Circle((tx, ty), 0.28, color=c))
        ax.text(tx, ty, t, ha="center", va="center", color="white", fontsize=10, fontweight="bold")
    ax.text(W + 1.4, 3.9, "A  Roof vent: releases warm air by buoyancy\n    (changes structure: outside scope)",
            fontsize=10, color="#616161", va="center")
    # option B: extraction fan high on end wall
    ax.add_patch(Rectangle((W - 0.12, 2.1), 0.24, 0.7, color=BLUE))
    arrow(ax, (W - 1.6, 2.45), (W + 1.0, 2.45), color=BLUE)
    ax.text(W + 1.4, 2.6, "B  Extraction fan: removes heat only if\n    replacement air can enter lower down",
            fontsize=10, color=BLUE, va="center")
    arrow(ax, (-1.0, 0.45), (0.6, 0.45), color=BLUE, ls="--")
    ax.text(-1.0, 0.75, "inlet air", fontsize=9, color=BLUE)
    # option C: circulation fan mixing
    ax.add_patch(Rectangle((2.3, 1.95), 0.5, 0.5, color=GREEN))
    arrow(ax, (2.8, 2.2), (5.5, 2.9), color=GREEN, rad=-0.25)
    arrow(ax, (5.5, 2.9), (5.0, 1.55), color=GREEN, rad=-0.3)
    ax.text(W + 1.4, 1.1, "C  Circulation fan: breaks up stagnant air,\n    but may push warm air down to the crops",
            fontsize=10, color=GREEN, va="center")
    ax.text(W / 2 + 3.6, -0.45, "Criterion: does the configuration improve crop-zone conditions without unnecessary fan energy?",
            ha="center", fontsize=10.5, style="italic", color="#37474f")
    fig.savefig(OUT + "fig-trapped-hot-air.png", dpi=130, bbox_inches="tight", facecolor="white")


# ---------------------------------------------------------------- D5 roadmap
def roadmap():
    d = dt.date
    tasks = [
        ("Sensing & deployment", "Sensor-node fabrication", d(2026, 11, 16), d(2026, 12, 31)),
        ("Sensing & deployment", "Installation and commissioning", d(2026, 12, 14), d(2027, 1, 22)),
        ("Sensing & deployment", "Durability test and data collection", d(2027, 1, 4), d(2027, 3, 31)),
        ("Digital twin & simulation", "GH1 3D model", d(2026, 11, 16), d(2026, 12, 18)),
        ("Digital twin & simulation", "CFD baseline set-up and calibration", d(2026, 12, 7), d(2027, 1, 31)),
        ("Digital twin & simulation", "Fan configuration study", d(2027, 1, 11), d(2027, 2, 21)),
        ("Control & decision-making", "Hotspot index and control logic", d(2027, 1, 18), d(2027, 2, 28)),
        ("Control & decision-making", "Edge integration and dashboard", d(2027, 2, 8), d(2027, 3, 14)),
        ("Actuation & validation", "Fan procurement and integration", d(2027, 1, 25), d(2027, 3, 7)),
        ("Actuation & validation", "Baseline vs proposed trials", d(2027, 3, 1), d(2027, 4, 11)),
    ]
    milestones = [
        (d(2026, 12, 31), "M1"), (d(2027, 1, 31), "M2"), (d(2027, 2, 21), "M3"),
        (d(2027, 3, 14), "M4"), (d(2027, 4, 11), "M5"),
    ]
    colors = {"Sensing & deployment": GREEN, "Digital twin & simulation": BLUE,
              "Control & decision-making": "#e65100", "Actuation & validation": RED}
    fig, ax = plt.subplots(figsize=(14, 5.8))
    for i, (grp, name, s, e) in enumerate(tasks):
        y = len(tasks) - i
        ax.barh(y, (e - s).days, left=mdates.date2num(s), height=0.55, color=colors[grp], alpha=0.85)
        ax.text(mdates.date2num(d(2026, 11, 9)), y, name, ha="right", va="center", fontsize=10)
    for m, lab in milestones:
        x = mdates.date2num(m)
        ax.axvline(x, color="#9e9e9e", lw=0.8, ls=":")
        ax.scatter([x], [len(tasks) + 0.95], marker="D", s=70, color="#212121", zorder=3)
        ax.text(x, len(tasks) + 1.45, lab, ha="center", fontsize=10, fontweight="bold")
    ax.set_ylim(0.3, len(tasks) + 2.0)
    ax.set_xlim(mdates.date2num(d(2026, 11, 9)), mdates.date2num(d(2027, 4, 30)))
    ax.xaxis.set_major_locator(mdates.MonthLocator())
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%b %Y"))
    ax.set_yticks([])
    for s in ("top", "right", "left"):
        ax.spines[s].set_visible(False)
    handles = [Rectangle((0, 0), 1, 1, color=c) for c in colors.values()]
    ax.legend(handles, colors.keys(), loc="lower center", bbox_to_anchor=(0.5, -0.22), ncol=4, frameon=False)
    fig.savefig(OUT + "fig-roadmap.png", dpi=130, bbox_inches="tight", facecolor="white")


problem_framing()
farmer_value()
architecture()
trapped_hot_air()
roadmap()
print("done")
