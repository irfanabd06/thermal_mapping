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
# Style matches the user's system diagram: grid paper, white boxes with dark-green
# borders, black arrows, green "framework" panel, Inter font.
DG = "#1e5631"        # box border
PANEL = "#4cd38f"     # framework panel fill
PANEL_EC = "#3b9a68"
PANEL_TXT = "#3f4a44"


def grid_bg(ax, w, h, step=0.55):
    x = 0.0
    while x <= w:
        ax.plot([x, x], [0, h], color="#efefef", lw=1.0, zorder=0)
        x += step
    y = 0.0
    while y <= h:
        ax.plot([0, w], [y, y], color="#efefef", lw=1.0, zorder=0)
        y += step


def flat_box(ax, x, y, w, h, title, body, tsize=13, bsize=11.5):
    ax.add_patch(Rectangle((x, y), w, h, fc="white", ec=DG, lw=1.8, zorder=3))
    ax.text(x + w / 2, y + h / 2 + 0.38, title, ha="center", va="center", fontsize=tsize,
            fontweight="bold", color="black", zorder=4)
    ax.text(x + w / 2, y + h / 2 - 0.3, body, ha="center", va="center", fontsize=bsize,
            color="black", linespacing=1.35, zorder=4)


def elbow(ax, pts, dashed=False):
    xs, ys = zip(*pts[:-1])
    ax.plot(list(xs) + [pts[-2][0]], list(ys) + [pts[-2][1]], color="black", lw=2.2,
            ls="--" if dashed else "-", zorder=2, solid_capstyle="round")
    ax.add_patch(FancyArrowPatch(pts[-2], pts[-1], arrowstyle="->,head_length=0.5,head_width=0.3",
                                 mutation_scale=18, color="black", lw=2.2,
                                 linestyle="--" if dashed else "-", zorder=2))


def problem_framing():
    with plt.rc_context({"font.family": "Inter"}):
        W, H = 17.0, 7.4
        fig, ax = canvas(W, H)
        # root cause and the two affected stages
        flat_box(ax, 0.3, 2.6, 3.4, 2.2, "Root Cause",
                 "Lack of spatially resolved\nthermal data and\nvalidated thermal models")
        flat_box(ax, 4.5, 4.4, 3.7, 2.2, "Design Stage",
                 "Fan number and placement\nchosen without evaluating\nairflow and heat distribution")
        flat_box(ax, 4.5, 0.8, 3.7, 2.2, "Operation Stage",
                 "Single monitoring point misses\ncrop-zone hotspots; fans\nrun 24/7 regardless of conditions")
        # proposed solution panel
        ax.add_patch(Rectangle((9.0, 0.25), 7.7, 6.9, fc=PANEL, ec=PANEL_EC, lw=1.8, zorder=1))
        ax.text(12.85, 6.72, "Proposed Solution: Thermal Digital Twin of GH1", ha="center",
                va="center", fontsize=14, fontweight="bold", color=PANEL_TXT, zorder=4)
        flat_box(ax, 9.35, 2.6, 2.6, 2.2, "Shared GH1 Model",
                 "Geometry, boundary\nconditions and\nsensor data", tsize=12.5)
        flat_box(ax, 12.55, 4.4, 3.85, 2.0, "Application 1: Design Evaluation",
                 "CFD and floor-fan tests compare\nfan number, placement, direction\nand speed (structure fixed)", tsize=12, bsize=11)
        flat_box(ax, 12.55, 0.6, 3.85, 2.2, "Application 2: Digital Twin",
                 "Sensors and soft sensors model\ntemperature and humidity; predicts\nwhen floor fans are needed", tsize=12, bsize=11)
        # arrows
        elbow(ax, [(3.7, 3.7), (4.1, 3.7), (4.1, 5.5), (4.5, 5.5)])
        elbow(ax, [(4.1, 3.7), (4.1, 1.9), (4.5, 1.9)])
        elbow(ax, [(8.2, 5.5), (8.7, 5.5), (8.7, 3.95), (9.35, 3.95)])
        elbow(ax, [(8.2, 1.9), (8.7, 1.9), (8.7, 3.45), (9.35, 3.45)])
        elbow(ax, [(11.95, 3.95), (12.25, 3.95), (12.25, 5.4), (12.55, 5.4)])
        elbow(ax, [(12.25, 3.95), (12.25, 1.7), (12.55, 1.7)])
        ax.add_patch(FancyArrowPatch((14.475, 4.4), (14.475, 2.8),
                                     arrowstyle="<->,head_length=0.5,head_width=0.3",
                                     mutation_scale=18, color="black", lw=2.2, linestyle="--", zorder=2))
        ax.text(14.65, 3.6, "Tested\ntogether;\nrecommended\nfan layout", fontsize=10.5,
                fontweight="bold", color="black", va="center", zorder=4)
        fig.savefig(OUT + "fig-problem-framing.png", dpi=150, bbox_inches="tight", facecolor="white")
        plt.close(fig)


