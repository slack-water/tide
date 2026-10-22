#!/usr/bin/env python3
"""make_cottle.py -- a minimal printed cottle that slips over a master's flange and holds the plaster to a minimum.

Same style as skull-votive-holder/make_cottle.py. Reads halves_positive.step (run make_mold_parts.py first) and
takes --margin / --thickness from make_half_masters.py so the flange matches. Parametric CAD, no mesh.

  - frame: the parting plane is y = 0; the half rises along +Y; the flange is y in [-thickness, 0], so the
    plaster pours over the face at y = 0.
  - sleeve: all four walls reach down --thickness mm past the flange face, round its edge, so the cottle slips
    over the master and locates on it. --fit mm of clearance per side.
  - top and bottom walls (z): flush with the flange edge, which is flush with the funnel-seat and plug-socket
    boss ends, so those pockets come out open in the plaster. Flat, parallel to the pull, no draft; the closed
    mold stands on the socket end. The cavity is exact here; only the sleeve takes the fit.
  - side walls (x): lean in toward the rim, each side by its own angle. The handle side (+X) takes the steepest
    angle that keeps --plaster mm of plaster beside the half (capped at --max-lean); the cup side (-X) has far
    less room, so it leans only --cup-draft degrees, which leaves it a thick wall of plaster. The lean is the
    draft, and it narrows the plaster.
  - rim: top of the half + --over mm. Pour to the rim. Print rim down, flange end up, no support.

Usage: .venv/bin/python make_cottle.py [--wall 0.8] [--over 20] [--plaster 15] [--margin 35] [--thickness 5]
           [--fit 0.15] [--draft DEG] [--cup-draft DEG] [--out-dir .]
"""
import argparse
from math import atan, degrees, radians, tan
from pathlib import Path

from build123d import Box, Polygon, Pos, Rot, Solid, export_step, export_stl, extrude, import_step

HERE = Path(__file__).parent
BIG = 1000


