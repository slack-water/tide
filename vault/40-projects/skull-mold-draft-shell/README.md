---
title: Skull Mold Draft & Shell Pipeline
created: 2026-07-29
updated: 2026-07-29
folder: 40
type: project
status: active
importance: 3
goal: Turn a hemisected skull scan into a pair of draft-corrected, shelled, mold-ready STLs (left + mirrored right)
scope: mesh-processing script + finished output files, not the physical casting process
tags: [3d-printing, mold-making, mesh-processing, python, cad]
related: []
schema-version: 1.0
ai-assisted: true
---

## Goal

Prepare a scanned half-skull STL (cut flush at the sagittal midline) so it can be pressed into wet plaster as a mold master and pulled back out cleanly, then produce a mirrored counterpart so both left and right sides exist.

## Scope

**In:** a reusable voxel-based Python script (`stl_add_draft.py`, copied into this folder) with three operations — `draft` (eliminate undercuts + optional draft angle), `shell` (hollow to a constant wall thickness, open at the parting plane), `mirror` (reflect a finished half across the centerline).
**Out:** the actual plaster pour / print / release process; a silicone-intermediate route (print → silicone → plaster) if direct plaster release turns out to lose too much tooth detail — noted as a fallback, not pursued yet.

## Done looks like

Two print-ready STLs, left and right, each: draft-corrected (5% grade) so the print releases from a plaster mold without undercutting, hollowed to a 1.2mm wall (open at the centerline face so it can be packed with frozen isopropyl alcohol to help shrink/release), with creases smoothed enough to release cleanly but teeth still distinct enough to hand-finish. Verified (not just visually) via ray-casting and volume checks, not just "looked right."

Current final outputs (not checked into this vault — see Files below):

- `Skull (Left)_shell1.2mm_blur3_teeth1.stl`
- `Skull (Right)_shell1.2mm_blur3_teeth1.stl` (mirror of the above)

## Next action

- [ ] Print both halves (0.2mm nozzle, per plan, to minimize layer lines)
- [ ] Press into wet plaster to make the mother mold; test release
- [ ] If release is tight, pack the shell interior with frozen isopropyl alcohol before pulling
- [ ] (stretch) if plaster-direct loses too much tooth definition, try print → silicone → plaster instead for a higher-fidelity intermediate

---

## Files

- `stl_add_draft.py` — the finished script, copied here as of 2026-07-29 (a working copy and a `stl_add_draft_v1.py` backup exist alongside the STL files elsewhere on disk). The STL inputs/outputs themselves (tens to hundreds of MB each) are intentionally not copied into this git-tracked vault.
- Original scan: `Skull (Left).stl` — 306,829 verts, watertight, medial-lateral axis is X, flat cut/parting face at x≈0, ear/lateral side at x≈39mm.

## Final recipe (the commands that produced the accepted output)

```bash
# 1. Draft-correct: eliminate undercuts along X (base=min, i.e. the flat cut
#    face), 5% draft angle, crease-rounding blur confined to added material,
#    heavy Taubin smoothing since it doesn't shrink the mesh.
python stl_add_draft.py draft "Skull (Left).stl" "Skull (Left)_draft5pct_p0.15_blur6.stl" \
    --pull-axis x --base min --pitch 0.15 --draft 5 --blur 6 \
    --smooth 20 --smooth-method taubin

# 2. Shell: hollow to 1.2mm wall, open at the same base face, with SEPARATE
#    blur strengths for creases (strong) vs. teeth (gentle) -- see "Shelling
#    sharpens creases" below for why these need to differ.
python stl_add_draft.py shell "Skull (Left)_draft5pct_p0.15_blur6.stl" "Skull (Left)_shell1.2mm_blur3_teeth1.stl" \
    --pull-axis x --base min --pitch 0.15 --thickness 1.2 \
    --blur 3 --teeth-blur 1 --teeth-radius 5 \
    --smooth 20 --smooth-method taubin

# 3. Mirror: reflect across the centerline (x=0) to get the right side.
python stl_add_draft.py mirror "Skull (Left)_shell1.2mm_blur3_teeth1.stl" "Skull (Right)_shell1.2mm_blur3_teeth1.stl" \
    --axis x --plane 0.0
```

Each run took roughly 1–1.5 minutes (`draft`/`shell` at pitch 0.15 on a ~66M-voxel grid) or ~10 seconds (`mirror`, pure mesh reflection, no voxelizing).

---

## How the pipeline works (short version)

