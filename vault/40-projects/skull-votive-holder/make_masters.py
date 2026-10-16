#!/usr/bin/env python3
"""make_masters.py -- drafted half-skull -> two printable masters (A left, B right) on a cottle flange.

Stage 2 of 2. Input is prep_skull.py's output after `stl_add_draft.py draft` (pull axis x, base min).

  - the drafted half is re-cut flat at the pour-boss tip (z = -boss-end) and at the crown plane
    (z = crown-height). Draft slopes both faces; the boss tip must be parallel to the pull and flush
    with the flange edge, or a wedge of plaster closes the pour hole. The crown plane stays flat so the
    cast's rim is level.
  - flange: a plate on the parting plane (x in [-thickness, 0], overlapping the half by 1 mm so the
    union fuses; coplanar unions fail), --margin mm past the half in Y and past the crown in Z. Its
    bottom edge is flush with the boss tip: stand the cottle board on that edge and the pour hole comes
    out open in the plaster. Natch holes (--natch-diameter, default 12 mm) at 25% / 75% of the flange
    height in each side strip: four, so at least three always register.
  - B is A mirrored across the parting plane. The flange is symmetric under that mirror, so natch holes
    land in the same (y, z) and the two plaster halves close on each other.
  - print files: flange on the bed, skull up, rotated here so the slicer needs none ("_PRINT").

Usage: python make_masters.py drafted.stl [--margin 30] [--thickness 5] [--natch-diameter 12]
           [--crown-height 79] [--boss-end 25] [--out-dir .]
"""
import argparse
from pathlib import Path

import numpy as np
import trimesh
from trimesh.transformations import rotation_matrix


def union(parts):
    return trimesh.boolean.union(parts, engine="manifold")


def box(x0, x1, y0, y1, z0, z1):
    b = trimesh.creation.box(extents=[x1 - x0, y1 - y0, z1 - z0])
    b.apply_translation([(x0 + x1) / 2, (y0 + y1) / 2, (z0 + z1) / 2])
    return b


def load_half(path, boss_end, crown_height):
    """Drafted half, main body only, re-cut flat at the boss tip, the crown plane and the parting plane."""
    half = trimesh.load(path, force="mesh")
    # marching cubes leaves debris (a few-face sliver and a ~10 mm3 blob in the last run) that a slicer
    # ignores and manifold3d refuses: keep only the main body, and say what went
    parts = sorted(half.split(only_watertight=False), key=lambda p: -len(p.faces))
    if len(parts) > 1:
        dropped = sum(abs(p.volume) for p in parts[1:])
        print(f"dropped {len(parts) - 1} stray pieces ({dropped:.1f} mm3 total, vs {parts[0].volume / 1000:.1f} cm3 kept)")
    half = parts[0]
    half = half.slice_plane([0, 0, -boss_end], [0, 0, 1], cap=True)
    half = half.slice_plane([0, 0, crown_height], [0, 0, -1], cap=True)
    return half.slice_plane([0, 0, 0], [1, 0, 0], cap=True)


def print_file(master, sign, path):
    """Rotate so the flange is on the bed and the half points up (+z); A: -90 about Y, B: +90."""
    m = master.copy()
    m.apply_transform(rotation_matrix(np.radians(-90.0 * sign), [0, 1, 0]))
    m.apply_translation([0, 0, -m.bounds[0][2]])
    m.export(path)
    return m


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("drafted")
    ap.add_argument("--margin", type=float, default=30.0, help="flange reach past the half in Y, and past the crown in Z")
    ap.add_argument("--thickness", type=float, default=5.0)
    ap.add_argument("--natch-diameter", type=float, default=12.0)
    ap.add_argument("--crown-height", type=float, default=79.0)
    ap.add_argument("--boss-end", type=float, default=25.0, help="boss tip below the base plane (mm); flange edge is flush")
    ap.add_argument("--out-dir", default=".")
    args = ap.parse_args()
    out = Path(args.out_dir)
    t, m, d = args.thickness, args.margin, args.natch_diameter

    half = load_half(args.drafted, args.boss_end, args.crown_height)
    b = half.bounds
    print(f"half {np.round(b[1] - b[0], 1).tolist()} mm, volume {half.volume / 1000:.1f} cm3, watertight {half.is_watertight}")

    y0, y1 = b[0][1] - m, b[1][1] + m
    z0, z1 = -args.boss_end, args.crown_height + m
    flange = box(-t, 1.0, y0, y1, z0, z1)
    natch = [(y, z) for y in (b[0][1] - m / 2, b[1][1] + m / 2) for z in (z0 + 0.25 * (z1 - z0), z0 + 0.75 * (z1 - z0))]
    for y, z in natch:
        cyl = trimesh.creation.cylinder(radius=d / 2, height=t + 4, sections=96)
        cyl.apply_transform(rotation_matrix(np.pi / 2, [0, 1, 0]))   # axis along X
        cyl.apply_translation([-t / 2, y, z])
        flange = trimesh.boolean.difference([flange, cyl], engine="manifold")
    master_a = union([flange, half])
    master_b = master_a.copy()
    master_b.apply_transform(np.diag([-1.0, 1, 1, 1]))               # trimesh re-winds a reflection itself

    # ---- checks ----
    bodies = len(master_a.split(only_watertight=False))
    print(f"flange {y1 - y0:.0f} x {z1 - z0:.0f} x {t} mm; natches {d} mm at "
          + ", ".join(f"(y{y:.1f}, z{z:.1f})" for y, z in natch))
    print(f"master A: watertight={master_a.is_watertight} bodies={bodies} volume {master_a.volume / 1000:.1f} cm3 "
          f"| B: watertight={master_b.is_watertight} volume {master_b.volume / 1000:.1f} cm3")
    assert bodies == 1 and master_a.is_watertight and master_b.is_watertight and master_a.volume > 0 and master_b.volume > 0
    inside = lambda mesh, p: mesh.contains([p])[0]
    for y, z in natch:
        assert not inside(master_a, (-t / 2, y, z)), "natch hole not open"
        assert inside(master_a, (-t / 2, y + d / 2 + 2, z)), "no flange around natch"
        assert not inside(master_b, (t / 2, y, z)) and inside(master_b, (t / 2, y + d / 2 + 2, z))
    # boss tip flush with the flange edge and flat
    tip = half.vertices[:, 2] < z0 + 1e-3
    print(f"boss tip: {tip.sum()} vertices on the z={z0:.0f} plane; flange bottom edge z={master_a.bounds[0][2]:.2f}")
    assert abs(master_a.bounds[0][2] - z0) < 1e-3

    a = print_file(master_a, +1, out / "master_A_PRINT.stl")
    bb = print_file(master_b, -1, out / "master_B_PRINT.stl")
    print(f"print A {np.round(a.extents, 1).tolist()} mm  min z {a.bounds[0][2]:.2f};  print B {np.round(bb.extents, 1).tolist()}")
    # sanity: the flange face must be the bed face (all bed-level vertices coplanar and ~ flange-sized)
    bed = a.vertices[:, 2] < 0.01
    print(f"bed-contact vertices on A: {bed.sum()} (flange face must be flat on z=0)")


if __name__ == "__main__":
    main()
