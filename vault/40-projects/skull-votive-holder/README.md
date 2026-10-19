---
title: Skull Votive Holder (Slip-Cast, Jawless)
created: 2026-10-15
updated: 2026-10-15
folder: 40
type: project
status: active
importance: 3
goal: Produce printable masters for a two-piece plaster slip-casting mold of a jawless, tipped-back skull that holds a 40 mm votive dropped in through the crown
scope: masters only (two printable halves on cottle flanges); not the plaster pour, the casting, or the firing
tags: [ceramics, slipcasting, mold-making, 3d-printing, python, skull]
related: [skull-mold-draft-shell, choochoomug-14oz]
schema-version: 1.0
ai-assisted: true
---

## Goal

A ceramic skull candle holder, cast in slip from a two-piece plaster mold, that rests on its upper teeth with the lower jaw gone, and takes a 40 × 20 mm votive dropped in through the top.

## Scope

**In:** removing the lower jaw from the existing half-skull scan; posing the skull as a jawless skull rests; cutting the crown open for the candle; a pour boss at the base; a sagittal split with lateral (X) draft; a cottle flange per half with 12 mm natch holes; scripts that rerun all of it; checks that the candle fits and the cast stands.
**Out:** pouring plaster, casting, firing, glaze; a candle seat or riser; eye-socket light holes; a lid. Anything else goes in the inbox, not here.

## Done looks like

A fired skull, tipped back on its teeth, with a 40 mm votive dropped in through the top and lit, cast from a mold whose halves close with the natches registered. Stretch: a second cast that fixes whatever the first one shows.

## Vocabulary

Follows [the skull glossary](../../90-archive/skull-mold-draft-shell/UBIQUITOUS_LANGUAGE.md) (parting plane, pull axis, natch, flange, master). New here:

- **Base plane:** the flat the finished skull stands on, z = 0 in every file. It cuts the incisor and canine crowns and the underside of the occiput.
- **Crown cut:** the flat cut across the top of the cranium. The cast closes over it with a flat lid; cut the lid out at leather hard and the opening is the rim.
- **Pour boss:** a half-cylinder on the parting plane, ⌀32, from the skull base down to z = -25. It becomes the pour hole in the plaster and the neck of the cast.

## Decisions and why

**The jaw is removed by min-cut, not by a plane.** The lower jaw is fused to the skull at the bite and at the jaw joint, and its ramus rises above any plane through the teeth. A plane through the bite line would leave the ramus on or cut the skull base. `prep_skull.py` voxelizes the scan, seeds known jaw and known skull voxels, and finds the minimal cut between them. The cut falls on the contacts: between the teeth, and at the joint. 8.4 cm³ of jaw came off. Seeds are measured on this one scan; they will not transfer to another.

**The pose is where a jawless skull comes to rest, not a tilt I chose.** The skull touches a table on its upper incisors and the underside of the occiput. That is the longest downward edge of the side-view convex hull, and it sits 11.0° off the scan's upright. Rotating about X (the pull axis) to level it leaves the sagittal split untouched. The face looks up and the skull reads as tipped back. `--extra-tilt` pitches it further if wanted.

**Scale ×1.1 of the scan.** Mold size, 86 × 126 mm wide and long; fired at 11% shrinkage about 77 × 112 × 70 mm. The widest circle through the cast opening is 47.6 mm fired, against 44 needed (40 candle plus 2 mm each side), so +3.6 mm. At 14% shrinkage it is still +2. Going smaller loses the fit. Going larger buys margin and costs a lot of plaster.

**Base plane trimmed 6.5 mm into the skull.** The natural contact is a single incisor tip. At 6.5 mm the cut is through the tooth row, giving a real foot of about 170 mm² per side at the front and 400 to 600 mm² at the occiput. This is the "bottom is the upper teeth" the brief asked for.

**Crown cut at 79 mm above the base plane.** The opening is the cranial cross-section there, about 48 × 60 mm inside after the wall, so the candle drops in with room. A higher cut shrinks the opening below the candle; a lower one turns the skull into a dish.

**Pour boss at the skull base, y = 0, ⌀32, tip at z = -25.** The cast is a closed hollow, so it needs one hole to pour and drain. The base, in the notch under the cranium, is the one place that is out of sight and not a bearing surface. After casting the neck is trimmed flush with the base plane and leaves a hole about 22 mm across. The candle (40) cannot fall through it. The boss lies on the parting plane so it does not block the pull. The draft slopes the end face of the boss, so `make_masters.py` re-cuts it flat; the flange bottom edge is flush with it. Stand the cottle board on that edge and the pour hole comes out open in the plaster instead of closed by a wedge.

**Two masters, A and B, mirrored across the parting plane.** Same as the 60% two-piece mold: a plaster half cast from each, closed face to face. The flange is symmetric under that mirror, so the natch holes land in the same (y, z) on both. Four 12 mm natches, at the 25% and 75% height in each side strip. Only three are needed.

**Rectangular flange, 30 mm margin, 5 mm thick,** following choochoomug-14oz, because the brief says cottle *boards*. The earlier skull molds used a circular flange and a printed ring; the boss end needs a flat edge to be flush with, so this one does not.

## Parts

All in `build/`, regenerated by the scripts (STLs are gitignored).

| File | What it is | Print or cast |
| --- | --- | --- |
| `master_A_PRINT.stl` | Left half on flange, 134 × 186.4 × 48.2 mm, flange on the bed, skull up, no support | Print; cast one plaster half |
| `master_B_PRINT.stl` | Mirror of A | Print; cast the other half |
| `drafted.stl`, `prep.stl` | Intermediates (drafted half; jawless posed half before draft) | Neither |

