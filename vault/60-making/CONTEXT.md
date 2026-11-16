---
title: Making Language (Mold Making, Slip Casting, 3D Printing)
created: 2026-11-08
updated: 2026-11-09
folder: 60
type: reference
status: active
schema-version: 1.0
ai-assisted: true
---

# Making Language

The shared vocabulary for the plaster mold, slip casting, CAD and 3D printing projects, so one word means one thing across them. It replaces the project-level vocabulary lists where they disagree.

## Language

### Mold pieces

**Mold piece**:
One separable plaster section of a mold, such as a side half or a foot insert.
_Avoid_: Plaster cast, cast (for plaster)

**Working face**:
A plaster surface whose shape matters on the finished mold piece.

**Pattern**:
A printed object with at least one surface that forms a working face.
_Avoid_: Master

**Foot insert**:
The separate plaster mold piece that forms a recessed foot and seats between the side halves.
_Avoid_: Plug, foot plug, base piece

**Natch**:
A mating pair of features that registers two mold pieces when they close, whether molded into the plaster or made with hardware.
_Avoid_: Key, registration key

**Boss**:
The convex half of a natch, always named with the object it is on: printed boss, plaster boss.

**Dimple**:
The concave half of a natch, always named with the object it is on: drilled dimple, plaster dimple.

**Cottle**:
The walls that hold liquid plaster around a pattern, printed or made of boards, and form no working face.
_Avoid_: Pour box, box

**Pattern plate**:
The printed plate a pattern is built on, whose flat surface forms a parting face.
_Avoid_: Back plate, plate, flange

**Parting board**:
A separate flat sheet that a pattern stands on and that forms a parting face.
_Avoid_: Follow board

### Mold chain

**Working mold**:
The plaster mold that forms clay in production: a casting, jigger or press mold.
_Avoid_: Mother mold, production mold

**Block mold**:
The first mold made from a finished model, used to make check casts before any case mold exists.
_Avoid_: Mother mold

**Case mold**:
A form made from a block mold that serves as the die for making working molds.
_Avoid_: Mother mold

### Parting

**Parting line**:
Where the division between mold pieces runs on a form.

**Parting plane**:
The flat geometric plane on which a form is divided in CAD.

**Parting face**:
The flat mating surface on a set plaster mold piece.
_Avoid_: Parting plane (for the physical surface)

**Seam**:
The mark a parting line leaves on a cast.
_Avoid_: Parting line (on a cast), seam (for a Z seam, cottle joint or mold joint)

**Mold joint**:
Where closed mold pieces meet, and where slip can weep.
_Avoid_: Seam, plug seam

**Cottle joint**:
Where two parts of a cottle, or a cottle and a pattern, meet and can leak plaster.
_Avoid_: Seam, box seam

### Process

**Pour**:
To fill with a liquid, either plaster into a cottle or slip into a mold.

**Cast**:
As a noun, the clay object formed in a mold. Plaster objects are never casts.

### Form geometry

**Model**:
The original form of the object being made.
_Avoid_: Mold cavity, part

**Positive**:
The CAD solid of a model plus its pouring features and any insert socket, from which a pattern is made.
_Avoid_: Master

**Cavity**:
The void inside a closed mold, where a cast forms.
_Avoid_: Cavity (for a solid)

**Undercut**:
A surface that blocks a form's release along the pull direction.
_Avoid_: Overhang

**Fin**:
A thin ridge formed where two sections of a mold or cottle meet.
_Avoid_: Flash

**Draft angle**:
The taper, in degrees from the pull direction, that lets a form release from a mold.
_Avoid_: Taper, slope

**Draft grade**:
The same taper as a percentage (rise over run), used only as the value of the draft script's flag.
_Avoid_: Draft angle (for a percentage)

**Shell**:
The CAD operation that hollows a solid to a constant-thickness wall.
_Avoid_: Shell (for the printed object)

### Printing

**Skin**:
The thin printed wall of a pattern that forms a working face.
_Avoid_: Shell

**Wall loop**:
One extruded outline of a layer in the slicer's sense.
_Avoid_: Perimeter, line, pass, wall (bare)

**Z seam**:
The line on a print where each layer's outline starts and ends.
_Avoid_: Seam (bare)

**Cottle wall**:
A wall of a cottle.
_Avoid_: Wall (bare)

**Cast wall**:
The thickness of clay in a cast.
_Avoid_: Wall (bare), mug wall

**Brim**:
The slicer's single-layer adhesion extension attached to a print's first layer.
_Avoid_: Brim (for a printed plate), flange

**Skirt**:
The slicer's loop drawn around a print to prime the nozzle.
_Avoid_: Skirt (for a modeled feature)

**Apron**:
The part of a foot insert's printed ring that hangs round the edge of its floor disc.
_Avoid_: Skirt

**Overhang**:
A printed surface that leans out past the layer below it.
_Avoid_: Undercut

**Bed**:
The printer's build surface.
_Avoid_: Table, base

**Table**:
The surface a pour is set up on.
_Avoid_: Bed

## References

When sources disagree, the higher one wins. Practitioner sources are used only where nothing above them covers a term.

1. **United States Gypsum Company, _Plasters and Gypsum Cements: Plasters for the Ceramic Industry_, IG526, rev. 4-03 (2003).** Settles block mold, case mold and working mold. Read in full via a [third-party copy](https://www.manualsdir.com/manuals/574730/usg-plasters-and-gypsum-cements-for-the-ceramic-industry.html). It has no entry for natch, parting line, seam, draft, cottle or mother mold.
2. **War Department, _Engineer Foundry_, TM 5-228 (6 September 1944).** Settles pattern, parting line, parting, draft and fin for general casting. Read in full via [GovInfo](https://www.govinfo.gov/content/pkg/GOVPUB-W-9fd04bd8192827eb4545f45c1f781f86/html/GOVPUB-W-9fd04bd8192827eb4545f45c1f781f86.htm). It is a metal-foundry source, so it yields to USG on ceramics.
3. **[US Patent 4,252,295, "Natch for multi-part mold"](https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/4252295).** Supports natch as the alignment feature between mating mold parts. Only an excerpt has been read.
4. **[ISO/ASTM 52900:2021](https://committee.iso.org/standard/74514.html), _Additive manufacturing: General principles, Fundamentals and vocabulary_.** The authority for general printing terms. Paywalled and not yet read, so no term here rests on it.
5. **[Bambu Studio wiki](https://wiki.bambulab.com/en/bambu-studio/parameter).** The vendor's names for slicer parameters. Only search excerpts have been read, because the wiki refuses automated fetches.

Practitioner sources, lowest priority: [Holst Porzellan](https://holst-porzellan.com/b2c/en/knowledge/forming/mould-making/), [Ceramics Monthly](https://ceramicartsnetwork.org/ceramics-monthly/ceramics-monthly-article/An-Exercise-in-Logic-and-Form-131604), [Artmolds](https://www.artmolds.com/block-mold-injection/) and, last, [Digitalfire](https://digitalfire.com/project/59), whose use of block mold and case mold conflicts with USG.

House terms with no source above: cottle, foot insert, working face, parting face, parting board, pattern plate, positive, skin and apron.
