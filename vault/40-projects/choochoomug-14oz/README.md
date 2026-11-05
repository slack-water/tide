---
title: Choochoo Mug, 14 oz (Plaster Mold Masters)
created: 2026-10-11
updated: 2026-11-05
folder: 40
type: project
status: active
importance: 3
goal: Scale the choochoo mug to hold 14 oz and produce printable masters for two plaster slip-casting molds, one for the handleless body (two side halves and a foot plug) and one for the handle (two halves)
scope: one mug form, Fusion STEP in, build123d scripts, printed masters, caps and cottles, a plywood box for the body, two plaster molds, stoneware and porcelain slip
tags: [ceramics, slipcasting, mold-making, 3d-printing, build123d]
related: [mug-recessed-foot, skull-mold-draft-shell]
schema-version: 1.0
ai-assisted: true
---

## Goal

A mug with a recessed foot that holds 14 oz fired (the first version held 11.95 oz), cast in stoneware and porcelain slip. The body and the handle are cast separately in their own plaster molds and joined at leather hard. The model exported from Fusion is the **mold cavity**: its outside surface is the outside of the mug, so it is solid and unshelled.

## Scope

**In:** uniform rescale. The handle split off the body. A body mold: two side halves, a grooved foot plug, and a plaster reservoir collar. A handle mold: two halves with sprues and pour cups. Printed masters with molded-in keys. The body's halves are poured at once from two masters paired back to back in a plywood box with printed end caps. The handle has a detachable printed cottle (U-walls with lock bars). Every printed molding surface 1.2 mm thick. A README and scripts that build all of it as exact build123d geometry.
**Out:** shelling the model, a general mold generator, new handle geometry (the choochoo handle stays, apart from a 2° release draft on its inner and outer faces), a printed funnel. Anything else goes in the inbox.

## Done looks like

One mug cast and assembled: a body with seams only on two vertical lines plus the foot ring, a handle joined over one seam line, a foot ring that trims cleanly, and a measured fired capacity close to 14 oz. Stretch: the same in porcelain.

## Vocabulary

Follows [the skull glossary](../../90-archive/skull-mold-draft-shell/UBIQUITOUS_LANGUAGE.md).

- **Parting plane:** Y=0. For the body it is any plane through the axis; for the handle it is the handle's mid-plane.
- **Master:** a printed back plate with half a positive and the keys on it. The body master is printed twice and the pair is poured at once. The handle master is cast twice.
- **Pair:** two body masters back to back, registered by **back pins** (a pin and a socket on each plate back, where no plaster reaches). The plates' **fences** run 10 mm past the plaster on both edges: the bottom one stands in a groove in the plywood floor, and the top one is a clamp edge.
- **End cap:** a flat printed plate that closes one end of the body box, both halves at once, and seals the skins' open ends.
- **Cottle:** the walls that hold the plaster around a master. For the body it is now plywood long sides and floor plus printed end caps. (It was two identical **U-halves** joined at mid-length by **fins** and slide-on **clips**.) Every printed cottle joint is now a pair of **T-rails** with a **lock** (a C-channel) slid down over them, as on the Old Forge D-handle kit. The handle's cottle is split that way: each U is a side wall plus half of each end wall, and the rails sit where the end walls meet. The plug ring's two halves meet on rails the same way.
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

**Foot plug with a V-groove, in a split ring.** For a side split, the dished underside is the only real undercut (4,860 of about 5,100 mm²), so the foot is still a separate plug. New: a 45° V-groove 3 mm deep sits 12.5 mm down the socket. It locks the plug between the halves, so the plug cannot drop out when the mold is turned over to drain. That replaces the 2° taper, which only resisted slip pressure. A grooved plug cannot leave a one-piece cup, so it is cast on a floor disc inside two identical ring halves. The halves join like the handle cottle, on T-rails with two locks (fins and clips until 2026-11-05), and a 45° seat sits on the disc's chamfered rim. The plug's foot-ring edge falls where the seat meets the disc. The Old Forge tumbler mould's insert works the same way, with a flange under the disc as well; ours dropped that (see below).

