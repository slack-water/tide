#!/usr/bin/env python3
"""Printed masters and detachable cottles for the plaster molds, as exact build123d geometry built
from the profiles in make_mold_parts.py.

Each master is a back plate (the parting plane, Y=0) with half a positive and the keys on it.
The cottle around it comes apart, like the Old Forge tumbler and handle moulds: two identical
U-halves (one end wall plus half of each side wall) stand on the table around the plate, meet at
mid-length with fins, and two slide-on clips pinch the fins together. Demold by pulling the clips,
sliding each U off along the mold's length, and lifting the plaster off the master in +Y.

Every surface that molds plaster is SKIN thick (1.2 mm = 3 lines at 0.4 mm), so the master flexes
away from the set plaster instead of holding it rigidly, and prints with little filament:
  - the half positive is hollow. Body: the positive's profile offset SKIN inward in 2D and revolved.
    Handle: a stadium SKIN smaller swept along the same path. Both hollows run out through the back
    of the plate, and the body's is open at both ends (the cottle end walls close them).
  - the parting face is a SKIN plate over a void, on 45 degree diagonal SKIN ribs (printable both
    upright and flat); each dimple is a SKIN cup. The bosses stay solid; they are tiny.
  - the cottle walls are SKIN thick. Fins and clips are not molding surfaces and stay thicker.

  body_master     half of body_positive. Cast it twice: two casts from one master mate after a
                  180 degree turn about the mug axis. Bosses on -X, dimples on +X. The socket and
                  collar ends meet the U end walls, so the socket and the reservoir come out open.
  body_cottle     one U-half for the body; print two.
  body_clip       fin clip for the body cottle; print two.
  handle_master   half of handle_positive. Cast it twice: the handle is symmetric top to bottom, so
                  a second cast turned 180 degrees about mid-height mates with the first. Bosses
                  above mid-height, dimples at the mirrored spots below. The pour cups meet the -X
                  side wall, so they come out open.
  handle_cottle   one U-half for the handle; print two.
  handle_clip     fin clip for the handle cottle; print two.

Print (STLs carry no settings; set them per object):
  all parts       3 or more wall loops, so each SKIN prints as solid perimeters; elephant-foot
                  compensation ~0.15 mm so the parting face and wall edges stay square.
  body_master_PRINT    standing on its socket end, 0.12 mm layers (the mug surface; rings, not
                       terraces). Foot cone overhang 51 degrees from vertical. No supports.
  handle_master_PRINT  back plate (the open side) on the bed, adaptive or 0.12 mm layers over the
                       handle. The hollow's crown is a 4.6 mm radius arch; no supports.
  *_cottle_PRINT, *_clip_PRINT   on their table edge, 0.2 mm.

Usage: .venv/bin/python make_masters.py [--margin 25] [--plate 6]
"""
import argparse
import math
from pathlib import Path

from build123d import (Align, Axis, Box, BuildSketch, Compound, Cone, Locations, Plane, Pos,
                       Rectangle, Rot, export_step, export_stl, extrude, mirror, revolve)

import make_mold_parts as mp

HERE = Path(__file__).parent
SKIN = mp.SKIN
KEY_D, KEY_TIP, KEY_H = 12.0, 6.0, 4.0   # conical key: base diameter, tip diameter, height
FIT = 0.15        # cottle wall to plate edge
FIN, FIN_T = 8.0, 3.0                     # fin reach out from the wall, fin thickness
CLIP_W, CLIP_FIT = 2.5, 0.1               # clip wall, clip-to-fin gap per side (snug pinch)
RIB_PITCH = 25.0                          # diagonal rib spacing behind the parting-face skin


def box(x0, x1, y0, y1, z0, z1):
    return Pos((x0 + x1) / 2, (y0 + y1) / 2, (z0 + z1) / 2) * Box(x1 - x0, y1 - y0, z1 - z0)


