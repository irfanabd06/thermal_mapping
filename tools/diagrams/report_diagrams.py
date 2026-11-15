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
                 "CFD suggests fan layouts for new\nor retrofitted greenhouses; real-life\ntests confirm the improvement", tsize=12, bsize=11)
        flat_box(ax, 12.55, 0.6, 3.85, 2.2, "Application 2: Digital Twin",
                 "Sensors and soft sensors monitor\ntemperature and humidity, predict\nhotspots and run the right fans", tsize=12, bsize=11)
        # arrows
        elbow(ax, [(3.7, 3.7), (4.1, 3.7), (4.1, 5.5), (4.5, 5.5)])
        elbow(ax, [(4.1, 3.7), (4.1, 1.9), (4.5, 1.9)])
        elbow(ax, [(8.2, 5.5), (8.7, 5.5), (8.7, 3.95), (9.35, 3.95)])
        elbow(ax, [(8.2, 1.9), (8.7, 1.9), (8.7, 3.45), (9.35, 3.45)])
        elbow(ax, [(11.95, 3.95), (12.25, 3.95), (12.25, 5.4), (12.55, 5.4)])
        elbow(ax, [(12.25, 3.95), (12.25, 1.7), (12.55, 1.7)])
        ax.add_patch(FancyArrowPatch((14.475, 4.4), (14.475, 2.8),
                                     arrowstyle="->,head_length=0.5,head_width=0.3",
                                     mutation_scale=18, color="black", lw=2.2, linestyle="--", zorder=2))
        ax.text(14.65, 3.6, "Chosen\nfan layout", fontsize=10.5,
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
                                           "Suggest the best\nfan layouts", "Test suggested layouts\nagainst the baseline"], "R7–R8"),
        ("O3 Targeted\ncooling", ["Forecast hotspots", "Decide the\ncooling action", "Operate the fans",
                                   "Confirm the right\nfans respond"], "R9–R14"),
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
    """Figure 13: system architecture in the Figure 7 style, with the two applications inside S2."""
    with plt.rc_context({"font.family": "Inter"}):
        W, H = 17.0, 15.2
        fig, ax = canvas(W, H)
        LIGHT = "#c9f1db"

        def fbox(x, y, w, h, title, body, dashed=False, fill="white", ts=15.5, bs=13.5):
            ax.add_patch(Rectangle((x, y), w, h, fc=fill, ec=DG, lw=1.8, ls="--" if dashed else "-", zorder=3))
            ax.text(x + w / 2, y + h - 0.38, title, ha="center", va="center", fontsize=ts, fontweight="bold", zorder=4)
            ax.text(x + w / 2, y + (h - 0.55) / 2, body, ha="center", va="center", fontsize=bs, zorder=4,
                    linespacing=1.25)

        def dline(pts, label=None, lpos=None, dashed=False, two_way=False):
            elbow(ax, pts, dashed=dashed)
            if two_way:
                ax.add_patch(FancyArrowPatch(pts[1], pts[0], arrowstyle="->,head_length=0.5,head_width=0.3",
                                             mutation_scale=18, color="black", lw=2.2, linestyle="--", zorder=2))
            if label:
                ax.text(lpos[0], lpos[1], label, fontsize=12.5, fontweight="bold", color="#11a85a", ha="center",
                        va="center", zorder=5, bbox=dict(fc="white", ec="none", pad=1.5))

        fbox(5.5, 13.5, 6.0, 1.4, "Physical greenhouse (GH1)", "Sun, wind, crops · fixed equipment · floor fans")
        fbox(5.5, 11.4, 6.0, 1.6, "S1 Sense", "Permanent and temporary nodes\nT, RH, canopy temperature · 1-min sampling")
        fbox(12.6, 11.4, 4.0, 1.6, "Weather data", "NEA live readings and\n2-hour nowcast (when online)", dashed=True)

        # S2 panel with the two applications
        ax.add_patch(Rectangle((1.0, 4.6), 15.6, 6.35, fc=PANEL, ec=PANEL_EC, lw=1.8, zorder=1))
        ax.text(8.8, 10.6, "S2 Map and Model", ha="center", va="center", fontsize=17, fontweight="bold",
                color=PANEL_TXT, zorder=4)
        ax.add_patch(Rectangle((1.2, 7.85), 15.2, 2.4, fc=LIGHT, ec=PANEL_EC, lw=1.4, zorder=2))
        ax.text(8.8, 9.95, "Application 2: live data-driven twin (on-site, Raspberry Pi 5)", ha="center",
                va="center", fontsize=13, fontweight="bold", color=PANEL_TXT, zorder=4)
        fbox(1.4, 8.05, 4.4, 1.6, "Clean data", "Remove spikes and\nmisting artefacts")
        fbox(6.6, 8.05, 4.4, 1.6, "Thermal map", "Soft sensors and Gaussian\nprocess regression")
        fbox(11.8, 8.05, 4.4, 1.6, "Hotspot prediction", "Exceedance 30 min ahead;\nlearned fan effects on T, RH")
        dline([(5.8, 8.85), (6.6, 8.85)])
        dline([(11.0, 8.85), (11.8, 8.85)])
        ax.add_patch(Rectangle((1.2, 4.8), 15.2, 2.85, fc=LIGHT, ec=PANEL_EC, lw=1.4, zorder=2))
        ax.text(8.8, 5.12, "Application 1: cooling layout evaluation (offline, design stage)", ha="center", va="center",
                fontsize=13, fontweight="bold", color=PANEL_TXT, zorder=4)
        fbox(1.4, 5.45, 4.8, 1.95, "Flow simulation (CFD)", "Airflow and heat for candidate\nlayouts; suggests the best")
        fbox(7.4, 5.45, 4.4, 1.95, "Layout tests", "Suggested layouts built with\nfloor fans; temperature vs baseline")
        dline([(6.2, 6.4), (7.4, 6.4)], dashed=True)
        ax.text(6.8, 6.8, "suggested\nlayouts", fontsize=11.5, fontweight="bold", color="#11a85a", ha="center", va="bottom", zorder=5)

        # flows
        dline([(8.5, 13.5), (8.5, 13.0)])
        dline([(8.5, 11.4), (8.5, 11.15), (3.6, 11.15), (3.6, 9.65)])
        dline([(14.6, 11.4), (14.6, 9.65)], dashed=True)
        dline([(9.6, 8.05), (9.6, 7.4)], "measured\ntemperature", (8.4, 7.72), dashed=True)
        # outputs below S2
        fbox(6.4, 2.5, 4.8, 1.45, "S3 Decide", "Right fans for each hotspot, fail-safe")
        fbox(6.4, 0.5, 4.8, 1.45, "S4 Actuate", "Four floor fans, energy metering")
        fbox(12.2, 2.5, 4.4, 1.45, "Dashboard", "Map, hotspots, fan status")
        dline([(13.0, 8.05), (13.0, 4.3), (8.8, 4.3), (8.8, 3.95)])
        dline([(15.2, 8.05), (15.2, 3.95)])
        dline([(8.8, 2.5), (8.8, 1.95)])
        dline([(2.0, 5.45), (2.0, 1.2), (6.4, 1.2)], dashed=True)
        ax.text(4.2, 1.45, "chosen fan layout", fontsize=12, fontweight="bold", color="#11a85a", ha="center", va="bottom")
        # feedback loop
        ax.plot([8.8, 8.8, 0.35, 0.35, 5.2], [0.5, 0.15, 0.15, 14.2, 14.2], color="black", lw=2.2, zorder=2)
        ax.add_patch(FancyArrowPatch((5.2, 14.2), (5.5, 14.2), arrowstyle="->,head_length=0.5,head_width=0.3",
                                     mutation_scale=18, color="black", lw=2.2, zorder=2))
        ax.text(0.6, 12.6, "Feedback", rotation=90, fontsize=15, fontweight="bold", ha="left", va="center")
        ax.set_xlim(0, W); ax.set_ylim(0, H)
        fig.savefig(OUT + "fig-system-architecture.png", dpi=150, bbox_inches="tight", pad_inches=0.05, facecolor="white")
        plt.close(fig)