**Plug clearance and a floating ring (2026-11-05).** The first plug came out too big to fit its socket, and the ring had not closed cleanly on the floor disc. Two causes. (1) The plug was the socket's exact size, so any error made it too big. (2) The ring was held vertically twice: by its flange under the disc and by its seat on the disc's chamfer. A disc printed even slightly tall stopped the seat before the fins met, and at 45° each 0.1 mm of extra height holds each half 0.1 mm open. Plaster's setting expansion (about 0.2%) then pushes on a ring that is already loose. Fixes: the ring now molds the plug 0.25 mm per side inside the socket, on the sides and the V-groove (`PLUG_CLEAR`). A 0.25 mm ledge at the foot ring steps in from the seat; it is trimmed with the knife edge anyway. The flange is gone. The ring hangs on its seat, with its bottom 0.5 mm off the table (`RING_LIFT`) and a skirt 0.3 mm round the disc edge. The seat is now the ring's only contact, so it stays sealed, the locks close the joints fully, and a tall disc just lifts the ring. Raising the seat off the chamfer was rejected: the gap would let plaster flash over the chamfer and down round the disc edge.

**Plaster reservoir collar instead of a printed funnel.** The collar steps out 4 mm from the rim on a 45° chamfer and rises 30 mm, holding about 200 mL against an estimated 150 to 200 mL of slip loss (assumes a 5 mm cast wall). The rim has a 0.5 mm round, so the cast has a slight waist at the rim, followed by the step: that is the cut line. This removes the printed funnel, its 0.3 mm gap and its seepage risk.

**Molded-in keys, not natch inserts.** The keys form in the plaster, so there is no hardware. Body keys are 2 bosses on -X and 2 dimples on +X. Handle keys come as boss/dimple pairs mirrored about mid-height, one pair outside the D and one inside the loop.

**Detachable cottles, not one-piece trays (2026-10-27, second pass; body part superseded 2026-11-03, see below).** The first pass printed the walls as part of the master, drafted 2°, with a slide-on cap. Plaster sets bonded to every wall at once and expands slightly, so a one-piece tray, the handle's above all, would be hard to release, and the undrafted floor and cap would drag. Now each master is just the back plate, the half positive and the keys. Around it stand two identical U-halves, joined at mid-length by fins and two slide-on C-clips, as on the Old Forge moulds. Demold: pull the clips, slide each U off along the mold's length (each wall touches the plaster on one face only), then lift the plaster off the master in +Y. No wall needs draft.

**Body: both halves poured at once, from a back-to-back pair (2026-11-03).** The goal changed. I want to queue up many molds and pour them all in one plaster session, so both halves of a mold have to be poured together, not one master cast twice. The halves then come from two different prints, and they match only if (1) the prints agree, which two prints of one STL on one printer do to about 0.1 mm, and (2) neither moves or warps during the pour, which a loose 1.2 mm skin in a box would not guarantee.

- **Pair the masters only while pouring.** Two prints of `body_master` stand back to back, the second turned 180° about the mug axis, as the two plaster halves already mate. The plaster on either face pushes against the other print's back, so neither plate bows.
- **Pins on the plate backs.** Each back has a pin (+X) and a socket (−X), a tapered 8 → 6 mm pin, 3.5 mm long, with 0.15 mm clearance. The 180° turn puts each pin in the other print's socket, so one STL mates with itself. The pins sit where no plaster reaches; through-pins would be buried in plaster on both faces.
- **Not a single double-sided plate.** I considered one plate with a half positive on each face and the keys as domes through it. Rejected: when the first plaster half lifts off, the second still holds the plate rigid, so the print cannot bow and peel. That is most of why the thin body skin releases well. Separating the pair before demolding keeps that flex.
- **Fences on both edges.** The 180° turn swaps the plate's ±X edges, so a clamp edge on top only would land on the bottom of the second print. Each plate runs 10 mm past the plaster on both edges. The bottom fences stand in a 12.3 mm groove in the plywood floor, which also holds the pair upright. The top fences are a clamp edge above the fill line.
- **Printed end caps, plywood sides.** The skins are open at both ends, and the end walls must meet them within the 0.15 mm fit, or plaster gets behind the skin. Plywood is not that flat, so the two end caps are printed (5 mm, flat). Plywood takes the long sides and the floor, which only have to hold liquid.
- **Keys moved out to 15 mm of plaster.** The keys had about 6.5 mm of plaster between them and the cavity, and the same to the outer face, which is thin enough to chip. A new `--side` (default 42) sets the side margin on its own; the margin behind the positive (`--margin`) stays 25. It costs plaster: 1.79 L per half (was 1.36), 3.58 L per pour.
- **Demold:** strip the plywood and caps, pull the pair apart at the backs, then release each master from its own plaster exactly as before.

