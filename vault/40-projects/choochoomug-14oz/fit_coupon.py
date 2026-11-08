#!/usr/bin/env python3
"""Fit coupon for the flat-pour, melamine-parting-face, set-jig method (sketch, 2026-11-08).

Tests one question before the body master is redesigned: do two plaster halves, poured flat on two
melamine boards with their positives and keys placed by one printed jig, close flush and in line?

Coordinates: the melamine board top is z = 0 and is the parting face. Plaster fills z in [0, H]
and lifts off in +Z. The positive runs along X for the full box length, so the cavity comes out
open at both plaster end faces, where the step at the seam can be checked by eye and by feel.

Parts:
  coupon_skin   half positive: a teardrop (a circle with a 45 degree roof, flattened at the top) so
                it prints rim-down with no supports. SKIN thick, open underneath, closed at both
                ends. The closed ends butt against the cottle's end boards.
  coupon_boss   printed key boss: a 90 degree point cone. Glue two per board (CA).
  coupon_jig    rigid locating slab, JIG_T thick:
                  - a cutout the skin's footprint plus JIG_FIT, which holds the thin rim true
                    while it is taped down
                  - holes the bosses drop into
                  - guide holes for a 12 mm 90 degree spot drill, which cuts the dimples into
                    the melamine. A spot drill's point diameter is its shank diameter, so the
                    shank rides in the hole. Set a stop collar so the cut is DIMPLE_D wide.
                One placement of the jig fixes everything, so the cavity-to-key relation comes
                from this one print.

Keys: bosses at y = +KEY_Y and dimples at y = -KEY_Y on every board. Turning a half 180 degrees
about X (y -> -y) puts each of its plaster bosses into the other half's plaster dimples, so any
two boards made with this jig mate.

Key geometry, why it is what it is: a drilled cone dimple has a sharp point. The plaster boss it
makes must clear the printed boss's dimple on its flanks and at its tip, while the parting faces
touch. With equal 90 degree cones the flank gap is (BOSS_D - DIMPLE_D) / 2 horizontally, and the tip
clears only if DIMPLE_D / 2 < BOSS_H. So the printed boss is a full point (height = radius) and the
drilled dimple is a little narrower.

Workflow per board:
  1. clamp the jig to the melamine by its ears
  2. spot-drill the two dimples through the guide holes to the stop collar, then vacuum the chips
  3. tape the skin's rim (thin double-sided tape all round the bed-side face), drop it into the
     cutout and press down. Glue the bosses (CA) into their holes.
  4. unclamp and lift the jig straight up
  5. butt the end boards against the skin's closed ends, pinwheel the side boards, seal, soap, pour

Print: skin rim down, 0.12 mm layers, 3 walls, elephant-foot compensation ~0.15 mm. Bosses base
down, 0.12 mm. Jig flat, 0.2 mm, 4 walls, 40 % infill (it should be stiff, not light).

Usage: .venv/bin/python fit_coupon.py
"""
import math
from pathlib import Path

from build123d import Align, Box, Cone, Cylinder, Pos, Rot, export_stl

HERE = Path(__file__).parent
SKIN = 1.2
R = 20.0            # teardrop circle radius
F = 26.0            # roof flattened at this height (the point would be at R * sqrt 2 = 28.3)
L = 90.0            # box length in X = positive length; the skin's ends butt the end boards
W = 100.0           # box width in Y
H = F + 14.0        # plaster depth above the board
KEY_X, KEY_Y = 25.0, 35.0
BOSS_D = 12.0       # printed boss: 90 degree cone, base BOSS_D, height BOSS_D / 2 (a point)
BOSS_H = BOSS_D / 2
DIMPLE_D = 11.6     # drilled dimple: 90 degree cone, this wide at the surface
JIG_T = 8.0         # jig thickness
JIG_FIT = 0.1       # cutout and boss-hole clearance per side
DRILL_D = 12.0      # spot drill shank and point diameter
DRILL_FIT = 0.05    # guide hole clearance per side (the hole wears; reprint the jig if it gets loose)
JIG_PAD = 15.0      # jig reaches this far past the box on every side
EAR = 25.0          # clamp ears beyond that, at both ends in X


def box(x0, x1, y0, y1, z0, z1):
    return Pos((x0 + x1) / 2, (y0 + y1) / 2, (z0 + z1) / 2) * Box(x1 - x0, y1 - y0, z1 - z0)


def teardrop(r, top, x0, x1, z0):
    """Circle r about the X axis, plus the 45 degree roof (a square of side r turned 45 degrees about
    X with a corner on the axis), kept between z0 and top and between x0 and x1."""
    n = x1 - x0
    cyl = Pos((x0 + x1) / 2, 0, 0) * Rot(0, 90, 0) * Cylinder(r, n)
    roof = Rot(45, 0, 0) * box(x0, x1, 0, r, 0, r)
    return (cyl + roof) & box(x0, x1, -r - 1, r + 1, z0, top)


def cone_z(d_base, h, at, down=False):
    """90-ish degree cone, base diameter d_base on z = 0 at (x, y), point at height h (or -h)."""
    c = Cone(d_base / 2, 0, h, align=(Align.CENTER, Align.CENTER, Align.MIN))
    if down:
        c = Rot(180, 0, 0) * c
    return Pos(at[0], at[1], 0) * c


def vol(shape):
    return shape.volume if shape else 0.0


