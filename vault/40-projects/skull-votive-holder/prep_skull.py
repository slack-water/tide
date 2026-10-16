#!/usr/bin/env python3
"""prep_skull.py -- hemisected skull scan -> half-skull "votive holder" positive, ready for `draft`.

Stage 1 of 2 (stage 2 is make_masters.py). Takes the left-half scan (parting plane x=0, pull axis X,
face toward -Y, up +Z) and:

  1. removes the lower jaw. The mandible is fused to the skull at the bite and at the jaw joint, so a
     plane cut cannot separate it (the ramus rises above any plane through the teeth). Instead: a
     min-cut on the voxel graph with seeds known to be mandible vs skull. The cut falls on the thinnest
     necks, which are the tooth contacts and the joint. Seeds are in SEEDS below; the cut surface is
     smoothed so it does not inherit the coarse grid's staircase.
  2. poses the skull the way a jawless skull rests on a table: on the upper incisors and the base of the
     occiput. That is the longest downward edge of the (y,z) convex hull; the skull is rotated about X
     (the pull axis, so the sagittal split is unaffected) until that edge is level. --extra-tilt then
     pitches it further (positive = face up / tipped back).
  3. scales (mold mm from here on), trims --foot-trim off the bottom so the incisors and occiput get
     flat bearing patches, and cuts the crown flat at --crown-height above the base plane. The candle
     drops in through the crown cut.
  4. fuses the pour boss: a half-cylinder (axis Z, centre on the parting plane) from below the base up
     into the skull base, at --boss-y. Its tip is at z = -boss-length, and the flange (make_masters.py)
     is flush with that tip, as in choochoomug-14oz.

Output is an STL in mold mm: parting face at x=0, base plane z=0, boss below it. Large intermediate
grids; needs roughly 4 GB at the default pitch.

Usage: python prep_skull.py [--scan ~/Downloads/"Skull (Left).stl"] [--scale 1.1] [--crown-height 79] \
           [--extra-tilt 0] [--boss-radius 16] [--boss-y 0] [--boss-length 25] [-o prep.stl] [--preview DIR]
"""
import argparse
import importlib.util
import sys
from pathlib import Path

import numpy as np
import scipy.sparse as sp
import trimesh
from scipy import ndimage as ndi
from scipy.sparse.csgraph import breadth_first_order, maximum_flow
from scipy.spatial import ConvexHull

HERE = Path(__file__).parent
DRAFT = HERE.parent.parent / "90-archive" / "skull-mold-draft-shell" / "stl_add_draft.py"


def load_sad():
    spec = importlib.util.spec_from_file_location("stl_add_draft", DRAFT)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def bite_z(y):
    """Height of the incisor/canine bite line (scan mm), read off the lateral view."""
    return 21.5 - 0.046 * (y + 62.0)


def seeds(X, Y, Z):
    """Voxel centres known to be mandible (src) or skull (snk), scan frame. Measured on Skull (Left).stl."""
    zb = bite_z(Y)
    front = Y < -52           # incisors and canines: bite line is a clean gap
    premol = (Y >= -52) & (Y < -33) & (X < 20)
    src = ((Z < 17) & (Y < -6)                                   # chin and body of the jaw
           | (Z < 19) & (Y < -33)                                # below the molar bite
           | front & (Z < zb - 0.7) | premol & (Z < zb - 0.5)    # lower teeth
           | (X > 22) & (Y > -30) & (Y < -5) & (Z < 28))         # ramus
    snk = ((Z > 23.5) & (Y < -33)                                # maxilla and teeth
           | front & (Z > zb + 0.7) | premol & (Z > zb + 0.5)
           | (Z > 38)                                            # vault, zygomatic arch
           | (Y > 0) & (Z > 20)                                  # back of the skull
           | (X < 20) & (Y > -30) & (Y < 0) & (Z > 25))          # skull base
    return src, snk & ~src


