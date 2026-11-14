"""Greenhouse 1 geometry: single source for the dashboard model (JSON) and the STEP file.

Plan coordinates (metres): x to the right of the layout drawing, y to the top of
the drawing, z up. Origin = inner (bottom) corner where the main section meets
the transition. The front wall (exhaust fans 1 and 2, airlock) is at x = 36.

Curvilinear coordinates: s = distance from the front wall along the building,
t = distance across from the bottom wall of the drawing (0..12.5).
"""
import json
import math
import sys

# ---------------------------------------------------------------- dimensions
W = 12.5            # width
L_MAIN = 36.0       # straight section
TOP_W, BOT_W = 3.67, 2.48        # transition, top / bottom wall lengths
WING_TOP, WING_BOT = 19.53, 20.5  # wing, top / bottom wall lengths
WALL_H = 3.0        # eave height (sketch: 300)
RIDGE_H = 3.35      # main roof at centreline (sketch: 335)
PEAK_H = 4.35       # top of raised ridge section (table: 4.35, sketch: 430)
MON_HALF = 1.5      # half width of raised ridge section (sketch proportion, ~3 m)
MON_SHOULDER = 3.95  # top of its vertical sides (assumed)
KERB_H = 0.29       # base kerb (sketch: 29)
MESH_TOP = 1.5      # top of mesh band (sketch line ~150, photo)
TP = 0.02           # nominal panel thickness for CAD
PLANT_H = 1.0       # plant height (sketch note)
BENCH_H = 0.6       # bench top (assumed), canopy from here to PLANT_H
S0, DS = 1.5, 3.1   # measurement columns: first column and spacing along the house
DT = 3.25           # measurement rows: spacing across (stated as 3 to 3.5 m)
T0 = W / 2 - DT
HUMP_S, HUMP_W, HUMP_H = 20.0, 2.1, 0.15   # floor hump: centre, width, peak height

HALF = math.asin((TOP_W - BOT_W) / (2 * W))
TH = 2 * HALF                       # bend angle
R0 = BOT_W / (2 * math.sin(HALF))   # pivot distance below bottom wall
LW = 2 * (R0 + W / 2) * math.sin(HALF)  # transition length on centreline
S_W1 = L_MAIN + LW
U = (-math.cos(TH), -math.sin(TH))  # wing axis direction


def s_end(t):
    return S_W1 + WING_BOT + (WING_TOP - WING_BOT) * t / W


def wing_start(t):
    return (-(R0 + t) * math.sin(TH), -R0 + (R0 + t) * math.cos(TH))


def P(s, t):
    """(s, t) -> plan (x, y)."""
    if s <= L_MAIN:
        return (L_MAIN - s, t)
    wx, wy = wing_start(t)
    if s <= S_W1:
        f = (s - L_MAIN) / LW
        return (wx * f, t + (wy - t) * f)
    d = s - S_W1
    return (wx + d * U[0], wy + d * U[1])


def roofline(t):
    return WALL_H + (RIDGE_H - WALL_H) * (1 - abs(t - W / 2) / (W / 2))


def mon_under(t):
    return (MON_SHOULDER - TP) + (PEAK_H - MON_SHOULDER) * (1 - abs(t - W / 2) / MON_HALF)


# ---------------------------------------------------------------- solids
solids = []


def sub(a, b): return (a[0]-b[0], a[1]-b[1], a[2]-b[2])
def cross(a, b): return (a[1]*b[2]-a[2]*b[1], a[2]*b[0]-a[0]*b[2], a[0]*b[1]-a[1]*b[0])
def dot(a, b): return a[0]*b[0]+a[1]*b[1]+a[2]*b[2]
def norm(a):
    l = math.sqrt(dot(a, a))
    return (a[0]/l, a[1]/l, a[2]/l)


def newell(pts):
    n = [0.0, 0.0, 0.0]
    for i in range(len(pts)):
        a, b = pts[i], pts[(i+1) % len(pts)]
        n[0] += (a[1]-b[1])*(a[2]+b[2])
        n[1] += (a[2]-b[2])*(a[0]+b[0])
        n[2] += (a[0]-b[0])*(a[1]+b[1])
    return tuple(n)