def architecture_v3():
    """Figure 13: three subsystems aligned with O1-O3 (S1 Sense and Map, S2 = Application 1, S3 = Application 2)."""
    with plt.rc_context({"font.family": "Inter"}):
        W, H = 17.0, 15.2
        fig, ax = canvas(W, H)

        def fbox(x, y, w, h, title, body, dashed=False, ts=15.5, bs=13.5):
            ax.add_patch(Rectangle((x, y), w, h, fc="white", ec=DG, lw=1.8, ls="--" if dashed else "-", zorder=3))
            ax.text(x + w / 2, y + h - 0.4, title, ha="center", va="center", fontsize=ts, fontweight="bold", zorder=4)
            ax.text(x + w / 2, y + (h - 0.6) / 2, body, ha="center", va="center", fontsize=bs, zorder=4,
                    linespacing=1.25)

        def panel(x, y, w, h, title, sub=None):
            ax.add_patch(Rectangle((x, y), w, h, fc=PANEL, ec=PANEL_EC, lw=1.8, zorder=1))
            ax.text(x + 0.2, y + h - 0.35, title, ha="left", va="center", fontsize=16.5, fontweight="bold",
                    color=PANEL_TXT, zorder=4)
            if sub:
                ax.text(x + 0.2, y + h - 0.8, sub, ha="left", va="center", fontsize=12.5, fontweight="bold",
                        color=PANEL_TXT, zorder=4)

        def lab(x, y, t, fc="white"):
            ax.text(x, y, t, fontsize=12, fontweight="bold", color="#0b7a40" if fc != "white" else "#11a85a",
                    ha="center", va="center", zorder=5, bbox=dict(fc=fc, ec="none", pad=1.5), linespacing=1.1)

        # environment
        fbox(1.3, 13.5, 7.5, 1.4, "Physical greenhouse (GH1)", "Sun, wind, crops · fixed equipment · floor fans")
        fbox(13.1, 9.8, 3.6, 2.2, "Weather data", "NEA live readings,\n2-hour nowcast\n(when online)", dashed=True)

        # S1
        panel(1.0, 9.3, 11.7, 3.75, "S1 Sense and Map")
        fbox(1.3, 9.55, 3.6, 2.4, "Sensor nodes", "Permanent and\ntemporary · T, RH,\ncanopy · 30-min")
        fbox(5.3, 9.55, 3.2, 2.4, "Clean data", "Remove spikes\nand misting\nartefacts")
        fbox(8.9, 9.55, 3.5, 2.4, "Thermal map", "Soft sensors and\nGaussian process\nregression")
        dline = lambda pts, dashed=False: elbow(ax, pts, dashed=dashed)
        dline([(4.9, 10.75), (5.3, 10.75)])
        dline([(8.5, 10.75), (8.9, 10.75)])
        dline([(4.3, 13.5), (4.3, 11.95)])

        # S2 = Application 1
        panel(1.0, 0.8, 5.9, 7.5, "S2 Cooling Layout Evaluation", "Application 1: before the greenhouse is built")
        fbox(1.3, 4.6, 5.3, 2.4, "CFD flow model", "Airflow and heat for candidate\nlayouts; suggests the best")
        fbox(1.3, 1.1, 5.3, 2.4, "Layout tests", "Suggested layouts built with\nfloor fans; temperature\nvs baseline")
        dline([(3.95, 4.6), (3.95, 3.5)], dashed=True)
        lab(5.25, 4.05, "suggested\nlayouts", fc=PANEL)

        # S3 = Application 2
        panel(7.6, 0.8, 9.1, 7.5, "S3 Live Cooling Control", "Application 2: once operating (Raspberry Pi 5)")
        fbox(12.4, 4.6, 4.0, 2.4, "Hotspot prediction", "Exceedance 30 min\nahead; learned fan\neffects on T, RH")
        fbox(7.9, 4.6, 3.9, 2.4, "Dashboard", "Map, hotspots,\nfan status")
        fbox(12.4, 1.1, 4.0, 2.4, "Decide", "Right fans for each\nhotspot, fail-safe")
        fbox(7.9, 1.1, 3.9, 2.4, "Actuate", "Four floor fans,\nenergy metering")
        dline([(14.4, 4.6), (14.4, 3.5)])
        dline([(12.4, 2.3), (11.8, 2.3)])
        dline([(12.4, 5.8), (11.8, 5.8)])

        # flows between subsystems
        dline([(11.9, 9.55), (11.9, 8.85), (13.3, 8.85), (13.3, 7.0)])
        dline([(14.9, 9.8), (14.9, 7.0)], dashed=True)
        dline([(9.6, 9.55), (9.6, 8.85), (7.25, 8.85), (7.25, 5.8), (6.6, 5.8)])
        lab(8.45, 8.85, "measured data")
        dline([(6.6, 2.3), (7.9, 2.3)], dashed=True)
        lab(7.25, 1.65, "chosen\nlayout")
        # feedback loop
        ax.plot([9.85, 9.85, 0.35, 0.35, 1.0], [1.1, 0.35, 0.35, 14.2, 14.2], color="black", lw=2.2, zorder=2)
        ax.add_patch(FancyArrowPatch((1.0, 14.2), (1.3, 14.2), arrowstyle="->,head_length=0.5,head_width=0.3",
                                     mutation_scale=18, color="black", lw=2.2, zorder=2))
        ax.text(0.6, 12.0, "Feedback", rotation=90, fontsize=15, fontweight="bold", ha="left", va="center")
        ax.set_xlim(0, W); ax.set_ylim(0, H)
        fig.savefig(OUT + "fig-system-architecture.png", dpi=150, bbox_inches="tight", pad_inches=0.05, facecolor="white")
        plt.close(fig)


