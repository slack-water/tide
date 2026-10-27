---
title: Choochoo Mug, 14 oz (Plaster Mold Masters)
created: 2026-10-11
updated: 2026-10-27
folder: 40
type: project
status: active
importance: 3
goal: Scale the choochoo mug to hold 14 oz and produce printable masters for two plaster slip-casting molds, one for the handleless body (two side halves and a foot plug) and one for the handle (two halves)
scope: one mug form, Fusion STEP in, build123d scripts, five printed parts, two plaster molds, stoneware and porcelain slip
tags: [ceramics, slipcasting, mold-making, 3d-printing, build123d]
related: [mug-recessed-foot, skull-mold-draft-shell]
schema-version: 1.0
ai-assisted: true
---

## Goal

A mug with a recessed foot that holds 14 oz fired (the first version held 11.95 oz), cast in stoneware and porcelain slip. The body and the handle are cast separately in their own plaster molds and joined at leather hard. The model exported from Fusion is the **mold cavity**: its outside surface is the outside of the mug, so it is solid and unshelled.

## Scope

**In:** uniform rescale. The handle split off the body. A body mold: two side halves, a grooved foot plug, and a plaster reservoir collar. A handle mold: two halves with sprues. Printed tray masters with drafted walls and molded-in keys. A README and scripts so the whole pipeline reruns from the STEP.
**Out:** shelling the model, a general mold generator, new handle geometry (the choochoo handle stays), a printed funnel. Anything else goes in the inbox.

## Done looks like

One mug cast and assembled: a body with seams only on two vertical lines plus the foot ring, a handle joined over one seam line, a foot ring that trims cleanly, and a measured fired capacity close to 14 oz. Stretch: the same in porcelain.

## Vocabulary

Follows [the skull glossary](../../90-archive/skull-mold-draft-shell/UBIQUITOUS_LANGUAGE.md).

- **Parting plane:** Y=0. For the body it is any plane through the axis; for the handle it is the handle's mid-plane.
- **Master:** a printed tray with half a positive on its back plate. Each master is cast twice.
- **Tray:** the back plate plus the walls that hold the plaster. Walls are drafted 2° wherever the plaster only needs to release.
- **Keys:** conical bosses and dimples on the back plate that become dimples and bosses in the plaster.
- **Plug:** the plaster disc that forms the recessed foot; it sits in a grooved socket between the two side halves.
- **Reservoir collar:** a 45° step out from the rim and a straight wall above it, cast into the top of the side halves. It holds the slip that drains into the plaster.
- **Sprue:** the handle's root cross-section extended 15.6 mm toward the mug. Both sprues run to the handle mold's pour face.

## Decisions and why

**Scale ×1.049 (4.9% linear).** 11.95 oz is the fired brim capacity, shrinkage already included. Wall thickness does not scale with the mold, so a plain cube-root of 14 / 11.95 (×1.054) overshoots. I backed the effective fired wall out of the 11.95 oz figure with the model's profile (4 to 6 mm at 10 to 14% shrinkage, which is typical slip casting) and solved for 14 oz. The factor is ×1.048 to ×1.050 across that whole shrinkage range. Treat it as an estimate good to about 0.5 oz until a fired mug is measured. Taking the handle off does not change the capacity.

**Handle cast separately (2026-10-27).** With the handle on, the body needed two mirrored masters, a flat print (layer terraces on the mug surface), and a 217 mm flange. Without it the body is a solid of revolution:

- One master, cast twice. The second cast mates after a 180° turn about the mug axis.
- The master prints upright, so its layers are rings around the mug rather than terraces.
- The parting plane can go anywhere. Put the handle over one seam line and that seam gets fettled away under the handle's root.

The handle is exactly symmetric top to bottom (checked on 3,000 sampled points), so its master is also cast twice and the second cast turns 180° about the mid-height line. The idea comes from Old Forge Creations' D-shaped handle mould; the geometry is ours.

