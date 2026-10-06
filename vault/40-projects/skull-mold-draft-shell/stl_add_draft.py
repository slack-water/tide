#!/usr/bin/env python3
"""
stl_add_draft.py

WHAT THIS IS FOR
=================
Prepares a scanned mesh (originally written for a half-skull STL, cut flush
along a sagittal midline) to be 3D-printed as a positive, pressed into wet
plaster to make a mold, then pulled back out. For that to work the shape
must have NO UNDERCUTS along the direction it gets pulled out ("pull axis"/
"draft axis") -- any surface that curves back over itself in that direction
would lock the plaster and tear the mold apart on release. This script adds
the minimum extra material needed to eliminate undercuts (`draft` command),
optionally with a draft *angle* (a slight taper) so the fit is generous
rather than a knife-edge fit that binds. It can also hollow the result into
a thin constant-thickness shell (`shell` command) so the print can later be
packed with something like frozen isopropyl alcohol to help shrink it loose
from the mold. A third command, `negative`, goes the other direction: it
carves the drafted solid OUT of a margin-padded block, producing a
directly 3D-printable mold half (a rigid cavity you pour into) instead of
a positive you press into plaster -- same draft/undercut requirement,
same pull axis, just subtracted instead of shelled. A fourth command,
`mirror`, is just a flat reflection across the parting plane -- handy for
turning a finished half (e.g. the left side of a hemisected skull) into
its opposite-side counterpart (a right side) without redoing any of the
draft/shell/negative work.

Both commands work by voxelizing the mesh (turning it into a 3D grid of
filled/empty cells), doing the geometric operation on that grid with array
math, then re-extracting a surface mesh from the result via marching cubes
(`skimage.measure.marching_cubes`). Voxel grids make "grow the shape in one
direction only" and "measure distance to the nearest surface" trivial to
express correctly; the tradeoff is you need enough resolution (small enough
--pitch) to avoid visible voxel/staircase artifacts, and enough care in how
the grid gets turned back into a mesh to avoid re-introducing those
artifacts during that final re-surfacing step.

--- draft command ---

Step 1, plain undercut removal (always happens, this is the "draft" concept
before any angle is added): voxelize the mesh, then for every column of
voxels running along the pull axis, find the topmost (or bottommost, if
--base max) occupied voxel and fill the entire column solid between the
parting-plane end and that point. Concretely this is a per-column flood-
fill: nothing above (tip-ward of) the highest point in a column can be an
undercut once everything below it is solid, because the mold could never
have reached that undercut anyway once the column beneath it is filled in.

Step 2, optional draft angle (--draft N, a percentage grade): instead of a
perfectly straight (0 degree) fill, make the filled region cone-shaped: as
you sweep from the tip (the point on the pull axis farthest from the
parting plane) back down toward the base (the parting plane itself), the
allowed fill radius grows by N% of the axial distance traveled so far. This
gives the print some clearance in the mold instead of an exact knife-edge
friction fit, which both eases release and forgives small print/scan
inaccuracies. The math for this (see draft_correct's docstring) is solved
in one closed-form pass across the whole grid, NOT as an iterative "grow by
a bit, repeat" loop -- an earlier version of this script tried the
iterative approach and it was a silent no-op: distance_transform_edt only
resolves whole-pixel distances, so thresholding at a sub-1-voxel radius
against a freshly recomputed mask every iteration never accumulates any
visible growth, no matter how many iterations you run.

Step 3, optional crease-rounding blur (--blur SIGMA): the draft fill from
step 2 is exact, but on a real scanned surface with several separate
undercut features close together (e.g. neighboring teeth), each one casts
its own draft cone, and where two neighboring cones' fill regions meet you
get a real sharp crease in the final surface -- this is genuine geometry,
not a resolution/aliasing artifact, so plain mesh smoothing (--smooth)
mostly just fights it unproductively (or has to run so many iterations it
shrinks/rounds off real anatomical detail elsewhere to make a dent in it).
--blur applies a 3D Gaussian blur directly to the distance field before
re-surfacing, which rounds these creases at the geometry level, but ONLY
inside the newly-added draft material (feathered at the edge so the
transition doesn't itself create a new seam) -- so the original scanned
surface, teeth included, is completely untouched no matter how high you
turn --blur up.

Step 4, re-surfacing: rather than running marching cubes directly on the
0/1 filled/empty grid (which forces every crossing to sit exactly halfway
between a filled and an empty voxel -- fine for a straight 0 degree pull,
but this is what produces a visible staircase on a shallow-sloped draft
surface, since the true surface is almost parallel to the voxel grid
there), the final filled/empty grid is converted to a full 3D signed
distance field (positive inside, negative outside, magnitude = distance to
the nearest surface -- this is simply EDT(filled) - EDT(~filled), so
"inside" naturally comes out positive since that's the array being handed
to EDT first) and THAT continuous field is what marching cubes actually
surfaces. Because the field varies continuously between grid
points, marching cubes can interpolate the true sub-voxel crossing position
instead of snapping to the voxel grid, which removes the staircase without
needing extra resolution.

  *** IMPORTANT gotcha discovered the hard way: this signed distance field
  MUST be computed in one shot, as a genuine 3D operation, on the FINAL
  filled/empty grid (scipy.ndimage.distance_transform_edt on the whole 3D
  array). Do NOT try to build a continuous field out of the per-2D-slice
  distance values used internally by the draft-angle math in step 2 (i.e.
  the `slice_dist`/`g`/`h` arrays in draft_correct) -- those are each valid
  and smooth WITHIN their own slice, but have no relationship to each
  other's values from one slice to the next, since each is computed
  independently in 2D. Feeding that stack of unrelated 2D fields to
  marching cubes as if it were one continuous 3D field produced a
  genuinely broken result the first time this was tried: a mesh that was
  recognizable as the right overall shape but covered in wild spikes,
  because marching cubes was linearly interpolating between axially-
  adjacent grid points whose values had no real geometric relationship to
  each other. The fix is exactly what step 4 does: commit to a hard
  filled/empty decision first (booleans don't care whether the field that
  produced them was continuous or not), THEN compute one proper full-3D
  distance field on that final result. ***

Usage:
    python stl_add_draft.py draft input.stl output.stl \
        --pull-axis x --base min --pitch 0.15 --draft 5 --blur 6 \
        --smooth 20 --smooth-method taubin

--- shell command ---

Voxelize the (typically already draft-corrected) mesh, then use a 3D
Euclidean distance transform to find every voxel within --thickness of the
true surface -- this gives a constant wall thickness measured as actual
nearest-surface distance, which is important for an irregular anatomical
shape (a naive "scale a copy down by X% and subtract it" shell would end up
with wildly uneven wall thickness: thin over convex areas like a cheekbone,
thick over concave ones like an eye socket, because percentage-scaling
moves every point toward one single center rather than moving each point
inward by a constant distance along the local surface normal).

The parting-plane face (the flat cut end at the base) is deliberately
treated as an already-open mouth during this computation, not a surface to
wall off: it's padded as solid material rather than empty space before the
distance transform runs, so the transform never "sees" it as a nearby
exterior surface needing its own wall. Every other face -- the true
anatomical/scanned surface, including the tip end -- is padded as empty and
gets a normal offset wall. The practical effect: the result has no cap at
the base, just the rim where the curved outer wall meets the opening --
shaped like a bowl, so it can be packed with something (e.g. frozen
isopropyl alcohol) after the plaster mold is poured, to help shrink/release
the printed part.

Usage:
    python stl_add_draft.py shell input.stl output.stl \
        --pull-axis x --base min --thickness 2.0 --pitch 0.2 --smooth 8

--- negative command ---

Takes the same kind of input as `shell` (an already draft-corrected,
undercut-free solid -- NOT the shelled positive, and not the raw
pre-draft scan) and produces the opposite kind of print: instead of a
thin positive you press into wet plaster, this carves that solid directly
out of a rectangular block, leaving a skull-shaped cavity -- a mold you
can 3D-print and pour directly into, skipping the physical plaster-
pressing step entirely.

The undercut-free requirement is the same and for a symmetric reason: a
positive with no undercuts along the pull axis can be pulled out of a
mold along that axis; a cavity with no undercuts along that same axis
lets the CAST piece be pulled back OUT of this mold along it afterward.
So `negative` reuses whatever draft angle/blur was already baked into the
input by `draft` -- it has no draft/blur options of its own.

HOW: voxelize the drafted solid, then build a second, all-True "block"
array around it -- padded by `--margin` on every side EXCEPT the base
(parting-plane) end of the pull axis, which is left flush with the
mesh's own base layer rather than padded. The cavity is simply
`block & ~mesh` (every block voxel that isn't part of the solid). Unlike
`shell`, this needs no special "treat the base face as already open"
padding trick: because the block isn't padded past the base plane, and
the mesh's own base layer is exactly the object's flat parting-plane
footprint, `block & ~mesh` at that layer is ALREADY empty everywhere the
object's footprint is -- so the cavity is a skull-shaped hole straight
through the block's top face by construction, without needing to be
told not to cap it there. Standard field_to_mesh boundary padding then
correctly caps every other face of the block (the true solid exterior
walls) while leaving that hole alone (empty bordered by more empty caps
nothing).

Usage:
    python stl_add_draft.py negative input.stl output.stl \
        --pull-axis x --base min --margin 8 --pitch 0.2 --smooth 8

--- mirror command ---

Reflects every vertex across a plane perpendicular to --axis at coordinate
--plane (default 0.0 -- e.g. for this project's convention of the parting
-plane/centerline sitting at x=0, mirroring across x=0 turns a left-side
STL into an anatomically correct right side, sitting on the opposite side
of the same centerline it was cut at). No voxelizing, no re-surfacing, no
smoothing -- it's an exact, lossless reflection of whatever mesh you feed
it, so run it LAST, on an already-finished draft+shell result, not on the
raw scan (there's nothing to gain by mirroring first and doing draft/shell
work twice, and every asymmetric measurement -- draft angle, blur, shell
thickness -- would need to be repeated identically on both sides anyway
since the two halves start out geometrically identical before any of that
processing).

Reflection flips handedness, which inverts every face's winding order --
left uncorrected this would flip all the normals inside-out (a solid mesh
that LOOKS right but whose "outside" is measured as "inside", which some
slicers handle fine and others render as an inverted/see-through mess).
mirror_mesh reverses each face's vertex order to undo exactly that, so the
output is oriented the same way (still watertight, still not accidentally
inverted) as the input.

Usage:
    python stl_add_draft.py mirror input.stl output.stl --axis x --plane 0.0

Run `python stl_add_draft.py draft --help`, `... shell --help`,
`... negative --help`, or `... mirror --help` for the full up-to-date
list of flags with explanations (kept in sync with this docstring, but
that's the authoritative source since argparse enforces it).
"""