def edge_gateway_v2():
    """Figure 14: field, edge and cloud layers of the system, in the Figure 13 style."""
    with plt.rc_context({"font.family": "Inter"}):
        W, H = 17.0, 12.3
        fig, ax = canvas(W, H)
        LIGHT = "#c9f1db"

        def fbox(x, y, w, h, title, body, dashed=False, tags=(), ts=14.5, bs=12.5):
            ax.add_patch(Rectangle((x, y), w, h, fc="white", ec=DG, lw=1.8, ls="--" if dashed else "-", zorder=3))
            ax.text(x + w / 2, y + h - 0.38, title, ha="center", va="center", fontsize=ts, fontweight="bold", zorder=4)
            ax.text(x + w / 2, y + (h - 0.55) / 2, body, ha="center", va="center", fontsize=bs, zorder=4,
                    linespacing=1.25)
            for i, t in enumerate(tags):
                tx = x + w - 0.08 - 0.52 * (len(tags) - i)
                ax.add_patch(Rectangle((tx, y + h - 0.02), 0.46, 0.34, fc=DG, ec=DG, zorder=5))
                ax.text(tx + 0.23, y + h + 0.15, t, ha="center", va="center", fontsize=10, fontweight="bold",
                        color="white", zorder=6)

        def lab(x, y, t, fc="white"):
            ax.text(x, y, t, fontsize=11.5, fontweight="bold", color="#0b7a40" if fc != "white" else "#11a85a",
                    ha="center", va="center", zorder=6, bbox=dict(fc=fc, ec="none", pad=1.2), linespacing=1.1)

        def layer(y, title, sub):
            ax.text(0.2, y + 0.25, title, ha="left", va="center", fontsize=17, fontweight="bold", color=PANEL_TXT)
            ax.text(0.2, y - 0.12, sub, ha="left", va="top", fontsize=11.5, color=PANEL_TXT, linespacing=1.2)

        c1, c2, c3, c4 = (2.7, 2.7), (5.9, 2.7), (9.1, 2.9), (12.6, 4.0)
        # cloud
        layer(11.2, "Cloud", "when online")
        fbox(c1[0], 10.4, c1[1], 1.5, "FlowFuse", "Remote deployment\n(optional)", dashed=True)
        fbox(c2[0], 10.4, c2[1], 1.5, "Remote dashboard", "Grafana Cloud\n(optional)", dashed=True)
        fbox(c3[0], 10.4, c3[1], 1.5, "NEA weather", "Live readings,\n2-hour nowcast", dashed=True)
        # edge
        ax.add_patch(Rectangle((2.45, 4.4), 14.4, 5.55, fc=PANEL, ec=PANEL_EC, lw=1.8, zorder=1))
        layer(7.4, "Edge", "Raspberry Pi 5\n(Docker)\nruns offline")
        fbox(c2[0], 7.75, c2[1], 1.7, "Grafana", "Map, hotspots,\nfan status", tags=("S3",))
        fbox(c3[0], 7.75, c3[1], 1.7, "InfluxDB", "Time-series\nstorage", tags=("S1",))
        fbox(c4[0], 7.75, c4[1], 1.7, "MATLAB models", "Soft sensors, GPR map,\nfan effects, 30-min prediction",
             tags=("S1", "S3"))
        fbox(c1[0], 4.75, c1[1], 1.7, "USB–RS-485", "adapter", tags=("S1",))
        fbox(c2[0], 4.75, c2[1], 1.7, "Mosquitto", "MQTT broker", tags=("S1",))
        fbox(c3[0], 4.75, c3[1], 1.7, "Node-RED", "Time-stamp, clean;\ncontrol rules, fail-safe",
             tags=("S1", "S3"))
        # field
        ax.add_patch(Rectangle((2.45, 0.3), 9.75, 3.45, fc=LIGHT, ec=PANEL_EC, lw=1.8, zorder=1))
        layer(2.3, "Field", "GH1")
        fbox(c1[0], 0.65, c1[1], 2.45, "Type A nodes", "ESP32-C6 + SHT45\nin shield · T, RH", tags=("S1",))
        fbox(c2[0], 0.65, c2[1], 2.45, "Type B nodes", "Type A + MLX90640\nleaf temperature", tags=("S1",))
        fbox(9.1, 0.65, 2.7, 2.45, "Floor fans ×4", "PWM or relay,\nenergy metering", tags=("S3",))
        fbox(12.9, 0.65, 3.7, 2.45, "Design workstation", "SOLIDWORKS Flow\nSimulation (offline)", dashed=True,
             tags=("S2",))

        e = lambda pts, d=False: elbow(ax, pts, dashed=d)
        # field to edge
        e([(4.05, 3.1), (4.05, 4.75)])
        ax.plot([7.25, 7.25, 4.05], [3.1, 4.07, 4.07], color="black", lw=2.2, zorder=2)
        lab(5.65, 4.07, "RS-485 · JSON")
        e([(5.4, 5.6), (5.9, 5.6)])
        e([(8.6, 5.6), (9.1, 5.6)])
        e([(10.55, 6.45), (10.55, 7.75)])
        e([(12.0, 8.6), (12.6, 8.6)])
        e([(9.1, 8.6), (8.6, 8.6)])
        e([(13.8, 7.75), (13.8, 5.6), (12.0, 5.6)])
        lab(14.75, 6.35, "predictions", fc=PANEL)
        e([(10.45, 4.75), (10.45, 3.1)])
        lab(10.45, 4.07, "fan commands")
        e([(15.8, 7.75), (15.8, 3.1)], True)
        lab(15.8, 4.07, "logged data")
        e([(12.9, 1.85), (11.8, 1.85)], True)
        lab(12.35, 2.55, "chosen\nlayout")
        # cloud links
        e([(10.55, 10.4), (10.55, 9.45)], True)
        e([(7.25, 9.45), (7.25, 10.4)], True)
        e([(4.05, 10.4), (4.05, 7.1), (9.6, 7.1), (9.6, 6.45)], True)
        ax.set_xlim(0, W); ax.set_ylim(0, H)
        fig.savefig(OUT + "fig-edge-gateway.png", dpi=150, bbox_inches="tight", pad_inches=0.05, facecolor="white")
        plt.close(fig)


