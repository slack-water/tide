---
title: Hydroponic Herb Garden
created: 2026-05-31
updated: 2026-05-31
folder: 40
type: project
status: active
importance: 3
goal: NFT hydroponic herb garden in the backyard, starting with a single-channel MVP
scope: build, iterate, expand
tags: [making, hydroponics, 3d-printing, backyard]
related: []
schema-version: 1.0
---

## Goal

A backyard NFT (Nutrient Film Technique) herb garden. Start with one channel, prove the system works, then expand to a full multi-channel structure.

## Scope

**In:** single channel MVP → multi-channel frame → eventually solar-powered with ESP32 monitoring
**Out:** fully automated, grow lights (find a better sun spot instead)

## Done looks like

Water flowing through a 2"×3" downspout channel, draining back to a 5-gal bucket, herbs growing in net pot sites, pump cycling on wifi timer. No leaks. Plants happy after 48h.

## Next action

- [ ] Find placement spot with 6+ hrs direct sun
- [ ] Print end caps + legs, verify fit on downspout before buying anything
- [ ] Home Depot run: downspout + vinyl tubing + sheet metal screws
- [ ] Pet store: AC aquarium pump (Aqueon/Fluval 150–250 GPH) + API pH test kit
- [ ] Nursery: LECA/clay pebbles + liquid nutrients (Fox Farm Grow Big or GH FloraGrow)

---

## Design

### Method: NFT (Nutrient Film Technique)

A thin film of nutrient solution flows continuously through angled channels. Roots dangle into the film. Excellent for herbs — basil, mint, cilantro, thyme, rosemary all thrive. Small pump, low water volume.

### Aesthetic: 2"×3" aluminum downspout + brown PETG

The channels and eventual frame are all made from standard rectangular aluminum downspout from Home Depot. Brown PETG printed brackets, end caps, and fittings tie it together. Clean, monolithic, looks intentional — not improvised.

---

## MVP Architecture

```
           [inlet barb] ← tubing from pump
                ↓
[net pot]  [net pot]  [net pot]  [net pot]    ← 4 sites
 ────────────────────────────────────────── ← 2×3 downspout, angled ~2–3°
                                       ↓
                                  [drain barb]
                                       ↓ tubing
                               [5-gal bucket]
                                       ↑
                           [pump → wifi timer → AC]
```

**Pump schedule:** run continuously for first 2 weeks while roots establish. Then 15 min ON / 5 min OFF. Don't go longer than 10–15 min off — NFT roots dry fast.

---

## 3D printed parts (brown PETG — on hand)

| Part | Notes |
|---|---|
| End cap — inlet (×1) | 2"×3" downspout fit; barb fitting in top face for pump tubing |
| End cap — drain (×1) | 2"×3" downspout fit; barb fitting in bottom face for gravity drain |
| Angle legs / feet (×2) | Different heights to create 2–3° slope; snap onto downspout ends |
| Net pot inserts (×4) | Press into 2" holes; hold solo cups or printed cups |
| Bucket lid pass-through (×1) | Pump cord + return tube through 5-gal bucket lid |

**Net cups:** solo cups with holes cut works fine for MVP. Print proper cups or buy 2" commercial ones later.

---

## BOM

### Home Depot (~$30)

| Item | Qty | Est. |
|---|---|---|
| 2"×3" aluminum downspout 10ft | 1 | ~$12 |
| ½" ID clear vinyl tubing 10ft | 1 | ~$10 |
| #8 × ¾" sheet metal screws | 1 small box | ~$5 |

### Local pet store — PetSmart / PetCo (~$30–35)

| Item | Notes | Est. |
|---|---|---|
| AC submersible pump | Aqueon or Fluval powerhead, 150–250 GPH; plugs straight into wifi timer | ~$20–25 |
| pH test kit | API Master Test Kit | ~$10 |

### Local nursery (~$25)

| Item | Notes | Est. |
|---|---|---|
| LECA / clay pebbles | Growing medium for net cups | ~$12 |
| Liquid nutrients | Fox Farm Grow Big or GH FloraGrow | ~$12–15 |

### Amazon (only if not found locally)

| Item | Notes | Est. |
|---|---|---|
| 2" net cups (50 pack) | Skip if using solo cups | ~$8 |
| GH Flora 3-part kit | If nursery doesn't carry nutrients | ~$25 |

---

## Build order

1. Find placement spot with 6+ hrs direct sun (south- or west-facing)
2. Print end caps + legs — verify fit on actual downspout before cutting anything
3. Cut 4 net pot holes in downspout top face (2" hole saw or step bit)
4. Press in net pot inserts, attach end caps
5. Home Depot + pet store + nursery runs
6. Set up bucket, print lid pass-through, connect tubing
7. Fill with plain water and run pump — verify flow and no leaks before adding nutrients
8. Mix nutrient solution to ~800 ppm, pH to 5.5–6.5, plant herbs in LECA

---

## Expand later

| Phase | What gets added |
|---|---|
| More channels | Add 2–3 more channels alongside the first |
| Full frame | Build the all-downspout ladder frame with printed corner brackets |
| Solar | 20W panel, MPPT controller, LiFePO4 battery — replace wall adapter |
| ESP32 controller | Timed relay, water temp (DS18B20), TDS sensor, web dashboard |

---

## Log

### 2026-05-31

Initial design. Settled on single-channel MVP using 2"×3" aluminum downspout, brown PETG printed parts, AC aquarium pump, existing wifi timer and 5-gal bucket. Print end caps first, source materials locally before ordering anything.

Key constraint: placement needs 6+ hrs direct sun — the shelving unit in partial shade doesn't qualify.