def lean_limit(half, x_edge, plaster, top):
    """Steepest lean (tan) of a side wall starting at x_edge, keeping `plaster` mm to the half, per side."""
    out = []
    for sign in (-1, 1):
        best = 1e9
        for k in range(1, int(top) + 1):
            y = float(k)
            sl = half & Pos(0, y + 0.5, 0) * Box(BIG, 1, BIG)
            if not sl.solids():
                continue
            bb = sl.bounding_box()
            edge = bb.min.X if sign < 0 else bb.max.X
            room = sign * (x_edge[0 if sign < 0 else 1] - edge) - plaster
            best = min(best, room / y)
        out.append(best)
    return out


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--wall", type=float, default=0.8, help="two passes of a 0.4 mm nozzle")
    ap.add_argument("--over", type=float, default=20.0, help="plaster over the highest point of the half")
    ap.add_argument("--plaster", type=float, default=15.0, help="minimum plaster beside the half at any height")
    ap.add_argument("--margin", type=float, default=35.0, help="flange reach past the part in X, as make_half_masters.py")
    ap.add_argument("--thickness", type=float, default=5.0, help="flange thickness, as make_half_masters.py")
    ap.add_argument("--fit", type=float, default=0.15, help="sleeve clearance on the flange edge, mm per side")
    ap.add_argument("--draft", type=float, default=None,
                    help="degrees the handle-side (+X) wall leans; default: the measured limit, capped at --max-lean")
    ap.add_argument("--cup-draft", type=float, default=20.0,
                    help="degrees the cup-side (-X) wall leans; less than the handle side for more plaster against the cup")
    ap.add_argument("--max-lean", type=float, default=40.0, help="printing rim down, a steeper wall is a near-45 deg overhang")
    ap.add_argument("--out-dir", default=str(HERE))
    a = ap.parse_args()
    out = Path(a.out_dir)
    w, t, f = a.wall, a.thickness, a.fit

    whole = import_step(HERE / "halves_positive.step")
    assert isinstance(whole, Solid)
    bb = whole.bounding_box()
    half = whole & Pos(0, BIG / 2, 0) * Box(BIG, BIG, BIG)           # +Y side, as make_half_masters.py
    hb = half.bounding_box()
    # flange outline: --margin past the part in X, flush with the boss ends in Z
    x0, x1 = bb.min.X - a.margin, bb.max.X + a.margin
    z0, z1 = bb.min.Z, bb.max.Z
    top = hb.max.Y + a.over
    print(f"half {hb.size.X:.1f} x {hb.max.Y:.1f} x {hb.size.Z:.1f} mm; flange {x1 - x0:.1f} x {z1 - z0:.1f}; rim y = {top:.1f}")

    lim = lean_limit(half, (x0 - f, x1 + f), a.plaster, hb.max.Y)
    limit_deg = [degrees(atan(m)) for m in lim]
    deg_cup = a.cup_draft
    deg = a.draft if a.draft is not None else float(int(min(limit_deg[1], a.max_lean) * 10) / 10)
    k_cup, k = tan(radians(deg_cup)), tan(radians(deg))
    assert k_cup <= lim[0] + 1e-9, f"cup lean {deg_cup} deg leaves under {a.plaster} mm of plaster (limit {limit_deg[0]:.1f})"
    assert k <= lim[1] + 1e-9, f"handle lean {deg} deg leaves under {a.plaster} mm of plaster (limit {limit_deg[1]:.1f})"
    print(f"side walls lean {deg_cup:.1f} deg on the cup side (-X) and {deg:.1f} deg on the handle side (+X); "
          f"limits for {a.plaster:g} mm of plaster beside the half: {limit_deg[0]:.1f} / {limit_deg[1]:.1f}")

    def prism(ox, oz0, oz1):
        """Cavity or outer wall: trapezoid in x-y (wide at the seat), extruded along z."""
        sk = Polygon((x0 - f - ox, 0), (x1 + f + ox, 0), (x1 + f + ox - top * k, top), (x0 - f - ox + top * k_cup, top),
                     align=None)
        return Pos(0, 0, oz0) * extrude(sk, oz1 - oz0, dir=(0, 0, 1))       # dir explicit: the face normal may point -Z

    cavity = prism(0, z0, z1)
    outer = prism(w, z0 - w, z1 + w)
    # sleeve: straight walls round the flange edge, y from the table to the seat; overlaps the ring so the union fuses
    sy = t + 0.2
    sx, sz = x1 - x0 + 2 * f, z1 - z0 + 2 * f
    c = ((x0 + x1) / 2, (0.2 - t) / 2, (z0 + z1) / 2)
    sleeve = Pos(*c) * Box(sx + 2 * w, sy, sz + 2 * w) - Pos(*c) * Box(sx, sy + 1, sz)
    cottle = outer - cavity + sleeve

    plaster = cavity.volume / 1000 - half.volume / 1000
    box = (x1 - x0) * (z1 - z0) * 80 / 1000 - half.volume / 1000
    print(f"cavity {x1 - x0 + 2 * f:.0f} x {z1 - z0:.0f} mm at the flange, narrowing to {x1 - x0 + 2 * f - top * (k + k_cup):.0f} mm at the rim")
    print(f"plaster per half ~{plaster / 1000:.2f} L (flange-sized box 80 mm tall, README: ~{box / 1000:.2f} L)")
    print(f"top/bottom walls z = {z1:.1f} / {z0:.1f}, flush with the flange edge and boss ends; cottle {cottle.volume / 1000:.0f} cm3")
    assert cottle.is_valid and len(cottle.solids()) == 1
    outside = half - cavity
    assert outside is None or outside.volume < 1e-3, f"half pokes through the cavity by {outside.volume:.1f} mm3"
    flange_box = Pos((x0 + x1) / 2, -t / 2, (z0 + z1) / 2) * Box(x1 - x0, t, z1 - z0)
    assert (cottle & flange_box) is None or (cottle & flange_box).volume < 1e-3, "sleeve collides with the flange"

    export_step(cottle, out / "cottle.step")
    pr = Rot(-90, 0, 0) * cottle                                           # +Y (rim) -> -Z: rim on the bed
    pr = Pos(0, 0, -pr.bounding_box().min.Z) * pr
    export_stl(pr, str(out / "cottle_PRINT.stl"))
    pb = pr.bounding_box()
    print(f"print {pb.size.X:.1f} x {pb.size.Y:.1f} x {pb.size.Z:.1f} mm, rim down")


if __name__ == "__main__":
    main()