def cone_y(r0, r1, h, at):
    """Cone with base radius r0 on the plate (y = 0) at (x, z), tip radius r1, height h toward +Y
    (h > 0) or into the plate (h < 0)."""
    c = Rot(-90, 0, 0) * Cone(r0, r1, abs(h), align=(Align.CENTER, Align.CENTER, Align.MIN))
    if h < 0:
        c = Rot(180, 0, 0) * c
    return Pos(at[0], 0, at[1]) * c


def master(half, inner, x0, x1, z0, z1, plate, bosses, dimples):
    """Plate + half positive + keys, minus the hollow and the plate void (ribs and dimple cups kept)."""
    outer = box(x0, x1, -plate, 0, z0, z1).fuse(half)
    outer = outer.fuse(*[cone_y(KEY_D / 2, KEY_TIP / 2, KEY_H, b) for b in bosses])
    outer = outer.cut(*[cone_y(KEY_D / 2, KEY_TIP / 2, -KEY_H, d) for d in dimples])
    void = plate_void(x0, x1, z0, z1, plate)
    cups = [cone_y(KEY_D / 2 + SKIN, KEY_TIP / 2 + SKIN, -(KEY_H + SKIN), d) for d in dimples]
    void = void.cut(*cups)
    m = outer.cut(inner, void)
    assert len(m.solids()) == 1 and m.is_valid, f"master boolean went wrong: {len(m.solids())} solids"
    return m


def cell_x(cx, i):
    """x of the centre of the i-th void cell on the plate's mid-height line (plate centre cx)."""
    return cx + (i + 0.5) * RIB_PITCH * math.sqrt(2)


def plate_void(x0, x1, z0, z1, plate):
    """The void behind the parting-face skin: diamond cells between 45 degree SKIN ribs at RIB_PITCH,
    clipped to the plate inside a SKIN rim and run out through the plate back. Built cell by cell
    (disjoint squares) because cutting a crossing grid of rib boxes out of one void runs OCC out of
    memory."""
    w = RIB_PITCH - SKIN                   # cell side; ribs lie on x + z = k*P and x - z = k*P
    P = RIB_PITCH * math.sqrt(2)
    cx, cz = (x0 + x1) / 2, (z0 + z1) / 2
    with BuildSketch(Plane.XZ) as rim:
        with Locations((cx, cz)):
            Rectangle(x1 - x0 - 2 * SKIN, z1 - z0 - 2 * SKIN)
    inside = rim.sketch.face()
    n = int(((x1 - x0) + (z1 - z0)) / P) + 2
    cells = []
    for i in range(-n, n + 1):
        for j in range(-n, n + 1):
            u, v = (i + 0.5) * P, (j + 0.5) * P
            x, z = cx + (u + v) / 2, cz + (u - v) / 2
            if not (x0 - P < x < x1 + P and z0 - P < z < z1 + P):
                continue
            with BuildSketch(Plane.XZ) as c:
                with Locations((x, z)):
                    Rectangle(w, w, rotation=45)
            cell = c.sketch.face() & inside
            if cell and cell.area > 1:
                cells.append(cell)
    # Plane.XZ's normal is -Y: lift the cells to y = -SKIN and extrude back past the plate
    return Compound([Pos(0, -SKIN, 0) * extrude(f, amount=plate + 1) for f in cells])


def skin_probe(name, part, points):
    """Each probe: a point on the molding surface and its inward unit normal. SKIN/2 in must be
    solid, SKIN + 0.1 in must be hollow."""
    ok = True
    for p, n in points:
        a = part.is_inside(tuple(p[i] + n[i] * SKIN / 2 for i in range(3)))
        b = part.is_inside(tuple(p[i] + n[i] * (SKIN + 0.1) for i in range(3)))
        if not (a and not b):
            print(f"  probe at {tuple(round(v, 2) for v in p)}: {SKIN / 2} in solid={a}, {SKIN + 0.1} in solid={b}")
        ok &= a and not b
    print(f"{name}: skin is {SKIN} mm at all {len(points)} probes: {ok}")
    assert ok


