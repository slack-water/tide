#!/usr/bin/env python3
"""Uniformly scale the choochoomug mold-cavity STEP so the fired mug holds 14 oz.

Setup:  python3 -m venv .venv && .venv/bin/pip install build123d trimesh
Usage:  .venv/bin/python scale_mug.py [--scale 1.049]

Scale factor derivation (see README/log): the model is the unshelled exterior of
the mug (the mold cavity), 11.95 fl oz brim capacity post-shrinkage. Back-solving
the effective fired wall from that figure gives ~4-6 mm for 10-14% shrinkage,
and the scale needed for 14 oz is x1.048-1.050 across that whole range. Uniform
scaling about the origin keeps the base on Z=0 and the axis on the Z axis.
"""
import argparse
from pathlib import Path

import trimesh
from build123d import Solid, export_step, export_stl, import_step, scale

OZ_MM3 = 29573.5  # one US fl oz in mm^3
SRC = Path(__file__).with_name("choochoomug.step")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--scale", type=float, default=1.049)
    args = ap.parse_args()

    mug = import_step(SRC)
    assert isinstance(mug, Solid), f"expected one solid, got {type(mug)}"
    big = scale(mug, by=args.scale)

    stem = "choochoomug-14oz"
    export_step(big, SRC.with_name(f"{stem}.step"))
    stl = SRC.with_name(f"{stem}.stl")
    export_stl(big, stl, tolerance=0.02, angular_tolerance=0.15)

    # tessellating the revolve's pole leaves one zero-length edge; drop it and re-save
    m = trimesh.load(stl)
    m.update_faces(m.nondegenerate_faces(height=1e-6))
    m.remove_unreferenced_vertices()
    trimesh.repair.fix_winding(m)
    trimesh.repair.fill_holes(m)
    m.export(stl)
    bb = big.bounding_box()
    print(f"scale          x{args.scale}")
    print(f"solid volume   {mug.volume / OZ_MM3:.2f} -> {big.volume / OZ_MM3:.2f} fl oz")
    print(f"bbox (mm)      {bb.size.X:.1f} x {bb.size.Y:.1f} x {bb.size.Z:.1f}  (zmin={bb.min.Z:.3f})")
    print(f"stl watertight {m.is_watertight}, mesh volume {m.volume / OZ_MM3:.2f} fl oz")


if __name__ == "__main__":
    main()
