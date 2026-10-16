#!/usr/bin/env python3
"""check_design.py -- will the candle fit, and will the cast stand?

Mirrors the drafted half into a whole skull, hollows it to a --wall mm cast wall (crown left open, as it
is once the lid is cut), and reports, in mold mm and in fired mm (x (1 - --shrink)):
  - the widest circle that fits through the crown opening, against the candle plus --clearance
  - how deep the cavity is under the crown rim, against the candle height
  - where the hollow cast's centre of mass falls against the contact patches (incisors .. occiput)

Usage: python check_design.py drafted.stl [--wall 5] [--shrink 0.11] [--crown-height 79] [--boss-end 25]
"""
import argparse
from pathlib import Path

import numpy as np
from scipy import ndimage as ndi

from make_masters import load_half
from prep_skull import load_sad


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("drafted")
    ap.add_argument("--wall", type=float, default=5.0, help="cast wall, mold mm")
    ap.add_argument("--shrink", type=float, default=0.11, help="drying+firing linear shrinkage")
    ap.add_argument("--candle-d", type=float, default=40.0)
    ap.add_argument("--candle-h", type=float, default=20.0)
    ap.add_argument("--clearance", type=float, default=2.0, help="per side, fired mm")
    ap.add_argument("--crown-height", type=float, default=79.0)
    ap.add_argument("--boss-end", type=float, default=25.0)
    ap.add_argument("--boss-radius", type=float, default=16.0)
    ap.add_argument("--pitch", type=float, default=0.5)
    args = ap.parse_args()
    sad = load_sad()
    P, k = args.pitch, 1.0 - args.shrink

    half = load_half(args.drafted, args.boss_end, args.crown_height)
    arr, T = sad.voxelize_solid(half, P)
    o = T[:3, 3]
    full = np.concatenate([arr[::-1], arr], axis=0)          # x mirrored; parting plane is the seam
    ox = -arr.shape[0] * P + o[0]
    # drop the boss stub below the base plane: only the skull itself is the vessel
    zs = o[2] + np.arange(arr.shape[2]) * P
    full[:, :, zs < -0.5 * P] = False
    ztop = int(np.argmin(np.abs(zs - args.crown_height))) + 1
    padded = np.pad(full[:, :, :ztop], ((0, 0), (0, 0), (0, 8)), mode="edge")   # open crown: not a wall
    padded[:, :, ztop:] = full[:, :, ztop - 1:ztop]
    edt = ndi.distance_transform_edt(padded) * P
    interior = (edt > args.wall) & padded
    shell = padded & ~interior
    shell[:, :, ztop:] = False
    interior[:, :, ztop:] = False

    # candle fit: widest circle through the crown opening
    slab = interior[:, :, ztop - 2]
    D = 2 * ndi.distance_transform_edt(slab).max() * P
    need = args.candle_d + 2 * args.clearance
    print(f"opening: widest circle {D:.1f} mold mm = {D * k:.1f} fired; candle {args.candle_d:g} + clearance = {need:g} "
          f"-> {'fits' if D * k >= need else 'DOES NOT FIT'} ({D * k - need:+.1f} mm)")
    ys = np.nonzero(slab.any(axis=0))[0]
    xs = np.nonzero(slab.any(axis=1))[0]
    print(f"opening interior {(xs.max() - xs.min() + 1) * P * k:.0f} wide x {(ys.max() - ys.min() + 1) * P * k:.0f} long fired mm")

    # cavity depth: interior connected to the opening
    lab, _ = ndi.label(interior)
    top_labels = np.unique(lab[:, :, ztop - 2][lab[:, :, ztop - 2] > 0])
    cav = np.isin(lab, top_labels)
    zc = np.nonzero(cav.any(axis=(0, 1)))[0]
    depth = (ztop - zc.min()) * P
    print(f"cavity under the rim: {depth:.0f} mold mm = {depth * k:.0f} fired; candle {args.candle_h:g} mm sits at the bottom, "
          f"flame ~{depth * k - args.candle_h:.0f} mm below the rim")

    # stance
    ix, iy, iz = np.nonzero(shell)
    com = np.array([ix.mean() * P + ox, iy.mean() * P + o[1], iz.mean() * P + o[2]])
    base = np.nonzero(full[:, :, np.argmin(np.abs(zs - 0.4))])
    yb = o[1] + base[1] * P
    yb = yb[np.abs(yb) > args.boss_radius + 4]               # the boss column is cut off after casting
    print(f"hollow cast: {shell.sum() * P ** 3 / 1000:.0f} cm3 of clay mold-scale; centre of mass y={com[1]:.1f}, z={com[2]:.1f}")
    print(f"contact patches (z<0.4 plane) span y {yb.min():.1f} .. {yb.max():.1f}; COM sits "
          f"{min(com[1] - yb.min(), yb.max() - com[1]):.0f} mm inside the nearer edge")


if __name__ == "__main__":
    main()