**Handle draft, 2° (2026-11-04).** The thin skin releases the body well, but it does not flex enough on the handle. The handle's inner and outer faces were 0° (parallel to the pull) for 5.8 mm either side of the parting plane, and a 1.2 mm skin on a 5.8 mm radius is nearly as stiff as solid plastic, so thickness was never going to fix it. Those faces now lean in 2° from the parting plane. The handle keeps its full 11.54 mm width at the parting plane and its 23.08 mm thickness. The flats narrow to 11.11 mm where they meet the end arcs, and the arcs shrink from r 5.77 to r 5.56 so they stay tangent. That is at most about 0.2 mm a side, gone in fettling, and the volume drops from 38.5 to 37.8 cm³. The sprues and pour cups get the same draft, so the swept section stays continuous. The checks still compare the undrafted handle with the Fusion STEP (an exact match), then probe the drafted faces. I chose 2° over 1° for more release margin.

**Handle walls with lock bars (2026-10-30).** The handle cottle now follows the Old Forge D-handle kit instead of the body's. Each U-wall is one side wall plus the matching half of both end walls (the other is the same part turned 180°). The walls meet at mid-width on the end walls, where each ends in a T-rail, and a C-channel lock slides down over each pair of rails for the full height. A friction clip on flat fins can creep off as the plaster pushes outward; the lock interlocks with the rails, so the walls cannot spread. The pour cups now face a plain side wall with no joint in it. Demold: slide the locks up, pull each wall straight off in ±X (the side wall leaves its face; the end-wall halves slide along theirs), then lift the plaster off.

**One joint style for every cottle (2026-11-05).** The rail-and-lock joint is now the standard: one builder (`rail_and_lock` in `make_masters.py`) makes the rails and locks for the handle cottle and the plug ring. The plug ring's fins and clips are replaced by a half T-rail at each end of each half, on a web out to the skirt, and a lock slides down over each pair. The body box is plywood and has no printed joints.

- The U-halves stand on the table beside the plate rather than hooking under it, so the plate lies flat under the plaster's weight.
- The plate stops 0.15 mm short of the end walls, so the socket, the reservoir collar and the handle's pour cups all touch a wall and come out open.
- The body's U end walls are its floor and top. The mold still stands flat on the struck plaster faces.

**1.2 mm skins on every molding surface (2026-10-27, third pass).** A solid master holds the set plaster rigidly. A 1.2 mm skin (three 0.4 mm lines) flexes inward as you pull, and it uses a fraction of the filament: the body master is 50 cm³ instead of 744, the handle master 23 instead of 83.

- **Body hollow:** the positive's profile, offset 1.2 mm inward and revolved. The offset is exact: OCC's 2D offset fails on this profile, because the 0.525 mm rim round collapses under a 1.2 mm offset. So the hollow is the region inside the profile minus a 1.2 mm "sausage" (Minkowski sum with a disc) around each edge. It runs out through the plate back and is open at both ends, where the end caps (body) close it. Standing upright, the print then has no roof to bridge.
- **Handle hollow:** a drafted stadium 1.2 mm smaller, swept along the same path. A drafted stadium's exact offset is a drafted stadium: the end arcs keep their centres and the flats move in 1.2 / cos(2°). The pour-cup hollows are inset 1.2 / cos(flare), so the flared walls are 1.2 mm thick too.
- **Parting face:** a 1.2 mm skin over a void, on 1.2 mm ribs at 45°, 25 mm apart. The ribs print both upright (body) and flat (handle), and they stop at the half's footprint so the shell can still flex. The void is built as disjoint diamond cells, because cutting a crossing grid of ribs out of one void ran OCC out of memory on this 3 GB machine.
- **Keys:** each dimple is a 1.2 mm cup. The bosses stay solid; they are tiny.
- **Cottles:** the cottle walls are 1.2 mm thick. Rails and locks mold no plaster, so they stay thicker.
- **Plug parts:** the plug ring is a 1.2 mm wall that follows the V-groove, then a 1.2 mm 45° seat and a 1.2 mm skirt round the disc edge. The plug floor is a 1.2 mm pit skin on concentric 1.2 mm rings at r 10, 20 and 30, open underneath.
- **Checks:** probes confirm solid 0.6 mm in and hollow 1.3 mm in on the mug wall, the handle's outer side, crown and inner side, and the parting face. They also confirm that each skin's rim reaches the cottle wall at the socket, the collar and the pour cups.

