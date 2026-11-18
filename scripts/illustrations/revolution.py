"""Part IV — revolution."""

from __future__ import annotations

import math

from .kit import (
    EIFFEL,
    FAINT,
    PAPER,
    Pt,
    arc,
    dim_v,
    ground,
    hatch,
    line,
    note,
    path,
    poly,
    rect,
    reference,
    tone,
    write,
)  # fmt: skip


def tatlin() -> None:
    """Tatlin's tower: two helices on a leaning cone, braced by one straight spine."""
    gy, s, bx = 432.0, 0.85, 392.0
    hgt = 400 * s
    lean = math.radians(23.5)
    flat = 0.34  # how far each ring opens toward the viewer

    def rad(t: float) -> float:
        return 104 * (1 - t) ** 1.12 + 2

    def at(t: float, phi: float) -> Pt:
        r = rad(t)
        x = bx - t * hgt * math.tan(lean) + r * math.cos(phi)
        y = gy - t * hgt - r * flat * (1 + math.sin(phi))
        return (x, y)

    b = [ground(gy)]
    apex = at(1, 0)
    b.append(line(bx, gy, apex[0], apex[1] - 3, 0.5, FAINT, dash="5 4"))

    # straight members: the cone's generators, far side first
    gens = [math.tau * j / 10 for j in range(10)]
    for front in (False, True):
        for phi in gens:
            if (math.sin(phi) < 0) != front:
                continue
            b.append(
                line(
                    *at(0, phi),
                    *at(0.94, phi),
                    0.55 if front else 0.35,
                    o=1 if front else 0.5,
                )
            )
        if not front:
            # the far half of each helix
            for phase in (0.0, math.pi):
                b.append(_helix(at, phase, front=False))
            b.append(_volumes(at, rad, bx, gy, hgt, lean, flat))
    for t in (0.0, 0.3, 0.56, 0.78):
        b.append(poly([at(t, math.tau * i / 48) for i in range(48)], 0.45, o=0.75))
    for phase in (0.0, math.pi):
        b.append(_helix(at, phase, front=True))

    # the spine: a lattice girder up the steep side
    foot = (bx + 116, gy)
    dx, dy = apex[0] - foot[0], apex[1] - 14 - foot[1]
    ln = math.hypot(dx, dy)
    ux, uy, px, py = dx / ln, dy / ln, -dy / ln * 3.5, dx / ln * 3.5
    for sgn in (-1, 1):
        b.append(
            line(
                foot[0] + sgn * px,
                foot[1] + sgn * py,
                foot[0] + dx + sgn * px,
                foot[1] + dy + sgn * py,
                1.1,
            )
        )
    zig = []
    for i in range(int(ln / 9) + 1):
        sgn = 1 if i % 2 else -1
        zig.append((foot[0] + ux * i * 9 + sgn * px, foot[1] + uy * i * 9 + sgn * py))
    b.append(poly(zig, 0.45, close=False))

    b.append(reference(602, gy, s, EIFFEL, "Eiffel Tower", "330 m"))
    b.append(
        path(
            f"M{602 - 38 * s},{gy}A{38 * s},{44 * s} 0 0 1 {602 + 38 * s},{gy}",
            0.6,
            c=FAINT,
        )
    )
    for z in (57, 115, 276):
        hwz = {57: 34, 115: 17.5, 276: 4.4}[z] * s
        b.append(line(602 - hwz, gy - z * s, 602 + hwz, gy - z * s, 0.5, FAINT))
    b.append(dim_v(532, gy - hgt - 14, gy, "400 m"))
    b.append(note(52, 110, "Hemisphere: radio", at(0.83, math.pi)))
    b.append(note(52, 170, "Cylinder: press, a turn a day", at(0.62, math.pi)))
    b.append(
        note(52, 250, "Pyramid: executive, a turn a month", at(0.43, math.pi * 0.9))
    )
    b.append(note(52, 340, "Cube: legislature, a turn a year", at(0.14, math.pi * 0.9)))
    b.append(
        note(
            52,
            404,
            "Axis leans 23.5°, as the Earth does",
            (bx - 0.07 * hgt * math.tan(lean), gy - 0.07 * hgt),
        )
    )
    write(
        "tatlin",
        "Monument to the Third International — Tatlin, 1919",
        "elevation",
        "",
        "".join(b),
    )


def _helix(at, phase: float, front: bool) -> str:
    """One helix, drawn as runs that are all on the near (or all on the far) side."""
    out, run = "", []
    steps = 360
    for i in range(steps + 1):
        t = 0.97 * i / steps
        phi = phase + math.tau * 3.2 * t
        if (math.sin(phi) < 0) == front:
            run.append(at(t, phi))
        elif run:
            out += poly(run, 1.7 if front else 0.8, close=False, o=1 if front else 0.5)
            run = []
    if run:
        out += poly(run, 1.7 if front else 0.8, close=False, o=1 if front else 0.5)
    return out


