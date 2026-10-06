#!/usr/bin/env python3
"""make_cottle_ring.py -- thin circular cottle STL (pure stdlib, no deps).

A straight ring by default. With --taper-to it becomes a funnel: the wall
goes straight up to --height, then angles inward (--taper-angle from
horizontal, default 45) until the opening is --taper-to mm across, to cut
the plaster volume above the piece.

usage: make_cottle_ring.py [--id 123.2] [--wall 0.8] [--height 27.5]
                           [--taper-to 61.6] [--taper-angle 45]
                           [--segments 360] [-o out.stl]
Axis along +z, open bottom on z=0, units mm.
"""
import argparse
import math
import struct


def profile(r_in, wall, h, taper_to=None, angle_deg=45.0):
    """Closed (r, z) cross-section of the wall, one loop."""
    r_out = r_in + wall
    if taper_to is None:
        return [(r_out, 0), (r_out, h), (r_in, h), (r_in, 0)]

    th = math.radians(angle_deg)
    s, c = math.sin(th), math.cos(th)
    r_ti = taper_to / 2
    zt = h + (r_in - r_ti) * math.tan(th)  # inner cone top / opening rim height
    # outer cone = inner cone offset by `wall` along its outward normal (s, c)
    t1 = (wall * s - wall) / c  # where it meets the vertical outer wall
    z1 = h + wall * c + t1 * s
    t2 = (zt - h - wall * c) / s  # where it meets the top plane z = zt
    r_to = r_in + wall * s - t2 * c
    return [(r_out, 0), (r_out, z1), (r_to, zt), (r_ti, zt), (r_in, h), (r_in, 0)]


def revolve(prof, n):
    def pt(k, i):
        r, z = prof[k % len(prof)]
        a = 2 * math.pi * (i % n) / n
        return (r * math.cos(a), r * math.sin(a), z)

    tris = []
    for k in range(len(prof)):
        for i in range(n):
            a, b = pt(k, i), pt(k, i + 1)
            c, d = pt(k + 1, i + 1), pt(k + 1, i)
            tris += [(a, b, c), (a, c, d)]
    # orient outward: signed volume must be positive
    vol = sum(
        (a[0] * (b[1] * c[2] - b[2] * c[1]) - a[1] * (b[0] * c[2] - b[2] * c[0]) + a[2] * (b[0] * c[1] - b[1] * c[0])) / 6
        for a, b, c in tris
    )
    if vol < 0:
        tris = [(a, c, b) for a, b, c in tris]
    return tris


def write_stl(path, tris):
    with open(path, "wb") as f:
        f.write(b"cottle".ljust(80, b"\0"))
        f.write(struct.pack("<I", len(tris)))
        for a, b, c in tris:
            u = [b[k] - a[k] for k in range(3)]
            v = [c[k] - a[k] for k in range(3)]
            nx = u[1] * v[2] - u[2] * v[1]
            ny = u[2] * v[0] - u[0] * v[2]
            nz = u[0] * v[1] - u[1] * v[0]
            m = math.sqrt(nx * nx + ny * ny + nz * nz) or 1.0
            f.write(struct.pack("<12fH", nx / m, ny / m, nz / m, *a, *b, *c, 0))


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--id", type=float, default=123.2, help="inner diameter mm")
    ap.add_argument("--wall", type=float, default=0.8)
    ap.add_argument("--height", type=float, default=4.0, help="height of the straight section")
    ap.add_argument("--taper-to", type=float, default=None, help="opening diameter of the funnel top (omit for a plain ring)")
    ap.add_argument("--taper-angle", type=float, default=45.0, help="funnel slope from horizontal, degrees")
    ap.add_argument("--segments", type=int, default=360)
    ap.add_argument("-o", "--out", default="cottle_ring_test.stl")
    a = ap.parse_args()
    prof = profile(a.id / 2, a.wall, a.height, a.taper_to, a.taper_angle)
    write_stl(a.out, revolve(prof, a.segments))
    total = max(z for _, z in prof)
    print(f"wrote {a.out}: ID {a.id} wall {a.wall} straight {a.height} total height {total:.2f}"
          + (f" opening {a.taper_to} @ {a.taper_angle} deg" if a.taper_to else ""))
