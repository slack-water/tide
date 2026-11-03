"""clay tube die for a caulk-gun clay extruder.

coordinates: z = 0 is the exit face (downstream, sits against the cap's end
wall). +z points upstream, into the barrel. the part prints in this
orientation: exit face on the bed, no supports.

layout, bottom to top:
  flange    z 0..FLANGE_T     drops into the cap (60 mm ID), clay pressure
                              seats it against the cap's end wall
  land      z 0..LAND         parallel annulus that sets the tube: 35 OD / 27 ID
  flare     z LAND..FLARE_TOP outer wall eases out to the inlet radius (S-curve)
  spider    z ARM_Z0..ARM_Z1  3 arms hold the mandrel; pointed top splits the
                              clay, knife-edge bottom lets it re-knit
  inlet     z ..BODY_H        open mouth, chamfered rim, sits inside the barrel
"""
import math
from pathlib import Path

from build123d import (
    Axis, Cone, chamfer, Cylinder, Edge, Face, Part, Pos, Rot, Spline, Wire,
    export_step, export_stl, extrude, revolve,
)

# --- measured -----------------------------------------------------------------
CAP_ID = 60.5        # cap inside diameter (calipers)
CAP_OPENING = 37.0   # hole in the cap's end wall
BARREL_ID = 51.5     # effective, from fit rings: 49.5 very loose, 51.5 slightly too big

# --- tube ---------------------------------------------------------------------
TUBE_OD = 35.0
TUBE_ID = 27.0                # v7: 29 → 27 for a 4 mm tube wall (OD capped by the 37 mm cap opening)

# --- die ----------------------------------------------------------------------
FIT = 2.1                     # diametral clearance in the cap (v1 at 1.1 was a press fit)
FLANGE_OD = CAP_ID - FIT
FLANGE_T = 4.0                # must be <= gap between barrel rim and cap wall
BODY_OD = BARREL_ID - 1.0     # upstream body slides into the barrel
FLANGE_CHAMFER = 0.8          # bottom edge: eats elephant's foot, leads into the cap
EXIT_CHAMFER = 0.6            # 45° on the exit bore and mandrel bed edges, against elephant's foot
WALL = 3.0                    # body wall at the inlet and spider roots. v6: 2 → 3 (v5 arms tore off the wall)
BODY_H = 54.0                 # total height, exit face to inlet rim (v6: 42 → 54 for longer arms)

LAND = 10.0                   # parallel section at the exit
FLARE_TOP = 24.0              # outer wall reaches inlet radius here
ARM_Z0, ARM_Z1 = 26.0, 50.0   # spider arms: trailing (bottom) to leading (top) edge.
                              # v6: 14 → 24 mm chord (v5 arms bent and tore at both roots)
N_ARMS = 3
ARM_W = 5.0                   # arm thickness (tangential). v6: 3 → 5

MANDREL_CONE_Z0 = ARM_Z1 - 2  # mandrel stays a full-diameter cylinder through the arms
                              # (v5 rooted them on the thin cone, where they hinged)…
MANDREL_TIP_Z = MANDREL_CONE_Z0 + 16.0  # …then cones to a point above them

R_OUT = TUBE_OD / 2
R_MAN = TUBE_ID / 2
R_IN = BODY_OD / 2 - WALL
R_BODY = BODY_OD / 2

assert TUBE_OD < CAP_OPENING, "tube must pass the cap opening"
assert BODY_OD < FLANGE_OD
assert R_IN > R_OUT
assert R_OUT + EXIT_CHAMFER < FLANGE_OD / 2 - FLANGE_CHAMFER
assert BODY_H - 1.6 > ARM_Z1, "arms must root in the straight part of the body wall"


