---
title: Skull Mold Draft & Shell Pipeline
created: 2026-07-29
updated: 2026-10-10
folder: 40
type: project
status: complete
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

**In:** a reusable voxel-based Python script (`stl_add_draft.py`, copied into this folder) with four operations — `draft` (eliminate undercuts + optional draft angle), `shell` (hollow to a constant wall thickness, open at the parting plane), `negative` (carve the drafted solid out of a block, for a directly-printable mold instead of a plaster-press positive), `mirror` (reflect a finished half across the centerline).
**Out:** the actual plaster pour / print / release process; a silicone-intermediate route (print → silicone → plaster) if direct plaster release turns out to lose too much tooth detail — noted as a fallback, not pursued yet. The `negative` route (below) is a third, so-far-untested alternative to both of these.

## Done looks like

Two print-ready STLs, left and right, each: draft-corrected (5% grade) so the print releases from a plaster mold without undercutting, hollowed to a 1.2mm wall (open at the centerline face so it can be packed with frozen isopropyl alcohol to help shrink/release), with creases smoothed enough to release cleanly but teeth still distinct enough to hand-finish. Verified (not just visually) via ray-casting and volume checks, not just "looked right."

Current final outputs (not checked into this vault — see Files below):

- `Skull (Left)_shell1.2mm_blur3_teeth1.stl`
- `Skull (Right)_shell1.2mm_blur3_teeth1.stl` (mirror of the above)

## Next action

- [x] Generate brimmed STLs and print both halves — done at 150% (half-skull press molds) and 60% (whole-skull two-piece mold)
- [x] Press brim-side-down into a cottleboard box, pour the plaster mother mold; test release — release was clean apart from one breakage at the cavity above the jaw bone (see 2026-10-09 log)
- [x] ~~If release is tight, pack the shell interior with frozen isopropyl alcohol before pulling~~ — not needed, release was clean
- [x] ~~(stretch) print → silicone → plaster for higher fidelity~~ — not needed; plaster-direct detail is good enough for ceramic, and glaze will soften it further anyway
- [x] decide: close or continue — closed as complete 2026-10-10; any skull-vessel work (designed rim, pour opening) goes in a new project
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

**negative**: the inverse of `shell` — instead of hollowing the drafted solid into a thin positive, subtract it from a `--margin`-padded block, leaving a skull-shaped cavity. Takes the same draft-corrected (not shelled) input as `shell` and reuses whatever draft angle/blur was already baked in, since the same undercut-free requirement applies in both directions (a positive with no undercuts along the pull axis releases from a mold along it; a cavity with no undercuts along that axis releases the *cast piece* along it afterward). No special "leave the mouth open" padding trick needed here, unlike `shell`: the block is left unpadded at the base end of the pull axis, so `block AND NOT mesh` is already empty exactly at the mesh's own footprint there, by construction. Untested physically — this is a from-scratch alternative to the whole plaster-press step, not yet validated against a real print/pour.

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

## Print prep (learned 2026-09-20/21, from failed first-layer prints on the A1)

**Import the `_PRINT` files, don't rotate in the slicer.** The rim (parting face) is flat to ~0.01 mm in the STL, but rotating/"Place on face" in the slicer can leave a fraction-of-a-degree tilt (0.1° over 126 mm = 0.22 mm, more than the whole first layer). Symptom: brim and first layer appear only along the lowest edge; the rest of the 1.2 mm ring isn't in layer 1, starts in mid-air at layers 2–3, and fails. Fix: bake the orientation into the file so it imports rim-down with no rotation — left rotated −90° about Y, right +90°, then translate so min z = 0 (`_PRINT` suffix). Verify: slice, scrub to layer 1, the whole ring must be there.

**Other first-layer settings that matter for a 1.2 mm ribbon (Bambu A1, Overture PLA):** elephant-foot compensation 0 (default 0.075 shrinks the ribbon), slower/fatter first layer, fan off for first 3 layers, calibrated PA (0.058 for this Overture spool, not the 0.02 default). Supports: Tree Hybrid, build plate only, 3 wall loops (1.2 mm wall ≈ 3 × 0.42 mm lines). Cavity-ceiling supports are the only ones that touch cast surfaces.