# ---------------------------------------------------------------- D2 farmer desirability
VENN_COLOURS = {"Thermal\nperformance": "#4cd38f", "Low operating\ncost": "#4a90e2", "Crop value": "#f5a623"}


def farmer_value():
    """Figure 8: Venn diagram of the farmer's three factors."""
    from matplotlib.patches import Circle
    with plt.rc_context({"font.family": "Inter"}):
        fig = plt.figure(figsize=(8.0, 7.2))
        ax = fig.add_axes([0, 0, 1, 1]); ax.set_xlim(0, 8.0); ax.set_ylim(0, 7.2)
        ax.set_aspect("equal"); ax.axis("off")
        r = 1.9
        centres = {"Thermal\nperformance": (2.95, 4.35), "Low operating\ncost": (5.05, 4.35),
                   "Crop value": (4.0, 2.55)}
        label_pos = {"Thermal\nperformance": (2.25, 5.0), "Low operating\ncost": (5.75, 5.0),
                     "Crop value": (4.0, 1.55)}
        for name, (cx, cy) in centres.items():
            ax.add_patch(Circle((cx, cy), r, fc=VENN_COLOURS[name], alpha=0.45, ec="none", zorder=2))
            lx, ly = label_pos[name]
            ax.text(lx, ly, name, ha="center", va="center", fontsize=14, fontweight="bold",
                    color="black", zorder=4, linespacing=1.15)
        ax.text(4.0, 3.75, "Commercially\nviable", ha="center", va="center", fontsize=12.5,
                fontweight="bold", color="black", zorder=4, linespacing=1.1)
        fig.savefig(OUT + "fig-farmer-value.png", dpi=150, bbox_inches="tight", facecolor="white")
        plt.close(fig)


def cooling_options():
    """Figure 9: illustrative bubble chart of cooling options."""
    from matplotlib.patches import Circle
    with plt.rc_context({"font.family": "Inter"}):
        fig = plt.figure(figsize=(11.0, 7.6))
        ax2 = fig.add_axes([0, 0, 1, 1]); ax2.set_xlim(-1.15, 1.45); ax2.set_ylim(-1.12, 1.15)
        ax2.set_aspect("equal", adjustable="datalim"); ax2.axis("off")
        ax2.add_patch(FancyArrowPatch((-1.05, 0), (1.12, 0), arrowstyle="-|>", mutation_scale=18,
                                      color="black", lw=2.2, zorder=2))
        ax2.add_patch(FancyArrowPatch((0, -0.92), (0, 1.0), arrowstyle="-|>", mutation_scale=18,
                                      color="black", lw=2.2, zorder=2))
        ax2.text(1.15, 0.0, "Thermal\nperformance", ha="left", va="center", fontsize=13,
                 fontweight="bold", color="#11a85a")
        ax2.text(0.0, 1.07, "Operating cost", ha="center", va="center", fontsize=13,
                 fontweight="bold", color="#11a85a")
        # (x = thermal performance, y = operating cost, radius ~ crop value)
        bubbles = [
            ("Natural\nventilation", -0.78, -0.62, 0.17, "#1f0fa8"),
            ("Baseline\n(fans 24/7)", -0.12, 0.30, 0.22, "#5b6770"),
            ("Targeted\nfan control\n(aim)", 0.40, -0.18, 0.25, "#064d24"),
            ("Air-\nconditioning", 0.80, 0.72, 0.34, "#a80000"),
        ]
        for name, x, y, rr, c in bubbles:
            ax2.add_patch(Circle((x, y), rr, fc=c, ec="none", zorder=3))
            ax2.text(x, y, name, ha="center", va="center", fontsize=10.5 if rr < 0.2 else 11.5,
                     fontweight="bold", color="white", zorder=4, linespacing=1.1)
        ax2.add_patch(FancyArrowPatch((-0.02, 0.17), (0.20, -0.02), arrowstyle="->,head_length=0.5,head_width=0.3",
                                      mutation_scale=18, color="#064d24", lw=2.4, zorder=5))
        ax2.text(1.4, -1.08, "*Size denotes crop value. Positions are illustrative, not measured.",
                 ha="right", va="bottom", fontsize=10.5, fontweight="bold", color="#b71c1c")
        fig.savefig(OUT + "fig-cooling-options.png", dpi=150, bbox_inches="tight", facecolor="white")
        plt.close(fig)


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



