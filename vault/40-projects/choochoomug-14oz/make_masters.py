#!/usr/bin/env python3
"""Printed masters for the plaster molds. Run make_mold_parts.py first.

Each master is a tray: the back plate is the parting plane (Y=0) with half a positive standing on
it, walls around it, and keys on the plate. Lay the tray on its back plate, pour plaster to the wall
tops, strike flat, and lift the block out in +Y. Walls that only need to release are drafted 2
degrees; walls whose plaster face must come out flat or open are not.

  body_master   half of body_positive (Y >= 0). The floor (socket end) is flat so the plug socket
                comes out open and the mold stands flat; the top end is closed by body_cap, flush
                with the reservoir collar. Cast it twice: two casts from one master mate after a
                180 degree turn about the mug axis, because the body is a solid of revolution.
                Bosses on -X, dimples on +X.
  body_cap      slides over the open top of body_master; lips hook the side walls and back plate.
  handle_master half of handle_positive. The sprue end (-X) is flat so both sprues come out open.
                Cast it twice: the handle is symmetric top to bottom, so a second cast turned 180
                degrees about the handle's mid-height line mates with the first. Bosses above
                mid-height, dimples at the mirrored spots below.

Print (STLs carry no settings; set them per object):
  body_master_PRINT    upright, floor on the bed, 0.12 mm layers (the mug surface; rings, not
                       terraces). Foot cone overhang is 51 degrees from vertical; check it on the
                       first print. No supports.
  handle_master_PRINT  back plate on the bed, adaptive or 0.12 mm layers over the handle.
  body_cap_PRINT       plate on the bed, 0.2 mm.
  elephant-foot compensation ~0.15 mm on all three.

Usage: .venv/bin/python make_masters.py [--margin 25] [--plate 6] [--wall 3] [--draft 2]
"""
import argparse
import math
from pathlib import Path

import trimesh
from build123d import (Align, Box, BuildLine, BuildPart, BuildSketch, Cone, Plane, Polyline, Pos,
                       Rot, Solid, export_step, export_stl, extrude, import_step, make_face)

HERE = Path(__file__).parent
KEY_D, KEY_TIP, KEY_H = 12.0, 6.0, 4.0   # conical key: base diameter, tip diameter, height
CAP_T, CAP_LIP, CAP_CLEAR, CAP_LIP_T = 4.0, 12.0, 0.3, 2.5


def prism(plane, pts, lo, hi):
    """Closed polyline on `plane`, extruded along its normal from offset lo to hi."""
    with BuildPart() as b:
        with BuildSketch(plane.offset(lo)):
            with BuildLine():
                Polyline(*pts, close=True)
            make_face()
        extrude(amount=hi - lo)
    return b.part


def tray(x0, x1, z0, z1, depth, plate, wall, t, draft, open_top):
    """Back plate y in [-plate, 0]; plaster space x in [x0, x1], z in [z0, z1] at y = 0, widening
    by t per mm of y on the sides named in `draft` ('-x', '+x', '-z', '+z'). open_top leaves +Z open."""
    d = depth + 1  # run the plaster space out through the open face
    xl = lambda y: x0 - (y * t if "-x" in draft else 0)
    xh = lambda y: x1 + (y * t if "+x" in draft else 0)
    zl = lambda y: z0 - (y * t if "-z" in draft else 0)
    zh = lambda y: z1 + (y * t if "+z" in draft else 0)
    big = 1000
    space = prism(Plane.XY, [(xl(0), 0), (xh(0), 0), (xh(d), d), (xl(d), d)], -big, big)
    space = space & prism(Plane.YZ, [(0, zl(0)), (0, zh(0) + (1 if open_top else 0)),
                                     (d, zh(d) + (1 if open_top else 0)), (d, zl(d))], -big, big)
    ox0, ox1 = xl(depth) - wall, xh(depth) + wall
    oz0, oz1 = zl(depth) - wall, (z1 if open_top else zh(depth) + wall)
    outer = Pos((ox0 + ox1) / 2, (depth - plate) / 2, (oz0 + oz1) / 2) * Box(ox1 - ox0, depth + plate, oz1 - oz0)
    return outer - space, (ox0, ox1, oz0, oz1)