**Body = the +Y profile revolved.** The Fusion solid has a 6.2 mm wide, 0.04 mm high flat strip along the full height at ±X, a split artifact, and the handle sits at +X. The YZ section on the +Y side has neither, so it is the true profile. The handle is whatever of the mug lies outside a body that is 0.5 mm oversize, which drops the strip. Body + handle rebuilds the mug to within 266 mm³: the 0.5 mm skin under the roots, plus the strip.

**Sprues, not fitted ends.** Each root's cross-section at x = 52.6 (just past the belly) is extruded to x = 37, which is the handle mold's pour face. Pour slip into one sprue and air leaves through the other. At leather hard, cut the sprues to the body's curve: r ≈ 51.6 at the lower root (z 21) and r ≈ 47.0 at the upper root (z 96). The upper root's flare stays on the handle and blends into the body.

**Foot plug with a V-groove, in a split ring.** For a side split, the dished underside is the only real undercut (4,860 of about 5,100 mm²), so the foot is still a separate plug. New: a 45° V-groove 3 mm deep sits 12.5 mm down the socket. It locks the plug between the halves, so the plug cannot drop out when the mold is turned over to drain. That replaces the 2° taper, which only resisted slip pressure. A grooved plug cannot leave a one-piece cup, so it is cast on a floor disc inside two identical ring halves. The Old Forge tumbler mould's insert works the same way.

**Plaster reservoir collar instead of a printed funnel.** The collar steps out 4 mm from the rim on a 45° chamfer and rises 30 mm, holding about 200 mL against an estimated 150 to 200 mL of slip loss (assumes a 5 mm cast wall). The rim has a 0.5 mm round, so the cast has a slight waist at the rim, followed by the step: that is the cut line. This removes the printed funnel, its 0.3 mm gap and its seepage risk.

**Trays with molded-in keys, not flanges with natch inserts.** Each master is one print: the back plate, the walls and the half positive. The pour box is the print, so there are no loose walls, and the keys form in the plaster, so there is no hardware. Body keys are 2 bosses on -X and 2 dimples on +X. Handle keys come as boss/dimple pairs mirrored about mid-height, one pair outside the D and one inside the loop. The walls that only release are drafted 2°. The faces that must come out flat or open are not drafted:

- the body floor, so the socket opens and the mold stands flat
- the body cap, flush with the collar so the reservoir opens
- the handle's sprue end, so both sprues open

## Parts

| File | What it is | Print or cast |
| --- | --- | --- |
| `body_master_PRINT.stl` | Body tray with half `body_positive`, 166 × 83 × 166 mm | Print upright, floor on the bed; cast plaster twice |
| `body_cap_PRINT.stl` | Cap that closes the top of the body tray, 172 × 86 × 16 mm | Print plate down |
| `handle_master_PRINT.stl` | Handle tray with half `handle_positive`, 85 × 134 × 38 mm | Print back plate down; cast plaster twice |
| `plug_floor.stl` | Floor disc with the dish pit and a locating lip, ⌀98.5 × 11 mm | Print; the plug is cast on it |
| `plug_ring.stl` | Half of the ring around the plug, with the V-ridge | Print two |
| `body_positive.step` | Body + filled dish + grooved socket + reservoir collar | Source for the body master |
| `handle_positive.step` | Handle cut at the body + both sprues | Source for the handle master |
| `body.step` | The handleless body | Reference |

STL files are gitignored. Regenerate them from the STEP files and scripts.

Plaster per pour: about 1.36 L per body half, 150 mL for the plug, 0.29 L per handle half.

## Scripts

Setup: `python3 -m venv .venv && .venv/bin/pip install build123d trimesh`. On this machine that needed `sudo apt install python3-venv python3-pip` first.