def cottle(x0, x1, z0, z1, depth, plate, wall):
    """U-half for plaster space x in [x0, x1], z in [z0, z1]: end wall at z0, side walls to mid-length,
    fins at mid-length. Walls run from the table (y = -plate) to the plaster top (y = depth).
    Returns the U-half, the clip, and the mid-length z."""
    zm = (z0 + z1) / 2
    y0, y1 = -plate, depth
    xi0, xi1 = x0 - FIT, x1 + FIT                  # wall inner faces
    xo0, xo1 = xi0 - wall, xi1 + wall              # wall outer faces
    ze = z0 - FIT - wall                           # end wall outer face
    u = box(xo0, xo1, y0, y1, ze, z0 - FIT).fuse(
        box(xo0, xi0, y0, y1, ze, zm), box(xi1, xo1, y0, y1, ze, zm),
        box(xo0 - FIN, xo0, y0, y1, zm - FIN_T, zm), box(xo1, xo1 + FIN, y0, y1, zm - FIN_T, zm))
    g = FIN_T + CLIP_FIT                           # clip: a C around one side's two fins
    clip = box(xo1, xo1 + FIN + CLIP_FIT + CLIP_W, y0, y1, zm - g - CLIP_W, zm + g + CLIP_W) \
        - box(xo1 - 1, xo1 + FIN + CLIP_FIT, y0 - 1, y1 + 1, zm - g, zm + g)
    other = mirror(u, about=Plane.XY.offset(zm))
    common = u & other
    closed = (u.is_inside(((x0 + x1) / 2, depth / 2, z0 - FIT - 0.1))
              and u.is_inside((x0 - FIT - 0.1, depth / 2, zm - 1))
              and other.is_inside((x0 - FIT - 0.1, depth / 2, zm + 1)))
    print(f"  U-halves overlap {common.volume if common else 0:.2f} mm3 (want 0), closed at end and joint: {closed}")
    assert closed and not (common and common.volume > 0.01)
    return u, clip