def _volumes(
    at, rad, bx: float, gy: float, hgt: float, lean: float, flat: float
) -> str:
    """The four suspended chambers, stacked along the leaning axis."""

    def centre(t: float) -> Pt:
        return (bx - t * hgt * math.tan(lean), gy - t * hgt - rad(t) * flat)

    out = ""
    x, y = centre(0.14)
    cube = [(x - 27, y - 27), (x + 27, y - 27), (x + 27, y + 27), (x - 27, y + 27)]
    lid = [(x - 27, y - 27), (x - 17, y - 36), (x + 37, y - 36), (x + 27, y - 27)]
    side = [(x + 27, y - 27), (x + 37, y - 36), (x + 37, y + 18), (x + 27, y + 27)]
    out += poly(cube, 1.0, PAPER) + poly(lid, 1.0, PAPER) + poly(side, 1.0, PAPER)
    out += hatch(side, 2.6, 62, o=0.5) + tone(cube, 0.08)
    x, y = centre(0.42)
    pyr = [(x - 24, y + 22), (x + 24, y + 22), (x, y - 30)]
    out += poly(pyr, 1.0, PAPER) + hatch(
        [(x + 5, y + 22), (x + 24, y + 22), (x, y - 30)], 2.6, 62, o=0.5
    )
    out += line(x + 5, y + 22, x, y - 30, 0.6)
    x, y = centre(0.62)
    out += rect(x - 13, y - 15, 26, 30, 0, PAPER)
    out += poly(
        arc(x, y + 15, 13, 4, 180, 360, 10) + arc(x, y - 15, 13, 4, 0, 180, 10),
        1.0,
        PAPER,
    )
    out += poly(arc(x, y - 15, 13, 4, 180, 360, 10), 0.8, close=False)
    out += hatch(
        [(x + 4, y - 15), (x + 13, y - 15), (x + 13, y + 15), (x + 4, y + 15)],
        2.6,
        62,
        o=0.5,
    )
    x, y = centre(0.8)
    out += poly(arc(x, y + 5, 8, 9, 0, 180, 10), 1.0, PAPER)
    return out


def _setback(cx: float, gy: float, tiers: list[Pt], k: float = 1.0) -> str:
    """A Ferriss tower: stacked masses, piered, darkening as they rise."""
    out, base = "", gy
    for i, (hw, h) in enumerate(tiers):
        hw, top = hw * k, gy - h * k
        mass = [(cx - hw, top), (cx + hw, top), (cx + hw, base), (cx - hw, base)]
        out += poly(mass, 1.2, PAPER) + tone(mass, 0.05 + 0.055 * i)
        out += hatch(
            [
                (cx + hw * 0.55, top),
                (cx + hw, top),
                (cx + hw, base),
                (cx + hw * 0.55, base),
            ],
            2.6,
            90,
            o=0.5,
        )
        piers = int(hw / 3.2)
        for j in range(-piers, piers + 1):
            out += line(cx + j * 3.2, top + 2, cx + j * 3.2, base, 0.3, o=0.55)
        # shoulders: lower blocks buttressing each mass
        if i < len(tiers) - 1:
            for sx in (-1, 1):
                sh = (base - top) * 0.5
                x0 = cx + sx * hw
                out += poly(
                    [
                        (x0, base - sh),
                        (x0 + sx * 7 * k, base - sh),
                        (x0 + sx * 7 * k, base),
                        (x0, base),
                    ],
                    0.9,
                    PAPER,
                )
        base = top
    return out


def ferriss() -> None:
    """Ferriss's zoned city: setback masses lit from the street, tops lost in dusk."""
    gy, s = 432.0, 0.86
    b = []
    for x0 in (300.0, 420.0):
        for spread in (-34, 30):
            b.append(
                tone(
                    [
                        (x0 - 3, gy),
                        (x0 + 3, gy),
                        (x0 + spread + 46, 66),
                        (x0 + spread - 46, 66),
                    ],
                    0.045,
                )
            )
    for cx, hw, h in ((100, 34, 150), (268, 30, 196), (458, 34, 176), (630, 38, 140)):
        far = [
            (cx - hw, gy),
            (cx - hw, gy - h * 0.6),
            (cx - hw * 0.6, gy - h * 0.6),
            (cx - hw * 0.6, gy - h * 0.86),
            (cx - hw * 0.25, gy - h * 0.86),
            (cx - hw * 0.25, gy - h),
        ]
        b.append(tone(far + [(2 * cx - x, y) for x, y in far[::-1]], 0.1))
    b.append(ground(gy))
    b.append(
        _setback(
            184,
            gy,
            [(64, 48), (50, 84), (38, 138), (27, 186), (16, 210), (7, 224)],
            0.94,
        )
    )
    b.append(
        _setback(540, gy, [(60, 44), (47, 80), (35, 130), (24, 166), (13, 190)], 0.92)
    )
    main = [
        (88.0, 52.0),
        (70, 92),
        (54, 150),
        (40, 212),
        (27, 246),
        (15, 262),
        (7, 270),
    ]
    b.append(_setback(360, gy, main, s / 0.86))
    top = gy - 305 * s
    b.append(poly([(356, gy - 270), (360, top), (364, gy - 270)], 1.0, PAPER))
    for x in range(44, 108, 13):
        b.append(
            rect(x, gy - 20 - (x % 3) * 3, 11, 20 + (x % 3) * 3, 0.6, PAPER, FAINT)
        )
    b.append(line(364, top, 646, top, 0.4, FAINT, dash="2 4"))
    b.append(dim_v(650, top, gy, "305 m — 1,000 ft"))
    b.append(note(52, 180, "1920s street wall, to scale", (74, gy - 24)))
    b.append(note(596, 96, "Searchlights", (454, 150)))
    write(
        "ferriss",
        "The Metropolis of Tomorrow — Ferriss, 1929",
        "elevation",
        "the business centre",
        "".join(b),
    )


ALL = [tatlin, ferriss]