def loft(name, cat, ring_a, ring_b):
    """Solid between two rings of equal length (caps + quad sides)."""
    n = len(ring_a)
    assert n == len(ring_b) and n >= 3
    verts = [tuple(round(c, 6) for c in p) for p in list(ring_a) + list(ring_b)]
    faces = [list(range(n - 1, -1, -1)), list(range(n, 2 * n))]
    for i in range(n):
        j = (i + 1) % n
        faces.append([i, j, n + j, n + i])
    # signed volume -> make normals outward
    vol = 0.0
    for f in faces:
        p0 = verts[f[0]]
        for k in range(1, len(f) - 1):
            vol += dot(p0, cross(verts[f[k]], verts[f[k+1]])) / 6.0
    if vol < 0:
        faces = [f[::-1] for f in faces]
        vol = -vol
    # planarity check
    for f in faces:
        pts = [verts[i] for i in f]
        nn = norm(newell(pts))
        d0 = dot(nn, pts[0])
        dev = max(abs(dot(nn, p) - d0) for p in pts)
        assert dev < 1e-5, (name, dev)
    solids.append({"name": name, "cat": cat, "verts": verts, "faces": faces, "vol": vol})


def zval(z, i, st):
    if callable(z):
        return z(st[1])
    if isinstance(z, (list, tuple)):
        return z[i]
    return z


def prism_st(name, cat, ring_st, zb, zt):
    a = [P(s, t) + (zval(zb, i, (s, t)),) for i, (s, t) in enumerate(ring_st)]
    b = [P(s, t) + (zval(zt, i, (s, t)),) for i, (s, t) in enumerate(ring_st)]
    loft(name, cat, a, b)


def box_st(name, cat, s0, s1, t0, t1, z0, z1):
    prism_st(name, cat, [(s0, t0), (s1, t0), (s1, t1), (s0, t1)], z0, z1)


def seg_rings(t0, t1, a=0.0, e=0.0):
    """Three (s,t) rings covering main / transition / wing between t0 and t1."""
    return [
        ("MAIN", [(a, t0), (L_MAIN, t0), (L_MAIN, t1), (a, t1)]),
        ("TRANSITION", [(L_MAIN, t0), (S_W1, t0), (S_W1, t1), (L_MAIN, t1)]),
        ("WING", [(S_W1, t0), (s_end(t0) - e, t0), (s_end(t1) - e, t1), (S_W1, t1)]),
    ]


# floor
for seg, ring in seg_rings(0, W):
    prism_st(f"FLOOR_{seg}", "floor", ring, -0.1, 0.0)

# side walls in three bands
for side, (t0, t1) in (("BOTTOM", (0, TP)), ("TOP", (W - TP, W))):
    for seg, ring in seg_rings(t0, t1, TP, TP):
        prism_st(f"WALL_{side}_{seg}_KERB", "kerb", ring, 0.0, KERB_H)
        prism_st(f"WALL_{side}_{seg}_NETTING_0P3MM", "mesh", ring, KERB_H, MESH_TOP)
        prism_st(f"WALL_{side}_{seg}_PLASTIC_0P3MM_SHADE_0P5MM", "plastic", ring, MESH_TOP, WALL_H)

# roof slopes, raised ridge section sides and roof
ML, MR = W / 2 - MON_HALF, W / 2 + MON_HALF
for side, (t0, t1) in (("BOTTOM", (0, ML)), ("TOP", (MR, W))):
    for seg, ring in seg_rings(t0, t1):
        prism_st(f"ROOF_{side}_{seg}", "roof", ring, roofline, lambda t: roofline(t) + TP)
for side, (t0, t1) in (("BOTTOM", (ML, ML + TP)), ("TOP", (MR - TP, MR))):
    for seg, ring in seg_rings(t0, t1, TP, TP):
        prism_st(f"RIDGE_RAISED_SIDE_{side}_{seg}", "monitor", ring, roofline, mon_under)