def mandible_labels(sad, mesh, pitch=0.5):
    """Coarse min-cut. Returns (mandible float mask smoothed, transform) on a pitch-mm grid."""
    arr, T = sad.voxelize_solid(mesh, pitch)
    o = T[:3, 3]
    ii = np.full(arr.shape, -1, np.int64)
    ids = np.flatnonzero(arr.ravel())
    ii.ravel()[ids] = np.arange(len(ids))
    n = len(ids)
    ix, iy, iz = np.nonzero(arr)
    src, snk = seeds(o[0] + ix * pitch, o[1] + iy * pitch, o[2] + iz * pitch)
    print(f"min-cut: {n} voxels, {src.sum()} mandible seeds, {snk.sum()} skull seeds")
    rows, cols = [], []
    for ax in range(3):
        a = [slice(None)] * 3
        b = [slice(None)] * 3
        a[ax], b[ax] = slice(0, -1), slice(1, None)
        A, B = ii[tuple(a)].ravel(), ii[tuple(b)].ravel()
        ok = (A >= 0) & (B >= 0)
        rows.append(A[ok])
        cols.append(B[ok])
    r, c = np.concatenate(rows), np.concatenate(cols)
    s_node, t_node, big = n, n + 1, 10 ** 6
    rr = np.concatenate([r, c, np.full(src.sum(), s_node), np.flatnonzero(snk)])
    cc = np.concatenate([c, r, np.flatnonzero(src), np.full(snk.sum(), t_node)])
    w = np.concatenate([np.full(2 * len(r), 1000), np.full(src.sum(), big), np.full(snk.sum(), big)]).astype(np.int32)
    G = sp.csr_matrix((w, (rr, cc)), shape=(n + 2, n + 2))
    res = maximum_flow(G, s_node, t_node)
    print(f"min-cut area {res.flow_value / 1000 * pitch ** 2:.0f} mm2")
    resid = (G - res.flow).tocsr()
    resid.data = np.where(resid.data > 0, 1, 0)
    resid.eliminate_zeros()
    reach = np.zeros(n + 2, bool)
    reach[breadth_first_order(resid, s_node, directed=True, return_predecessors=False)] = True
    # the minimal source side leaves unseeded jaw on the skull side: grow the mandible to everything
    # not reachable from the skull seeds instead, then take the midpoint of the two cuts
    resid_t = resid.T.tocsr()
    reach_t = np.zeros(n + 2, bool)
    reach_t[breadth_first_order(resid_t, t_node, directed=True, return_predecessors=False)] = True
    mand = reach[:n] | ~reach_t[:n]
    mask = np.zeros(arr.shape, np.float32)
    mask[ix, iy, iz] = mand
    mask = ndi.gaussian_filter(mask, 1.2) > 0.5
    return mask & arr, arr, T


def skull_mesh(sad, scan, pitch, coarse_pitch=0.5):
    mand_c, arr_c, Tc = mandible_labels(sad, scan, coarse_pitch)
    arr, T = sad.voxelize_solid(scan, pitch)
    oc, o = Tc[:3, 3], T[:3, 3]
    idx = [np.round((o[a] + np.arange(arr.shape[a]) * pitch - oc[a]) / coarse_pitch).astype(int) for a in range(3)]
    ok = [(i >= 0) & (i < arr_c.shape[a]) for a, i in enumerate(idx)]
    idx = [np.clip(i, 0, arr_c.shape[a] - 1) for a, i in enumerate(idx)]
    mand = mand_c[np.ix_(*idx)] & ok[0][:, None, None] & ok[1][None, :, None] & ok[2][None, None, :]
    skull = arr & ~mand
    lab, nlab = ndi.label(skull)
    sizes = ndi.sum(skull, lab, range(1, nlab + 1))
    skull = lab == (1 + int(np.argmax(sizes)))
    print(f"skull {skull.sum() * pitch ** 3 / 1000:.1f} cm3, jaw removed {(arr & ~skull).sum() * pitch ** 3 / 1000:.1f} cm3, "
          f"{nlab - 1} stray pieces dropped")
    sdf = (ndi.distance_transform_edt(skull) - ndi.distance_transform_edt(~skull)).astype(np.float32)
    sdf = ndi.gaussian_filter(sdf, 1.0)
    return sad.field_to_mesh(sdf, T, level=0.0, pad_value=float(sdf.min()) - 1.0)