def save(name, part):
    part = Pos(0, 0, -part.bounding_box().min.Z) * part
    stl = HERE / f"{name}_PRINT.stl"
    stl.unlink(missing_ok=True)
    ok = export_stl(part, stl, tolerance=0.02, angular_tolerance=0.15)
    assert ok and stl.exists() and stl.stat().st_size > 0, f"{name}: STL export failed"
    bb = part.bounding_box()
    print(f"{name:12s} print {bb.size.X:6.1f} x {bb.size.Y:6.1f} x {bb.size.Z:5.1f} mm  "
          f"vol {part.volume/1000:5.1f} cm3  solids={len(part.solids())} valid={part.is_valid}")


def main():
    # ---- skin: outer teardrop minus inner teardrop; open underneath, closed at both ends ----
    outer = teardrop(R, F, -L / 2, L / 2, 0)
    inner = teardrop(R - SKIN, F - SKIN, -L / 2 + SKIN, L / 2 - SKIN, -1)   # 45 degree offset stays 45 degree
    skin = outer - inner
    assert len(skin.solids()) == 1 and skin.is_valid, "skin boolean went wrong"
    # probes: solid half a skin in from the side wall, roof and end; hollow just past each
    side = [((0, R - SKIN / 2, 0.5), True), ((0, R - SKIN - 0.1, 0.5), False),
            ((0, 0, F - SKIN / 2), True), ((0, 0, F - SKIN - 0.1), False),
            ((L / 2 - SKIN / 2, 0, 10), True), ((L / 2 - SKIN - 0.1, 0, 10), False)]
    bad = [p for p, want in side if skin.is_inside(p) != want]
    assert not bad, f"skin probes failed at {bad}"

    bosses = [cone_z(BOSS_D, BOSS_H, (x, KEY_Y)) for x in (-KEY_X, KEY_X)]
    dimple_at = [(x, -KEY_Y) for x in (-KEY_X, KEY_X)]

    # ---- one plaster half, and the mate: the same half turned 180 degrees about X ----
    plaster = box(-L / 2, L / 2, -W / 2, W / 2, 0, H) - outer
    plaster = plaster - bosses
    plaster = plaster + [cone_z(DIMPLE_D, DIMPLE_D / 2, d, down=True) for d in dimple_at]
    mate = Rot(180, 0, 0) * plaster
    over = vol(plaster & mate)
    shift = 0.3
    over_shift = vol(plaster & (Pos(0, shift, 0) * mate))
    flank = (BOSS_D - DIMPLE_D) / 2
    tip = BOSS_H - DIMPLE_D / 2
    print(f"keys: flank gap {flank:.2f} mm horizontal ({flank * math.cos(math.radians(45)):.2f} normal), "
          f"tip clearance {tip:.2f} mm")
    print(f"mate: overlap closed {over:.3f} mm3 (want 0); shifted {shift} mm in y {over_shift:.1f} mm3 "
          f"(want > 0: the keys stop a shift that size)")
    assert tip > 0 and flank > 0 and over < 0.01 and over_shift > 1.0
    gap_cav = KEY_Y - BOSS_D / 2 - R
    gap_wall = W / 2 - KEY_Y - BOSS_D / 2
    print(f"plaster round each key: {gap_cav:.1f} mm to the cavity, {gap_wall:.1f} mm to the side face; "
          f"{H - F:.0f} mm over the crown")
    half_l = (L * W * H - outer.volume) / 1e6
    print(f"plaster per half ~{half_l:.2f} L (box {L:.0f} x {W:.0f} x {H:.0f} mm inside), "
          f"~{2 * half_l:.2f} L per coupon pour")

    # ---- jig ----
    x0, x1 = -L / 2 - JIG_PAD - EAR, L / 2 + JIG_PAD + EAR
    y0, y1 = -W / 2 - JIG_PAD, W / 2 + JIG_PAD
    jig = box(x0, x1, y0, y1, 0, JIG_T)
    jig -= box(-L / 2 - JIG_FIT, L / 2 + JIG_FIT, -R - JIG_FIT, R + JIG_FIT, -1, JIG_T + 1)
    holes = [Pos(x, KEY_Y, JIG_T / 2) * Cylinder(BOSS_D / 2 + JIG_FIT, JIG_T + 2) for x in (-KEY_X, KEY_X)]
    guides = [Pos(x, y, JIG_T / 2) * Cylinder(DRILL_D / 2 + DRILL_FIT, JIG_T + 2) for x, y in dimple_at]
    jig = jig - holes - guides
    assert len(jig.solids()) == 1 and jig.is_valid, "jig boolean went wrong"
    clash = vol(jig & skin) + sum(vol(jig & b) for b in bosses)
    print(f"jig: clears skin and bosses ({clash:.3f} mm3 overlap, want 0); stop collar {JIG_T + DIMPLE_D / 2:.1f} mm "
          f"above the drill's point (jig {JIG_T:.0f} + cone depth {DIMPLE_D / 2:.1f})")
    assert clash < 0.01
    # the skin and bosses are narrower above the board than at it, so the jig lifts straight off
    assert all(jig.is_inside((x, R + JIG_FIT + 0.5, JIG_T / 2)) for x in (-L / 4, L / 4))

    save("coupon_skin", skin)
    save("coupon_boss", bosses[0])
    save("coupon_jig", jig)
    print("print: 2 skins, 4 bosses, 1 jig. Cut 2 melamine boards and 4 cottle boards per pour.")


if __name__ == "__main__":
    main()