**Shell thickness runs ~half a voxel thin** (distance is measured voxel-centre to voxel-centre): pitch 0.15 → ~1.17 mm, pitch 0.2 → ~1.10 mm for a requested 1.2. At 150% I requested `--thickness 1.3` at pitch 0.2 to land at median 1.23 mm (p5 1.06).

**150% recipe** (near real skull size; 143.8 × 188.7 × 58.6 mm printed, ~52 cm³ each half). Pitch 0.2, not 0.15: at 0.15 the grid is ~474M voxels, too much for 16 GB RAM.

```bash
python stl_add_draft.py draft "Skull (Left).stl" draft150.stl --scale 1.5 \
    --pull-axis x --base min --pitch 0.2 --draft 5 --blur 6 --smooth 20 --smooth-method taubin
python stl_add_draft.py shell draft150.stl shell150.stl --pull-axis x --base min --pitch 0.2 \
    --thickness 1.3 --blur 3 --teeth-blur 1 --teeth-radius 5 --smooth 20 --smooth-method taubin
python stl_add_draft.py mirror shell150.stl shell150R.stl --axis x --plane 0
# then rotate to rim-down (see Print prep): left -90°, right +90° about Y, drop to z=0
```

## Brim (mounting flange for the plaster pour) (added 2026-09-24)

Not a slicer brim (the throwaway adhesion skirt) -- a physical part: a rigid, ribbed, 4-holed flange fused onto a `shell` output's own open base rim, so the printed positive can sit skull-side-up, brim-side-down, at the bottom of a cottleboard box while the plaster mother mold gets poured over it. Run it as the last step, after `shell` (and after `mirror`, if mirroring a `shell` output that already has a brim also works -- `mirror`'s reflect-and-fix-winding is agnostic to what shape it's given). On a `_PRINT` file the parting face has already been rotated onto the bed, so the pull axis there is `z`/`min`, not the `x`/`min` every earlier recipe on this page uses.

```bash
python stl_add_draft.py brim "Skull (Left)_50pct_shell1.2mm_blur3_teeth1_PRINT.stl" \
    "Skull (Left)_50pct_brim.stl" \
    --pull-axis z --base min --thickness 6 --margin 25 \
    --natch-diameter 6 --natch-margin 5 --rib-count 8 --rib-height 6 --rib-width 3
```

- `--thickness 6`, ribbed underneath (`--rib-count`/`--rib-width`/`--rib-height`) rather than solid, for rigidity without much extra material/print time.
- `--margin` is the real decision here: how far the flange extends past the shell's own footprint, i.e. roughly the cottleboard box's interior size and how much plaster the pour uses. 25–35mm is a typical hand-mixed plaster piece-mold margin -- go bigger for a heavier/rougher-handled mold, but note `--margin` also has to leave room for the natch holes' own clearance (see below) or the command refuses to run.
- 4 through-holes (`--natch-diameter`/`--natch-margin`) for inserting natches, held with clips from below so the wet plaster casts around them, spaced evenly around the ring wherever it has `natch_margin + radius` clearance from BOTH the outer edge and the vent -- not literal "corners" for an irregular shape like a skull's. The script only cuts clean round holes -- how the natch itself keys/clips into that hole is a hardware choice, not something it decides. Size the diameter to the scale you're printing at (the original 8–16mm estimate is for 100%+ scale; a 50% test piece this small wants something more like 6mm, and needs `--margin` widened a few mm to give that clearance room on both sides).
- Critically, the brim attaches only to the shell's actual rim material (sliced from the mesh itself, not assumed from its bounding box) -- it does **not** span/cap the open interior, so packing the cavity with frozen isopropyl alcohol (see Next action) still works exactly as before.
- Left/right: since natch positions are derived from each half's own rim shape before mirroring, running `brim` before `mirror` (not after) means the two finished halves' natch holes land at matching mirrored positions automatically -- no separate symmetry step needed.
- If the input isn't a single clean watertight body (real exported STLs often aren't, even when they print fine -- see below), `brim` keeps only the largest connected piece and says how much it dropped. Read that line; it's assuming the dropped material is processing noise, not checking that it actually is.