def channel() -> Part:
    """the outer flow boundary, as a solid of revolution to subtract."""
    c = EXIT_CHAMFER
    pts_bottom = [(0, -1), (R_OUT + c + 1, -1), (R_OUT, c), (R_OUT, LAND)]  # 45° bore chamfer
    flare = Spline((R_OUT, 0, LAND), (R_IN, 0, FLARE_TOP),
                   tangents=[(0, 0, 1), (0, 0, 1)])
    pts_top = [(R_IN, FLARE_TOP), (R_IN, BODY_H - 1.6), (R_BODY - 0.2, BODY_H),
               (R_BODY - 0.2, BODY_H + 1), (0, BODY_H + 1)]
    edges = []
    def seg(a, b):
        edges.append(Edge.make_line((a[0], 0, a[1]), (b[0], 0, b[1])))
    for a, b in zip(pts_bottom, pts_bottom[1:]):
        seg(a, b)
    edges.append(flare)
    for a, b in zip(pts_top, pts_top[1:]):
        seg(a, b)
    seg(pts_top[-1], pts_bottom[0])
    face = Face(Wire(edges))
    return revolve(face, Axis.Z, 360)


def mandrel() -> Part:
    cyl = Pos(0, 0, MANDREL_CONE_Z0 / 2) * Cylinder(R_MAN, MANDREL_CONE_Z0)
    foot = cyl.edges().filter_by(lambda e: e.center().Z < 0.01)
    cyl = chamfer(foot, EXIT_CHAMFER)
    h = MANDREL_TIP_Z - MANDREL_CONE_Z0
    cone = Pos(0, 0, MANDREL_CONE_Z0 + h / 2) * Cone(R_MAN, 0.01, h)
    return cyl + cone


def arm() -> Part:
    """streamlined spoke along +x. section in (tangential y, axial z) is a
    teardrop: round nose at the top (leading edge, splits the clay), long
    taper to a small round tip at the bottom (trailing edge — lets the clay
    re-knit, and prints without supports). tangent-continuous so the root
    boolean with the body stays clean."""
    R, r = ARM_W / 2, 0.4
    zt, zb = ARM_Z1 - R, ARM_Z0 + r
    # explicit two-circle tangent hull (build123d's make_hull leaves a
    # degenerate edge here that breaks the boolean with the body)
    sa = (R - r) / (zt - zb)
    ca = math.sqrt(1 - sa * sa)
    P = lambda y, z: (0, y, z)
    t_r, t_l = P(R * ca, zt + R * sa), P(-R * ca, zt + R * sa)
    b_r, b_l = P(r * ca, zb + r * sa), P(-r * ca, zb + r * sa)
    section = Face(Wire([
        Edge.make_three_point_arc(t_r, P(0, zt + R), t_l),
        Edge.make_line(t_l, b_l),
        Edge.make_three_point_arc(b_l, P(0, zb - r), b_r),
        Edge.make_line(b_r, t_r),
    ]))
    # starts on the axis, ends mid-wall
    return extrude(section, amount=R_IN + WALL / 2, dir=(1, 0, 0))


def build() -> Part:
    body = Pos(0, 0, FLANGE_T / 2) * Cylinder(FLANGE_OD / 2, FLANGE_T)
    rim = body.edges().filter_by(lambda e: e.center().Z < 0.01 and e.radius > FLANGE_OD / 2 - 0.01)
    body = chamfer(rim, FLANGE_CHAMFER)
    body += Pos(0, 0, BODY_H / 2) * Cylinder(R_BODY, BODY_H)
    body -= channel()

    core = mandrel()
    for i in range(N_ARMS):
        core += Rot(0, 0, i * 360 / N_ARMS) * arm()
    part = body + core

    return part


if __name__ == "__main__":
    out = Path(__file__).parent
    die = build()
    if not die.is_valid:
        raise SystemExit("die solid is invalid")
    if len(die.solids()) != 1:
        raise SystemExit(f"expected 1 solid, got {len(die.solids())}")
    print(f"volume {die.volume / 1000:.1f} cm³, bbox {die.bounding_box().size}")
    if not export_step(die, out / "clay_tube_die.step"):
        raise SystemExit("step export failed")
    if not export_stl(die, out / "clay_tube_die.stl", tolerance=0.01, angular_tolerance=0.1):
        raise SystemExit("stl export failed")