Voxelize the mesh (turn it into a 3D grid of filled/empty cells), do the geometric operation with array math (trivial to express correctly at the grid level), then re-extract a surface mesh via marching cubes. The tradeoff: need fine enough `--pitch` to avoid voxel staircasing, and care in how the grid becomes a mesh again to avoid re-introducing exactly that staircasing.

**draft**: fill each column along the pull axis solid from the parting plane up to its topmost occupied voxel (removes undercuts by definition — nothing above the highest point in a filled column can still be an undercut). Optionally cone-widen that fill as it sweeps from tip back to base (the draft angle), solved as one closed-form pass, not an iterative grow-loop.

**shell**: full-3D Euclidean distance transform, keep only voxels within `--thickness` of the true surface. The parting-plane face is padded as already-solid (not empty) before the transform runs, so it's treated as an open mouth rather than a wall to offset from — this is what leaves the result open/bowl-shaped instead of a sealed cavity.

**mirror**: pure vertex reflection across a plane, with face winding reversed to undo the orientation flip a reflection otherwise causes (left uncorrected, the output would be geometrically right but "inside-out" from a solid-modeling point of view).

Full algorithmic detail, including the derivation of the draft-angle math, lives in the script's own docstrings — it was deliberately written to be self-explanatory returning to cold in 6 months, so that's the source of truth, not this note.

---

## Lessons learned this session (the parts worth remembering)

**Wrong pull axis on the first attempt.** Started with Z (top of head) by assumption; the actual medial-lateral pull axis was X, found by checking which face's vertices clustered at a bounding-box extreme (the flat cut face at x≈0). Always verify the axis geometrically before trusting an assumption about which way a hemisected scan "should" pull.

**Iterative sub-voxel growth is a silent no-op.** First attempt at the draft angle tried "grow the fill mask by a bit each step, repeat." `distance_transform_edt` only resolves whole-pixel distances, so thresholding at a sub-1-voxel radius against a freshly recomputed mask every iteration accumulates literally nothing, no matter how many iterations run — and it fails silently (no error, just no visible effect). Fixed by solving the whole draft-cone fill in one closed-form pass (a per-slice 2D distance transform, combined via a running suffix-min across the axial direction) instead of iterating.

**Default voxelization doesn't scale to messy real scans.** trimesh's built-in `mesh.voxelized(pitch).fill()` subdivides triangles until each is smaller than one voxel — fine for clean CAD meshes, but for a 300k-vertex raw scan at fine pitch it blows up in time/memory before finishing. Fix: a custom ray-scanline solid voxelizer (one Z-ray per grid column, fill between paired entry/exit crossings) that scales with grid resolution and mesh complexity via the ray-BVH, not subdivided-triangle count. Went from OOM/multi-minute hangs to ~13s at pitch 0.15, ~60s at pitch 0.1.

