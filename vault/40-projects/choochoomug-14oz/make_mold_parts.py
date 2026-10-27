#!/usr/bin/env python3
"""Split the 14 oz choochoomug into a handleless body and a separate handle, and build the
positives the plaster molds are cast around (run scale_mug.py first).

Axis = Z, foot ring at Z=0, handle on +X, handle mid-plane = Y=0.

  body             the mug without its handle: the +Y profile revolved (the +Y side has no handle
                   and no Fusion split strip). Reference only.
  body_positive    body + filled dish + grooved socket boss below the foot + reservoir collar on
                   the rim. Both plaster side halves are cast around this (make_masters.py).
  handle_positive  the handle cut at the body surface, with both roots extended along -X into
                   sprues. The handle's own 2-part plaster mold is cast around this.
  plug_floor       printed disc with the dish pit; the plug is cast dish-down on it.
  plug_ring        half of the split ring that walls the plug; print two. Its V ridge forms the
                   plug's groove, which is why the ring has to split.

Setup:  python3 -m venv .venv && .venv/bin/pip install build123d trimesh
Usage:  .venv/bin/python make_mold_parts.py
"""
import math
from pathlib import Path

import trimesh
from build123d import (Align, Axis, Box, BuildLine, BuildPart, BuildSketch, Cylinder, Plane,
                       Polyline, Pos, Rot, Solid, export_step, export_stl, extrude, import_step,
                       make_face, revolve, scale, section)

HERE = Path(__file__).parent
OZ = 29573.5
MIN = (Align.CENTER, Align.CENTER, Align.MIN)

# --- measured from choochoomug-14oz.step ---
R_RING = 41.96     # dish edge / foot ring radius at Z=0
DISH_H = 4.2       # dish rise at the centre
Z_RIM = 108.047    # flat top = pour opening
R_RIM = 45.66      # rim radius at the top face
R_MAX = 52.39      # belly radius (Z=9.5)

# --- design parameters (mm) ---
SOCKET_DEPTH = 25.0   # plug body below the foot ring
GROOVE_Z = -12.5      # V-groove centre on the socket boss; locks the plug between the halves
GROOVE_DEPTH = 3.0    # 45 degree flanks, so 6 mm tall at the boss surface
COLLAR_STEP = 4.0     # reservoir steps out this far from the rim, on a 45 degree chamfer
COLLAR_H = 30.0       # reservoir height above the rim (~200 mL against 150-200 mL slip loss)
SPRUE_X = 52.6        # handle section taken here (just past the belly) and extruded toward -X
SPRUE_END = 37.0      # sprues end here; this is the handle mold's pour face
RING_WALL = 4.0
RING_CLEAR = 0.3
LIP = 3.0             # floor lip that locates the ring halves
FLOOR = 3.0           # plug floor under the dish pit