for side, (t0, t1) in (("BOTTOM", (ML, W / 2)), ("TOP", (W / 2, MR))):
    for seg, ring in seg_rings(t0, t1):
        prism_st(f"RIDGE_RAISED_ROOF_{side}_{seg}", "monitor", ring, mon_under, lambda t: mon_under(t) + TP)

# end walls (full profile including raised ridge section)
profile = [(0, MESH_TOP), (W, MESH_TOP), (W, WALL_H), (MR, roofline(MR)), (MR, mon_under(MR)),
           (W / 2, mon_under(W / 2)), (ML, mon_under(ML)), (ML, roofline(ML)), (0, WALL_H)]
bands = [("KERB", "kerb", [(0, 0), (W, 0), (W, KERB_H), (0, KERB_H)]),
         ("NETTING_0P3MM", "mesh", [(0, KERB_H), (W, KERB_H), (W, MESH_TOP), (0, MESH_TOP)]),
         ("PLASTIC_0P3MM_SHADE_0P5MM", "plastic", profile)]
for bname, bcat, prof in bands:
    loft(f"END_WALL_FRONT_{bname}", bcat,
         [P(0, t) + (z,) for t, z in prof], [P(TP, t) + (z,) for t, z in prof])
    loft(f"END_WALL_REAR_{bname}", bcat,
         [P(s_end(t), t) + (z,) for t, z in prof], [P(s_end(t) - TP, t) + (z,) for t, z in prof])

# beds: (name, cat, s0, s1) per row; rows are numbered from the bottom of the drawing
ROWS = {1: (0.7, 3.5), 2: (4.85, 7.65), 3: (9.0, 11.8)}
beds = [
    ("GERMINATION", 3, 1.9, 11.3, "Germination"),
    ("PLANTS_MAIN_R3", 3, 12.1, 33.9, "Plants"),
    ("PLANTS_MAIN_R2_FRONT", 2, 1.9, 18.9, "Plants"),
    ("PLANTS_MAIN_R2_REAR", 2, 21.1, 33.9, "Plants"),
    ("SEEDLING_CHANNELS", 1, 1.9, 18.9, "Seedling channels"),
    ("PLANTS_MAIN_R1_REAR", 1, 21.1, 33.9, "Plants"),
    ("PLANTS_WING_R3", 3, S_W1 + 2.2, S_W1 + 18.4, "Plants"),
    ("PLANTS_WING_R2", 2, S_W1 + 2.2, S_W1 + 18.4, "Plants"),
    ("PLANTS_WING_R1", 1, S_W1 + 2.2, S_W1 + 18.4, "Plants"),
]
bed_info = []
for name, row, s0, s1, label in beds:
    t0, t1 = ROWS[row]
    cat = "germ" if name == "GERMINATION" else "bed"
    box_st(f"BED_{name}", cat, s0, s1, t0, t1, 0.0, PLANT_H)
    bed_info.append({"label": label, "row": row, "s0": round(s0, 3), "s1": round(s1, 3),
                     "t0": t0, "t1": t1, "germ": cat == "germ"})
for row, (t0, t1) in ROWS.items():
    box_st(f"RESERVOIR_MAIN_R{row}", "tank", 34.0, 35.5, t0 + 0.4, t1 - 0.4, 0.0, 0.8)
    box_st(f"RESERVOIR_WING_R{row}", "tank", S_W1 + 0.5, S_W1 + 2.0, t0 + 0.4, t1 - 0.4, 0.0, 0.8)

# floor hump (hazard strip in the layout), kept clear of the row-3 bed that crosses it
_R = (HUMP_W ** 2 / 4 + HUMP_H ** 2) / (2 * HUMP_H)
_arc = [(-HUMP_W / 2 + HUMP_W * i / 12) for i in range(13)]
_arc = [(HUMP_S + x, max(0.0, math.sqrt(_R * _R - x * x) - (_R - HUMP_H))) for x in _arc]
for nm, (ta, tb) in (("A", (TP, 9.0)), ("B", (11.8, W - TP))):
    loft(f"FLOOR_HUMP_{nm}", "hump", [P(sv, ta) + (zv,) for sv, zv in _arc], [P(sv, tb) + (zv,) for sv, zv in _arc])