## Parts

| File | What it is | Print or cast |
| --- | --- | --- |
| `body_master_PRINT.stl` | Hollow back plate with half `body_positive`, face keys, back pin and socket, and fences, 209 × 62 × 163 mm, 66 cm³ | Print two, standing on the socket end; pour both at once, back to back |
| `body_cap_PRINT.stl` | Flat end cap for the body box, both halves, 199 × 167 × 5 mm | Print two |
| `handle_master_PRINT.stl` | Hollow back plate with half `handle_positive` and keys, 78 × 136 × 23 mm, 23 cm³ | Print back plate down; cast plaster twice |
| `handle_cottle_PRINT.stl` | U-wall of the handle cottle (side wall + two half end walls with T-rails), 40 × 149 × 43 mm | Print two |
| `handle_lock_PRINT.stl` | C-channel lock over the end-wall rails, 14 × 7 × 43 mm | Print two |
| `plug_floor_PRINT.stl` | Floor disc with the dish pit and a 45° chamfered rim, ⌀89.9 × 7.2 mm | Print; the plug is cast on it |
| `plug_ring_PRINT.stl` | Half of the ring around the plug: V-ridge, seat, skirt round the disc and T-rails, 103 × 47 × 32 mm | Print two |
| `plug_lock_PRINT.stl` | C-channel lock over the ring's rails, 7 × 14 × 32 mm | Print two |
| `plug_ring_test_PRINT.stl`, `plug_lock_test_PRINT.stl` | The ring's and lock's bottom 10.7 mm (skirt, seat, rails), for checking the fit on the floor disc | Print two of each first |
| `body_positive.step` | Body + filled dish + grooved socket + reservoir collar | Source for the body master |
| `handle_positive.step` | Handle (2° draft on its inner and outer faces) + both sprues and pour cups | Source for the handle master |
| `body.step` | The handleless body | Reference |

STL files are gitignored. Regenerate them with the scripts. The `.step` files are the same parts, for CAD.

Plaster per pour: about 1.79 L per body half (3.58 L for the pair), 150 mL for the plug, 0.37 L per handle half.

## Scripts

Setup: `python3 -m venv .venv && .venv/bin/pip install -r requirements.txt` (pins build123d 0.13.0 and its OCC kernel, the versions these scripts were checked with; `scale_mug.py` also needs `trimesh`). On this machine that needed `sudo apt install python3-venv python3-pip` first.

