"""Part VIII — late phantoms."""

from __future__ import annotations

import math

from .kit import (
    EIFFEL,
    FAINT,
    INK,
    PAPER,
    Pt,
    circle,
    dim_v,
    ground,
    hatch,
    line,
    n,
    note,
    path,
    person,
    poly,
    rect,
    reference,
    tone,
    water,
    write,
)  # fmt: skip

GIZA: list[Pt] = [(0, 115), (139, 0)]


def mega_city_pyramid() -> None:
    """Shimizu's TRY 2004: a truss of tubes and node-spheres, towers hung inside."""
    cx, gy, s = 360.0, 428.0, 0.178
    h, half, tiers = 2004 * s, 1400 * s, 8
    top, step, rise = gy - h, 2 * half / tiers, h / tiers
    b = [water(gy, 36, 684, 2)]

    def node(i: int, j: int) -> Pt:
        return (cx + (j - i / 2) * step, top + i * rise)

    # struts on the far faces
    for i in range(tiers - 1):
        for j in range(i + 1):
            b.append(line(*node(i, j), *node(i + 2, j + 1), 0.4, FAINT))
    # skyscrapers standing inside each cell
    for i in range(2, tiers):
        for j in range(i + 1):
            ax, ay = node(i, j)
            for f in (-0.27, 0.0, 0.27):
                ht = rise * (1 - 2 * abs(f)) * 0.62
                b.append(
                    rect(
                        ax + f * step - 1.7, ay + rise - ht - 2, 3.4, ht, 0, INK, o=0.55
                    )
                )
    edges = []
    for i in range(tiers):
        for j in range(i + 1):
            edges += [
                (node(i, j), node(i + 1, j)),
                (node(i, j), node(i + 1, j + 1)),
                (node(i + 1, j), node(i + 1, j + 1)),
            ]
    for wt, col in ((3.4, INK), (1.9, PAPER)):
        for p, q in edges:
            b.append(line(*p, *q, wt, col))
    for i in range(tiers + 1):
        for j in range(i + 1):
            b.append(circle(*node(i, j), 4.4, 1.0, PAPER))
    for j in range(tiers + 1):
        x = node(tiers, j)[0]
        b.append(line(x, gy + 4, x, gy + 13, 1.2))

    b += [
        reference(64, gy, s, GIZA, "Great Pyramid", "139 m"),
        reference(655, gy, s, EIFFEL, "Eiffel", "330 m"),
        dim_v(626, top, gy, "2,004 m"),
        note(52, 96, "Node: a sphere where the tubes meet", node(3, 0)),
        note(52, 134, "Eight tiers, each 250 m", node(2, 0)),
        note(
            52,
            290,
            "Towers of 100 storeys",
            (node(6, 0)[0] + 3, node(6, 0)[1] + rise * 0.6),
        ),
        note(52, 299, "inside every cell"),
    ]
    write(
        "mega-city-pyramid",
        "Mega-City Pyramid / TRY 2004 — Shimizu, 1989",
        "elevation",
        "Tokyo Bay",
        "".join(b),
    )