def edge_gateway_v3():
    """Figure 14: field, edge and cloud layers with pictures and drawn symbols, few words."""
    from matplotlib.patches import Circle, Ellipse
    src = plt.imread(os.path.join(os.path.dirname(os.path.abspath(__file__)), "edge-gateway-src.png"))
    k = src.shape[1] / 1600.0
    CROPS = {"pi": (345, 208, 612, 372), "typeA": (340, 562, 445, 668), "typeB": (532, 562, 615, 668),
             "fan": (868, 562, 978, 668), "laptop": (1335, 272, 1560, 398), "gh": (1178, 558, 1528, 708)}
    with plt.rc_context({"font.family": "Inter"}):
        W, H = 16.4, 12.9
        fig, ax = canvas(W, H)
        LIGHT = "#c9f1db"

        def pic(name, cx, cy, mw, mh):
            x0, y0, x1, y1 = [int(v * k) for v in CROPS[name]]
            im = src[y0:y1, x0:x1]
            r = im.shape[1] / im.shape[0]
            w, h = (mw, mw / r) if mw / r <= mh else (mh * r, mh)
            ax.imshow(im, extent=[cx - w / 2, cx + w / 2, cy - h / 2, cy + h / 2], aspect="auto", zorder=4)

        def ln(xs, ys, lw=2.4):
            ax.plot(xs, ys, color=DG, lw=lw, zorder=5, solid_capstyle="round")

        def i_db(cx, cy):
            for dy in (-0.32, 0.0, 0.32):
                ax.add_patch(Ellipse((cx, cy + dy), 1.0, 0.34, fc=LIGHT if dy == 0.32 else "white", ec=DG, lw=2.4,
                                     zorder=5 + (dy + 0.4)))
            ax.add_patch(Rectangle((cx - 0.5, cy - 0.32), 1.0, 0.64, fc="white", ec="none", zorder=5.05))
            ax.add_patch(Ellipse((cx, cy), 1.0, 0.34, fc="white", ec=DG, lw=2.4, zorder=5.4))
            ax.add_patch(Rectangle((cx - 0.5, cy), 1.0, 0.32, fc="white", ec="none", zorder=5.5))
            ax.add_patch(Ellipse((cx, cy + 0.32), 1.0, 0.34, fc=LIGHT, ec=DG, lw=2.4, zorder=5.8))
            for sx in (-0.5, 0.5):
                ax.plot([cx + sx, cx + sx], [cy - 0.32, cy + 0.32], color=DG, lw=2.4, zorder=6)

        def i_hub(cx, cy):
            import math
            for a in (90, 210, 330):
                px, py = cx + 0.44 * math.cos(math.radians(a)), cy - 0.12 + 0.44 * math.sin(math.radians(a))
                ln([cx, px], [cy - 0.12, py])
                ax.add_patch(Circle((px, py), 0.14, fc="white", ec=DG, lw=2.4, zorder=6))
            ax.add_patch(Circle((cx, cy - 0.12), 0.19, fc=LIGHT, ec=DG, lw=2.4, zorder=6))

        def i_flow(cx, cy):
            ln([cx - 0.35, cx, cx, cx + 0.3], [cy, cy, cy + 0.28, cy + 0.28])
            ln([cx, cx, cx + 0.3], [cy, cy - 0.28, cy - 0.28])
            for px, py, fc in ((-0.6, 0, LIGHT), (0.55, 0.28, "white"), (0.55, -0.28, "white")):
                ax.add_patch(Rectangle((cx + px - 0.27, cy + py - 0.15), 0.54, 0.3, fc=fc, ec=DG, lw=2.4, zorder=6))

        def i_chart(cx, cy):
            ln([cx - 0.55, cx - 0.55, cx + 0.6], [cy + 0.45, cy - 0.42, cy - 0.42])
            xs = [cx - 0.4, cx - 0.1, cx + 0.15, cx + 0.5]
            ys = [cy - 0.2, cy + 0.02, cy - 0.08, cy + 0.36]
            ln(xs, ys)
            for x, y in zip(xs, ys):
                ax.add_patch(Circle((x, y), 0.07, fc=LIGHT, ec=DG, lw=2, zorder=6))

        def i_plug(cx, cy):
            ax.add_patch(Rectangle((cx - 0.75, cy - 0.2), 0.5, 0.4, fc=LIGHT, ec=DG, lw=2.4, zorder=6))
            ax.add_patch(Rectangle((cx + 0.25, cy - 0.27), 0.5, 0.54, fc="white", ec=DG, lw=2.4, zorder=6))
            ln([cx - 0.25, cx + 0.25], [cy, cy])
            for dy in (-0.14, 0, 0.14):
                ln([cx + 0.75, cx + 0.92], [cy + dy, cy + dy], lw=2)

        def i_cloud(cx, cy, sun=False):
            if sun:
                import math
                sx, sy = cx + 0.38, cy + 0.3
                for a in range(0, 360, 45):
                    ln([sx + 0.3 * math.cos(math.radians(a)), sx + 0.42 * math.cos(math.radians(a))],
                       [sy + 0.3 * math.sin(math.radians(a)), sy + 0.42 * math.sin(math.radians(a))], lw=2)
                ax.add_patch(Circle((sx, sy), 0.22, fc=LIGHT, ec=DG, lw=2.4, zorder=5))
            parts = [(-0.3, -0.08, 0.24), (0.02, 0.1, 0.34), (0.36, -0.08, 0.24)]
            for fc, grow, z in ((DG, 0.035, 6), ("white", -0.035, 7)):
                for px, py, r in parts:
                    ax.add_patch(Circle((cx + px, cy + py), r + grow, fc=fc, ec="none", zorder=z))
                ax.add_patch(Rectangle((cx - 0.3, cy - 0.32 - grow), 0.66, 0.4 + grow, fc=fc, ec="none", zorder=z))

        def i_monitor(cx, cy):
            import numpy as np
            ax.add_patch(Rectangle((cx - 0.7, cy - 0.3), 1.4, 0.85, fc="white", ec=DG, lw=2.4, zorder=5))
            ln([cx, cx], [cy - 0.3, cy - 0.5]); ln([cx - 0.3, cx + 0.3], [cy - 0.5, cy - 0.5])
            t = np.linspace(-0.5, 0.45, 40)
            for dy in (-0.1, 0.12, 0.34):
                ax.plot(cx + t, cy + dy + 0.06 * np.sin(9 * t), color="#11a85a", lw=2, zorder=6)
                ax.plot([cx + 0.37, cx + 0.47, cx + 0.37], [cy + dy + 0.02, cy + dy - 0.05, cy + dy - 0.12],
                        color="#11a85a", lw=2, zorder=6)

        def card(x, y, w, h, title, sub=None, icon=None, img=None, dashed=False, tags=()):
            ax.add_patch(Rectangle((x, y), w, h, fc="white", ec=DG, lw=1.8, ls="--" if dashed else "-", zorder=3))
            ty = y + (0.62 if sub else 0.42)
            ax.text(x + w / 2, ty, title, ha="center", va="center", fontsize=14.5, fontweight="bold", zorder=4)
            if sub:
                ax.text(x + w / 2, y + 0.25, sub, ha="center", va="center", fontsize=11.5, zorder=4)
            top = ty + 0.3
            cy = (top + y + h) / 2
            if icon:
                icon(x + w / 2, cy)
            if img:
                pic(img, x + w / 2, cy, w - 0.5, y + h - top - 0.2)
            for i, t in enumerate(tags):
                tx = x + w - 0.08 - 0.52 * (len(tags) - i)
                ax.add_patch(Rectangle((tx, y + h - 0.02), 0.46, 0.34, fc=DG, ec=DG, zorder=5))
                ax.text(tx + 0.23, y + h + 0.15, t, ha="center", va="center", fontsize=10, fontweight="bold",
                        color="white", zorder=6)

        def lab(x, y, t, fc="white"):
            ax.text(x, y, t, fontsize=11.5, fontweight="bold", color="#0b7a40" if fc != "white" else "#11a85a",
                    ha="center", va="center", zorder=6, bbox=dict(fc=fc, ec="none", pad=1.2), linespacing=1.1)

        def layer(y, title, sub):
            ax.text(0.2, y, title, ha="left", va="center", fontsize=17, fontweight="bold", color=PANEL_TXT)
            ax.text(0.2, y - 0.4, sub, ha="left", va="center", fontsize=11.5, color=PANEL_TXT)

        X1, X2, X3, X4, CW = 2.75, 6.15, 9.55, 12.95, 2.9
        # cloud
        layer(12.1, "Cloud", "when online")
        card(X2, 10.5, CW, 2.1, "Remote access", "optional", icon=i_cloud, dashed=True)
        card(X3, 10.5, CW, 2.1, "NEA weather", icon=lambda cx, cy: i_cloud(cx - 0.1, cy - 0.12, sun=True), dashed=True)
        # edge
        ax.add_patch(Rectangle((2.45, 4.2), 13.7, 5.75, fc=PANEL, ec=PANEL_EC, lw=1.8, zorder=1))
        layer(9.5, "Edge", "Raspberry Pi 5")
        pic("pi", 1.25, 7.9, 2.1, 1.6)
        ax.text(0.2, 6.75, "runs offline", ha="left", va="center", fontsize=11.5, color=PANEL_TXT)
        card(X2, 7.3, CW, 2.1, "Grafana", "Dashboard", img="laptop", tags=("S3",))
        card(X3, 7.3, CW, 2.1, "InfluxDB", "Storage", icon=i_db, tags=("S1",))
        card(X4, 7.3, CW, 2.1, "Models", "Map · prediction", icon=i_chart, tags=("S1", "S3"))
        card(X1, 4.5, CW, 2.1, "USB–RS-485", icon=i_plug, tags=("S1",))
        card(X2, 4.5, CW, 2.1, "Mosquitto", "MQTT", icon=i_hub, tags=("S1",))
        card(X3, 4.5, CW, 2.1, "Node-RED", "Clean · control", icon=i_flow, tags=("S1", "S3"))
        # field
        ax.add_patch(Rectangle((2.45, 0.3), 10.25, 3.2, fc=LIGHT, ec=PANEL_EC, lw=1.8, zorder=1))
        layer(3.1, "Field", "GH1")
        pic("gh", 1.25, 1.5, 2.1, 1.5)
        card(X1, 0.6, CW, 2.3, "Type A node", "T, RH", img="typeA", tags=("S1",))
        card(X2, 0.6, CW, 2.3, "Type B node", "+ leaf temperature", img="typeB", tags=("S1",))
        card(X3, 0.6, CW, 2.3, "Floor fans ×4", img="fan", tags=("S3",))
        card(13.6, 0.6, 2.55, 2.3, "CFD", "offline", icon=i_monitor, dashed=True, tags=("S2",))

        e = lambda pts, d=False: elbow(ax, pts, dashed=d)
        e([(4.2, 2.9), (4.2, 4.5)])
        ax.plot([7.6, 7.6, 4.2], [2.9, 3.85, 3.85], color="black", lw=2.2, zorder=2)
        lab(5.9, 3.85, "RS-485")
        e([(5.65, 5.55), (6.15, 5.55)])
        e([(9.05, 5.55), (9.55, 5.55)])
        e([(10.4, 6.6), (10.4, 7.3)])
        e([(12.45, 8.35), (12.95, 8.35)])
        e([(9.55, 8.35), (9.05, 8.35)])
        e([(13.6, 7.3), (13.6, 5.55), (12.45, 5.55)])
        lab(13.6, 6.6, "predictions", fc=PANEL)
        e([(10.7, 4.5), (10.7, 2.9)])
        lab(10.7, 3.85, "fan commands")
        e([(15.3, 7.3), (15.3, 2.9)], True)
        lab(15.3, 3.85, "logged data")
        e([(13.6, 1.75), (12.45, 1.75)], True)
        lab(13.15, 2.45, "chosen\nlayout")
        e([(11.0, 10.5), (11.0, 9.4)], True)
        e([(7.6, 9.4), (7.6, 10.5)], True)
        ax.set_xlim(0, W); ax.set_ylim(0, H)
        fig.savefig(OUT + "fig-edge-gateway.png", dpi=150, bbox_inches="tight", pad_inches=0.05, facecolor="white")
        plt.close(fig)


