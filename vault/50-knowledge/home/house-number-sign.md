---
title: House Number Sign — Bulbs and Troubleshooting
created: 2026-11-16
updated: 2026-11-16
folder: 50
type: reference
status: active
importance: 2
tags: [home, electrical, low-voltage, maintenance]
schema-version: 1.0
ai-assisted: true
---

# House Number Sign

*the lit house number sign above the garage door. how it's powered, what bulb it takes, and how to find the fault when it goes dark.*

---

## the setup

- two small incandescent bulbs, probably wired in series. one dead bulb takes out both.
- powered by a small transformer, doorbell style. it read **18.3V AC** with no load. that drops toward ~16V once the bulbs are drawing current, which is normal.
- bulb: **193**, a miniature wedge base, T3-1/4 size. about 14V, 0.33A, ~4.6W.

---

## buying replacements

- **exact match:** 193. it's often listed as "12V". that's the car-electrical nominal and it's the same part.
- **fine substitute:** 194. same base and voltage, a bit less current (~3.8W).
- **where:** auto parts stores (sold as dash and license-plate bulbs; ask for it by number), the specialty bulb aisle at a hardware store, or amazon ("193 miniature wedge bulb").
- **replace both at once.** the surviving bulb has the same hours on it.
- bring the old bulb if buying in person.

### don't buy

- **"wedge landscape incandescent" bulbs.** these are the larger T5 size, 5–18W. same wedge base style, so they look interchangeable in a listing, but they aren't. an 18W one draws ~1.5A, so two would pull ~3A. a doorbell transformer (10–20VA) only supplies ~0.6–1.2A, so that risks killing it. the bulbs also put a lot of heat into a small enclosure.
- **921**: 12V, 18W. same problem.
- **LED wedge bulbs**, unless they're labeled **AC/DC / non-polarized** and rated for this voltage. most LED wedges are DC-only and polarity-sensitive. on this transformer's AC they flicker, glow dim, or don't light.
- rule of thumb: the sign was designed for low-wattage bulbs. keep each one at **≤ ~5W**. check that the listing says "193" or "T3-1/4" and is around 4–5W. ignore "18W equivalent" LED claims.

---

## troubleshooting: sign is dark

1. power off. pull both bulbs.
2. look first. a broken filament is often visible.
3. meter each bulb on the **200 Ω range** (the Ω symbol, not 200k or 2M). probes go on the two metal end contacts.
   - **a few ohms** (one read 4.1 Ω): filament is intact. a cold filament reads much lower than a hot one, so this is normal.
   - **"1" on the left of the display**: open circuit. the bulb is burnt.
   - continuity (beep) mode works too: beep is good, silence is burnt.
4. if one bulb is open, replace it (and the other one with it).
5. if both bulbs read good, the fault is in the sockets. clean off any corrosion, check for loose contacts, and make sure the bulbs seat firmly.

---

## log

- **2026-11-16**: sign went dark. one bulb read 4.1 Ω (good). the other was visibly broken. identified it as a 193. found that the "12V 18W wedge landscape" listings were the wrong bulb.