# ---------------------------------------------------------------- 4.1 decompositions (Figure 7 style)
def functional_decomposition():
    """Figure 10: functions each objective requires, with the requirements that test them."""
    cols = [
        ("O1 Thermal\ncharacterisation", ["Measure temperature,\nhumidity and leaf\ntemperature at crop height",
                                           "Capture readings\nat the same time", "Clean the data",
                                           "Map the distribution", "Identify where and when\nhotspots occur"], "R1–R6"),
        ("O2 Cooling layout\nevaluation", ["Represent the greenhouse\nand its fans", "Estimate airflow",
                                           "Estimate heat\ndistribution",
                                           "Test fan configurations", "Compare with\nthe baseline"], "R7–R8"),
        ("O3 Targeted\ncooling", ["Forecast hotspots", "Decide the\ncooling action", "Operate the fans",
                                   "Check the response\nagainst the baseline"], "R9–R14"),
    ]
    with plt.rc_context({"font.family": "Inter"}):
        W, H = 15.0, 11.2
        fig, ax = canvas(W, H)
        ax.add_patch(Rectangle((0.3, 9.85), W - 0.6, 1.05, fc=PANEL, ec=PANEL_EC, lw=1.8, zorder=1))
        ax.text(W / 2, 10.375, "Make cooling more effective where heat builds up unevenly",
                ha="center", va="center", fontsize=15, fontweight="bold", color=PANEL_TXT)
        cw, gap = 4.4, 0.5
        x0 = (W - (3 * cw + 2 * gap)) / 2
        bh, step = 1.05, 1.42
        for k, (head, funcs, reqs) in enumerate(cols):
            x = x0 + k * (cw + gap)
            ax.add_patch(Rectangle((x, 8.25), cw, 1.2, fc="white", ec=DG, lw=2.4, zorder=3))
            ax.text(x + cw / 2, 8.85, head, ha="center", va="center", fontsize=13.5, fontweight="bold", zorder=4,
                    linespacing=1.1)
            elbow(ax, [(x + cw / 2, 9.85), (x + cw / 2, 9.45)])
            y = 8.25 - 0.35
            for f in funcs:
                ytop = y; yb = y - bh
                elbow(ax, [(x + cw / 2, ytop + 0.35), (x + cw / 2, ytop)])
                ax.add_patch(Rectangle((x + 0.25, yb), cw - 0.5, bh, fc="white", ec=DG, lw=1.6, zorder=3))
                ax.text(x + cw / 2, yb + bh / 2, f, ha="center", va="center", fontsize=11.5, zorder=4, linespacing=1.15)
                y = yb - (step - bh)
            ax.text(x + cw / 2, 0.45, "Tested by " + reqs, ha="center", va="center", fontsize=12,
                    fontweight="bold", color="#11a85a")
        fig.savefig(OUT + "fig-functional-decomposition.png", dpi=150, bbox_inches="tight", facecolor="white")
        plt.close(fig)


