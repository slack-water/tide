# Ubiquitous Language

Shape-agnostic vocabulary for `stl_add_draft.py`, so its capabilities can be described (and reused) for any part, not just the skull. "Skull" appears only as the first worked example, never in a term.

## Geometry of a pull

| Term | Definition | Aliases to avoid |
| --- | --- | --- |
| **Part** | The scanned or modeled solid being processed. Any watertight mesh works. | Object, model, skull (as a generic term) |
| **Parting plane** | The flat face of the **part** where a mold splits, and which stays open/flush through every operation. | Cut face, flat face, midline, rim face |
| **Pull axis** | The axis along which the **part** is withdrawn from (or pressed into) a mold. | Draft axis, mold direction, up |
| **Base** | The end of the **pull axis** where the **parting plane** sits (`min` or `max`). | Bottom, floor, bed |
| **Tip** | The end of the **pull axis** farthest from the **parting plane**. | Top, apex |
| **Undercut** | Surface that curves back over itself along the **pull axis**, locking a mold in place. | Overhang (reserve for print supports), lock |
| **Draft angle** | The deliberate taper, as a percent grade, that widens the **part** toward the **parting plane** for easy release. | Taper, slope |
| **Crease** | A concave seam where two **draft cones** meet. It is real geometry, not aliasing. | Facet, artifact, seam |
| **Thin protrusion** | Convex material narrower than ~2 × `--teeth-radius`; the script's generic stand-in for features like teeth. | Teeth (skull-specific), spike |

## Operations (the script's commands)