def key_cone():
    """Key standing on the plate (y = 0) toward +Y."""
    return Rot(-90, 0, 0) * Cone(KEY_D / 2, KEY_TIP / 2, KEY_H, align=(Align.CENTER, Align.CENTER, Align.MIN))


def add_keys(master, half, bosses, dimples):
    k = key_cone()
    pit = Rot(180, 0, 0) * k                 # same cone mirrored into the plate
    for x, z in bosses:
        assert half.distance_to(Pos(x, 0, z) * k) > 3, f"boss at ({x:.0f},{z:.0f}) within 3 mm of the cavity"
        master = master.fuse(Pos(x, 0, z) * k, tol=0.01)
    for x, z in dimples:
        assert half.distance_to(Pos(x, 0, z) * pit) > 3, f"dimple at ({x:.0f},{z:.0f}) within 3 mm of the cavity"
        master = master - Pos(x, 0, z) * pit
    return master


def check(name, master, expect_vol):
    n = len(master.solids())
    err = abs(master.volume - expect_vol) / expect_vol
    print(f"{name:14s} solids={n}  vol {master.volume/1000:6.1f} cm3 (parts sum {expect_vol/1000:6.1f}, off {100*err:.2f}%)")
    assert n == 1 and err < 0.01, f"{name}: boolean went wrong"


def save_print(name, solid, rot):
    export_step(solid, HERE / f"{name}.step")
    on_bed = rot * solid
    on_bed = Pos(0, 0, -on_bed.bounding_box().min.Z) * on_bed
    stl = HERE / f"{name}_PRINT.stl"
    export_stl(on_bed, stl, tolerance=0.02, angular_tolerance=0.15)
    m = trimesh.load(stl)
    m.update_faces(m.nondegenerate_faces(height=1e-6))
    m.remove_unreferenced_vertices()
    trimesh.repair.fix_winding(m)
    trimesh.repair.fill_holes(m)
    m.export(stl)
    bb = on_bed.bounding_box()
    print(f"{name:14s} print {bb.size.X:6.1f} x {bb.size.Y:6.1f} x {bb.size.Z:6.1f} mm  watertight={m.is_watertight}")