# stations and other items
box_st("WEATHER_STATION", "station", 36.2, 38.2, 9.3, 11.0, 0.0, 1.5)
box_st("WORK_STATION_TRANSITION", "station", 36.2, 38.0, 5.1, 6.8, 0.0, 0.9)
box_st("WORK_STATION_FRONT", "station", 0.4, 1.5, 0.2, 2.9, 0.0, 0.9)
box_st("UNLABELLED_BOX_TRANSITION", "station", 36.3, 38.2, 0.1, 1.4, 0.0, 2.0)
box_st("AIRLOCK_FRONT", "airlock", -1.5, 0.0, 3.7, 6.1, 0.0, 2.3)
box_st("WATER_TANK_MAIN", "tank", 33.7, 35.8, 13.5, 15.0, 0.0, 1.8)
box_st("WATER_TANK_WING", "tank", S_W1 + 0.3, S_W1 + 2.5, 13.5, 15.0, 0.0, 1.8)

# fans
FAN_Z = 2.65
fans = [
    {"id": "1", "type": "exhaust", "s": 0.0, "t": 5.8, "dir": -1, "where": "Front wall"},
    {"id": "2", "type": "exhaust", "s": 0.0, "t": 3.07, "dir": -1, "where": "Front wall"},
    {"id": "3", "type": "circ", "s": 5.6, "t": 8.1, "dir": 1, "where": "Main, front"},
    {"id": "4", "type": "circ", "s": 16.0, "t": 4.1, "dir": -1, "where": "Main, middle"},
    {"id": "5", "type": "circ", "s": 28.8, "t": 8.1, "dir": 1, "where": "Main, rear"},
    {"id": "6", "type": "circ", "s": S_W1 + 4.2, "t": 4.1, "dir": -1, "where": "Wing, near"},
    {"id": "7", "type": "circ", "s": S_W1 + 6.6, "t": 8.1, "dir": 1, "where": "Wing, near"},
    {"id": "8", "type": "circ", "s": S_W1 + 15.7, "t": 4.1, "dir": -1, "where": "Wing, far"},
    {"id": "9", "type": "exhaust", "s": None, "t": 6.2, "dir": 1, "where": "Rear wall"},
    {"id": "10", "type": "exhaust", "s": None, "t": 3.9, "dir": 1, "where": "Rear wall"},
]
for f in fans:
    t = f["t"]
    if f["type"] == "exhaust":
        if f["s"] is None:
            f["s"] = s_end(t)
            ring = [(s_end(t - 0.3), t - 0.3), (s_end(t - 0.3) + 0.3, t - 0.3),
                    (s_end(t + 0.3) + 0.3, t + 0.3), (s_end(t + 0.3), t + 0.3)]
        else:
            ring = [(-0.3, t - 0.3), (0.0, t - 0.3), (0.0, t + 0.3), (-0.3, t + 0.3)]
        prism_st(f"EXHAUST_FAN_{f['id']}", "fan_exh", ring, FAN_Z - 0.25, FAN_Z + 0.25)
        f["z"] = FAN_Z
    else:
        f["z"] = 2.5
        n, r = 16, 0.3
        ra, rb = [], []
        for k in range(n):
            a = 2 * math.pi * k / n
            tt, zz = t + r * math.cos(a), f["z"] + r * math.sin(a)
            ra.append(P(f["s"] - 0.1, tt) + (zz,))
            rb.append(P(f["s"] + 0.1, tt) + (zz,))
        loft(f"CIRCULATING_FAN_{f['id']}", "fan_circ", ra, rb)
    x, y = P(f["s"], t)
    # unit direction of +s at this point
    x2, y2 = P(f["s"] + 0.01, t) if f["s"] + 0.01 <= s_end(t) else (None, None)
    if x2 is None:
        x1, y1 = P(f["s"] - 0.01, t)
        dx, dy = x - x1, y - y1
    else:
        dx, dy = x2 - x, y2 - y
    l = math.hypot(dx, dy)
    f.update({"x": round(x, 3), "y": round(y, 3), "s": round(f["s"], 3),
              "dx": round(f["dir"] * dx / l, 4), "dy": round(f["dir"] * dy / l, 4)})