def revolved(pts):
    """Revolve a closed (r, z) polyline about Z."""
    with BuildPart() as b:
        with BuildSketch(Plane.XZ):
            with BuildLine():
                Polyline(*pts, close=True)
            make_face()
        revolve(axis=Axis.Z)
    return b.part


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

    # ---- body: revolve the +Y half of the YZ section ----
    sec = max(section(mug, Plane.YZ).faces(), key=lambda f: f.area)
    half_sec = sec & Box(1, 400, 400, align=(Align.CENTER, Align.MIN, Align.CENTER))
    body = revolve(half_sec, Axis.Z)

    # ---- handle: whatever of the mug lies outside a 0.5 mm oversize body ----
    # (the oversize drops the 0.04 mm Fusion split strip that runs the full height at +-X)
    oversize = scale(body, by=((R_MAX + 0.5) / R_MAX, (R_MAX + 0.5) / R_MAX, 1))
    handle = max((mug - oversize).solids(), key=lambda s: s.volume)
    root_secs = section(handle, Plane.YZ.offset(SPRUE_X)).faces()
    assert len(root_secs) == 2, f"expected two handle roots at x={SPRUE_X}, got {len(root_secs)}"
    sprues = [extrude(f, amount=SPRUE_X - SPRUE_END, dir=(-1, 0, 0)) for f in root_secs]
    # a plain fuse here is flaky (sometimes returns a lone sprue or nothing); the fuzzy one is stable
    handle_pos = handle.fuse(*sprues, tol=0.01)
    added = handle_pos.volume - handle.volume
    assert len(handle_pos.solids()) == 1 and added > 0.75 * sum(s.volume for s in sprues), \
        f"handle + sprues fuse failed: {len(handle_pos.solids())} solids, {added:.0f} mm3 added"

    # ---- foot: dish fill + grooved socket boss; the plug is the part of that below the dish ----
    fill = Cylinder(R_RING, DISH_H + 0.4, align=MIN)
    g0, g1 = GROOVE_Z - GROOVE_DEPTH, GROOVE_Z + GROOVE_DEPTH
    boss = revolved([(0, -SOCKET_DEPTH), (R_RING, -SOCKET_DEPTH), (R_RING, g0),
                     (R_RING - GROOVE_DEPTH, GROOVE_Z), (R_RING, g1), (R_RING, 0), (0, 0)])
    plug = (boss + fill) - body              # top face = the mug's own dish surface

    # ---- reservoir collar: 45 degree step out from the rim, then straight up ----
    rc = R_RIM + COLLAR_STEP
    collar = revolved([(0, Z_RIM), (R_RIM, Z_RIM), (rc, Z_RIM + COLLAR_STEP),
                       (rc, Z_RIM + COLLAR_H), (0, Z_RIM + COLLAR_H)])

    body_pos = (body + boss + fill + collar).clean()

    # ---- plug mold: plug flipped dish-down on a floor with the dish pit, walled by a split ring ----
    plug_flip = Rot(180, 0, 0) * plug                  # spans Z in [-DISH_H, SOCKET_DEPTH]
    z_ring = FLOOR + DISH_H                             # foot-ring plane after the shift
    plug_up = Pos(0, 0, z_ring) * plug_flip
    top = z_ring + SOCKET_DEPTH
    r_in, r_out = R_RING, R_RING + RING_WALL
    floor = Cylinder(r_out + RING_CLEAR + LIP, z_ring, align=MIN) - plug_up
    lip = Pos(0, 0, z_ring) * (Cylinder(r_out + RING_CLEAR + LIP, 4, align=MIN)
                               - Cylinder(r_out + RING_CLEAR, 4, align=MIN))
    plug_floor = (floor + lip).clean()
    ring = Pos(0, 0, z_ring) * Cylinder(r_out, SOCKET_DEPTH, align=MIN) - plug_up
    ring_half = ring & Box(200, 200, 200, align=(Align.MIN, Align.CENTER, Align.CENTER))
    ring_half = Pos(0, 0, -z_ring) * ring_half          # print on its foot-ring end

    # ---- checks ----
    print(f"body {body.volume/OZ:.2f} fl oz solid; body outside mug {(body - mug).volume:.2f} mm3 (want 0)")
    rebuilt = body + handle
    print(f"body + handle vs mug: {(mug - rebuilt).volume:.0f} mm3 missing "
          f"(the 0.5 mm skin under the handle roots plus the split strip), "
          f"{(rebuilt - mug).volume:.2f} mm3 extra (want 0)")
    print(f"handle {handle.volume/1000:.1f} cm3; sprue sections "
          + ", ".join(f"{f.area:.0f} mm2 at z {f.center().Z:.0f}" for f in root_secs))
    cavity = body_pos - plug - collar
    diff = (cavity - body).volume + (body - cavity).volume
    print(f"side-half cavity minus collar vs body: symmetric difference {diff:.2f} mm3 (want ~0)")
    res = math.pi * rc**2 * (COLLAR_H - COLLAR_STEP) / 1000
    print(f"reservoir above the rim: ~{res:.0f} mL")
    gap = (plug_up - Cylinder(r_in + 0.01, top, align=MIN)).volume
    print(f"plug {plug.volume/1000:.0f} cm3 (plaster for the insert); plug outside the ring bore: {gap:.2f} mm3 (want 0)")

    save("body", body)
    save("body_positive", body_pos)
    save("handle_positive", handle_pos)
    save("plug_preview", plug)     # for checking only; not printed
    save("plug_floor", plug_floor)
    save("plug_ring", ring_half)


if __name__ == "__main__":
    main()
