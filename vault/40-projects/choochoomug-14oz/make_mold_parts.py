#!/usr/bin/env python3
"""The 14 oz choochoomug as exact build123d geometry, and the positives the plaster molds are cast
around. Everything is built from the dimensions below; choochoomug-14oz.step (scale_mug.py output)
is only read to check that the analytic body and handle match it.

Axis = Z, foot ring at Z=0, handle on +X, handle mid-plane = Y=0.

The body is a revolve: foot cone, a fillet onto the belly, a 3.6 degree wall, a small rim round, a
flat top, and the dish underneath (a spline; it is neither a circle nor a parabola). The handle is a
stadium cross-section (11.538 x 23.078) swept around a half circle about an axis parallel to Y at the
belly; its roots end in the plane x = HANDLE_CX.

  body             the mug without its handle. Reference only.
  body_positive    body + filled dish + grooved socket boss below the foot + reservoir collar on
                   the rim. Both plaster side halves are cast around this (make_masters.py).
  handle_positive  the handle, both roots extended along -X as straight sprues that flare into
                   pour cups at the pour face (x = SPRUE_END). The handle mold is cast around this.
  plug_floor       printed disc with the dish pit; the plug is cast dish-down on it. A SKIN-thick
                   pit on concentric SKIN rings, open underneath.
  plug_ring        half of the split ring that walls the plug; print two. A SKIN-thick wall that
                   follows the plug's V-groove, which is why the ring has to split.

Setup:  python3 -m venv .venv && .venv/bin/pip install build123d
Usage:  .venv/bin/python make_mold_parts.py
"""
import math
import random
from pathlib import Path

from build123d import (Align, Axis, BuildLine, BuildSketch, Circle, Kind, Line, Locations, Mode, Plane,
                       Polyline, Pos,
                       Rectangle, Rot, SlotOverall, Spline, ThreePointArc, Transition, Wire,
                       export_step, export_stl, import_step, loft, make_face, mirror, offset,
                       revolve, section, sweep)

HERE = Path(__file__).parent
OZ = 29573.5
SKIN = 1.2            # every printed molding surface; 3 lines at 0.4 mm

# --- body, measured from choochoomug-14oz.step (r, z) ---
R_RING = 41.96                          # foot ring = dish edge
DISH = [(0.0, 4.196), (5.2754, 4.0971), (10.5453, 3.836), (15.8059, 3.4282), (21.0556, 2.8978),
        (26.2947, 2.2708), (31.5245, 1.5696), (36.746, 0.8099), (41.96, 0.0)]
DISH_T = ((1.0, 0.0), (0.987433, -0.158038))   # dish tangents at the centre and the foot ring
FOOT_TOP = (51.598, 7.7104)             # foot cone R_RING,0 -> here, then a fillet
BELLY_FILLET = ((50.2874, 9.3487), 2.098)
BELLY = (52.3812, 9.4809)               # widest point; the 3.61 degree wall starts here
WALL_TOP = (46.187, 107.5556)
RIM_ROUND = ((45.6636, 107.5225), 0.5245)
Z_RIM = 108.047
R_RIM = 45.6636                         # rim radius at the flat top
R_MAX = BELLY[0]

# --- handle, measured from choochoomug-14oz.step ---
HANDLE_CX, HANDLE_CZ = 52.41782, 58.49622   # sweep axis, parallel to Y
HANDLE_R = (31.35067 + 42.8892) / 2         # centre line radius
HANDLE_W = 42.8892 - 31.35067               # radial width (11.538)
HANDLE_L = 23.078                           # thickness along Y (semicircle ends, radius W/2)