# sensors: 19 columns x 3 rows, 3 m grid, 1 m height
sensors = []
for k in range(19):
    for r in range(3):
        s, t = S0 + DS * k, T0 + DT * r
        x, y = P(s, t)
        sensors.append({"id": f"T{3*k+r+1}", "col": k, "row": r + 1, "s": round(s, 3), "t": t,
                        "x": round(x, 3), "y": round(y, 3)})


# ---------------------------------------------------------------- triangulation (for the web model)
def ear_clip(pts3):
    n = norm(newell(pts3))
    ax = max(range(3), key=lambda i: abs(n[i]))
    i0, i1 = [(1, 2), (2, 0), (0, 1)][ax]
    sgn = 1 if n[ax] > 0 else -1
    p2 = [(p[i0], p[i1] * sgn) for p in pts3]
    idx = list(range(len(p2)))
    tris = []

    def area(a, b, c): return (b[0]-a[0])*(c[1]-a[1]) - (b[1]-a[1])*(c[0]-a[0])

    def inside(p, a, b, c):
        return area(a, b, p) > 1e-12 and area(b, c, p) > 1e-12 and area(c, a, p) > 1e-12
    guard = 0
    while len(idx) > 3 and guard < 10000:
        guard += 1
        for k in range(len(idx)):
            ia, ib, ic = idx[k-1], idx[k], idx[(k+1) % len(idx)]
            a, b, c = p2[ia], p2[ib], p2[ic]
            if area(a, b, c) <= 1e-12:
                continue
            if any(inside(p2[j], a, b, c) for j in idx if j not in (ia, ib, ic)):
                continue
            tris.append((ia, ib, ic))
            idx.pop(k)
            break
        else:
            break
    if len(idx) == 3:
        tris.append(tuple(idx))
    return tris


def web_solid(sd):
    tri, edges = [], set()
    for f in sd["faces"]:
        pts = [sd["verts"][i] for i in f]
        for a, b, c in ear_clip(pts):
            tri += [f[a], f[b], f[c]]
        for i in range(len(f)):
            a, b = f[i], f[(i+1) % len(f)]
            edges.add((min(a, b), max(a, b)))
    return {"n": sd["name"], "c": sd["cat"],
            "v": [round(c, 3) for p in sd["verts"] for c in p],
            "i": tri, "e": [i for e in sorted(edges) for i in e]}


# ---------------------------------------------------------------- STEP writer (AP214, mm)
COLOURS = {
    "floor": (0.72, 0.72, 0.70), "kerb": (0.55, 0.55, 0.53), "mesh": (0.62, 0.72, 0.66),
    "plastic": (0.85, 0.90, 0.92), "roof": (0.88, 0.92, 0.94), "monitor": (0.80, 0.88, 0.92),
    "bed": (0.36, 0.62, 0.34), "germ": (0.62, 0.80, 0.36), "tank": (0.30, 0.55, 0.80),
    "hump": (0.90, 0.75, 0.10), "station": (0.60, 0.58, 0.55), "airlock": (0.50, 0.52, 0.55),
    "fan_exh": (0.85, 0.40, 0.15), "fan_circ": (0.20, 0.20, 0.22),
}


def fr(v):
    v = round(v, 4)
    if v == 0:
        v = 0.0
    s = f"{v:.4f}".rstrip("0")
    return s


