#!/usr/bin/env python3
"""Mold-making parts for the 14 oz choochoomug (run scale_mug.py first).

Axis = Z, base ring at Z=0, handle plane = Y=0 (the parting plane of the two halves).
Writes STEP + STL for three printed parts:

  halves_positive  mug + dish filled + tapered socket boss below the foot + funnel-seat boss
                   on the rim. Cast the two plaster side halves around this.
  plug_cup         shallow printed cup; plaster poured in makes the foot plug (dish bump).
                   The plug sits in the halves' socket and is captured between them.
  funnel           printed pour reservoir. Foot seats in the pocket the seat boss leaves in
                   the plaster top; bore equals the rim so the cast ends at the plaster edge.

Setup:  .venv/bin/pip install build123d trimesh
Usage:  .venv/bin/python make_mold_parts.py
"""
import math
from pathlib import Path

import trimesh
from build123d import (Align, Axis, BuildLine, BuildPart, BuildSketch, Cone, Cylinder,
                       Plane, Polyline, Pos, Rot, Solid, export_step, export_stl,
                       import_step, make_face, revolve)

HERE = Path(__file__).parent
OZ = 29573.5

# --- measured from choochoomug-14oz.step ---
R_RING = 41.96     # dish edge / foot ring radius at Z=0
Z_RIM = 108.047    # flat top = pour opening
R_RIM = 45.85      # rim radius (pour opening)

# --- design parameters (mm) ---
SOCKET_DEPTH = 25.0   # plug body below the foot ring
SOCKET_TAPER = 2.0    # deg; plug WIDER toward its flat bottom so it can leave its casting cup
CLEAR = 0.3           # printed-funnel-to-pocket radial clearance
SEAT_R = 50.0         # funnel pocket radius in the plaster top
SEAT_DEPTH = 8.0      # funnel foot height / pocket depth
COLLAR_H = 35.0       # straight bore above the plaster top (reservoir ~ 230 mL)
FLARE_H = 25.0        # flare height
FLARE_R = 58.0        # bore radius at the mouth
WALL = 3.0            # funnel wall above the foot
CUP_WALL = 4.0
CUP_FLOOR = 3.0


def cone_down(r_top, depth, taper_deg):
    """Solid of revolution, top face at Z=0 radius r_top, widening downward to Z=-depth."""
    r_bot = r_top + depth * math.tan(math.radians(taper_deg))
    return Pos(0, 0, -depth) * Cone(r_bot, r_top, depth, align=(Align.CENTER, Align.CENTER, Align.MIN))


def save(name, solid):
    export_step(solid, HERE / f"{name}.step")
    stl = HERE / f"{name}.stl"
    export_stl(solid, stl, tolerance=0.02, angular_tolerance=0.15)
    m = trimesh.load(stl)               # drop zero-length pole edges from tessellation
    m.update_faces(m.nondegenerate_faces(height=1e-6))
    m.remove_unreferenced_vertices()
    trimesh.repair.fix_winding(m)
    trimesh.repair.fill_holes(m)
    m.export(stl)
    bb = solid.bounding_box()
    print(f"{name:16s} {bb.size.X:6.1f} x {bb.size.Y:6.1f} x {bb.size.Z:6.1f} mm   "
          f"vol {solid.volume/1000:7.1f} cm3   watertight={m.is_watertight}")
    return m


def main():
    mug = import_step(HERE / "choochoomug-14oz.step")
    assert isinstance(mug, Solid)

    # ---- foot: dish fill + socket boss; the plug is the part of that below the dish ----
    fill = Cylinder(R_RING, 4.6, align=(Align.CENTER, Align.CENTER, Align.MIN))
    boss = cone_down(R_RING, SOCKET_DEPTH, SOCKET_TAPER)
    plug = (boss + fill) - mug              # top face = the mug's own dish surface

    # ---- funnel seat boss on the rim ----
    seat = Pos(0, 0, Z_RIM) * Cylinder(SEAT_R, SEAT_DEPTH, align=(Align.CENTER, Align.CENTER, Align.MIN))

    halves_pos = mug + boss + fill + seat
    halves_pos = halves_pos.clean()

    # ---- plug cup: plug flipped dish-down inside a printed cup ----
    plug_flip = Rot(180, 0, 0) * plug       # dish now faces down
    plug_bb = plug_flip.bounding_box()
    outer_r = plug_bb.max.X + CUP_WALL
    # flipped plug spans Z in [-top, +SOCKET_DEPTH]; put the dish pit's lowest point CUP_FLOOR above the bed
    z_shift = CUP_FLOOR - plug_bb.min.Z
    cup_h = plug_bb.size.Z + CUP_FLOOR
    cup_body = Cylinder(outer_r, cup_h, align=(Align.CENTER, Align.CENTER, Align.MIN))
    cup = cup_body - (Pos(0, 0, z_shift) * plug_flip)
    # extend the cavity through the open top so it's a cup, not a sealed void
    cup = cup - Pos(0, 0, z_shift + plug_bb.max.Z - 0.01) * Cylinder(
        plug_bb.max.X + 0.2, 5, align=(Align.CENTER, Align.CENTER, Align.MIN))

    # ---- funnel (revolved profile, foot down) ----
    r_foot = SEAT_R - CLEAR
    h0, h1, h2 = SEAT_DEPTH, SEAT_DEPTH + COLLAR_H, SEAT_DEPTH + COLLAR_H + FLARE_H
    # inner bore = rim radius up to h1, then flares; foot (r_foot) seats in the plaster pocket,
    # then the outer steps in to a WALL-thick collar that follows the bore
    pts = [(R_RIM, 0), (r_foot, 0), (r_foot, h0), (R_RIM + WALL, h0),
           (R_RIM + WALL, h1), (FLARE_R + WALL, h2), (FLARE_R, h2), (R_RIM, h1)]
    with BuildPart() as fb:
        with BuildSketch(Plane.XZ):
            with BuildLine():
                Polyline(*pts, close=True)
            make_face()
        revolve(axis=Axis.Z)
    funnel = fb.part

    # ---- checks ----
    cavity = halves_pos - plug                        # what the halves actually form
    restored = cavity - seat
    diff = (restored - mug).volume + (mug - restored).volume
    print(f"halves cavity minus seat vs mug: symmetric difference {diff:.2f} mm3 (want ~0)")
    seated = Pos(0, 0, Z_RIM) * funnel               # funnel as it sits on the rim ledge
    print(f"funnel intrudes into mug cavity: {(seated & mug).volume:.2f} mm3 (want 0)")
    foot = seated & (Pos(0, 0, Z_RIM) * Cylinder(80, SEAT_DEPTH, align=(Align.CENTER, Align.CENTER, Align.MIN)))
    print(f"funnel foot outside the pocket: {(foot - seat).volume:.2f} mm3 (want 0), "
          f"foot volume {foot.volume:.0f} mm3")
    res_ml = math.pi * R_RIM**2 * COLLAR_H / 1000
    print(f"funnel straight-bore reservoir: {res_ml:.0f} mL")

    save("halves_positive", halves_pos)
    save("plug_preview", plug)     # for checking only; not printed
    save("plug_cup", cup)
    save("funnel", funnel)


if __name__ == "__main__":
    main()