# --- design parameters (mm) ---
SOCKET_DEPTH = 25.0   # plug body below the foot ring
GROOVE_Z = -12.5      # V-groove centre on the socket boss; locks the plug between the halves
GROOVE_DEPTH = 3.0    # 45 degree flanks, so 6 mm tall at the boss surface
COLLAR_STEP = 4.0     # reservoir steps out this far from the rim, on a 45 degree chamfer
COLLAR_H = 30.0       # reservoir height above the rim (~200 mL against 150-200 mL slip loss)
SPRUE_END = 37.0      # sprues end here; this is the handle mold's pour face
CUP_DEPTH = 10.0      # each sprue flares into a pour cup over its last CUP_DEPTH mm
CUP_GROW = 5.0        # the cup mouth is this much wider than the sprue on every side
RING_CLEAR = 0.3
LIP = 3.0             # floor lip that locates the ring halves
FLOOR = 3.0           # plug floor under the deepest point of the dish pit
FLOOR_RIBS = (10.0, 20.0, 30.0)   # concentric ribs under the pit skin

Z_TOP = Z_RIM + COLLAR_H
R_COLLAR = R_RIM + COLLAR_STEP


# ---------------- 2D profiles (r along x, z along y of Plane.XZ) ----------------

def arc_mid(centre, radius, a, b):
    """Midpoint of the short arc from a to b about centre."""
    cx, cz = centre
    t0 = math.atan2(a[1] - cz, a[0] - cx)
    t1 = math.atan2(b[1] - cz, b[0] - cx)
    d = (t1 - t0 + math.pi) % (2 * math.pi) - math.pi
    return (cx + radius * math.cos(t0 + d / 2), cz + radius * math.sin(t0 + d / 2))


def outline_face(build):
    """Face on Plane.XZ from a function that adds a closed run of edges inside a BuildLine."""
    with BuildSketch(Plane.XZ) as s:
        with BuildLine():
            build()
        make_face()
    return s.sketch.face()


def rect(r0, r1, z0, z1):
    return outline_face(lambda: Polyline((r0, z0), (r1, z0), (r1, z1), (r0, z1), (r0, z0)))


def wall_edges(start):
    """Foot cone, belly fillet, wall, rim round: from `start` (the foot ring) to the rim top."""
    Line(start, FOOT_TOP)
    ThreePointArc(FOOT_TOP, arc_mid(*BELLY_FILLET, FOOT_TOP, BELLY), BELLY)
    Line(BELLY, WALL_TOP)
    ThreePointArc(WALL_TOP, arc_mid(*RIM_ROUND, WALL_TOP, (R_RIM, Z_RIM)), (R_RIM, Z_RIM))


def groove_pts():
    g0, g1 = GROOVE_Z - GROOVE_DEPTH, GROOVE_Z + GROOVE_DEPTH
    return [(0, -SOCKET_DEPTH), (R_RING, -SOCKET_DEPTH), (R_RING, g0), (R_RING - GROOVE_DEPTH, GROOVE_Z),
            (R_RING, g1), (R_RING, 0)]


def body_profile():
    def b():
        Spline(*DISH, tangents=DISH_T)
        wall_edges((R_RING, 0))
        Polyline((R_RIM, Z_RIM), (0, Z_RIM), DISH[0])
    return outline_face(b)


def positive_profile():
    """Body with the dish filled, the grooved socket below, and the reservoir collar above."""
    def b():
        Polyline(*groove_pts())
        wall_edges((R_RING, 0))
        Polyline((R_RIM, Z_RIM), (R_COLLAR, Z_RIM + COLLAR_STEP), (R_COLLAR, Z_TOP), (0, Z_TOP),
                 (0, -SOCKET_DEPTH))
    return outline_face(b)


def plug_profile():
    def b():
        Polyline(*groove_pts())
        Spline(*reversed(DISH), tangents=[(-DISH_T[1][0], -DISH_T[1][1]), (-1, 0)])
        Line(DISH[0], (0, -SOCKET_DEPTH))
    return outline_face(b)


def socket_profile():
    """The plug's side region without the dish: the groove line out from the axis."""
    return outline_face(lambda: Polyline(*groove_pts(), (0, 0), (0, -SOCKET_DEPTH)))


def revolve_half(face):
    """Revolve a profile 180 degrees about Z into the Y >= 0 half."""
    part = revolve(face, Axis.Z, 180)
    if part.bounding_box().min.Y < -1e-3:
        part = mirror(part, about=Plane.XZ)
    return part