| Term | Definition | Aliases to avoid |
| --- | --- | --- |
| **Draft** | The operation that fills **undercuts** and adds a **draft angle**, producing a **drafted solid**. | Undercut removal, draft-correct |
| **Drafted solid** | The undercut-free, tapered output of **draft**; the input to every other operation. | Draft file, corrected mesh |
| **Shell** | The operation that hollows a **drafted solid** into a constant-thickness wall, open at the **parting plane**. | Hollow, offset |
| **Core** | The operation that erodes a **drafted solid** inward by a fixed **inset**, keeping it solid and flush at the **parting plane**. | Plug (the physical object), inner offset |
| **Negative** | The operation that carves a **drafted solid** out of a **margin**-padded block, producing a printable mold cavity. | Inverse, mold (ambiguous) |
| **Mirror** | The operation that reflects a finished **part** across a plane to produce its counterpart. | Flip, reflect |
| **Brim** | The operation that fuses a rigid, ribbed, hole-punched **flange** onto a **part**'s **parting plane**. | Slicer brim, base plate |
| **Flange** | The flat plate the **brim** adds so a **part** can stand in a pour box; has a **footprint**. | Brim (as the object), plate |
| **Footprint** | The outline of the **flange**: `rim` (follows the part's cross-section) or `circle`. | Shape, outline |
| **Natch** | A hole through the **flange** that holds a registration key for the poured mold. | Corner hole, mounting hole |
| **Vent** | The open interior loop in a **shell**'s cross-section that the **brim** must leave unplugged. | Cavity mouth, hole |

## Resolution and tuning

| Term | Definition | Aliases to avoid |
| --- | --- | --- |
| **Pitch** | Voxel edge length in mm; coarser is faster, finer keeps detail. | Resolution, voxel size |
| **Scale** | Uniform enlargement about the origin, applied once at **draft** so the **parting plane** stays put. | Zoom, resize |
| **Blur** | Gaussian rounding of **creases** in the signed distance field before surfacing. | Smoothing (that is mesh-level, see below) |
| **Mesh smoothing** | Post-surfacing Taubin or Laplacian passes on vertices; distinct from **blur**. | Blur |
| **Thickness** | Wall depth of a **shell**, in mm of true nearest-surface distance. | Wall, offset |
| **Inset** | Inward distance a **core** moves from the **drafted solid**'s surface, in mm. | Thickness (reserve for **shell**) |
| **Margin** | Extra material beyond the **part**: wall around a **negative**, or reach of a **flange**. | Padding, clearance |

## Physical workflow

| Term | Definition | Aliases to avoid |
| --- | --- | --- |
| **Master** | A printed **part** (a **shell**, **core**, or solid) used to make a mold. | Positive, original |
| **Mold** | The cavity cast in plaster (or printed via **negative**) from a **master**. | Negative (when meaning the physical object) |
| **Pour box** | The cottleboard enclosure a **master** stands in on its **flange** while plaster is poured. | Cottle, box |
| **Press plug** | A **core** printed to press a clay sheet into a **mold**. | Core (when meaning the physical object) |
| **Print file** | An STL with the **parting plane** pre-rotated flat on the bed so the slicer needs no rotation. | `_PRINT` file, oriented file |

## Same idea in other fields

Associations to help transfer the operations to other shapes; none of these are script terms, and they are not yet confirmed as the user's own framing.

| Script term | Dental / orthodontic | Machining / moldmaking | Image processing / graphics |
| --- | --- | --- | --- |
| **Pull axis** | Path of insertion | Pull direction | Projection direction |
| **Undercut** | Undercut (found with a dental surveyor) | Undercut | Occluded region |
| **Draft** (filling undercuts) | Blocking out a model with wax | Undercut elimination | Directional sweep, shadow volume or extrusion |
| **Draft angle** | Taper / convergence angle of a crown prep | Draft angle | Flared sweep |
| **Blur** (rounding creases) | Smoothing the wax block-out | Fillet | Gaussian smoothing of a distance field |
| **Core** | Reduction of a tooth for a crown | Inset / offset cut | Erosion |
| **Shell** | Thin appliance wall, as in an aligner | Hollowing / wall offset | Erosion difference |
| **Thin protrusion** test | Single cusp or tooth tip | Thin rib or boss | Morphological opening |
| **Parting plane** | Midline or cut base of the model | Parting line | Cut plane |

## Relationships

- A **Part** has exactly one **parting plane** and one **pull axis**; **base** and **tip** are its two ends.
- A **Drafted solid** is produced from one **Part** by **draft**, at one **scale**, **pitch** and **draft angle**.
- **Shell**, **core**, **negative** and **brim** each take a **drafted solid** (**brim** also accepts a **shell**) and must use the same **pull axis** and **base** as the **draft** that made it.
- **Shell** and **core** differ only in what they keep: **shell** keeps the outer rind of **thickness**; **core** keeps everything deeper than **inset**.
- A **Mold** is cast from the outer surface of a **Master**; a **Press plug**'s surface sits **inset** inside that **Mold**, leaving a clay-thick gap.
- A **Brim** adds one **flange** with zero or more **natches** and preserves one **vent** if the **part** has one.
- **Mirror** acts on any finished output and yields its counterpart; run **brim** before **mirror** so **natch** positions match.

## Example dialogue

> **Dev:** "I have a new **part**, a hollow bowl. Do I run **shell** first?"
> **Domain expert:** "First pick the **pull axis** and **base**, then run **draft** to get a **drafted solid**. Only that can be fed to **shell**, **core** or **negative**."
> **Dev:** "And if I already have a plaster **mold** of the bowl and want to press clay into it?"
> **Domain expert:** "Run **core** on the same **drafted solid** with an **inset** equal to the clay thickness. That prints the **press plug**, and its **tip** stays that far inside the **mold**."
> **Dev:** "Does **blur** matter there?"
> **Domain expert:** "Slightly. Erosion sharpens **creases**, so a small **blur** on the **core** helps. **Mesh smoothing** is a separate pass on the vertices."
> **Dev:** "Last question: I need a left and right of the bowl, with a **flange** for the **pour box**."
> **Domain expert:** "Run **brim** on the left half first, then **mirror** it, so the **natches** land in matching positions."

## Flagged ambiguities

- **"negative"** names both the script's **negative** operation and any physical mold. Use **Negative** only for the operation; call the physical object a **mold**.
- **"core"** and **"plug"**: **Core** is the operation and its geometry; **press plug** is the physical print. Do not say "plug" for the geometry.
- **"brim"** is a slicer adhesion skirt elsewhere, but here it is a rigid part. Say **brim** for the operation and **flange** for the object; say "slicer brim" for the other one.
- **"shell"** is also the mother-mold shell in casting. Here it only means the hollow-wall operation or its output; call the plaster mother mold a **mold**.
- **"thickness"** appears on **shell** (wall), **brim** (flange plate) and informally for clay. Use **thickness** for **shell** walls, **inset** for **core**, and "flange thickness" explicitly for **brim**.
- **"margin"** means wall around a **negative** and reach of a **brim** flange. Always say which: "negative margin" or "flange margin".
- **"blur"** vs smoothing: **blur** is field-level and **mesh smoothing** is vertex-level; the CLI uses `--blur` and `--smooth`, and the docs should keep them apart.
- **"base"** means the **parting plane** end of the **pull axis**, not the print bed, though a **print file** puts them together. Say "bed" for the printer.
- **"teeth"** and **"left/right half"** are skull-specific. Use **thin protrusion** and **part** / **counterpart** when describing the script generally. Keep `--teeth-blur` and `--teeth-radius` as flag names only.
- **"draft"** is a verb (the operation), a number (the **draft angle**) and a file (the **drafted solid**). Pick the matching term each time.
