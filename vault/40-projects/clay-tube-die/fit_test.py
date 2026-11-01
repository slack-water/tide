"""quick fit coupons. sizes come straight from make_die.py, so they always
match the current die.

  fit_flange.stl  4 mm flange ring: does it pass the cap threads and seat
                  against the end wall?
  fit_body.stl    5 mm ring at the body OD: does it slide into the barrel?

both print flat. their bed edges are chamfered, so elephant's foot doesn't
make them read tighter than the real die (in the die, the body never touches
the bed).
"""
from pathlib import Path

from build123d import Cylinder, Pos, chamfer, export_stl

import make_die as d


def ring(od: float, h: float, wall: float = 2.5):
    r = Pos(0, 0, h / 2) * (Cylinder(od / 2, h) - Cylinder(od / 2 - wall, h))
    bed = r.edges().filter_by(lambda e: e.center().Z < 0.01 and e.radius > od / 2 - 0.01)
    return chamfer(bed, d.FLANGE_CHAMFER)


if __name__ == "__main__":
    out = Path(__file__).parent
    for name, part in (("fit_flange", ring(d.FLANGE_OD, d.FLANGE_T)),
                       ("fit_body", ring(d.BODY_OD, 5.0))):
        if not part.is_valid:
            raise SystemExit(f"{name} invalid")
        if not export_stl(part, out / f"{name}.stl"):
            raise SystemExit(f"{name} export failed")
        bb = part.bounding_box().size
        print(f"{name}: {bb.X:.1f} OD × {bb.Z:.1f} tall")