def system_decomposition():
    """Figure 11: what the functions act on - uncontrolled inputs, fixed equipment, the one lever, and the microclimate."""
    import matplotlib.image as mpimg
    photo = mpimg.imread(os.path.join(os.path.dirname(os.path.abspath(__file__)), "gh1-heat-paths.png"))
    with plt.rc_context({"font.family": "Inter"}):
        W, H = 20.0, 8.0
        fig, ax = canvas(W, H)

        def group(x, y, w, title, items, fill="white"):
            h = 0.62 + 0.52 * len(items)
            ax.add_patch(Rectangle((x, y - h), w, h, fc=fill, ec=DG, lw=1.8, zorder=3))
            ax.text(x + w / 2, y - 0.33, title, ha="center", va="center", fontsize=12.5, fontweight="bold", zorder=4)
            for i, it in enumerate(items):
                ax.text(x + w / 2, y - 0.85 - 0.52 * i, it, ha="center", va="center", fontsize=11.5, zorder=4)
            return y - h / 2

        c1 = group(0.3, 7.7, 4.2, "Uncontrolled inputs", ["Solar radiation", "Outside air and wind", "Crop transpiration"])
        c2 = group(0.3, 5.05, 4.2, "Fixed equipment", ["Structure and netting", "Shade nets", "Misting",
                                                      "Ventilation and ceiling fans"])
        c3 = group(0.3, 1.65, 4.2, "Adjustable", ["Floor-fan airflow"], fill=PANEL)
        # microclimate
        mx, my, mw, mh = 5.6, 2.4, 3.6, 3.6
        ax.add_patch(Rectangle((mx, my), mw, mh, fc="white", ec=DG, lw=2.4, zorder=3))
        ax.text(mx + mw / 2, my + mh - 0.4, "Crop-zone\nmicroclimate", ha="center", va="top", fontsize=13.5,
                fontweight="bold", zorder=4, linespacing=1.1)
        ax.text(mx + mw / 2, my + 1.75, "Measured directly:\nair temperature, humidity,\nleaf temperature",
                ha="center", va="center", fontsize=11, zorder=4, linespacing=1.2)
        ax.text(mx + mw / 2, my + 0.55, "Estimated: airflow", ha="center", va="center", fontsize=11,
                fontweight="bold", color="#b71c1c", zorder=4)
        for cy in (c1, c2, c3):
            elbow(ax, [(4.5, cy), (5.05, cy), (5.05, min(max(cy, my + 0.5), my + mh - 0.5)),
                       (mx, min(max(cy, my + 0.5), my + mh - 0.5))])
        # photo
        ph, pw = photo.shape[0], photo.shape[1]
        w_in = 10.0; h_in = w_in * ph / pw
        ax.imshow(photo, extent=(9.8, 9.8 + w_in, (H - h_in) / 2, (H - h_in) / 2 + h_in), zorder=2)
        ax.set_xlim(0, W); ax.set_ylim(0, H)
        fig.savefig(OUT + "fig-system-decomposition.png", dpi=150, bbox_inches="tight", facecolor="white")
        plt.close(fig)