import argparse
import sys
import numpy as np
import trimesh
from scipy import ndimage
from skimage import measure


AXES = {"x": 0, "y": 1, "z": 2}


def voxelize_solid(mesh: trimesh.Trimesh, pitch: float):
    """
    Turn a watertight mesh into a solid-filled 3D boolean grid ("voxel
    grid"), where True means "inside the mesh".

    HOW: cast one ray straight up (+Z) through every (x,y) column of the
    grid, from below the mesh's bounding box. Where a ray crosses the mesh
    surface, it's either entering or exiting the solid; since the mesh is
    watertight, crossings along one ray must alternate entry/exit/entry/...
    in order along the ray. So: sort each ray's crossing points by Z, pair
    them up (1st-2nd, 3rd-4th, ...), and mark every voxel between each pair
    as filled. This handles multiple separate solid regions stacked along
    the same column correctly (e.g. a ray passing through two separate
    horizontal slabs of material). This is the standard even-odd /ray-
    casting solid-voxelization algorithm.

    WHY NOT trimesh's built-in `mesh.voxelized(pitch).fill()`: that method
    subdivides every triangle until each piece is smaller than one voxel,
    which for a big, messy raw 3D scan (hundreds of thousands of
    triangles) at a fine pitch generates an enormous number of subdivided
    triangles and can blow up in time/memory well before this scanline
    approach even gets warm. This function instead casts a fixed number of
    rays (one per grid column) against the ORIGINAL triangle count using
    trimesh's ray-BVH acceleration structure, so its cost scales with grid
    resolution and mesh complexity, not with how many times a triangle had
    to be chopped up to fit inside one voxel.

    (There's also `trimesh.voxel.creation.voxelize(..., method='ray')`,
    which sounds like the same idea, but it only marks the individual
    surface-crossing points themselves, not the solid interior between
    them -- so `.fill()` on top of it does essentially nothing for this
    kind of mesh. Not used here for that reason.)

    Returns (arr, transform):
      arr        bool ndarray, shape (nx, ny, nz). arr[i,j,k] is True if
                 that voxel is inside the mesh.
      transform  4x4 matrix mapping a voxel's (i,j,k) index (as float,
                 e.g. via trimesh.transform_points) to its world-space
                 center coordinate. Same convention as
                 trimesh.voxel.base.VoxelGrid.transform, so it's a drop-in
                 replacement anywhere that was used.
    """
    mins, maxs = mesh.bounds
    nx = int(np.ceil((maxs[0] - mins[0]) / pitch)) + 1
    ny = int(np.ceil((maxs[1] - mins[1]) / pitch)) + 1
    nz = int(np.ceil((maxs[2] - mins[2]) / pitch)) + 1

    # One ray per (x,y) voxel column, centered on that column, starting
    # comfortably below the mesh so every ray's first crossing is a true
    # entry into the solid.
    xs = mins[0] + (np.arange(nx) + 0.5) * pitch
    ys = mins[1] + (np.arange(ny) + 0.5) * pitch
    gx, gy = np.meshgrid(xs, ys, indexing="ij")
    ray_origins = np.column_stack(
        [gx.ravel(), gy.ravel(), np.full(gx.size, mins[2] - pitch)]
    )
    ray_dirs = np.tile([0.0, 0.0, 1.0], (len(ray_origins), 1))

    locations, index_ray, _ = mesh.ray.intersects_location(
        ray_origins, ray_dirs, multiple_hits=True
    )

    arr = np.zeros((nx, ny, nz), dtype=bool)
    # intersects_location returns hits in no particular per-ray order, so
    # group them by which ray they belong to (index_ray) and sort each
    # ray's own hits by Z before pairing them up.
    order = np.argsort(index_ray, kind="stable")
    index_ray_s = index_ray[order]
    z_hits_s = locations[order, 2]
    unique_rays, start_idx = np.unique(index_ray_s, return_index=True)
    start_idx = list(start_idx) + [len(index_ray_s)]
    for k, ray_i in enumerate(unique_rays):
        zs = np.sort(z_hits_s[start_idx[k]:start_idx[k + 1]])
        if len(zs) < 2:
            continue
        ix, iy = divmod(ray_i, ny)
        z_idx = np.round((zs - mins[2]) / pitch).astype(np.int64)
        # pair up crossings (entry, exit, entry, exit, ...) by parity, and
        # fill solid between each entry/exit pair
        for j in range(0, len(z_idx) - (len(z_idx) % 2), 2):
            a, b = z_idx[j], z_idx[j + 1]
            a = max(a, 0)
            b = min(b, nz - 1)
            if a <= b:
                arr[ix, iy, a:b + 1] = True

    transform = np.eye(4)
    transform[0, 0] = transform[1, 1] = transform[2, 2] = pitch
    transform[:3, 3] = mins + 0.5 * pitch
    return arr, transform