def half_of(positive):
    half = positive & Box(1000, 500, 1000, align=(Align.CENTER, Align.MIN, Align.CENTER))
    err = abs(half.volume - positive.volume / 2) / positive.volume
    assert err < 0.002, f"half split went wrong ({half.volume:.0f} vs {positive.volume/2:.0f})"
    return half


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--margin", type=float, default=25.0, help="plaster around the body in X and Y (mm)")
    ap.add_argument("--plate", type=float, default=6.0, help="back plate thickness (mm); dimples are 4 deep")
    ap.add_argument("--wall", type=float, default=3.0)
    ap.add_argument("--draft", type=float, default=2.0, help="degrees on the walls that only release")
    args = ap.parse_args()
    t = math.tan(math.radians(args.draft))

    # ---------------- body ----------------
    pos = import_step(HERE / "body_positive.step")
    assert isinstance(pos, Solid)
    bb = pos.bounding_box()
    half = half_of(pos)
    w2 = bb.max.X + args.margin
    depth = bb.max.Y + args.margin
    z0, z1 = bb.min.Z, bb.max.Z           # socket end flush with the floor, collar flush with the cap
    shell, (ox0, ox1, oz0, oz1) = tray(-w2, w2, z0, z1, depth, args.plate, args.wall, t, ("-x", "+x"), True)
    master = shell.fuse(half, tol=0.01)
    check("body tray", master, shell.volume + half.volume)
    kx = bb.max.X + args.margin / 2
    kz = [z0 + 0.25 * (z1 - z0), z0 + 0.75 * (z1 - z0)]
    body_master = add_keys(master, half, [(-kx, z) for z in kz], [(kx, z) for z in kz])
    kv = Cone(KEY_D / 2, KEY_TIP / 2, KEY_H).volume
    check("body_master", body_master, master.volume + 2 * kv - 2 * kv)

    # cap: plate over the open top, lips down the outside of both side walls and the back plate
    c = CAP_CLEAR
    cx0, cx1 = ox0 - c - CAP_LIP_T, ox1 + c + CAP_LIP_T
    cy0, cy1 = -args.plate - c - CAP_LIP_T, depth
    plate = Pos((cx0 + cx1) / 2, (cy0 + cy1) / 2, z1 + CAP_T / 2) * Box(cx1 - cx0, cy1 - cy0, CAP_T)
    lips = (Pos((cx0 + cx1) / 2, (cy0 + cy1) / 2, z1 - CAP_LIP / 2) * Box(cx1 - cx0, cy1 - cy0, CAP_LIP)
            - Pos((ox0 + ox1) / 2, (cy0 + c + CAP_LIP_T + cy1) / 2 + 1, z1 - CAP_LIP / 2)
            * Box(ox1 - ox0 + 2 * c, cy1 - (cy0 + c + CAP_LIP_T) + 2, CAP_LIP + 0.01))
    body_cap = plate.fuse(lips, tol=0.01)
    print(f"body tray outer {ox1-ox0:.1f} x {depth+args.plate:.1f} x {oz1-oz0:.1f} mm; plaster space "
          f"~{(2*w2*depth*(z1-z0) - half.volume)/1e6:.2f} L per half (one master, cast twice)")

    # ---------------- handle ----------------
    hpos = import_step(HERE / "handle_positive.step")
    hb = hpos.bounding_box()
    hhalf = half_of(hpos)
    zc = (hb.min.Z + hb.max.Z) / 2
    m = 20.0
    hdepth = hb.max.Y + m
    hx0, hx1, hz0, hz1 = hb.min.X, hb.max.X + m, hb.min.Z - m, hb.max.Z + m   # sprue end flush with -X wall
    hshell, _ = tray(hx0, hx1, hz0, hz1, hdepth, args.plate, args.wall, t, ("+x", "-z", "+z"), False)
    hmaster = hshell.fuse(hhalf, tol=0.01)
    check("handle tray", hmaster, hshell.volume + hhalf.volume)
    # keys come in boss/dimple pairs mirrored about mid-height: outside the D and inside the loop
    pairs = [(hb.max.X + 11, 25.0), (62.0, 18.0)]
    handle_master = add_keys(hmaster, hhalf, [(x, zc + d) for x, d in pairs], [(x, zc - d) for x, d in pairs])
    check("handle_master", handle_master, hmaster.volume)
    print(f"handle tray plaster ~{((hx1-hx0)*hdepth*(hz1-hz0) - hhalf.volume)/1e6:.2f} L per half (one master, cast twice)")

    # ---- mating checks: the second cast is the first turned 180 degrees about the mating axis ----
    turned = Rot(0, 0, 180) * half             # about the mug axis
    rebuilt = half.fuse(turned, tol=0.01)
    print(f"body: half + turned half vs positive: {abs(rebuilt.volume - pos.volume):.1f} mm3 off (want ~0)")
    hturned = Pos(0, 0, zc) * Rot(180, 0, 0) * Pos(0, 0, -zc) * hhalf   # about the handle's mid-height line
    hrebuilt = hhalf.fuse(hturned, tol=0.01)
    print(f"handle: half + turned half vs positive: {abs(hrebuilt.volume - hpos.volume):.1f} mm3 off (want ~0)")

    save_print("body_master", body_master, Rot(0, 0, 0))
    save_print("body_cap", body_cap, Rot(180, 0, 0))
    save_print("handle_master", handle_master, Rot(90, 0, 0))   # back plate (-Y) onto the bed


if __name__ == "__main__":
    main()
