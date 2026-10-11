---
title: Choochoo Mug, 14 oz (Plaster Mold Masters)
created: 2026-10-11
updated: 2026-10-11
folder: 40
type: project
status: active
importance: 3
goal: Scale the choochoo mug to hold 14 oz and produce printable masters for a plaster slip-casting mold (two sagittal halves, a foot plug, a pour funnel)
scope: one mug form, Fusion STEP in, build123d scripts, six printed parts, one plaster mold, stoneware and porcelain slip
tags: [ceramics, slipcasting, mold-making, 3d-printing, build123d]
related: [mug-recessed-foot, skull-mold-draft-shell]
schema-version: 1.0
ai-assisted: true
---

## Goal

A handled mug with a recessed foot that holds 14 oz fired (the first version held 11.95 oz), cast in stoneware and porcelain slip from a plaster mold made from printed masters. The model exported from Fusion is the **mold cavity**: its outside surface is the outside of the mug, so it is solid and unshelled.

## Scope

**In:** uniform rescale; a foot plug; a funnel seat and printed funnel; two masters split on the sagittal plane, each fused to a flange with natch holes; a README and scripts so the whole pipeline reruns from the STEP.
**Out:** shelling the model, a general mold generator, new handle geometry, a mold for the plug beyond the one printed cup. Anything else goes in the inbox.

## Done looks like

One mug cast from the finished mold, with a clean seam on the underside only, a foot ring that trims cleanly, and a measured fired capacity close to 14 oz. Stretch: the same in porcelain.

## Vocabulary

Follows [the skull glossary](../../90-archive/skull-mold-draft-shell/UBIQUITOUS_LANGUAGE.md).

- **Sagittal plane:** the median plane through the handle (Y=0). It is this mug's **parting plane**.
- **Master:** a printed half fused to its flange, used to cast one plaster half.
- **Flange:** the printed pour-box floor the half stands on; **natches** are the 12 mm holes through it.
- **Plug:** the plaster disc that forms the recessed foot; it sits in a socket between the two halves.
- **Funnel seat:** a short boss on the rim that leaves a pocket in the plaster top for the funnel.

## Decisions and why

**Scale ×1.049 (4.9% linear).** 11.95 oz is the fired brim capacity, shrinkage already included. Wall thickness does not scale with the mold, so a plain cube-root of 14 / 11.95 (×1.054) overshoots. I backed the effective fired wall out of the 11.95 oz figure with the model's profile (4 to 6 mm at 10 to 14% shrinkage, which is typical slip casting) and solved for 14 oz. The factor is ×1.048 to ×1.050 across that whole shrinkage range. Treat it as an estimate good to about 0.5 oz until a fired mug is measured.

**Foot as a plug between full-height halves, not a base split at the belly.** For a split on the sagittal plane, about 95% of the undercut area (4,860 of about 5,100 mm²) is the dished underside, up to about 9°. Everything else, including the flare and belly, releases sideways. A belly split would leave a visible ring seam on the widest part; a plug puts its seam on the underside at the foot ring, which is trimmed anyway. The fallback if the plug seam leaks is a base piece split at the belly (r 52.5 mm, z about 9).

**Plug is 2° wider toward its flat bottom.** A plug that narrows toward its open face cannot come out of its own plaster-casting cup. The assembled mold stands on a flat surface, which takes the slip pressure on the plug, so the taper does not have to resist it.

**Two masters, A and B.** The halves are mirror images. Plaster poured over two copies of the same master gives two same-handed halves, and the handle ends up on opposite sides when they close. B is A mirrored across the flange's vertical centre line; flip a half cast from B about that line and it mates with a half cast from A, with the natches on top of each other.

**Funnel.** Bore equals the rim (diameter 91.7 mm), so the cast ends at the plaster edge instead of at a spare you cut off. The straight bore holds about 230 mL against an estimated 150 to 200 mL slip loss (assumes a 5 mm cast wall). Expect a faint line where the cast meets the funnel.

## Parts

| File | What it is | Print or cast |
| --- | --- | --- |
| `master_A_PRINT.stl`, `master_B_PRINT.stl` | Half + flange, 217.7 × 141 × 57.4 mm, flat on the bed, no support | Print both; cast one plaster half from each |
| `plug_cup.stl` | Printed cup, ⌀93.7 × 32 mm | Pour plaster in; the plug is the result |
| `funnel.stl` | Pour reservoir, ⌀122 × 68 mm | Print, foot down |
| `halves_positive.step` | Whole positive: mug, filled dish, 25 mm socket boss, 8 mm funnel-seat boss | Source for the masters |

STL files are gitignored. Regenerate them from the STEP files and scripts.

## Scripts

Setup: `python3 -m venv .venv && .venv/bin/pip install build123d trimesh`