def field_to_mesh(field: np.ndarray, transform: np.ndarray,
                   level: float = 0.5, pad_value: float = 0.0) -> trimesh.Trimesh:
    """
    Turn a 3D scalar grid back into a surface mesh via marching cubes,
    then map the result from voxel-index coordinates back to world/mesh
    coordinates using `transform` (see voxelize_solid).

    `field` can be either:
      - a plain 0/1 (or bool-as-float) occupancy grid, with level=0.5 and
        pad_value=0.0 (the defaults) -- the extracted surface always sits
        exactly halfway between a 0 voxel and a 1 voxel, since that's the
        only information a binary field carries. Fine for a straight
        (non-drafted, non-shallow-sloped) surface; this is what produces
        visible voxel staircasing on shallow slopes, since real sub-voxel
        crossing position is lost.
      - a continuous signed field, e.g. a true distance transform (positive
        inside, negative outside, magnitude = distance to the surface --
        see draft_correct/shell_correct for how it's built: EDT(filled) -
        EDT(~filled)), with level=0.0 and pad_value below the field's
        global minimum (i.e. even more "outside" than anything real in the
        field, so padding never fabricates a false inside/solid region).
        Marching cubes then linearly
        interpolates between neighboring grid samples to find the exact
        zero-crossing, recovering the true sub-voxel surface position.
        This is what removes staircase artifacts on shallow slopes (like
        a draft cone) without needing finer --pitch or heavier --smooth.

    `pad_value` matters because the grid is padded by one voxel on every
    side before surfacing (see below) so marching cubes can close off the
    shape at the boundary instead of leaving it open where the array ends.
    """
    print("Re-surfacing with marching cubes ...")
    # Pad by 1 voxel on every side so the object's boundary is always
    # fully enclosed inside the padded array -- otherwise a shape that
    # touches the edge of the array would come out with a hole/opening
    # there instead of a properly closed surface.
    padded = np.pad(field, 1, mode="constant", constant_values=pad_value)
    verts, faces, normals, _ = measure.marching_cubes(
        padded.astype(np.float32), level=level
    )
    # Undo the 1-voxel padding offset, then map voxel-index space -> world
    # space using the affine transform computed in voxelize_solid.
    verts -= 1.0
    verts = trimesh.transform_points(verts, transform)

    # skimage winds faces for a field that is LOWER inside, but every field
    # this script builds is positive inside (see docstring above), so the
    # raw output comes out inside-out (negative volume, normals pointing
    # into the material). Verified on a synthetic sphere: volume -4166 as-is,
    # +4166 flipped. Slicers tend to silently auto-repair this, which is how
    # it went unnoticed, but anything that trusts normals (overhang/support
    # analysis, boolean ops) gets it backwards. Flip so output is outward-
    # facing like the input scan.
    faces = faces[:, ::-1]

    out = trimesh.Trimesh(vertices=verts, faces=faces, process=True)
    out.remove_unreferenced_vertices()
    return out


def smooth_mesh(mesh: trimesh.Trimesh, iterations: int, method: str):
    """
    Post-process smoothing to soften whatever voxel-resolution roughness
    is left after marching cubes. Mutates `mesh` in place (trimesh's
    smoothing filters operate in place); does nothing if iterations <= 0.

    'taubin' vs 'laplacian': plain Laplacian smoothing repeatedly moves
    each vertex toward the average of its neighbors, which is simple and
    effective but also shrinks the mesh a little on every iteration --
    stack enough iterations and it visibly eats into fine detail (like
    individual teeth) and thins out margins you added on purpose (draft
    clearance, shell wall thickness). Taubin smoothing alternates a
    shrinking pass with a subsequent inflating pass tuned to cancel out
    the average shrinkage, so it can be run for many more iterations with
    ~no net volume loss -- use this whenever pushing --smooth high.
    """
    if iterations <= 0:
        return
    print(f"Smoothing ({method}, {iterations} iterations) ...")
    if method == "taubin":
        trimesh.smoothing.filter_taubin(mesh, iterations=iterations)
    else:
        trimesh.smoothing.filter_laplacian(mesh, iterations=iterations)


def mirror_mesh(mesh: trimesh.Trimesh, axis: int, plane: float = 0.0) -> trimesh.Trimesh:
    """
    Reflect `mesh` across the plane perpendicular to `axis` at coordinate
    `plane` (e.g. axis=0 ("x"), plane=0.0 reflects across the y-z plane
    where x=0). See the module docstring's "mirror command" section for
    when/why to use this (short version: run it last, on a finished
    draft+shell result, not on the raw pre-processed scan).

    A reflection is an orientation-reversing transform -- it turns a
    right-handed coordinate frame into a left-handed one -- which flips
    every triangle's winding order (the order its 3 vertices are listed
    in, which is how a mesh encodes which side is "outside"). If left
    alone, that inverts every face normal: the geometry would look
    correct but be inside-out from a solid-modeling point of view (volume
    computations flip sign, some slicers/viewers render it as a hollow
    see-through mess instead of a solid). Reversing each face's own vertex
    order (faces[:, ::-1]) undoes exactly that flip, so the output is a
    solid mesh with the same "which side is outside" convention as the
    input -- this is the standard fix for mirroring any triangle mesh, not
    specific to this script.
    """
    verts = mesh.vertices.copy()
    verts[:, axis] = 2.0 * plane - verts[:, axis]
    faces = mesh.faces[:, ::-1]
    out = trimesh.Trimesh(vertices=verts, faces=faces, process=True)
    out.remove_unreferenced_vertices()
    return out


