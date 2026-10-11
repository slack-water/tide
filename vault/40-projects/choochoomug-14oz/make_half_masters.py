#!/usr/bin/env python3
"""Split halves_positive on the sagittal plane (Y=0, through the handle) and fuse each
half onto a printed flange (the pour box floor) with natch holes. Run make_mold_parts.py first.

Vocabulary follows 90-archive/skull-mold-draft-shell/UBIQUITOUS_LANGUAGE.md:
  parting plane = the mug's sagittal plane; master = printed half + flange; natch = hole in
  the flange that holds a registration insert; print file = STL with the parting plane on the bed.

Why two masters: the halves are mirror images. Two plaster halves cast from the same master are
same-handed (handle ends up on opposite sides when they close). Master B is master A mirrored
across the flange's vertical centre line, so flipping a plaster half about that line mates it with
a half cast from A, and the natch holes land on top of each other.

Flange edges at the top (Z max) and bottom (Z min) are flush with the funnel-seat and plug-socket
boss ends: stand the pour-box walls on those edges and the pocket and socket come out open in the
finished plaster.

Usage: .venv/bin/python make_half_masters.py [--margin 35] [--thickness 5] [--natch-diameter 12]
"""
import argparse
from pathlib import Path

import trimesh
from build123d import (Align, Box, Cylinder, Pos, Rot, Plane, Solid, mirror,
                       export_step, export_stl, import_step)

HERE = Path(__file__).parent


def save_print(name, solid):
    """STEP in the model frame; STL rotated so the flange (parting plane) lies on the bed."""
    export_step(solid, HERE / f"{name}.step")
    on_bed = Rot(90, 0, 0) * solid                  # +Y (up out of the parting plane) -> +Z
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
    print(f"{name:14s} print {bb.size.X:6.1f} x {bb.size.Y:6.1f} x {bb.size.Z:5.1f} mm  "
          f"vol {solid.volume/1000:6.1f} cm3  watertight={m.is_watertight}")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--margin", type=float, default=35.0, help="flange reach past the part in X (mm)")
    ap.add_argument("--thickness", type=float, default=5.0, help="flange thickness (mm)")
    ap.add_argument("--natch-diameter", type=float, default=12.0)
    args = ap.parse_args()

    whole = import_step(HERE / "halves_positive.step")
    assert isinstance(whole, Solid)
    bb = whole.bounding_box()
    big = 1000

    # one half on the +Y side of the sagittal plane
    half = whole & Pos(0, big / 2, 0) * Box(big, big, big)

    # flange on the -Y side, flush with the boss ends in Z, `margin` beyond the part in X
    x0, x1 = bb.min.X - args.margin, bb.max.X + args.margin
    z0, z1 = bb.min.Z, bb.max.Z
    flange = Pos((x0 + x1) / 2, -args.thickness / 2, (z0 + z1) / 2) * Box(x1 - x0, args.thickness, z1 - z0)

    # natches: two in each side strip, mid-strip in X, at 25% / 75% of the height
    xs = [x0 + args.margin / 2, x1 - args.margin / 2]
    zs = [z0 + 0.25 * (z1 - z0), z0 + 0.75 * (z1 - z0)]
    natch_pts = [(x, z) for x in xs for z in zs]
    for x, z in natch_pts:
        flange = flange - Pos(x, -args.thickness / 2, z) * Rot(90, 0, 0) * Cylinder(
            args.natch_diameter / 2, args.thickness + 2, align=(Align.CENTER, Align.CENTER, Align.CENTER))

    master_a = (half + flange).clean()
    xc = (x0 + x1) / 2
    master_b = mirror(master_a, about=Plane.YZ.offset(xc))  # mirror across the flange's vertical centre line

    # ---- checks ----
    print(f"flange {x1 - x0:.1f} x {z1 - z0:.1f} x {args.thickness} mm, natches {args.natch_diameter} mm at "
          + ", ".join(f"({x:.1f},{z:.1f})" for x, z in natch_pts))
    print(f"half volume {half.volume/1000:.1f} cm3 (positive/2 = {whole.volume/2000:.1f}); solids in master A: {len(master_a.solids())}")
    for x, z in natch_pts:
        assert not master_a.is_inside((x, -args.thickness / 2, z)), "natch hole not open"
        assert master_a.is_inside((x + args.natch_diameter / 2 + 1, -args.thickness / 2, z)), "no flange around natch"
    # mating: flip B about the vertical line through the flange centre, then B's mug half plus A's must rebuild the positive
    flipped = Pos(2 * xc, 0, 0) * Rot(0, 0, 180) * master_b
    a_mug = master_a & Pos(0, big / 2, 0) * Box(big, big, big)
    b_mug = flipped & Pos(0, -big / 2, 0) * Box(big, big, big)
    rebuilt = a_mug + b_mug
    err = (rebuilt - whole).volume + (whole - rebuilt).volume
    print(f"A + flipped B vs the whole positive: symmetric difference {err:.2f} mm3 (want ~0)")
    holes_b = set()
    for x, z in natch_pts:
        c = (flipped.is_inside((x, args.thickness / 2, z)), flipped.is_inside((x + args.natch_diameter / 2 + 1, args.thickness / 2, z)))
        holes_b.add(c)
    print("flipped B has open natches at A's positions with flange around them:", holes_b == {(False, True)})

    save_print("master_A", master_a)
    save_print("master_B", master_b)


if __name__ == "__main__":
    main()
