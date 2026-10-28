---
title: Choochoo Mug, 14 oz (Plaster Mold Masters)
created: 2026-10-11
updated: 2026-10-27
folder: 40
type: project
status: active
importance: 3
goal: Scale the choochoo mug to hold 14 oz and produce printable masters for two plaster slip-casting molds, one for the handleless body (two side halves and a foot plug) and one for the handle (two halves)
scope: one mug form, Fusion STEP in, build123d scripts, eleven printed parts, two plaster molds, stoneware and porcelain slip
tags: [ceramics, slipcasting, mold-making, 3d-printing, build123d]
related: [mug-recessed-foot, skull-mold-draft-shell]
schema-version: 1.0
ai-assisted: true
---

## Goal

A mug with a recessed foot that holds 14 oz fired (the first version held 11.95 oz), cast in stoneware and porcelain slip. The body and the handle are cast separately in their own plaster molds and joined at leather hard. The model exported from Fusion is the **mold cavity**: its outside surface is the outside of the mug, so it is solid and unshelled.

## Scope

**In:** uniform rescale. The handle split off the body. A body mold: two side halves, a grooved foot plug, and a plaster reservoir collar. A handle mold: two halves with sprues and pour cups. Printed masters with molded-in keys, and detachable printed cottles (U-halves and clips) around them. Every printed molding surface 1.2 mm thick. A README and scripts that build all of it as exact build123d geometry.
**Out:** shelling the model, a general mold generator, new handle geometry (the choochoo handle stays), a printed funnel. Anything else goes in the inbox.

## Done looks like

One mug cast and assembled: a body with seams only on two vertical lines plus the foot ring, a handle joined over one seam line, a foot ring that trims cleanly, and a measured fired capacity close to 14 oz. Stretch: the same in porcelain.

## Vocabulary

Follows [the skull glossary](../../90-archive/skull-mold-draft-shell/UBIQUITOUS_LANGUAGE.md).

- **Parting plane:** Y=0. For the body it is any plane through the axis; for the handle it is the handle's mid-plane.
- **Master:** a printed back plate with half a positive and the keys on it. Each master is cast twice.
- **Cottle:** the walls that hold the plaster around a master. Here it is two identical **U-halves** (an end wall plus half of each side wall) joined at mid-length by **fins** and slide-on **clips**.
- **Keys:** conical bosses and dimples on the back plate that become dimples and bosses in the plaster.
- **Plug:** the plaster disc that forms the recessed foot; it sits in a grooved socket between the two side halves.
- **Reservoir collar:** a 45° step out from the rim and a straight wall above it, cast into the top of the side halves. It holds the slip that drains into the plaster.
- **Sprue:** the handle's cross-section continued 15.4 mm straight past its root plane (x = 52.4) toward the mug. Over its last 10 mm each sprue flares into a **pour cup** (5 mm wider on every side, a 33.1 × 21.5 mm mouth) at the handle mold's pour face (x = 37).
- **Skin:** the 1.2 mm (three 0.4 mm lines) shell that every printed molding surface is made of.

## Decisions and why

**Scale ×1.049 (4.9% linear).** 11.95 oz is the fired brim capacity, shrinkage already included. Wall thickness does not scale with the mold, so a plain cube-root of 14 / 11.95 (×1.054) overshoots. I backed the effective fired wall out of the 11.95 oz figure with the model's profile (4 to 6 mm at 10 to 14% shrinkage, which is typical slip casting) and solved for 14 oz. The factor is ×1.048 to ×1.050 across that whole shrinkage range. Treat it as an estimate good to about 0.5 oz until a fired mug is measured. Taking the handle off does not change the capacity.

**Handle cast separately (2026-10-27).** With the handle on, the body needed two mirrored masters, a flat print (layer terraces on the mug surface), and a 217 mm flange. Without it the body is a solid of revolution:

- One master, cast twice. The second cast mates after a 180° turn about the mug axis.
- The master prints upright, so its layers are rings around the mug rather than terraces.
- The parting plane can go anywhere. Put the handle over one seam line and that seam gets fettled away under the handle's root.

The handle is exactly symmetric top to bottom (checked on 3,000 sampled points), so its master is also cast twice and the second cast turns 180° about the mid-height line. The idea comes from Old Forge Creations' D-shaped handle mould; the geometry is ours.

**Exact geometry, no meshes (2026-10-27, third pass).** Everything is described in build123d from measured dimensions; `choochoomug-14oz.step` is only read to check the result. I measured the dimensions from the STEP's own analytic faces.