def draft_correct(mesh: trimesh.Trimesh, axis: int, base: str, pitch: float,
                   draft_pct: float = 0.0, blur_sigma: float = 0.0) -> trimesh.Trimesh:
    """
    Add the minimum material needed to remove undercuts along `axis`
    (pulling apart from the `base` end), optionally with a draft angle
    and/or crease-rounding blur. See the module docstring's "draft
    command" section for the full picture; this docstring covers the
    step-2 draft-angle math in detail since it's the least obvious part.

    Args:
      axis        0/1/2 for x/y/z -- the pull/draft axis.
      base        'min' or 'max' -- which end of `axis` is the parting
                  plane (the fixed/open end the mold pulls away from).
      pitch       voxel size, same units as the mesh.
      draft_pct   percentage grade (0 = straight pull, no taper).
      blur_sigma  Gaussian sigma in voxels for crease rounding (0 = off).

    --- The draft-angle math (step 2) ---

    Think of the pull axis as a stack of n 2D cross-section slices, indexed
    i = 0..n-1, with d(i) = distance (in voxel steps) from slice i to the
    base (so d=0 at the base, d=n-1 at the far tip). With a draft angle,
    the allowed growth radius at slice i is r(i) = d(i) * step_radius
    (step_radius = draft_pct/100, i.e. "radius grown per voxel of axial
    travel").

    A voxel (i, y, z) should end up filled if there's SOME occupied voxel
    (i', y', z') at least as close to the tip as i (i.e. d(i') >= d(i)) --
    including i itself -- whose in-plane (2D, same-slice) distance to
    (y, z) is within the radius budget available by the time you've swept
    from i' back to i. That available budget is the DIFFERENCE in radius
    between the two slices: r(i') - r(i). So the fill condition is:

        exists i' (with d(i') >= d(i)) and in-plane distance
        dist2d((y,z), occupied-region-of-slice-i') <= r(i') - r(i)

    Rearranged so i and i' are on opposite sides of a "<=":

        d(i)*step_radius  <=  d(i')*step_radius - dist2d

    Define, independently per slice i' (this is the only per-slice, 2D-only
    piece of the computation):

        g(i') = slice_dist(i')  -  d(i')*step_radius

    where slice_dist(i') is the ordinary 2D Euclidean distance transform of
    slice i' (distance from every point to the nearest occupied point
    WITHIN THAT SAME SLICE; 0 wherever the slice is already occupied).
    Then the fill condition for voxel (i,y,z) becomes, after minimizing
    over every valid candidate i':

        h(i,y,z) = min over i' with d(i') >= d(i) of g(i')(y,z)
        filled  iff  h(i,y,z) <= -d(i)*step_radius

    h is computed in one vectorized pass as a running (suffix) minimum of
    g, swept from the tip slice toward the base -- so every slice's h
    reuses the previous slice's h rather than re-scanning all farther
    slices from scratch. This whole thing is a closed-form, exact,
    one-shot computation -- deliberately NOT an iterative "grow the mask
    by a bit, re-measure, repeat" loop. An earlier version of this script
    used that iterative approach and it was a silent, total no-op: each
    iteration re-ran distance_transform_edt (whole-pixel resolution) on a
    freshly snapshotted boolean mask and thresholded at a sub-1-voxel
    radius, so no sub-voxel "progress" ever survived between iterations,
    no matter how many were run. Verified against a synthetic test mesh
    (an overhanging "mushroom" shape) before trusting it on the real scan.

    IMPORTANT: h/g/slice_dist are per-slice (2D) fields and are only valid
    for the BOOLEAN "filled or not" decision above -- do not repurpose them
    as a continuous 3D field for marching cubes (see the module docstring's
    *** warning *** for why that specific mistake produced a badly broken
    "hairy"/spiky mesh the first time it was tried).
    """
    print(f"Voxelizing at pitch={pitch:.4f} ...")
    arr, transform = voxelize_solid(mesh, pitch)
    print(f"Voxel grid shape: {arr.shape} ({arr.sum()} occupied voxels)")

    step_radius = draft_pct / 100.0  # voxels of growth per axial voxel step

    # The array is sized to the mesh's tight bounding box, with zero
    # clearance in the transverse (non-pull-axis) directions. Draft growth
    # dilates outward in those directions, so without extra headroom it
    # gets silently clipped at the array edge -- most severely wherever the
    # mesh already touches the bounding box there (which is common), making
    # the draft angle appear to do nothing. Pad the transverse axes by the
    # maximum possible growth before sweeping.
    n_axis = arr.shape[axis]
    max_growth = int(np.ceil((n_axis - 1) * step_radius)) if step_radius > 0 else 0
    if max_growth > 0:
        pad = max_growth + 2
        pad_width = [(0, 0)] * 3
        for a in range(3):
            if a != axis:
                pad_width[a] = (pad, pad)
        arr = np.pad(arr, pad_width, mode="constant", constant_values=False)
        # shift the transform so padded voxel-index space still maps to
        # the correct world coordinates
        for a in range(3):
            if pad_width[a][0] > 0:
                transform[:3, 3] -= pad_width[a][0] * transform[:3, a]
        print(f"Padded transverse axes by {pad} voxels to give the "
              f"{draft_pct:.1f}% draft room to grow.")

    # Move the pull axis to the front so we can work slice-by-slice.
    arr_m = np.moveaxis(arr, axis, 0)
    n = arr_m.shape[0]

    if step_radius <= 0:
        # Plain undercut removal: fill each column solid from the base end
        # up to its topmost (or bottommost) occupied voxel.
        idx = np.arange(n).reshape(n, 1, 1)
        if base == "min":
            masked_idx = np.where(arr_m, idx, -1)
            top_idx = masked_idx.max(axis=0, keepdims=True)
            fill_mask = (idx <= top_idx) & (top_idx >= 0)
        else:
            masked_idx = np.where(arr_m, idx, n)
            bottom_idx = masked_idx.min(axis=0, keepdims=True)
            fill_mask = (idx >= bottom_idx) & (bottom_idx < n)
        new_arr_m = arr_m | fill_mask
    else:
        # Draft angle: closed-form g/h suffix-min solve. See this
        # function's docstring ("The draft-angle math") for the full
        # derivation -- summary: g(i') = slice_dist[i'] - d(i')*step_radius,
        # h(i) = running min of g from the tip down to i, and voxel
        # (i,y,z) is filled iff h(i,y,z) <= -d(i)*step_radius.
        d = np.arange(n) if base == "min" else np.arange(n)[::-1]
        print("Computing per-slice distance transforms for draft angle ...")
        slice_dist = np.empty(arr_m.shape, dtype=np.float32)
        for i in range(n):
            slice_dist[i] = ndimage.distance_transform_edt(~arr_m[i])
        d_r = (d.astype(np.float32) * step_radius)[:, None, None]
        g = slice_dist - d_r
        if base == "min":
            h = np.minimum.accumulate(g[::-1], axis=0)[::-1]
        else:
            h = np.minimum.accumulate(g, axis=0)
        new_arr_m = h <= -d_r

    new_arr = np.moveaxis(new_arr_m, 0, axis)
    added = new_arr.sum() - arr.sum()
    axis_name = ['x', 'y', 'z'][axis]
    if draft_pct > 0:
        print(f"Filled {added} voxels ({added / max(arr.sum(),1):.1%} volume added) "
              f"to eliminate undercuts along {axis_name} (base={base}) "
              f"with a {draft_pct:.1f}% draft angle.")
    else:
        print(f"Filled {added} voxels ({added / max(arr.sum(),1):.1%} volume added) "
              f"to eliminate undercuts along {axis_name} "
              f"(base={base}).")

    # Surface a proper full-3D signed distance field (consistent across all
    # three axes, unlike a per-slice distance stack) rather than the raw
    # boolean, so marching cubes interpolates the true sub-voxel crossing
    # point everywhere -- this is what removes staircasing on shallow
    # slopes like the draft cone without any risk of the axial
    # discontinuities a naive per-slice field would introduce.
    print("Computing signed distance field for smooth re-surfacing ...")
    sdf = (ndimage.distance_transform_edt(new_arr)
           - ndimage.distance_transform_edt(~new_arr)).astype(np.float32)

    if blur_sigma > 0:
        # The draft fill is exact, and where two separate undercut features
        # (e.g. neighbouring teeth) each cast their own conical fill, the
        # envelope of those cones meets at a real crease -- not aliasing, and
        # not something more resolution or mesh smoothing removes (Taubin
        # fights a genuine sharp edge instead of noise). Blur the SDF to
        # round those creases, but confine the blur to the newly-added
        # material with a feathered falloff, so the original scanned surface
        # (teeth included) stays untouched and sharp.
        print(f"Rounding draft-cone crease lines (gaussian sigma={blur_sigma:.1f} "
              f"voxels, confined to added material) ...")
        added = new_arr & ~arr
        margin = max(int(np.ceil(blur_sigma * 3)), 1)
        smooth_zone = ndimage.binary_dilation(added, iterations=margin)
        blurred = ndimage.gaussian_filter(sdf, sigma=blur_sigma)
        weight = ndimage.distance_transform_edt(smooth_zone).astype(np.float32)
        weight = np.clip(weight / margin, 0.0, 1.0)
        sdf = weight * blurred + (1.0 - weight) * sdf

    return field_to_mesh(sdf, transform, level=0.0, pad_value=float(sdf.min()) - 1.0)