1. `scale_mug.py`: scales `choochoomug.step` by `--scale` (default 1.049); writes `choochoomug-14oz.step` and `.stl`.
2. `make_mold_parts.py`: writes `halves_positive`, `plug_cup`, `funnel` and a `plug_preview` check part. Its checks print the cavity difference (want 0) and the funnel fit.
3. `make_half_masters.py`: splits the positive, adds the flange and natches (`--margin 35`, `--thickness 5`, `--natch-diameter 12`), writes `master_A` and `master_B`, and checks that A plus flipped B rebuild the positive.

Flange edges at the top and bottom sit flush with the boss ends. Stand the pour-box walls on those edges and the funnel pocket and plug socket come out open in the plaster.

## Print settings

STLs cannot carry slicer settings, so set these per object in the slicer.

| Part | Layer height | Notes |
| --- | --- | --- |
| Masters A and B | 0.12 mm | The surface is the mug's outer surface. Elephant-foot compensation about 0.15 mm, 2 walls, about 15% infill, no supports. Import `_PRINT` files as-is: no rotation, no "place on face" |
| Plug cup | 0.12 mm | Its floor forms the foot dish |
| Funnel | 0.2 mm | Foot down; the 45° flare needs no support |

The parting face is the bed face, so a flared first layer would put a lip at the cavity edge, right where the halves seal. If the 217 × 141 mm flange bows on the first print, rerun `make_half_masters.py --thickness 8` or add a brim. Lying flat leaves layer terraces on the mug's outer ridge (at most the layer height tall, about 7 mm wide at 0.12 mm). Standing the master upright would avoid that but the handle loop would need support; print one flat and look before changing anything.

## Lessons from the Glencairn 3-part mold

Studied 2026-10-11: a MakerWorld 3-part (three identical sides plus a foot insert) Glencairn mold by Old Forge Creations, used widely by others. MakerWorld Exclusive License, so only the design ideas are taken here, no geometry.

- **Same architecture.** The foot is a separate insert, and the maker revised it in V2 ("Changed Foot Insert"). The foot is the likeliest part of ours to need a second iteration, so print and cast the plug early.
- **Surface layers differ from structure layers.** Masters and foot parts at 0.12 mm, cottle parts at 0.2 mm; 2 walls, 15% cubic infill, no supports; elephant-foot compensation 0.15 mm.
- **Release and bubbles.** Mouldmaker's soap on the master's flat base surface. Pour plaster until it covers the surface but the cavity is not full, brush gently to free trapped air, then fill.
- **Quantities.** About 375 mL of plaster per side piece and 50 mL for the insert on a roughly 9 cm glass; uniform scaling keeps everything fitting. His 9 cm cast fires to 8 cm, about 11% shrinkage, inside the 10 to 14% I assumed for the ×1.049 scale.
- **Identical pieces need threefold symmetry.** A handle breaks that, which is why this project has mirrored masters A and B.
- **Registration is built into his master** (round bosses and rectangular slots). I keep my own natch-insert system instead. This and the next point are my reading of the photos and geometry, not stated by the maker.
- **His master prints standing on its edge** (glass axis vertical), which gives concentric rings on the cast surface. Ours lies flat because of the handle loop.
- **A reservoir cap in plaster.** His master has a half-disc cap on the rim that looks like a plaster reservoir. My printed funnel is a different, untested approach.

## Pour and assembly (planned, not yet run)

1. Print both masters, the plug cup and the funnel.
2. Stand pour-box walls on the master's flange edges, at least about 80 mm tall (the half rises 52 mm; leave 25 to 30 mm of plaster over it).
3. Clip a natch insert in each hole from below, pour plaster over master A, and demold. Repeat with master B.
4. Pour plaster into the plug cup, strike it flat, and demold.
5. Dry everything. Dry-fit before the first slip: plug in the socket, close the halves (flip B about its vertical centre line), seat the funnel.
6. Strap the halves, add a thin clay coil at the seams if slip weeps, and stand the mold on a flat surface.

## Risks to watch

- Plug seam sits at the highest slip head. If it weeps, add a wider clay coil or go to the belly-split fallback.
- The foot ring is a knife edge by geometry (the underside rises 4.2 mm over 42 mm); trim and sponge it at leather hard.
- The funnel foot is 0.3 mm under the pocket radius and has no gasket. A clay coil or O-ring fixes seepage.
- The handle's conical faces show about 1.7° of reverse draft over about 260 mm². Untested; a gentle pull should clear it.
- Scope creep: if more than three next actions are active at once, cut back to the smallest version.

## Next action

- [ ] Print master A and the plug cup first, at 0.12 mm; check the natch holes against the clip and insert and the flange flatness before printing the rest

## Log

### 2026-10-11

Scaled the Fusion STEP to ×1.049 for 14 oz. Chose a foot plug over a belly split after measuring that the dish is the only real undercut. Built the halves positive, plug cup and funnel, then split on the sagittal plane and fused each half to a natch flange. Two masters because the halves are mirror images. Nothing printed or cast yet. Studied a Glencairn 3-part mold file and took print settings and process notes from it (see Lessons). Overlaps with [mug-recessed-foot](../mug-recessed-foot/README.md); that project's base-piece plan is superseded by the plug here.