def write_step(path):
    L = []

    def add(txt):
        L.append(txt)
        return len(L)

    def pt(p): return add(f"CARTESIAN_POINT('',({fr(p[0])},{fr(p[1])},{fr(p[2])}))")
    def fd(v):
        v = round(v, 12)
        if v == 0:
            v = 0.0
        t = f"{v:.12f}".rstrip("0")
        return t

    def dr(d): return add(f"DIRECTION('',({fd(d[0])},{fd(d[1])},{fd(d[2])}))")

    ac = add("APPLICATION_CONTEXT('core data for automotive mechanical design processes')")
    add(f"APPLICATION_PROTOCOL_DEFINITION('international standard','automotive_design',2000,#{ac})")
    pc = add(f"PRODUCT_CONTEXT('',#{ac},'mechanical')")
    pr = add(f"PRODUCT('Greenhouse_1','Greenhouse 1','CDE4301 greenhouse model, dimensions in mm',(#{pc}))")
    add(f"PRODUCT_RELATED_PRODUCT_CATEGORY('part',$,(#{pr}))")
    pdf = add(f"PRODUCT_DEFINITION_FORMATION('','',#{pr})")
    pdc = add(f"PRODUCT_DEFINITION_CONTEXT('part definition',#{ac},'design')")
    pd = add(f"PRODUCT_DEFINITION('design','',#{pdf},#{pdc})")
    pds = add(f"PRODUCT_DEFINITION_SHAPE('','',#{pd})")
    lu = add("(LENGTH_UNIT()NAMED_UNIT(*)SI_UNIT(.MILLI.,.METRE.))")
    au = add("(NAMED_UNIT(*)PLANE_ANGLE_UNIT()SI_UNIT($,.RADIAN.))")
    su = add("(NAMED_UNIT(*)SI_UNIT($,.STERADIAN.)SOLID_ANGLE_UNIT())")
    um = add(f"UNCERTAINTY_MEASURE_WITH_UNIT(LENGTH_MEASURE(1.E-2),#{lu},'distance_accuracy_value','confusion accuracy')")
    ctx = add(f"(GEOMETRIC_REPRESENTATION_CONTEXT(3)GLOBAL_UNCERTAINTY_ASSIGNED_CONTEXT((#{um}))"
              f"GLOBAL_UNIT_ASSIGNED_CONTEXT((#{lu},#{au},#{su}))REPRESENTATION_CONTEXT('Context #1','3D Context with UNIT and UNCERTAINTY'))")
    o = pt((0, 0, 0)); dz = dr((0, 0, 1)); dx = dr((1, 0, 0))
    ax0 = add(f"AXIS2_PLACEMENT_3D('',#{o},#{dz},#{dx})")

    brep_ids, styled = [], []
    col_ids = {}
    for sd in solids:
        V = [tuple(c * 1000.0 for c in p) for p in sd["verts"]]
        cp = [pt(p) for p in V]
        vp = [add(f"VERTEX_POINT('',#{c})") for c in cp]
        ecache = {}

        def edge(a, b):
            key = (min(a, b), max(a, b))
            if key not in ecache:
                p, q = V[key[0]], V[key[1]]
                d = sub(q, p)
                ln = math.sqrt(dot(d, d))
                di = dr(norm(d))
                ve = add(f"VECTOR('',#{di},{fr(ln)})")
                li = add(f"LINE('',#{cp[key[0]]},#{ve})")
                ecache[key] = add(f"EDGE_CURVE('',#{vp[key[0]]},#{vp[key[1]]},#{li},.T.)")
            return ecache[key], (a == key[0])

        face_ids = []
        for f in sd["faces"]:
            oes = []
            for i in range(len(f)):
                a, b = f[i], f[(i+1) % len(f)]
                e, same = edge(a, b)
                oes.append(add(f"ORIENTED_EDGE('',*,*,#{e},{'.T.' if same else '.F.'})"))
            loop = add("EDGE_LOOP('',(" + ",".join(f"#{x}" for x in oes) + "))")
            fb = add(f"FACE_OUTER_BOUND('',#{loop},.T.)")
            pts = [V[i] for i in f]
            n = norm(newell(pts))
            ref = norm(sub(pts[1], pts[0]))
            a2 = add(f"AXIS2_PLACEMENT_3D('',#{cp[f[0]]},#{dr(n)},#{dr(ref)})")
            pl = add(f"PLANE('',#{a2})")
            face_ids.append(add(f"ADVANCED_FACE('',(#{fb}),#{pl},.T.)"))
        sh = add("CLOSED_SHELL('',(" + ",".join(f"#{x}" for x in face_ids) + "))")
        br = add(f"MANIFOLD_SOLID_BREP('{sd['name']}',#{sh})")
        brep_ids.append(br)
        cat = sd["cat"]
        if cat not in col_ids:
            r, g, b = COLOURS[cat]
            c = add(f"COLOUR_RGB('{cat}',{fr(r)},{fr(g)},{fr(b)})")
            fc = add(f"FILL_AREA_STYLE_COLOUR('',#{c})")
            fs = add(f"FILL_AREA_STYLE('',(#{fc}))")
            sf = add(f"SURFACE_STYLE_FILL_AREA(#{fs})")
            ss = add(f"SURFACE_SIDE_STYLE('',(#{sf}))")
            uu = add(f"SURFACE_STYLE_USAGE(.BOTH.,#{ss})")
            col_ids[cat] = add(f"PRESENTATION_STYLE_ASSIGNMENT((#{uu}))")
        styled.append(add(f"STYLED_ITEM('',(#{col_ids[cat]}),#{br})"))

    rep = add("ADVANCED_BREP_SHAPE_REPRESENTATION('Greenhouse 1',(#%d,%s),#%d)" %
              (ax0, ",".join(f"#{x}" for x in brep_ids), ctx))
    add(f"SHAPE_DEFINITION_REPRESENTATION(#{pds},#{rep})")
    add("MECHANICAL_DESIGN_GEOMETRIC_PRESENTATION_REPRESENTATION('',(" +
        ",".join(f"#{x}" for x in styled) + f"),#{ctx})")

    with open(path, "w") as fh:
        fh.write("ISO-10303-21;\nHEADER;\n")
        fh.write("FILE_DESCRIPTION(('Greenhouse 1 - envelope, beds, fans. Units: mm. Z up.'),'2;1');\n")
        fh.write("FILE_NAME('greenhouse1.step','2026-11-14T10:00:00',('CDE4301'),(''),'custom writer','custom writer','');\n")
        fh.write("FILE_SCHEMA(('AUTOMOTIVE_DESIGN { 1 0 10303 214 1 1 1 1 }'));\nENDSEC;\nDATA;\n")
        for i, t in enumerate(L, 1):
            fh.write(f"#{i}={t};\n")
        fh.write("ENDSEC;\nEND-ISO-10303-21;\n")
    return len(L)