def shell_correct(mesh: trimesh.Trimesh, axis: int, base: str, pitch: float,
                   thickness: float, blur_sigma: float = 0.0,
                   teeth_blur_sigma: float = 0.0, teeth_radius: int = 5) -> trimesh.Trimesh:
    """
    Hollow `mesh` into a constant-thickness shell (measured as true nearest
    -surface distance, not a percentage scale), open at the `base` end of
    `axis` so the result is bowl-shaped rather than a fully sealed cavity.
    See the module docstring's "shell command" section for the full
    picture and the reasoning for why the parting-plane face gets special
    padding treatment below.

    IMPORTANT: shelling isn't just a smoothness-preserving copy of the
    input surface moved inward -- a constant-distance inward offset is a
    morphological erosion, and erosion mathematically SHARPENS concave
    creases (while it softens/rounds convex ones). If the input mesh had a
    concave crease smoothed out with draft_correct's --blur (e.g. where
    two neighboring teeth's draft cones met), shelling it can partially
    re-sharpen exactly that crease -- independent of how smooth the input
    mesh was, since it's the offset operation itself doing this, not a
    resolution/aliasing artifact.

    `blur_sigma`/`teeth_blur_sigma` are two DIFFERENT strength blurs for
    two DIFFERENT kinds of feature, split apart because they want opposite
    treatment: concave creases (the draft-cone seams above) need rounding
    for good mold release and aren't fine anatomical detail worth keeping
    crisp, whereas convex, thin protrusions (teeth) are worth keeping
    distinct even though a little rounding also helps THEM release from
    the plaster -- so they get their own, typically much gentler, sigma
    rather than sharing one setting with the creases. (draft_correct's
    --blur doesn't need this split: it's already confined to the newly
    -added draft material, which is where creases live, and doesn't touch
    original scanned geometry like teeth at all. shell_correct has no such
    "added vs. original" region -- the whole shell comes from one uniform
    offset -- so it needs its own way to tell the two apart.)

    The split is done morphologically, not by curvature estimation (which
    would be more fragile): a "thin convex protrusion" is, by definition,
    solid material that a big-enough morphological OPENING (erode then
    dilate by `teeth_radius`) erases -- opening can't preserve anything
    narrower than about 2*teeth_radius, so what it erases is exactly the
    thin spikes/cusps (teeth), while broad concave creases are untouched
    by it (there's no "thin" material there to erase). That erased region,
    grown outward by `teeth_radius` more voxels to feather the transition
    (so there's no hard seam at the boundary, same feathering approach as
    draft_correct's own masked blur), is where `teeth_blur_sigma` applies;
    everywhere else gets `blur_sigma`.

    Like draft_correct, the final mask is surfaced via a full-3D signed
    distance field (level=0.0) rather than the raw boolean (level=0.5), so
    marching cubes can interpolate the true sub-voxel wall position instead
    of snapping to the voxel grid -- same staircase-removal trick, same
    reason (see field_to_mesh's docstring).

    Same pad_value choice as draft_correct (very negative, i.e. "more
    outside than anything real in the field") and for the same underlying
    reason, but it matters more here: field_to_mesh pads all six sides of
    the array with one constant value, and the whole point of the base-
    face padding trick above was to leave an OPEN RIM at that edge of the
    array (the bowl's mouth) rather than a capped wall. Since "positive"
    means inside/solid and "negative" means outside/empty here (see
    field_to_mesh's docstring), padding with a very positive ("very
    inside") value would fabricate a false membrane sealing the whole
    mouth shut -- exactly the opposite of what --base is for. Padding with
    a very negative ("very outside/empty") value instead means: real walls
    that happen to reach the array edge still get capped correctly (an
    edge value deep in solid material is strongly positive, so it still
    crosses zero against an even-more-negative pad), while the open
    rim -- already close to zero/empty right at that edge, since nothing
    forced it solid -- stays open, because empty-to-more-empty never
    crosses zero.
    """
    print(f"Voxelizing at pitch={pitch:.4f} ...")
    arr, transform = voxelize_solid(mesh, pitch)
    print(f"Voxel grid shape: {arr.shape} ({arr.sum()} occupied voxels)")

    # Distance transform below needs `thickness` worth of headroom around
    # the whole grid (plus a couple voxels of margin) or the shell would
    # get clipped at the array edge, same issue as the transverse padding
    # in draft_correct.
    pad = int(np.ceil(thickness / pitch)) + 2
    pad_width = [(pad, pad)] * 3
    const_vals = [(False, False)] * 3
    # Treat the base (parting-plane / flat cut) face as an open mouth, not
    # a wall to offset from: pad it with solid (True) instead of empty so
    # the distance transform never treats it as nearby exterior -- a point
    # near that face measures its distance to the *interior* padding, not
    # to a phantom wall, so no shell material gets added there and the
    # result stays open like a bowl. Every other face -- the true
    # anatomical surface, including the tip -- is padded with empty
    # (False) and gets a normal offset wall.
    if base == "min":
        const_vals[axis] = (True, False)
    else:
        const_vals[axis] = (False, True)

    padded_arr = np.pad(arr, pad_width=pad_width, mode="constant",
                         constant_values=const_vals)

    print(f"Computing distance transform for {thickness:.2f}mm shell ...")
    # For every solid voxel, distance to the nearest empty (exterior)
    # voxel -- keep only the ones within `thickness` of that exterior,
    # i.e. a constant-thickness rind just inside the original surface.
    dist = ndimage.distance_transform_edt(padded_arr) * pitch
    shell_padded = padded_arr & (dist < thickness)

    # Undo the padding to get back to the original (unpadded) grid shape.
    crop = tuple(slice(pad, pad + s) for s in arr.shape)
    shell_mask = shell_padded[crop]

    kept = shell_mask.sum()
    print(f"Kept {kept} of {arr.sum()} voxels ({kept / max(arr.sum(),1):.1%}) "
          f"as a {thickness:.2f}mm shell, open at the {['x','y','z'][axis]} "
          f"{base} face.")

    print("Computing signed distance field for smooth re-surfacing ...")
    sdf = (ndimage.distance_transform_edt(shell_mask)
           - ndimage.distance_transform_edt(~shell_mask)).astype(np.float32)

    if blur_sigma > 0 or teeth_blur_sigma > 0:
        # Split into "thin convex protrusion" (teeth) vs. everything else
        # (creases, broad anatomy) via morphological opening -- see this
        # function's docstring for the reasoning. An opening can't preserve
        # anything narrower than ~2*teeth_radius voxels, so what it erases
        # is exactly the thin spikes.
        print(f"Splitting shell into teeth (radius<{teeth_radius} vox) vs. "
              f"crease/broad regions for differential blur "
              f"(blur={blur_sigma:.1f}, teeth-blur={teeth_blur_sigma:.1f}) ...")
        opened = ndimage.binary_opening(
            shell_mask, structure=np.ones((3, 3, 3)), iterations=teeth_radius)
        protrusion = shell_mask & ~opened
        margin = max(teeth_radius, 1)
        teeth_zone = ndimage.binary_dilation(protrusion, iterations=margin)
        # feathered 0..1 weight: 1 deep inside a tooth, fading to 0 at its
        # edge (and 0 everywhere outside teeth_zone) -- same feathering
        # pattern as draft_correct's masked blur, just protecting a
        # different region.
        weight_teeth = ndimage.distance_transform_edt(teeth_zone).astype(np.float32)
        weight_teeth = np.clip(weight_teeth / margin, 0.0, 1.0)

        crease_sdf = ndimage.gaussian_filter(sdf, sigma=blur_sigma) if blur_sigma > 0 else sdf
        teeth_sdf = ndimage.gaussian_filter(sdf, sigma=teeth_blur_sigma) if teeth_blur_sigma > 0 else sdf
        sdf = weight_teeth * teeth_sdf + (1.0 - weight_teeth) * crease_sdf

    # very-negative ("very outside") pad -- see docstring for why this
    # sign, specifically, is required here and not just a style choice.
    return field_to_mesh(sdf, transform, level=0.0, pad_value=float(sdf.min()) - 1.0)