**`--footprint circle` and solid (unshelled) input (added 2026-09-25).** Two independent additions to `brim`, usually used together:

- `input` no longer has to be a `shell` output. A solid `draft_correct` half (just split at the sagittal midline, never hollowed) works too -- `brim` now detects whether the rim cross-section has a vent at all and only preserves/differences one if it exists, instead of hard-erroring on a solid mesh. Point of this: a heavier, solid-print master skips the whole shell/interior-alcohol-packing question entirely, at the cost of more plastic and print time. Solid input can also have real, incidental interior loops in its cross-section that AREN'T a vent (a foramen/sinus wall crossing right at the slice depth -- found on the real skull, see 2026-09-25 log below) -- pass `--no-vent` to seal over those instead of trying to preserve them.
- `--footprint circle` replaces the rim-shaped plate outline with a single circle instead, centered to minimize how much the cross-section's edge-to-center distance varies, sized to the cross-section's own MEAN distance from that center plus `--margin` as a **target** width around the boundary -- not a worst-case minimum (an earlier version guaranteed `--margin` at the single farthest point, which measured more like +15mm over that everywhere else on the real, irregular skull cross-section -- see 2026-09-25 log). The realized min/mean/max clearance prints every run so the actual spread is visible, not just assumed. Combine with a thin `--thickness` (e.g. 1mm) and `--rib-height` as the real structural depth (e.g. 3mm) for a light skin-and-grid brim instead of a solid plate; the crosshatch grid is boolean-clipped to the circle's own shape so it can't overshoot at the corners the way a square grid naturally would against a round plate. `--footprint rim` (unchanged) stays the default.

Verified on synthetic test meshes before touching a real file (same discipline as the ring-shaped rim version's own debugging log, above, which found 6 silent bugs this way): an off-center solid half-sphere (footprint circle, no vent) and an off-center hollow half-shell (footprint circle, vent preserved) both checked out as `body_count`=1, watertight, exact minimum clearance (recomputed independently, not just trusting the script's own printed number), zero rib/plate overshoot past the circle via 400-ray radial cast, ~99% vertical-ray coverage across the disc (the ~1% misses land in the natch holes, as they should), and the interior cavity still ray-casts open on the vented case.

**Debugging note -- this took multiple rounds of silent failures, on both a synthetic test mesh AND the real file, each one a new instance of the same failure mode this project keeps running into: `is_watertight` and even the resulting volume can both look completely fine while the actual geometry is wrong (see "General takeaway" further up).** In order found:

1. First version built the plate as a plain rectangle covering the shell's whole bounding box. For an open shell that doesn't just attach to the rim, it PLUGS the mouth shut -- `body_count` going 1 → 2 (the plugged cavity's own wall stranded as a second, now fully enclosed body) was the only thing that caught it. Fixed by slicing the mesh's own rim cross-section and building the plate from that true shape, not its bounding box.
2. Crosshatch ribs touching the plate at an exactly coplanar face (rather than overlapping it) failed to fuse in the boolean union (`body_count` 1 → 3, watertight throughout).
3. The natch holes' axial span referenced the wrong pre-sorted extreme, so they cut cleanly through the ribs but stopped short of the plate itself -- a hole that silently isn't one.
4. Natch hole placement (a ray cast from the rim's centroid at 4 fixed angles) assumed the rim is roughly convex. A skull's rim is a RING -- its own centroid sits in the hollow middle, not on material -- and on the real 50%-scale file 2 of 4 holes landed in genuinely empty space, confirmed by grid-scanning a neighborhood around each (not just an unlucky exact edge). Fixed by eroding the plate's actual final shape (already correctly excluding the vent) by the hole's full required clearance and walking whatever's left by arc length instead.
5. Even after that fix, natch positions were STILL wrong on the real file specifically -- `mesh.section()`'s returned 2D coordinates live in an arbitrary local frame with its own translation (chosen by trimesh for its own convenience, unrelated to the plane origin passed in), and natch placement had been using those coordinates directly as global ones. This happened to be harmless on the synthetic test sphere (which was centered at the same point the local frame's origin ended up at, purely by construction) and wrong by ~19mm on the real, off-center skull. Fixed by pushing the local points through the same `to_3D` transform `extrude_polygon` was already correctly using for the plate itself.
6. Real exported STLs aren't guaranteed to be one clean watertight body just because they printed fine -- the `_PRINT` file's `is_watertight` came back False, caused not by a hole but by ~25 tiny (1-2 face) degenerate slivers plus one small 3430-vertex blob, all disconnected from the main 2.3M-vertex shell (a slicer silently ignores debris like this; `manifold3d`'s boolean engine does not). Fixed by keeping only the largest connected component and reporting what got dropped.

All of the above were caught by `body_count`, ray-casting for genuine pass-through material (not just checking a single point -- checking its surroundings too, since a "hole" that's actually a whole empty region looks identical to a real one at just its center), and, for #6, running the actual `_PRINT` file rather than trusting the synthetic test alone. The synthetic hemisphere-shell test mesh caught #1-4 in seconds each; #5 and #6 only showed up on the real geometry, which is exactly why this got run against it before calling any of it settled.

## Log

### 2026-10-09

Both physical loops done, all from plaster poured over the brimmed prints:

- **150% half-skull dishes** — two clay half-skull dishes from the 150% press molds. One breakage in the 150% plaster mold, at the cavity above the jaw bone; minor, and the resulting flaw on the clay piece was easy to fettle. Otherwise release was clean.
- **60% whole skull, drain-cast** — the 60% left and mirrored right molds closed together as a two-piece sagittal mold. No pour opening was designed in, so it was rotocast instead: filled the mold halfway with slip, closed it, rolled it continuously for even (enough) wall coverage, then demolded, cut a hole in the bottom, and drained it. The natches registered perfectly and the halves lined up.
- **Detail** — lower than the scan (the single-axis X draft blocks out some of the orbit/nasal/arch detail), but plenty good enough for ceramic; glazing will lose more detail than the draft did. So a third mold piece along another pull axis isn't justified by these results.

What this settles: the left + mirrored right molds already work as a two-piece mold for a whole hollow vessel, and natches placed with brim-before-mirror register correctly. Neither the frozen-alcohol packing nor the silicone intermediate was needed.

Still open (only matters if this goes further): the jaw-bone cavity is the one weak spot in the plaster, probably a thin plaster fin where the X-draft leaves a narrow concave pocket — more draft blur there, or a slightly larger draft angle, would likely thicken it. A designed pour opening would replace the rotocast + cut-a-hole step if a clean, intentional rim matters.

### 2026-10-04

150% shell printed and cast into a plaster negative (worked). Added a `core` command (solid inward erosion by `--inset` mm, flush at the parting face — `shell`'s padding trick without the hollowing) to make a clay-pressing plug: its outer surface sits 5 mm inside the plaster cavity, leaving a 5 mm gap for a clay sheet. Detail is already in the plaster, so it's low-res for fast printing:

```bash
python stl_add_draft.py draft "Skull (Left).stl" draft150_p04.stl --scale 1.5 \
    --pull-axis x --base min --pitch 0.4 --draft 5 --blur 3 --smooth 20 --smooth-method taubin
python stl_add_draft.py core draft150_p04.stl core150.stl --pull-axis x --base min \
    --pitch 0.4 --inset 5 --blur 1.5 --smooth 20 --smooth-method taubin
# rotate -90° about Y, drop to z=0 -> `Skull (Left)_150pct_core5mm_PRINT.stl`
```

Verified: watertight, 556 cm³, 132.4 × 175.6 × 53.7 mm printed; vertex distance to the drafted outer surface 4.3–5.3 mm (median 4.85, same half-voxel-thin bias as `shell`). Teeth and thin ridges vanish (narrower than 10 mm). Not yet printed.

### 2026-09-25

Updated `brim` per a design change: the brimmed piece is now meant to mount a solid, split-in-half (not shelled) skull half, with a circular flange instead of one shaped to the object's own rim. Added `--footprint circle` (see the Brim section above for the clearance-guarantee math and why a square rib grid needs boolean-clipping against a round plate) and made the vent-preserving logic optional so a solid `draft_correct` input no longer hard-errors. Also swapped `--thickness`/`--rib-height` semantics in practice, though not in the code (both already existed as separate flags) -- for a 1mm skin + 3mm structural grid, pass `--thickness 1 --rib-height 3` rather than the old solid-plate-style `--thickness 6`.

Verified on synthetic meshes only so far (see Brim section) -- not yet run against the real draft-corrected skull half or printed. Still open: what `--margin`/clearance to actually use for the real piece (45mm was given as a requirement, not yet run), and whether `--rib-count`/`--rib-width` need retuning now that the grid sits under a much thinner 1mm skin than the original 6mm solid-plate design assumed.

**Follow-up, same day: ran it for real, found two more issues.** Generated `Skull (Left)_draft60pct_blur6.stl` (60% scale, `--pitch 0.09 --draft 5 --blur 6`, matching the half-scale recipe's proportional pitch) and ran `brim --footprint circle` against it (natch sizing scaled down from the full-size 12mm/15mm to 8mm/10mm, in between the 50%-test-piece's 6mm and full size, since this is still an intermediate-scale test, not final hardware). Two problems, neither caught by the synthetic tests (both had been too clean/symmetric to surface either):

1. **The solid cross-section had real interior loops that weren't a vent.** The draft-corrected base cross-section came back with 2 tiny (<3mm²) interior loops -- real anatomy (a foramen/sinus wall crossing right at the slice depth), not a mold-cavity mouth, but `brim`'s vent-detection couldn't tell the difference and either errors (buffered to nothing by `--brim-overlap`) or would've cut a pointless pinhole in a solid piece. Fixed by adding `preserve_vent`/`--no-vent`, an explicit opt-out rather than a guessed size threshold -- see Brim section above.
2. **The "guaranteed minimum" circle overshot badly.** Asked for 45mm minimum clearance, measured closer to 60mm almost everywhere except the one farthest point that had set the circle's radius -- an irregular cross-section's max distance from center can sit well beyond its own mean (measured on this file: mean 31.5mm vs. max 44.6mm, a ~13mm gap). Re-centering the circle to minimize the edge-distance spread barely helped (<1mm of std) -- the gap is a property of the shape's radius distribution, not of where it's centered. Switched `--footprint circle` from a worst-case-guaranteed minimum to a target width: center fit by `scipy.optimize.minimize` to minimize distance-spread, radius = mean distance + `--margin`. Re-run with `--margin 30`: realized clearance now ranges 16.2-46.2mm, averaging exactly 30.0mm as targeted (full range printed by the command, not just the average).

Verified: main body of both outputs is a single watertight component (2,212,060 of 2,212,064 faces on the left; the other 4 are single-triangle STL float32 export slivers, the same kind of debris the 2026-09-24 entry below found on the `_PRINT` file -- cosmetic, slicers auto-repair it). Left/right correspondence re-confirmed on the real files the same way as the synthetic check: 500 random left-mesh vertices, reflected across x=0, land at exactly 0.0mm from the right mesh's surface. Not yet printed.

### 2026-09-24

Added the `brim` command (see section above) for the actual plaster-pour step: a rigid, ribbed, natch-holed mounting flange fused onto a `shell` output's open rim. First verified on a synthetic hemisphere-shell test mesh (single fused watertight body, natch holes confirmed as genuine through-holes by grid-scanning for empty/pass-through points, interior cavity confirmed still open by ray-casting through the center, both `--base min` and `--base max` checked via a mirrored copy of the test mesh) — found and fixed 3 silent boolean-CSG bugs there, none caught by `is_watertight`.

Then ran it for real against `Skull (Left)_50pct_shell1.2mm_blur3_teeth1_PRINT.stl` (the actual half-scale print file from 2026-09-19/20, `--pull-axis z --base min` since that file's parting face is already rotated onto the bed) and found 2 more bugs that the synthetic test's symmetry had been masking: natch placement assumed a roughly-convex rim (broke on a skull's actual ring-shaped, non-convex cross-section), and separately used `mesh.section()`'s local 2D coordinates as if they were global ones (harmless on a mesh centered at the same point the local frame happened to land on; ~19mm off on the real, off-center skull). Also handled real-world mesh mess along the way: the `_PRINT` file's `is_watertight` was False from ~25 tiny degenerate slivers plus one small disconnected blob (not from any real hole) — invisible to the slicer that already printed this file fine, fatal to `manifold3d`'s boolean engine. All 5 real-file bugs total (3 from the synthetic round + 2 new ones) are logged in the section above with what specifically broke and how it was caught. Final output: `Skull (Left)_50pct_shell1.2mm_blur3_teeth1_PRINT_brim.stl` in Downloads, `--margin 25 --natch-diameter 6 --natch-margin 5` — verified via the same body-count/ray-cast checks, all 4 holes confirmed as genuine clearances surrounded by real material at their corrected positions.

Not yet run on the 150% file, not yet physically printed/poured, and the natch/clip hardware itself (how a natch physically keys and clips into the printed hole) is still an open, unscripted decision. The dropped small blob (bounds roughly x∈[0.6,1.5] y∈[-34.1,-33.4] z∈[0,7.9], a thin ~8mm-tall sliver) hasn't been visually confirmed as junk vs. a real disconnected anatomical fragment (e.g. from a thin tooth pinching off during shelling) — worth a look before trusting the dropped-material assumption on a print that matters.

### 2026-09-23

Ran the `negative` pipeline on the real skull scan for the first time (previously only tested on the synthetic mushroom mesh). 50% scale, 4mm margin, draft `--blur 3` (negative has no separate teeth-blur/teeth-radius — those are shell-only, since negative has no erosion step to re-sharpen creases against). Draft → negative → mirror, pitch 0.075, 5% draft, smooth 20 taubin throughout.

```bash
python stl_add_draft.py draft "Skull (Left).stl" "Skull (Left)_draft50pct_blur3.stl" \
    --pull-axis x --base min --pitch 0.075 --draft 5 --blur 3 --scale 0.5 \
    --smooth 20 --smooth-method taubin
python stl_add_draft.py negative "Skull (Left)_draft50pct_blur3.stl" "Skull (Left)_negative_50pct_blur3_margin4mm.stl" \
    --pull-axis x --base min --pitch 0.075 --margin 4 --smooth 20 --smooth-method taubin
python stl_add_draft.py mirror "Skull (Left)_negative_50pct_blur3_margin4mm.stl" "Skull (Right)_negative_50pct_blur3_margin4mm.stl" \
    --axis x --plane 0.0
```

Verified: both halves watertight, positive volume (67,020.5 mm³ each, matching between L/R as expected from mirroring), correct mirrored bounds. Open-mouth ray-cast (25 rays through the cavity's central footprint, cast toward the base) showed zero near-base crossings — genuinely open pour face, not a fabricated floor. Not yet printed or poured — direct-print mold cavity route is still otherwise untested per the 2026-09-22 entry below.

### 2026-09-22

Added a `negative` command: carves the draft-corrected solid out of a margin-padded block instead of shelling it, producing a mold cavity that could in principle be printed and poured into directly, skipping the plaster-press step entirely. Verified on a synthetic mushroom-overhang test mesh (draft → negative): watertight, positive volume (no inside-out orientation), and ray-cast-confirmed genuinely open at the pour face (rays pass through the mouth and first hit the cavity's far interior wall, not a fabricated floor) — same verification approach the shell command's log entry below describes, applied to the new command before touching the real skull scan. Not yet run on the actual skull file or tested physically; still an open question whether a rigid direct-print mold gets comparable tooth detail to the plaster-press route.

### 2026-09-19 to 2026-09-21

Half-scale, then 100% and 150% shells generated with the fixed script. First-layer failures on Overture PLA traced to slicer tilt of the rim, not the filament (see Print prep). 150% (closer to real skull size) is the current print target; plaster release and support release still untested.

### 2026-07-29

Built out the full draft → shell → mirror pipeline this session (see Lessons learned above for the technical arc). Landed on a final accepted recipe: 5% draft with blur=6, shell at 1.2mm with blur=3/teeth-blur=1/teeth-radius=5, both at pitch 0.15. Produced and mirrored the final left+right STLs. Script is documented heavily (module + per-function docstrings, full argparse help text) specifically so it's readable cold in 6 months without re-deriving any of this. Next physical step is printing and testing plaster release.