def side_chain():
    """The positive's outside, bottom to top, as ('line', p, q) and ('arc', centre, radius, p, q)."""
    g = groove_pts()[1:]
    chain = [("line", g[i], g[i + 1]) for i in range(len(g) - 1)]
    chain += [("line", (R_RING, 0), FOOT_TOP), ("arc", *BELLY_FILLET, FOOT_TOP, BELLY),
              ("line", BELLY, WALL_TOP), ("arc", *RIM_ROUND, WALL_TOP, (R_RIM, Z_RIM)),
              ("line", (R_RIM, Z_RIM), (R_COLLAR, Z_RIM + COLLAR_STEP)),
              ("line", (R_COLLAR, Z_RIM + COLLAR_STEP), (R_COLLAR, Z_TOP))]
    return chain


def disc(c, r):
    with BuildSketch(Plane.XZ) as s:
        with Locations((c[0], c[1])):
            Circle(r)
    return s.sketch.face()


def sausage(edge, d):
    """Everything within d of one chain edge (its Minkowski sum with a disc of radius d)."""
    if edge[0] == "line":
        _, p, q = edge
        L = math.dist(p, q)
        with BuildSketch(Plane.XZ) as s:
            with Locations(((p[0] + q[0]) / 2, (p[1] + q[1]) / 2)):
                Rectangle(L, 2 * d, rotation=math.degrees(math.atan2(q[1] - p[1], q[0] - p[0])))
        return s.sketch.face() + disc(p, d) + disc(q, d)
    _, c, r, p, q = edge
    ring = disc(c, r + d) - disc(c, r - d) if r > d else disc(c, r + d)
    far = 4 * (r + d)                       # wedge from the centre through both arc ends (arcs < 180 deg)
    ang = lambda pt: math.atan2(pt[1] - c[1], pt[0] - c[0])
    a0, a1 = ang(p), ang(q)
    span = (a1 - a0 + math.pi) % (2 * math.pi) - math.pi
    pts = [c] + [(c[0] + far * math.cos(a0 + span * t / 4), c[1] + far * math.sin(a0 + span * t / 4))
                 for t in range(5)]
    wedge = outline_face(lambda: Polyline(*pts, c))
    return (ring & wedge) + disc(p, d) + disc(q, d)


def positive_inner_profile(skin=SKIN):
    """Profile of the body master's hollow: everything inside the positive's outside at least `skin`
    from it (an exact 2D offset: the region minus a `skin` sausage around every edge), run 5 mm past
    both ends so the hollow is open there (the cottle end walls close it)."""
    zb, zt = -SOCKET_DEPTH - 5, Z_TOP + 5
    chain = side_chain()

    def b():
        Line((0, zb), (R_RING, zb))
        Line((R_RING, zb), chain[0][1])
        for e in chain:
            if e[0] == "line":
                Line(e[1], e[2])
            else:
                ThreePointArc(e[3], arc_mid(e[1], e[2], e[3], e[4]), e[4])
        Polyline(chain[-1][2], (R_COLLAR, zt), (0, zt), (0, zb))
    region = outline_face(b)
    edges = [("line", (R_RING, zb), chain[0][1])] + chain + [("line", chain[-1][2], (R_COLLAR, zt))]
    for e in edges:
        region = region - sausage(e, skin)
    return region


# ---------------- handle ----------------

def stadium(origin, length, width, half=False):
    """Stadium in the plane x = origin.x: `length` along Y, `width` along Z. half keeps Y >= 0."""
    pl = Plane(origin=origin, x_dir=(0, 1, 0), z_dir=(1, 0, 0))
    with BuildSketch(pl) as s:
        SlotOverall(length, width)
        if half:
            Rectangle(length, width + 2, align=(Align.MIN, Align.CENTER), mode=Mode.INTERSECT)
    return s.sketch.face()


