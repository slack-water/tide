---
title: clay tube die — caulk gun extruder
created: 2026-11-01
updated: 2026-11-02
folder: 40
type: project
status: active
importance: 3
tags: [making, ceramics, 3d-printing, build123d]
ai-assisted: true
schema-version: 1.0
---

# clay tube die

a 3d-printed die that drops into my caulk gun's endcap and extrudes a hollow clay tube: **35 mm OD / 29 mm ID** (3 mm wall).

## done when

- a printed die extrudes a continuous tube with no visible seam lines from the spider arms
- the wall comes out even all the way around

## fixed dimensions

| what | value |
|---|---|
| cap inside diameter | 60.5 mm (calipers) |
| cap end-wall opening | 37 mm |
| tube OD / ID | 35 / 29 mm |
| barrel fit | body at 50.5 mm OD, from fit rings (49.5 very loose, 51.5 slightly too big) |

## how it works

z = 0 is the exit face. it sits against the cap's end wall, and the rest of the die points upstream into the barrel.

- **flange** (58.4 mm OD × 4 mm, 0.8 mm chamfer on the bed-side edge): drops into the cap. clay pressure pushes it against the end wall, so it doesn't need clamping. it just has to be thinner than the gap between the barrel rim and the cap wall when the cap is screwed on.
- **body** (50.5 mm OD): reaches up into the barrel and holds the inlet.
- **inlet → flare**: the opening is 44.5 mm across with a chamfered rim. the outer wall then eases down to 35 mm along an S-curve (z 24 → 10).
- **spider**: 3 teardrop-section arms (z 26–50, 5 mm thick) hold the mandrel. the round nose at the top splits the clay. the long taper underneath ends in a 0.4 mm tip, which lets the clay re-knit and also prints without supports.
- **mandrel**: 29 mm cylinder through the land, flare, and spider, then a cone to a point at z 64 (it pokes 10 mm above the inlet). the arms join the full-diameter cylinder, not the cone.
- **land** (z 0–10): straight 35/29 annulus that sets the tube size.

the open area drops steadily from about 1400 mm² at the inlet, through about 800 mm² between the arms, to 302 mm² at the exit. it never widens again, so the clay is squeezed the whole way. that's what welds the three streams back together after the arms. the clay has 26 mm to re-knit between the arm tails and the exit.

## printing

print it upright with the exit face on the bed. no supports needed: the mandrel and the outer wall both start on the bed, the flare only narrows going down, and the arm undersides are a steep taper.

- the 37 mm opening gives the tube 1 mm of clearance per side past the cap wall
- slicer: 0.2 mm layers, 100% infill (or a modifier at 100% over z 24–52), 4+ walls. v5 at 0.28 mm / 15% grid would leave 5 mm arms hollow inside. at 100% the die is ~90 g of PETG

## files

- `make_die.py` — parametric build123d source. everything is a constant at the top
- `clay_tube_die.step` — CAD exchange
- `clay_tube_die.stl` — print file (gitignored, regenerate with the script)
- `fit_test.py` → `fit_flange.stl`, `fit_body.stl`: thin fit rings at the current flange and body ODs. print these before the full die

```bash
# reuses the build123d 0.13 venv from the mug project
../choochoomug-14oz/.venv/bin/python make_die.py
```

## log

- **v1 (2026-11-01)**: printed. the body (53.0 OD) just barely wouldn't enter the barrel. the flange (59.4 OD) needed thread leverage to seat in the cap and probably can't come out without breaking. likely cause: elephant's foot on the bed-side flange plus a tight cap bore. the exit ring looks right. the 3 mm wall may make fragile tubes, but that's fine for now: the plan is to fire them upright and hear how they ring when struck.
- **v2 (2026-11-01)**: body OD 53.0 → 51.5 (inlet 49 → 47.5), flange OD 59.4 → 58.4, added a 0.8 mm chamfer on the flange's bed edge. tube geometry unchanged. superseded before printing.
- **v3 (2026-11-01)**: calipers: barrel ID 50.5, cap ID 60.5. body OD → 49.5 (inlet 45.5), flange stays 58.4 (2.1 mm under the cap ID, since 1.1 mm was a press fit). tube geometry unchanged.
- **fit tests (2026-11-01)**: the 58.4 flange ring fits the cap well. the 49.5 body ring was very loose, so the caliper reading was probably off.
- **v4 (2026-11-01)**: body OD → 51.5 (inlet 47.5), same as v2. flange stays 58.4. tube geometry unchanged.
- **v5 (2026-11-01)**: the 51.5 fit ring was slightly too big. body OD → 50.5 (inlet 46.5), splitting the difference. fit ring confirmed good. printing the full die.
- **v5 extrusion test (2026-11-01)**: failed. stiff clay. all three arms tore off the outer wall and bent nearly 90° at the mandrel joint, and the mandrel came out with the clay. rough load: 0.5–1 MPa barrel pressure on the mandrel's ~660 mm² projected area, so 300–700 N on the spider. the arms were 3 mm thick with a 14 mm chord, mostly thin taper, rooted on the thin part of the cone. tearing at both roots means the arms failed in bending.
- **v6 (2026-11-01)**: stronger spider, tube geometry unchanged. arm chord 14 → 24 mm (z 26–50), `ARM_W` 3 → 5 mm, mandrel stays a full 29 mm cylinder through the arms (cone starts at z 48, tip at z 64). arm span drops from ~14 to 8.75 mm. roughly 8× stronger in bending. `BODY_H` 42 → 54, so the die takes ~12 mm more of the barrel. still 3 arms (each one is a seam), and the arm tails stay at z 26, so the clay still has 26 mm to re-knit. `WALL` 2 → 3 mm (inlet 46.5 → 44.5), because the v5 arms tore off a 2 mm wall. v5 was PETG at 0.28 mm layers, 15% grid infill. PETG explains the bending instead of snapping. next test: slightly softer clay.
- **v5 printed (2026-11-02)**: 100% infill. extrudes clean tubes with slightly softer clay, but they curve to one side as they leave the nozzle. not yet known if it's the die (off-center mandrel), the feed (tilted seat, uneven slug), or gravity sag. next: rotate the die in the cap and check whether the curve follows it, and caliper the wall around a cut slice.

## open questions

- [ ] why do the tubes curve? rotation test + wall-thickness check. if the mandrel is off-center: tape on the fast side as a test, then v6 with `ARM_W` 4. keep `LAND` at 10: a longer land roughly doubles its share of the extrusion force
- [ ] extruding takes a hard crank on the 18:1 gun. at 0.5 MPa the ~2000 mm² plunger already needs ~1000 N, so this is mostly physics. free fixes first: oil the barrel, land and mandrel; load half-barrel slugs; sand the land (the layer lines run across the flow). for v6, a 4 mm wall cuts the land's share of the force by about a quarter and makes stronger tubes. if it's still hard, a cordless caulk gun beats a 26:1 (only ~44% more force, more pumps), since steady flow also helps straightness. any new gun has to take the 50.5 mm barrel and 60.5 mm cap, or the die needs a new fit
- [ ] measure the gap between the barrel rim and the cap wall with the cap screwed on. `FLANGE_T` (4 mm) has to fit in it
- [ ] the arm roots aren't filleted: OCC wouldn't fillet those junctions at any radius tried. if v6 cracks there, the next steps are 4 arms, then a steel cross-pin through the arms and mandrel