- **The body is a revolve.** It runs: a foot cone from (r 41.96, z 0) to (51.598, 7.710), an r 2.098 fillet to the belly at (52.381, 9.481), a 3.61° straight wall to (46.187, 107.556), an r 0.525 round onto the flat top at z 108.047 and r 45.664, and the dish underneath. The dish is neither a circle nor a parabola, so it is a spline through 9 points sampled from the STEP, with its end tangents. 0 of 1,500 sampled points disagree with the STEP.
- **The handle is a stadium swept around a half circle.** The stadium is 11.538 radial by 23.078 along Y, with semicircle ends. It sweeps on r 37.12 about an axis parallel to Y through (52.418, 58.496). Fusion's side faces are cones with a 0° semi-angle about that axis. Sections at six angles match the STEP's; Fusion's crown is a B-spline within 0.07 mm of the semicircle. The roots end in the plane x = 52.418, at the belly.
- The Fusion solid also has a 6.2 mm wide, 0.04 mm high flat strip down both sides, a split artifact. The analytic body drops it.

An earlier pass cut the handle off with booleans against the Fusion faces and hollowed the masters as meshes. Those booleans were flaky (lone sprues, `.clean()` collapsing unions, nonsense symmetric differences), and the mesh hollowing left non-manifold edges. Built from the dimensions, every boolean is between lines, arcs, cones and stadiums.

**Sprues, not fitted ends.** The handle's sweep runs on past its root plane in a straight line to x = 47. Over the last 10 mm, to x = 37 (the handle mold's pour face), it flares into a pour cup. The bare sprue is only 11.5 × 23 mm, too small to pour into cleanly. Pour slip into one cup and air leaves through the other. At leather hard, cut the sprues to the body's curve: r ≈ 51.6 at the lower root (z 21) and r ≈ 47.0 at the upper root (z 96). Fusion's small root fillets are not modelled; blend the joint by hand.

**Foot plug with a V-groove, in a split ring.** For a side split, the dished underside is the only real undercut (4,860 of about 5,100 mm²), so the foot is still a separate plug. New: a 45° V-groove 3 mm deep sits 12.5 mm down the socket. It locks the plug between the halves, so the plug cannot drop out when the mold is turned over to drain. That replaces the 2° taper, which only resisted slip pressure. A grooved plug cannot leave a one-piece cup, so it is cast on a floor disc inside two identical ring halves. The Old Forge tumbler mould's insert works the same way.

**Plaster reservoir collar instead of a printed funnel.** The collar steps out 4 mm from the rim on a 45° chamfer and rises 30 mm, holding about 200 mL against an estimated 150 to 200 mL of slip loss (assumes a 5 mm cast wall). The rim has a 0.5 mm round, so the cast has a slight waist at the rim, followed by the step: that is the cut line. This removes the printed funnel, its 0.3 mm gap and its seepage risk.

**Molded-in keys, not natch inserts.** The keys form in the plaster, so there is no hardware. Body keys are 2 bosses on -X and 2 dimples on +X. Handle keys come as boss/dimple pairs mirrored about mid-height, one pair outside the D and one inside the loop.

**Detachable cottles, not one-piece trays (2026-10-27, second pass).** The first pass printed the walls as part of the master, drafted 2°, with a slide-on cap. Plaster sets bonded to every wall at once and expands slightly, so a one-piece tray, the handle's above all, would be hard to release, and the undrafted floor and cap would drag. Now each master is just the back plate, the half positive and the keys. Around it stand two identical U-halves, joined at mid-length by fins and two slide-on C-clips, as on the Old Forge moulds. Demold: pull the clips, slide each U off along the mold's length (each wall touches the plaster on one face only), then lift the plaster off the master in +Y. No wall needs draft.

- The U-halves stand on the table beside the plate rather than hooking under it, so the plate lies flat under the plaster's weight.
- The plate stops 0.15 mm short of the end walls, so the socket, the reservoir collar and the handle's pour cups all touch a wall and come out open.
- The body's U end walls are its floor and top. The mold still stands flat on the struck plaster faces.

**1.2 mm skins on every molding surface (2026-10-27, third pass).** A solid master holds the set plaster rigidly. A 1.2 mm skin (three 0.4 mm lines) flexes inward as you pull, and it uses a fraction of the filament: the body master is 50 cm³ instead of 744, the handle master 23 instead of 83.