def save_print(name, part, rot):
    export_step(part, HERE / f"{name}.step")
    on_bed = rot * part
    on_bed = Pos(0, 0, -on_bed.bounding_box().min.Z) * on_bed
    export_stl(on_bed, HERE / f"{name}_PRINT.stl", tolerance=0.02, angular_tolerance=0.15)
    bb = on_bed.bounding_box()
    print(f"{name:14s} print {bb.size.X:6.1f} x {bb.size.Y:6.1f} x {bb.size.Z:6.1f} mm  "
          f"vol {part.volume/1000:6.1f} cm3  solids={len(part.solids())} valid={part.is_valid}")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--margin", type=float, default=25.0, help="plaster around the body in X and Y (mm)")
    ap.add_argument("--plate", type=float, default=6.0, help="back plate depth (mm); dimples are 4 deep")
    args = ap.parse_args()
    T = args.plate

    # ---------------- body ----------------
    half = mp.revolve_half(mp.positive_profile())
    inner = revolve(mp.positive_inner_profile(), Axis.Z)       # full turn: its -Y half opens the plate back
    w2 = mp.R_MAX + args.margin
    depth = mp.R_MAX + args.margin
    z0, z1 = -mp.SOCKET_DEPTH + FIT, mp.Z_TOP - FIT   # plate stops FIT short so the positive meets the end walls
    kx = mp.R_MAX + args.margin / 2
    kz = [z0 + 0.25 * (z1 - z0), z0 + 0.75 * (z1 - z0)]
    body_master = master(half, inner, -w2, w2, z0, z1, T, [(-kx, z) for z in kz], [(kx, z) for z in kz])
    # probes: belly wall (inward normal -Y), parting face between ribs (normal -Y), a dimple cup
    zw = 60.0
    rw = mp.BELLY[0] + (zw - mp.BELLY[1]) * (mp.WALL_TOP[0] - mp.BELLY[0]) / (mp.WALL_TOP[1] - mp.BELLY[1])
    tilt = math.atan((mp.BELLY[0] - mp.WALL_TOP[0]) / (mp.WALL_TOP[1] - mp.BELLY[1]))
    skin_probe("body master", body_master, [
        ((0, rw, zw), (0, -math.cos(tilt), -math.sin(tilt))),
        ((cell_x(0, 1), 0, (z0 + z1) / 2), (0, -1, 0))])
    # dimple cups: SKIN behind the pit tip is solid (the next 0.1 mm may be a rib, so not checked)
    assert all(body_master.is_inside((kx, -KEY_H - SKIN / 2, z)) for z in kz), "dimple cup missing"

    print("body cottle:")
    body_u, body_clip = cottle(-w2, w2, z0, z1, depth, T, SKIN)
    print(f"body plaster space {2*w2:.1f} x {depth:.1f} x {z1-z0:.1f} mm, "
          f"~{(2*w2*depth*(z1-z0) - half.volume)/1e6:.2f} L per half (one master, cast twice)")

    # ---------------- handle ----------------
    hhalf = mp.handle_solid(half=True)
    hinner = mp.handle_inner()
    hb = hhalf.bounding_box()
    zc = mp.HANDLE_CZ
    m = 20.0
    hdepth = hb.max.Y + m
    hx0, hx1, hz0, hz1 = hb.min.X + FIT, hb.max.X + m, hb.min.Z - m, hb.max.Z + m   # pour cups meet the -X wall
    pairs = [(hb.max.X + 11, 25.0), (62.0, 18.0)]   # boss/dimple pairs: outside the D, inside the loop
    handle_master = master(hhalf, hinner, hx0, hx1, hz0, hz1, T,
                           [(x, zc + d) for x, d in pairs], [(x, zc - d) for x, d in pairs])
    ro = mp.HANDLE_R + mp.HANDLE_W / 2
    skin_probe("handle master", handle_master, [
        ((mp.HANDLE_CX + ro, 2.0, zc), (-1, 0, 0)),                        # outer side of the D
        ((mp.HANDLE_CX + mp.HANDLE_R, mp.HANDLE_L / 2, zc), (0, -1, 0)),   # crown
        ((mp.HANDLE_CX, 2.0, zc + mp.HANDLE_R - mp.HANDLE_W / 2), (0, 0, 1)),  # inner side, top arm
        ((cell_x((hx0 + hx1) / 2, -1), 0, (hz0 + hz1) / 2), (0, -1, 0))])      # parting face, inside the loop
    print("handle cottle:")
    handle_u, handle_clip = cottle(hx0, hx1, hz0, hz1, hdepth, T, SKIN)
    print(f"handle plaster space {hx1-hx0:.1f} x {hdepth:.1f} x {hz1-hz0:.1f} mm, "
          f"~{((hx1-hx0)*hdepth*(hz1-hz0) - hhalf.volume)/1e6:.2f} L per half (one master, cast twice)")
    # the skin's rim reaches the cottle wall plane at each opening, so plaster cannot get behind it
    mouth = mp.HANDLE_L / 2 + mp.CUP_GROW
    rims = {"socket": body_master.is_inside((0, mp.R_RING - SKIN / 2, z0 - FIT / 2)),
            "collar": body_master.is_inside((0, mp.R_COLLAR - SKIN / 2, z1 + FIT / 2)),
            "handle cups": all(handle_master.is_inside((hb.min.X + 0.05, mouth - SKIN / 2, z))
                               for z in (zc - mp.HANDLE_R, zc + mp.HANDLE_R))}
    print("skin rims reach the cottle walls:", rims)
    assert all(rims.values())

    flat = Rot(90, 0, 0)                       # y = -plate (table side / open back) onto the bed
    save_print("body_master", body_master, Rot(0, 0, 0))   # standing on its socket end
    save_print("body_cottle", body_u, flat)
    save_print("body_clip", body_clip, flat)
    save_print("handle_master", handle_master, flat)
    save_print("handle_cottle", handle_u, flat)
    save_print("handle_clip", handle_clip, flat)


if __name__ == "__main__":
    main()