if __name__ == "__main__":
    out = sys.argv[1]
    n = write_step(f"{out}/greenhouse1.step")
    model = {
        "params": {"W": W, "L_MAIN": L_MAIN, "TH": TH, "R0": R0, "LW": LW, "S_W1": S_W1,
                   "WING_TOP": WING_TOP, "WING_BOT": WING_BOT, "WALL_H": WALL_H, "RIDGE_H": RIDGE_H,
                   "PEAK_H": PEAK_H, "PLANT_H": PLANT_H, "BENCH_H": BENCH_H,
                   "S0": S0, "DS": DS, "T0": T0, "DT": DT, "HUMP_S": HUMP_S, "HUMP_W": HUMP_W},
        "solids": [web_solid(s) for s in solids],
        "fans": fans, "sensors": sensors, "beds": bed_info,
    }
    with open(f"{out}/model.json", "w") as fh:
        json.dump(model, fh, separators=(",", ":"))
    print("solids", len(solids), "step entities", n)
    print("bend angle deg", round(math.degrees(TH), 3), "transition centre length", round(LW, 3))
    print("centreline length", round(S_W1 + (WING_TOP + WING_BOT) / 2, 2))
    xs = [p[0] for s in solids for p in s["verts"]]
    ys = [p[1] for s in solids for p in s["verts"]]
    print("plan extent x", round(min(xs), 2), round(max(xs), 2), "y", round(min(ys), 2), round(max(ys), 2))
    rear = math.dist(P(s_end(0), 0), P(s_end(W), W))
    print("rear wall length", round(rear, 3))
    env = sum(s["vol"] for s in solids if s["name"].startswith("FLOOR")) / 0.1
    print("floor area m2", round(env, 1))