- **Body hollow:** the positive's profile, offset 1.2 mm inward and revolved. The offset is exact: OCC's 2D offset fails on this profile, because the 0.525 mm rim round collapses under a 1.2 mm offset. So the hollow is the region inside the profile minus a 1.2 mm "sausage" (Minkowski sum with a disc) around each edge. It runs out through the plate back and is open at both ends, where the cottle end walls close it. Standing upright, the print then has no roof to bridge.
- **Handle hollow:** a stadium 1.2 mm smaller, swept along the same path. A stadium's exact offset is a stadium. The pour-cup hollows are inset 1.2 / cos(flare), so the flared walls are 1.2 mm thick too.
- **Parting face:** a 1.2 mm skin over a void, on 1.2 mm ribs at 45°, 25 mm apart. The ribs print both upright (body) and flat (handle), and they stop at the half's footprint so the shell can still flex. The void is built as disjoint diamond cells, because cutting a crossing grid of ribs out of one void ran OCC out of memory on this 3 GB machine.
- **Keys:** each dimple is a 1.2 mm cup. The bosses stay solid; they are tiny.
- **Cottles:** the cottle walls are 1.2 mm thick. Fins and clips mold no plaster, so they stay thicker.
- **Plug parts:** the plug ring is a 1.2 mm wall that follows the V-groove. The plug floor is a 1.2 mm pit skin on concentric 1.2 mm rings at r 10, 20 and 30, open underneath.
- **Checks:** probes confirm solid 0.6 mm in and hollow 1.3 mm in on the mug wall, the handle's outer side, crown and inner side, and the parting face. They also confirm that each skin's rim reaches the cottle wall at the socket, the collar and the pour cups.

## Parts

| File | What it is | Print or cast |
| --- | --- | --- |
| `body_master_PRINT.stl` | Hollow back plate with half `body_positive` and keys, 155 × 58 × 163 mm, 50 cm³ | Print standing on its socket end; cast plaster twice |
| `body_cottle_PRINT.stl` | U-half of the body cottle, 174 × 83 × 83 mm | Print two |
| `body_clip_PRINT.stl` | Fin clip, 83 mm long | Print two |
| `handle_master_PRINT.stl` | Hollow back plate with half `handle_positive` and keys, 78 × 136 × 23 mm, 23 cm³ | Print back plate down; cast plaster twice |
| `handle_cottle_PRINT.stl` | U-half of the handle cottle, 97 × 69 × 43 mm | Print two |
| `handle_clip_PRINT.stl` | Fin clip, 43 mm long | Print two |
| `plug_floor.stl` | Floor disc with the dish pit and a locating lip, ⌀92.9 × 11 mm | Print; the plug is cast on it |
| `plug_ring.stl` | Half of the ring around the plug, with the V-ridge | Print two |
| `body_positive.step` | Body + filled dish + grooved socket + reservoir collar | Source for the body master |
| `handle_positive.step` | Handle + both sprues and pour cups | Source for the handle master |
| `body.step` | The handleless body | Reference |

STL files are gitignored. Regenerate them with the scripts. The `.step` files are the same parts, for CAD.

Plaster per pour: about 1.36 L per body half, 150 mL for the plug, 0.37 L per handle half.

## Scripts

Setup: `python3 -m venv .venv && .venv/bin/pip install build123d` (`scale_mug.py` also needs `trimesh`). On this machine that needed `sudo apt install python3-venv python3-pip` first.

