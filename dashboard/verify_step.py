"""Independent check of the STEP file: parse it back and test topology and geometry."""
import re, sys, math, collections
txt = open(sys.argv[1]).read()
assert txt.startswith("ISO-10303-21;") and txt.rstrip().endswith("END-ISO-10303-21;")
data = txt.split("DATA;")[1].split("ENDSEC;")[0]
ents = {}
for m in re.finditer(r"#(\d+)=(.*?);\n", data, re.S):
    ents[int(m.group(1))] = m.group(2)
refs_ok = all(int(r) in ents for body in ents.values() for r in re.findall(r"#(\d+)", body))
print("entities", len(ents), "all references resolve:", refs_ok)
def typ(i): return ents[i].split("(")[0]
def refs(i): return [int(r) for r in re.findall(r"#(\d+)", ents[i])]
def nums(i): return [float(x) for x in re.findall(r"-?\d+\.\d*(?:E-?\d+)?", ents[i].split("',",1)[1])]
def point(i): assert typ(i)=="CARTESIAN_POINT"; return tuple(nums(i))
def direction(i): assert typ(i)=="DIRECTION"; return tuple(nums(i))
def sub(a,b): return tuple(x-y for x,y in zip(a,b))
def dot(a,b): return sum(x*y for x,y in zip(a,b))
def cross(a,b): return (a[1]*b[2]-a[2]*b[1],a[2]*b[0]-a[0]*b[2],a[0]*b[1]-a[1]*b[0])
breps=[i for i in ents if typ(i)=="MANIFOLD_SOLID_BREP"]
bad=0; total=0.0; rows=[]
for b in breps:
    name=re.search(r"'(.*?)'",ents[b]).group(1)
    shell=refs(b)[0]; assert typ(shell)=="CLOSED_SHELL"
    use=collections.Counter(); vol=0.0; V=set(); E=set(); F=0; maxdev=0.0; maxlen=0.0
    for f in refs(shell):
        assert typ(f)=="ADVANCED_FACE" and ents[f].endswith(".T.)")
        fb, pl = refs(f); assert typ(fb)=="FACE_OUTER_BOUND" and typ(pl)=="PLANE"
        a2=refs(pl)[0]; o,nz,nx=refs(a2); o=point(o); n=direction(nz); xr=direction(nx)
        assert abs(dot(n,n)-1)<1e-9 and abs(dot(n,xr))<1e-3, (dot(n,n),dot(n,xr))
        loop=refs(fb)[0]; pts=[]
        prev_end=None; first_start=None
        for oe in refs(loop):
            assert typ(oe)=="ORIENTED_EDGE"
            ec=refs(oe)[0]; same=ents[oe].endswith(".T.)")
            v1,v2,ln=refs(ec); p1=point(refs(v1)[0]); p2=point(refs(v2)[0])
            lp,vec=refs(ln); d=direction(refs(vec)[0]); L=float(re.findall(r",(-?\d+\.\d*)\)$",ents[vec])[0])
            # line really joins the two vertices
            err=max(abs(point(lp)[k]+d[k]*L-p2[k]) for k in range(3)); maxlen=max(maxlen,err)
            assert point(lp)==p1
            a,bv=(p1,p2) if same else (p2,p1)
            use[(ec,same)]+=1; E.add(ec); V.add(v1); V.add(v2)
            if prev_end is not None: assert prev_end==a, "loop not connected"
            if first_start is None: first_start=a
            prev_end=bv; pts.append(a)
        assert prev_end==first_start, "loop not closed"
        F+=1
        # planarity and orientation (loop counter-clockwise about the plane normal)
        nn=[0,0,0]
        for k in range(len(pts)):
            p,q=pts[k],pts[(k+1)%len(pts)]
            nn[0]+=(p[1]-q[1])*(p[2]+q[2]); nn[1]+=(p[2]-q[2])*(p[0]+q[0]); nn[2]+=(p[0]-q[0])*(p[1]+q[1])
        assert dot(nn,n)>0, "face orientation"
        maxdev=max(maxdev,max(abs(dot(n,sub(p,o))) for p in pts))
        for k in range(1,len(pts)-1): vol+=dot(pts[0],cross(pts[k],pts[k+1]))/6
    twice=all(use[(e,True)]==1 and use[(e,False)]==1 for e in E)
    euler=len(V)-len(E)+F
    ok = twice and euler==2 and vol>0 and maxdev<0.01 and maxlen<0.01
    bad+= (not ok); total+=vol
    rows.append((name,len(V),len(E),F,vol/1e9,maxdev,maxlen,ok))
print("solids", len(breps), "failing", bad)
print("worst planarity deviation (mm)", max(r[5] for r in rows), " worst edge end error (mm)", max(r[6] for r in rows))
for r in rows:
    if not r[7] or r[0] in ("FLOOR_MAIN","END_WALL_FRONT","AIRLOCK_FRONT","CIRCULATING_FAN_4","BED_GERMINATION","ROOF_TOP_TRANSITION"):
        print("  %-28s V=%d E=%d F=%d vol=%.4f m3 ok=%s"%(r[0],r[1],r[2],r[3],r[4],r[7]))
styled=[i for i in ents if typ(i)=="STYLED_ITEM"]; print("styled items", len(styled))