**The "hairy mesh" bug — the one mistake worth remembering hardest.** To remove voxel staircasing on the shallow draft-cone slope, tried feeding marching cubes a continuous field built from the same per-slice (2D) distance values used to compute the draft fill. Result: a mesh that was recognizably the right shape but covered in spikes ("like it's made of hairs standing on end"). Root cause: those per-slice fields are only smooth *within* their own 2D slice — there's no relationship between one slice's values and its neighbor's, since each is computed independently. Feeding that stack to marching cubes (which linearly interpolates between axially-adjacent grid points, assuming they're samples of one continuous field) produced chaotic, unrelated crossings. **The fix, and the general lesson: commit to a hard boolean fill/no-fill decision first (booleans don't care whether the field that produced them was continuous), then compute ONE proper full-3D signed distance transform on that final result, and surface *that*.** Never repurpose an algorithm's internal per-slice/2D working fields as if they were a valid continuous 3D field for isosurface extraction.

**Real creases vs. aliasing.** After the SDF fix, ~10-13 distinct facets remained on the drafted surface at regular intervals. These are genuine geometry, not aliasing: neighboring undercut features (teeth) each cast their own draft cone, and where two cones' fill regions meet there's a real crease in the envelope surface. More resolution sharpens this pattern, it doesn't remove it — and plain mesh smoothing (Taubin/Laplacian) fights a real edge rather than noise, so it either does nothing or has to run so many iterations it erodes real detail elsewhere. Fix: blur the signed distance field directly (before surfacing) with a Gaussian, confined *only* to newly-added draft material via a feathered mask, so the original scanned surface (teeth included) never gets touched no matter how strong the blur.

**Shelling re-sharpens exactly the creases you just smoothed.** A constant-distance inward offset (what shelling is) is a morphological erosion, and erosion mathematically sharpens concave features while it softens convex ones. The draft-cone creases are concave, so shelling an already-blurred draft body partially undoes that blur — independent of how smooth the input mesh was. This isn't a bug to "fix" once; it's a property of the offset operation itself, so shelling needs its own blur step, separate from draft's.

**Teeth and creases need opposite treatment, and shell can't reuse draft's masking trick.** draft's blur confines itself to newly-added material (a clean mask, since draft always knows what it added vs. what was original). Shell has no such split — the whole shell comes from one uniform offset of whatever mesh it's given. Splitting "crease/broad anatomy" (needs real rounding, for both mold release and because shelling re-sharpens it) from "thin convex protrusion" (teeth — worth keeping distinct, though a little rounding helps their release too) was done morphologically rather than via curvature estimation (more fragile): a binary opening (erode-then-dilate) by `teeth_radius` voxels can't preserve anything narrower than about 2×that radius, so what it erases is exactly the thin spikes. That region (feathered outward a bit to avoid a hard seam) gets its own gentler blur.

**A subtle sign bug in the shell's "open mouth" fix, and how it was actually caught.** First attempt at applying the same SDF-blur trick to shelling padded the parting-plane boundary with the wrong sign, which fabricated a false floor sealing the bowl shut. `mesh.is_watertight` did NOT catch this — a properly hollow, open-mouthed shell is *supposed* to be a closed 2-manifold (inner + outer wall surfaces meeting at the rim), so watertightness alone can't distinguish "correctly open" from "accidentally capped." The real check: cast a ray through the interior along the pull axis and count crossings near the base — zero crossings there means genuinely open, any crossing means something (possibly just the rim, possibly a fabricated floor) is blocking it. Verified on a small synthetic test mesh before trusting it on the real ~1-minute skull run.

**General takeaway across all of the above:** every one of these bugs was silent — no exception, no error, just a wrong-looking (or wrong-in-a-way-that-doesn't-visually-register) result. Cheap synthetic test meshes (a simple mushroom shape with a known overhang) caught most of them in ~1 second instead of burning a ~1-minute real run per iteration, and geometric verification (ray-casting through a shape, checking volume against expected filled-voxel count, checking bounds after a transform) caught what visual inspection and `is_watertight` alone missed.

## Half-scale test print recipe (2026-09-19)

Same pipeline, `draft --scale 0.5` (new flag; scales about the origin so x=0 stays the parting plane). `--pitch` is in scaled units: 0.075 = 0.15 × 0.5 gives an identical voxel grid, so blur/teeth-radius behave the same relative to features. Shell wall stays an absolute 1.2 mm (≈ 3 loops of 0.42 mm on the A1).

```bash
python stl_add_draft.py draft "Skull (Left).stl" draft50.stl --scale 0.5 \
    --pull-axis x --base min --pitch 0.075 --draft 5 --blur 6 --smooth 20 --smooth-method taubin
python stl_add_draft.py shell draft50.stl "Skull (Left)_50pct_shell1.2mm_blur3_teeth1.stl" \
    --pull-axis x --base min --pitch 0.075 --thickness 1.2 --blur 3 --teeth-blur 1 --teeth-radius 5 \
    --smooth 20 --smooth-method taubin
python stl_add_draft.py mirror "Skull (Left)_50pct_shell1.2mm_blur3_teeth1.stl" "Skull (Right)_50pct_shell1.2mm_blur3_teeth1.stl" --axis x --plane 0
```

Result: 19.6 × 63.1 × 48.1 mm, 5.3 cm³ of plastic (~¼ of full size, since wall thickness is constant). ~1 min per step.

**Print orientation:** flat parting face on the bed (pull axis X = up). Measured on the half-scale shell: outer (cast) surface needs **0 mm²** of support; inner cavity ceiling needs support on ~23% of its 4184 mm² at Bambu's 30° threshold (33% at 45°), mostly a shallow dome 15–18 mm above the bed. So supports only ever touch the interior.

**Bug fixed:** `field_to_mesh` emitted inside-out meshes (negative volume) for every draft/shell output before this date, including the full-size STLs. Slicers auto-repair it, so prints were unaffected, but fixed now (verified on a sphere: −4166 → +4166). Old full-size outputs are still inside-out.

## Log

### 2026-07-29

Built out the full draft → shell → mirror pipeline this session (see Lessons learned above for the technical arc). Landed on a final accepted recipe: 5% draft with blur=6, shell at 1.2mm with blur=3/teeth-blur=1/teeth-radius=5, both at pitch 0.15. Produced and mirrored the final left+right STLs. Script is documented heavily (module + per-function docstrings, full argparse help text) specifically so it's readable cold in 6 months without re-deriving any of this. Next physical step is printing and testing plaster release.