1. `scale_mug.py`: scales `choochoomug.step` by `--scale` (default 1.049) and writes `choochoomug-14oz.step` and `.stl`.
2. `make_mold_parts.py`: the dimensions and the profile, stadium and path builders. Writes `body`, `body_positive`, `handle_positive`, `plug_floor` and `plug_ring` (about 1 minute). Checks:
   - the body matches the STEP by point sampling
   - the handle matches the STEP by sections at six angles (point sampling gives false insides near Fusion's B-spline crown)
   - the flipped plug sits on the floor's pit without overlapping it
   - it reports the reservoir volume
3. `make_masters.py`: imports those builders and makes the hollow masters (`--margin 25`, `--plate 6`), the keys and the cottles. Writes `body_master`, `body_cottle`, `body_clip`, `handle_master`, `handle_cottle` and `handle_clip` (about 10 seconds). Checks:
   - each master is one valid solid
   - no key is within 3 mm of the cavity
   - the skin probes pass
   - the skin rims reach the cottle walls
   - the two U-halves close the space without overlapping

Gotchas hit along the way:
- build123d's `Spline` needs both end tangents or neither.
- `Plane.XZ`'s normal is -Y.
- OCC cannot 2D-offset these B-spline or tiny-arc profiles, hence the exact stadium and sausage offsets.

## Print settings

STLs cannot carry slicer settings, so set these per object in the slicer.

| Part | Layer height | Notes |
| --- | --- | --- |
| Body master | 0.12 mm | Standing on its socket end as exported; the layers are rings around the mug. The foot cone overhangs 51° from vertical over about 10 mm; look at it on the first print. 45° chamfers on the groove and collar. No supports |
| Handle master | adaptive, or 0.12 mm over the handle | Open back on the bed. The handle half rises 11.5 mm (16.5 at the cups), so terraces are short. The hollow's crown is a 4.6 mm radius arch and the plate skin bridges diamond cells about 24 mm across; both sit inside, away from the molding faces |
| Plug floor | 0.12 mm | Its pit forms the foot dish; the pit skin bridges at most 10 mm between its rings |
| Plug ring ×2 | 0.2 mm | On its end; the V-ridge is 45° |
| Cottle U-halves ×2 per mold, clips ×2 per mold | 0.2 mm | On their table edge as exported. The clips pinch the fins with 0.1 mm per side; if too tight, scale the clip 102% in X and Z |

All parts: at least 3 wall loops at 0.4 mm, so every 1.2 mm skin prints as solid perimeters (the parts are already hollow; infill only fills the thicker fins, clips and ledges). Elephant-foot compensation about 0.15 mm. Import as-is: no rotation, no "place on face".

## Lessons from the Glencairn 3-part mold

Studied 2026-10-11: a MakerWorld 3-part (three identical sides plus a foot insert) Glencairn mold by Old Forge Creations, used widely by others. MakerWorld Exclusive License, so only the design ideas are taken here, no geometry.

- **Same architecture.** The foot is a separate insert, and the maker revised it in V2 ("Changed Foot Insert"). The foot is the likeliest part of ours to need a second iteration, so print and cast the plug early.
- **Surface layers differ from structure layers.** Masters and foot parts at 0.12 mm, cottle parts at 0.2 mm; 2 walls, 15% cubic infill, no supports; elephant-foot compensation 0.15 mm.
- **Release and bubbles.** Mouldmaker's soap on the master's flat base surface. Pour plaster until it covers the surface but the cavity is not full, brush gently to free trapped air, then fill.
- **Quantities.** About 375 mL of plaster per side piece and 50 mL for the insert on a roughly 9 cm glass; uniform scaling keeps everything fitting. His 9 cm cast fires to 8 cm, about 11% shrinkage, inside the 10 to 14% I assumed for the ×1.049 scale.
- **Identical pieces need symmetry.** A handle on the body breaks it. That is now solved by casting the handle separately.

## Lessons from the tumbler and D-handle moulds

Studied 2026-10-27: Old Forge Creations' "Smooth Tumbler/Mug Mould" (2 sides + base insert, ×1.12 for shrinkage) and "D-Shaped Handle Mould" (2-part). Same maker and license as the Glencairn, so again ideas only, no geometry.

- **The print is the whole pour box.** The tumbler master is back plate + floor + half body in one upright print, with clip-on walls; the handle kit is the same with locks. Ours copies that: the walls come apart so they release one face at a time. (A first pass built the walls into the master with draft; I reverted that.)
- **Keys are molded in.** Round bosses and dimples on the back plate, placed so one master's two casts mate.
- **The foot insert has a groove** and is cast in a split form on a floor disc.
- **A collar on the rim** casts a reservoir into the plaster.
- **One master, cast twice** for each mold, made possible by symmetry. Moving the handle off the body gives us the same thing.
- **Handle mold demolding:** the maker flexes the printed mold away from the set plaster. Release agent on the printed surface.
- **Plaster:** about 1350 mL per tumbler side and 180 mL for the insert, close to our 1.36 L and 150 mL.

## Pour and assembly (planned, not yet run)

1. Print the body master, two body U-halves and two clips; the handle master, two handle U-halves and two clips; the plug floor and two plug rings.
2. Body halves: lay the master on its back plate. Slide one U-half on from each end, then push the clips down over the fins. Seal the outside of the wall/plate seam and the fin joints with a clay coil. Soap everything. Pour to the wall tops, brushing the mug surface first, and strike flat. Once set, pull the clips, slide the U-halves off, and lift the plaster off the master. Pour again for the second half.
3. Handle halves: the same, with the handle cottle. Brush plaster into the pour cups and around the handle first.
4. Plug: set the two ring halves inside the floor's lip with their seams closed, tape or band the outside, soap, pour to the ring top, and strike flat.
5. Dry everything. Dry-fit the body mold: plug in the socket (the groove must seat), turn one half 180° and close on the keys, strap. Dry-fit the handle mold the same way.
6. Body: stand the mold on a flat surface and fill to the top of the collar. Top up as the level drops, drain at wall thickness, then cut the cast at the rim step when it releases.
7. Handle: stand the mold with the pour cups up, pour into one cup until slip shows in the other, and let it fill solid. Demold and cut the sprues to the body's curve.
8. At leather hard, score and slip the joints. Attach the handle over one body seam line, then fettle.

## Risks to watch

- The plug seam sits at the highest slip head. If it weeps, add a clay coil. If the groove does not seat, sand the plug's ridge or reprint the ring.
- Cottle seams: the U-halves stand beside the plate with 0.15 mm clearance and butt at the fins. Plaster can seep at those seams; a clay coil outside both seams should hold it. If a U-half drags as it slides off, flex its walls out first.
- Upright print: the foot cone overhangs 51° from vertical. If it sags, reprint with slower outer walls, or fill the shelf with a 45° skirt and carve the plaster back.
- The foot ring is a knife edge by geometry (the underside rises 4.2 mm over 42 mm); trim and sponge it at leather hard.
- The handle's inner and outer faces have 0° draft for 5.8 mm next to the parting line (cylinders about the handle axis). The 1.2 mm skin is there to flex away; pull gently.
- Handle joint: cut sprues to fit by hand. If fitting by eye is unreliable, add a printed trimming template (not in scope yet; inbox it).
- Scope creep: if more than three next actions are active at once, cut back to the smallest version.

## Next action

- [ ] Print the handle master, its two U-halves and two clips, plus the plug floor and one plug ring (small and quick). Check the clip fit on the fins, the ring's V-ridge against the floor lip, and how the 1.2 mm skins print before printing the 163 mm body master

## Log

### 2026-10-27 (third pass)

Two asks: make every molding surface 1.2 mm thick so the masters flex off the plaster and use less filament, and build everything as plain build123d geometry. A mesh-erosion attempt (manifold3d) produced non-manifold STLs, so I dropped it.

Measured the body and handle from the STEP's analytic faces. The handle turned out to be a stadium swept about a Y axis at the belly. Rebuilt the body, handle, positives and plug parts from those dimensions, and checked them against the STEP. Hollowed everything with exact 2D offsets: stadiums for the handle, edge sausages for the body. Built the plate void as diamond cells after a crossing rib grid ran OCC out of memory.

Masters: body 50 cm³ (was 744), handle 23 cm³ (was 83). Nothing printed or cast yet.

### 2026-10-27 (second pass)

Reviewed the first pass: the cottle was part of each master, which would make release hard (the handle's above all), and the handle sprues had no pour cups. Split each cottle into two identical U-halves with fins and slide-on clips, Old Forge style; the masters are now plate + half positive + keys, and the body cap is gone. Added 10 mm pour cups to the handle sprues. Nothing printed or cast yet.

### 2026-10-27

Studied the Old Forge tumbler and D-handle moulds and decided to cast the handle separately. Revolved the body from its +Y profile, cut the handle at the body surface, and extended the roots into sprues. With the handle gone the body is a solid of revolution, and the handle is symmetric top to bottom, so each mold now needs one master cast twice.

Replaced the flange + natch masters (A and B) with upright tray masters that have drafted walls and molded-in keys. Replaced the printed funnel with a 30 mm plaster reservoir collar, and the 2° taper plug with a V-grooved plug cast in a split ring. Removed `master_A`, `master_B`, `funnel`, `plug_cup` and `halves_positive`. Also removed `make_cottle.py` and `cottle.step` (added 2026-10-27 on the remote: a 0.8 mm leaning-wall tub sleeved over the A/B flange), which fit only the old masters. The trays now carry their own walls. Ideas kept from it: lean the walls to save plaster, and budget about 15 mm of plaster beside the cavity at minimum.

Hit two flaky OCC booleans (handle + sprue fuse, `.clean()`); worked around them with a fuzzy fuse and volume asserts. Nothing printed or cast yet.

### 2026-10-11

Scaled the Fusion STEP to ×1.049 for 14 oz. Chose a foot plug over a belly split after measuring that the dish is the only real undercut. Built the halves positive, plug cup and funnel, then split on the sagittal plane and fused each half to a natch flange. Two masters because the halves are mirror images. Nothing printed or cast yet. Studied a Glencairn 3-part mold file and took print settings and process notes from it (see Lessons). Overlaps with [mug-recessed-foot](../mug-recessed-foot/README.md); that project's base-piece plan is superseded by the plug here.