1. `scale_mug.py`: scales `choochoomug.step` by `--scale` (default 1.049) and writes `choochoomug-14oz.step` and `.stl`.
2. `make_mold_parts.py`: the dimensions and the profile, stadium and path builders. Writes `body`, `body_positive` and `handle_positive` (about 40 seconds). Checks:
   - the body matches the STEP by point sampling
   - the handle matches the STEP by sections at six angles (point sampling gives false insides near Fusion's B-spline crown)
   - it reports the reservoir volume
3. `make_masters.py`: imports those builders and makes the hollow masters (`--margin 25`, `--side 42`, `--plate 6`), the keys, the body end cap and the handle cottle. Writes `body_master`, `body_cap`, `handle_master`, `handle_cottle`, `handle_lock`, `plug_floor`, `plug_ring`, `plug_lock` and the two plug test parts (about 12 seconds). Checks:
   - each master is one valid solid
   - no key is within 3 mm of the cavity
   - the skin probes pass
   - the skin rims reach the cottle walls
   - body pair: each back pin sits in the other print's socket, the backs touch at the rim, and the two prints do not overlap (a deliberate 0.5 mm interference reads 1,249 mm³ and a 0.6 mm sideways shift 18 mm³, so the check is live)
   - it prints the plywood box size, the floor groove, and the plaster per pour
   - handle walls and locks do not overlap, close at the corners and the end-wall joints, and each lock's lips sit behind both rail heads
   - plug mold: ring halves, plug, floor and locks do not overlap; the ring closes at the wall, seat, disc edge and rails, and the locks capture both rail heads; the ring stands 0.5 mm off the table; the flipped plug sits on the floor's pit and clears its socket by 0.25 mm

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
| Plug ring ×2, test ring ×2 | 0.2 mm | Skirt down, as exported; the seat and V-ridge are 45° |
| Body end caps ×2 | 0.2 mm | Flat on the bed |
| Handle U-walls ×2, handle locks ×2, plug locks ×2 | 0.2 mm | On their table edge or end as exported. The locks slide over the rails with 0.15 mm per side |

All parts: at least 3 wall loops at 0.4 mm, so every 1.2 mm skin prints as solid perimeters (the parts are already hollow; infill only fills the thicker rails, locks and ledges). Elephant-foot compensation about 0.15 mm. Import as-is: no rotation, no "place on face".

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
- **The foot insert has a groove** and is cast in a split ring on a floor disc. The ring halves have fins clamped by short clips (the same clips as the walls), and the ring carries the disc on an inward flange, so the insert form stands as one unit.
- **A collar on the rim** casts a reservoir into the plaster.
- **One master, cast twice** for each mold, made possible by symmetry. Moving the handle off the body gives us the same thing.
- **Handle mold demolding:** the maker flexes the printed mold away from the set plaster. Release agent on the printed surface.
- **Plaster:** about 1350 mL per tumbler side and 180 mL for the insert, close to our 1.36 L and 150 mL.

## Pour and assembly (planned, not yet run)

1. Print two body masters and two body end caps; the handle master, two handle U-walls and two locks; the plug floor, two plug rings and two plug locks (two plug test rings and test locks first).
2. Body halves, both at once: build the plywood box. `make_masters.py` prints the inside size (173 × 167 mm, fill to 189 mm) and the floor groove (12.3 mm wide, 10 mm deep, centred). Pin the two masters back to back and stand the pair in the groove. Set an end cap against each end so it touches both skins' rims, close the plywood long sides against the caps' edges, and clamp. Clamp the pair's top fences too. Seal the cap and groove joints with clay. Soap everything. Pour both sides together so the levels stay even, brushing the mug surfaces first, and strike flat at the fill line, below the fences. Once set, strip the plywood and caps, pull the pair apart at the backs, and release each master from its plaster.
3. Handle halves: lay the master on its back plate. Stand the two U-walls around it, pour cups against the plain side wall, and slide a lock down over the rails at each end. Seal, soap and pour as for the body, brushing plaster into the pour cups and around the handle first. Once set, slide the locks up, pull each wall straight off sideways, and lift the plaster off the master.
4. Plug: first close the two test rings on the floor disc and slide the test locks down over the rails. The halves must meet with no light between them, and the ring must clear the table all round. If the joints stay open, sand the disc's chamfer. Then set the floor disc pit-up on the table and close the two ring halves around it, so the seats sit on its chamfer and the skirts hang round its edge, clear of the table. Slide the locks down over the rails and check the halves meet along their whole length. Press the ring down onto the disc and run a clay coil round its bottom edge onto the table. The coil holds it down and seals the gap under it. Seal the rail joints with clay, soap, pour to the ring top, and strike flat. Once set, slide the locks up and part the ring halves off the plug.
5. Dry everything. Dry-fit the body mold: plug in the socket (the groove must seat), turn one half 180° and close on the keys, strap. Dry-fit the handle mold the same way.
6. Body: stand the mold on a flat surface and fill to the top of the collar. Top up as the level drops, drain at wall thickness, then cut the cast at the rim step when it releases.
7. Handle: stand the mold with the pour cups up, pour into one cup until slip shows in the other, and let it fill solid. Demold and cut the sprues to the body's curve.
8. At leather hard, score and slip the joints. Attach the handle over one body seam line, then fettle.

## Risks to watch

- The plug seam sits at the highest slip head. If it weeps, add a clay coil. If the groove does not seat, sand the plug's ridge or reprint the ring.
- The plug ring rests on its seat by its own weight (about 20 g for the pair) and the clay coil. The plaster's upward push on the V-ridge is small (about 0.1 N), but if the cast plug shows a fin at the foot ring, the ring lifted: weight the locks next time.
- Plug fit: it is 0.25 mm per side under the socket. If it rattles or slip weeps at the foot ring, reduce `PLUG_CLEAR`; if it still will not go in, measure it across and along the joint line to see whether the ring opened again.
- Body box seams: the caps butt against the skin rims and the plywood, and the plates stand in the floor groove. Plaster can seep at any of them; clay coils outside should hold it. Handle cottle seams: the U-walls butt at the end-wall rails, so seal them the same way.
- Body pair: pour both sides together. A head difference loads the pair sideways, and only the pins and the groove resist it. Check for bowing the first time.
- Body master size: 209 mm across the fences. Check it fits the bed before slicing.
- Upright print: the foot cone overhangs 51° from vertical. If it sags, reprint with slower outer walls, or fill the shelf with a 45° skirt and carve the plaster back.
- The foot ring is a knife edge by geometry (the underside rises 4.2 mm over 42 mm); trim and sponge it at leather hard.
- The handle's inner and outer faces now have 2° of draft (they had 0° for 5.8 mm next to the parting line). If it still drags, the next step is a TPU handle positive in a rigid PLA plate.
- Handle joint: cut sprues to fit by hand. If fitting by eye is unreliable, add a printed trimming template (not in scope yet; inbox it).
- Scope creep: if more than three next actions are active at once, cut back to the smallest version.

## Next action

- [ ] Print two body masters and two end caps. Check the back pins seat (0.15 mm clearance) and the pair sits flat back to back, then stand it in a test groove before building the full plywood box

## Log

### 2026-11-05

The first cast plug was too big to fit its socket, and the plug ring had not seated cleanly on the floor disc. The plug now has 0.25 mm per side of clearance in its socket. The ring's flange is gone: the ring hangs on its 45° seat, 0.5 mm off the table, so the locks close the joints fully even if the disc prints a little tall. Added `plug_ring_test`, the bottom of the ring, to check the fit on the disc before printing the full ring. Standardized every printed cottle joint on the handle's T-rails and slide-down locks: the plug ring's fins and clips are gone, `plug_clip` is replaced by `plug_lock` (and `plug_lock_test`), and the handle and plug share one builder. The handle cottle's geometry is unchanged. See Decisions.

### 2026-11-04

Added a 2° draft to the handle's inner and outer faces, as a drafted stadium swept the same way. It is full width at the parting plane, the flats lean in, and the end arcs stay tangent and still reach the same crown. The hollow is an exact 1.2 mm offset of it. The undrafted handle still matches the Fusion STEP exactly; probes confirm the lean. `handle_positive` and `handle_master` regenerated; nothing else changed. Not printed yet.

### 2026-11-03

New goal: pour many molds in one plaster session, so both halves of a mold pour together. For the body: print the master twice and pin the two back to back for the pour (a pin and a socket on each plate back, self-mating after the 180° turn). Added a fence on both plate edges (a groove in the plywood floor below, a clamp edge above the fill line) and flat printed end caps that close both halves' ends. Plywood replaces the U-halves and clips, so `body_cottle` and `body_clip` are removed. Keys now have 15 mm of plaster round them (new `--side 42`, was about 6.5 mm). Considered and rejected a single double-sided plate, because the second plaster half would hold it rigid and stop the skin peeling. The handle and plug are unchanged for now. Handle release is still the open problem; the next direction to try there is a TPU positive in a rigid PLA plate. Nothing printed or cast yet.

### 2026-10-30

Rebuilt the handle cottle like the Old Forge D-handle kit (from its 3MF): two identical U-walls, each a side wall plus half of both end walls, joined on the end walls by T-rails and slide-down C-channel locks. They replace the mid-length fins and clips, which the body and plug keep. `handle_clip` is replaced by `handle_lock`. The handle itself is unchanged. Nothing printed or cast yet.

### 2026-10-28

The plug ring had no way to come apart or be held closed. Compared it against the Old Forge foot insert (two ring halves with fins and short clips; the ring's flange carries a 5 mm base disc) and rebuilt ours that way: fins at both ends of each half, the cottle clip at 34 mm, a 2 mm flange under the floor disc, and a 45° seat on the disc's chamfered rim in place of the floor lip. The plug parts moved to `make_masters.py` to share the fins and clip, and now export as `*_PRINT.stl`. Also made exports fail loudly and pinned build123d/OCP in `requirements.txt`, after `body_master_PRINT.stl` silently did not appear on another machine.

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