def core_correct(mesh: trimesh.Trimesh, axis: int, base: str, pitch: float,
                  inset: float, blur_sigma: float = 0.0) -> trimesh.Trimesh:
    """
    Solid inward offset: erode `mesh` by `inset` (true nearest-surface
    distance) and keep ALL of what's left, still open/flush at the `base`
    end of `axis`. Use case: a plug that presses a clay sheet of thickness
    `inset` into a plaster mold cast from `mesh`'s outer surface.

    Same base-face padding trick as shell_correct (pad the parting face
    as solid so the distance transform doesn't treat it as a wall), so
    the core stays full-height right down to the parting plane instead of
    shrinking away from it. Features thinner than 2*inset (teeth tips,
    thin ridges) vanish entirely -- expected for a clay-pressing plug.
    """
    print(f"Voxelizing at pitch={pitch:.4f} ...")
    arr, transform = voxelize_solid(mesh, pitch)
    print(f"Voxel grid shape: {arr.shape} ({arr.sum()} occupied voxels)")

    pad = int(np.ceil(inset / pitch)) + 2
    const_vals = [(False, False)] * 3
    if base == "min":
        const_vals[axis] = (True, False)
    else:
        const_vals[axis] = (False, True)
    padded = np.pad(arr, [(pad, pad)] * 3, mode="constant",
                     constant_values=const_vals)

    print(f"Eroding by {inset:.2f}mm ...")
    dist = ndimage.distance_transform_edt(padded) * pitch
    core_mask = (padded & (dist >= inset))[
        tuple(slice(pad, pad + s) for s in arr.shape)]
    print(f"Kept {core_mask.sum()} of {arr.sum()} voxels "
          f"({core_mask.sum() / max(arr.sum(), 1):.1%}).")

    sdf = (ndimage.distance_transform_edt(core_mask)
           - ndimage.distance_transform_edt(~core_mask)).astype(np.float32)
    if blur_sigma > 0:
        sdf = ndimage.gaussian_filter(sdf, sigma=blur_sigma)
    return field_to_mesh(sdf, transform, level=0.0, pad_value=float(sdf.min()) - 1.0)