1. `scale_mug.py`: scales `choochoomug.step` by `--scale` (default 1.049) and writes `choochoomug-14oz.step` and `.stl`.
2. `make_mold_parts.py`: splits the body and handle, then writes `body`, `body_positive`, `handle_positive`, `plug_floor`, `plug_ring` and a `plug_preview` check part. Checks: body outside mug (want 0), side-half cavity vs body (want 0), plug inside the ring bore (want 0), reservoir volume.
3. `make_masters.py`: builds the trays (`--margin 25`, `--plate 6`, `--wall 3`, `--draft 2`), adds the keys, and writes `body_master`, `body_cap` and `handle_master`. Checks: each master is one solid and its volume equals its parts; no key is within 3 mm of the cavity; each half plus its turned copy rebuilds the positive.

Two build123d (OCC) booleans in this pipeline are flaky. Fusing the sprues to the handle sometimes returns a lone sprue, and `.clean()` on that union does the same. The scripts use a fuzzy fuse (`tol=0.01`) and assert on volumes, so a bad boolean fails loudly instead of writing a broken part.

## Print settings

STLs cannot carry slicer settings, so set these per object in the slicer.

| Part | Layer height | Notes |
| --- | --- | --- |
| Body master | 0.12 mm | Upright as exported; the layers are rings around the mug. The foot cone overhangs 51° from vertical over about 10 mm; look at it on the first print. 45° chamfers on the groove and collar. No supports |
| Handle master | adaptive, or 0.12 mm over the handle | Back plate on the bed. The handle half rises 11.5 mm, so terraces are short |
| Plug floor | 0.12 mm | Its pit forms the foot dish |
| Plug ring ×2 | 0.2 mm | On its end; the V-ridge is 45° |
| Body cap | 0.2 mm | |

All parts: elephant-foot compensation about 0.15 mm, 2 walls, about 15% infill. Import as-is: no rotation, no "place on face".

## Lessons from the Glencairn 3-part mold

Studied 2026-10-11: a MakerWorld 3-part (three identical sides plus a foot insert) Glencairn mold by Old Forge Creations, used widely by others. MakerWorld Exclusive License, so only the design ideas are taken here, no geometry.

- **Same architecture.** The foot is a separate insert, and the maker revised it in V2 ("Changed Foot Insert"). The foot is the likeliest part of ours to need a second iteration, so print and cast the plug early.
- **Surface layers differ from structure layers.** Masters and foot parts at 0.12 mm, cottle parts at 0.2 mm; 2 walls, 15% cubic infill, no supports; elephant-foot compensation 0.15 mm.
- **Release and bubbles.** Mouldmaker's soap on the master's flat base surface. Pour plaster until it covers the surface but the cavity is not full, brush gently to free trapped air, then fill.
- **Quantities.** About 375 mL of plaster per side piece and 50 mL for the insert on a roughly 9 cm glass; uniform scaling keeps everything fitting. His 9 cm cast fires to 8 cm, about 11% shrinkage, inside the 10 to 14% I assumed for the ×1.049 scale.
- **Identical pieces need symmetry.** A handle on the body breaks it. That is now solved by casting the handle separately.

## Lessons from the tumbler and D-handle moulds

Studied 2026-10-27: Old Forge Creations' "Smooth Tumbler/Mug Mould" (2 sides + base insert, ×1.12 for shrinkage) and "D-Shaped Handle Mould" (2-part). Same maker and license as the Glencairn, so again ideas only, no geometry.

- **The print is the whole pour box.** The tumbler master is back plate + floor + half body in one upright print, with clip-on walls; the handle kit is the same with locks. Ours goes one step further: drafted walls are part of the master, and only the cap is separate.
- **Keys are molded in.** Round bosses and dimples on the back plate, placed so one master's two casts mate.
- **The foot insert has a groove** and is cast in a split form on a floor disc.
- **A collar on the rim** casts a reservoir into the plaster.
- **One master, cast twice** for each mold, made possible by symmetry. Moving the handle off the body gives us the same thing.
- **Handle mold demolding:** the maker flexes the printed mold away from the set plaster. Release agent on the printed surface.
- **Plaster:** about 1350 mL per tumbler side and 180 mL for the insert, close to our 1.36 L and 150 mL.