def handle_path(x_end):
    cx, cz, r = HANDLE_CX, HANDLE_CZ, HANDLE_R
    return Wire([Line((x_end, 0, cz - r), (cx, 0, cz - r)),
                 ThreePointArc((cx, 0, cz - r), (cx + r, 0, cz), (cx, 0, cz + r)),
                 Line((cx, 0, cz + r), (x_end, 0, cz + r))])


def handle_solid(length=HANDLE_L, width=HANDLE_W, cup_inset=0.0, half=False, open_cups=0.0):
    """Handle + sprues swept from x = SPRUE_END + CUP_DEPTH, plus a pour cup lofted on each end.
    cup_inset shrinks the cups (on every side) relative to the sweep; open_cups runs them that much
    past the pour face."""
    x1 = SPRUE_END + CUP_DEPTH
    zs = (HANDLE_CZ - HANDLE_R, HANDLE_CZ + HANDLE_R)
    body = sweep(stadium((x1, 0, zs[0]), length, width, half), path=handle_path(x1),
                 transition=Transition.RIGHT)
    grow = CUP_GROW * (CUP_DEPTH + open_cups) / CUP_DEPTH
    cups = [loft([stadium((x1, 0, z), length - 2 * cup_inset, width - 2 * cup_inset, half),
                  stadium((SPRUE_END - open_cups, 0, z), length - 2 * cup_inset + 2 * grow,
                          width - 2 * cup_inset + 2 * grow, half)]) for z in zs]
    return body.fuse(*cups)


def handle_inner(skin=SKIN):
    """The handle master's hollow: the stadium offset by `skin` (an exact offset of a stadium is a
    stadium), cups offset by skin / cos(flare) so the flared wall is still `skin` thick, open at the
    pour face. Full, not half: its lower half runs out through the plate back."""
    k = 1 / math.cos(math.atan(CUP_GROW / CUP_DEPTH))
    return handle_solid(HANDLE_L - 2 * skin, HANDLE_W - 2 * skin, cup_inset=skin * (k - 1), open_cups=1.0)


# ---------------- plug mold ----------------

def plug_floor_profile():
    """Floor, in the flipped frame (bed at z = 0, plug dish-down): a SKIN pit on concentric SKIN
    rings, a solid ledge for the ring halves, and the locating lip."""
    z_ring = FLOOR + DISH[0][1]                          # foot-ring plane after the flip
    pit = [(r, z_ring - z) for r, z in DISH]              # dish pit, deepest (z = FLOOR) at the centre
    r_lip = R_RING + SKIN + RING_CLEAR

    def b():
        Spline(*pit, tangents=[(1, 0), (DISH_T[1][0], -DISH_T[1][1])])
        Polyline((R_RING, z_ring), (r_lip, z_ring), (r_lip, z_ring + 4), (r_lip + LIP, z_ring + 4),
                 (r_lip + LIP, 0), (0, 0), pit[0])
    solid = outline_face(b)
    under = [(r, z - SKIN) for r, z in pit[:-1]] + [(R_RING - SKIN, pit[-1][1] - SKIN)]

    def v():
        Spline(*under, tangents=[(1, 0), (DISH_T[1][0], -DISH_T[1][1])])
        Polyline(under[-1], (under[-1][0], -1), (0, -1), under[0])
    void = outline_face(v)
    for r in FLOOR_RIBS:
        void = void - rect(r - SKIN / 2, r + SKIN / 2, -5, 20)
    return solid - void, z_ring


def plug_ring_profile():
    """A SKIN wall outside the plug's side that follows the V-groove (an outward offset of the
    socket profile), between the plug's flat bottom and the foot-ring plane."""
    s = socket_profile()
    band = offset(s, amount=SKIN, kind=Kind.INTERSECTION) - s
    return band & rect(0, 200, -SOCKET_DEPTH, 0)


# ---------------- checks and output ----------------

def save(name, solid):
    export_step(solid, HERE / f"{name}.step")
    export_stl(solid, HERE / f"{name}.stl", tolerance=0.02, angular_tolerance=0.15)
    bb = solid.bounding_box()
    print(f"{name:16s} {bb.size.X:6.1f} x {bb.size.Y:6.1f} x {bb.size.Z:6.1f} mm   "
          f"vol {solid.volume/1000:7.1f} cm3   solids={len(solid.solids())} valid={solid.is_valid}")