def architecture_v2():
    """Figure 13: system architecture in the Figure 7 style (current design)."""
    with plt.rc_context({"font.family": "Inter"}):
        W, H = 17.0, 13.2
        fig, ax = canvas(W, H)

        def fbox(x, y, w, h, title, body, dashed=False, fill="white", ts=12.5, bs=10.8):
            ax.add_patch(Rectangle((x, y), w, h, fc=fill, ec=DG, lw=1.8, ls="--" if dashed else "-", zorder=3))
            ax.text(x + w / 2, y + h - 0.38, title, ha="center", va="center", fontsize=ts, fontweight="bold", zorder=4)
            ax.text(x + w / 2, y + (h - 0.55) / 2, body, ha="center", va="center", fontsize=bs, zorder=4,
                    linespacing=1.25)

        def dline(pts, label=None, lpos=None, dashed=False):
            elbow(ax, pts, dashed=dashed)
            if label:
                ax.text(lpos[0], lpos[1], label, fontsize=10, fontweight="bold", color="#11a85a", ha="center",
                        va="center", zorder=5, bbox=dict(fc="white", ec="none", pad=1.5))

        fbox(5.5, 11.5, 6.0, 1.4, "Physical greenhouse (GH1)", "Sun, wind and crops · fixed equipment · floor fans")
        fbox(5.5, 9.4, 6.0, 1.6, "S1 Sense", "Permanent and temporary nodes · temperature, humidity,\ncanopy temperature · 1-min synchronised sampling")
        fbox(12.6, 9.4, 4.0, 1.6, "Weather data", "NEA live readings and\n2-hour nowcast (when online)", dashed=True)
        # S2 live panel
        ax.add_patch(Rectangle((1.0, 5.55), 15.6, 3.3, fc=PANEL, ec=PANEL_EC, lw=1.8, zorder=1))
        ax.text(8.8, 8.5, "S2 Map & Model: on-site edge computer (Raspberry Pi 5)", ha="center", va="center",
                fontsize=13.5, fontweight="bold", color=PANEL_TXT, zorder=4)
        fbox(1.4, 6.0, 4.4, 1.75, "Clean data", "Remove spikes and\nmisting artefacts")
        fbox(6.6, 6.0, 4.4, 1.75, "Thermal map", "Soft sensors and Gaussian\nprocess regression")
        fbox(11.8, 6.0, 4.4, 1.75, "Hotspot prediction", "Crop-zone exceedance\n30 min ahead")
        dline([(5.8, 6.875), (6.6, 6.875)])
        dline([(11.0, 6.875), (11.8, 6.875)])
        # offline CFD, decide, actuate, dashboard
        fbox(1.0, 1.2, 4.4, 2.7, "S2 Offline CFD", "Airflow, and heat for\nuntested layouts;\nfan-layout ranking")
        fbox(6.4, 3.35, 4.8, 1.45, "S3 Decide", "Prediction-triggered rules, fail-safe")
        fbox(6.4, 1.2, 4.8, 1.45, "S4 Actuate", "Four floor fans, energy metering")
        fbox(12.2, 3.35, 4.4, 1.45, "Dashboard", "Map, hotspots, fan status")
        # flows
        dline([(8.5, 11.5), (8.5, 11.0)])
        dline([(8.5, 9.4), (8.5, 9.15), (3.6, 9.15), (3.6, 7.75)])
        dline([(14.6, 9.4), (14.6, 7.75)], dashed=True)
        dline([(12.6, 6.0), (12.6, 5.25), (8.8, 5.25), (8.8, 4.8)])
        dline([(15.2, 6.0), (15.2, 4.8)])
        dline([(8.8, 3.35), (8.8, 2.65)])
        dline([(3.2, 6.0), (3.2, 3.9)], "test-section\ndata", (4.35, 4.75), dashed=True)
        dline([(5.4, 1.9), (6.4, 1.9)], dashed=True)
        ax.text(5.9, 2.25, "fan\nlayout", fontsize=9.5, fontweight="bold", color="#11a85a", ha="center", va="bottom")
        dline([(5.4, 3.6), (6.4, 3.6)], dashed=True)
        ax.text(5.9, 3.85, "fan\ninfluence", fontsize=9.5, fontweight="bold", color="#11a85a", ha="center", va="bottom")
        # feedback loop
        ax.plot([8.8, 8.8, 0.35, 0.35, 5.2], [1.2, 0.55, 0.55, 12.2, 12.2], color="black", lw=2.2, zorder=2)
        ax.add_patch(FancyArrowPatch((5.2, 12.2), (5.5, 12.2), arrowstyle="->,head_length=0.5,head_width=0.3",
                                     mutation_scale=18, color="black", lw=2.2, zorder=2))
        ax.text(0.6, 6.9, "Feedback", rotation=90, fontsize=12, fontweight="bold", ha="left", va="center")
        ax.set_xlim(0, W); ax.set_ylim(0, H)
        fig.savefig(OUT + "fig-system-architecture.png", dpi=150, bbox_inches="tight", facecolor="white")
        plt.close(fig)

problem_framing()
farmer_value()
cooling_options()
functional_decomposition()
system_decomposition()
architecture_v2()
trapped_hot_air()
roadmap()
print("done")