## Pour and assembly (planned, not yet run)

1. Print the body master, the body cap, the handle master, the plug floor and two plug rings.
2. Body halves: slide the cap on and seal the cap seam from outside with clay or hot glue. Soap all surfaces. Lay the tray on its back plate and pour to the wall tops, brushing the mug surface first. Strike flat, let it set, and slide the block out in +Y. Pour again for the second half.
3. Handle halves: soap, pour to the wall tops, strike, flex the tray off. Pour again.
4. Plug: set the two ring halves inside the floor's lip with their seams closed, tape or band the outside, soap, pour to the ring top, and strike flat.
5. Dry everything. Dry-fit the body mold: plug in the socket (the groove must seat), turn one half 180° and close on the keys, strap. Dry-fit the handle mold the same way.
6. Body: stand the mold on a flat surface and fill to the top of the collar. Top up as the level drops, drain at wall thickness, then cut the cast at the rim step when it releases.
7. Handle: stand the mold with the sprues up, pour into one sprue until slip shows at the other, and let it fill solid. Demold and cut the sprues to the body's curve.
8. At leather hard, score and slip the joints. Attach the handle over one body seam line, then fettle.

## Risks to watch

- The plug seam sits at the highest slip head. If it weeps, add a clay coil. If the groove does not seat, sand the plug's ridge or reprint the ring.
- The body floor and cap are not drafted, so the plaster slides along them as it lifts out. If the block sticks, flex the walls, use more soap, or add 0.5° to the floor and accept a slight rock that a sanded base removes.
- Upright print: the foot cone overhangs 51° from vertical. If it sags, reprint with slower outer walls, or fill the shelf with a 45° skirt and carve the plaster back.
- The foot ring is a knife edge by geometry (the underside rises 4.2 mm over 42 mm); trim and sponge it at leather hard.
- Handle conical faces had about 1.7° of reverse draft over about 260 mm² for this split. Untested; flex the tray and pull gently.
- Handle joint: cut sprues to fit by hand. If fitting by eye is unreliable, add a printed trimming template (not in scope yet; inbox it).
- Scope creep: if more than three next actions are active at once, cut back to the smallest version.

## Next action

- [ ] Print the plug floor, one plug ring and the handle master first (small, quick), and check the ring's V-ridge against the floor lip before printing the 166 mm body master

## Log

### 2026-10-27

Studied the Old Forge tumbler and D-handle moulds and decided to cast the handle separately. Revolved the body from its +Y profile, cut the handle at the body surface, and extended the roots into sprues. With the handle gone the body is a solid of revolution, and the handle is symmetric top to bottom, so each mold now needs one master cast twice.

Replaced the flange + natch masters (A and B) with upright tray masters that have drafted walls and molded-in keys. Replaced the printed funnel with a 30 mm plaster reservoir collar, and the 2° taper plug with a V-grooved plug cast in a split ring. Removed `master_A`, `master_B`, `funnel`, `plug_cup` and `halves_positive`. Also removed `make_cottle.py` and `cottle.step` (added 2026-10-27 on the remote: a 0.8 mm leaning-wall tub sleeved over the A/B flange), which fit only the old masters. The trays now carry their own walls. Ideas kept from it: lean the walls to save plaster, and budget about 15 mm of plaster beside the cavity at minimum.

Hit two flaky OCC booleans (handle + sprue fuse, `.clean()`); worked around them with a fuzzy fuse and volume asserts. Nothing printed or cast yet.

### 2026-10-11

Scaled the Fusion STEP to ×1.049 for 14 oz. Chose a foot plug over a belly split after measuring that the dish is the only real undercut. Built the halves positive, plug cup and funnel, then split on the sagittal plane and fused each half to a natch flange. Two masters because the halves are mirror images. Nothing printed or cast yet. Studied a Glencairn 3-part mold file and took print settings and process notes from it (see Lessons). Overlaps with [mug-recessed-foot](../mug-recessed-foot/README.md); that project's base-piece plan is superseded by the plug here.