| `cottle_PRINT.stl`, `cottle.step` | One cottle for both masters (`make_cottle.py`, build123d, no mesh): a tub 182 × 124 mm at the flange, 62 mm deep, 0.8 mm wall (two passes of a 0.4 nozzle), its Y walls leaning in 35° so it narrows to about 95 mm at the rim. Stands on the flange face; skirt reaches the table at the boss end. Print rim down, no support | Print; pour plaster to the rim |

The cottle's boss-end wall is flush with the boss tip (open pour hole); the opposite wall is flat with no draft, so the closed mold stands on it boss up. The 35° lean follows the cranium narrowing as it rises (measured: at least 15 mm of plaster beside the half everywhere; the limit is about 36°) and doubles as the draft, so the cottle lifts off along +X. About 0.8 L of plaster per half against 1.5 L for a flange-sized box. Untested physically.

Each master is about 64 MB (1.9M faces) because the draft's marching-cubes surface is fine. Slicers cope. If one does not, decimate the STL to about 500k faces, not lower.

## Reproduce

Source scan: the left half-skull, `~/Downloads/Skull (Left).stl` (not in the vault). From this folder:

```bash
python3 -m venv .venv && .venv/bin/pip install -r requirements.txt
.venv/bin/python prep_skull.py -o build/prep.stl --preview build          # jaw off, pose, scale, crown, boss  (~20 s)
.venv/bin/python ../../90-archive/skull-mold-draft-shell/stl_add_draft.py draft build/prep.stl build/drafted.stl \
    --pull-axis x --base min --pitch 0.2 --draft 5 --blur 6 --smooth 20 --smooth-method taubin   # (~40 s)
.venv/bin/python make_masters.py build/drafted.stl --out-dir build         # flange, natches, A and B  (~15 s)
.venv/bin/python check_design.py build/drafted.stl                         # candle fit and stance
```

`prep_skull.py` imports the archived `stl_add_draft.py` by relative path instead of copying it; if the archive moves, update `DRAFT` at its top. Draft recipe is the one from the 150% run, at pitch 0.2.

## Checks run (2026-10-15)

- Jaw removal: looked at lateral renders and X-sections. The upper tooth row is intact and the ramus is gone. Not yet inspected from below or at the joint at high zoom; a small nub of condyle may remain under the zygomatic arch.
- Masters: A and B each one watertight body, positive volume, 400.7 cm³. Natch holes open with flange around them, on both A and B. Boss tip flat on z = -25, flange edge exactly flush. Both print files sit on z = 0 with the flange down. Not yet checked in a slicer.
- Candle fit: opening +3.6 mm over need (above). Cavity under the rim is 74 mold mm deep, 66 fired, so a 20 mm candle at the bottom burns about 46 mm below the rim.
- Stance: the hollow cast (5 mm wall, crown open) has its centre of mass at y = -6.6, inside the contact patches that span y = -70.9 to +46.1, 53 mm from the nearer edge. It stands.

## Open decisions and risks

- **The candle seat.** The skull is hollow, so the candle falls to the lowest interior point, at the back of the cranium, tilted with the pose, with the flame about 46 mm below the rim. It will burn, but the glow is deep. Ways out, none built: a loose ceramic riser or a layer of sand under the candle; or a lower crown cut. Decide after seeing the first cast, not before.
- **Draining.** In its resting pose the occiput is lower than the pour hole, so a little slip pools there when the mold is turned boss-down. Tilt the mold face-forward while draining.
- **The lid.** The crown cast closes with a flat lid. Cut it out at leather hard from inside the rim; the rim is the wall, 5 mm. The mold has no cut guide.
- **Fit margin is 3.6 mm.** If the first cast shrinks more than 14% or the wall runs thick, the candle will not drop in. Cheapest fix is `--scale 1.15` in `prep_skull.py`, which reruns the whole chain in about 2 minutes.
- **The first plaster mold will show whether the X draft holds the orbits and nose.** The 60% skull lost some detail to the single pull axis and that was acceptable. Same expectation here.
- Scope creep: this project has one goal. If more than three next actions are active, cut back. New ideas (seat, lid, light holes) go in the inbox.

## Print and pour notes

Print settings and plaster process follow [choochoomug-14oz](../choochoomug-14oz/README.md): 0.12 mm layers for the masters, elephant-foot compensation about 0.15 mm so the bed-contact parting face has no flared lip, 2 walls, about 15% infill, no supports, `_PRINT` files imported as-is with no rotation or "place on face". If the flange bows, rerun `make_masters.py --thickness 8`.

Cottle walls stand on the flange edges, at least 70 mm tall (the half is 43 mm; leave 25 mm of plaster over it). About 1.4 L of plaster per half. The bottom board sits flush with the boss tip. Clip natch inserts into the holes from below before pouring.

## Next action

- [ ] Look at `overview.png` and say whether the pose reads as tipped back the way you wanted. If yes, print master A at 0.12 mm and check the natch holes and the flange flatness before printing B.

## Log

### 2026-10-15

Created from the skull-mold-draft-shell scan and pipeline, and the choochoomug-14oz flange method. Wrote `prep_skull.py`, `make_masters.py`, `check_design.py`; built masters A and B end to end. Decisions and checks above. Several things changed along the way: the first plan was a planar cut at the bite line, dropped because the ramus rises above the teeth; the first foot trim (1.5 mm) left only a tooth tip touching, so it went to 6.5; the first mirror flipped the volume negative because trimesh already re-winds a reflection. Nothing printed or cast yet.
