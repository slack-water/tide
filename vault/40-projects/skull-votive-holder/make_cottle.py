#!/usr/bin/env python3
"""make_cottle.py -- a plain drafted cottle that stands on a master's flange and holds the plaster to a minimum.

Parametric CAD (build123d), no mesh. Dimensions are the half's, from README (y -71.2..55.2, z -25..79, 43.2 tall)
and make_masters' flange (--margin 30 past the half); change them if either changes.

  - seat: the flange face, x = 1 (make_masters overlaps the half into the flange by 1 mm).
  - sleeve: all four walls reach down --thickness + 1 mm past the seat, around the flange edge to the table, so the
    cottle slips over the master and locates on it. --fit mm of clearance on the sides and the crown end.
  - boss end (z = -boss-end): wall's inner face is flush with the boss tip and the flange edge (no clearance), so
    the pour hole comes out open.
  - flat base (z = flange edge, crown + margin): a plane parallel to the pull, no draft, so the closed mold stands on it.
  - draft: the two Y walls lean in --draft degrees from the flange to the rim; the plaster block narrows toward
    its back and the cottle lifts off along +X. The two flat end walls are parallel to the pull.
  - rim: top of the half + --over mm. Pour to the rim. Print rim down, flange end up.

Usage: .venv/bin/python make_cottle.py [--draft 35] [--wall 0.8] [--over 20] [--margin 30] [--fit 0.15] [--out-dir .]
"""
import argparse
from math import radians, tan
from pathlib import Path

from build123d import Axis, Box, Plane, Polygon, Pos, export_step, export_stl, extrude

SEAT = 1.0


def prism(x0, x1, y0, y1, z0, z1, taper):
    """Trapezoid in the x-y plane, wider at x0, extruded along z: drafts the Y walls only."""
    d = (x1 - x0) * taper
    sk = Polygon((x0, y0), (x0, y1), (x1, y1 - d), (x1, y0 + d), align=None)
    return Pos(0, 0, z0) * extrude(sk, z1 - z0, dir=(0, 0, 1))   # dir explicit: the face normal points -Z


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--y-min", type=float, default=-71.2, help="half extent in Y")
    ap.add_argument("--y-max", type=float, default=55.2)
    ap.add_argument("--half-height", type=float, default=43.2, help="half extent in X above the parting plane")
    ap.add_argument("--half-volume", type=float, default=265.9, help="cm3, to report plaster")
    ap.add_argument("--draft", type=float, default=35.0,
                    help="degrees the Y walls lean in; the half narrows as it rises, and measured on it 35 keeps >= 15 mm of plaster (limit ~36)")
    ap.add_argument("--wall", type=float, default=0.8, help="two passes of a 0.4 mm nozzle")
    ap.add_argument("--over", type=float, default=20.0, help="plaster over the highest point")
    ap.add_argument("--margin", type=float, default=30.0, help="flange reach past the half, as make_masters.py")
    ap.add_argument("--fit", type=float, default=0.15, help="sleeve clearance on the flange edge, mm per side")
    ap.add_argument("--crown-height", type=float, default=79.0)
    ap.add_argument("--boss-end", type=float, default=25.0)
    ap.add_argument("--thickness", type=float, default=5.0, help="flange thickness")
    ap.add_argument("--out-dir", default=".")
    a = ap.parse_args()
    out = Path(a.out_dir)
    w, t, k = a.wall, a.thickness, tan(radians(a.draft))

    top = SEAT + a.half_height + a.over - 1.0
    y0, y1 = a.y_min - a.margin - a.fit, a.y_max + a.margin + a.fit     # cavity at the seat = flange outline + fit
    z0, z1 = -a.boss_end, a.crown_height + a.margin + a.fit              # boss end exact: flush, no clearance

    cavity = prism(SEAT, top, y0, y1, z0, z1, k)
    outer = prism(SEAT, top, y0 - w, y1 + w, z0 - w, z1 + w, k)
    # sleeve: straight walls round the flange edge, x from the table to the seat; overlaps the ring so the union fuses
    sx = t + SEAT + 0.2
    sleeve = (Pos((SEAT + 0.2 - t) / 2, (y0 + y1) / 2, (z0 + z1) / 2) * Box(sx, y1 - y0 + 2 * w, z1 - z0 + 2 * w)
              - Pos((SEAT + 0.2 - t) / 2, (y0 + y1) / 2, (z0 + z1) / 2) * Box(sx + 1, y1 - y0, z1 - z0))
    cottle = outer - cavity + sleeve

    plaster = cavity.volume / 1000 - a.half_volume
    print(f"cavity {y1 - y0:.0f} x {z1 - z0:.0f} mm at the flange, {top - SEAT:.1f} mm deep; "
          f"rim narrower by {2 * (top - SEAT) * k:.1f} mm across Y")
    print(f"plaster per half ~{plaster / 1000:.2f} L (flange-sized box 70 mm tall: ~1.49 L)")
    print(f"flat base wall z = {z1:.0f}, boss-end wall z = {z0:.0f} (flush with boss tip and flange edge); cottle {cottle.volume / 1000:.0f} cm3")
    assert cottle.is_valid and len(cottle.solids()) == 1

    export_step(cottle, out / "cottle.step")
    pr = cottle.rotate(Axis.Y, 90)                         # +X (rim) -> -Z: rim on the bed
    pr = Pos(0, 0, -pr.bounding_box().min.Z) * pr
    export_stl(pr, str(out / "cottle_PRINT.stl"))
    bb = pr.bounding_box()
    print(f"print {bb.size.X:.1f} x {bb.size.Y:.1f} x {bb.size.Z:.1f} mm, rim down")


if __name__ == "__main__":
    main()