def negative_correct(mesh: trimesh.Trimesh, axis: int, base: str, pitch: float,
                      margin: float) -> trimesh.Trimesh:
    """
    Carve `mesh` (an already draft-corrected, undercut-free solid) OUT of a
    rectangular block, producing a mold cavity instead of a positive -- see
    the module docstring's "negative command" section for the full picture.

    Args:
      axis    0/1/2 for x/y/z -- same pull axis as the `draft` run that
              produced `mesh`. Must match: this determines which block face
              stays flush (the cavity's pour opening) vs. which get padded
              (the mold's solid walls).
      base    'min' or 'max' -- same as the `draft` run; identifies which
              end of `axis` is the parting-plane face.
      margin  wall thickness / clearance, in the mesh's own units, added
              around the solid on every side of the block EXCEPT the base
              face (which stays flush with the mesh's own parting plane --
              see below for why).

    Unlike shell_correct, there's no distance-transform offset here and no
    special-cased "treat the base face as open" padding: the block is built
    by padding `margin` worth of solid on every side of the mesh's voxel
    grid EXCEPT the base end of `axis`, which is left at zero padding, flush
    with the mesh's own base layer. Since the mesh's base layer is already
    exactly the object's flat parting-plane footprint (solid where the
    object is, empty where it isn't), `block & ~mesh` at that one layer is
    empty precisely where the object's footprint is and solid everywhere
    else in the block's cross-section there -- i.e. a skull-shaped hole
    through the block's top face, open by construction, with no need to
    tell the boundary-padding step in field_to_mesh not to cap it (empty
    bordered by more empty during that padding caps nothing). Every other
    face of the block -- the two transverse sides and the far (tip) end of
    the pull axis -- IS padded with real margin, so those get capped into
    genuine solid mold walls the normal way.
    """
    print(f"Voxelizing at pitch={pitch:.4f} ...")
    arr, transform = voxelize_solid(mesh, pitch)
    print(f"Voxel grid shape: {arr.shape} ({arr.sum()} occupied voxels)")

    margin_vox = max(int(np.ceil(margin / pitch)), 1)
    pad_width = [(margin_vox, margin_vox)] * 3
    # Leave the base (parting-plane) end of the pull axis flush/unpadded --
    # that's the mold's pour opening, not a wall -- while every other face
    # gets `margin` worth of solid wall around the mesh.
    if base == "min":
        pad_width[axis] = (0, margin_vox)
    else:
        pad_width[axis] = (margin_vox, 0)

    mesh_padded = np.pad(arr, pad_width, mode="constant", constant_values=False)
    block = np.ones_like(mesh_padded)
    negative = block & ~mesh_padded

    for a in range(3):
        if pad_width[a][0] > 0:
            transform[:3, 3] -= pad_width[a][0] * transform[:3, a]

    print(f"Block is {negative.size} voxels; carved out {mesh_padded.sum()} as "
          f"the cavity, leaving {negative.sum()} solid "
          f"({negative.sum() / negative.size:.1%}) as the mold body, "
          f"{margin:.2f}mm wall margin, open at the {['x','y','z'][axis]} "
          f"{base} face.")

    print("Computing signed distance field for smooth re-surfacing ...")
    sdf = (ndimage.distance_transform_edt(negative)
           - ndimage.distance_transform_edt(~negative)).astype(np.float32)

    return field_to_mesh(sdf, transform, level=0.0, pad_value=float(sdf.min()) - 1.0)


def _add_shared_args(sp):
    """
    Args common to both 'draft' and 'shell' subcommands. Factored out so
    the help text can't drift out of sync between the two -- if you're
    tempted to tweak wording, do it here once rather than in two places.
    """
    sp.add_argument("input", help="Path to the input mesh (e.g. an STL).")
    sp.add_argument("output", help="Path to write the resulting mesh to "
                     "(format inferred from the extension, e.g. .stl).")
    sp.add_argument("--pull-axis", choices=["x", "y", "z"], default="z",
                     help="The axis the mold/plaster pulls apart along -- "
                          "i.e. the direction from the open parting-plane "
                          "face toward the far tip of the object. Get this "
                          "wrong and material gets added/removed in a "
                          "direction that doesn't correspond to how the "
                          "mold actually comes apart. Default: z.")
    sp.add_argument("--base", choices=["min", "max"], default="min",
                     help="Which end of --pull-axis is the open parting-"
                          "plane face (e.g. the flat cut face of a "
                          "hemisected scan). 'min' = that face is at the "
                          "low-coordinate end of the axis and the object "
                          "extends toward +axis from there; 'max' is the "
                          "mirror image. Check the mesh's bounding box if "
                          "unsure which end is which. Default: min.")
    sp.add_argument("--pitch", type=float, default=None,
                     help="Voxel edge length, in the mesh's own units (mm "
                          "for a typical STL). Smaller = finer surface "
                          "detail and less staircasing, but more time and "
                          "memory -- roughly cubic in 1/pitch. If omitted, "
                          "auto-picked as (bounding box diagonal) / 250, "
                          "which is a coarse default suitable for a first "
                          "look, not a final print.")
    sp.add_argument("--smooth", type=int, default=8,
                     help="Number of post-processing smoothing iterations "
                          "to run on the final mesh, softening whatever "
                          "voxel-resolution roughness marching cubes left "
                          "behind. 0 disables smoothing entirely. Default: "
                          "8.")
    sp.add_argument("--smooth-method", choices=["laplacian", "taubin"],
                     default="laplacian",
                     help="'laplacian' is the simple/classic smoothing "
                          "filter but visibly shrinks the mesh if you push "
                          "--smooth high, eating into draft clearance, "
                          "shell wall thickness, and fine detail. 'taubin' "
                          "is slower per-iteration but preserves volume, "
                          "so prefer it whenever --smooth is more than "
                          "single digits. Default: laplacian (matches this "
                          "script's original/simplest behavior; switch to "
                          "taubin deliberately once you're pushing "
                          "iteration counts up).")