def edge_gateway_v5():
    """Figure 14: IT/OT bus layout (cloud, edge, field) reusing pictures and logos from the author's original figure."""
    import numpy as np
    from matplotlib.patches import Circle
    src = plt.imread(os.path.join(os.path.dirname(os.path.abspath(__file__)), "edge-gateway-src.png"))[:, :, :3].copy()
    k = src.shape[1] / 2110.0
    CROPS = {"flowfuse": (748, 66, 948, 112), "grafana_word": (1172, 64, 1362, 118), "pi": (470, 256, 822, 466),
             "nodered": (931, 279, 1022, 361), "influx_icon": (943, 392, 1018, 464), "influx_word": (1030, 394, 1162, 432),
             "matlab": (1350, 270, 1432, 352), "solidworks": (1360, 398, 1594, 464), "grafana": (1760, 260, 1830, 332),
             "laptop": (1745, 348, 2052, 506), "mqtt": (746, 552, 878, 590), "rs485": (970, 548, 1024, 590),
             "typeA": (462, 726, 597, 852), "typeB": (716, 726, 820, 860), "fan": (1158, 728, 1292, 854),
             "gh": (1563, 733, 2017, 908)}
    GREY, MUTED = "#555555", "#777777"
    with plt.rc_context({"font.family": "Inter"}):
        W, H = 17.0, 12.4
        fig, ax = canvas(W, H)

        def pic(name, cx, cy, w, clean=True):
            x0, y0, x1, y1 = [int(v * k) for v in CROPS[name]]
            im = src[y0:y1, x0:x1].copy()
            if clean:  # tinted off-white background -> white
                bg = (im.min(axis=2) > 0.9) & ((im.max(axis=2) - im.min(axis=2)) < 0.06)
                im[bg] = 1.0
            h = w * im.shape[0] / im.shape[1]
            ax.imshow(im, extent=[cx - w / 2, cx + w / 2, cy - h / 2, cy + h / 2], aspect="auto", zorder=4)
            return h

        def t(x, y, s, size=12, bold=False, color="black", ha="center"):
            ax.text(x, y, s, ha=ha, va="center", fontsize=size, fontweight="bold" if bold else "normal",
                    color=color, zorder=6, linespacing=1.25)

        def dbl(x0, x1, y):
            ax.add_patch(FancyArrowPatch((x0, y), (x1, y), arrowstyle="<->", mutation_scale=13, color=GREY, lw=1.4,
                                         linestyle=(0, (2.5, 2.5)), zorder=3))

        def cloud(cx, y0, w, h=2.2):
            re = 0.4 * h
            parts = [(-(w / 2 - re), re, re), (w / 2 - re, re, re), (-0.13 * w, 0.52 * h, 0.43 * h),
                     (0.16 * w, 0.48 * h, 0.39 * h)]
            for fc, g, z in (("black", 0.022, 2), ("white", -0.022, 3)):
                for px, py, r in parts:
                    ax.add_patch(Circle((cx + px, y0 + py), r + g, fc=fc, ec="none", zorder=z))
                ax.add_patch(Rectangle((cx - w / 2 + re, y0 - g), w - 2 * re, re + g, fc=fc, ec="none", zorder=z))

        # layer labels and bus lines
        IT, OT = 9.0, 4.6
        t(0.25, 10.3, "Cloud\nService", 12.5, color=MUTED, ha="left")
        t(0.25, 6.9, "Edge\nComputing", 12.5, color=MUTED, ha="left")
        t(0.25, 2.6, "Field\nLayer", 12.5, color=MUTED, ha="left")
        t(0.25, IT, "IT", 22, bold=True, ha="left")
        t(0.25, OT, "OT", 22, bold=True, color=DG, ha="left")
        ax.add_patch(FancyArrowPatch((0.6, IT - 0.45), (0.6, 7.45), arrowstyle="<-", mutation_scale=12, color=MUTED,
                                     lw=1.2, linestyle=(0, (2.5, 2.5))))
        ax.add_patch(FancyArrowPatch((0.6, 6.35), (0.6, OT + 0.45), arrowstyle="->", mutation_scale=12, color=MUTED,
                                     lw=1.2, linestyle=(0, (2.5, 2.5))))
        ax.plot([1.5, 16.7], [IT, IT], color="black", lw=2.2, zorder=2)
        ax.plot([1.5, 16.7], [OT, OT], color=DG, lw=2.4, zorder=2)

        # cloud: modelling, dashboard, services
        Y0, PX = 9.75, 7.8
        cloud(4.7, Y0, 5.0)
        pic("solidworks", 3.65, Y0 + 1.2, 1.9)
        t(3.65, Y0 + 0.62, "CFD", 12.5, bold=True); t(3.65, Y0 + 0.3, "S2 · fan layout", 10.5, color=GREY)
        pic("matlab", 5.85, Y0 + 1.22, 0.72)
        t(5.85, Y0 + 0.62, "Models", 12.5, bold=True); t(5.85, Y0 + 0.3, "map · prediction", 10.5, color=GREY)
        cloud(9.9, Y0, 4.4)
        pic("grafana_word", 8.95, Y0 + 1.1, 1.3, clean=False)
        t(8.95, Y0 + 0.5, "Dashboard", 12.5, bold=True)
        pic("laptop", 10.75, Y0 + 0.85, 1.85)
        cloud(14.4, Y0, 3.6)
        t(14.4, Y0 + 1.25, "NEA weather", 13, bold=True)
        t(14.4, Y0 + 0.92, "live readings · nowcast", 10.5, color=GREY)
        pic("flowfuse", 14.0, Y0 + 0.42, 1.0, clean=False); t(14.6, Y0 + 0.42, "optional", 10, color=GREY, ha="left")
        ax.plot([4.7, 4.7, 14.4, 14.4], [Y0, 9.38, 9.38, Y0], color="black", lw=1.6, zorder=1)
        ax.plot([9.9, 9.9], [Y0, 9.38], color="black", lw=1.6, zorder=1)
        ax.plot([PX, PX], [9.38, IT], color="black", lw=1.6, zorder=1)
        ax.plot([PX, PX], [IT, 8.05], color="black", lw=1.8, ls=(0, (1, 2)), zorder=1)
        t(PX + 0.2, 8.55, "internet", 10.5, color=MUTED, ha="left")

        # edge
        pic("pi", PX, 6.95, 3.2)
        t(PX, 5.62, "Raspberry Pi 5 edge gateway", 13.5, bold=True)
        t(PX, 5.27, "collects, stores and controls (Docker)", 11, color=GREY)
        ax.plot([PX, PX], [5.05, OT], color=DG, lw=2.4, zorder=2)
        for y in (7.9, 6.95, 6.0):
            dbl(PX + 1.75, PX + 2.55, y)
        pic("mqtt", PX + 3.3, 7.9, 1.25, clean=False); t(PX + 4.1, 7.9, "Mosquitto", 12, ha="left")
        pic("nodered", PX + 2.98, 6.95, 0.62, clean=False); t(PX + 3.45, 6.95, "Node-RED", 13, bold=True, ha="left")
        pic("influx_icon", PX + 2.98, 6.0, 0.58); pic("influx_word", PX + 3.98, 6.02, 1.15)

        # field
        pic("rs485", 3.2, OT + 0.33, 0.42); t(3.5, OT + 0.33, "RS-485", 12, bold=True, ha="left")
        ax.plot([4.3, 4.3], [OT, 3.95], color=DG, lw=2.0, zorder=2)
        ax.plot([3.0, 5.6], [3.95, 3.95], color=DG, lw=2.0, zorder=2)
        for x in (3.0, 5.6):
            ax.plot([x, x], [3.95, 3.55], color=DG, lw=2.0, zorder=2)
        pic("typeA", 3.0, 2.8, 1.3); t(3.0, 1.82, "Type A", 12.5, bold=True); t(3.0, 1.5, "T, RH", 10.5, color=GREY)
        pic("typeB", 5.6, 2.8, 1.05); t(5.6, 1.82, "Type B", 12.5, bold=True)
        t(5.6, 1.5, "+ leaf temperature", 10.5, color=GREY)
        t(6.75, 2.8, "…", 16, bold=True)
        ax.plot([10.0, 10.0], [OT, 3.55], color=DG, lw=2.0, zorder=2)
        t(10.2, 4.1, "PWM / relay", 10.5, color=GREY, ha="left")
        pic("fan", 10.0, 2.8, 1.35); t(10.0, 1.82, "Floor fans ×4", 12.5, bold=True)
        t(10.0, 1.5, "energy metered", 10.5, color=GREY)
        pic("gh", 14.45, 2.75, 3.5)
        for x in (8.0, 12.1):
            ax.plot([x, x], [OT - 0.2, 0.3], color="#9fb8a8", lw=1.3, ls=(0, (1, 2.5)), zorder=1)
        t(4.4, 0.65, "S1 Sense and Map", 13, bold=True)
        t(10.0, 0.65, "S3 Live Cooling Control", 13, bold=True)
        t(14.45, 0.65, "GH1 greenhouse", 13, bold=True)
        ax.set_xlim(0, W); ax.set_ylim(0, H)
        fig.savefig(OUT + "fig-edge-gateway.png", dpi=150, bbox_inches="tight", pad_inches=0.05, facecolor="white")
        plt.close(fig)


problem_framing()
farmer_value()
cooling_options()
functional_decomposition()
system_decomposition()
architecture_v3()
edge_gateway_v5()
trapped_hot_air()
roadmap()
print("done")