def cardiff_opera() -> None:
    """Hadid's opera house: a glazed perimeter block, strung with tilted volumes."""
    gy = 432.0
    b = [ground(gy)]

    # the auditorium, a faceted solid rising behind the perimeter block
    r1, r2 = (300.0, 262.0), (372.0, 268.0)
    crystal = [(196, 372), (176, 292), (238, 214), (352, 188), (428, 236), (452, 360)]
    fly = [(288, 208), (300, 150), (350, 158), (346, 190)]
    b += [
        poly(fly, 1.2, PAPER),
        hatch([(330, 155), (350, 158), (346, 190), (328, 196)], 2.8, 62, o=0.45),
        poly(crystal, 1.6, PAPER),
        tone([(176, 292), r1, (262, 368), (196, 372)], 0.12),
        hatch([(352, 188), (428, 236), r2], 3, 62, o=0.45),
        hatch([(428, 236), (452, 360), (400, 362), r2], 2.4, 62, o=0.55),
        tone([r1, r2, (400, 362), (262, 368)], 0.05),
    ]
    for p, q in (
        ((238, 214), r1),
        ((176, 292), r1),
        (r1, (262, 368)),
        (r1, r2),
        ((352, 188), r2),
        ((428, 236), r2),
        (r2, (400, 362)),
        ((352, 188), r1),
    ):
        b.append(line(*p, *q, 0.8))

    # rehearsal volumes, tipped against the block
    for shape, ang in (
        ([(104, 380), (140, 330), (192, 346), (168, 404)], 62),
        ([(468, 300), (522, 286), (536, 356), (486, 364)], 118),
    ):
        b += [poly(shape, 1.2, PAPER), hatch(shape, 3, ang, o=0.4)]

    # the perimeter block: "the necklace"
    bar = [(86, 372), (560, 350), (560, 392), (86, 404)]
    b += [poly(bar, 1.4, PAPER), tone(bar, 0.06)]
    for i in range(1, 68):
        x = 86 + i * 7
        t = (x - 86) / 474
        b.append(line(x, 372 - 22 * t + 2, x - 2, 404 - 12 * t - 2, 0.35))
    b.append(line(86, 388, 560, 371, 0.6))
    plinth = [(86, 404), (300, 398.6), (300, gy), (86, gy)]
    b += [poly(plinth, 1.2, PAPER), hatch(plinth, 3.4, 0, o=0.4)]
    for x in range(326, 560, 34):
        t = (x - 86) / 474
        b.append(line(x, 404 - 12 * t, x + 7, gy, 1.2))
        b.append(line(x + 14, 404 - 12 * t, x + 7, gy, 1.2))

    # the cantilevered prow
    prow = [(506, 352.5), (670, 318), (560, 392)]
    b += [
        poly(prow, 1.6, PAPER),
        hatch([(560, 392), (670, 318), (556, 366)], 2.4, 20, o=0.5),
    ]
    b.append(line(506, 352.5, 556, 366, 0.7))
    for x, y in (
        (470, gy),
        (498, gy),
        (506, gy),
        (548, gy),
        (590, gy),
        (598, gy),
        (634, gy),
        (662, gy),
        (60, gy),
        (348, gy),
        (420, gy),
    ):
        b.append(person(x, y, 7.5))
    b += [
        note(52, 96, "Auditorium, 1,900 seats: the jewel", (250, 232)),
        note(52, 134, "Fly tower", (296, 172)),
        note(470, 96, "Cantilevered prow", (640, 330)),
        note(470, 134, "Glazed perimeter block: the necklace", (520, 366)),
    ]
    write(
        "cardiff-opera",
        "Cardiff Bay Opera House — Zaha Hadid, 1994",
        "elevation",
        "competition scheme",
        "".join(b),
    )


def crystal_island() -> None:
    """Foster's tent for Moscow: one skin, wound from two spirals of steel."""
    cx, gy, s = 356.0, 432.0, 0.66
    h, base = 450 * s, 231.0

    def hw(z: float) -> float:
        t = z / h
        return base * (1 - t) ** 1.9 + 2.5 * (1 - t)

    b = [ground(gy)]
    k = 60
    zs = [h * i / k for i in range(k + 1)]
    b.append(
        poly(
            [(cx - hw(z), gy - z) for z in zs]
            + [(cx + hw(z), gy - z) for z in zs[::-1]],
            0,
            PAPER,
        )
    )
    b.append(
        hatch(
            [(cx + hw(z) * 0.5, gy - z) for z in zs]
            + [(cx + hw(z), gy - z) for z in zs[::-1]],
            3,
            62,
            o=0.4,
        )
    )
    d = ""
    for turn in (1, -1):
        for j in range(26):
            run = False
            for z in zs[:-1]:
                phi = math.tau * j / 26 + turn * 2.5 * z / h
                if math.cos(phi) > 0:
                    d += f"{'L' if run else 'M'}{n(cx + hw(z) * math.sin(phi))},{n(gy - z)}"
                    run = True
                else:
                    run = False
    b.append(path(d, 0.4, o=0.75))
    for i in range(1, 9):
        z = h * i / 9.6
        b.append(
            path(
                f"M{n(cx - hw(z))},{n(gy - z)}Q{cx},{n(gy - z + 0.12 * hw(z))} {n(cx + hw(z))},{n(gy - z)}",
                0.3,
                o=0.7,
            )
        )
    b.append(
        poly(
            [(cx - hw(z), gy - z) for z in zs]
            + [(cx + hw(z), gy - z) for z in zs[::-1]],
            1.6,
        )
    )
    b.append(line(cx, gy - h, cx, gy - h - 9, 0.9))
    for i in range(-11, 12):
        x = cx + i * 22
        if abs(i) > 1:
            b.append(line(x, gy, x, gy - 4, 0.5))
            b.append(circle(x, gy - 6.5, 3.2, 0.6, PAPER))
    b.append(
        tone(
            [(cx - 16, gy), (cx - 16, gy - 12), (cx + 16, gy - 12), (cx + 16, gy)], 0.6
        )
    )
    b += [
        reference(644, gy, s, EIFFEL, "Eiffel Tower", "330 m"),
        dim_v(46, gy - h, gy, "450 m"),
        note(52, 96, "Vented at the apex", (cx - 3, gy - h + 4)),
        note(52, 134, "Diagrid wound as two", (cx - 46, gy - 150)),
        note(52, 143, "opposed spirals"),
        note(470, 96, "2.5 million m² under one skin", (cx + 60, gy - 96)),
    ]
    write(
        "crystal-island",
        "Crystal Island — Foster + Partners, 2007",
        "elevation",
        "Moscow",
        "".join(b),
    )


ALL = [mega_city_pyramid, cardiff_opera, crystal_island]