def build_parser():
    p = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = p.add_subparsers(dest="command", required=True)

    pd = sub.add_parser("draft", help="Add material to eliminate undercuts "
                         "along a pull axis, with optional draft angle.")
    _add_shared_args(pd)
    pd.add_argument("--draft", type=float, default=0.0,
                     help="Draft angle as a percentage grade (rise/run * "
                          "100, i.e. tan(angle)*100 -- e.g. 5 means about "
                          "2.9 degrees per side, tan(angle)=0.05). 0 (the "
                          "default) is a straight, 0-degree pull with no "
                          "taper -- just the minimum undercut-eliminating "
                          "fill. A nonzero value makes that fill cone-"
                          "widen as it moves from the tip back toward the "
                          "base, giving the print clearance in the mold "
                          "instead of an exact knife-edge fit.")
    pd.add_argument("--scale", type=float, default=1.0,
                     help="Uniformly scale the input mesh by this factor "
                          "BEFORE voxelizing, e.g. 0.5 for a half-size test "
                          "print. Scales about the origin, so a parting "
                          "plane at x=0 stays at x=0 (mirror's default "
                          "--plane keeps working). --pitch and everything "
                          "downstream (shell --thickness, etc.) are in the "
                          "scaled units, so to get an identical-looking "
                          "result at a smaller size, scale --pitch by the "
                          "same factor (voxel-denominated flags like --blur "
                          "then behave the same relative to the features). "
                          "Draft is a percentage grade, so it is scale-"
                          "invariant. Run shell on this command's output "
                          "with no scale of its own. Default: 1.0.")
    pd.add_argument("--blur", type=float, default=0.0,
                     help="Gaussian sigma, in voxels, used to round off "
                          "sharp crease lines that form where two nearby "
                          "undercut features' individual draft cones (e.g. "
                          "neighboring teeth) meet each other. This is "
                          "REAL geometry, not a resolution artifact, so "
                          "plain --smooth mostly fights it rather than "
                          "removing it. The blur is confined to the newly"
                          "-added draft material only (feathered at the "
                          "edge), so the original scanned surface -- "
                          "teeth included -- stays untouched and sharp no "
                          "matter how high this is set. 0 = off (default). "
                          "Try 3-6 as a starting point; there's no strict "
                          "upper bound, higher just rounds the added "
                          "material more.")

    ps = sub.add_parser("shell", help="Hollow a mesh into a constant-"
                         "thickness shell, open at the parting-plane face.")
    _add_shared_args(ps)
    ps.add_argument("--thickness", type=float, default=2.0,
                     help="Target shell wall thickness, in the mesh's own "
                          "units (mm for a typical STL), measured as true "
                          "nearest-surface distance (not a percentage "
                          "scale-and-subtract, which would give uneven "
                          "wall thickness on an irregular/anatomical "
                          "shape). Default: 2.0.")
    ps.add_argument("--blur", type=float, default=0.0,
                     help="Gaussian sigma, in voxels, softening concave "
                          "creases and broad anatomy on the shell surface "
                          "-- mainly useful because a constant-distance "
                          "inward offset (what shelling is) mathematically "
                          "SHARPENS concave creases (e.g. the crease left "
                          "where two neighboring draft cones met, even if "
                          "--blur already rounded it on the drafted input "
                          "mesh) while it softens convex ones. Does NOT "
                          "apply to thin convex protrusions (teeth) -- "
                          "those get --teeth-blur instead, so the two can "
                          "be tuned independently. 0 = off (default).")
    ps.add_argument("--teeth-blur", type=float, default=0.0,
                     help="Separate, usually gentler, Gaussian sigma (in "
                          "voxels) applied ONLY to thin convex protrusions "
                          "(teeth) rather than --blur's strength, since "
                          "creases (which need real rounding for mold "
                          "release) and teeth (which you may want to keep "
                          "recognizable, or only round a little for their "
                          "own release from the plaster) usually don't "
                          "want the same amount. 'Thin' is defined by "
                          "--teeth-radius. 0 = off, teeth stay exactly as "
                          "sharp as the input mesh (default).")
    ps.add_argument("--teeth-radius", type=int, default=5,
                     help="Voxel radius used to decide what counts as a "
                          "'thin convex protrusion' for --teeth-blur: "
                          "material narrower than about 2x this radius "
                          "gets treated as a tooth; anything broader "
                          "(creases, general anatomy) is left to --blur "
                          "instead. Bump this up if real teeth are being "
                          "classified as broad anatomy (getting --blur's "
                          "strength) or down if some non-tooth thin "
                          "feature is wrongly getting --teeth-blur's. "
                          "Default: 5.")

    pc = sub.add_parser("core", help="Erode a solid inward by a fixed "
                         "distance (a plug for pressing clay into a mold "
                         "cast from the input's surface), flush at the "
                         "parting-plane face.")
    _add_shared_args(pc)
    pc.add_argument("--inset", type=float, default=5.0,
                     help="Inward offset in mm (= clay thickness). Default 5.")
    pc.add_argument("--blur", type=float, default=0.0,
                     help="Gaussian sigma (voxels) to round creases that "
                          "erosion sharpens. 0 = off.")

    pn = sub.add_parser("negative", help="Carve a draft-corrected solid out "
                         "of a block, producing a printable mold cavity "
                         "instead of a positive.")
    _add_shared_args(pn)
    pn.add_argument("--margin", type=float, default=8.0,
                     help="Wall thickness / clearance, in the mesh's own "
                          "units (mm for a typical STL), added around the "
                          "solid on every side of the block EXCEPT the base "
                          "(parting-plane) face, which stays flush with the "
                          "mesh's own base -- that face is the mold's pour "
                          "opening, not a wall. This is a mold body meant "
                          "to hold its shape under a plaster/resin pour, "
                          "not a thin release shell, so it wants a much "
                          "thicker margin than --shell's wall thickness. "
                          "Default: 8.0.")

    pm = sub.add_parser("mirror", help="Reflect a mesh across a plane -- "
                         "e.g. turn a finished left-side half into a "
                         "right-side counterpart.")
    pm.add_argument("input", help="Path to the input mesh (e.g. an STL).")
    pm.add_argument("output", help="Path to write the mirrored mesh to "
                     "(format inferred from the extension, e.g. .stl).")
    pm.add_argument("--axis", choices=["x", "y", "z"], default="x",
                     help="Axis perpendicular to the mirror plane -- i.e. "
                          "reflecting flips coordinates along this axis "
                          "and leaves the other two untouched. For this "
                          "project's convention (parting-plane/centerline "
                          "at x=0), that's x. Default: x.")
    pm.add_argument("--plane", type=float, default=0.0,
                     help="Coordinate along --axis where the mirror plane "
                          "sits (e.g. 0.0 for a centerline at x=0). "
                          "Default: 0.0.")

    return p


def main():
    args = build_parser().parse_args()

    # force="mesh" merges any multi-body/scene STL into one Trimesh; a raw
    # scan is usually already one body, but this is cheap insurance.
    mesh = trimesh.load(args.input, force="mesh")

    if args.command == "mirror":
        # No voxelizing/re-surfacing/smoothing involved -- see mirror_mesh
        # and the module docstring's "mirror command" section for why. In
        # particular, skip the watertight check below: it exists to warn
        # about voxelize_solid's requirements, which mirror never uses, and
        # a shell_correct output is EXPECTED to be non-watertight (it's an
        # intentionally open bowl) so the warning would just be noise here.
        result = mirror_mesh(mesh, AXES[args.axis], args.plane)
        result.export(args.output)
        print(f"Wrote {args.output}  ({len(result.vertices)} verts, "
              f"{len(result.faces)} faces)")
        return

    if not mesh.is_watertight:
        # voxelize_solid's ray-parity fill (draft/shell/negative) and the
        # boolean mesh engine (brim) both require a watertight/manifold
        # mesh -- a leaky mesh can produce missing chunks, extra solid
        # material, or a failed/garbage boolean, with no error either way.
        print("WARNING: input mesh is not watertight -- this command may "
              "produce imperfect or garbage results. Consider running an "
              "STL repair pass first.", file=sys.stderr)

    if args.command == "draft" and args.scale != 1.0:
        mesh.apply_scale(args.scale)
        print(f"Scaled input by {args.scale:g} about the origin; new extents "
              f"{np.round(mesh.extents, 2).tolist()} mm")

    if args.pitch is None:
        diag = np.linalg.norm(mesh.bounding_box.extents)
        args.pitch = diag / 250.0
        print(f"No --pitch given, auto-selected pitch={args.pitch:.4f}")

    axis = AXES[args.pull_axis]

    if args.command == "draft":
        result = draft_correct(mesh, axis, args.base, args.pitch, args.draft,
                                args.blur)
    elif args.command == "shell":
        result = shell_correct(mesh, axis, args.base, args.pitch, args.thickness,
                                args.blur, args.teeth_blur, args.teeth_radius)
    elif args.command == "core":
        result = core_correct(mesh, axis, args.base, args.pitch, args.inset,
                               args.blur)
    else:
        result = negative_correct(mesh, axis, args.base, args.pitch, args.margin)

    smooth_mesh(result, args.smooth, args.smooth_method)

    result.export(args.output)
    print(f"Wrote {args.output}  ({len(result.vertices)} verts, "
          f"{len(result.faces)} faces)")


if __name__ == "__main__":
    main()