def compare(name, ours, ref, box, n=1500, seed=1):
    """Point-sample `box` and count where `ours` and the reference STEP disagree."""
    rnd = random.Random(seed)
    lo, hi = box
    hits = bad = 0
    while hits < n:
        p = tuple(rnd.uniform(lo[i], hi[i]) for i in range(3))
        a, b = ours.is_inside(p), ref.is_inside(p)
        if a or b:
            hits += 1
            bad += a != b
    print(f"{name}: {bad} of {n} sampled points disagree with choochoomug-14oz.step (want 0)")
    return bad


def compare_handle(ours, ref, angles=(-80, -45, 0, 30, 60, 85)):
    """Section both handles in radial planes through the sweep axis and compare. (Point sampling is
    unreliable here: OCC's classifier reports false insides near Fusion's B-spline crown faces.)"""
    worst = 0.0
    for deg in angles:
        a = math.radians(deg)
        pl = Plane(origin=(HANDLE_CX, 0, HANDLE_CZ), x_dir=(math.cos(a), 0, math.sin(a)),
                   z_dir=(-math.sin(a), 0, math.cos(a)))
        def sec(shape):
            f = [f for f in section(shape, pl).faces() if pl.to_local_coords(f.center()).X > 20]
            assert len(f) == 1, f"expected one handle section at {deg} degrees"
            pts = [pl.to_local_coords(e.position_at(t / 20)) for e in f[0].edges() for t in range(21)]
            return f[0].area, min(q.X for q in pts), max(q.X for q in pts), max(abs(q.Y) for q in pts)
        o, r = sec(ours), sec(ref)
        worst = max(worst, max(abs(x - y) for x, y in zip(o[1:], r[1:])))
        assert abs(o[0] - r[0]) < 0.5, f"handle section area differs at {deg} degrees: {o[0]:.2f} vs {r[0]:.2f}"
    print(f"handle: sections at {len(angles)} angles match choochoomug-14oz.step "
          f"(area within 0.5 mm2, extents within {worst:.3f} mm)")


def main():
    body = revolve(body_profile(), Axis.Z)
    body_pos = revolve(positive_profile(), Axis.Z)
    handle_pos = handle_solid()
    plug = revolve(plug_profile(), Axis.Z)

    floor_face, z_ring = plug_floor_profile()
    plug_floor = revolve(floor_face, Axis.Z)
    # ring halves sit on the floor ledge around the flipped plug; print on the foot-ring end
    ring_half = Rot(180, 0, 0) * revolve_half(plug_ring_profile())
    ring_half = Pos(0, 0, -ring_half.bounding_box().min.Z) * ring_half

    # ---- checks ----
    ref = import_step(HERE / "choochoomug-14oz.step")
    compare("body (y > 12, clear of the handle and the Fusion split strip)", body, ref,
            ((-55, 12, -1), (55, 55, 110)))
    compare_handle(handle_pos, ref)
    print(f"body {body.volume / OZ:.2f} fl oz solid; plug {plug.volume / 1000:.0f} cm3 of plaster; "
          f"reservoir above the rim ~{math.pi * R_COLLAR**2 * (COLLAR_H - COLLAR_STEP) / 1000:.0f} mL")
    flipped = Pos(0, 0, z_ring) * Rot(180, 0, 0) * plug
    common = flipped & plug_floor
    print(f"flipped plug vs floor: overlap {common.volume if common else 0:.2f} mm3 (want 0), "
          f"pit floor at z {FLOOR} touches the plug: {flipped.is_inside((0, 0, FLOOR + 0.05))}")

    save("body", body)
    save("body_positive", body_pos)
    save("handle_positive", handle_pos)
    save("plug_floor", plug_floor)
    save("plug_ring", ring_half)


if __name__ == "__main__":
    main()