def rest_rotation(mesh):
    """Angle (rad, about +X) that levels the longest downward edge of the (y,z) hull."""
    pts = np.unique(mesh.vertices[:, 1:].round(2), axis=0)
    h = ConvexHull(pts)
    best = None
    for simplex, eq in zip(h.simplices, h.equations):
        if eq[1] < -0.5:
            a, b = pts[simplex]
            if a[0] > b[0]:
                a, b = b, a
            length = np.hypot(*(b - a))
            if best is None or length > best[0]:
                best = (length, a, b)
    _, a, b = best
    alpha = np.arctan2(b[1] - a[1], b[0] - a[0])
    print(f"rest edge ({a[0]:.1f},{a[1]:.1f}) -> ({b[0]:.1f},{b[1]:.1f}), {np.degrees(alpha):.1f} deg from scan-upright")
    return -alpha


def keep_half_above(mesh, origin, normal):
    return mesh.slice_plane(origin, normal, cap=True)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--scan", default=str(Path.home() / "Downloads" / "Skull (Left).stl"))
    ap.add_argument("--scale", type=float, default=1.1, help="uniform scale of the scan (mold mm from here on)")
    ap.add_argument("--pitch", type=float, default=0.2, help="voxel size for the jaw-removed surface (scan mm)")
    ap.add_argument("--extra-tilt", type=float, default=0.0, help="degrees beyond the natural rest pose; + = face up")
    ap.add_argument("--foot-trim", type=float, default=6.5, help="mm cut off the bottom for flat bearing patches")
    ap.add_argument("--crown-height", type=float, default=79.0, help="crown cut, mm above the base plane (mold mm)")
    ap.add_argument("--boss-radius", type=float, default=16.0)
    ap.add_argument("--boss-y", type=float, default=0.0, help="boss centre along Y in the rest frame (mold mm)")
    ap.add_argument("--boss-length", type=float, default=30.0,
                    help="boss tip below the base plane (mold mm); make_masters.py re-cuts it flat 5 mm short, "
                         "because the draft slopes the tip face")
    ap.add_argument("-o", "--out", default=str(HERE / "prep.stl"))
    ap.add_argument("--preview", default=None, help="directory for check renders")
    args = ap.parse_args()

    sad = load_sad()
    scan = trimesh.load(args.scan, force="mesh")
    assert scan.is_watertight, "scan must be watertight"
    skull = skull_mesh(sad, scan, args.pitch)

    theta = rest_rotation(skull) - np.radians(args.extra_tilt)
    skull.apply_transform(trimesh.transformations.rotation_matrix(theta, [1, 0, 0]))
    skull.apply_scale(args.scale)
    skull.apply_translation([0, 0, -skull.bounds[0][2]])
    print(f"posed+scaled bounds {np.round(skull.bounds, 1).tolist()}")

    # foot trim, parting plane, crown cut
    skull = keep_half_above(skull, [0, 0, args.foot_trim], [0, 0, 1])
    skull.apply_translation([0, 0, -args.foot_trim])
    skull = keep_half_above(skull, [0, 0, 0], [1, 0, 0])
    skull = skull.slice_plane([0, 0, args.crown_height], [0, 0, -1], cap=True)

    # pour boss: half-cylinder on the parting plane, from the tip up into the skull base
    top = 14.0
    cyl = trimesh.creation.cylinder(radius=args.boss_radius, height=args.boss_length + top, sections=96)
    cyl.apply_translation([0, args.boss_y, (top - args.boss_length) / 2])
    boss = cyl.slice_plane([0, 0, 0], [1, 0, 0], cap=True)
    out = trimesh.boolean.union([skull, boss], engine="manifold")
    out.export(args.out)
    print(f"wrote {args.out}: bounds {np.round(out.bounds, 1).tolist()} watertight={out.is_watertight} "
          f"volume {out.volume / 1000:.1f} cm3")

    if args.preview:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
        Path(args.preview).mkdir(parents=True, exist_ok=True)
        fig, ax = plt.subplots(1, 3, figsize=(21, 7))
        for a, x in zip(ax, [1, 12, 25]):
            sec = out.section(plane_origin=[x, 0, 0], plane_normal=[1, 0, 0])
            if sec is not None:
                for e in sec.entities:
                    p = sec.vertices[e.points]
                    a.plot(p[:, 1], p[:, 2], "k", lw=0.8)
            a.axhline(0, color="r", lw=0.5)
            a.set_aspect("equal")
            a.set_title(f"x={x}")
            a.grid(alpha=0.3)
        plt.savefig(Path(args.preview) / "prep_sections.png", dpi=60, bbox_inches="tight")


if __name__ == "__main__":
    main()
